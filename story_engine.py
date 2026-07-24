import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


try:
    from google import genai
except ImportError:
    genai = None


def get_ai_client():
    """
    Creates a Gemini AI client using a secure environment variable.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. "
            "Add it to Streamlit Secrets."
        )

    if genai is None:
        raise ImportError(
            "google-genai is not installed. "
            "Add google-genai to requirements.txt."
        )

    return genai.Client(
        api_key=api_key
    )


def calculate_story_structure(
    duration_minutes: int
) -> Dict[str, Any]:

    if duration_minutes <= 5:

        scenes = 10

    elif duration_minutes <= 10:

        scenes = 20

    elif duration_minutes <= 20:

        scenes = 35

    else:

        scenes = 50

    return {
        "duration_minutes": duration_minutes,
        "approximate_scenes": scenes,
        "acts": 3,
        "average_scene_duration_seconds": max(
            30,
            int(
                (duration_minutes * 60)
                / scenes
            )
        )
    }


def create_story_prompt(
    story_idea: str,
    duration_minutes: int,
    language: str = "English",
    genre: str = "Cinematic",
    visual_style: str = "Cinematic"
) -> str:

    structure = calculate_story_structure(
        duration_minutes
    )

    return f"""
You are an expert filmmaker, screenwriter,
story architect, and AI animation director.

Create a complete original {duration_minutes}-minute
cinematic movie based on the following idea:

STORY IDEA:
{story_idea}

LANGUAGE:
{language}

GENRE:
{genre}

VISUAL STYLE:
{visual_style}

MOVIE STRUCTURE:

Duration:
{duration_minutes} minutes

Approximate scenes:
{structure["approximate_scenes"]}

Acts:
{structure["acts"]}

Average scene duration:
{structure["average_scene_duration_seconds"]} seconds

STORY REQUIREMENTS:

1. Create a complete cinematic story with a strong beginning,
middle, climax, and satisfying ending.

2. Use a professional three-act structure:

ACT 1:
Introduction, world building, characters, and the main conflict.

ACT 2:
Rising conflict, emotional development, discoveries,
failures, challenges, and major turning points.

ACT 3:
Climax, final confrontation, emotional resolution,
and a satisfying ending.

3. Create detailed characters before creating scenes.

4. Maintain perfect character continuity throughout the movie.

Never randomly change:

- Face
- Hair
- Age
- Body type
- Clothing
- Personality
- Powers
- Weapons
- Relationships
- Character development

5. Maintain world continuity.

Locations, rules, powers, technology,
magic, mythology, and story logic must remain consistent.

6. Every scene must logically continue from the previous scene.

7. The story must feel like a professionally written movie,
not disconnected AI-generated clips.

8. If the language is Hindi,
all dialogue and narration must be written in Hindi.

9. Every scene must include:

- Scene number
- Scene title
- Act
- Duration
- Location
- Time of day
- Characters present
- Story purpose
- Action
- Character emotions
- Dialogue
- Narration
- Visual description
- Camera direction
- Lighting
- Environment animation
- Sound effects
- Background music
- Image generation prompt
- Animation prompt

10. Image prompts must maintain character consistency.

11. Animation prompts must describe realistic movement,
camera movement, environment animation, emotions,
lighting, and cinematic action.

12. The movie must contain emotional moments,
tension, surprises, memorable character moments,
and a powerful climax.

RETURN ONLY VALID JSON.

DO NOT RETURN MARKDOWN.

USE THIS EXACT JSON STRUCTURE:

{{
    "movie": {{
        "title": "",
        "logline": "",
        "duration_minutes": {duration_minutes},
        "language": "{language}",
        "genre": "{genre}",
        "visual_style": "{visual_style}"
    }},

    "world": {{
        "description": "",
        "rules": [],
        "locations": []
    }},

    "characters": [
        {{
            "name": "",
            "role": "",
            "age": "",
            "personality": "",
            "appearance": "",
            "clothing": "",
            "abilities": "",
            "character_arc": ""
        }}
    ],

    "acts": [
        {{
            "act_number": 1,
            "title": "",
            "purpose": "",
            "scene_numbers": []
        }},
        {{
            "act_number": 2,
            "title": "",
            "purpose": "",
            "scene_numbers": []
        }},
        {{
            "act_number": 3,
            "title": "",
            "purpose": "",
            "scene_numbers": []
        }}
    ],

    "scenes": [
        {{
            "scene_number": 1,
            "title": "",
            "act": 1,
            "duration_seconds": 0,
            "location": "",
            "time_of_day": "",
            "characters_present": [],
            "story_purpose": "",
            "action": "",
            "emotions": "",
            "dialogue": [],
            "narration": "",
            "visual_description": "",
            "camera_direction": "",
            "lighting": "",
            "environment_animation": "",
            "sound_effects": [],
            "background_music": "",
            "image_generation_prompt": "",
            "animation_prompt": ""
        }}
    ]
}}
"""


def generate_story(
    story_idea: str,
    duration_minutes: int,
    language: str = "English",
    genre: str = "Cinematic",
    visual_style: str = "Cinematic"
) -> Dict[str, Any]:

    if not story_idea.strip():

        raise ValueError(
            "Story idea cannot be empty."
        )

    client = get_ai_client()

    prompt = create_story_prompt(
        story_idea=story_idea,
        duration_minutes=duration_minutes,
        language=language,
        genre=genre,
        visual_style=visual_style
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    if not response or not response.text:

        raise ValueError(
            "Gemini returned an empty response."
        )

    response_text = response.text.strip()

    if response_text.startswith(
        "```json"
    ):

        response_text = response_text[
            7:
        ]

    elif response_text.startswith(
        "```"
    ):

        response_text = response_text[
            3:
        ]

    if response_text.endswith(
        "```"
    ):

        response_text = response_text[
            :-3
        ]

    response_text = response_text.strip()

    try:

        story_data = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Gemini returned invalid JSON. "
            f"Details: {error}"
        )

    return story_data


def save_story(
    story_data: Dict[str, Any],
    filename: str = "generated_story.json"
) -> str:

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            story_data,
            file,
            ensure_ascii=False,
            indent=4
        )

    return filename
