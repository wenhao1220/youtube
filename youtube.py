import streamlit as st
import yt_dlp

st.title("🎬 YouTube 下載器")

# 使用者輸入 YouTube 連結
url = st.text_input("請輸入 YouTube 網址：")

# 定義下載影片的函數
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',  # 檔名使用標題
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 定義下載音訊（不使用 ffmpeg）
def download_audio_no_ffmpeg(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 建立兩個按鈕：下載 MP4 / 音訊
col1, col2 = st.columns(2)

with col1:
    if st.button("⬇️ 下載 MP4"):
        if url:
            st.success("開始下載影片...")
            download_video(url)
            st.success("✅ 影片下載完成！")
        else:
            st.warning("請輸入影片網址")

with col2:
    if st.button("🎵 下載 MP3"):
        if url:
            st.success("開始下載音訊...")
            download_audio_no_ffmpeg(url)
            st.success("✅ 音訊下載完成！")
        else:
            st.warning("請輸入影片網址")
