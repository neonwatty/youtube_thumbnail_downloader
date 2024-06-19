from youtube_thumbnail_downloader.fetch import get_yt_thumbnail_url
from youtube_thumbnail_downloader.download import download_thumbnail
from typing import Tuple


def fetch_yt_thumbnail(youtube_url: str,
                       savedir: str) -> Tuple[str, str, str]:
    try:
        yt_title, yt_thumbnail_url = get_yt_thumbnail_url(youtube_url)
        yt_thumbnail_savepath = download_thumbnail(yt_thumbnail_url, 
                                                   yt_title,
                                                   savedir)
        return yt_title, yt_thumbnail_savepath, yt_thumbnail_url
    except:
        return None, None, None
    
    
def batch_fetch_yt_thumbnails(youtube_urls: list,
                              savedir: str) -> Tuple[list, list]:
    yt_save_data = []
    yt_thumbnail_savepaths = []
    for youtube_url in youtube_urls:
        yt_title, yt_thumbnail_savepath, yt_thumbnail_url = fetch_yt_thumbnail(youtube_url, 
                                                                               savedir)
        if yt_title is not None:
            entry = {}
            entry["video_url"] = youtube_url
            entry["title"] = yt_title
            entry["thumbnail_url"] = yt_thumbnail_url
            yt_save_data.append(entry)
            
            yt_thumbnail_savepaths.append(yt_thumbnail_savepath)
    return yt_save_data, yt_thumbnail_savepaths
