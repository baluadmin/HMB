from datetime import datetime
import csv
import os
import random
import pandas as pd
import requests
import streamlit as st

# 1. Streamlit Page Configuration & Professional E-Commerce Styling CSS
st.set_page_config(
    page_title="HMB Nuts and Seeds",
    page_icon="🥜",
    layout="wide",
)

# Enforce strict mobile viewport scaling to fit all phone screens automatically and prevent wrapping
st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@700;800;900&display=swap');

        /* Lock screen width to prevent horizontal overflow or scrolling */
        html, body, [class*="css"] {
            font-family: 'Mulish', sans-serif !important;
            font-size: 14px !important;
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
            padding-top: 0.3rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0.3rem !important;
            padding-right: 0.3rem !important;
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
            height: 70px !important;
            object-fit: cover !important;
            border-radius: 4px !important;
            pointer-events: none !important;
        }
        
        /* High contrast text formatting */
        label, .stTextInput label, p, span, div[data-testid="stMarkdownContainer"] p {
            color: #0f172a !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }
        
        /* Input boxes styling with explicit light mode colors */
        input, textarea, div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 2px solid #cbd5e1 !important;
            font-size: 15px !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            box-sizing: border-box !important;
        }
        input:focus, textarea:focus {
            border-color: #f472b6 !important;
            box-shadow: 0 0 0 3px rgba(244, 114, 182, 0.15) !important;
        }

        /* Soft Light Pink Gradient Header Banner */
        .brand-banner {
            background: linear-gradient(135deg, #ffe4e6 0%, #fbcfe8 100%);
            padding: 6px 8px;
            border-radius: 8px;
            color: #831843 !important;
            text-align: center;
            box-shadow: 0 2px 8px -2px rgba(251, 207, 232, 0.3);
            margin-bottom: 4px;
            border: 1px solid #fbcfe8;
            width: 100%;
            box-sizing: border-box;
        }
        .brand-banner .brand-title {
            font-family: 'Mulish', sans-serif !important;
            font-size: 19px !important;
            font-weight: 900 !important;
            letter-spacing: 0.5px;
            color: #831843 !important;
            margin: 0 0 2px 0;
            text-transform: lowercase;
        }
        .brand-banner .brand-phone {
            font-size: 12px !important;
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
            font-size: 13px !important;
            border-radius: 6px !important;
            padding: 0.2rem 0.3rem !important;
            width: 100% !important;
            display: block !important;
            box-shadow: 0 2px 6px rgba(251, 207, 232, 0.4) !important;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
            background: linear-gradient(135deg, #fbcfe8 0%, #f472b6 100%) !important;
            color: #0f172a !important;
        }

        /* Force ALL horizontal blocks (including top nav and products layout) to remain side-by-side without wrapping */
        div[data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            width: 100% !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            flex: 1 1 auto !important;
            min-width: 0px !important;
            padding: 0px 1px !important;
        }

        /* Fully responsive login wrapper centered perfectly */
        .login-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding-top: 1.5rem;
            width: 100%;
            box-sizing: border-box;
        }

        .login-title {
            text-align: center;
            margin: 5px 0 15px 0;
            width: 100%;
            padding: 0 10px;
            box-sizing: border-box;
        }

        .login-title h1 {
            font-family: 'Mulish', sans-serif !important;
            font-size: 24px !important;
            font-weight: 900 !important;
            margin: 0 0 5px 0;
            color: #0f172a !important;
            text-transform: lowercase;
        }

        .login-title p {
            font-size: 12px !important;
            color: #64748b !important;
            margin: 0;
        }

        .login-card-container {
            width: 100%;
            max-width: 380px;
            margin: 0 auto;
            padding: 0 10px;
            box-sizing: border-box;
        }

        .login-card {
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            background-color: #ffffff !important;
            border: 2px solid #fbcfe8 !important;
            box-shadow: 0 8px 20px -5px rgba(251, 207, 232, 0.3);
            text-align: center;
            box-sizing: border-box;
        }

        .login-card h3 {
            margin: 0 0 8px 0;
            font-size: 16px !important;
            font-weight: 800 !important;
            color: #1e293b !important;
        }

        div[data-testid="stForm"] {
            border: none !important;
            padding: 0px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_phone" not in st.session_state:
    st.session_state.user_phone = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "Home"
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "Nuts"
if "product_page" not in st.session_state:
    st.session_state.product_page = 0
if "quantities" not in st.session_state:
    st.session_state.quantities = {}

# Google Apps Script Web App Endpoint URL Updated
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"


# Function to log customer login into the "LOGIN" tab
def log_login_to_sheet(name, phone):
    try:
        payload = {
            "Type": "Login",
            "Customer_Name": name,
            "Primary_Phone": phone
        }
        requests.post(GOOGLE_SCRIPT_URL, json=payload)
    except Exception as e:
        print(f"Login sheet error: {e}")


# 2. Centered Customer Login Screen (Before Login) fully responsive for mobile screens
if not st.session_state.logged_in_user:

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)

    st.markdown("""
        <div class="login-title">
            <h1>hmb nuts and seeds</h1>
            <p>Thiruverkadu - Premium Quality Nuts, Seeds & Dry Fruits | 📞 9840450113</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-card-container">', unsafe_allow_html=True)
    st.markdown("""
        <div class="login-card">
            <h3>Customer Portal Login</h3>
        </div>
    """, unsafe_allow_html=True)

    with st.form("customer_direct_login_center", clear_on_submit=False):
        cust_name = st.text_input("Your Name:")
        
        # Raw string input for mobile number to filter out non-digits automatically
        raw_phone = st.text_input("Mobile Number:", max_chars=10)
        cust_phone = "".join([char for char in raw_phone if char.isdigit()])

        login_btn = st.form_submit_button(
            "Secure Login",
            use_container_width=True
        )

        if login_btn:
            if cust_name.strip() and len(cust_phone) == 10:
                st.session_state.logged_in_user = cust_name.strip()
                st.session_state.user_phone = cust_phone.strip()
                st.session_state.user_role = "Customer"
                st.session_state.selected_menu = "Nuts"
                st.session_state.product_page = 0

                log_login_to_sheet(
                    cust_name.strip(),
                    cust_phone.strip()
                )

                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.warning(
                    "⚠️ Please provide a valid name and exact 10-digit numeric mobile number."
                )

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# --- AFTER LOGIN: PROPERLY ARRANGED HEADER & NAVIGATION ---
st.markdown("""
    <div class="brand-banner">
        <h1 class="brand-title">hmb nuts and seeds thiruverkadu</h1>
        <p class="brand-phone">📞 Mobile: 9840450113</p>
    </div>
""", unsafe_allow_html=True)

# Navigation row: Welcome message, Home, Cart, Logout forced strictly into a single horizontal line
top_comm, top_c1, top_c2, top_c3 = st.columns([1.5, 1, 1, 1], gap="small")
with top_comm:
    st.markdown(f"👋 **{st.session_state.logged_in_user}**")
with top_c1:
    if st.button("Home", use_container_width=True):
        st.session_state.current_view = "Home"
        st.rerun()
with top_c2:
    cart_count = len(st.session_state.cart)
    if st.button(f"Cart({cart_count})", use_container_width=True):
        st.session_state.current_view = "Cart"
        st.rerun()
with top_c3:
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("---")


# Load Inventory Directly from Google Sheets CSV Link with Short TTL Cache
@st.cache_data(ttl=2)
def load_inventory_from_sheet():
    sheet_csv_url = "https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv"
    try:
        df = pd.read_csv(sheet_csv_url)
        df.to_csv("inventory.csv", index=False)
        return df
    except Exception as e:
        if os.path.exists("inventory.csv"):
            return pd.read_csv("inventory.csv")
        return pd.DataFrame()


inv_df = load_inventory_from_sheet()


# Load Product Records from Google Sheet Data dynamically with correct index mapping
product_records = []
if not inv_df.empty:
    try:
        for _, row in inv_df.iterrows():
            product_records.append({
                "id": str(row.iloc[0]),
                "name": str(row.iloc[1]),
                "category": str(row.iloc[2]),
                "stock": str(row.iloc[3]),
                "price": str(row.iloc[4]),
                "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                "image": str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
            })
    except Exception:
        product_records = []

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Premium California Almonds", "price": "850", "stock": "50", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM002", "name": "W320 Cashew Nuts", "price": "900", "stock": "40", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM003", "name": "Mamra Walnut Kernels", "price": "1200", "stock": "120", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM004", "name": "Pista Green Pistachios", "price": "1100", "stock": "90", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM005", "name": "Raw Pumpkin Seeds", "price": "350", "stock": "200", "category": "Seeds", "image": "", "description": ""},
        {"id": "ITM006", "name": "Organic Sunflower Seeds", "price": "300", "stock": "150", "category": "Seeds", "image": "", "description": ""},
        {"id": "ITM007", "name": "Chia Seeds for Weight Loss", "price": "400", "stock": "30", "category": "Seeds", "image": "", "description": ""},
        {"id": "ITM008", "name": "Nutritious Flax Seeds", "price": "250", "stock": "80", "category": "Seeds", "image": "", "description": ""},
        {"id": "ITM009", "name": "Afghani Dried Black Raisins", "price": "450", "stock": "45", "category": "Dry Fruits", "image": "", "description": ""},
        {"id": "ITM010", "name": "Premium Dried Cranberries", "price": "600", "stock": "300", "category": "Dry Fruits", "image": "", "description": ""},
        {"id": "ITM011", "name": "Medjool Dates", "price": "750", "stock": "75", "category": "Dry Fruits", "image": "", "description": ""},
        {"id": "ITM012", "name": "Mixed Dry Fruits Gift Box", "price": "1500", "stock": "60", "category": "Gift Box", "image": "", "description": ""},
        {"id": "ITM013", "name": "Daily Immunity Booster Mix", "price": "550", "stock": "85", "category": "Mixes", "image": "", "description": ""},
        {"id": "ITM014", "name": "Roasted & Salted Snack Mix", "price": "480", "stock": "110", "category": "Mixes", "image": "", "description": ""},
        {"id": "ITM015", "name": "Pure Honey with Nuts Jar", "price": "650", "stock": "150", "category": "Mixes", "image": "", "description": ""},
    ]


def process_cart_checkout(address: str, secondary_phone: str, description: str) -> str:
    """Checkout all items currently in the cart with delivery details, and send to Google Sheet 'HMB Nuts Orders'."""
    if not st.session_state.cart:
        return "Your cart is empty. Please add products first."
    
    customer_name = st.session_state.logged_in_user
    primary_phone = st.session_state.user_phone
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txn_id = "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")

    cart_summary = ", ".join([f"{item['quantity']} of {item['product']}" for item in st.session_state.cart])
    st.session_state.last_booked_item = cart_summary

    try:
        order_data = {
            "Type": "Order",
            "Timestamp": timestamp,
            "Customer_Name": customer_name,
            "Primary_Phone": primary_phone,
            "Items": cart_summary,
            "Address": address,
            "Secondary_Phone": secondary_phone,
            "Description": description
        }
        requests.post(GOOGLE_SCRIPT_URL, json=order_data)
    except Exception as e:
        print(f"Order sheet error: {e}")

    file_exists = os.path.isfile("orders.csv")
    with open("orders.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Customer Name", "Primary Phone", "Items", "Address", "Secondary Phone", "Description"])
        writer.writerow([timestamp, customer_name, primary_phone, cart_summary, address, secondary_phone, description])

    st.session_state.cart = []
    return f"Checkout complete! Order placed for: {cart_summary}. Order successful (TXN ID: {txn_id})."


# View Switching: Home View vs Cart/Checkout View
if st.session_state.current_view == "Home":
    # --- TWO-COLUMN LAYOUT MATCHING YOUR REFERENCE IMAGE ---
    col_menu, col_items = st.columns([1, 2.3], gap="small")

    with col_menu:
        st.markdown("#### Menu")
        categories = list(set([p['category'] for p in product_records]))
        for cat in categories:
            if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                st.session_state.selected_menu = cat
                st.session_state.product_page = 0
                st.rerun()

    with col_items:
        current_cat = st.session_state.get("selected_menu", "Nuts")
        st.markdown(f"#### {current_cat}")
        filtered_items = [p for p in product_records if p['category'] == current_cat]
        
        if filtered_items:
            items_per_page = 5
            total_items = len(filtered_items)
            total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
            
            if st.session_state.product_page >= total_pages:
                st.session_state.product_page = 0
            
            start_idx = st.session_state.product_page * items_per_page
            end_idx = min(start_idx + items_per_page, total_items)
            current_page_items = filtered_items[start_idx:end_idx]

            for idx, prod in enumerate(current_page_items):
                global_idx = start_idx + idx
                qty_key = f"qty_val_{current_cat}_{global_idx}"
                if qty_key not in st.session_state.quantities:
                    st.session_state.quantities[qty_key] = 1

                with st.container(border=True):
                    st.markdown(f"**{prod['name']}**")
                    st.markdown(f"**₹{prod['price']}**")
                    
                    q_minus, q_display, q_plus = st.columns([1, 1, 1], gap="small")
                    with q_minus:
                        if st.button("-", key=f"minus_{current_cat}_{global_idx}", use_container_width=True):
                            if st.session_state.quantities[qty_key] > 1:
                                st.session_state.quantities[qty_key] -= 1
                                st.rerun()
                    with q_display:
                        st.markdown(f"<div style='text-align: center; padding-top: 4px; font-weight: 800;'>{st.session_state.quantities[qty_key]}</div>", unsafe_allow_html=True)
                    with q_plus:
                        if st.button("+", key=f"plus_{current_cat}_{global_idx}", use_container_width=True):
                            st.session_state.quantities[qty_key] += 1
                            st.rerun()
                    
                    if st.button("Add to Cart", key=f"add_btn_{current_cat}_{global_idx}", use_container_width=True):
                        qty_val = st.session_state.quantities[qty_key]
                        full_q_str = f"{qty_val} Units"
                        st.session_state.cart.append({"product": prod['name'], "quantity": full_q_str})
                        st.success(f"Added!")
                        st.rerun()
            
            # Pagination Controls at the bottom
            if total_pages > 1:
                pg_prev, pg_info, pg_next = st.columns([1, 2, 1], gap="small")
                with pg_prev:
                    if st.button("⬅ Prev", use_container_width=True):
                        if st.session_state.product_page > 0:
                            st.session_state.product_page -= 1
                            st.rerun()
                with pg_info:
                    st.markdown(f"<p style='text-align: center; margin-top: 4px; font-size: 12px;'>Page {st.session_state.product_page + 1} of {total_pages}</p>", unsafe_allow_html=True)
                with pg_next:
                    if st.button("Next ➡", use_container_width=True):
                        if st.session_state.product_page < total_pages - 1:
                            st.session_state.product_page += 1
                            st.rerun()
        else:
            st.info("No items found.")

else:
    st.subheader("🛒 Your Shopping Cart & Checkout")
    if st.session_state.cart:
        for c_idx, item in enumerate(st.session_state.cart):
            cc1, cc2 = st.columns([4, 1])
            with cc1:
                st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with cc2:
                if st.button("Remove", key=f"rem_cart_view_{c_idx}__", use_container_width=True):
                    st.session_state.cart.pop(c_idx)
                    st.rerun()
        
        st.markdown("---")
        st.subheader("📍 Secure Checkout Form")
        with st.form("checkout_form_main_view"):
            checkout_address = st.text_area("Delivery Address:")
            
            raw_sec_phone = st.text_input("Alternative Contact Number:", max_chars=10)
            secondary_phone = "".join([char for char in raw_sec_phone if char.isdigit()])
            
            product_desc = st.text_area("Product Specifications / Custom Description:")
            
            submit_checkout = st.form_submit_button("Complete Order", use_container_width=True)
            if submit_checkout:
                if checkout_address and len(secondary_phone) == 10:
                    result_msg = process_cart_checkout(
                        checkout_address, secondary_phone, product_desc
                    )
                    st.success(result_msg)
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Please provide a delivery address and a valid 10-digit numeric alternative contact number.")
    else:
        _, center_msg_col, _ = st.columns([1, 2, 1])
        with center_msg_col:
            st.info("Your cart is empty. Click **Home** above to browse and add products.")
