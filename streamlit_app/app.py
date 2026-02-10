import streamlit as st
from youtube_auth import get_youtube_service
from googleapiclient.errors import HttpError
from datetime import datetime

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="YouTube Channel Analytics",
    page_icon="📊",
    layout="centered"
)

# ---------------- Attractive & Tight UI Styling ----------------
st.markdown("""
<style>
    /* Global Tightening */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Clean Professional Card */
    .result-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #edf2f7;
        margin-top: 1.5rem;
    }
    
    /* Title & Subtitle */
    .main-title {
        color: #1a202c;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    .sub-title {
        color: #718096;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #3182ce 0%, #2b6cb0 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
    }
    
    /* Sample Buttons Section */
    .sample-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 1rem;
    }
    
    /* Stat Labels */
    .stat-card {
        text-align: center;
        padding: 1rem;
        background: #f7fafc;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- Main Interface -----------------
# Header with Icon
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="main-title">📊 YouTube Analytics</h1>
    <p class="sub-title">Extract professional insights from any YouTube channel identity.</p>
</div>
""", unsafe_allow_html=True)

# Instructions (Restored)
with st.expander("ℹ️ How to use"):
    st.write("""
    1. **Find ID**: Look for the 24-character YouTube Channel ID (starts with 'UC').
    2. **Paste**: Enter the ID in the field below.
    3. **Analyze**: Click the button to see real-time engagement data.
    """)

# Centered Input Section
st.write("") # Tiny spacer
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    channel_id_input = st.text_input("Channel ID", label_visibility="collapsed", placeholder="Enter Channel ID (UC...)")
    
    # Analyze Button (Now lone and clean)
    analyze_clicked = st.button("🔍 Analyze Channel", use_container_width=True)

# ---------------- Logic & Results ----------------
if analyze_clicked and channel_id_input:

    cid = channel_id_input.strip()
    
    if not (cid.startswith("UC") and len(cid) == 24):
        st.error("⚠️ Invalid Format: Must start with 'UC' and be 24 chars.")
    else:
        try:
            with st.spinner("✨ Fetching Intelligence..."):
                youtube = get_youtube_service()
                response = youtube.channels().list(part="snippet,statistics", id=cid).execute()

            if not response.get("items"):
                st.info("No data found for this identity.")
            else:
                ch = response["items"][0]
                snip, stats = ch["snippet"], ch["statistics"]
                
                # Formatters
                def fmt(n):
                    n = int(n)
                    if n >= 1e6: return f"{n/1e6:.2f}M"
                    if n >= 1e3: return f"{n/1e3:.1f}K"
                    return str(n)

                # Result Card Start
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                
                # Profile Header
                p_col1, p_col2 = st.columns([1, 3])
                with p_col1:
                    st.image(snip["thumbnails"]["high"]["url"], width=110)
                with p_col2:
                    st.subheader(snip["title"])
                    st.caption(f"📅 Established: {snip['publishedAt'][:10]}")
                
                st.write("---")
                
                # Metrics Container
                st.markdown("### 📊 Engagement Statistics")
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.metric("👥 Subscribers", fmt(stats.get("subscriberCount", 0)))
                with m_col2:
                    st.metric("👁️ Total Views", fmt(stats.get("viewCount", 0)))
                with m_col3:
                    st.metric("🎥 Video Count", f"{int(stats.get('videoCount', 0)):,}")
                
                st.write("---")
                
                # Description (Renamed)
                st.markdown("### 📝 Description")
                desc = snip.get("description", "No description available.")
                if len(desc) > 250:
                    st.write(desc[:250] + "...")
                    with st.expander("Read More"):
                        st.write(desc)
                else:
                    st.write(desc)
                
                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Minimal Footer
st.markdown('<div style="text-align: center; margin-top: 3rem; color: #cbd5e0; font-size: 0.85rem;">© 2026 YouTube Analytics Pro • Professional Insight Suite</div>', unsafe_allow_html=True)

