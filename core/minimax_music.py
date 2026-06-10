"""MiniMax 音乐生成客户端（Token Plan 用户专用）

API: POST https://api.minimaxi.com/v1/music_generation
Model: music-2.6（Token Plan 用户用完整版，RPM更高）

2026-06-09: 改用 MINIMAX_MUSIC_API_KEY（独立于 chat key），
如果没设，自动 fallback 到 MINIMAX_API_KEY（Token Plan 全功能场景）。
"""
import requests
import tempfile
import os
import logging
from core.config import MINIMAX_MUSIC_API_KEY, MINIMAX_BASE_URL

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 音乐功能是否可用
MUSIC_AVAILABLE = bool(MINIMAX_MUSIC_API_KEY)


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
        logger.warning("MINIMAX_MUSIC_API_KEY not configured")
        return None

    full_prompt = f"中国传统乐器演奏的{mood}氛围音乐，{prompt}，{place}场景，空灵悠远，适合冥想放松"

    headers = {
        "Authorization": f"Bearer {MINIMAX_MUSIC_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "music-2.6",  # Token Plan 用完整版
        "prompt": full_prompt,
        "is_instrumental": is_instrumental,
        "output_format": "url",
        "aigc_watermark": False,
    }

    try:
        # 先用短超时获取响应
        logger.info("Calling MiniMax music API...")
        resp = requests.post(
            f"{MINIMAX_BASE_URL}/v1/music_generation",
            headers=headers,
            json=payload,
            timeout=180,
        )
        logger.info(f"API response status: {resp.status_code}")

        resp.raise_for_status()
        data = resp.json()
        logger.info(f"API response: {data}")

        # 检查响应状态
        base_resp = data.get("base_resp", {})
        status_code = base_resp.get("status_code")
        if status_code != 0:
            logger.error(f"API error: {base_resp}")
            return None

        music_data = data.get("data", {})
        status = music_data.get("status")
        logger.info(f"Music generation status: {status}")

        if status == 1:
            # 还在生成中，需要轮询
            logger.info("Music is being generated, waiting...")
            return None  # Streamlit Cloud 不支持轮询，直接返回

        if status == 2:
            # 生成完成
            audio_url = music_data.get("audio", "")
            if not audio_url:
                logger.error("No audio URL in response")
                return None

            logger.info(f"Downloading audio from: {audio_url[:50]}...")

            # 下载音频
            audio_resp = requests.get(audio_url, timeout=120)
            if audio_resp.status_code != 200:
                logger.error(f"Failed to download audio: {audio_resp.status_code}")
                return None

            logger.info(f"Downloaded {len(audio_resp.content)} bytes")

            # 保存为临时文件
            tmp = tempfile.NamedTemporaryFile(
                suffix=".mp3", prefix=f"treehole_{place}_{mood}_", delete=False
            )
            tmp.write(audio_resp.content)
            tmp.close()
            logger.info(f"Saved to: {tmp.name}")
            return tmp.name

        logger.error(f"Unknown status: {status}")
        return None

    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return None
    except Exception as e:
        logger.error(f"Error: {type(e).__name__}: {e}")
        return None