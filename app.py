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
# 🐛 DEBUG MARKER — 如果你看到这行黄色条 = Cloud 在跑新代码
# 如果没看到 = Cloud 卡了, 请到 Manage app → Reboot
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div style="background: #ffeb3b; color: #000; padding: 12px; text-align: center;
            font-size: 16px; font-weight: bold; border: 3px solid #f44336;
            border-radius: 8px; margin: 10px 0;">
    🐛 DEBUG: BUILD 28b082b+v3 | 如果你看到这条黄条 = Cloud 已部署新代码
</div>
""", unsafe_allow_html=True)

# ── 自定义 CSS（与原版 index.html 完全对齐）──
st.markdown("""<style>
/* 隐藏 Streamlit 默认元素 */
#MainMenu, footer, header {visibility: hidden}
.block-container {padding-top: 0.5rem; padding-bottom: 2rem; max-width: 520px}

/* 顶部 page_link 风格：仿按钮 */
[data-testid="stPageLink-NavLink"] {
    display: inline-block;
    background: #f5f0e8;
    color: #2c1810;
    border: 1px solid #e8dfd0;
    border-radius: 10px;
    padding: 0.5rem 0.8rem;
    margin: 0.2rem 0.15rem;
    font-size: 0.88rem;
    font-weight: 500;
    text-decoration: none;
    transition: all 0.2s;
}
[data-testid="stPageLink-NavLink"]:hover {
    background: #b8860b;
    color: #fff;
    border-color: #b8860b;
}

/* 全局字体 */
.stApp {font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', serif}

/* 卡片样式 */
.card {
    background: #f5f0e8;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 0.8rem 0;
    border: 1px solid #e8dfd0;
}
.card-dark {
    background: #2c1810;
    color: #f5f0e8;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 0.8rem 0;
}

/* 场景卡片 */
.scene-card {
    background: linear-gradient(135deg, #f5f0e8, #e8dfd0);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    border: 1px solid #d4c5a9;
    cursor: pointer;
    transition: all 0.3s;
}
.scene-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(44,24,16,0.12);
    border-color: #b8860b;
}

/* 聊天气泡 */
.chat-ai {
    background: #e8dfd0;
    border-radius: 16px 16px 16px 4px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    max-width: 85%;
}
.chat-user {
    background: #2c1810;
    color: #f5f0e8;
    border-radius: 16px 16px 4px 16px;
    padding: 0.8rem 1rem;
    margin: 0.4rem 0;
    max-width: 85%;
    margin-left: auto;
}

/* 标签 */
.tag {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    background: rgba(184,134,11,0.1);
    color: #b8860b;
    border-radius: 99px;
    font-size: 0.8rem;
    margin: 0.15rem;
}

/* 模式指示器 */
.mock-badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    background: rgba(192,57,43,0.1);
    color: #c0392b;
    border-radius: 99px;
    font-size: 0.7rem;
}

/* Hero 头部（对齐原版 .hero） */
.hero {
    background: linear-gradient(135deg, #2c1810, #4a2c1a 50%, #3d1f0e);
    padding: 2.5rem 1.5rem 2rem;
    color: #f5f0e8;
    text-align: center;
    position: relative;
    overflow: hidden;
    border-radius: 0 0 16px 16px;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 30% 50%, rgba(184,134,11,0.12), transparent 60%);
    pointer-events: none;
}
.hero h1 {
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 0.4rem;
    position: relative;
}
.hero .sub {
    opacity: 0.7;
    font-size: 0.85rem;
    margin: 0.4rem 0 0.8rem;
    position: relative;
}
.hero .motto {
    font-size: 0.8rem;
    opacity: 0.5;
    font-style: italic;
    position: relative;
}

/* 安全徽章（对齐原版 .badge） */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.3rem 0.8rem;
    background: rgba(45,106,79,0.1);
    color: #2d6a4f;
    border-radius: 99px;
    font-size: 0.75rem;
}

