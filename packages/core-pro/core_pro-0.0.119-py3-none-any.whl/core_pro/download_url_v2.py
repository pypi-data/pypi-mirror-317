import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from io import BytesIO
from typing import List, Tuple, Optional
from functools import partial
from rich import print
from tqdm.auto import tqdm
from tenacity import retry, stop_after_attempt, wait_exponential
from PIL import Image, ImageFile
import httpx
from time import sleep, time
import certifi

ImageFile.LOAD_TRUNCATED_IMAGES = True


class RetryableHTTPTransport(httpx.HTTPTransport):
    def handle_request(self, request):
        for _ in range(3):  # Try up to 3 times
            try:
                return super().handle_request(request)
            except (httpx.ConnectTimeout, httpx.ReadTimeout) as e:
                if _ == 2:  # Last attempt
                    raise e
                sleep(1 * (_ + 1))  # Progressive delay


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry_error_callback=lambda retry_state: None
)
def httpx_fetch(url: str, timeout: float = 30.0):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "image/webp,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    transport = RetryableHTTPTransport()

    limits = httpx.Limits(
        max_keepalive_connections=5,
        max_connections=10,
        keepalive_expiry=30.0
    )

    try:
        with httpx.Client(
                verify=certifi.where(),
                headers=headers,
                follow_redirects=True,
                timeout=timeout,
                transport=transport,
                limits=limits
        ) as client:
            response = client.get(url)
            response.raise_for_status()
            return response

    except httpx.HTTPError as e:
        print(f"HTTP Error for {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error downloading {url}: {str(e)}")
        return None


def download_and_process_image(
    data: Tuple[int, str],
    output_dir: str,
    timeout: int = 10,
    resize_size: Optional[Tuple[int, int]] = None,
) -> bool:
    """Download and process a single image."""
    idx, url = data
    try:
        # Skip if already downloaded
        output_path = Path(output_dir) / f'{idx}.jpg'
        if output_path.exists():
            print(f"Skipping existing image: {output_path.stem}")
            return True

        # Download image
        # response = requests.get(url, timeout=timeout)
        response = httpx_fetch(url)

        # Open and validate image
        img = Image.open(BytesIO(response.content))
        if img.mode != "RGB":
            img = img.convert("RGB")
        if resize_size:
            img = img.resize(resize_size, Image.Resampling.LANCZOS)

        # Save image
        img.save(output_path, "JPEG")
        return True

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return False


def process_batch(
    urls: List[str],
    output_dir: str,
    threads: int,
    timeout: int,
    resize_size: Optional[Tuple[int, int]] = None,
) -> List[bool]:
    """Process a batch of URLs using threads."""
    download_func = partial(
        download_and_process_image,
        output_dir=output_dir,
        timeout=timeout,
        resize_size=resize_size,
    )

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(tqdm(executor.map(download_func, urls), total=len(urls)))
    return results


class ImageDownloader:
    def __init__(
        self,
        output_dir: Path,
        num_processes: int = 4,
        threads_per_process: int = 4,
        timeout: int = 10,
        resize_size: Optional[Tuple[int, int]] = None,
    ):
        self.output_dir = output_dir
        self.output_dir.mkdir(exist_ok=True)
        self.num_processes = num_processes
        self.threads_per_process = threads_per_process
        self.timeout = timeout
        self.resize_size = resize_size

    def download_images(self, data: List[Tuple[int, str]]) -> Tuple[int, int]:
        """Download images using multiple processes and threads."""
        start_time = time()
        total_urls = len(data)
        print(f'[green]START[/] {total_urls} images {self.num_processes} threads, {self.num_processes} processes')

        # Split URLs into chunks for each process
        chunk_size = total_urls // self.num_processes + (1 if total_urls % self.num_processes else 0)
        url_chunks = [
            data[i : i + chunk_size] for i in range(0, total_urls, chunk_size)
        ]

        # Create partial function with fixed parameters
        process_func = partial(
            process_batch,
            output_dir=str(self.output_dir),
            threads=self.threads_per_process,
            timeout=self.timeout,
            resize_size=self.resize_size,
        )

        # Process URLs using multiple processes
        with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
            results = list(executor.map(process_func, url_chunks))

        # Flatten results and count successes
        flat_results = [item for sublist in results for item in sublist]
        successful = sum(flat_results)

        elapsed_time = time() - start_time
        print(f'[green]DOWNLOADED[/] {successful}/{total_urls} images in {elapsed_time:.2f} seconds')

        return successful, total_urls


# Example usage
# if __name__ == "__main__":
#     import polars as pl
#     from core_pro.ultilities import make_sync_folder
#
#     path = make_sync_folder("item_match/scs")
#     path_image = path / "img"
#     shp = pl.read_parquet(path / "shp.parquet").with_row_index()
#     sample_urls = shp[['index', 'image_url_1']].to_numpy().tolist()[:1000]
#     # Initialize downloader
#     downloader = ImageDownloader(
#         output_dir=Path("/media/kevin/data_4t/test"),
#         num_processes=4,
#         threads_per_process=4,
#         resize_size=(224, 224),
#     )
#
#     # Download images
#     successful, total = downloader.download_images(sample_urls)
