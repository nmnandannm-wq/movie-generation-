import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

try:
    import fal_client
except ImportError:
    fal_client = None


VIDEO_MODEL = "fal-ai/wan-t2v"
IMAGE_VIDEO_MODEL = "fal-ai/wan-i2v"


def check_fal_key():
    api_key = os.getenv("FAL_KEY")

    if not api_key:
        raise ValueError(
            "FAL_KEY is missing. Add it to your .env file."
        )

    if fal_client is None:
        raise ImportError(
            "fal-client is not installed."
        )


def download_video(
    video_url: str,
    output_path: str
) -> str:

    response = requests.get(
        video_url,
        timeout=300
    )

    response.raise_for_status()

    with open(
        output_path,
        "wb"
    ) as file:

        file.write(
            response.content
        )

    return output_path


def generate_video_clip(
    prompt: str,
    output_path: str,
    negative_prompt: str = "",
    aspect_ratio: str = "16:9"
) -> dict:

    check_fal_key()

    if not prompt.strip():
        raise ValueError(
            "Video prompt cannot be empty."
        )

    result = fal_client.subscribe(
        VIDEO_MODEL,
        arguments={
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "aspect_ratio": aspect_ratio
        }
    )

    video_data = result.get(
        "video"
    )

    if not video_data:
        raise ValueError(
            "Video generation returned no video."
        )

    video_url = video_data.get(
        "url"
    )

    if not video_url:
        raise ValueError(
            "Video URL was not returned."
        )

    download_video(
        video_url,
        output_path
    )

    return {
        "success": True,
        "video_url": video_url,
        "local_path": output_path
    }


def generate_scene_video(
    scene: dict,
    output_folder: str = "generated_videos"
) -> dict:

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    scene_number = scene.get(
        "scene_number",
        1
    )

    prompt = scene.get(
        "animation_prompt",
        ""
    )

    if not prompt:

        prompt = scene.get(
            "visual_description",
            ""
        )

    output_path = os.path.join(
        output_folder,
        f"scene_{scene_number:03d}.mp4"
    )

    return generate_video_clip(
        prompt=prompt,
        output_path=output_path,
        negative_prompt=(
            "blurry, low quality, distorted anatomy, "
            "extra fingers, bad hands, deformed face, "
            "flickering, unstable camera"
        )
    )