/* 结果卡片（对齐原版 .result-type/.result-scene/.result-reason/.result-quote） */
.result-type {
    font-size: 2.5rem;
    font-weight: 800;
    color: #c0392b;
    text-align: center;
    letter-spacing: 0.3rem;
    margin: 0.5rem 0;
}
.result-desc {
    text-align: center;
    font-size: 0.9rem;
    color: #8b7355;
    margin-bottom: 0.8rem;
}
.result-scene {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.8rem;
    background: #fff;
    border-radius: 12px;
    border: 1px solid #e8dfd0;
    margin-bottom: 0.8rem;
}
.result-scene .icon {
    font-size: 2rem;
    width: 48px;
    text-align: center;
}
.result-scene .name {
    font-weight: 600;
    font-size: 0.95rem;
    color: #2c1810;
}
.result-scene .info {
    font-size: 0.8rem;
    color: #8b7355;
    margin-top: 0.1rem;
}
.result-reason {
    background: #f5f0e8;
    border-radius: 12px;
    padding: 0.8rem;
    margin: 0.8rem 0;
    font-size: 0.85rem;
    line-height: 1.7;
    color: #2c1810;
}
.result-quote {
    text-align: center;
    font-style: italic;
    color: #8b7355;
    font-size: 0.85rem;
    padding: 0.8rem;
    border-left: 3px solid #b8860b;
    margin: 0.8rem 0;
}

/* 星座按钮（对齐原版 .zodiac-btn） */
.zodiac-btn {
    background: #fff;
    border: 1px solid #e8dfd0;
    border-radius: 12px;
    padding: 0.6rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
}
.zodiac-btn:hover {
    border-color: #b8860b;
    box-shadow: 0 4px 12px rgba(44,24,16,0.08);
}

