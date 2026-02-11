
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
        display: none !important;
        height: 0 !important;
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
    
    /* Branding Area - Absolute Top */
    .sidebar-brand {
        padding: 0rem 1rem 0.5rem 1rem !important;
        margin-top: -1rem !important;
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
</style>
"""
