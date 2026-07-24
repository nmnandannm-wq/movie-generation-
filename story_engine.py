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
    Creates the Google Gemini AI client.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )

    if genai is None:
        raise ImportError(
            "google-genai is not installed. "
            "Run: pip install google-genai"
        )

    return genai.Client(api_key=api_key)


def calculate_story_structure(duration_minutes: int) -> Dict[str, Any]:
    """
    Calculates the approximate story structure
    based on the requested movie duration.
    """

    if duration_minutes <= 5:
        scenes = 10
        acts = 3

    elif duration_minutes <= 10:
        scenes = 20
        acts = 3

    elif duration_minutes <= 20:
        scenes = 35
        acts = 3

    else:
        scenes = 50
        acts = 3

    return {
        "duration_minutes": duration_minutes,
        "approximate_scenes": scenes,
        "acts": acts,
        "average_scene_duration_seconds": int(
            (duration_minutes * 60) / scenes
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
cinematic movie based on this idea:

STORY IDEA:
{story_idea}

LANGUAGE:
{language}

GENRE:
{genre}

VISUAL STYLE:
{visual_style}

MOVIE STRUCTURE:
The movie must contain approximately
{structure["approximate_scenes"]} scenes divided into
{structure["acts"]} acts.

The average scene duration should be approximately
{structure["average_scene_duration_seconds"]} seconds.

IMPORTANT STORY REQUIREMENTS:

1. Create a strong beginning, middle, and ending.

2. Build a complete cinematic story with:
   - Introduction
   - Character development
   - Conflict
   - Rising tension
   - Emotional moments
   - Major turning points
   - Climax
   - Resolution

3. Maintain character continuity throughout the entire story.

4. Do not randomly change:
   - Character appearance
   - Character personality
   - Clothing
   - Powers
   - Relationships
   - Locations
   - Story rules

5. Every scene must logically continue from
   the previous scene.

6. Create detailed characters before creating scenes.

7. Create a detailed world and its rules.

8. Every scene must include:
   - Scene number
   - Scene title
   - Act
   - Location
   - Time of day
   - Characters present
   - Story purpose
   - Action
   - Character emotions
   - Dialogue
   - Narration if required
   - Visual description
   - Camera direction
   - Lighting
   - Environment movement
   - Sound effects
   - Background music
   - Image generation prompt
   - Animation prompt

9. The movie must feel like a professionally written
cinematic film and not like disconnected AI-generated clips.

10. If the language is Hindi, all dialogues and narration
must be written in Hindi.

RETURN ONLY VALID JSON.

Use this exact JSON structure:

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
            "scenes": []
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

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

    try:
        story_data = json.loads(
            response_text
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            f"AI returned invalid JSON: {error}"
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
