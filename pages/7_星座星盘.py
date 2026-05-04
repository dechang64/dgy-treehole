"""星座指引 + 星盘分析 — 完整版

12星座×4元素 + 6星体简化天文计算 + 元素→角色匹配
原版数据完整移植。
"""

import streamlit as st
from core.zodiac_data import (
    ZODIAC, ZODIAC_MAP, ELEMENTS, ELEM_CHARS, PLANET_DESC, CITIES,
    calc_birth_chart,
)
from core.config import SCENE_MAP

st.set_page_config(page_title="星座星盘 · 大观园树洞", page_icon="⭐", layout="centered")

# ── 返回 ──
if st.button("← 回到大观园", use_container_width=True):
    st.switch_page("app.py")

# ── Tab ──
tab_zodiac, tab_chart = st.tabs(["⭐ 星座指引", "🔮 星盘分析"])

# ═══════════════════════════════════════════════════════════
#  星座指引
# ═══════════════════════════════════════════════════════════
with tab_zodiac:
    st.markdown("""
<div class="card-dark" style="text-align:center; padding: 1.2rem;">
    <div style="font-size: 2rem;">⭐</div>
    <h2 style="margin: 0.3rem 0;">星座指引</h2>
    <p style="font-size: 0.85rem; color: #d4c5a9;">选择你的星座，找到最适合的倾听者</p>
</div>
""", unsafe_allow_html=True)

    # 按元素分组
    elem_groups = {"火象": [], "土象": [], "风象": [], "水象": []}
    for z in ZODIAC:
        elem_groups[z["elem"] + "象"].append(z)

    for elem_name, zodiacs in elem_groups.items():
        elem_info = ELEMENTS.get(elem_name.replace("象", ""), {})
        color = elem_info.get("color", "#8b7355")
        icon = elem_info.get("icon", "")

        st.markdown(f"""
<div style="margin:0.8rem 0 0.3rem;">
    <span style="color:{color};font-weight:600;font-size:0.9rem;">{icon} {elem_name}</span>
</div>
""", unsafe_allow_html=True)

        cols = st.columns(3)
        for i, z in enumerate(zodiacs):
            with cols[i]:
                sign_short = z["sign"].split(" ")[1]
                if st.button(
                    f"{z['sign'].split(' ')[0]}\n{sign_short}",
                    key=f"zodiac_{sign_short}",
                    use_container_width=True,
                ):
                    st.session_state.selected_zodiac = sign_short
                    st.rerun()

    # 星座结果
    if "selected_zodiac" in st.session_state:
        z = ZODIAC_MAP.get(st.session_state.selected_zodiac)
        if z:
            elem = ELEMENTS.get(z["elem"], {})
            scene_info = SCENE_MAP.get(z["scene"], {})

            st.markdown("---")
            st.markdown(f"""
<div class="card" style="text-align:center; padding:1.2rem; border:2px solid {elem.get('color','#8b7355')};">
    <div style="font-size:2.5rem;">{z['sign'].split(' ')[0]}</div>
    <div style="font-size:1.1rem;font-weight:600;">{z['sign'].split(' ')[1]}</div>
    <div style="font-size:0.8rem;color:#8b7355;">{z['date']} · {z['elem']}象 · {z['trait']}</div>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="card" style="border-left:3px solid {elem.get('color','#8b7355')};">
    <div style="font-size:0.8rem;color:#b8860b;margin-bottom:0.3rem;">🎯 推荐场景</div>
    <div style="font-size:1.1rem;font-weight:600;">{scene_info.get('icon','')} {z['scene']}</div>
    <div style="font-size:0.85rem;color:#8b7355;">倾听者：{z['char']}</div>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div class="card">
    <div style="font-size:0.8rem;color:#b8860b;margin-bottom:0.3rem;">💡 为什么适合你</div>
    <p style="line-height:1.8;">{z['reason']}</p>
</div>
""", unsafe_allow_html=True)

            # 元素建议
            if elem:
                st.markdown(f"""
<div class="card" style="background:linear-gradient(135deg,#2c1810,#4a2c1a);color:#f5f0e8;">
    <div style="font-size:0.8rem;color:#b8860b;margin-bottom:0.3rem;">{elem.get('icon','')} {z['elem']}象特质 · {elem.get('style','')}</div>
    <p style="line-height:1.8;font-size:0.9rem;">{elem.get('advice','')}</p>
</div>
""", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"💬 去找{z['char']}聊聊", type="primary", use_container_width=True):
                    st.session_state.current_scene = z["scene"]
                    st.session_state.chat_character = z["char"]
                    st.session_state.chat_history = []
                    st.switch_page("pages/1_倾诉对话.py")
            with col2:
                if st.button("🔮 星盘分析", use_container_width=True):
                    tab_chart


