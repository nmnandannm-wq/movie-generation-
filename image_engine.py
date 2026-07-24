import os
import requests
from dotenv import load_dotenv

load_dotenv()


def check_image_api_key():

    api_key = os.getenv(
        "FAL_KEY"
    )

    if not api_key:

        raise ValueError(
            "FAL_KEY is missing."
        )

    return api_key


def download_image(
    image_url: str,
    output_path: str
) -> str:

    response = requests.get(
        image_url,
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


def create_scene_image_prompt(
    scene: dict
) -> str:

    character_details = scene.get(
        "characters",
        []
    )

    visual_description = scene.get(
        "visual_description",
        ""
    )

    lighting = scene.get(
        "lighting",
        ""
    )

    location = scene.get(
        "location",
        ""
    )

    return (
        "Create a high-quality cinematic movie frame. "
        f"Location: {location}. "
        f"Characters: {character_details}. "
        f"Visual description: {visual_description}. "
        f"Lighting: {lighting}. "
        "Maintain consistent character appearance, "
        "clothing, face, body proportions and visual style. "
        "Professional cinematic composition, detailed "
        "environment, high-quality production design."
    )


def save_image_prompt(
    scene: dict,
    output_path: str
) -> str:

    prompt = create_scene_image_prompt(
        scene
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            prompt
        )

    return output_path
