import streamlit as st
import pandas as pd
from youtube_thumbnail_downloader.main import batch_fetch_yt_thumbnails
import tempfile

st.set_page_config(page_title="Youtube Thumbnail Downloader", layout="wide")
st.title("Youtube Thumbnail Downloader")
st.markdown(
    "instructions: enter in urls separated by commas or upload a text file with one url per line"
)


base = st.container(border=True)
with base:
    col1, sep_col, col2 = st.columns([5, 2, 5])
    
    with col1:
        text_urls = st.text_area("youtube urls", value="", placeholder="enter urls separated by commas - for example: https://www.youtube.com/shorts/o7a9hx-Pqyo, https://www.youtube.com/shorts/xkAYLnIsfX4")
    
    with col2:
        uploaded_file = st.file_uploader("Choose a File", type=["txt"])
        
    col3, col4, col5 = st.columns([3, 2, 3])
    with col3:
        fetch_button_val = st.button(label="fetch thumbnails", type="primary")
    with col4:
        empty_container = st.container()
    with col5:
        placeholder = st.empty()
        
download_area = st.container()


@st.cache_data
def convert_df(df: pd.DataFrame) -> "csv":
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def button_logic(youtube_urls: list) -> None:
    if fetch_button_val:
        with tempfile.TemporaryDirectory() as tmpdirname:
            yt_save_data, yt_thumbnail_savepaths = batch_fetch_yt_thumbnails(youtube_urls, tmpdirname)
            df = pd.DataFrame(yt_save_data)
            converted_dv = convert_df(df)

            # download metadata
            with download_area:
                st.download_button(
                    label="Download thumbnail metadata",
                    data=converted_dv,
                    file_name="output.csv",
                    mime="text/csv",
                    disabled=False,
                    type="primary",
                )
                
            # display images for download
            for ind, thumbnail_savepath in enumerate(yt_thumbnail_savepaths):
                title = yt_save_data[ind]["title"]
                thumbnail_url = yt_save_data[ind]["thumbnail_url"] 
                with st.container(border=True):
                    a, b, c = st.columns([1, 3, 1])
                    with b:
                        st.subheader(title)
                        st.image(thumbnail_savepath)


# default_file_path = main_dir + "/data/input/test_input.txt"
youtube_urls = []
if uploaded_file is not None:
    if text_urls is not None:
        st.warning("you can enter urls manually or from file but not both", icon="⚠️")
        st.stop()
    
    if uploaded_file.type == "text/plain":
        from io import StringIO

        stringio = StringIO(uploaded_file.read().decode("utf-8"))
        for line in stringio:
            youtube_urls.append(line.strip())

if text_urls is not None:
    if uploaded_file is not None:
        st.warning("you can enter urls manually or from file but not both", icon="⚠️")
        st.stop()
        
    try:
        text_urls_split = text_urls.split(",")
        text_urls_split = [v.strip() for v in text_urls_split]
        youtube_urls = text_urls_split
    except:
        st.warning("please check your manually entered urls", icon="⚠️") 
        st.stop()
    
    with st.spinner(text="thumbnail pull in progress..."):
        button_logic(youtube_urls)