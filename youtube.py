import streamlit as st
import yt_dlp
import os

st.title("🎬 YouTube 下載器")

# 使用者輸入 YouTube 連結
url = st.text_input("請輸入 YouTube 網址：")

# 正確通關密語
CORRECT_PASSWORD = "李文豪好帥"

# 狀態儲存用 session_state
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'password_verified' not in st.session_state:
    st.session_state.password_verified = False

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
    filename = f"{title}.webm"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename

# 按鈕：使用者選擇要下載哪一種格式
col1, col2 = st.columns(2)
with col1:
    if st.button("⬇️ 下載 MP4"):
        if url:
            st.session_state.mode = "video"
            st.session_state.password_verified = False
        else:
            st.warning("⚠️ 請先輸入影片網址")

with col2:
    if st.button("🎵 下載音訊"):
        if url:
            st.session_state.mode = "audio"
            st.session_state.password_verified = False
        else:
            st.warning("⚠️ 請先輸入影片網址")

# 若有選擇下載模式，則顯示密碼輸入欄位
if st.session_state.mode and not st.session_state.password_verified:
    password = st.text_input("🔐 請輸入通關密語以繼續下載")
    if st.button("確認密語"):
        if password == CORRECT_PASSWORD:
            st.session_state.password_verified = True
            st.success("✅ 密語正確，可以開始下載")
        else:
            st.error("❌ 密語錯誤，請再試一次")

# 密碼正確後執行下載
if st.session_state.password_verified:
    with st.spinner("下載中...請稍候"):
        if st.session_state.mode == "video":
            video_file = download_video(url)
            with open(video_file, "rb") as f:
                st.download_button(
                    label="✅ 點我下載影片",
                    data=f,
                    file_name=video_file,
                    mime="video/mp4"
                )
        elif st.session_state.mode == "audio":
            audio_file = download_audio_no_ffmpeg(url)
            with open(audio_file, "rb") as f:
                st.download_button(
                    label="✅ 點我下載音訊",
                    data=f,
                    file_name=audio_file,
                    mime="audio/webm"
                )
