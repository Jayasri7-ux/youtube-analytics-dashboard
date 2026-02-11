import os
import sys
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Add project root to Python path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from streamlit_app.youtube_auth import get_youtube_service
from data_processing.channel_extractor import extract_channel_data
from data_processing.video_extractor import get_all_video_metadata
from database.persistence import save_channel_to_db, save_videos_to_db
from database.db_config import SessionLocal
from database.models import Channel, Video, VideoStatistics

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="YouTube Analytics Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Theme Injection -----------------
from streamlit_app.theme import THEME_CONTENT
st.markdown(THEME_CONTENT, unsafe_allow_html=True)

# ----------------- Session State -----------------
if 'channel_data' not in st.session_state:
    st.session_state.channel_data = None
if 'video_data' not in st.session_state:
    st.session_state.video_data = None
if 'current_cid' not in st.session_state:
    st.session_state.current_cid = None
if 'navigation' not in st.session_state:
    st.session_state.navigation = "🏠 Home"

# ----------------- Navigation -----------------
# ----------------- Navigation -----------------
with st.sidebar:
    st.markdown("<div class='sidebar-brand'><h1 style='font-family: \"Outfit\", sans-serif; font-size: 1.6rem; margin: 0; color: #1e3a8a; font-weight: 900;'>📊 YouTube Analytics</h1></div>", unsafe_allow_html=True)
    
    st.radio(
        "Navigation",
        ["🏠 Home", "🔎 Channel", "🎬 Videos", "📈 Dashboard", "ℹ️ About"],
        label_visibility="collapsed",
        key="navigation"
    )

# ----------------- View Functions -----------------

def navigate_to_channel():
    st.session_state.navigation = "🔎 Channel"

def show_home():
    st.markdown('<h1 class="page-title"><span class="blue-accent">YouTube Analytics</span> — Home</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.container(border=True):
            st.markdown("### Welcome to YouTube Analytics Pro")
            st.write("Our platform provides deep insights into video performance and channel audience engagement.")
            st.markdown("---")
            st.write("✅ **Channel Overview**: Real-time subscriber tracking.")
            st.write("✅ **Video Archive**: Deep metadata extraction.")
            st.write("✅ **Data Intelligence**: Automated SQL persistence.")
        
        st.button("GET STARTED", use_container_width=True, on_click=navigate_to_channel)

    with col2:
        st.info("💡 Start by entering a Channel ID in the 'Channel' section.")

def show_analyzer():
    st.markdown('<h1 class="page-title">Channel <span class="blue-accent">Analyzer</span></h1>', unsafe_allow_html=True)
    
    # Input Area
    with st.container(border=True):
        col_in, col_btn = st.columns([4, 1])
        with col_in:
            cid_input = st.text_input("Enter Channel ID (starts with UC)", placeholder="UC_x5XG1OV2P6uZZ5FSM9Ttw...", label_visibility="collapsed")
        with col_btn:
            if st.button("ANALYZE", use_container_width=True):
                if cid_input.startswith("UC") and len(cid_input) == 24:
                    with st.spinner("Fetching..."):
                        df = extract_channel_data([cid_input])
                        if not df.empty:
                            st.session_state.channel_data = df.iloc[0]
                            st.session_state.current_cid = cid_input
                            st.session_state.video_data = None
                            save_channel_to_db(df.iloc[0])
                            st.success("Analysis Complete!")
                        else:
                            st.error("Channel not found.")
                else:
                    st.warning("Please enter a valid 24-char Channel ID.")

    # Display Result
    if st.session_state.channel_data is not None:
        ch = st.session_state.channel_data
        with st.container(border=True):
            c1, c2 = st.columns([1, 4])
            with c1:
                st.image(ch["thumbnail_high"], use_container_width=True)
            with c2:
                st.markdown(f"<h2 style='margin: 0;'>{ch['channel_name']}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #64748b; font-size: 0.9rem;'>🆔 {ch['channel_id']}</p>", unsafe_allow_html=True)
                
                st.divider()
                m1, m2, m3 = st.columns(3)
                m1.metric("👥 Subscribers", f"{int(ch['subscriber_count']):,}")
                m2.metric("🎥 Videos", f"{int(ch['video_count']):,}")
                m3.metric("👁️ Views", f"{int(ch['view_count']):,}")
                
                st.divider()
                handle = ch.get("custom_url", "")
                url = f"https://youtube.com/{handle}" if handle else f"https://youtube.com/channel/{ch['channel_id']}"
                st.link_button("VISIT YOUTUBE CHANNEL", url, use_container_width=True)

def show_video_analytics():
    if not st.session_state.current_cid:
        st.warning("⚠️ No channel selected. Go to Channel first.")
        return

    st.markdown('<h1 class="page-title">Video <span class="blue-accent">Archive</span></h1>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.write(f"Exploring video library for **{st.session_state.channel_data['channel_name']}**")
        if st.button("LOAD ARCHIVE"):
            with st.spinner("Processing..."):
                v_df = get_all_video_metadata(st.session_state.current_cid)
                if not v_df.empty:
                    st.session_state.video_data = v_df
                    save_videos_to_db(v_df, st.session_state.current_cid)
                    st.success(f"Archived {len(v_df)} videos.")

    if st.session_state.video_data is not None:
        v_df = st.session_state.video_data
        search = st.text_input("🔍 Search titles...", placeholder="Type to filter...")
        filtered = v_df[v_df['title'].str.contains(search, case=False)] if search else v_df
        with st.container(border=True):
            st.dataframe(filtered, use_container_width=True, hide_index=True)

def show_dashboard():
    if not st.session_state.current_cid:
        st.warning("⚠️ No channel selected. Go to Channel first.")
        return
    
    st.markdown('<h1 class="page-title">Statistics <span class="blue-accent">Dashboard</span></h1>', unsafe_allow_html=True)

    if st.session_state.video_data is not None:
        df = st.session_state.video_data
        
        rd1, rd2 = st.columns(2)
        with rd1:
            with st.container(border=True):
                st.markdown("### Top 10 Videos")
                top_10 = df.nlargest(10, 'view_count')
                fig = px.bar(top_10, x='view_count', y='title', orientation='h', 
                             color='view_count', color_continuous_scale='Blues')
                fig.update_layout(yaxis={'autorange': 'reversed'}, showlegend=False, height=350,
                                  margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
            
        with rd2:
            with st.container(border=True):
                st.markdown("### View vs Like Engagement")
                fig = px.scatter(df, x='view_count', y='like_count', size='comment_count', 
                                 hover_name='title', color='view_count', color_continuous_scale='Blues')
                fig.update_layout(margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("💡 Load data in 'Analyzer' section to unlock charts.")

def show_about():
    st.markdown('<h1 class="page-title">About <span class="blue-accent">Project</span></h1>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### YouTube Analytics Pro v2.2")
        st.write("A high-performance research tool for professional content analysis.")
        st.divider()
        st.write("Professional Insight Suite • 2026")

# ----------------- Router -----------------
if st.session_state.navigation == "🏠 Home":
    show_home()
elif st.session_state.navigation == "🔎 Channel":
    show_analyzer()
elif st.session_state.navigation == "🎬 Videos":
    show_video_analytics()
elif st.session_state.navigation == "📈 Dashboard":
    show_dashboard()
elif st.session_state.navigation == "ℹ️ About":
    show_about()
