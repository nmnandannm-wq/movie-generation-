import os
import json
from typing import Dict, Any


def create_audio_plan(
    scene: Dict[str, Any]
) -> Dict[str, Any]:

    return {
        "scene_number": scene.get(
            "scene_number",
            0
        ),

        "dialogue": scene.get(
            "dialogue",
            []
        ),

        "narration": scene.get(
            "narration",
            ""
        ),

        "background_music": scene.get(
            "background_music",
            ""
        ),

        "sound_effects": scene.get(
            "sound_effects",
            []
        )
    }


def prepare_movie_audio_plan(
    scenes: list
) -> list:

    audio_plan = []

    for scene in scenes:

        audio_plan.append(
            create_audio_plan(
                scene
            )
        )

    return audio_plan


def save_audio_plan(
    audio_plan: list,
    output_path: str = "audio_plan.json"
) -> str:

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            audio_plan,
            file,
            ensure_ascii=False,
            indent=4
        )

    return output_path
