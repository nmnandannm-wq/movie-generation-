import streamlit as st
import json
import os
import traceback

from story_engine import generate_story
from scene_engine import prepare_scenes
from audio_engine import prepare_movie_audio_plan


try:
    from video_engine import generate_scene_video
    VIDEO_ENGINE_AVAILABLE = True
except Exception:
    VIDEO_ENGINE_AVAILABLE = False


st.set_page_config(
    page_title="VisionCraft AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>

    .stApp {
        background: #08090d;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background: #0d0f15;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        color: #8d93a1;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%;
        min-height: 45px;
        border-radius: 10px;
        font-weight: 700;
    }

    .story-card {
        background: #11141b;
        border: 1px solid #242833;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


if "story_data" not in st.session_state:
    st.session_state.story_data = None

if "prepared_scenes" not in st.session_state:
    st.session_state.prepared_scenes = None

if "audio_plan" not in st.session_state:
    st.session_state.audio_plan = None

if "generated_videos" not in st.session_state:
    st.session_state.generated_videos = []


with st.sidebar:

    st.markdown("## 🎬 VisionCraft AI")

    st.caption(
        "AI Movie Creation Studio"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🎥 Create Movie",
            "🎬 Scene Production",
            "🖼️ Image to Video",
            "🎞️ Scene Generator",
            "📁 Projects",
            "⚙️ Settings"
        ]
    )

    st.divider()

    st.markdown(
        "### ⚡ Movie Pipeline"
    )

    st.write(
        "1️⃣ Story Creation"
    )

    st.write(
        "2️⃣ Scene Breakdown"
    )

    st.write(
        "3️⃣ Visual Generation"
    )

    st.write(
        "4️⃣ Video Generation"
    )

    st.write(
        "5️⃣ Audio Production"
    )

    st.write(
        "6️⃣ Movie Assembly"
    )

    st.divider()

    st.caption(
        "VisionCraft AI v1.0"
    )


st.markdown(
    '<div class="hero-title">🎬 VisionCraft AI</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="hero-subtitle">'
    'Transform a story idea into a complete cinematic movie.'
    '</div>',
    unsafe_allow_html=True
)


if page == "🎥 Create Movie":

    st.header(
        "🎥 Create Your Movie"
    )

    st.write(
        "Describe your movie idea and VisionCraft AI "
        "will create a complete story structure "
        "with characters and scenes."
    )

    story_idea = st.text_area(
        "💡 What movie do you want to create?",
        height=180,
        placeholder=(
            "Example: Create a 20-minute Hindi anime "
            "fantasy movie about six friends who discover "
            "powerful Bond Beasts and must protect their "
            "world from an ancient evil."
        )
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        duration = st.selectbox(
            "🎬 Movie Duration",
            [
                5,
                10,
                20,
                30
            ],
            format_func=lambda x:
            f"{x} minutes"
        )

        language = st.selectbox(
            "🗣️ Language",
            [
                "English",
                "Hindi",
                "Kannada"
            ]
        )

    with col2:

        genre = st.selectbox(
            "🎭 Genre",
            [
                "Cinematic",
                "Fantasy",
                "Anime",
                "Action",
                "Adventure",
                "Sci-Fi",
                "Thriller",
                "Mythology",
                "Drama"
            ]
        )

        visual_style = st.selectbox(
            "🎨 Visual Style",
            [
                "Cinematic",
                "Anime",
                "Photorealistic",
                "Hollywood",
                "Dark Fantasy",
                "Epic Fantasy"
            ]
        )

    st.divider()

    if st.button(
        "✨ Generate Complete Story",
        type="primary"
    ):

        if not story_idea.strip():

            st.warning(
                "Please enter your movie idea first."
            )

        else:

            try:

                with st.status(
                    "🎬 Building your movie...",
                    expanded=True
                ) as status:

                    st.write(
                        "🧠 Creating characters and world..."
                    )

                    story_data = generate_story(
                        story_idea=story_idea,
                        duration_minutes=duration,
                        language=language,
                        genre=genre,
                        visual_style=visual_style
                    )

                    st.write(
                        "🎞️ Preparing scene continuity..."
                    )

                    prepared_scenes = prepare_scenes(
                        story_data
                    )

                    st.write(
                        "🎵 Preparing audio plan..."
                    )

                    audio_plan = prepare_movie_audio_plan(
                        [
                            item["scene"]
                            for item in prepared_scenes
                        ]
                    )

                    st.session_state.story_data = (
                        story_data
                    )

                    st.session_state.prepared_scenes = (
                        prepared_scenes
                    )

                    st.session_state.audio_plan = (
                        audio_plan
                    )

                    status.update(
                        label=(
                            "✅ Movie story created "
                            "successfully!"
                        ),
                        state="complete"
                    )

                st.success(
                    "Your complete movie blueprint is ready!"
                )

            except Exception as error:

                st.error(
                    f"Movie creation failed: {error}"
                )

                with st.expander(
                    "Technical Error"
                ):

                    st.code(
                        traceback.format_exc()
                    )


    if st.session_state.story_data:

        story = (
            st.session_state.story_data
        )

        movie = story.get(
            "movie",
            {}
        )

        st.divider()

        st.header(
            f"🎬 {movie.get(
                'title',
                'Untitled Movie'
            )}"
        )

        st.write(
            movie.get(
                "logline",
                ""
            )
        )

        col1, col2, col3 = st.columns(
            3
        )

        with col1:

            st.metric(
                "Duration",
                f"{movie.get(
                    'duration_minutes',
                    0
                )} min"
            )

        with col2:

            st.metric(
                "Language",
                movie.get(
                    "language",
                    ""
                )
            )

        with col3:

            st.metric(
                "Scenes",
                len(
                    story.get(
                        "scenes",
                        []
                    )
                )
            )

        st.divider()

        with st.expander(
            "🌍 World Bible"
        ):

            world = story.get(
                "world",
                {}
            )

            st.write(
                world.get(
                    "description",
                    ""
                )
            )

            st.write(
                "### World Rules"
            )

            for rule in world.get(
                "rules",
                []
            ):

                st.write(
                    f"• {rule}"
                )

        with st.expander(
            "👥 Character Bible"
        ):

            for character in story.get(
                "characters",
                []
            ):

                st.markdown(
                    f"### {character.get(
                        'name',
                        'Character'
                    )}"
                )

                st.write(
                    f"**Role:** {character.get(
                        'role',
                        ''
                    )}"
                )

                st.write(
                    f"**Personality:** {character.get(
                        'personality',
                        ''
                    )}"
                )

                st.write(
                    f"**Appearance:** {character.get(
                        'appearance',
                        ''
                    )}"
                )

                st.write(
                    f"**Abilities:** {character.get(
                        'abilities',
                        ''
                    )}"
                )

                st.divider()


