"""疗愈音乐 — 大观园树洞

音乐文件通过 raw.githubusercontent.com CDN 直接托管，无需 API 调用，直接播放。
"""
import streamlit as st
from core.config import MUSIC_PLACES, MUSIC_MOODS

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

# CDN: raw.githubusercontent.com — 已经是真实音频（非 LFS 指针）
CDN_BASE = "https://raw.githubusercontent.com/dechang64/dgy-treehole/main/static/music"

def get_audio_url(place: str, mood: str) -> str:
    """根据场景和情绪返回音频 URL"""
    return f"{CDN_BASE}/{place}_{mood}.mp3"


# ── 选择参数 ──
col1, col2 = st.columns(2)
with col1:
    place = st.selectbox("场景", MUSIC_PLACES, index=0)
with col2:
    mood = st.selectbox("情绪", MUSIC_MOODS, index=0)

# ── 播放 ──
audio_url = get_audio_url(place, mood)

st.markdown(f"""
<div class="card" style="text-align:center;">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎶</div>
    <h3>{place} · {mood}</h3>
    <p style="font-size: 0.8rem; color: #8b7355;">AI 专属生成</p>
</div>
""", unsafe_allow_html=True)

st.audio(audio_url, format="audio/mp3")

# 下载按钮
st.markdown(f"""
<div style="text-align:center; margin-top: 1rem;">
    <a href="{audio_url}" download="大观园_{place}_{mood}.mp3">
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

for scene in MUSIC_PLACES:
    with st.expander(f"🎋 {scene}", expanded=False):
        for emotion in MUSIC_MOODS:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"  {emotion}")
            with col2:
                url = get_audio_url(scene, emotion)
                st.audio(url, format="audio/mp3")