# ═══════════════════════════════════════════════════════════
#  星盘分析
# ═══════════════════════════════════════════════════════════
with tab_chart:
    st.markdown("""
<div class="card-dark" style="text-align:center; padding: 1.2rem;">
    <div style="font-size: 2rem;">🔮</div>
    <h2 style="margin: 0.3rem 0;">星盘分析</h2>
    <p style="font-size: 0.85rem; color: #d4c5a9;">输入出生信息，解读你的六大星体</p>
</div>
""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        birth_date = st.date_input("出生日期", value=None)
    with col2:
        birth_time = st.time_input("出生时间", value=None)
    with col3:
        city = st.selectbox("出生城市", list(CITIES.keys()), index=0)

    if st.button("🔮 解读星盘", type="primary", use_container_width=True):
        if not birth_date or not birth_time:
            st.warning("请填写出生日期和时间")
        else:
            chart = calc_birth_chart(
                year=birth_date.year, month=birth_date.month, day=birth_date.day,
                hour=birth_time.hour, minute=birth_time.minute,
                city=city,
            )
            st.session_state.birth_chart = chart
            st.rerun()

    # ── 星盘结果 ──
    if "birth_chart" in st.session_state:
        chart = st.session_state.birth_chart

        # 元素分布
        elements = chart["elements"]
        dominant = chart["dominant"]
        elem_info = ELEMENTS.get(dominant[0], {})
        elem_char = ELEM_CHARS.get(dominant[0], {})

        st.markdown(f"""
<div style="display:flex;gap:0.4rem;padding:0.5rem 0;">
""", unsafe_allow_html=True)

        elem_icons = {"火": "🔥", "土": "🏔️", "风": "💨", "水": "🌊"}
        elem_cols = st.columns(4)
        for i, (elem, count) in enumerate(elements.items()):
            with elem_cols[i]:
                is_dominant = elem == dominant[0]
                bg = "linear-gradient(135deg,#2c1810,#4a2c1a)" if is_dominant else "#fff"
                fg = "#f5f0e8" if is_dominant else "#2c1810"
                border = "2px solid #b8860b" if is_dominant else "1px solid #e8dfd0"
                st.markdown(f"""
<div style="text-align:center;padding:0.5rem;background:{bg};color:{fg};border-radius:10px;border:{border};">
    <div style="font-size:1.2rem;">{elem_icons.get(elem,'')}</div>
    <div style="font-size:0.7rem;">{elem}象 {count}</div>
</div>
""", unsafe_allow_html=True)

        # 主导元素
        if elem_char:
            st.markdown(f"""
<div class="card" style="border-left:3px solid {elem_info.get('color','#8b7355')};">
    <div style="font-size:0.8rem;color:#b8860b;margin-bottom:0.3rem;">🌟 主导元素：{dominant[0]}象</div>
    <div style="font-size:0.9rem;font-weight:600;">推荐倾听者：{elem_char.get('icon','')} {elem_char.get('char','')}</div>
    <div style="font-size:0.85rem;color:#8b7355;">场景：{elem_char.get('scene','')} · {elem_char.get('theory','')}</div>
    <p style="line-height:1.8;margin-top:0.5rem;font-size:0.9rem;">{elem_char.get('desc','')}</p>
</div>
""", unsafe_allow_html=True)

        # 六大星体详情
        st.markdown("### 六大星体")
        planet_keys = ["太阳", "月亮", "水星", "金星", "火星", "上升"]
        planet_icons = {"太阳": "☀️", "月亮": "🌙", "水星": "💬", "金星": "💕", "火星": "🔥", "上升": "⬆️"}

        for key in planet_keys:
            p = chart.get(key, {})
            if not p:
                continue
            planet_info = PLANET_DESC.get(key, {})
            sign_name = p.get("sign", "")
            desc_text = planet_info.get("desc", {}).get(sign_name, "")

            st.markdown(f"""
<div class="card" style="padding:0.8rem 1rem;">
    <div style="display:flex;align-items:center;gap:0.5rem;">
        <span style="font-size:1.5rem;">{planet_icons.get(key,'')}</span>
        <div>
            <div style="font-weight:600;">{planet_info.get('name',key)} · {sign_name}</div>
            <div style="font-size:0.8rem;color:#8b7355;">{planet_info.get('label','')} · {p.get('elem','')}象</div>
        </div>
    </div>
    <p style="line-height:1.8;margin-top:0.5rem;font-size:0.9rem;color:#2c1810;">{desc_text}</p>
</div>
""", unsafe_allow_html=True)

        # 元素建议
        if elem_info:
            st.markdown(f"""
<div class="card" style="background:linear-gradient(135deg,#2c1810,#4a2c1a);color:#f5f0e8;">
    <div style="font-size:0.8rem;color:#b8860b;margin-bottom:0.3rem;">{elem_info.get('icon','')} {dominant[0]}象特质 · {elem_info.get('style','')}</div>
    <p style="line-height:1.8;font-size:0.9rem;">{elem_info.get('advice','')}</p>
</div>
""", unsafe_allow_html=True)

        # 操作
        if elem_char:
            scenes = elem_char.get("scene", "").split("/")
            chars = elem_char.get("char", "").split("/")
            if scenes and chars:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"💬 去找{chars[0]}聊聊", type="primary", use_container_width=True):
                        st.session_state.current_scene = scenes[0]
                        st.session_state.chat_character = chars[0]
                        st.session_state.chat_history = []
                        st.switch_page("pages/1_倾诉对话.py")
                with col2:
                    if st.button("🧠 MBTI测试", use_container_width=True):
                        st.switch_page("pages/5_心灵指引.py")
