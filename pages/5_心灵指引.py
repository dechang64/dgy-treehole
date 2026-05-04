"""MBTI 红楼梦情境化测试 — 完整版

8题情境化测试，16种MBTI类型，每种映射到红楼梦角色+场景+疗法。
原版数据完整移植。
"""

import streamlit as st
from core.mbti_data import (
    MBTI_QUESTIONS, MBTI_MAP, DIM_LABELS, DIM_DESCS, calc_mbti,
)
from core.characters import get_character_by_scene

st.set_page_config(page_title="心灵指引 · 大观园树洞", page_icon="🔮", layout="centered")

# ── 返回 ──
if st.button("← 回到大观园", use_container_width=True):
    st.switch_page("app.py")

st.markdown("""
<div class="card-dark" style="text-align:center; padding: 1.5rem;">
    <div style="font-size: 2.5rem;">🔮</div>
    <h2 style="margin: 0.5rem 0;">心灵指引</h2>
    <p style="font-size: 0.85rem; color: #d4c5a9;">8道红楼梦情境题，找到最适合你的倾听者</p>
</div>
""", unsafe_allow_html=True)

# ── 初始化 ──
if "mbti_answers" not in st.session_state:
    st.session_state.mbti_answers = {}
if "mbti_result" not in st.session_state:
    st.session_state.mbti_result = None

# ── 重新测试 ──
if st.session_state.mbti_result is not None:
    if st.button("🔄 重新测试", use_container_width=True):
        st.session_state.mbti_answers = {}
        st.session_state.mbti_result = None
        st.rerun()

# ── 答题 ──
answered = len(st.session_state.mbti_answers)

if answered < 8:
    # 进度条
    st.markdown(f"""
<div style="padding: 0.5rem 0;">
    <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:#8b7355;margin-bottom:0.3rem;">
        <span>第 {answered + 1}/8 题</span>
        <span>{answered * 12}%</span>
    </div>
    <div style="background:#e8dfd0;border-radius:99px;height:6px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#b8860b,#c0392b);height:100%;width:{answered * 12}%;border-radius:99px;transition:width 0.3s;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

    q = MBTI_QUESTIONS[answered]

    st.markdown(f"""
<div class="card" style="text-align:center; padding: 1.5rem;">
    <div style="font-size:0.75rem;color:#b8860b;margin-bottom:0.5rem;">{q['dim']} 维度</div>
    <div style="font-size:1.1rem;font-weight:600;line-height:1.6;">{q['q']}</div>
</div>
""", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(q["a"], key=f"mbti_a_{answered}", use_container_width=True):
            st.session_state.mbti_answers[answered] = q["at"]
            st.rerun()
    with col_b:
        if st.button(q["b"], key=f"mbti_b_{answered}", use_container_width=True):
            st.session_state.mbti_answers[answered] = q["bt"]
            st.rerun()

else:
    # ── 计算结果 ──
    mbti = calc_mbti(st.session_state.mbti_answers)
    st.session_state.mbti_result = mbti
    info = MBTI_MAP.get(mbti, MBTI_MAP["INFP"])
    char_info = get_character_by_scene(info["scene"])

    st.markdown(f"""
<div class="card-dark" style="text-align:center; padding: 1.5rem;">
    <div style="font-size:2rem;margin-bottom:0.3rem;">{char_info['icon']}</div>
    <div style="font-size:2.5rem;font-weight:700;color:#f5f0e8;letter-spacing:0.1em;">{mbti}</div>
    <div style="font-size:1rem;color:#d4c5a9;margin-top:0.3rem;">{info['desc']}</div>
</div>
""", unsafe_allow_html=True)

    # 推荐场景
    st.markdown(f"""
<div class="card" style="border-left:3px solid #b8860b;">
    <div style="font-size:0.8rem;color:#b8860b;margin-bottom:0.3rem;">🎯 推荐场景</div>
    <div style="font-size:1.1rem;font-weight:600;">{char_info['icon']} {info['scene']}</div>
    <div style="font-size:0.85rem;color:#8b7355;">倾听者：{info['char']} · {info['theory']}</div>
</div>
""", unsafe_allow_html=True)

    # 原因分析
    st.markdown(f"""
<div class="card">
    <div style="font-size:0.8rem;color:#b8860b;margin-bottom:0.3rem;">💡 为什么适合你</div>
    <p style="line-height:1.8;">{info['reason']}</p>
</div>
""", unsafe_allow_html=True)

    # 红楼梦引言
    st.markdown(f"""
<div class="card" style="text-align:center;font-style:italic;">
    <div style="font-size:0.8rem;color:#8b7355;margin-bottom:0.3rem;">——</div>
    <p style="color:#2c1810;font-size:1rem;line-height:1.8;">{info['quote']}</p>
</div>
""", unsafe_allow_html=True)

    # 维度解析
    st.markdown("### 维度解析")
    dims_info = [
        (mbti[0], mbti[1], "E/I"),
        (mbti[2], mbti[3], "S/N"),
        (mbti[4], mbti[5], "T/F"),
        (mbti[6], mbti[7], "J/P"),
    ]
    for chosen, other, dim_pair in dims_info:
        st.markdown(f"""
<div class="card" style="padding:0.6rem 1rem;">
    <strong style="color:#c0392b;">{chosen}</strong> — {DIM_LABELS[chosen]}
    <span style="color:#8b7355;font-size:0.85rem;">（vs {other} {DIM_LABELS[other]}）</span><br>
    <span style="color:#8b7355;font-size:0.85rem;">{DIM_DESCS[chosen]}</span>
</div>
""", unsafe_allow_html=True)

    # 操作按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"💬 去找{info['char']}聊聊", type="primary", use_container_width=True):
            st.session_state.current_scene = info["scene"]
            st.session_state.chat_character = info["char"]
            st.session_state.chat_history = []
            st.switch_page("pages/1_倾诉对话.py")
    with col2:
        if st.button("⭐ 看看星座指引", use_container_width=True):
            st.switch_page("pages/7_星座星盘.py")
