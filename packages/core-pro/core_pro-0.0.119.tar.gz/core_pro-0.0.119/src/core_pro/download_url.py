from io import BytesIO
from PIL import Image, UnidentifiedImageError, ImageFile
from rich import print
from typing import Tuple, Optional
from pathlib import Path
import orjson
import httpx
from concurrent.futures import ThreadPoolExecutor
import certifi
from tqdm import tqdm
from time import sleep
from tenacity import retry, stop_after_attempt, wait_exponential

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


class DownloadImage:
    def __init__(
            self,
            resize: Tuple[int, int] = (224, 224),
            path: Path = None,
            max_workers: int = None,
    ):
        self.resize = resize
        self.path = path
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        self.status = 'success'
        self.max_workers = max_workers

    def _process_image(self, response):
        """Process image data into PIL Image."""
        try:
            return (
                Image.open(BytesIO(response.content))
                .convert('RGB')
                .resize(self.resize, Image.Resampling.LANCZOS)
            )
        except UnidentifiedImageError as e:
            print(f"Error processing image: {str(e)}")
            return None

    def _save_results(self, idx: int, url: str, img: Optional[Image.Image]) -> None:
        status = 'success' if img else 'error'

        # Save image if successful
        if img:
            img.save(self.path / f'{idx}.jpg')

        # Save metadata
        json_path = self.path / f'{idx}.json'
        json_dict = {'index': idx, 'url': url, 'status': status}
        json_object = orjson.dumps(json_dict, option=orjson.OPT_INDENT_2).decode("utf-8")
        with open(json_path, 'w') as outfile:
            outfile.write(json_object)

    def process_single(self, data):
        idx, url = data

        # Download
        file_name = self.path / f'{idx}.jpg'
        if not file_name.exists():
            response = httpx_fetch(url)

            # Process
            img = self._process_image(response)

            # Save results
            self._save_results(idx, url, img)

    def process_batch(self, urls: list):
        """Process a batch of images, optionally using threads."""
        if self.max_workers:
            with ThreadPoolExecutor(self.max_workers) as executor:
                results = list(tqdm(
                    executor.map(self.process_single, urls),
                    total=len(urls),
                    desc='Downloading images multi thread'
                ))
        else:
            results = [
                self.process_single(url_data)
                for url_data in tqdm(urls, desc='Downloading images single thread')
            ]

        return results
