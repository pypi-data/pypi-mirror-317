from pathlib import Path
import pandas as pd
import polars as pl
from concurrent.futures import ThreadPoolExecutor
import trino
import os
from rich import print
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    SpinnerColumn
)
from datetime import datetime


class DataPipeLine:
    def __init__(
            self,
            query: str | Path,
            count_rows: bool = False,
    ):
        # config
        self.count_rows = count_rows
        self.query = self._process_query(query)
        self.filename = query.stem if isinstance(query, Path) else ''

        # status
        self.status = '[bright_blue]🤖 JDBC[/bright_blue]'
        self.status_query = f'{self.status} [bold green]QUERY[/]'
        self.status_fetch = f'{self.status} [bold green]FETCHING...[/]'
        self.status_done = f'{self.status} [bold green]DONE:[/]'

    def debug_query(self):
        print(self.query)

    def _process_query(self, query: str | Path) -> str:
        if isinstance(query, Path):
            with open(str(query), 'r') as f:
                text_query = f.read()
        text_query = f"SELECT COUNT(*) FROM ({query})" if self.count_rows else text_query
        return text_query

    def _time(self) -> str:
        return f'[orange1]{datetime.now().strftime('%H:%M:%S')}[/]'

    def _records_to_df(self, records, columns: list, save_path: Path):
        # records to df
        try:
            df = pl.DataFrame(records, orient='row', schema=columns)
        except (pl.exceptions.ComputeError, TypeError) as e:
            print(f'{self.status} Errors on Polars, switch to Pandas: {e}')
            df = pd.DataFrame(records, columns=columns)

        # write
        if save_path:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(df, pl.DataFrame):
                df.write_parquet(save_path)
            else:
                df.to_parquet(save_path, index=False, compression='zstd')

        # message
        message = f"Data shape ({df.shape[0]:,.0f}, {df.shape[1]})"
        return message, df

    def _connection(self):
        username, password = os.environ['PRESTO_USER'], os.environ['PRESTO_PASSWORD']
        conn = trino.dbapi.connect(
            host='presto-secure.data-infra.shopee.io',
            port=443,
            user=username,
            catalog='hive',
            http_scheme='https',
            source=f'(50)-(vnbi-dev)-({username})-(jdbc)-({username})-(SG)',
            auth=trino.auth.BasicAuthentication(username, password)
        )
        return conn

    def _progress(self):
        query_progress = Progress(
            TextColumn("{task.description}"),
            SpinnerColumn("simpleDots"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            BarColumn(),
            SpinnerColumn("simpleDots"),
            transient=True
        )
        return query_progress

    def run_presto_to_df(
            self,
            save_path: Path = None,
            verbose: bool = True,
            overwrite: bool = True,
    ):
        # connection
        conn = self._connection()
        cur = conn.cursor()

        # check if overwrite
        if not overwrite:
            if save_path.exists():
                print(f"{self._time()} {self.status_done}: {save_path} is already exists")
                return None

        # run
        print(f"{self._time()} {self.status_query}: file name [{self.filename}], Count rows: [{self.count_rows}]")
        if verbose:
            # progress
            query_progress = self._progress()
            thread = ThreadPoolExecutor(1)

            async_result = thread.submit(cur.execute, self.query)
            task_id_query = query_progress.add_task("[cyan]Presto to Local", total=100)

            # query
            memory = 0
            with query_progress:
                while not async_result.done():
                    try:
                        memory = cur.stats.get('peakMemoryBytes', 0) * 10 ** -9
                        perc = 0
                        stt = cur.stats.get('state', 'Not Ready')
                        if stt == "RUNNING":
                            current = cur.stats.get('completedSplits', 1e-3) * 100.0
                            total = cur.stats.get('totalSplits', 0)
                            perc = round(current / total, 2)
                        status = f"{stt} - Memory {memory:,.0f}GB"
                        query_progress.update(task_id_query, description=status, advance=perc)
                    except ZeroDivisionError as e:
                        print(e)
                        continue
        else:
            cur.execute(self.query)

        print(f"{self._time()} {self.status_fetch} Memory {memory:,.0f}GB")
        try:
            # fetch
            records = cur.fetchall()
            # result
            columns = [i[0] for i in cur.description]
            text, df = self._records_to_df(records, columns, save_path)
            # update status
            print(f"{self._time()} {self.status_done} {text}")
            return df
        except AssertionError as e:
            print(e)
