import streamlit as st
from PIL import Image, ImageDraw
import io
import base64

st.set_page_config(
    page_title="About - Solar ROI Predictor",
    page_icon="ℹ️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Top Navigation Bar */
    .top-nav {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(10px);
        padding: 1rem 2rem;
        border-bottom: 1px solid rgba(96, 165, 250, 0.3);
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .nav-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .nav-team {
        color: #94a3b8;
        font-size: 0.9rem;
    }

    .team-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(96, 165, 250, 0.3);
        border-radius: 1rem;
        padding: 2rem;
        margin: 1rem 0;
    }

    .team-member {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(96, 165, 250, 0.2);
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .member-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #60a5fa;
    }

    .member-role {
        color: #34d399;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }

    .member-bio {
        color: #94a3b8;
        line-height: 1.6;
    }

    .badge {
        background: rgba(96, 165, 250, 0.1);
        border: 1px solid #60a5fa;
        border-radius: 1rem;
        padding: 0.5rem 1rem;
        color: #60a5fa;
        display: inline-block;
        margin: 0.3rem;
        font-size: 0.9rem;
    }

    .profile-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #60a5fa;
        margin: 0 auto 1rem auto;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

# Top Navigation
st.markdown("""
<div class="top-nav">
    <div>
        <div class="nav-title">☀️ Solar ROI Predictor</div>
        <div class="nav-team">by NASA Techies 🇵🇰</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Header
st.title("About Solar ROI Predictor")

# NASA Challenge Badge
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="team-card" style="text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
        <h2 style="color: #f1f5f9; margin-bottom: 0.5rem;">NASA Space Apps Challenge 2025</h2>
        <p style="color: #60a5fa; font-size: 1.2rem; margin: 0;">Team: NASA Techies</p>
        <p style="color: #94a3b8; margin-top: 0.5rem;">🇵🇰 Pakistan</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Mission
st.markdown("## 🎯 Our Mission")
st.markdown("""
<div class="team-card">
    <p style="font-size: 1.1rem; color: #cbd5e1; line-height: 1.8;">
        Solar ROI Predictor addresses a critical challenge: making NASA's decades of space solar irradiance
        data accessible and actionable for solar energy investments. We transform complex satellite data into
        clear, data-driven investment insights, helping investors, engineers, and policymakers make informed
        decisions about solar farm locations.
    </p>
</div>
""", unsafe_allow_html=True)

# Team Description
st.markdown("## 💪 Our Team")
st.markdown("""
<div class="team-card">
    <p style="font-size: 1.1rem; color: #cbd5e1; line-height: 1.8; text-align: center;">
        Our team brings together a powerful mix of expertise in <strong style="color: #60a5fa;">machine learning</strong>,
        <strong style="color: #34d399;">backend automation</strong>, <strong style="color: #60a5fa;">mobile app development</strong>,
        and <strong style="color: #34d399;">financial analytics</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

# Team Members
# Function to create circular image
def create_circular_image(image_path, size=120):
    img = Image.open(image_path)
    img = img.resize((size, size))
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    buffered = io.BytesIO()
    output.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Create circular images for all team members
sheeraz_img = create_circular_image("assets/sheeraz.png")
sonia_img = create_circular_image("assets/sonia.png")
waqad_img = create_circular_image("assets/waqad.png")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="team-member">
        <img src="data:image/png;base64,{sheeraz_img}" class="profile-img" alt="Muhammad Sheeraz">
        <div class="member-name">Muhammad Sheeraz</div>
        <div class="member-role">ML Engineer & Full-Stack Developer</div>
        <div class="member-bio">
            Machine learning expert with 5+ years in mobile development, specializing in model training, optimization, and deployment. Experienced in building intelligent, scalable solutions that bridge data science and software engineering.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="team-member">
        <img src="data:image/png;base64,{sonia_img}" class="profile-img" alt="Sonia Irfan">
        <div class="member-name">Sonia Irfan</div>
        <div class="member-role">Financial Analytics Expert</div>
        <div class="member-bio">
            ACCA-qualified and B.Com (Hons.) graduate with 7 years in teaching and finance. Taught Stanford’s Code in Place (Python 106A) and winner of Harvard Puzzle Day. Passionate about AI, ML, and sustainable, tech-driven finance solutions.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="team-member">
        <img src="data:image/png;base64,{waqad_img}" class="profile-img" alt="Waqad">
        <div class="member-name">Waqad</div>
        <div class="member-role">Mobile App Developer</div>
        <div class="member-bio">
            Passionate Mobile App Developer skilled in Dart, Node.js, and Python, building seamless, high-performance applications.
            Experienced in crafting efficient API integrations that connect systems and elevate user experiences. 
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Technology Stack
st.markdown("## 🛠️ Technology Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Frontend & Visualization")
    st.markdown("""
    <div style="margin-top: 1rem;">
        <span class="badge">🎨 Streamlit</span>
        <span class="badge">🐍 Python</span>
        <span class="badge">📊 Plotly</span>
        <span class="badge">🗺️ Folium</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Backend & Data")
    st.markdown("""
    <div style="margin-top: 1rem;">
        <span class="badge">🛰️ NASA POWER API</span>
        <span class="badge">📈 Pandas</span>
        <span class="badge">🔢 NumPy</span>
        <span class="badge">⚙️ Node.js</span>
    </div>
    """, unsafe_allow_html=True)

# Team Skills
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 💡 Team Skills & Expertise")
st.markdown("""
<div style="text-align: center; margin-top: 1rem;">
    <span class="badge">Machine Learning</span>
    <span class="badge">Python</span>
    <span class="badge">Flutter/Dart</span>
    <span class="badge">Node.js</span>
    <span class="badge">Financial Analytics</span>
    <span class="badge">Data Visualization</span>
    <span class="badge">Backend Automation</span>
    <span class="badge">Mobile Development</span>
    <span class="badge">NASA APIs</span>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Key Features
st.markdown("## ⭐ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🔍 Smart Analysis
    - Real-time NASA satellite data integration
    - Accurate solar irradiance measurements
    - 25-year ROI projections with degradation modeling
    - Location-based optimization
    """)

with col2:
    st.markdown("""
    ### 📊 Comprehensive Insights
    - Interactive visualizations and charts
    - Multi-location comparison tools
    - Downloadable data exports
    - Financial breakeven analysis
    """)

st.markdown("<br>", unsafe_allow_html=True)

# Impact
st.markdown("## 🌍 Project Impact")
st.markdown("""
<div class="team-card">
    <p style="font-size: 1.1rem; color: #cbd5e1; line-height: 1.8;">
        This project democratizes access to NASA's solar data, enabling better investment decisions and promoting
        renewable energy adoption worldwide. By making complex satellite data accessible to everyone, we're
        contributing to a sustainable energy future and helping accelerate the global transition to clean energy.
    </p>
</div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h3 style="color: #f1f5f9; margin-bottom: 1rem;">Ready to Analyze Solar Potential?</h3>
    <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 1.5rem;">
        Click the button below to start analyzing solar investments
    </p>
</div>
""", unsafe_allow_html=True)

# Add button to navigate to home
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🏠 Go to Home", use_container_width=True, type="primary"):
        st.switch_page("Home.py")
