"""全局配置：API密钥、常量、环境检测"""

import os

# ── GLM API（智谱AI，OpenAI 兼容格式）──
GLM_API_KEY = os.environ.get("GLM_API_KEY", "")
GLM_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"

# ── MiniMax API（仅用于音乐生成，可选）──
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimaxi.com"

# ── 模型 ──
CHAT_MODEL = "glm-4-flash"          # GLM 免费模型，速度快，适合对话
# MUSIC_MODEL 已移除，请在 minimax_music.py 中使用 "music-2.6"（Token Plan 用户）

# ── 数据库（Streamlit Cloud 无持久文件系统，用内存数据库）──
DB_PATH = os.environ.get("TREEHOLE_DB_PATH", ":memory:")

# ── 模式检测 ──
MOCK_MODE = not GLM_API_KEY

# ── 设计令牌 ──
INK = "#2c1810"
PAPER = "#f5f0e8"
PAPER2 = "#e8dfd0"
RED = "#c0392b"
GOLD = "#b8860b"
JADE = "#2d6a4f"
MUTED = "#8b7355"

# ── 9大场景（6 经典 + 3 新增：栊翠庵/缀锦楼/紫菱洲）──
SCENES = [
    {"name": "潇湘馆", "icon": "🎋", "desc": "竹林深处，月影斑驳",
     "mood": "孤独、思念", "char": "林黛玉", "theory": "叙事疗法",
     "style": "倾听你的心事", "color": "#2d6a4f"},
    {"name": "蘅芜苑", "icon": "🌿", "desc": "幽香弥漫，清冷如月",
     "mood": "迷茫、压抑", "char": "薛宝钗", "theory": "认知行为疗法",
     "style": "理性帮你理清", "color": "#5a7d6b"},
    {"name": "怡红院", "icon": "🌸", "desc": "花团锦簇，温暖如春",
     "mood": "焦虑、不安", "char": "贾宝玉", "theory": "人本主义",
     "style": "温柔化解不安", "color": "#c0392b"},
    {"name": "稻香村", "icon": "🌾", "desc": "田园宁静，炊烟袅袅",
     "mood": "疲惫、倦怠", "char": "李纨", "theory": "正念+ACT",
     "style": "安静的陪伴", "color": "#8b7355"},
    {"name": "藕香榭", "icon": "🪷", "desc": "碧水清波，荷香四溢",
     "mood": "纠结、犹豫", "char": "史湘云", "theory": "积极心理学",
     "style": "大大方方翻篇", "color": "#d4a574"},
    {"name": "秋爽斋", "icon": "📜", "desc": "窗明几净，笔墨书香",
     "mood": "愤怒、不满", "char": "探春", "theory": "赋权+SFBT",
     "style": "陪你把话说清楚", "color": "#a0522d"},
    # ── 新增三院 ──
    {"name": "栊翠庵", "icon": "🪷", "desc": "古柏青灯，禅房清寂",
     "mood": "执念、完美", "char": "妙玉", "theory": "正念禅修",
     "style": "教你放下", "color": "#7d6b5d"},
    {"name": "缀锦楼", "icon": "🎨", "desc": "绣帘半卷，针线生辉",
     "mood": "内耗、委屈", "char": "惜春", "theory": "艺术疗法+边界",
     "style": "把话绣出来", "color": "#b87a8a"},
    {"name": "紫菱洲", "icon": "🫧", "desc": "菱花照水，波光柔软",
     "mood": "自卑、隐忍", "char": "迎春", "theory": "自我悲悯+ACT",
     "style": "温柔地抱住你", "color": "#a8c4d4"},
]

SCENE_MAP = {s["name"]: s for s in SCENES}

# ── 树洞释放方式 ──
RELEASE_METHODS = {
    "wind":  {"icon": "🍃", "title": "已随风飘散", "sub": "风会带走它"},
    "lake":  {"icon": "💧", "title": "已沉入湖底", "sub": "湖水会记住它"},
    "petal": {"icon": "🌸", "title": "已化为花瓣", "sub": "花瓣会替你开"},
    "smoke": {"icon": "🕯️", "title": "已燃为青烟", "sub": "烟会替你说"},
    "silent":{"icon": "🎧", "title": "静静聆听",     "sub": "什么都不做，只是听"},
}

# ── 情绪分类 ──
EMOTIONS = ["悲伤", "焦虑", "愤怒", "迷茫", "疲惫", "孤独", "平静",
            "感恩", "期待", "执念", "委屈", "自卑"]

# ── 音乐场景 ──
MUSIC_PLACES = ["潇湘馆", "蘅芜苑", "怡红院", "稻香村", "藕香榭", "秋爽斋",
                "栊翠庵", "缀锦楼", "紫菱洲"]
MUSIC_MOODS = ["宁静", "释然", "思念", "疗愈", "欢愉", "沉思"]

