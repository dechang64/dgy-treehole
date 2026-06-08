"""匿名树洞 — 释放心事，不留痕迹

设计原则：
- 释放即消失，内容不持久化
- 4种释放方式（风/湖/花/烟）
- 仅统计聚合数据用于联邦学习
- 与倾诉旅程串联：感知情绪上下文，给出个性化疗愈回复
"""

import random
import uuid
import requests
import tempfile
import streamlit as st
from core.config import RELEASE_METHODS, EMOTION_MUSIC_MAP, MUSIC_PLACES, MUSIC_MOODS
from core.emotion_detector import detect_emotion, compute_session_emotion_profile
from core.fl_engine import submit_local_stats
from core.db import record_treehole, get_treehole_stats

st.set_page_config(page_title="匿名树洞 · 大观园树洞", page_icon="🌳", layout="centered")
from core.styles import inject_css; inject_css()
# Layer 1: 树皮纹理背景
st.markdown('<div class="treehole-body">', unsafe_allow_html=True)

# GitHub Release — 音乐文件（同 music.py）
# GitHub Release — 音乐文件（同 music.py）
RELEASE_BASE = "https://github.com/dechang64/dgy-treehole/releases/download/v1.0-music"
# GitHub Release — ambient音效（同 Release）
RELEASE_AMBIENT_BASE = "https://github.com/dechang64/dgy-treehole/releases/download/v1.0-music"
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
    # ── 新增三院 ──
    "栊翠庵_宁静.mp3": "longcuian_ningjing.mp3",
    "栊翠庵_思念.mp3": "longcuian_sinian.mp3",
    "栊翠庵_欢愉.mp3": "longcuian_huanyu.mp3",
    "栊翠庵_沉思.mp3": "longcuian_chensi.mp3",
    "栊翠庵_疗愈.mp3": "longcuian_liaoyu.mp3",
    "栊翠庵_释然.mp3": "longcuian_shiran.mp3",
    "缀锦楼_宁静.mp3": "zhuilou_ningjing.mp3",
    "缀锦楼_思念.mp3": "zhuilou_sinian.mp3",
    "缀锦楼_欢愉.mp3": "zhuilou_huanyu.mp3",
    "缀锦楼_沉思.mp3": "zhuilou_chensi.mp3",
    "缀锦楼_疗愈.mp3": "zhuilou_liaoyu.mp3",
    "缀锦楼_释然.mp3": "zhuilou_shiran.mp3",
    "紫菱洲_宁静.mp3": "zilingzhou_ningjing.mp3",
    "紫菱洲_思念.mp3": "zilingzhou_sinian.mp3",
    "紫菱洲_欢愉.mp3": "zilingzhou_huanyu.mp3",
    "紫菱洲_沉思.mp3": "zilingzhou_chensi.mp3",
    "紫菱洲_疗愈.mp3": "zilingzhou_liaoyu.mp3",
    "紫菱洲_释然.mp3": "zilingzhou_shiran.mp3",
}


@st.cache_data(ttl=3600, show_spinner=False)
def get_audio_file(place: str, mood: str) -> str | None:
    chinese_name = f"{place}_{mood}.mp3"
    asset_name = FILENAME_MAP.get(chinese_name, chinese_name)
    url = f"{RELEASE_BASE}/{asset_name}"
    try:
        resp = requests.get(url, timeout=60, stream=True)
        resp.raise_for_status()
        tmp = tempfile.NamedTemporaryFile(
            suffix=".mp3", prefix=f"treehole_{place}_{mood}_", delete=False
        )
        for chunk in resp.iter_content(chunk_size=65536):
            tmp.write(chunk)
        tmp.close()
        return tmp.name
    except Exception:
        return None


@st.cache_data(ttl=86400, show_spinner=False)
def get_ambient_file(method: str) -> str | None:
    """下载 ambient音效文件用于释放动画"""
    url = f"{RELEASE_AMBIENT_BASE}/{method}.mp3"
    try:
        resp = requests.get(url, timeout=30, stream=True)
        resp.raise_for_status()
        tmp = tempfile.NamedTemporaryFile(
            suffix=".mp3", prefix=f"ambient_{method}_", delete=False
        )
        for chunk in resp.iter_content(chunk_size=32768):
            tmp.write(chunk)
        tmp.close()
        return tmp.name
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════
#  个性化疗愈回复引擎
# ═══════════════════════════════════════════════════════════

