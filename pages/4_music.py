"""疗愈音乐 — 大观园树洞

音乐文件通过 GitHub Release 直接托管（Range 请求友好），
由 Streamlit Cloud 代为请求后以本地临时文件方式播放。
"""
import streamlit as st
import requests
import tempfile
import os
from core.config import MUSIC_PLACES, MUSIC_MOODS

st.set_page_config(page_title="疗愈音乐 · 大观园树洞", page_icon="🎵", layout="centered")
from core.styles import inject_css; inject_css()

# GitHub Release — Release API 不支持中文字符名，用 ASCII 资源名
RELEASE_BASE = "https://github.com/dechang64/dgy-treehole/releases/download/v1.0-music"

FILENAME_MAP = {
    "潇湘馆_宁静.mp3": "xiaoxiangguan_ningjing.mp3",
    "潇湘馆_思念.mp3": "xiaoxiangguan_sinian.mp3",
    "潇湘馆_欢愉.mp3": "xiaoxiangguan_huanyu.mp3",
    "潇湘馆_沉思.mp3": "xiaoxiangguan_chensi.mp3",
    "潇湘馆_疗愈.mp3": "xiaoxiangguan_liaoyu.mp3",
    "潇湘馆_释然.mp3": "xiaoxiangguan_shiran.mp3",
    "蘅芜苑_宁静.mp3": "hengwuyuan_ningjing.mp3",
    "蘅芜苑_思念.mp3": "hengwuyuan_sinian.mp3",
    "蘅芜苑_欢愉.mp3": "hengwuyuan_huanyu.mp3",
    "蘅芜苑_沉思.mp3": "hengwuyuan_chensi.mp3",
    "蘅芜苑_疗愈.mp3": "hengwuyuan_liaoyu.mp3",
    "蘅芜苑_释然.mp3": "hengwuyuan_shiran.mp3",
    "怡红院_宁静.mp3": "yihongyuan_ningjing.mp3",
    "怡红院_思念.mp3": "yihongyuan_sinian.mp3",
    "怡红院_欢愉.mp3": "yihongyuan_huanyu.mp3",
    "怡红院_沉思.mp3": "yihongyuan_chensi.mp3",
    "怡红院_疗愈.mp3": "yihongyuan_liaoyu.mp3",
    "怡红院_释然.mp3": "yihongyuan_shiran.mp3",
    "稻香村_宁静.mp3": "daoxiangcun_ningjing.mp3",
    "稻香村_思念.mp3": "daoxiangcun_sinian.mp3",
    "稻香村_欢愉.mp3": "daoxiangcun_huanyu.mp3",
    "稻香村_沉思.mp3": "daoxiangcun_chensi.mp3",
    "稻香村_疗愈.mp3": "daoxiangcun_liaoyu.mp3",
    "稻香村_释然.mp3": "daoxiangcun_shiran.mp3",
    "藕香榭_宁静.mp3": "ouxiangxie_ningjing.mp3",
    "藕香榭_思念.mp3": "ouxiangxie_sinian.mp3",
    "藕香榭_欢愉.mp3": "ouxiangxie_huanyu.mp3",
    "藕香榭_沉思.mp3": "ouxiangxie_chensi.mp3",
    "藕香榭_疗愈.mp3": "ouxiangxie_liaoyu.mp3",
    "藕香榭_释然.mp3": "ouxiangxie_shiran.mp3",
    "秋爽斋_宁静.mp3": "qiushuangzhai_ningjing.mp3",
    "秋爽斋_思念.mp3": "qiushuangzhai_sinian.mp3",
    "秋爽斋_欢愉.mp3": "qiushuangzhai_huanyu.mp3",
    "秋爽斋_沉思.mp3": "qiushuangzhai_chensi.mp3",
    "秋爽斋_疗愈.mp3": "qiushuangzhai_liaoyu.mp3",
    "秋爽斋_释然.mp3": "qiushuangzhai_shiran.mp3",
}


@st.cache_data(ttl=3600, show_spinner="正在加载音乐...")
def get_audio_file(place: str, mood: str) -> str | None:
    """下载音频到临时文件并返回路径，缓存1小时"""
    chinese_name = f"{place}_{mood}.mp3"
    asset_name = FILENAME_MAP.get(chinese_name, chinese_name)
    url = f"{RELEASE_BASE}/{asset_name}"

    try:
        with st.spinner("加载音乐中..."):
            resp = requests.get(url, timeout=60, stream=True)
            resp.raise_for_status()

        tmp = tempfile.NamedTemporaryFile(
            suffix=".mp3", prefix=f"treehole_{place}_{mood}_", delete=False
        )
        for chunk in resp.iter_content(chunk_size=65536):
            tmp.write(chunk)
        tmp.close()
        return tmp.name
    except Exception as e:
        st.error(f"加载音乐失败: {e}")
        return None


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

# ── 选择参数 ──
col1, col2 = st.columns(2)
with col1:
    place = st.selectbox("场景", MUSIC_PLACES, index=0)
with col2:
    mood = st.selectbox("情绪", MUSIC_MOODS, index=0)

# ── 播放 ──
audio_path = get_audio_file(place, mood)
chinese_name = f"{place}_{mood}.mp3"

st.markdown(f"""
<div class="card" style="text-align:center;">
    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎶</div>
    <h3>{place} · {mood}</h3>
    <p style="font-size: 0.8rem; color: #8b7355;">AI 专属生成</p>
</div>
""", unsafe_allow_html=True)

if audio_path:
    st.audio(audio_path, format="audio/mp3")
    # 下载按钮
    with open(audio_path, "rb") as f:
        st.download_button(
            label="📥 下载音乐",
            data=f,
            file_name=chinese_name,
            mime="audio/mpeg",
            use_container_width=True,
        )
else:
    st.warning("音乐加载失败，请检查网络后重试。")

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
                path = get_audio_file(scene, emotion)
                if path:
                    st.audio(path, format="audio/mp3")
