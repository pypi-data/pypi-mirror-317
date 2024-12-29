"""
web crawler library
===================

Contains a few nice-to-haves as far as web crawling goes; still in early development
"""
import json
import logging
from pathlib import Path
from time import sleep, time

import bs4
import urllib3

from .path_tools import find_available_path, make_FS_safe


class WebRequestEngine:
    """Handles everything having to do with request execution"""

    last_request_time: float
    """Internal use; timestamp of last request time"""
    pool_manager: urllib3.PoolManager
    """Executes requests"""
    log: logging.Logger
    """Logs messages"""
    wait_time_after_request_s: float
    """Minimum wait time between requests, in seconds"""
    cache_dir: Path
    """Where cached request responses' contents are saved"""
    bad_request_cache: dict[str, int]
    """In-memory cache of bad request file content; dictionnary of bad urls and their expiration time as an epoch timestamp"""

    def __init__(
        self,
        cache_dir: Path,
        wait_time_after_request_s: float = 0.1,
        log: logging.Logger | None = None,
    ) -> None:
        self.last_request_time = 0.0
        self.pool_manager = urllib3.PoolManager()
        # log
        self.log = logging.getLogger(__file__) if log is None else log
        # cache_dir
        if cache_dir is None or not isinstance(cache_dir, Path):
            raise ValueError(f"Only non-null Path instances are accepted: {cache_dir=}")
        if not cache_dir.exists():
            self.log.info("Creating cache directory %s", cache_dir)
            cache_dir.mkdir(parents=True)
        self.cache_dir = cache_dir
        # wait_time_after_request_s
        if wait_time_after_request_s < 0:
            raise ValueError(
                f"Only non-negative wait time values are accepted: {wait_time_after_request_s=}"
            )
        self.wait_time_after_request_s = wait_time_after_request_s
        self.__reload_bad_request_cache()

    @property
    def bad_request_file(self) -> Path:
        """Returns the path of the 'bad request cache' file"""
        return self.cache_dir / "bad-requests.json"

    def __reload_bad_request_cache(self) -> None:
        """Ensures bad request file exists and reloads it into cache"""
        bad_request_file = self.bad_request_file
        bad_request_file.touch()
        file_contents = bad_request_file.read_text(encoding="utf-8")
        self.bad_request_cache = json.loads(file_contents) if file_contents else {}

    def __persist_bad_request_cache(self) -> None:
        """Persist bad request cache into file"""
        # First, filter bad request cache to remove deprecated items
        _now = time()
        self.bad_request_cache = {
            url: end_timestamp
            for url, end_timestamp in self.bad_request_cache.items()
            if end_timestamp > _now or end_timestamp == 0
        }
        # Then, persist cache into file
        self.bad_request_file.write_text(
            json.dumps(self.bad_request_cache, ensure_ascii=False), encoding="utf-8"
        )

    def cache_bad_request(self, url: str, end_time: int) -> None:
        """Registers a bad request in cache and persists it to file"""
        self.log.debug(
            "Caching bad request for url '%s' with end timestamp %s", url, end_time
        )
        self.bad_request_cache[url] = end_time
        self.__persist_bad_request_cache()

    def is_a_cached_bad_request(self, url: str, _now: float) -> bool:
        """Check if a url is a cached bad request"""
        bad_request_cache_end_time = self.bad_request_cache.get(url)
        if bad_request_cache_end_time is None:
            return False

        if bad_request_cache_end_time == 0 or bad_request_cache_end_time > _now:
            self.log.debug("Cache hit: bad request for url '%s'", url)
            return True

        self.log.debug(
            "Removing cached bad request entry for url '%s': end time %s < curr time %.1f",
            url,
            bad_request_cache_end_time,
            _now,
        )
        del self.bad_request_cache[url]
        return False

    def request(self, method, url, fields=None, headers=None, **urlopen_kw):
        """Perform request; see urllib3.PoolManager.request
        Implements delay set by `wait_time_after_request_s`
        """
        if (
            diff := (self.last_request_time + self.wait_time_after_request_s) - time()
        ) > 0:
            self.log.debug("Sleeping for %0.1fs before next request", diff)
            sleep(diff)
        self.last_request_time = time()
        return self.pool_manager.request(method, url, fields, headers, **urlopen_kw)

    def get_html(
        self,
        url: str,
    ) -> str:
        """Get HTML content from URL; for cached requests see `cache_and_get_html`"""
        self.log.debug("[GET] html at %s", url)
        response: urllib3.response.HTTPResponse = self.request("GET", url)
        if response.status == 200:
            return response.data.decode(encoding="utf8")
        raise ValueError(f"Return status is {response.status}")

    def get_cache_file(self, url: str, suffix: str) -> Path:
        """Return cache file path for given url and file suffix"""
        return (
            self.cache_dir
            / f"{make_FS_safe(url, mode='utf-replace', len_limit=150)}{suffix}"
        )

    def cache_and_get_html(self, url: str, cache_duration_s: int | float = 0, bad_request_cache_duration_s: int | float = 0) -> str:
        """caches to file the first time and retrieves from it next times; cache
        can be invalidated after some time using `cache_duration_s` :
         - positive value: cache file is updated after at least the given time has passed
         - 0: never update the cache file
         - negative value: cache file is always updated
        WARNING: the default value of 0 means file is never updated. If you want it to always be updated, use a negative value
        `bad_request_cache_duration_s`: positive values makes the bad request expire, negative/zero makes it permanent
        """
        html_file = self.get_cache_file(url, suffix=".html")
        file_exists = html_file.exists()
        do_download = not file_exists
        self.log.debug("Cache hit: %s", not do_download)
        _now = time()

        # Check if this is a known bad request
        if do_download and self.is_a_cached_bad_request(url, _now):
            self.log.debug("Known bad url: %s", url)
            raise ValueError("Invalid url")
        # Cache invalidation
        elif file_exists and cache_duration_s < 0:
            self.log.info("Cache invalidation: always update")
            html_file.unlink()
            do_download = True
        elif (
            file_exists
            and cache_duration_s > 0
            and (
                cached_file_age := _now
                - max(html_file.stat().st_mtime, html_file.stat().st_ctime)
            ) > cache_duration_s
        ):
            self.log.info(
                "Cache invalidation: cached file too old: %.0f > %s",
                cached_file_age,
                cache_duration_s,
            )
            html_file.unlink()
            do_download = True

        # Caching
        if do_download:
            self.log.debug("Will download html file at url '%s'", url)
            try:
                html_file.write_text(self.get_html(url), encoding="utf8")
            except ValueError as e:
                self.cache_bad_request(
                    url, int(_now) + bad_request_cache_duration_s if bad_request_cache_duration_s > 0 else 0
                )
                raise e

        return html_file.read_text(encoding="utf8")

    def get_img(self, url: str) -> bytes:
        """Get image content from URL"""
        self.log.debug("[GET] image at %s", url)
        response: urllib3.response.HTTPResponse = self.request("GET", url)
        if response.status == 200:
            return response.data
        raise ValueError(f"Return status is {response.status}")

    def cache_and_download_image(
        self,
        img_url: str,
        destination_dir: Path,
        override_name: str | None = None,
    ) -> Path:
        """download image to file if not exists already; returns file"""
        self.log.debug("Trying to cache and download img from url '%s'", img_url)

        # cache file
        img_cache_file = self.get_cache_file(img_url, Path(img_url).suffix)
        self.log.debug("Cache hit: %s", img_cache_file.exists())
        if not img_cache_file.exists():
            img_cache_file.write_bytes(self.get_img(img_url))

        # determine destination file path and whether it exists or needs to be written
        file_name = (
            Path(img_url).name
            if override_name is None
            else (override_name + img_cache_file.suffix)
        )
        target_file = destination_dir / file_name
        if target_file.exists():
            if img_cache_file.read_bytes() != target_file.read_bytes():
                target_file = find_available_path(destination_dir, file_name)
                self.log.warning(
                    "Target file has different contents, changing name from '%s' to '%s'",
                    file_name,
                    target_file.name,
                )
            else:
                return target_file

        # copy cache to target file
        target_file.write_bytes(img_cache_file.read_bytes())
        return target_file


class TagNotFoundError(Exception):
    pass


def get_unique_page_subpart(
    article: bs4.BeautifulSoup,
    tag: str,
    tag_class: str | None = None,
    dont_throw: bool = False,
) -> bs4.Tag | None:
    """Dumb method that either finds and return expected part or raises exception"""
    _found: bs4.ResultSet = article.findAll(
        tag, attrs={"class": tag_class} if tag_class else None
    )
    if len(_found) != 1:
        if dont_throw:
            return None
        raise ValueError(
            f"Searched for {tag} tag with class {tag_class}; Found: {_found}"
        )
    return _found[0]


def get_unique_text(
    article: bs4.BeautifulSoup, tag: str, tag_class: str, dont_throw: bool = False
) -> str | None:
    """Dumb method that either finds and return expected text or raises exception"""
    found_tag = get_unique_page_subpart(article, tag, tag_class, dont_throw)
    if found_tag is None:
        if dont_throw:
            return None
        raise TagNotFoundError()
    return found_tag.get_text().strip()
