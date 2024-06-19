from typing import Tuple
from pytube import YouTube
import re


def is_valid_youtube_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    pattern = r"^https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    if "shorts" in url:
        pattern = r"^https://www\.youtube\.com/shorts/[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    return re.match(pattern, url) is not None


def get_yt_thumbnail_url(
    url: str, my_proxies: dict = {}
) -> Tuple[str, str]:
    try:
        # validate url
        if is_valid_youtube_url(url):
            # load in video
            yt = YouTube(url, proxies=my_proxies)

            # get title and thumbnail
            yt_title = yt.title
            yt_thumbnail_url = yt.thumbnail_url

            return (
                yt_title,
                yt_thumbnail_url
            )
        else:
            raise ValueError(f"invalid input url: {url}")
    except Exception as e:
        raise ValueError(f"get_yt_thumbnail_url failed with exception {e}")
