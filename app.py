import streamlit as st
import time

st.set_page_config(
    page_title="VisionCraft AI",
    page_icon="🎬",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #08090d;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #0d0f15;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
    }

    .hero-subtitle {
        color: #8d93a1;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 45px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "generated_prompt" not in st.session_state:
    st.session_state.generated_prompt = ""

if "video_generated" not in st.session_state:
    st.session_state.video_generated = False

with st.sidebar:
    st.markdown("## 🎬 VisionCraft AI")
    st.caption("AI Video Creation Studio")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🎥 Create Video",
            "🖼️ Image to Video",
            "🎞️ Scene Generator",
            "📁 Projects",
            "⚙️ Settings"
        ]
    )

    st.divider()

    st.markdown("### ⚡ Quick Stats")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Projects", "0")

    with col2:
        st.metric("Videos", "0")

    st.divider()

    st.caption("VisionCraft AI v1.0")

st.markdown(
    '<div class="hero-title">🎬 Create Your Vision</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Transform your imagination into cinematic AI-generated videos.'
    '</div>',
    unsafe_allow_html=True
)

if page == "🎥 Create Video":

    left, right = st.columns([1.2, 0.8], gap="large")

    with left:

        st.subheader("✍️ Describe Your Video")

        prompt = st.text_area(
            "Video Prompt",
            height=180,
            placeholder=(
                "A powerful warrior walks through a burning battlefield "
                "at sunset..."
            )
        )

        st.subheader("🎨 Video Settings")

        col1, col2 = st.columns(2)

        with col1:

            style = st.selectbox(
                "Visual Style",
                [
                    "Cinematic",
                    "Anime",
                    "Photorealistic",
                    "Hollywood",
                    "Fantasy",
                    "Sci-Fi",
                    "Documentary"
                ]
            )

            aspect_ratio = st.selectbox(
                "Aspect Ratio",
                [
                    "16:9",
                    "9:16",
                    "1:1"
                ]
            )

        with col2:

            duration = st.selectbox(
                "Duration",
                [
                    "5 seconds",
                    "10 seconds",
                    "15 seconds",
                    "30 seconds"
                ]
            )

            camera = st.selectbox(
                "Camera Movement",
                [
                    "Cinematic Slow Push-In",
                    "Dynamic Tracking Shot",
                    "Epic Crane Shot",
                    "360 Degree Orbit",
                    "Handheld Camera",
                    "Static Shot"
                ]
            )

        negative_prompt = st.text_area(
            "Negative Prompt",
            height=80,
            placeholder="blurry, low quality, distorted face..."
        )

        enhance_prompt = st.button(
            "✨ Enhance Prompt"
        )

        generate_video = st.button(
            "🎬 Generate Video",
            type="primary"
        )

    with right:

        st.subheader("🎞️ Video Preview")

        st.markdown(
            """
            <div style="
                height: 430px;
                border: 1px dashed #343945;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #0b0d12;
                text-align: center;
            ">
                <div>
                    <div style="font-size: 55px;">🎬</div>
                    <div style="color: #8d93a1;">
                        Your generated video will appear here
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "💡 Describe the subject, environment, lighting, "
            "camera movement, mood, and style for better results."
        )

    if enhance_prompt:

        if not prompt.strip():

            st.warning(
                "Please enter a video idea first."
            )

        else:

            enhanced = (
                f"Create a {duration} {style.lower()} cinematic video. "
                f"Main action: {prompt}. "
                f"Visual style: high-quality {style.lower()} production, "
                f"detailed environment, realistic lighting, cinematic "
                f"composition and professional visual effects. "
                f"Camera movement: {camera}. "
                f"Aspect ratio: {aspect_ratio}. "
                f"Atmosphere: dramatic, immersive, detailed and cinematic. "
                f"Negative prompt: "
                f"{negative_prompt if negative_prompt else 'blurry, low quality, distorted anatomy'}"
            )

            st.session_state.generated_prompt = enhanced

            st.success(
                "✨ Prompt enhanced successfully!"
            )

            st.text_area(
                "Enhanced Cinematic Prompt",
                value=st.session_state.generated_prompt,
                height=250
            )

    if generate_video:

        if not prompt.strip():

            st.error(
                "Please enter a video prompt first."
            )

        else:

            st.session_state.video_generated = True

            with st.spinner(
                "🎬 Preparing your cinematic video..."
            ):

                time.sleep(2)

            st.success(
                "Your video generation request is ready!"
            )

            st.info(
                "🚀 Real AI video generation will be connected next."
            )

elif page == "🖼️ Image to Video":

    st.header("🖼️ Image to Video")

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
                "Camera slowly moves forward while the character's "
                "clothes move in the wind..."
            )
        )

        if st.button(
            "🎬 Animate Image",
            type="primary"
        ):

            st.info(
                "🚀 Image-to-video API will be connected next."
            )

elif page == "🎞️ Scene Generator":

    st.header("🎞️ AI Scene Generator")

    project_idea = st.text_area(
        "Describe your movie, trailer, or story",
        height=180,
        placeholder=(
            "Create a 2-minute Mahabharata anime trailer..."
        )
    )

    number_of_scenes = st.slider(
        "Number of Scenes",
        min_value=3,
        max_value=20,
        value=10
    )

    if st.button(
        "✨ Generate Scene Structure",
        type="primary"
    ):

        if not project_idea.strip():

            st.warning(
                "Please describe your project first."
            )

        else:

            st.success(
                f"Ready to generate {number_of_scenes} cinematic scenes!"
            )

            for i in range(
                1,
                number_of_scenes + 1
            ):

                with st.expander(
                    f"🎬 Scene {i}"
                ):

                    st.text_area(
                        f"Scene {i} Description",
                        placeholder=(
                            "Scene description will be generated by AI..."
                        ),
                        key=f"scene_{i}"
                    )

elif page == "📁 Projects":

    st.header("📁 Your Projects")

    st.info(
        "Your generated projects will appear here once database storage is connected."
    )

elif page == "⚙️ Settings":

    st.header("⚙️ Settings")

    st.subheader("🎬 Generation Preferences")

    st.selectbox(
        "Default Video Style",
        [
            "Cinematic",
            "Anime",
            "Photorealistic",
            "Hollywood"
        ]
    )

    st.selectbox(
        "Default Aspect Ratio",
        [
            "16:9",
            "9:16",
            "1:1"
        ]
    )

    st.success(
        "VisionCraft AI is ready for AI model integration."
    )
