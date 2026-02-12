
THEME_CONTENT = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Outfit:wght@500;700;900&display=swap" rel="stylesheet">

<style>
    /* Global Layout - Full Fit & Zero Space */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 1rem !important;
        max-width: 98% !important;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(255, 255, 255, 0.0) !important;
    }
    
    /* Ensure the sidebar toggle button is visible */
    [data-testid="stHeader"] button {
        color: #1e3a8a !important;
    }
    
    footer {
        visibility: hidden;
        height: 0;
    }

    /* Professional Sidebar - High Alignment */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        padding-top: 0 !important;
    }
    
    [data-testid="stSidebarNav"] {
        padding-top: 0 !important;
    }
    
    /* Hide collapse button to keep sidebar always visible */
    [data-testid="sidebar-close-button"], button[kind="header"] {
        /* display: none !important; */ /* Keeping it hidden is risky if it's the only way to toggle. But if user wants it visible entire session, we can hide it. */
    }

    /* Branding Area - Absolute Top */
    .sidebar-brand {
        padding: 0.5rem 1rem 0.5rem 1rem !important;
        border-bottom: 1px solid #f1f5f9;
        margin-bottom: 1rem;
    }
    
    /* Style Link Buttons to match Primary Buttons */
    .stLinkButton > a {
        background: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 2rem !important;
        border: none !important;
        width: 100%;
        text-align: center;
        text-decoration: none !important;
        display: inline-block;
        transition: all 0.2s ease;
    }
    .stLinkButton > a:hover {
        background: #1d4ed8 !important;
        color: white !important;
        transform: translateY(-1px);
    }

    /* Cards - Using Streamlit's native container border */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #edf2f7 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02) !important;
        padding: 1rem !important;
    }
    
    /* Headers - Professional Blue */
    .page-title {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-top: 0 !important;
        padding-top: 1rem !important;
        letter-spacing: -0.02em;
    }
    
    .blue-accent { color: #3b82f6; }
    
    /* Buttons */
    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 2rem !important;
        border: none !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: #1d4ed8 !important;
        transform: translateY(-1px);
    }
    /* Premium Metric Cards */
    .metrics-container {
        display: flex;
        gap: 1.5rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        flex: 1;
        min-width: 250px;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: #3b82f6;
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin: 0;
    }
    
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
</style>
"""
