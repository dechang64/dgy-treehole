"""AI 倾诉对话 — MiniMax API 驱动的真 AI 对话

6位红楼梦角色，各有独立 system prompt 和疗愈风格。
联邦学习：每次对话结束后提交本地情绪统计。
"""

import uuid
import streamlit as st
from core.minimax_chat import chat
from core.characters import get_character
from core.emotion_detector import detect_emotion, compute_session_emotion_profile
from core.fl_engine import submit_local_stats
from core.config import MOCK_MODE

st.set_page_config(page_title="倾诉对话 · 大观园树洞", page_icon="💬", layout="centered")

# ── 返回按钮 ──
if st.button("← 回到大观园", use_container_width=True):
    st.switch_page("app.py")

# ── 初始化 session ──
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── 获取角色 ──
character = st.session_state.get("chat_character", "贾宝玉")
scene_name = st.session_state.get("current_scene", "怡红院")
char_info = get_character(character)

# ── 场景标题 ──
st.markdown(f"""
<div class="card-dark" style="text-align:center; padding: 1rem;">
    <div style="font-size: 2rem;">{char_info['icon']}</div>
    <div style="font-weight: 600; font-size: 1.1rem;">{char_info['scene']} · {character}</div>
    <div style="font-size: 0.8rem; color: #d4c5a9; margin-top: 0.2rem;">{char_info['theory']}</div>
</div>
""", unsafe_allow_html=True)

# ── 聊天记录 ──
for msg in st.session_state.chat_history:
    role = msg.get("role", "")
    content = msg.get("content", msg.get("text", ""))
    if role == "user":
        st.markdown(f"""
<div class="chat-user">{content}</div>
""", unsafe_allow_html=True)
    elif role == "assistant":
        st.markdown(f"""
<div class="chat-ai"><strong>{character}：</strong>{content}</div>
""", unsafe_allow_html=True)

# ── 输入框 ──
user_input = st.chat_input("说出你的心事...")

if user_input:
    # 情绪检测
    emotion = detect_emotion(user_input)

    # 添加用户消息
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input,
        "emotion": emotion,
    })

    # 调用 AI
    response = chat(
        messages=st.session_state.chat_history,
        character=character,
    )

    st.session_state.chat_history.append({"role": "assistant", "content": response})

    # 提交联邦学习统计
    try:
        profile = compute_session_emotion_profile(st.session_state.chat_history)
        if profile:
            submit_local_stats(st.session_state.session_id, profile)
    except Exception:
        pass

    st.rerun()

# ── 底部操作 ──
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 换个场景", use_container_width=True):
        st.session_state.chat_history = []
        st.switch_page("app.py")
with col2:
    if st.button("🌳 去树洞", use_container_width=True):
        st.switch_page("pages/2_匿名树洞.py")
with col3:
    if st.button("📊 情绪洞察", use_container_width=True):
        st.switch_page("pages/6_情绪洞察.py")

# ── 情绪标签显示 ──
user_msgs = [m for m in st.session_state.chat_history if m.get("role") == "user" and m.get("emotion")]
if user_msgs:
    last_emotion = user_msgs[-1].get("emotion", "")
    if last_emotion:
        st.markdown(f"""
<div style="text-align:center; padding: 0.5rem;">
    <span class="tag">当前情绪：{last_emotion}</span>
    <span class="tag">联邦学习保护中 🔒</span>
</div>
""", unsafe_allow_html=True)
