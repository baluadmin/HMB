<style>
        @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@600;700;800;900&display=swap');
        html, body, [class*="css"] { font-family: 'Mulish', sans-serif !important; background-color: #f8fafc !important; }
        
        /* Pushed flush to the top edge */
        .block-container { padding-top: 0rem !important; margin-top: -1rem !important; padding-bottom: 0.4rem !important; padding-left: 0.4rem !important; padding-right: 0.4rem !important; max-width: 480px !important; margin-left: auto; margin-right: auto; }
        #MainMenu, header, footer, div[data-testid="stToolbar"] {visibility: hidden; display: none; height: 0px;}

        /* Prevent Streamlit columns from stacking on mobile screens */
        [data-testid="column"] {
            width: 50% !important;
            flex: 1 1 50% !important;
            min-width: 50% !important;
        }

        div.stButton > button {
            background: #ffffff !important;
            color: #2563eb !important; border: 1px solid #bfdbfe !important; font-weight: 800 !important; font-size: 11px !important; border-radius: 6px !important; padding: 5px !important; min-height: unset !important; width: 100% !important;
        }
        div.stButton > button:hover { background: #f0f9ff !important; }

        /* Lock the sticky header and search bar securely to the top */
        .sticky-header {
            position: sticky !important;
            top: 0px !important;
            z-index: 99999 !important;
            background-color: #f8fafc !important;
            padding-top: 10px !important;
            padding-bottom: 6px !important;
            margin-top: 0px !important;
        }

        /* Scrollable product catalog viewport wrapper */
        .scrollable-catalog {
            max-height: 72vh;
            overflow-y: auto;
            padding-right: 2px;
        }
    </style>
