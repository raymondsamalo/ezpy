import shutil

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

from pool_executor import PoolExecutor
def make_empty_file(fname: str, total_length: int):
    """ This function create an empty file and fill it with 0 of total_length bytes """
    expected = total_length
    length = 8192
    with open(fname, 'wb') as stream:
        while expected > 0:
            if expected < length:
                length = expected
            stream.write(bytes('\0' * length, 'utf-8'))
            expected -= length
          
          import os


DEFAULT_TIMEOUT = 5  # seconds
MULTIPART_MAX_THREADING = 10
MULTIPART_CHUNK_SIZE = 10_000_000

def api_create_client():  # pragma: no cover
    """ factory method to create fully configured requests session """
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=2
    )
    client = requests.session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    client.mount("https://", adapter)
    client.mount("http://", adapter)
    return client


class Downloader:
    """
    This class handle downloading from a url to file
    """
    def __init__(self, client_creator=api_create_client) -> None:
        self.client = client_creator()

    def get(self, url: str, headers: dict = None, params: dict = None, timeout: int = None, #pylint: disable=too-many-arguments
            stream: bool = False) -> requests.Response:
        """ perform GET request """
        if timeout is None:
            timeout = DEFAULT_TIMEOUT
        return self.client.get(url=url, headers=headers, params=params,
                               timeout=timeout, stream=stream)

    def _download_url(self, url: str, target_path: str) -> None:
        with self.get(url, stream=True) as stream:
            with open(target_path, "wb") as file:
                shutil.copyfileobj(stream.raw, file)

    def download_url(self, url: str, target_path: str) -> None:
        """ Stream download a file from a URL to a local file. """
        temp_path = target_path + '.downloading'
        try:
            if os.path.exists(target_path):
                os.remove(target_path)
            self._download_url(url, temp_path)
            os.rename(temp_path, target_path)
        except (Exception, KeyboardInterrupt) as exception:
            os.remove(temp_path)
            raise exception


class MultiPartDownloader(Downloader):
    """
    This class handle downloading from a url to file
    utilizing http range header to download in parallel
    """
    def _get_length(self, url: str) -> int:
        length = 0
        with self.get(url, stream=True) as stream:
            length = int(stream.headers['Content-length'])
            stream.close()
        return length

    def _download_url_chunk(self, url: str, target_path: str, start: int, end: int) -> None:
        headers = {'Range': 'bytes=%d-%d' % (start, end)}
        response = self.get(url, headers=headers, stream=True)
        with open(target_path, 'r+b') as stream:
            stream.seek(start)
            stream.write(response.content)

    def _download_url(self, url: str, target_path: str) -> None:
        total_length = self._get_length(url)
        # create file
        make_empty_file(target_path, total_length)
        length = MULTIPART_CHUNK_SIZE  # 200 MB per thread
        start = 0
        end = 0
        with PoolExecutor(MULTIPART_MAX_THREADING) as pool:
            while end < total_length:
                start = end
                end += length
                if end > total_length:
                    end = total_length
                pool.submit(self._download_url_chunk,
                            url, target_path, start, end-1)
            
