"""AMAX Token Router 聊天客户端（OpenAI 兼容格式）

API: POST https://api.amaxapi.com/v1/chat/completions
Model: deepseek-v3 (默认) / gpt-4o-mini / glm-4-flash / claude-3-5-haiku ...

2026-06-10: 切换到 AMAX Token Router（MiniMax key 全失效后的回退方案）
"""
import requests
import logging
from core.config import AMAX_API_KEY, AMAX_BASE_URL, AMAX_CHAT_MODEL

logger = logging.getLogger(__name__)

# 配置
MOCK_MODE = not AMAX_API_KEY
DEFAULT_MODEL = AMAX_CHAT_MODEL


def chat(
    messages: list[dict],
    character: str = "贾宝玉",
    personality_params: dict | None = None,
    temperature: float = 0.7,
    max_tokens: int = 300,
) -> str:
    """
    发送聊天请求到 MiniMax API。

    Args:
        messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
        character: 角色名（用于 system prompt 注入）
        personality_params: MBTI/星座人格参数

    Returns:
        AI 回复文本
    """
    if MOCK_MODE:
        return _mock_response(character, messages, personality_params)

    from core.characters import get_character, build_system_prompt

    system_prompt = build_system_prompt(character, personality_params)

    # MiniMax API 用 sender_type + text，不是标准 messages 格式
    # 但 chatcompletion_v2 支持 messages 格式（类似 OpenAI）
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", msg.get("text", ""))
        if role != "system" and content:
            # 转换 role 名（OpenAI: system/user/assistant; MiniMax: USER/BOT）
            mapped_role = {"user": "user", "assistant": "assistant"}.get(role, "user")
            api_messages.append({"role": mapped_role, "content": content})

    headers = {
        "Authorization": f"Bearer {AMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    # AMAX: OpenAI 兼容 /v1/chat/completions
    payload = {
        "model": DEFAULT_MODEL,
        "messages": api_messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
    }

    url = f"{AMAX_BASE_URL}/v1/chat/completions"

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        # AMAX (OpenAI 兼容) — 业务错误也走 base_resp（如果路由有包装）
        base_resp = data.get("base_resp", {})
        status_code = base_resp.get("status_code", 0) if base_resp else 0
        if status_code != 0:
            status_msg = base_resp.get("status_msg", "")
            logger.error(f"AMAX API error: {status_code} - {status_msg}")

            if status_code in (1004, 1000, 1001, 1002):
                logger.warning(f"AMAX key issue ({status_code}), falling back to mock for this turn")
                mock = _mock_response(character, messages, personality_params)
                return f"💭 *（AI 暂未连接,先用温柔模板陪着你）*\n\n{mock}"

            return f"（服务暂时不可用，错误：{status_code}）"

        # 解析回复 — AMAX OpenAI 兼容格式
        choices = data.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            content = msg.get("content", "").strip()
            if content:
                return content

        # 兜底
        logger.error(f"AMAX empty response: {data}")
        return "（AI 这次没说话,可能网络抖动,再试一次？）"

    except requests.exceptions.Timeout:
        return "（网络超时，请稍后再试。）"
    except requests.exceptions.HTTPError as e:
        code = e.response.status_code if e.response else 0
        body = e.response.text if e.response else ''
        logger.error(f"AMAX HTTP error: {code} - {body[:200]}")
        if code == 429:
            return "（请求太频繁了，请稍等片刻再试。）"
        if code in (401, 403):
            mock = _mock_response(character, messages, personality_params)
            return f"💭 *（AI 暂未连接,先用温柔模板陪着你）*\n\n{mock}"
        return f"（服务暂时不可用，错误：{code}）"
    except requests.exceptions.ConnectionError as e:
        # Cloud 连不上 AMAX（DNS/网络/被墙）→ mock 兜底
        logger.error(f"AMAX connection error: {e}")
        mock = _mock_response(character, messages, personality_params)
        return f"💭 *（AI 暂未连接,先用温柔模板陪着你）*\n\n{mock}"
    except Exception as e:
        logger.error(f"AMAX unexpected error: {type(e).__name__}: {e}")
        mock = _mock_response(character, messages, personality_params)
        return f"💭 *（AI 暂未连接,先用温柔模板陪着你）*\n\n{mock}"


def _mock_response(character: str, messages: list[dict], personality_params: dict | None = None) -> str:
    """Mock 模式：基于关键词的简单回复（无 API Key 时 fallback）"""
    from core.characters import get_character

    char_info = get_character(character)
    user_msgs = [m["content"] for m in messages if m["role"] == "user"]
    last_msg = user_msgs[-1] if user_msgs else ""

    sad_words = ["难过", "伤心", "哭", "悲伤", "心痛", "难受", "委屈", "不开心"]
    anxious_words = ["焦虑", "紧张", "害怕", "担心", "压力", "崩溃"]
    angry_words = ["生气", "愤怒", "讨厌", "恨", "烦", "气"]
    lost_words = ["迷茫", "不知道", "方向", "意义", "为什么"]
    tired_words = ["累", "疲惫", "撑不住", "加班", "熬夜"]

    is_sad = any(w in last_msg for w in sad_words)
    is_anxious = any(w in last_msg for w in anxious_words)
    is_angry = any(w in last_msg for w in angry_words)
    is_lost = any(w in last_msg for w in lost_words)
    is_tired = any(w in last_msg for w in tired_words)

    tone = (personality_params or {}).get("tone", "warm")
    short_tones = {"light", "guiding"}
    gentle_tones = {"gentle_listening"}

    if is_sad:
        base = f"我是{character}，我听到了。你的难过是真实的，不需要假装没事。"
        extra = "……你愿意多说一些吗？" if tone in gentle_tones else "你愿意告诉我发生了什么吗？"
        return base + "\n\n" + extra
    elif is_anxious:
        if tone in short_tones:
            return f"{character}说：深呼吸。焦虑是在告诉你——这件事对你很重要。先让自己安定下来，再想怎么办。"
        return f"深呼吸。你现在感受到的焦虑，是你的身体在告诉你——这件事对你很重要。\n\n不用急着解决，先让自己安定下来。"
    elif is_angry:
        return f"{character}听到了：你的愤怒是合理的。不公平的事情确实让人难以接受。\n\n你愿意告诉我发生了什么吗？我在听。"
    elif is_lost:
        if tone in short_tones:
            return f"{character}说：迷茫的时候，不需要立刻找到方向。你最近在纠结什么？"
        return f"迷茫的时候，不需要立刻找到方向。有时候，承认\"我不知道\"本身就需要勇气。\n\n你最近在纠结什么？"
    elif is_tired:
        return f"你已经很努力了。累的时候，允许自己停下来休息，这不是软弱。\n\n你有多久没有好好休息了？"
    else:
        return f"嗯，我是{character}，我在听。你说的每一句话，我都认真对待。\n\n你还有什么想说的吗？"
