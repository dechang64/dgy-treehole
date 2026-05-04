"""全局配置：API密钥、常量、环境检测"""

import os

# ── MiniMax API ──
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_GROUP_ID = os.environ.get("MINIMAX_GROUP_ID", "")
MINIMAX_BASE_URL = "https://api.minimaxi.com"

# ── 模型 ──
CHAT_MODEL = "MiniMax-Text-01"
MUSIC_MODEL = "music-2.6-free"

# ── 数据库 ──
DB_PATH = os.environ.get("TREEHOLE_DB_PATH", "treehole.db")

# ── 模式检测 ──
MOCK_MODE = not MINIMAX_API_KEY

# ── 设计令牌 ──
INK = "#2c1810"
PAPER = "#f5f0e8"
PAPER2 = "#e8dfd0"
RED = "#c0392b"
GOLD = "#b8860b"
JADE = "#2d6a4f"
MUTED = "#8b7355"

# ── 6大场景 ──
SCENES = [
    {"name": "潇湘馆", "char": "林黛玉", "icon": "🎋", "color": "#2d6a4f",
     "desc": "竹林深处，适合倾诉心事", "theory": "叙事疗法"},
    {"name": "蘅芜苑", "char": "薛宝钗", "icon": "🌿", "color": "#5a7d6b",
     "desc": "清幽雅致，适合理性梳理", "theory": "认知行为疗法"},
    {"name": "怡红院", "char": "贾宝玉", "icon": "🌸", "color": "#c0392b",
     "desc": "温暖包容，适合释放情绪", "theory": "人本主义疗法"},
    {"name": "稻香村", "char": "李纨", "icon": "🌾", "color": "#8b7355",
     "desc": "质朴宁静，适合沉淀思考", "theory": "正念疗法"},
    {"name": "藕香榭", "char": "史湘云", "icon": "🪷", "color": "#d4a574",
     "desc": "开阔明亮，适合畅所欲言", "theory": "积极心理学"},
    {"name": "秋爽斋", "char": "探春", "icon": "🍂", "color": "#a0522d",
     "desc": "爽朗明快，适合寻求方向", "theory": "焦点解决疗法"},
]

SCENE_MAP = {s["name"]: s for s in SCENES}

# ── 树洞释放方式 ──
RELEASE_METHODS = {
    "wind":  {"icon": "🍃", "title": "已随风飘散", "sub": "风会带走它"},
    "lake":  {"icon": "💧", "title": "已沉入湖底", "sub": "湖水会记住它"},
    "petal": {"icon": "🌸", "title": "已化为花瓣", "sub": "花瓣会替你开"},
    "smoke": {"icon": "🕯️", "title": "已燃为青烟", "sub": "烟会替你说"},
}

# ── 情绪分类 ──
EMOTIONS = ["悲伤", "焦虑", "愤怒", "迷茫", "疲惫", "孤独", "平静", "感恩", "期待"]

# ── 音乐场景 ──
MUSIC_PLACES = ["潇湘馆", "蘅芜苑", "怡红院", "稻香村", "藕香榭", "秋爽斋"]
MUSIC_MOODS = ["宁静", "释然", "思念", "疗愈", "欢愉", "沉思"]
