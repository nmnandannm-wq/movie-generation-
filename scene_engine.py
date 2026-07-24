import json
from typing import Dict, Any, List


def validate_story(story_data: Dict[str, Any]) -> None:
    """
    Checks whether the generated story contains
    the required movie structure.
    """

    if not isinstance(story_data, dict):
        raise ValueError("Story data must be a dictionary.")

    if "movie" not in story_data:
        raise ValueError("Story is missing the movie section.")

    if "characters" not in story_data:
        raise ValueError("Story is missing characters.")

    if "scenes" not in story_data:
        raise ValueError("Story is missing scenes.")

    if not isinstance(
        story_data["scenes"],
        list
    ):
        raise ValueError(
            "Scenes must be stored as a list."
        )


def create_character_bible(
    story_data: Dict[str, Any]
) -> Dict[str, Any]:

    validate_story(story_data)

    characters = story_data.get(
        "characters",
        []
    )

    character_bible = {}

    for character in characters:

        name = character.get(
            "name",
            "Unknown Character"
        )

        character_bible[name] = {
            "name": name,
            "role": character.get(
                "role",
                ""
            ),
            "age": character.get(
                "age",
                ""
            ),
            "personality": character.get(
                "personality",
                ""
            ),
            "appearance": character.get(
                "appearance",
                ""
            ),
            "clothing": character.get(
                "clothing",
                ""
            ),
            "abilities": character.get(
                "abilities",
                ""
            ),
            "character_arc": character.get(
                "character_arc",
                ""
            )
        }

    return character_bible


def create_world_bible(
    story_data: Dict[str, Any]
) -> Dict[str, Any]:

    validate_story(story_data)

    world = story_data.get(
        "world",
        {}
    )

    return {
        "description": world.get(
            "description",
            ""
        ),
        "rules": world.get(
            "rules",
            []
        ),
        "locations": world.get(
            "locations",
            []
        )
    }


def build_scene_context(
    scene: Dict[str, Any],
    character_bible: Dict[str, Any],
    world_bible: Dict[str, Any],
    previous_scene: Dict[str, Any] = None
) -> Dict[str, Any]:

    characters_present = scene.get(
        "characters_present",
        []
    )

    characters = []

    for character_name in characters_present:

        if character_name in character_bible:

            characters.append(
                character_bible[character_name]
            )

    context = {
        "scene_number": scene.get(
            "scene_number",
            0
        ),
        "title": scene.get(
            "title",
            ""
        ),
        "act": scene.get(
            "act",
            1
        ),
        "duration_seconds": scene.get(
            "duration_seconds",
            0
        ),
        "location": scene.get(
            "location",
            ""
        ),
        "time_of_day": scene.get(
            "time_of_day",
            ""
        ),
        "characters": characters,
        "world_rules": world_bible.get(
            "rules",
            []
        ),
        "story_purpose": scene.get(
            "story_purpose",
            ""
        ),
        "action": scene.get(
            "action",
            ""
        ),
        "emotions": scene.get(
            "emotions",
            ""
        ),
        "dialogue": scene.get(
            "dialogue",
            []
        ),
        "narration": scene.get(
            "narration",
            ""
        ),
        "visual_description": scene.get(
            "visual_description",
            ""
        ),
        "camera_direction": scene.get(
            "camera_direction",
            ""
        ),
        "lighting": scene.get(
            "lighting",
            ""
        ),
        "environment_animation": scene.get(
            "environment_animation",
            ""
        ),
        "sound_effects": scene.get(
            "sound_effects",
            []
        ),
        "background_music": scene.get(
            "background_music",
            ""
        ),
        "image_generation_prompt": scene.get(
            "image_generation_prompt",
            ""
        ),
        "animation_prompt": scene.get(
            "animation_prompt",
            ""
        )
    }

    if previous_scene:

        context["continuity"] = {
            "previous_scene_number": previous_scene.get(
                "scene_number",
                0
            ),
            "previous_location": previous_scene.get(
                "location",
                ""
            ),
            "previous_action": previous_scene.get(
                "action",
                ""
            ),
            "previous_emotions": previous_scene.get(
                "emotions",
                ""
            )
        }

    else:

        context["continuity"] = {
            "previous_scene_number": None,
            "previous_location": "",
            "previous_action": "",
            "previous_emotions": ""
        }

    return context


def prepare_scenes(
    story_data: Dict[str, Any]
) -> List[Dict[str, Any]]:

    validate_story(
        story_data
    )

    character_bible = create_character_bible(
        story_data
    )

    world_bible = create_world_bible(
        story_data
    )

    scenes = story_data.get(
        "scenes",
        []
    )

    prepared_scenes = []

    previous_scene = None

    for scene in scenes:

        scene_context = build_scene_context(
            scene=scene,
            character_bible=character_bible,
            world_bible=world_bible,
            previous_scene=previous_scene
        )

        prepared_scene = {
            "scene": scene,
            "context": scene_context
        }

        prepared_scenes.append(
            prepared_scene
        )

        previous_scene = scene

    return prepared_scenes


def save_prepared_scenes(
    prepared_scenes: List[Dict[str, Any]],
    filename: str = "prepared_scenes.json"
) -> str:

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            prepared_scenes,
            file,
            ensure_ascii=False,
            indent=4
        )

    return filename


def get_scene(
    prepared_scenes: List[Dict[str, Any]],
    scene_number: int
) -> Dict[str, Any]:

    for prepared_scene in prepared_scenes:

        scene = prepared_scene.get(
            "scene",
            {}
        )

        if scene.get(
            "scene_number"
        ) == scene_number:

            return prepared_scene

    raise ValueError(
        f"Scene {scene_number} was not found."
    )
