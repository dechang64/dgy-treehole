"""批量生成 4 个 ambient 音效（风/湖/花瓣/烟）
用法：确保 MINIMAX_API_KEY 环境变量已设置，然后运行：
    python scripts/batch_generate_ambient.py

生成后会自动打印 GitHub Release 上传命令。
"""
import os
import sys
import time
import requests
import tempfile

# ── 配置 ──
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
BASE_URL = "https://api.minimaxi.com"

AMBIENT_SOUNDS = [
    {
        "name": "wind",
        "filename": "wind.mp3",
        "prompt": "Gentle wind blowing through ancient Chinese garden trees, rustling leaves, soft natural ambient sound, no music, peaceful",
    },
    {
        "name": "lake",
        "filename": "lake.mp3",
        "prompt": "Serene lake water rippling gently, distant birds, natural pond ambience, calm and peaceful, no music, tranquil nature sound",
    },
    {
        "name": "petal",
        "filename": "petal.mp3",
        "prompt": "Cherry blossom petals falling softly through still air, delicate rustling sound, peaceful spring garden atmosphere, no music, gentle",
    },
    {
        "name": "smoke",
        "filename": "smoke.mp3",
        "prompt": "Candle flame crackling softly, incense smoke drifting in quiet room, gentle natural fire ambience, no music, meditative atmosphere",
    },
]


def generate_audio(prompt: str, timeout: int = 180) -> str | None:
    """调用 MiniMax 音频 API，返回本地文件路径"""
    if not MINIMAX_API_KEY:
        print("  ❌ MINIMAX_API_KEY 未设置")
        return None

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "music-2.6",
        "prompt": prompt,
        "is_instrumental": False,  # 环境音效不需要纯音乐标记
        "output_format": "url",
        "aigc_watermark": False,
    }

    print(f"  调用 MiniMax API...")
    resp = requests.post(
        f"{BASE_URL}/v1/music_generation",
        headers=headers,
        json=payload,
        timeout=timeout,
    )
    print(f"  响应状态: {resp.status_code}")
    resp.raise_for_status()
    data = resp.json()

    base_resp = data.get("base_resp", {})
    status_code = base_resp.get("status_code")
    if status_code != 0:
        print(f"  API错误: {base_resp}")
        return None

    music_data = data.get("data", {})
    status = music_data.get("status")
    print(f"  生成状态: {status}")

    if status == 1:
        # 需要轮询（音乐生成中）
        print("  生成中 (status=1)，MiniMax 需要30-60 秒，请稍候...")
        return None

    if status == 2:
        audio_url = music_data.get("audio", "")
        if not audio_url:
            print("  响应中无 audio URL")
            return None

        print(f"  下载音频: {audio_url[:60]}...")
        audio_resp = requests.get(audio_url, timeout=120)
        audio_resp.raise_for_status()
        print(f"  下载完成: {len(audio_resp.content):,} bytes")

        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", prefix="ambient_", delete=False)
        tmp.write(audio_resp.content)
        tmp.close()
        print(f"  保存至: {tmp.name}")
        return tmp.name

    print(f"  未知状态: {status}")
    return None


def main():
    if not MINIMAX_API_KEY:
        print("❌ 请先设置 MINIMAX_API_KEY 环境变量")
        print("   Windows PowerShell: $env:MINIMAX_API_KEY='你的key'")
        print("   macOS/Linux:       export MINIMAX_API_KEY='你的key'")
        sys.exit(1)

    print("🌿 开始生成 4 个 ambient 音效\n")

    for sound in AMBIENT_SOUNDS:
        print(f"── {sound['name']} ──")
        path = generate_audio(sound["prompt"])
        if path:
            # 重命名为规范名称
            out_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "static", "ambient"
            )
            os.makedirs(out_dir, exist_ok=True)
            out_path = os.path.join(out_dir, sound["filename"])
            os.rename(path, out_path)
            print(f"  ✅ → {out_path}")
        else:
            print(f" ⚠️  跳过（需要手动重试）")
        time.sleep(3)  # 避免 API限流

    print("\n✅ 完成！如需上传到 GitHub Release：")
    print("   1. git add static/ambient/")
    print("   2. git commit -m 'add ambient sound effects'")
    print("   3. git push")
    print("   4. 创建/更新 GitHub Release（将4 个 mp3 文件添加为 assets）")
    print("   5. 更新 pages/2_treehole.py 中的 RELEASE_AMBIENT_BASE URL")


if __name__ == "__main__":
    main()