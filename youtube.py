import streamlit as st
import yt_dlp
import subprocess
import os

st.title("🎬 YouTube 下載器")

# 使用者輸入 YouTube 網址
url = st.text_input("請輸入 YouTube 網址：")

# 初始化 session_state
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'full_file' not in st.session_state:
    st.session_state.full_file = None
if 'output_file' not in st.session_state:
    st.session_state.output_file = None
if 'download_mode' not in st.session_state:
    st.session_state.download_mode = "full"

# 下載影片
def download_full_video(url):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
            'proxy': None,  # 如果要加代理，這裡改成 'http://你的proxy:port'
            'noplaylist': True,
            'quiet': True,  # 不要印一堆log
            'retries': 3,  # 失敗自動重試3次
            'fragment_retries': 5,  # 分段失敗也重試
            'continuedl': True,  # 如果下載中斷，繼續下載
            'nocheckcertificate': True,  # 有些https驗證錯誤，跳過
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return filename
    except yt_dlp.utils.DownloadError:
        st.error("❌ 下載失敗，可能是連線問題或影片受限。建議稍後再試或更換代理伺服器。")
        st.stop()
    except Exception as e:
        st.error(f"❌ 發生錯誤：{str(e)}")
        st.stop()

# 下載音訊（不使用 ffmpeg）
def download_full_audio(url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'proxy': None,  # 如果要加代理，這裡改成 'http://你的proxy:port'
            'noplaylist': True,
            'quiet': True,
            'retries': 3,
            'fragment_retries': 5,
            'continuedl': True,
            'nocheckcertificate': True,
            'postprocessors': [],  # 不轉檔
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return filename
    except yt_dlp.utils.DownloadError:
        st.error("❌ 下載失敗，可能是連線問題或影片受限。建議稍後再試或更換代理伺服器。")
        st.stop()
    except Exception as e:
        st.error(f"❌ 發生錯誤：{str(e)}")
        st.stop()


# 裁切影片
def cut_video(input_file, output_file, start_time, end_time):
    command = [
        "ffmpeg", "-i", input_file,
        "-ss", start_time,
        "-to", end_time,
        "-c", "copy",
        output_file, "-y"
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# 裁切音訊
def cut_audio(input_file, output_file, start_time, end_time):
    command = [
        "ffmpeg", "-i", input_file,
        "-ss", start_time,
        "-to", end_time,
        "-vn",  # no video
        "-acodec", "copy",
        output_file, "-y"
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

# 動作按鈕
col1, col2 = st.columns(2)
with col1:
    if st.button("⬇️ MP4"):
        if url:
            with st.spinner("處理中，請稍後..."):
                full_file = download_full_video(url)
                st.session_state.mode = "video"
                st.session_state.full_file = full_file
        else:
            st.warning("⚠️ 請先輸入網址")
with col2:
    if st.button("🎵 音訊"):
        if url:
            with st.spinner("處理中，請稍後..."):
                full_file = download_full_audio(url)
                st.session_state.mode = "audio"
                st.session_state.full_file = full_file
        else:
            st.warning("⚠️ 請先輸入網址")

# 顯示選項與裁切設定
if st.session_state.full_file:
    st.success(f"✅ 選擇下載範圍")
    st.session_state.download_mode = st.radio(
        "請選擇：",
        ("全部下載", "下載時間段")
    )

    start_time = None
    end_time = None

    if st.session_state.download_mode == "下載時間段":
        start_time = st.text_input("開始時間（格式 00:01:30）", value="00:00:00")
        end_time = st.text_input("結束時間（格式 00:03:00）", value="00:01:00")

    # 產生最終下載檔案
    if st.button("✂️ 產生下載檔案"):
        with st.spinner("處理中..."):
            base_name, ext = os.path.splitext(st.session_state.full_file)
            if st.session_state.download_mode == "全部下載":
                st.session_state.output_file = st.session_state.full_file
            else:
                if st.session_state.mode == "video":
                    output_file = f"{base_name}_clip.mp4"
                    cut_video(st.session_state.full_file, output_file, start_time, end_time)
                elif st.session_state.mode == "audio":
                    output_file = f"{base_name}_clip.webm"
                    cut_audio(st.session_state.full_file, output_file, start_time, end_time)
                st.session_state.output_file = output_file

# 最終下載按鈕
if st.session_state.output_file and os.path.exists(st.session_state.output_file):
    with open(st.session_state.output_file, "rb") as f:
        file_ext = os.path.splitext(st.session_state.output_file)[1].lower()
        if st.session_state.mode == "video":
            mime = "video/mp4"
        elif st.session_state.mode == "audio":
            mime = "audio/webm" if file_ext == ".webm" else "audio/m4a"
        st.download_button(
            label="✅ 點我下載",
            data=f,
            file_name=os.path.basename(st.session_state.output_file),
            mime=mime
        )