# ═══════════════════════════════════════════════════════════
#  MBTI → 疗愈偏好参数（贯穿整个旅程）
# ═══════════════════════════════════════════════════════════
MBTI_PARAMS = {
    # I — 内向 / 深度，N — 直觉 / 意义
    "INFP": {"tone": "gentle_listening", "reply_length": "medium_long",
             "music_mood": "reflective", "approach": "narrative"},
    "INFJ": {"tone": "guiding", "reply_length": "medium",
             "music_mood": "serene", "approach": "cbt"},
    # E — 外向 / 能量
    "ENFP": {"tone": "light", "reply_length": "medium",
             "music_mood": "uplifting", "approach": "positive"},
    "ENFJ": {"tone": "warm", "reply_length": "medium",
             "music_mood": "warm", "approach": "humanistic"},
    # 理性分析型
    "INTJ": {"tone": "guiding", "reply_length": "medium",
             "music_mood": "meditative", "approach": "cbt"},
    "INTP": {"tone": "guiding", "reply_length": "medium_long",
             "music_mood": "meditative", "approach": "cbt"},
    "ENTJ": {"tone": "guiding", "reply_length": "short",
             "music_mood": "uplifting", "approach": "empowering"},
    "ENTP": {"tone": "light", "reply_length": "short",
             "music_mood": "uplifting", "approach": "positive"},
    # 实际感受型
    "ISFP": {"tone": "gentle_listening", "reply_length": "medium_long",
             "music_mood": "reflective", "approach": "narrative"},
    "ISFJ": {"tone": "warm", "reply_length": "medium_long",
             "music_mood": "warm", "approach": "mindfulness"},
    "ESFP": {"tone": "light", "reply_length": "short",
             "music_mood": "uplifting", "approach": "positive"},
    "ESFJ": {"tone": "warm", "reply_length": "medium",
             "music_mood": "warm", "approach": "humanistic"},
    "ISTP": {"tone": "guiding", "reply_length": "short",
             "music_mood": "serene", "approach": "empowering"},
    "ISTJ": {"tone": "guiding", "reply_length": "medium",
             "music_mood": "serene", "approach": "cbt"},
    "ESTP": {"tone": "light", "reply_length": "short",
             "music_mood": "uplifting", "approach": "positive"},
    "ESTJ": {"tone": "guiding", "reply_length": "short",
             "music_mood": "serene", "approach": "empowering"},
}

# ═══════════════════════════════════════════════════════════
#  星座元素 → 疗愈偏好参数
# ═══════════════════════════════════════════════════════════
ELEM_PARAMS = {
    "火": {"tone": "light", "reply_length": "short",
           "music_mood": "uplifting", "approach": "positive"},
    "土": {"tone": "warm", "reply_length": "medium_long",
           "music_mood": "warm", "approach": "mindfulness"},
    "风": {"tone": "light", "reply_length": "short",
           "music_mood": "uplifting", "approach": "positive"},
    "水": {"tone": "gentle_listening", "reply_length": "medium_long",
           "music_mood": "reflective", "approach": "narrative"},
}

# ═══════════════════════════════════════════════════════════
#  情绪 → 场景推荐（首页入口用）
# ═══════════════════════════════════════════════════════════
EMOTION_SCENE_MAP = {
    "悲伤":  {"scene": "潇湘馆", "icon": "🎋", "msg": "有些话，潇湘馆的竹叶愿意听"},
    "焦虑":  {"scene": "稻香村", "icon": "🌾", "msg": "稻香村很安静，适合你降降速"},
    "愤怒":  {"scene": "藕香榭", "icon": "🪷", "msg": "藕香榭的水波，能帮你把火气散开"},
    "迷茫":  {"scene": "秋爽斋", "icon": "📜", "msg": "秋爽斋的探春，擅长帮人理清方向"},
    "疲惫":  {"scene": "稻香村", "icon": "🌾", "msg": "你累了。稻香村适合安静地待一会儿"},
    "孤独":  {"scene": "怡红院", "icon": "🌸", "msg": "怡红院很暖，有人愿意陪你坐坐"},
    "平静":  {"scene": "稻香村", "icon": "🌾", "msg": "平静也是一种力量。稻香村适合你"},
    "感恩":  {"scene": "怡红院", "icon": "🌸", "msg": "怡红院很适合这份温暖"},
    "期待":  {"scene": "藕香榭", "icon": "🪷", "msg": "藕香榭的阳光，和你的期待很配"},
    # ── 新增三院 ──
    "执念":  {"scene": "栊翠庵", "icon": "🪷", "msg": "栊翠庵的青灯下，没有放不下的事"},
    "委屈":  {"scene": "缀锦楼", "icon": "🎨", "msg": "缀锦楼很安静，可以把说不出口的话绣出来"},
    "自卑":  {"scene": "紫菱洲", "icon": "🫧", "msg": "紫菱洲的水很温柔，先把自己抱住"},
}

# ═══════════════════════════════════════════════════════════
#  情绪 → 音乐情绪推荐（主情绪优先，次情绪辅助）
# ═══════════════════════════════════════════════════════════
EMOTION_MUSIC_MAP = {
    "悲伤":   {"primary": "疗愈", "secondary": "沉思"},
    "焦虑":   {"primary": "宁静", "secondary": "沉思"},
    "愤怒":   {"primary": "释然", "secondary": "欢愉"},
    "迷茫":   {"primary": "沉思", "secondary": "宁静"},
    "疲惫":   {"primary": "疗愈", "secondary": "宁静"},
    "孤独":   {"primary": "疗愈", "secondary": "宁静"},
    "平静":   {"primary": "宁静", "secondary": "沉思"},
    "感恩":   {"primary": "欢愉", "secondary": "疗愈"},
    "期待":   {"primary": "欢愉", "secondary": "释然"},
    # ── 新增三院 ──
    "执念":   {"primary": "沉思", "secondary": "释然"},
    "委屈":   {"primary": "疗愈", "secondary": "思念"},
    "自卑":   {"primary": "思念", "secondary": "疗愈"},
}

# ═══════════════════════════════════════════════════════════
#  疗愈偏好 → 音乐氛围推荐（personality params 的 music_mood）
# ═══════════════════════════════════════════════════════════
MUSIC_MOOD_MUSIC_MAP = {
    "serene":     "宁静",
    "warm":       "疗愈",
    "meditative": "沉思",
    "uplifting":  "欢愉",
    "reflective": "思念",
}
