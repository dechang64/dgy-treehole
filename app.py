"""大观园树洞 v2 — 主入口

红楼梦主题心理疗愈平台
Streamlit + MiniMax API + 联邦学习
"""

import streamlit as st

# ── 页面配置 ──
st.set_page_config(
    page_title="大观园树洞",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── 自定义 CSS ──
st.markdown("""<style>
/* 隐藏 Streamlit 默认元素 */
#MainMenu, footer, header {visibility: hidden}
.block-container {padding-top: 0.5rem; padding-bottom: 2rem; max-width: 520px}

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

/* 按钮 */
.stButton > button {
    border-radius: 99px;
    border: none;
    padding: 0.6rem 1.5rem;
    font-weight: 500;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* 输入框 */
.stTextInput > div > div > input {
    border-radius: 99px;
    border: 1px solid #d4c5a9;
}
.stTextArea > div > div > textarea {
    border-radius: 12px;
    border: 1px solid #d4c5a9;
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

/* 动画 */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.5s ease-out; }

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.float { animation: float 3s ease-in-out infinite; }
</style>""", unsafe_allow_html=True)

# ── 初始化数据库 ──
from core.db import init_db
init_db()

# ── Session State 初始化 ──
if "current_scene" not in st.session_state:
    st.session_state.current_scene = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_character" not in st.session_state:
    st.session_state.chat_character = None
if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())[:8]

# ── Hero ──
st.markdown("""
<div style="
    background: linear-gradient(135deg, #2c1810, #4a2c1a 50%, #3d1f0e);
    padding: 2rem 1.5rem 1.5rem;
    border-radius: 0 0 24px 24px;
    text-align: center;
    color: #f5f0e8;
    margin: -0.5rem -1rem 1rem -1rem;
    position: relative;
    overflow: hidden;
">
    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌸</div>
    <h1 style="font-size: 1.5rem; margin: 0; font-weight: 600; letter-spacing: 2px;">大观园树洞</h1>
    <p style="font-size: 0.85rem; color: #d4c5a9; margin-top: 0.3rem;">红楼梦主题 · 心理疗愈平台</p>
</div>
""", unsafe_allow_html=True)

# ── 模式指示 ──
from core.config import MOCK_MODE
if MOCK_MODE:
    st.markdown('<div style="text-align:center"><span class="mock-badge">🎭 演示模式（未配置 API Key）</span></div>', unsafe_allow_html=True)

# ── 导航 ──
from core.config import SCENES

nav_cols = st.columns(7)
nav_items = [
    ("💬", "倾诉"),
    ("🌳", "树洞"),
    ("🌸", "共鸣"),
    ("🎵", "音乐"),
    ("🔮", "MBTI"),
    ("⭐", "星座"),
    ("📊", "洞察"),
]
nav_pages = [
    "1_倾诉对话", "2_匿名树洞", "3_匿名共鸣",
    "4_疗愈音乐", "5_心灵指引", "7_星座星盘", "6_情绪洞察",
]
for i, (icon, label) in enumerate(nav_items):
    with nav_cols[i]:
        if st.button(f"{icon}\n{label}", key=f"nav_{i}", use_container_width=True):
            st.switch_page(f"pages/{nav_pages[i]}.py")

# ── 6大场景 ──
st.markdown("### 🏯 选择你的场景")

for i in range(0, len(SCENES), 2):
    cols = st.columns(2)
    for j, scene in enumerate(SCENES[i:i+2]):
        with cols[j]:
            st.markdown(f"""
<div class="scene-card" onclick="document.querySelector('[data-testid=\\'stSidebarNav\\']')">
    <div style="font-size: 1.8rem; margin-bottom: 0.3rem;">{scene['icon']}</div>
    <div style="font-weight: 600; font-size: 1rem; color: #2c1810;">{scene['name']}</div>
    <div style="font-size: 0.8rem; color: #8b7355; margin-top: 0.2rem;">{scene['desc']}</div>
    <div style="margin-top: 0.5rem;">
        <span class="tag">倾听者：{scene['char']}</span>
        <span class="tag">{scene['theory']}</span>
    </div>
</div>
""", unsafe_allow_html=True)
            if st.button(f"进入{scene['name']} →", key=f"scene_{scene['name']}", use_container_width=True):
                st.session_state.current_scene = scene["name"]
                st.session_state.chat_character = scene["char"]
                st.session_state.chat_history = []
                st.switch_page("pages/1_倾诉对话.py")

# ── 底部信息 ──
st.markdown("""
<div style="text-align:center; padding: 1rem 0; color: #8b7355; font-size: 0.75rem;">
    🌸 在这里，你不需要假装坚强 🌸<br>
    <span style="color: #b8860b;">联邦学习保护你的隐私 · 你的话只属于你</span>
</div>
""", unsafe_allow_html=True)