/* 星盘卡片（对齐原版 .chart-planet） */
.chart-planet {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.5rem 0.7rem;
    background: #fff;
    border-radius: 10px;
    margin: 0.3rem 0;
    border: 1px solid #e8dfd0;
}
.chart-planet .p-icon {
    font-size: 1.3rem;
    width: 32px;
    text-align: center;
    flex-shrink: 0;
}
.chart-planet .p-info { flex: 1; }
.chart-planet .p-name { font-size: 0.78rem; font-weight: 600; }
.chart-planet .p-sign { font-size: 0.7rem; color: #8b7355; }
.chart-planet .p-desc { font-size: 0.72rem; color: #2c1810; margin-top: 0.1rem; line-height: 1.5; }

/* 星盘总结（对齐原版 .chart-summary） */
.chart-summary {
    background: linear-gradient(135deg, #2c1810, #4a2c1a);
    color: #f5f0e8;
    border-radius: 12px;
    padding: 1rem;
    margin: 0.8rem 0;
    text-align: center;
}

/* 元素标签（对齐原版 .elem-label） */
.elem-label {
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0.3rem 0;
    margin-top: 0.5rem;
}

/* 动画 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.5s ease-out; }
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  Hero（对齐原版首页）
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <h1>大观园树洞</h1>
    <p class="sub">在这里，你可以放下所有防备</p>
    <p class="motto">"满纸荒唐言，一把辛酸泪。"</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center"><span class="badge">🔒 匿名安全 · 不留痕迹 · 随时离开</span></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  ✨ 找到属于你的院落 — 用 nav 4×2 网格替代（原 MBTI/星座 大按钮删除，与 nav 重复）
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div style="padding: 0.4rem 0;">
    <p style="font-size: 0.95rem; font-weight: 600; margin-bottom: 0.3rem;">✨ 找到属于你的院落</p>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  导航（7个功能入口）
#  st.page_link 包在 flex-wrap 容器里，浏览器自然换行
#  原因：st.columns 在 mobile 强制降级为单列（跟列数无关）
#  streamlit page_link 在 <a> 上加 [data-testid="stPageLink-NavLink"] class
#  外层 .nav-flex-wrap 用 flex-wrap:wrap 让窄屏自动 2-3 个一行
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="nav-flex-wrap">', unsafe_allow_html=True)
nav_items = [
    ("💬", "倾诉", "1_chat"),
    ("🌳", "树洞", "2_treehole"),
    ("🌸", "共鸣", "3_resonance"),
    ("🎵", "音乐", "4_music"),
    ("🔮", "MBTI", "5_mbti"),
    ("⭐", "星座", "7_zodiac"),
    ("📊", "洞察", "6_insight"),
]
for icon, label, page in nav_items:
    st.page_link(
        f"pages/{page}.py",
        label=f"{icon} {label}",
    )
st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  9大场景（6 经典 + 3 新增：栊翠庵/缀锦楼/紫菱洲）
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🏯 选择你的场景</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  情绪入口（可选，非强制）
#  3 列 × 3 行布局 — desktop 和 mobile 都友好
#  7 情绪 + 占位 + 占位 = 9
# ═══════════════════════════════════════════════════════════
_entry_emotions = ["悲伤", "焦虑", "愤怒", "迷茫", "疲惫", "孤独", "平静", "", ""]
# 3 行 × 3 列
for i in range(0, len(_entry_emotions), 3):
    cols = st.columns(3)
    for j in range(3):
        emo = _entry_emotions[i + j]
        with cols[j]:
            if emo:
                if st.button(f"{emo}", key=f"emo_pick_{emo}", use_container_width=True):
                    st.session_state.selected_emotion = emo
                    # 根据情绪自动进入推荐场景
                    if emo in EMOTION_SCENE_MAP:
                        rec = EMOTION_SCENE_MAP[emo]
                        st.session_state.current_scene = rec["scene"]
                        # 找到该场景对应的角色
                        scene_info = SCENE_MAP.get(rec["scene"], {})
                        st.session_state.chat_character = scene_info.get("char", "贾宝玉")
                        st.session_state.chat_history = []
                        st.switch_page("pages/1_chat.py")

# 如果用户已选了情绪，显示推荐信息
if "selected_emotion" in st.session_state:
    emo = st.session_state.selected_emotion
    if emo in EMOTION_SCENE_MAP:
        rec = EMOTION_SCENE_MAP[emo]
        st.markdown(f"""
<div class="card" style="border-left: 3px solid #b8860b; padding: 0.6rem 0.8rem;">
    <div style="font-size: 0.85rem; color: #8b7355;">
        {rec["icon"]} {rec["msg"]}——
        <a href="#" onclick="document.querySelectorAll('[data-testid=\"stButton\"] button')[0].click()">
            <strong>进入{rec["scene"]}</strong>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# 纯 CSS grid 渲染9个场景卡片 + 隐藏的全卡片点击区
# 关键: 卡片本身 HTML 仅展示信息, 真正的"点击"由一个铺满卡片的透明按钮触发
# 避免 streamlit page_link 在 HTML <a> 里不能触发 SPA 路由的问题
# 视觉: 卡片右下角小箭头 "→" 提示可点
# 2 列布局 — desktop 和 mobile 都友好
_cards_html = '<div class="scene-card-grid">'
for scene in SCENES:
    _cards_html += f"""
<div class="scene-card">
    <div class="scene-card-inner">
        <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">{scene['icon']}</div>
        <div style="font-weight: 600; font-size: 1rem; color: #2c1810;">{scene['name']}</div>
        <div style="font-size: 0.8rem; color: #8b7355; margin-top: 0.2rem;">{scene['desc']}</div>
        <div style="font-size: 0.75rem; color: #b8860b; margin-top: 0.2rem;">{scene['mood']} · {scene['style']}</div>
        <div style="margin-top: 0.5rem;">
            <span class="tag">倾听者：{scene['char']}</span>
            <span class="tag">{scene['theory']}</span>
        </div>
        <div class="scene-card-cta">进入 →</div>
    </div>
</div>"""
_cards_html += '</div>'
st.markdown(_cards_html, unsafe_allow_html=True)

# 隐藏按钮 grid (铺在卡片下面, 全透明覆盖) — 用 st.button 触发 switch_page
# 桌面 2 列, mobile streamlit 自动降级为 1 列
# 按钮文案简短避免与卡片信息重复
st.markdown('<div class="scene-btn-grid">', unsafe_allow_html=True)
for i in range(0, len(SCENES), 2):
    cols = st.columns(2)
    for j, scene in enumerate(SCENES[i:i+2]):
        with cols[j]:
            if st.button(
                f"开始倾诉 →",
                key=f"scene_{scene['name']}",
                use_container_width=True,
            ):
                st.session_state.current_scene = scene["name"]
                st.session_state.chat_character = scene["char"]
                st.session_state.chat_history = []
                st.switch_page("pages/1_chat.py")
st.markdown('</div>', unsafe_allow_html=True)

# ── 底部信息 ──
st.markdown("""
<div style="text-align:center; padding: 1rem 0; color: #8b7355; font-size: 0.75rem;">
    🌸 在这里，你不需要假装坚强 🌸<br>
    <span style="color: #b8860b;">联邦学习保护你的隐私 · 你的话只属于你</span>
</div>
""", unsafe_allow_html=True)

# ── MOCK_MODE 下不再显示"演示模式"红 badge
# 内部仍走固定回复作为 safety net（见 core/minimax_chat.py）
# 用户感知不到差别，UX 更干净
# if MOCK_MODE:
#     st.markdown('<div style="text-align:center"><span class="mock-badge">🎭 演示模式（未配置 GLM_API_KEY）</span></div>', unsafe_allow_html=True)
