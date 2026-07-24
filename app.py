import streamlit as st
import time

# ─────────────────────────────────────────────

# PAGE CONFIGURATION

# ─────────────────────────────────────────────

st.set_page_config(
page_title="VisionCraft AI",
page_icon="🎬",
layout="wide",
initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────

# CUSTOM CSS

# ─────────────────────────────────────────────

st.markdown("""

<style>

    /* Main background */
    .stApp {
        background: #08090d;
        color: #f5f5f5;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0d0f15;
        border-right: 1px solid #20232c;
    }

    /* Main content */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1500px;
    }

    /* Header */
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        color: #8d93a1;
        font-size: 16px;
        margin-bottom: 30px;
    }

    /* Cards */
    .card {
        background: #11141b;
        border: 1px solid #242833;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 46px;
        font-weight: 700;
        border: 1px solid #343945;
        background: #181c25;
        color: white;
        transition: 0.2s;
    }

    .stButton > button:hover {
        border-color: #ffffff;
        background: #222733;
    }

    /* Primary button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: #ffffff;
        color: #000000;
        border: none;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: #dddddd;
    }

    /* Text areas */
    textarea {
        background: #0b0d12 !important;
        color: white !important;
        border: 1px solid #2b303b !important;
        border-radius: 12px !important;
    }

    /* Select boxes */
    div[data-baseweb="select"] > div {
        background: #0b0d12;
        border-color: #2b303b;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: #11141b;
        border: 1px solid #242833;
        padding: 15px;
        border-radius: 12px;
    }

    /* Divider */
    hr {
        border-color: #242833;
    }

</style>

""", unsafe_allow_html=True)

# ─────────────────────────────────────────────

# SESSION STATE

# ─────────────────────────────────────────────

if "generated_prompt" not in st.session_state:
st.session_state.generated_prompt = ""

if "video_generated" not in st.session_state:
st.session_state.video_generated = False

# ─────────────────────────────────────────────

# SIDEBAR

# ─────────────────────────────────────────────

with st.sidebar:

```
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
st.caption("Built for cinematic creators")
```

# ─────────────────────────────────────────────

# MAIN HEADER

# ─────────────────────────────────────────────

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

# ─────────────────────────────────────────────

# CREATE VIDEO PAGE

# ─────────────────────────────────────────────

if page == "🎥 Create Video":

```
left, right = st.columns([1.2, 0.8], gap="large")

# ───────────── LEFT PANEL ─────────────

with left:

    st.markdown(
        '<div class="section-title">✍️ Describe Your Video</div>',
        unsafe_allow_html=True
    )

    prompt = st.text_area(
        "Video Prompt",
        height=180,
        placeholder=(
            "Example: A powerful warrior walks through a burning battlefield "
            "at sunset. Cinematic camera movement, dramatic atmosphere, "
            "epic lighting..."
        ),
        label_visibility="collapsed"
    )

    st.markdown("### 🎨 Video Settings")

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
                "16:9 — YouTube / Cinema",
                "9:16 — Shorts / Reels",
                "1:1 — Social Media"
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
                "360° Orbit",
                "Handheld Camera",
                "Static Shot"
            ]
        )

    negative_prompt = st.text_area(
        "Negative Prompt",
        placeholder="blurry, distorted face, low quality, extra fingers...",
        height=80
    )

    st.markdown("")

    enhance_col, generate_col = st.columns(2)

    with enhance_col:

        enhance_prompt = st.button(
            "✨ Enhance Prompt"
        )

    with generate_col:

        generate_video = st.button(
            "🎬 Generate Video",
            type="primary"
        )

# ───────────── RIGHT PANEL ─────────────

with right:

    st.markdown(
        '<div class="section-title">🎞️ Video Preview</div>',
        unsafe_allow_html=True
    )

    preview_box = st.container()

    with preview_box:

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
                    <div style="color:#8d93a1;">
                        Your generated video will appear here
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    st.info(
        "💡 Tip: Describe the subject, environment, lighting, "
        "camera movement, mood, and visual style for better results."
    )
```

# ─────────────────────────────────────────────

# PROMPT ENHANCEMENT

# ─────────────────────────────────────────────

if page == "🎥 Create Video" and enhance_prompt:

```
if not prompt.strip():

    st.warning("Please enter a video idea first.")

else:

    enhanced = f"""
```

Create a {duration} {style.lower()} cinematic video.

Main subject and action:
{prompt}

Visual direction:
High-quality {style.lower()} visual style, detailed environment, realistic lighting,
strong cinematic composition, professional production quality.

Camera:
{camera} with smooth, controlled cinematic motion.

Aspect ratio:
{aspect_ratio}

Atmosphere:
Dramatic mood, rich depth, natural environmental movement, realistic shadows,
detailed textures, immersive cinematic presentation.

Negative prompt:
{negative_prompt if negative_prompt else "low quality, blurry, distorted anatomy, unwanted objects"}
"""

```
    st.session_state.generated_prompt = enhanced.strip()

    st.success("✨ Prompt enhanced successfully!")

    st.text_area(
        "Enhanced Cinematic Prompt",
        value=st.session_state.generated_prompt,
        height=300
    )
```

# ─────────────────────────────────────────────

# VIDEO GENERATION PLACEHOLDER

# ─────────────────────────────────────────────

if page == "🎥 Create Video" and generate_video:

```
if not prompt.strip():

    st.error("Please enter a video prompt first.")

else:

    st.session_state.video_generated = True

    with st.spinner("🎬 Preparing your cinematic video..."):

        time.sleep(2)

    st.success(
        "Your video generation request is ready!"
    )

    st.info(
        "🚀 The actual AI video generation API will be connected in the next step."
    )
```

# ─────────────────────────────────────────────

# IMAGE TO VIDEO

# ─────────────────────────────────────────────

elif page == "🖼️ Image to Video":

```
st.markdown("## 🖼️ Image to Video")

uploaded_image = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg", "webp"]
)

if uploaded_image:

    st.image(
        uploaded_image,
        caption="Source Image",
        use_container_width=True
    )

    motion_prompt = st.text_area(
        "Describe the motion",
        placeholder="Camera slowly moves forward while the character's clothes move in the wind..."
    )

    if st.button("🎬 Animate Image", type="primary"):

        st.info(
            "🚀 Image-to-video API will be connected in the next step."
        )
```

# ─────────────────────────────────────────────

# SCENE GENERATOR

# ─────────────────────────────────────────────

elif page == "🎞️ Scene Generator":

```
st.markdown("## 🎞️ AI Scene Generator")

project_idea = st.text_area(
    "Describe your movie, trailer, or story",
    height=180,
    placeholder="Example: Create a 2-minute Mahabharata anime trailer..."
)

number_of_scenes = st.slider(
    "Number of Scenes",
    min_value=3,
    max_value=20,
    value=10
)

if st.button("✨ Generate Scene Structure", type="primary"):

    if not project_idea.strip():

        st.warning("Please describe your project first.")

    else:

        st.success(
            f"Ready to generate {number_of_scenes} cinematic scenes!"
        )

        for i in range(1, number_of_scenes + 1):

            with st.expander(f"🎬 Scene {i}"):

                st.text_area(
                    f"Scene {i} Description",
                    placeholder="Scene description will be generated by AI...",
                    key=f"scene_{i}"
                )
```

# ─────────────────────────────────────────────

# PROJECTS

# ─────────────────────────────────────────────

elif page == "📁 Projects":

```
st.markdown("## 📁 Your Projects")

st.info(
    "Your generated projects will appear here once database storage is connected."
)
```

# ─────────────────────────────────────────────

# SETTINGS

# ─────────────────────────────────────────────

elif page == "⚙️ Settings":

```
st.markdown("## ⚙️ Settings")

st.subheader("🎬 Generation Preferences")

st.selectbox(
    "Default Video Style",
    ["Cinematic", "Anime", "Photorealistic", "Hollywood"]
)

st.selectbox(
    "Default Aspect Ratio",
    ["16:9", "9:16", "1:1"]
)

st.success(
    "VisionCraft AI is ready for AI model integration."
)
```