def get_healing_reply(emotion: str, personality_tone: str, word_count: int) -> str:
    """根据情绪 + 人格语气 + 内容长度生成个性化疗愈回复"""

    # 基础回复（按人格语气分组）
    tone_replies = {
        "gentle_listening": [
            "你愿意把这些话说出来，本身就是很勇敢的事。",
            "说出来就够了。你不需要解释，不需要辩护，只需要被听见。",
            "这些话藏在心里很久了吧。今天你说出来了，这就够了。",
        ],
        "warm": [
            "你已经很棒了。能承认自己的感受，本身就是一种力量。",
            "有些话不需要被理解，只需要被说出来。你做到了。",
            "你已经撑了很久了。今天，就让这些话有个出口吧。",
        ],
        "light": [
            "好，说出来了就好了。",
            "有些事情，说出来就不一样了。",
            "行了，剩下的交给风和湖水吧。",
        ],
        "guiding": [
            "你能识别自己的情绪，这很重要。你已经迈出了第一步。",
            "愿意面对自己的感受，本身就是成熟的标志。",
            "你不需要一个人扛。但今天，你选择了说出来——这很了不起。",
        ],
    }

    # 情绪补充（接在基础回复后）
    emotion_addons = {
        "悲伤": "悲伤不是软弱，它是爱过的证据。",
        "焦虑": "不安的时候，允许自己不安，就已经是在照顾自己了。",
        "愤怒": "有情绪是正常的。你的感受是真实的，不需要被评判。",
        "迷茫": "不知道方向也没关系。有时候，走着走着，路就出现了。",
        "疲惫": "你已经很努力了。今天，就让自己停一停吧。",
        "孤独": "孤独是一种感受，不是事实。你并不孤单。",
        "平静": "平静也是一种力量——它意味着你不需要依赖外界的回应。",
        "感恩": "能感受到感恩的人，内心一定是柔软的。",
        "期待": "有期待的人，说明还没有放弃。",
    }

    # 随机选一条基础回复
    tone_key = personality_tone if personality_tone in tone_replies else "warm"
    base = random.choice(tone_replies.get(tone_key, tone_replies["warm"]))

    # 情绪补充（悲伤/焦虑/疲惫优先触发，其他随机）
    addon = ""
    priority_emotions = ["悲伤", "焦虑", "疲惫", "愤怒"]
    if emotion in priority_emotions:
        addon = " " + random.choice([emotion_addons.get(e, "") for e in [emotion]])
    elif emotion in emotion_addons and random.random() > 0.4:
        addon = " " + random.choice([emotion_addons[emotion]])

    return (base + addon).strip()


def get_music_recommendation(emotion: str) -> tuple[str, str]:
    """根据情绪推荐音乐场景+情绪"""
    if emotion in EMOTION_MUSIC_MAP:
        mood = EMOTION_MUSIC_MAP[emotion]["primary"]
    else:
        mood = "疗愈"

    # 悲伤/孤独 → 怡红院（温暖），焦虑/疲惫 → 稻香村（宁静）
    # 执念 → 栊翠庵（放下），委屈 → 缀锦楼（边界），自卑 → 紫菱洲（自我悲悯）
    scene_map = {
        "悲伤": "怡红院",
        "孤独": "怡红院",
        "焦虑": "稻香村",
        "疲惫": "稻香村",
        "迷茫": "潇湘馆",
        "愤怒": "藕香榭",
        "平静": "稻香村",
        "感恩": "怡红院",
        "期待": "藕香榭",
        # ── 新增三院 ──
        "执念": "栊翠庵",
        "委屈": "缀锦楼",
        "自卑": "紫菱洲",
    }
    scene = scene_map.get(emotion, "稻香村")
    return scene, mood

# ── 初始化 session ──
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

# ── 返回 ──
if st.button("← 回到大观园", use_container_width=True):
    st.switch_page("app.py")

