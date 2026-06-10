"""大观园树洞 v2 — 主入口

红楼梦主题心理疗愈平台
Streamlit + MiniMax API + 联邦学习
"""

# 2026-06-08: trigger streamlit cloud rebuild to pick up latest config.py
import streamlit as st
from core.config import SCENES, EMOTION_SCENE_MAP, SCENE_MAP
from core.db import init_db
from core.styles import inject_css  # 注入移动端 + 树洞/hero 样式

# ── 初始化数据库（建表，幂等）──
init_db()

# ── 页面配置（必须是第一个 st 命令）──
st.set_page_config(
    page_title="大观园树洞",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── 注入全局 CSS（在 set_page_config 之后）──
inject_css()

# ═══════════════════════════════════════════════════════════
#  🎬 区块 1：Hero（沉浸式开场 + 1 个核心 CTA）
# ═══════════════════════════════════════════════════════════
st.html("""
<div class="home-hero fade-in">
    <div class="hero-eyebrow">RED · MANSIONS · HEALING</div>
    <div class="hero-title">大观园树洞</div>
    <div class="hero-sub">在这里，你可以放下所有防备</div>
    <div class="hero-motto">"满纸荒唐言，一把辛酸泪。"</div>
</div>
""")

# 主 CTA：进入树洞（这是新用户最高频动作）
if st.button("🌳  进入树洞，写下心事", key="hero_cta_treehole", type="primary", use_container_width=True):
    st.session_state.current_scene = "潇湘馆"
    st.session_state.chat_character = "林黛玉"
    st.session_state.chat_history = []
    st.switch_page("pages/2_treehole.py")

st.html("""
<div style="text-align:center; margin: 0.4rem 0 0.2rem;">
    <span class="badge">🔒 匿名安全 · 不留痕迹 · 随时离开</span>
</div>
""")

# ═══════════════════════════════════════════════════════════
#  🧭 区块 2：7 个功能导航（4 列 × 2 行，desktop & mobile 通用）
# ═══════════════════════════════════════════════════════════
st.html("""
<div class="home-section">
    <div class="section-header">
        <span class="section-icon">🧭</span>
        <span class="section-title-main">去任何地方</span>
        <span class="section-title-sub">7 个功能区，随点随到</span>
    </div>
</div>
""")

# 7 个 nav：st.columns 强制 4 列；mobile 1 列是 streamlit 默认行为（无法绕过）
st.html('<div class="home-nav-grid">')
nav_items = [
    ("💬", "倾诉", "1_chat"),
    ("🌳", "树洞", "2_treehole"),
    ("🌸", "共鸣", "3_resonance"),
    ("🎵", "音乐", "4_music"),
    ("🔮", "MBTI", "5_mbti"),
    ("⭐", "星座", "7_zodiac"),
    ("📊", "洞察", "6_insight"),
]
nav_cols = st.columns(4)
for idx, (icon, label, page) in enumerate(nav_items):
    with nav_cols[idx % 4]:
        st.page_link(
            f"pages/{page}.py",
            label=f"{icon}\n{label}",
        )
st.html('</div>')

# ═══════════════════════════════════════════════════════════
#  💭 区块 3：12 情绪快速入口（3×4 网格）
# ═══════════════════════════════════════════════════════════
st.html("""
<div class="home-section">
    <div class="section-header">
        <span class="section-icon">💭</span>
        <span class="section-title-main">心里装着什么？</span>
        <span class="section-title-sub">点一下，直接去对应的院落</span>
    </div>
</div>
""")

# 12 情绪（带 emoji）→ EMOTION_SCENE_MAP 自动跳到对应场景
EMOTION_EMOJI = {
    "悲伤": "💧", "焦虑": "🌊", "愤怒": "🔥", "迷茫": "🌫️",
    "疲惫": "🍂", "孤独": "🌙", "平静": "🍃", "感恩": "🌸",
    "期待": "🌅", "执念": "⛓️", "委屈": "🌧️", "自卑": "🥀",
}
_entry_emotions = list(EMOTION_EMOJI.keys())  # 12 个

st.html('<div class="home-emotion-grid">')
# 4 列 × 3 行
for i in range(0, len(_entry_emotions), 4):
    emo_cols = st.columns(4)
    for j in range(4):
        if i + j < len(_entry_emotions):
            emo = _entry_emotions[i + j]
            with emo_cols[j]:
                icon = EMOTION_EMOJI[emo]
                if st.button(
                    f"{icon}\n{emo}",
                    key=f"emo_pick_{emo}",
                    use_container_width=True,
                ):
                    st.session_state.selected_emotion = emo
                    if emo in EMOTION_SCENE_MAP:
                        rec = EMOTION_SCENE_MAP[emo]
                        st.session_state.current_scene = rec["scene"]
                        scene_info = SCENE_MAP.get(rec["scene"], {})
                        st.session_state.chat_character = scene_info.get("char", "贾宝玉")
                    st.session_state.chat_history = []
                    st.switch_page("pages/1_chat.py")
st.html('</div>')

# ═══════════════════════════════════════════════════════════
#  🏯 区块 4：9 大院落（2 列网格）
# ═══════════════════════════════════════════════════════════
st.html("""
<div class="home-section">
    <div class="section-header">
        <span class="section-icon">🏯</span>
        <span class="section-title-main">9 大院落，等你入住</span>
        <span class="section-title-sub">6 处经典 + 栊翠庵/缀锦楼/紫菱洲</span>
    </div>
</div>
""")

st.html('<div class="home-scene-grid">')
for i in range(0, len(SCENES), 2):
    scene_cols = st.columns(2)
    for j, scene in enumerate(SCENES[i:i+2]):
        with scene_cols[j]:
            if st.button(
                f"{scene['icon']}  {scene['name']}\n{scene['mood']} · {scene['char']}",
                key=f"enter_{scene['name']}",
                use_container_width=True,
            ):
                st.session_state.current_scene = scene["name"]
                st.session_state.chat_character = scene["char"]
                st.session_state.chat_history = []
                st.switch_page("pages/1_chat.py")
st.html('</div>')

# ═══════════════════════════════════════════════════════════
#  🌸 区块 5：今日一签（每日一张红楼梦人物签）
# ═══════════════════════════════════════════════════════════
import random
import hashlib

_daily_signs = [
    ("黛玉", "花谢花飞花满天，红消香断有谁怜？", "把无法言说的哀愁，写成诗就轻了。"),
    ("宝玉", "任凭弱水三千，我只取一瓢饮。", "世间繁华三千，你只需守住心里那一瓢。"),
    ("宝钗", "好风凭借力，送我上青云。", "聪明不是算计，是顺势而为的从容。"),
    ("湘云", "幸生来，英豪阔大宽宏量。", "大大方方地活，纠结就少了大半。"),
    ("探春", "我但凡是个男人，可以出得去，我必早走了。", "清醒不是冷漠，是知道什么值得做。"),
    ("妙玉", "过洁世同嫌，至洁亦世所罕。", "放下执念不是妥协，是放过自己。"),
    ("惜春", "独卧青灯古佛旁，心如止水念无常。", "安静不是没有情绪，是懂得照顾自己。"),
    ("迎春", "金闺花柳质，一载赴黄粱。", "先抱住自己，世界才会温柔待你。"),
    ("李纨", "如冰水好空相妒，枉与他人作笑谈。", "生活的担子，放一放，没人怪你。"),
    ("凤姐", "凡事自有定数，何必空忙一场。", "精明之外，留一点温柔给自己。"),
]
# 用今天日期 hash 选一张签（每天固定，但每天不同）
_today_seed = hashlib.md5(__import__('datetime').date.today().isoformat().encode()).hexdigest()
_pick = _daily_signs[int(_today_seed, 16) % len(_daily_signs)]
_char, _quote, _remark = _pick

st.html(f"""
<div class="home-section">
    <div class="daily-sign">
        <div class="sign-label">今 日 一 签</div>
        <div class="sign-content">
            <div style="font-size:0.78rem;color:#d4a574;margin-bottom:0.3rem;">— {_char} —</div>
            <div style="font-style:italic;margin-bottom:0.4rem;">「{_quote}」</div>
            <div style="color:#d4c5a9;font-size:0.82rem;">{_remark}</div>
        </div>
        <div class="sign-footer">每天换一张 · 来自《红楼梦》</div>
    </div>
</div>
""")

# ═══════════════════════════════════════════════════════════
#  📊 区块 6：底部信息
# ═══════════════════════════════════════════════════════════
st.html("""
<div class="home-footer">
    🌸 在这里，你不需要假装坚强 🌸<br>
    <span class="footer-tag">联邦学习保护你的隐私 · 你的话只属于你</span>
</div>
""")
