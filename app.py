from datetime import datetime
import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="HMB Nuts & Spices", page_icon="🥜", layout="centered")

st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@600;700;800;900&display=swap');
        html, body, [class*="css"] { font-family: 'Mulish', sans-serif !important; background-color: #f8fafc !important; }
        .block-container { padding: 0.3rem 0.5rem !important; max-width: 480px !important; margin: auto; }
        #MainMenu, header, footer, div[data-testid="stToolbar"] {visibility: hidden; display: none;}
        
        .compact-header {
            background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
            padding: 6px 10px; border-radius: 8px; margin-bottom: 4px; border: 1px solid #fecdd3;
            display: flex; justify-content: space-between; align-items: center;
        }

        div.stButton > button {
            background: #ffffff !important;
            color: #e11d48 !important; border: 1px solid #f43f5e !important; font-weight: 800 !important; font-size: 10px !important; border-radius: 6px !important; padding: 4px !important; min-height: unset !important; width: 100% !important;
        }
        div.stButton > button:hover { background: #fff1f2 !important; }

        .login-box { width: 100%; max-width: 380px; padding: 18px; border-radius: 12px; background-color: #ffffff !important; border: 2px solid #fbcfe8 !important; text-align: center; margin: 30px auto; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

NEW_GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1b_oAav63v5OVFxJBKOBbCxyW3cVcXu2J6zJCzQUxkCc/export?format=csv&gid=0"
NEW_GOOGLE_SCRIPT_URL = ""

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_phone" not in st.session_state:
    st.session_state.user_phone = None
if "cart" not in st.session_state:
    st.session_state.cart = []
if "current_view" not in st.session_state:
    st.session_state.current_view = "Shop"
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""
if "quantities" not in st.session_state:
    st.session_state.quantities = {}

def log_login_to_sheet(name, phone):
    if not NEW_GOOGLE_SCRIPT_URL: return
    try:
        requests.post(NEW_GOOGLE_SCRIPT_URL, json={"Type": "Login", "Customer_Name": name, "Primary_Phone": phone})
    except Exception:
        pass

if not st.session_state.logged_in_user:
    st.markdown('<div style="display: flex; justify-content: center;"><div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #881337; margin-bottom: 2px;'>🥜 HMB Nuts & Spices</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b; font-size: 11px; margin-bottom: 12px;'>Thiruverkadu | Customer Login</p>", unsafe_allow_html=True)
    with st.form("mobile_login_form"):
        cust_name = st.text_input("Your Full Name:")
        cust_phone = "".join([c for c in st.text_input("Mobile Number (10 digits):", max_chars=10) if c.isdigit()])
        if st.form_submit_button("Get Started", use_container_width=True):
            if cust_name.strip() and len(cust_phone) == 10:
                st.session_state.logged_in_user = cust_name.strip()
                st.session_state.user_phone = cust_phone.strip()
                log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                st.success("Welcome!")
                st.rerun()
            else:
                st.warning("Please enter a valid name and 10-digit mobile number.")
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# Compact Top Bar with Shop Name and User Info
st.markdown(f"""
    <div class="compact-header">
        <div>
            <span style="font-size: 13px; font-weight: 900; color: #881337; text-transform: uppercase;">🥜 HMB Nuts & Spices</span>
            <span style="font-size: 9px; color: #9f1239; margin-left: 6px;">Thiruverkadu</span>
        </div>
        <div style="font-size: 10px; font-weight: 800; color: #475569;">👤 {st.session_state.logged_in_user}</div>
    </div>
""", unsafe_allow_html=True)

# Tight Navigation Action Strip
nav1, nav2, nav3 = st.columns(3, gap="small")
with nav1:
    if st.button("🏠 Shop", use_container_width=True):
        st.session_state.current_view = "Shop"
        st.rerun()
with nav2:
    cart_count = len(st.session_state.cart)
    if st.button(f"🛒 Cart ({cart_count})", use_container_width=True):
        st.session_state.current_view = "Cart"
        st.rerun()
with nav3:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.markdown("<hr style='margin: 4px 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

@st.cache_data(ttl=2)
def load_shop_inventory():
    try:
        if NEW_GOOGLE_SHEET_CSV_URL:
            df = pd.read_csv(NEW_GOOGLE_SHEET_CSV_URL)
            df.to_csv("inventory.csv", index=False)
            return df
        else:
            return pd.read_csv("inventory.csv") if os.path.exists("inventory.csv") else pd.DataFrame()
    except Exception:
        return pd.read_csv("inventory.csv") if os.path.exists("inventory.csv") else pd.DataFrame()

inv_df = load_shop_inventory()
product_records = []
if not inv_df.empty:
    for _, row in inv_df.iterrows():
        if len(row) > 4 and pd.notna(row.iloc[0]) and pd.notna(row.iloc[1]) and str(row.iloc[0]).strip() != "id":
            product_records.append({
                "id": str(row.iloc[0]), "name": str(row.iloc[1]), "category": str(row.iloc[2]).strip(),
                "stock": str(row.iloc[3]), "price": str(row.iloc[4]),
                "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "",
                "image": str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
            })

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Premium California Almonds", "price": "850", "stock": "50", "category": "Nuts", "image": "", "description": "Fresh and crunchy"},
        {"id": "ITM002", "name": "W320 Cashew Nuts", "price": "900", "stock": "40", "category": "Nuts", "image": "", "description": "Whole premium cashews"},
        {"id": "ITM003", "name": "Raw Pumpkin Seeds", "price": "350", "stock": "100", "category": "Seeds", "image": "", "description": "High in antioxidants"}
    ]

all_categories = sorted(list(set([p['category'] for p in product_records if p['category']])))
if not st.session_state.selected_category or st.session_state.selected_category not in all_categories:
    if all_categories: st.session_state.selected_category = all_categories[0]

def process_order_submission(address, secondary_phone, description):
    if not st.session_state.cart: return "Cart is empty."
    cart_summary = ", ".join([f"{i['quantity']} of {i['product']}" for i in st.session_state.cart])
    if NEW_GOOGLE_SCRIPT_URL:
        try:
            requests.post(NEW_GOOGLE_SCRIPT_URL, json={
                "Type": "Order", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Customer_Name": st.session_state.logged_in_user, "Primary_Phone": st.session_state.user_phone,
                "Items": cart_summary, "Address": address, "Secondary_Phone": secondary_phone, "Description": description
            })
        except Exception:
            pass
    st.session_state.cart = []
    return f"Order placed successfully for: {cart_summary}!"

if st.session_state.current_view == "Shop":
    search_query = st.text_input("Search", placeholder="🔍 Search dry fruits, nuts, seeds...", label_visibility="collapsed")

    if all_categories:
        cat_cols = st.columns(len(all_categories), gap="small")
        for i, cat in enumerate(all_categories):
            with cat_cols[i]:
                is_selected = (st.session_state.selected_category == cat)
                if st.button(cat, key=f"pill_{cat}", use_container_width=True):
                    st.session_state.selected_category = cat
                    st.rerun()

    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
    current_cat = st.session_state.get("selected_category", all_categories[0] if all_categories else "")
    
    if search_query.strip():
        filtered_products = [p for p in product_records if search_query.lower() in p['name'].lower() or search_query.lower() in p['category'].lower()]
        st.markdown(f"<p style='font-size: 11px; font-weight: 700; color: #64748b;'>Search Results for '{search_query}'</p>", unsafe_allow_html=True)
    else:
        filtered_products = [p for p in product_records if p['category'] == current_cat]
        st.markdown(f"<p style='font-size: 11px; font-weight: 700; color: #64748b;'>⚡ Fresh in {current_cat}</p>", unsafe_allow_html=True)

    if filtered_products:
        for i in range(0, len(filtered_products), 2):
            cols = st.columns(2, gap="small")
            for j in range(2):
                if i + j < len(filtered_products):
                    prod = filtered_products[i + j]
                    idx = i + j
                    q_key = f"qty_app_{idx}"
                    if q_key not in st.session_state.quantities: st.session_state.quantities[q_key] = 1
                    
                    with cols[j]:
                        with st.container(border=True):
                            st.markdown("<div style='background: #f1f5f9; height: 50px; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 9px; font-weight: 800; margin-bottom: 4px;'>📦 HMB FRESH</div>", unsafe_allow_html=True)
                            st.markdown("<div style='color: #0284c7; font-size: 9px; font-weight: 800;'>⚡ 5 MINS</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-weight: 800; font-size: 11px; height: 28px; overflow: hidden; color: #0f172a;'>{prod['name']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='color: #64748b; font-size: 9px; height: 16px; overflow: hidden;'>{prod['description']}</div>", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-weight: 900; font-size: 12px; color: #e11d48; margin: 2px 0;'>₹{prod['price']}</div>", unsafe_allow_html=True)
                            
                            if st.button("ADD +", key=f"add_app_{idx}", use_container_width=True):
                                st.session_state.cart.append({"product": prod['name'], "quantity": "1 Unit"})
                                st.success("Added!")
                                st.rerun()
    else:
        st.info("No items found.")
else:
    st.markdown("### 🛒 Your Shopping Cart")
    if st.session_state.cart:
        for idx, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([4, 1], gap="small")
            with c1: st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with c2:
                if st.button("✕", key=f"rem_{idx}", use_container_width=True):
                    st.session_state.cart.pop(idx)
                    st.rerun()
        
        st.markdown("---")
        st.markdown("#### Delivery Checkout")
        with st.form("mobile_checkout"):
            address = st.text_area("Delivery Address (Thiruverkadu area):")
            sec_phone = "".join([c for c in st.text_input("Alternate Phone (10 digits):", max_chars=10) if c.isdigit()])
            desc = st.text_input("Special instructions (optional):")
            if st.form_submit_button("Place Order Now", use_container_width=True):
                if address.strip() and len(sec_phone) == 10:
                    res_msg = process_order_submission(address, sec_phone, desc)
                    st.success(res_msg)
                    st.session_state.current_view = "Shop"
                    st.rerun()
                else:
                    st.warning("Please provide a valid delivery address and 10-digit alternate phone number.")
    else:
        st.info("Your cart is empty. Go back to Shop to add items.")
