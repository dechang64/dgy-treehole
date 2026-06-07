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

# GitHub Release — 为媒体流设计，支持 Range 请求，浏览器原生 audio 元素可直接播放
RELEASE_BASE = "https://github.com/dechang64/dgy-treehole/releases/download/v1.0-music"

# 中文名 → Release 资源名（Release API 不支持中文字符名）
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

def get_audio_url(place: str, mood: str) -> str:
    """根据场景和情绪返回音频 URL"""
    chinese_name = f"{place}_{mood}.mp3"
    asset_name = FILENAME_MAP.get(chinese_name, chinese_name)
    return f"{RELEASE_BASE}/{asset_name}"


# ── 选择参数 ──
col1, col2 = st.columns(2)
with col1:
    place = st.selectbox("场景", MUSIC_PLACES, index=0)
with col2:
    mood = st.selectbox("情绪", MUSIC_MOODS, index=0)

# ── 播放 ──
audio_url = get_audio_url(place, mood)
chinese_name = f"{place}_{mood}.mp3"

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
        <a href="{audio_url}" download="{chinese_name}">
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