elif page == "🎬 Scene Production":

    st.header(
        "🎬 Scene Production"
    )

    if not st.session_state.prepared_scenes:

        st.info(
            "Create a movie first to prepare scenes."
        )

    else:

        scenes = (
            st.session_state.prepared_scenes
        )

        st.success(
            f"{len(scenes)} scenes are ready "
            "for production."
        )

        scene_number = st.number_input(
            "Select Scene",
            min_value=1,
            max_value=len(scenes),
            value=1,
            step=1
        )

        selected = scenes[
            scene_number - 1
        ]

        scene = selected.get(
            "scene",
            {}
        )

        st.subheader(
            f"🎬 Scene "
            f"{scene.get('scene_number', '')}: "
            f"{scene.get('title', '')}"
        )

        st.write(
            f"**Location:** "
            f"{scene.get('location', '')}"
        )

        st.write(
            f"**Duration:** "
            f"{scene.get('duration_seconds', 0)} seconds"
        )

        st.write(
            f"**Action:** "
            f"{scene.get('action', '')}"
        )

        st.write(
            f"**Emotions:** "
            f"{scene.get('emotions', '')}"
        )

        with st.expander(
            "🖼️ Image Generation Prompt"
        ):

            st.write(
                scene.get(
                    "image_generation_prompt",
                    ""
                )
            )

        with st.expander(
            "🎥 Animation Prompt"
        ):

            st.write(
                scene.get(
                    "animation_prompt",
                    ""
                )
            )

        with st.expander(
            "🎵 Audio"
        ):

            st.write(
                f"Music: "
                f"{scene.get(
                    'background_music',
                    ''
                )}"
            )

            st.write(
                f"Sound Effects: "
                f"{scene.get(
                    'sound_effects',
                    []
                )}"
            )

        if st.button(
            "🎬 Generate This Scene Video",
            type="primary"
        ):

            if not VIDEO_ENGINE_AVAILABLE:

                st.error(
                    "Video engine is unavailable. "
                    "Check video_engine.py and "
                    "requirements.txt."
                )

            else:

                try:

                    with st.spinner(
                        "🎬 Generating scene video..."
                    ):

                        result = (
                            generate_scene_video(
                                scene
                            )
                        )

                    st.session_state.generated_videos.append(
                        result
                    )

                    st.success(
                        "Scene video generated successfully!"
                    )

                    if result.get(
                        "local_path"
                    ):

                        st.video(
                            result[
                                "local_path"
                            ]
                        )

                except Exception as error:

                    st.error(
                        f"Video generation failed: "
                        f"{error}"
                    )

                    with st.expander(
                        "Technical Error"
                    ):

                        st.code(
                            traceback.format_exc()
                        )


