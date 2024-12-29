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

ImageFile.LOAD_TRUNCATED_IMAGES = True


def httpx_fetch(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "image/webp,image/*,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    try:
        # Configure client with appropriate SSL settings
        client = httpx.Client(
            verify=certifi.where(),
            headers=headers,
            follow_redirects=True,
            timeout=30.0
        )

        response = client.get(url)
        response.raise_for_status()
        return response

    except Exception as e:
        print(f"Error downloading image: {e}")
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
        response = httpx_fetch(url)
        if not response:
            return {'index': idx, 'url': url, 'status': 'error'}

        # Process
        img = self._process_image(response)

        # Save results
        self._save_results(idx, url, img)

    def process_batch(self, urls: list):
        """Process a batch of images, optionally using threads."""
        if self.max_workers:
            with ThreadPoolExecutor(self.max_workers) as executor:
                results = list(tqdm(executor.map(self.process_single, urls), total=len(urls)))
        else:
            results = [
                self.process_single(url_data)
                for url_data in tqdm(urls, description='Downloading images single thread')
            ]

        return results
