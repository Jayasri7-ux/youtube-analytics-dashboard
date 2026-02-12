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
if 'video_page' not in st.session_state:
    st.session_state.video_page = 0

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

def format_count(number):
    """Formats large numbers into K and M strings."""
    if number is None:
        return "0"
    number = float(number)
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return str(int(number))

def render_metric_cards(metrics):
    """Renders metrics in a custom HTML card layout.
    Args:
        metrics (list): List of dicts with {'label', 'value', 'icon'}
    """
    cards_html = ""
    for m in metrics:
        cards_html += f"""
<div class="metric-card">
    <div class="metric-icon">{m.get('icon', '📊')}</div>
    <div class="metric-label">{m['label']}</div>
    <div class="metric-value">{m['value']}</div>
</div>
"""
    
    st.markdown(f"""
<div class="metrics-container">
    {cards_html}
</div>
""", unsafe_allow_html=True)

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
                cid_input = cid_input.strip()
                if cid_input.startswith("UC") and len(cid_input) == 24:
                    with st.spinner("Fetching..."):
                        df = extract_channel_data([cid_input])
                        if not df.empty:
                            st.session_state.channel_data = df.iloc[0]
                            st.session_state.current_cid = cid_input
                            st.session_state.video_data = None
                            st.session_state.video_page = 0
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
                render_metric_cards([
                    {"label": "Subscribers", "value": format_count(ch['subscriber_count']), "icon": "👥"},
                    {"label": "Videos", "value": format_count(ch['video_count']), "icon": "🎥"},
                    {"label": "Views", "value": format_count(ch['view_count']), "icon": "👁️"}
                ])
                
                st.divider()
                handle = ch.get("custom_url", "")
                url = f"https://youtube.com/{handle}" if handle else f"https://youtube.com/channel/{ch['channel_id']}"
                st.link_button("VISIT YOUTUBE CHANNEL", url, use_container_width=True)

def show_video_analytics():
    if not st.session_state.current_cid:
        st.warning("⚠️ No channel selected. Go to Channel first.")
        return

    st.markdown('<h1 class="page-title">Video <span class="blue-accent">Archive</span></h1>', unsafe_allow_html=True)
    
    # Calculate averages or use placeholders
    if st.session_state.video_data is not None:
        v_df = st.session_state.video_data
        avg_views = format_count(v_df['view_count'].mean())
        avg_likes = format_count(v_df['like_count'].mean())
        avg_comments = format_count(v_df['comment_count'].mean())
    else:
        avg_views = "---"
        avg_likes = "---"
        avg_comments = "---"

    # Show video-specific metrics in cards
    render_metric_cards([
        {"label": "Avg Views", "value": avg_views, "icon": "📈"},
        {"label": "Avg Likes", "value": avg_likes, "icon": "👍"},
        {"label": "Avg Comments", "value": avg_comments, "icon": "💬"}
    ])

    with st.container(border=True):
        st.write(f"Exploring video library for **{st.session_state.channel_data['channel_name']}**")
        if st.button("LOAD ARCHIVE"):
            with st.spinner("Processing..."):
                v_df = get_all_video_metadata(st.session_state.current_cid)
                if not v_df.empty:
                    st.session_state.video_data = v_df
                    st.session_state.video_page = 0
                    save_videos_to_db(v_df, st.session_state.current_cid)
                    st.success(f"Archived {len(v_df)} videos.")

    if st.session_state.video_data is not None:
        v_df = st.session_state.video_data
        search = st.text_input("🔍 Search titles...", placeholder="Type to filter...")
        filtered = v_df[v_df['title'].str.contains(search, case=False)] if search else v_df
        
        # Pagination calculations
        total_items = len(filtered)
        items_per_page = 50
        total_pages = max(1, (total_items - 1) // items_per_page + 1)
        
        # Ensure current page is within bounds
        if st.session_state.video_page >= total_pages:
            st.session_state.video_page = total_pages - 1
            
        start_idx = st.session_state.video_page * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)
        
        display_df = filtered.iloc[start_idx:end_idx]
        
        with st.container(border=True):
            st.markdown(f"**Showing {start_idx+1}-{end_idx} of {total_items}**")
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Navigation Controls
            col_p, col_info, col_n = st.columns([1, 2, 1])
            with col_p:
                if st.button("⬅️ Prev", disabled=(st.session_state.video_page == 0), use_container_width=True):
                    st.session_state.video_page -= 1
                    st.rerun()
            with col_info:
                st.markdown(f"<p style='text-align: center; margin-top: 0.5rem;'>Page {st.session_state.video_page + 1} of {total_pages}</p>", unsafe_allow_html=True)
            with col_n:
                if st.button("Next ➡️", disabled=(st.session_state.video_page >= total_pages - 1), use_container_width=True):
                    st.session_state.video_page += 1
                    st.rerun()

def show_dashboard():
    if not st.session_state.current_cid:
        st.warning("⚠️ No channel selected. Go to Channel first.")
        return
    
    st.markdown('<h1 class="page-title">Statistics <span class="blue-accent">Dashboard</span></h1>', unsafe_allow_html=True)

    if st.session_state.video_data is not None:
        df = st.session_state.video_data
        
        # Row 1: Top Videos and Engagement
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
        
        # Row 2: Posting Frequency
        with st.container(border=True):
            st.markdown("### 📅 Posting Frequency")
            
            # Prepare frequency data
            freq_df = df.copy()
            freq_df['month_year'] = freq_df['published_at'].dt.to_period('M').astype(str)
            freq_counts = freq_df.groupby('month_year').size().reset_index(name='video_count')
            freq_counts = freq_counts.sort_values('month_year')
            
            fig = px.bar(freq_counts, x='month_year', y='video_count',
                         labels={'month_year': 'Month', 'video_count': 'Videos Posted'},
                         color_discrete_sequence=['#2563eb'])
            
            fig.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=20, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title=None
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Simple summary
            avg_freq = freq_counts['video_count'].mean()
            st.info(f"💡 This channel posts approximately **{avg_freq:.1f}** videos per active month.")

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