# ── 树洞 Hero：古槐内腔，月光从树缝漏下 ──
st.markdown("""
<div class="treehole-hero">
    <div class="moon">🌕</div>
    <h2>古 · 树 · 洞</h2>
    <p class="sub">把心事说给这棵千年老槐，让它替你记得</p>
    <div class="quote">
        <span class="falling-leaf">🍃</span>
        <span class="falling-leaf">🍂</span>
        <span class="falling-leaf">🍃</span>
        &nbsp;说出即放下，落地即归尘
    </div>
    <p style="font-size: 0.72rem; color: #8b7355; margin-top: 1rem;">
        🔒 你的话不会被存储 · 释放即消失
    </p>
    <p style="font-size: 0.68rem; color: #b8860b; margin-top: 0.3rem;">
        💡 想留下共鸣？去「🌸 匿名共鸣」发布
    </p>
</div>
""", unsafe_allow_html=True)

# ── 情绪上下文（来自倾诉旅程）──
chat_history = st.session_state.get("chat_history", [])
personality_tone = st.session_state.get("personality_params", {}).get("tone", "warm")
personality_source = st.session_state.get("personality_source", "")
current_scene = st.session_state.get("current_scene", "")
personality_tag = ""
if personality_source == "mbti":
    personality_tag = st.session_state.get("personality_type", "")

# 如果有对话历史，显示情绪上下文
if chat_history:
    profile = compute_session_emotion_profile(chat_history)
    if profile:
        top_emotion = max(profile, key=profile.get)
        top_score = profile[top_emotion]
        msg_count = len([m for m in chat_history if m.get("role") == "user"])

        context_lines = [f"你在{current_scene or '这里'}倾诉了 {msg_count} 句话"]
        if top_score > 0.3:
            context_lines.append(f"主要感到「{top_emotion}」（{top_score:.0%}）")

        context_text = "，".join(context_lines)

        if personality_tag:
            personality_tag_html = f'<span class="tag">{personality_tag}</span>'
        else:
            personality_tag_html = ""

        st.markdown(f"""
<div class="card" style="border-left: 3px solid #2d6a4f; padding: 0.8rem;">
    <div style="font-size: 0.78rem; color: #8b7355;">{context_text}{personality_tag_html}</div>
</div>
""", unsafe_allow_html=True)

# ── 输入 ──
treehole_text = st.text_area(
    "把你想说的话写在这里...",
    height=120,
    placeholder="这里只有你和风...",
    label_visibility="collapsed",
)

