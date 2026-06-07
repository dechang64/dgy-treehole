"""疗愈音乐 — 使用预生成的音乐文件

音乐文件已预生成，直接播放，无需调用 API
"""

import streamlit as st
from core.config import MUSIC_PLACES, MUSIC_MOODS
import os
from pathlib import Path

st.set_page_config(page_title="疗愈音乐 · 大观园树洞", page_icon="🎵", layout="centered")
from core.styles import inject_css; inject_css()

# ── 返回 ──
if st.button("← 回到大观园", use_container_width=True):
    st.switch_page("app.py")

st.markdown("""
<div class="card-dark" style="text-align:center; padding: 1.5rem;">
    <div style="font-size: 2.5rem;">🎵</div>
    <h2 style="margin: 0.5rem 0;">疗愈音乐</h2>
    <p style="font-size: 0.85rem; color: #d4c5a9;">AI 为你生成专属疗愈音乐</p>
</div>
""", unsafe_allow_html=True)

# ── 音乐目录（兼容本地和 Streamlit Cloud）──
# 本地路径: static/music/
# Streamlit Cloud: 从 repo 根目录访问
MUSIC_DIR = Path("static/music")

# ── 选择参数 ──
col1, col2 = st.columns(2)
with col1:
    place = st.selectbox("场景", MUSIC_PLACES, index=0)
with col2:
    mood = st.selectbox("情绪", MUSIC_MOODS, index=0)

# ── 查找音乐文件 ──
music_file = MUSIC_DIR / f"{place}_{mood}.mp3"

if music_file.exists():
    # 显示音乐信息
    file_size_mb = music_file.stat().st_size / (1024 * 1024)
    st.markdown(f"""
<div class="card" style="text-align:center;">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎶</div>
    <h3>{place} · {mood}</h3>
    <p style="font-size: 0.8rem; color: #8b7355;">AI 专属生成 · {file_size_mb:.1f} MB</p>
</div>
""", unsafe_allow_html=True)

    # 播放音乐
    with open(music_file, "rb") as f:
        st.audio(f.read(), format="audio/mp3")

    # 下载按钮
    with open(music_file, "rb") as f:
        audio_data = f.read()
    st.download_button(
        "📥 下载音乐",
        data=audio_data,
        file_name=f"大观园_{place}_{mood}.mp3",
        mime="audio/mp3",
        use_container_width=True,
    )
else:
    # 尝试从 GitHub raw URL 获取
    github_raw_base = "https://raw.githubusercontent.com/dechang64/dgy-treehole/main/static/music"
    github_url = f"{github_raw_base}/{place}_{mood}.mp3"

    st.markdown(f"""
<div class="card" style="text-align:center;">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎶</div>
    <h3>{place} · {mood}</h3>
    <p style="font-size: 0.8rem; color: #8b7355;">从云端加载...</p>
</div>
""", unsafe_allow_html=True)

    # 直接使用 GitHub URL 播放
    st.audio(github_url, format="audio/mp3")

    # 下载按钮
    st.markdown(f"""
<div style="text-align:center; margin-top: 1rem;">
    <a href="{github_url}" download="大观园_{place}_{mood}.mp3" class="stButton">
        <button style="background-color: #c0392b; color: white; padding: 0.5rem 1rem; border: none; border-radius: 0.5rem; cursor: pointer;">
            📥 下载音乐
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

# ── 所有音乐列表 ──
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding: 1rem;">
    <p style="font-size: 0.9rem; color: #d4c5a9;">🎼 所有音乐</p>
</div>
""", unsafe_allow_html=True)

# GitHub raw base URL
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/dechang64/dgy-treehole/main/static/music"

# 显示所有可用音乐（按场景分组）
for scene in MUSIC_PLACES:
    with st.expander(f"🎋 {scene}", expanded=False):
        for emotion in MUSIC_MOODS:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"  {emotion}")
            with col2:
                audio_url = f"{GITHUB_RAW_BASE}/{scene}_{emotion}.mp3"
                st.audio(audio_url, format="audio/mp3")