# app.py
import streamlit as st
from source_code import generate_story_from_images, narrate_story
from PIL import Image

# === PAGE CONFIGURATION ===
st.set_page_config(
    page_title="SSB TAT Story Generator",
    page_icon="🎖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CUSTOM CSS FOR BEAUTIFUL DASHBOARD ===
st.markdown("""
<style>
    /* Reset all paddings */
    .main .block-container {
        padding-top: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hero Banner - Exactly 30% height with background image */
    .hero-banner {
        width: 100%;
        height: 30vh;
        min-height: 300px;
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url('https://images.unsplash.com/photo-1593005510327-b6e7567b5c8a?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 20px 20px;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .hero-content {
        text-align: center;
        color: white;
        z-index: 2;
        padding: 40px;
        max-width: 900px;
    }
    
    .hero-title {
        font-size: 3.8rem;
        font-weight: 900;
        margin-bottom: 20px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        letter-spacing: 1px;
    }
    
    .hero-subtitle {
        font-size: 1.8rem;
        font-weight: 400;
        opacity: 0.95;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.5;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    
    /* Cute floating elements */
    .floating-element {
        position: absolute;
        background: rgba(255,255,255,0.15);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Dashboard Cards */
    .dashboard-card {
        background: white;
        border-radius: 20px;
        padding: 35px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #f0f0f0;
        margin-bottom: 25px;
    }
    
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    
    .card-title {
        color: #1a237e;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f0f0;
    }
    
    /* Text sizes increased throughout */
    .card-content {
        color: #444;
        font-size: 1.15rem;
        line-height: 1.8;
    }
    
    .list-item {
        font-size: 1.15rem;
        line-height: 1.8;
        margin-bottom: 12px;
    }
    
    /* Beautiful Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #f0f2ff 100%);
        padding: 35px 25px !important;
        border-right: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .sidebar-header {
        color: #1a237e;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 35px;
        padding-bottom: 20px;
        border-bottom: 3px solid rgba(102, 126, 234, 0.2);
    }
    
    /* Upload Area Styling */
    .upload-area {
        border: 3px dashed #c3cfe2;
        border-radius: 20px;
        padding: 45px 25px;
        text-align: center;
        background: rgba(255,255,255,0.9);
        cursor: pointer;
        transition: all 0.3s;
        margin-bottom: 30px;
    }
    
    .upload-area:hover {
        border-color: #667eea;
        background: rgba(102, 126, 234, 0.05);
        transform: scale(1.01);
    }
    
    .upload-icon {
        font-size: 3.5rem;
        color: #667eea;
        margin-bottom: 20px;
    }
    
    .upload-text {
        font-size: 1.3rem;
        color: #667eea;
        margin-bottom: 10px;
        font-weight: 600;
    }
    
    .upload-subtext {
        color: #888;
        font-size: 1rem;
    }
    
    /* Beautiful Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        border: none;
        padding: 20px 40px;
        border-radius: 15px;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 6px 20px rgba(26, 35, 126, 0.3);
        position: relative;
        overflow: hidden;
        margin-top: 25px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(26, 35, 126, 0.4);
        background: linear-gradient(135deg, #283593 0%, #3949ab 100%);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        border: 2px solid #e0e0e0;
        border-radius: 12px;
        padding: 12px;
        background: white;
        transition: all 0.3s;
        font-size: 1.1rem;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #1a237e;
    }
    
    /* File List Styling */
    .file-item {
        background: white;
        border-radius: 15px;
        padding: 18px;
        margin: 15px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #1a237e;
        transition: all 0.3s;
    }
    
    .file-item:hover {
        transform: translateX(5px);
    }
    
    .file-name {
        font-weight: 600;
        color: #333;
        font-size: 1.1rem;
    }
    
    .file-size {
        color: #666;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Story Display */
    .story-box {
        background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
        border-radius: 20px;
        padding: 40px;
        margin: 35px 0;
        border-left: 6px solid #1a237e;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    .story-title {
        color: #1a237e;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 25px;
        padding-bottom: 15px;
        border-bottom: 2px solid rgba(26, 35, 126, 0.2);
    }
    
    .story-content {
        color: #333;
        line-height: 1.9;
        font-size: 1.2rem;
    }
    
    /* Audio Player Styling */
    .audio-player {
        background: white;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 25px 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.3rem;
        }
        .card-title {
            font-size: 1.5rem;
        }
        .card-content {
            font-size: 1rem;
        }
    }
    
    /* Section Headers */
    h1, h2, h3 {
        color: #1a237e !important;
    }
    
    h1 {
        font-size: 2.8rem !important;
    }
    
    h2 {
        font-size: 2.2rem !important;
    }
    
    h3 {
        font-size: 1.8rem !important;
    }
    
    p {
        font-size: 1.15rem !important;
        line-height: 1.7 !important;
    }
</style>
""", unsafe_allow_html=True)

# === HERO BANNER WITH SPECIFIED IMAGE ===
hero_html = """
<div class="hero-banner">
    <!-- Floating elements -->
    <div class="floating-element" style="width: 80px; height: 80px; top: 20%; left: 10%;"></div>
    <div class="floating-element" style="width: 60px; height: 60px; top: 60%; right: 15%;"></div>
    <div class="floating-element" style="width: 40px; height: 40px; bottom: 20%; left: 20%;"></div>
    
    <div class="hero-content">
        <h1 class="hero-title">🎖️ SSB TAT STORY GENERATOR</h1>
        <p class="hero-subtitle">Transform Images into Inspiring Stories for SSB Interview Preparation</p>
    </div>
</div>
"""

# === SIDEBAR WITH BEAUTIFUL CONTROLS ===
with st.sidebar:
    st.markdown('<div class="sidebar-header">🎯 CONTROLS PANEL</div>', unsafe_allow_html=True)
    
    # Upload Section
    st.markdown("### 📁 UPLOAD IMAGES")
    
    # Custom upload area
    st.markdown("""
    <div class="upload-area" onclick="document.querySelector('input[type=file]').click()">
        <div class="upload-icon">📤</div>
        <div class="upload-text">DRAG & DROP FILES HERE</div>
        <div class="upload-subtext">Limit 200MB per file • JPG, PNG, JPEG</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "",
        type=["jpg", "png", "jpeg"],
        accept_multiple_files=True,
        key="image_uploader",
        label_visibility="collapsed"
    )
    
    # Display uploaded files
    if uploaded_files:
        st.markdown("### 📎 UPLOADED FILES")
        for file in uploaded_files:
            file_size = file.size
            if file_size < 1024 * 1024:  # Less than 1MB
                size = f"{file_size/1024:.1f} KB"
            else:
                size = f"{file_size/(1024*1024):.1f} MB"
            
            st.markdown(f"""
            <div class="file-item">
                <div class="file-name">{file.name[:25]}{'...' if len(file.name) > 25 else ''}</div>
                <div class="file-size">{size}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Story Style Selection
    st.markdown("### 🎨 STORY STYLE")
    story_style = st.selectbox(
        "Choose your preferred story style:",
        ["Humorous", "Dramatic", "Romantic", "Suspenseful", "Inspirational", "Comedy", "Thriller", "Sci-fi"],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Generate Button
    generate_button = st.button(
        "✨ **GENERATE STORY NOW** ✨",
        type="primary",
        use_container_width=True,
        key="generate_btn"
    )

# === DISPLAY HERO BANNER ===
st.markdown(hero_html, unsafe_allow_html=True)

# === DASHBOARD CONTENT ===
# Create columns for dashboard
col1, col2 = st.columns([2, 1])

with col1:
    # About This Tool Card
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">🎯 ABOUT THIS TOOL</div>
        <div class="card-content">
            Welcome to the SSB Thematic Apperception Test (TAT) Story Generator! 
            This powerful tool helps defense aspirants practice for SSB interviews by generating 
            compelling stories based on uploaded images. Each story demonstrates 
            key Officer Like Qualities (OLQs) required for selection into the armed forces.
            Perfect for NDA, CDS, AFCAT, and SSB aspirants.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How to Use Card
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">📝 HOW TO USE</div>
        <ol style="color: #444; line-height: 1.9; padding-left: 20px;">
            <li class="list-item"><b>Upload Images:</b> Add 1-5 images using the sidebar uploader</li>
            <li class="list-item"><b>Select Style:</b> Choose your preferred story tone and mood</li>
            <li class="list-item"><b>Generate:</b> Click the magic button to create your story</li>
            <li class="list-item"><b>Enjoy:</b> Read and listen to your personalized story</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Features Card
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">⭐ KEY FEATURES</div>
        <ul style="color: #444; line-height: 1.9; padding-left: 20px;">
            <li class="list-item">🤖 <b>AI-Powered Stories</b> - Smart story generation</li>
            <li class="list-item">🔊 <b>Audio Narration</b> - Listen to your story</li>
            <li class="list-item">🎭 <b>Multiple Styles</b> - Various story tones</li>
            <li class="list-item">📁 <b>Easy Upload</b> - Simple drag & drop</li>
            <li class="list-item">🎯 <b>OLQ-Focused</b> - Military-relevant content</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Tips Card
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">💡 QUICK TIPS</div>
        <ul style="color: #444; line-height: 1.9; padding-left: 20px;">
            <li class="list-item">Use clear, action-oriented images</li>
            <li class="list-item">Include people in your images</li>
            <li class="list-item">Mix different scenarios</li>
            <li class="list-item">Try different story styles</li>
            <li class="list-item">Practice with various themes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# === STORY GENERATION SECTION ===
if generate_button:
    if not uploaded_files:
        st.error("⚠️ Please upload at least one image to generate a story! 📸")
    elif len(uploaded_files) > 5:
        st.error("⚠️ Maximum 5 images allowed! 🚫")
    else:
        # Show uploaded images
        st.markdown("## 📸 YOUR IMAGES")
        cols = st.columns(len(uploaded_files))
        for idx, (col, uploaded_file) in enumerate(zip(cols, uploaded_files)):
            with col:
                try:
                    image = Image.open(uploaded_file)
                    st.image(
                        image, 
                        caption=f"Image {idx+1}",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Could not load image {idx+1}")
        
        # Generate story
        with st.spinner("✨ Creating your magical story... Please wait!"):
            try:
                pil_images = [Image.open(uploaded_file) for uploaded_file in uploaded_files]
                generate_story = generate_story_from_images(pil_images, story_style)
                
                # Display story in beautiful box
                st.markdown(f"""
                <div class="story-box">
                    <div class="story-title">📖 YOUR {story_style.upper()} STORY</div>
                    <div class="story-content">
                        {generate_story}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Generate and display audio with better error handling
                st.markdown("## 🔊 AUDIO NARRATION")
                
                try:
                    audio_data = narrate_story(generate_story)
                    
                    if audio_data and isinstance(audio_data, bytes) and len(audio_data) > 1000:
                        st.markdown('<div class="audio-player">', unsafe_allow_html=True)
                        
                        # Display audio player
                        st.audio(audio_data, format="audio/mp3")
                        
                        # Download button
                        col1, col2 = st.columns([3, 1])
                        with col2:
                            st.download_button(
                                label="📥 DOWNLOAD AUDIO",
                                data=audio_data,
                                file_name=f"ssb_story_{story_style.lower()}.mp3",
                                mime="audio/mp3",
                                use_container_width=True
                            )
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.success("✅ Audio narration ready! Click play to listen or download.")
                    else:
                        st.warning("⚠️ Audio file generated but may be incomplete. Try downloading it.")
                        if audio_data:
                            st.download_button(
                                label="📥 DOWNLOAD AUDIO (Fallback)",
                                data=audio_data,
                                file_name=f"ssb_story_{story_style.lower()}.mp3",
                                mime="audio/mp3",
                                use_container_width=True
                            )
                        else:
                            st.info("💡 Tip: Audio generation failed. The story text is still available above for reading.")
                            
                except Exception as audio_error:
                    st.warning(f"⚠️ Audio player error: {str(audio_error)}")
                    st.info("You can still read the story above. Try refreshing the page or generating again.")
                
            except Exception as e:
                st.error(f"❌ Oops! Something went wrong: {str(e)}")

# === FOOTER ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 40px 20px 30px;">
    <p style="font-size: 1.2rem; margin-bottom: 15px; font-weight: 600;">
        Made with ❤️ for Defense Aspirants • Powered by Gemini AI
    </p>
    <p style="font-size: 1rem; color: #888;">
        🎖️ SSB Thematic Apperception Test Generator • Practice Makes Perfect!
    </p>
    <p style="font-size: 0.9rem; color: #aaa; margin-top: 20px;">
        For best results: Upload clear images with visible subjects and action scenarios
    </p>
</div>
""", unsafe_allow_html=True)