# ── 释放方式 ──
if treehole_text:
    st.markdown("### 选择释放方式")
    cols = st.columns(5)
    selected_method = None

    for i, (key, info) in enumerate(RELEASE_METHODS.items()):
        with cols[i]:
            if st.button(
                f"{info['icon']}\n{key}",
                key=f"release_{key}",
                use_container_width=True,
            ):
                selected_method = key

    # ── 释放动画 ──
    if selected_method:
        method_info = RELEASE_METHODS[selected_method]
        emotion = detect_emotion(treehole_text)

        # 记录树洞统计
        try:
            record_treehole(selected_method, emotion, len(treehole_text))
        except Exception:
            pass

        # 提交联邦学习统计（只提交情绪标签，不提交内容）
        try:
            submit_local_stats(
                st.session_state.session_id,
                {emotion: 1.0}
            )
        except Exception:
            pass

        # ── Layer 3: 静默模式 ──
        if selected_method == "silent":
            music_scene, music_mood = get_music_recommendation(emotion)
            audio_path = get_audio_file(music_scene, music_mood)

            st.markdown("""
<div style="text-align:center; padding: 2rem;" class="fade-in">
    <div style="font-size: 3.5rem;" class="gentle-float">🎧</div>
    <h3 style="color: #b8860b; margin-top: 1rem;">静静聆听</h3>
    <p style="color: #8b7355;">什么都不做，只是听</p>
</div>""", unsafe_allow_html=True)

            if audio_path:
                st.audio(audio_path, format="audio/mp3")
            else:
                st.warning("音乐加载失败，请检查网络后重试。")

            # 个性化疗愈回复
            reply = get_healing_reply(emotion, personality_tone, len(treehole_text))
            st.markdown(f"""
<div class="card" style="text-align:center; margin-top: 0.5rem;">
    <p style="font-style:italic; color: #8b7355; line-height: 1.8;">
        "{reply}"
    </p>
</div>
""", unsafe_allow_html=True)

            st.markdown(f"""
<div style="text-align:center; margin-top: 0.5rem;">
    <span style="font-size: 0.8rem; color: #8b7355;">为你推荐 · </span>
    <a href="/pages/4_music.py" target="_self">
        <button style="background-color: #2d6a4f; color: white; padding: 0.4rem 0.8rem; border: none; border-radius: 0.5rem; cursor: pointer; font-size: 0.8rem;">
            🎵 {music_scene} · {music_mood}
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

        else:
            # ── 普通释放动画 ──
            animations = {
                "wind": """
<div style="text-align:center; padding: 2rem;" class="fade-in">
    <div style="font-size: 4rem;" class="float">🍃</div>
    <h3 style="color: #2d6a4f; margin-top: 1rem;">已随风飘散</h3>
    <p style="color: #8b7355;">风会带走它</p>
</div>""",
                "lake": """
<div style="text-align:center; padding: 2rem;" class="fade-in">
    <div style="font-size: 4rem;" class="float">💧</div>
    <h3 style="color: #2d6a4f; margin-top: 1rem;">已沉入湖底</h3>
    <p style="color: #8b7355;">湖水会记住它</p>
</div>""",
                "petal": """
<div style="text-align:center; padding: 2rem;" class="fade-in">
    <div style="font-size: 4rem;" class="float">🌸</div>
    <h3 style="color: #c0392b; margin-top: 1rem;">已化为花瓣</h3>
    <p style="color: #8b7355;">花瓣会替你开</p>
</div>""",
                "smoke": """
<div style="text-align:center; padding: 2rem;" class="fade-in">
    <div style="font-size: 4rem;" class="float">🕯️</div>
    <h3 style="color: #8b7355; margin-top: 1rem;">已燃为青烟</h3>
    <p style="color: #8b7355;">烟会替你说</p>
</div>""",
            }

            st.markdown(animations[selected_method], unsafe_allow_html=True)

            # ── Layer 2: ambient音效（静默模式除外）──
            ambient_path = get_ambient_file(selected_method)
            if ambient_path:
                st.audio(ambient_path, format="audio/mp3")

            # 个性化疗愈回复
            reply = get_healing_reply(emotion, personality_tone, len(treehole_text))
            st.markdown(f"""
<div class="card" style="text-align:center; margin-top: 0.5rem;">
    <p style="font-style:italic; color: #8b7355; line-height: 1.8;">
        "{reply}"
    </p>
</div>
""", unsafe_allow_html=True)

            # 音乐推荐
            music_scene, music_mood = get_music_recommendation(emotion)
            st.markdown(f"""
<div style="text-align:center; margin-top: 0.8rem;">
    <span style="font-size: 0.8rem; color: #8b7355;">为你推荐 · </span>
    <a href="/pages/4_music.py" target="_self">
        <button style="background-color: #2d6a4f; color: white; padding: 0.4rem 0.8rem; border: none; border-radius: 0.5rem; cursor: pointer; font-size: 0.8rem;">
            🎵 {music_scene} · {music_mood}
        </button>
    </a>
</div>
""", unsafe_allow_html=True)

        if st.button("🏠 回到大观园", use_container_width=True):
            st.rerun()

# ── 树洞统计 ──
try:
    stats = get_treehole_stats()
except Exception:
    stats = {}
total_count = sum(v["count"] for v in stats.values()) if stats else 0
if total_count > 0:
    st.markdown("---")
    st.markdown(f"""
<div style="text-align:center; color: #8b7355; font-size: 0.8rem;">
    已有 <strong>{total_count}</strong> 位朋友在这里释放了心事<br>
    <span style="color: #b8860b;">联邦学习保护了每一位朋友的隐私</span>
</div>
""", unsafe_allow_html=True)

# 关闭树皮纹理 wrapper
st.markdown("</div>", unsafe_allow_html=True)
