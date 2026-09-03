# 1. Streamlit Page Configuration & Professional E-Commerce Styling CSS
st.set_page_config(
    page_title="HMB Nuts and Seeds",
    page_icon="🥜",
    layout="wide",
)

# Enforce strict mobile viewport scaling to fit all phone screens automatically
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@700;800;900&display=swap');

        /* Lock screen width to prevent horizontal overflow or scrolling */
        html, body, [class*="css"] {
            font-family: 'Mulish', sans-serif !important;
            font-size: 16px !important;
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }

        .stApp {
            background-color: #fff5f8 !important; 
            max-width: 100vw !important;
            overflow-x: hidden !important;
        }

        /* Restrict main container margins so everything aligns safely on mobile screens */
        .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 100% !important;
            overflow-x: hidden !important;
        }

        /* Hide Streamlit default top header, menu, share, github, and badges */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden; display: none;}
        section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        iframe[title="streamlit_app.manage"] {display: none !important;}
        .manage-app {display: none !important;}
        div[class*="viewerBadge"] {display: none !important;}
        div[data-testid="stDecoration"] {display: none;}
        
        /* Completely HIDE "Press Enter to submit form" tooltip & instruction popups */
        [data-testid="InputInstructions"],
        div[data-testid="InputInstructions"],
        span[data-testid="InputInstructions"],
        .stTextInput div[data-testid="InputInstructions"],
        div[data-testid="stFormSubmitButtonInstructions"] {
            display: none !important;
            visibility: hidden !important;
            height: 0px !important;
        }

        /* Hide header link icons and full-screen tools */
        a.stMarkdownHeaderLink {display: none !important;}
        h1 svg, h2 svg, h3 svg, h4 svg, h5 svg, h6 svg {display: none !important;}
        button[kind="header"] {visibility: hidden !important;}

        /* Target all possible image hover toolbars and full screen elements */
        [data-testid="stImage"] button,
        [data-testid="imageToolbar"],
        button[title*="View fullscreen"],
        button[title*="Zoom"],
        button[aria-label*="Zoom"],
        button[aria-label*="Fullscreen"],
        div[data-testid="StyledFullScreenButton"],
        div[class*="imageToolbar"],
        div[class*="toolbar"],
        div[data-testid="stImageContainer"] button {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        
        /* Enforce full-box filling and edge-to-edge cover sizing for all images */
        [data-testid="stImage"] {
            width: 100% !important;
            pointer-events: none !important;
        }
        [data-testid="stImage"] img {
            width: 100% !important;
            height: 100px !important;
            object-fit: cover !important;
            border-radius: 8px !important;
            pointer-events: none !important;
        }
        
        /* High contrast text formatting */
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 16px !important;
        }
        
        /* Input boxes styling with explicit light mode colors */
        input, textarea, div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 2px solid #cbd5e1 !important;
            font-size: 18px !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
        }
        input:focus, textarea:focus {
            border-color: #f472b6 !important;
            box-shadow: 0 0 0 3px rgba(244, 114, 182, 0.15) !important;
        }

        /* Soft Light Pink Gradient Header Banner */
        .brand-banner {
            background: linear-gradient(135deg, #ffe4e6 0%, #fbcfe8 100%);
            padding: 10px 12px;
            border-radius: 10px;
            color: #831843 !important;
            text-align: center;
            box-shadow: 0 3px 10px -2px rgba(251, 207, 232, 0.3);
            margin-bottom: 8px;
            border: 1px solid #fbcfe8;
            width: 100%;
            box-sizing: border-box;
        }
        .brand-banner .brand-title {
            font-family: 'Mulish', sans-serif !important;
            font-size: 26px !important;
            font-weight: 900 !important;
            letter-spacing: 0.5px;
            color: #831843 !important;
            margin: 0 0 2px 0;
            text-transform: lowercase;
        }
        .brand-banner .brand-phone {
            font-size: 15px !important;
            font-weight: 800 !important;
            letter-spacing: 0.5px;
            color: #9d174d !important;
            margin: 0;
        }

        /* Light Pink Streamlit Buttons */
        div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #ffe4e6 0%, #fbcfe8 100%) !important;
            color: #0f172a !important;
            border: 1px solid #f472b6 !important;
            font-weight: 800 !important;
            font-size: 16px !important;
            border-radius: 10px !important;
            padding: 0.5rem 0.6rem !important;
            width: 100% !important;
            display: block !important;
            box-shadow: 0 4px 12px rgba(251, 207, 232, 0.4) !important;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
            background: linear-gradient(135deg, #fbcfe8 0%, #f472b6 100%) !important;
            color: #0f172a !important;
            box-shadow: 0 6px 15px rgba(244, 114, 182, 0.5) !important;
        }

        /* Fully responsive login wrapper centered perfectly */
        .login-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding-top: 1rem;
            width: 100%;
            box-sizing: border-box;
        }

        @media (max-width: 900px) {
            .stMainBlockContainer div[data-testid="stHorizontalBlock"]:first-of-type {
                flex-direction: row !important;
                flex-wrap: nowrap !important;
            }
            .stMainBlockContainer div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="column"] {
                width: auto !important;
                flex: 1 1 auto !important;
                min-width: 0px !important;
                padding: 0px 2px !important;
            }

            div[data-testid="stHorizontalBlock"]:not(:first-of-type) {
                flex-direction: column !important;
                flex-wrap: wrap !important;
            }
            div[data-testid="stHorizontalBlock"]:not(:first-of-type) > div[data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
                min-width: 100% !important;
                padding: 4px 0px !important;
            }
        }

        .login-title {
            text-align: center;
            margin: 5px 0 10px 0;
            width: 100%;
        }

        .login-title h1 {
            font-family: 'Mulish', sans-serif !important;
            font-size: 28px !important;
            font-weight: 900 !important;
            margin: 0 0 5px 0;
            color: #0f172a !important;
            text-transform: lowercase;
        }

        .login-title p {
            font-size: 14px !important;
            color: #64748b !important;
            margin: 0;
        }

        .login-card {
            width: 100%;
            max-width: 100%;
            margin: 0 auto;
            padding: 15px;
            border-radius: 12px;
            background-color: #ffffff !important;
            border: 2px solid #fbcfe8 !important;
            box-shadow: 0 10px 25px -5px rgba(251, 207, 232, 0.3);
            text-align: center;
            box-sizing: border-box;
        }

        .login-card h3 {
            margin: 0 0 10px 0;
            font-size: 20px !important;
            font-weight: 800 !important;
            color: #1e293b !important;
        }

        div[data-testid="stForm"] {
            border: none !important;
            padding: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)
