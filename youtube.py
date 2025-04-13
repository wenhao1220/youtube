import streamlit as st
import yt_dlp
import os

st.title("🎬 YouTube 下載器（可下載到本機）")

# 使用者輸入 YouTube 連結
url = st.text_input("請輸入 YouTube 網址：")

# 儲存檔案的變數
video_file = None
audio_file = None

# 定義下載影片的函數
def download_video(url):
    info = yt_dlp.YoutubeDL().extract_info(url, download=False)
    title = info.get("title", "video")
    filename = f"{title}.mp4"
    ydl_opts = {
        'format': 'best',
        'outtmpl': filename,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename

# 定義下載音訊（不使用 ffmpeg）
def download_audio_no_ffmpeg(url):
    info = yt_dlp.YoutubeDL().extract_info(url, download=False)
    title = info.get("title", "audio")
    filename = f"{title}.webm"  # 不轉 mp3，直接下載原始音訊格式（多為 webm）
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename

# 建立兩個按鈕：下載 MP4 / 音訊
col1, col2 = st.columns(2)

with col1:
    if st.button("⬇️ 下載 MP4"):
        if url:
            with st.spinner("下載中...請稍候"):
                video_file = download_video(url)
            with open(video_file, "rb") as f:
                st.download_button(
                    label="✅ 點我下載影片",
                    data=f,
                    file_name=video_file,
                    mime="video/mp4"
                )
        else:
            st.warning("請輸入影片網址")

with col2:
    if st.button("🎵 下載音訊（原始格式）"):
        if url:
            with st.spinner("下載中...請稍候"):
                audio_file = download_audio_no_ffmpeg(url)
            with open(audio_file, "rb") as f:
                st.download_button(
                    label="✅ 點我下載音訊",
                    data=f,
                    file_name=audio_file,
                    mime="audio/webm"
                )
        else:
            st.warning("請輸入影片網址")