elif page == "🖼️ Image to Video":

    st.header(
        "🖼️ Image to Video"
    )

    uploaded_image = st.file_uploader(
        "Upload an image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]
    )

    if uploaded_image:

        st.image(
            uploaded_image,
            caption="Source Image",
            use_container_width=True
        )

        motion_prompt = st.text_area(
            "Describe the motion",
            placeholder=(
                "The camera slowly moves forward "
                "while the character's clothes move "
                "in the wind."
            )
        )

        if st.button(
            "🎬 Animate Image",
            type="primary"
        ):

            st.info(
                "Image-to-video production will use "
                "the image engine and video engine."
            )


elif page == "🎞️ Scene Generator":

    st.header(
        "🎞️ Scene Generator"
    )

    st.info(
        "The complete scene generator is automatically "
        "created when you generate a movie."
    )

    if st.session_state.prepared_scenes:

        for item in (
            st.session_state.prepared_scenes
        ):

            scene = item.get(
                "scene",
                {}
            )

            with st.expander(
                f"Scene "
                f"{scene.get('scene_number', '')}: "
                f"{scene.get('title', '')}"
            ):

                st.write(
                    scene.get(
                        "action",
                        ""
                    )
                )


elif page == "📁 Projects":

    st.header(
        "📁 Projects"
    )

    if st.session_state.story_data:

        st.success(
            "Current movie project is loaded."
        )

        story_json = json.dumps(
            st.session_state.story_data,
            ensure_ascii=False,
            indent=4
        )

        st.download_button(
            "⬇️ Download Story JSON",
            data=story_json,
            file_name="generated_story.json",
            mime="application/json"
        )

    else:

        st.info(
            "No movie project has been created yet."
        )


elif page == "⚙️ Settings":

    st.header(
        "⚙️ Settings"
    )

    st.subheader(
        "🔐 API Configuration"
    )

    st.info(
        "API keys are loaded securely from environment "
        "variables or Streamlit Secrets. Never place "
        "API keys directly in app.py."
    )

    fal_status = bool(
        os.getenv(
            "FAL_KEY"
        )
    )

    gemini_status = bool(
        os.getenv(
            "GEMINI_API_KEY"
        )
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        if fal_status:

            st.success(
                "FAL_KEY detected"
            )

        else:

            st.warning(
                "FAL_KEY not detected"
            )

    with col2:

        if gemini_status:

            st.success(
                "GEMINI_API_KEY detected"
            )

        else:

            st.warning(
                "GEMINI_API_KEY not detected"
            )

    st.divider()

    st.subheader(
        "🎬 Movie Production Settings"
    )

    st.selectbox(
        "Default Video Style",
        [
            "Cinematic",
            "Anime",
            "Photorealistic",
            "Hollywood",
            "Dark Fantasy"
        ]
    )

    st.selectbox(
        "Default Language",
        [
            "English",
            "Hindi",
            "Kannada"
        ]
    )

    st.success(
        "VisionCraft AI is ready for cinematic production."
    )

