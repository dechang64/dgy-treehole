"""MiniMax 音乐生成客户端（Token Plan 用户专用）

API: POST https://api.minimaxi.com/v1/music_generation
Model: music-2.6（Token Plan 用户用完整版，RPM更高）

注意：音乐生成是可选功能，不配置 MINIMAX_API_KEY 时该页面显示提示。
聊天功能使用 GLM API，两者独立。
"""

import requests
import tempfile
import os
from core.config import MINIMAX_API_KEY, MINIMAX_BASE_URL

# 音乐功能是否可用（独立于聊天 MOCK_MODE）
MUSIC_AVAILABLE = bool(MINIMAX_API_KEY)


def generate_music(
    prompt: str,
    place: str = "潇湘馆",
    mood: str = "宁静",
    is_instrumental: bool = True,
) -> str | None:
    """
    生成疗愈音乐

    Args:
        prompt: 音乐描述
        place: 场景名（用于生成提示词）
        mood: 情绪风格
        is_instrumental: 是否纯音乐

    Returns:
        音频文件路径，失败返回 None
    """
    if not MUSIC_AVAILABLE:
        return None

    full_prompt = f"中国传统乐器演奏的{mood}氛围音乐，{prompt}，{place}场景，空灵悠远，适合冥想放松"

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "music-2.6",  # Token Plan 用完整版
        "prompt": full_prompt,
        "is_instrumental": is_instrumental,
        "output_format": "url",  # 用 url 不用 hex，更稳定
        "aigc_watermark": False,
    }

    try:
        resp = requests.post(
            f"{MINIMAX_BASE_URL}/v1/music_generation",
            headers=headers,
            json=payload,
            timeout=180,  # 音乐生成需要更长时间
        )
        resp.raise_for_status()
        data = resp.json()

        # 检查响应状态
        base_resp = data.get("base_resp", {})
        if base_resp.get("status_code") != 0:
            return None

        music_data = data.get("data", {})
        if music_data.get("status") != 2:
            return None

        # 获取音频 URL 并下载
        audio_url = music_data.get("audio", "")
        if not audio_url:
            return None

        # 下载音频
        audio_resp = requests.get(audio_url, timeout=60)
        if audio_resp.status_code != 200:
            return None

        # 保存为临时文件
        tmp = tempfile.NamedTemporaryFile(
            suffix=".mp3", prefix=f"treehole_{place}_{mood}_", delete=False
        )
        tmp.write(audio_resp.content)
        tmp.close()
        return tmp.name

    except requests.exceptions.Timeout:
        return None
    except Exception:
        return None