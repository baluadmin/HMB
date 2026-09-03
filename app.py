from datetime import datetime
import csv
import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="HMB Nuts and Seeds", page_icon="🥜", layout="centered")

st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@600;700;800;900&display=swap');
        html, body, [class*="css"] { font-family: 'Mulish', sans-serif !important; font-size: 11px !important; }
        .stApp { background-color: #fffafb !important; }
        .block-container { padding: 0.3rem !important; max-width: 100% !important; }
        #MainMenu, header, footer, div[data-testid="stToolbar"], section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        
        .store-header {
            background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
            padding: 6px; border-radius: 6px; text-align: center; margin-bottom: 6px; border: 1px solid #fecdd3;
        }
        .store-title { font-size: 14px !important; font-weight: 900 !important; color: #881337 !important; margin: 0; text-transform: uppercase; }
        .store-subtitle { font-size: 9px !important; font-weight: 700 !important; color: #9f1239 !important; margin: 1px 0 0 0; }

        /* Compact button sizing to fit side-by-side */
        div.stButton > button {
            background: #e11d48 !important;
            color: #ffffff !important; border: none !important; font-weight: 700 !important; font-size: 10px !important; border-radius: 3px !important; padding: 3px 2px !important; min-height: unset !important; width: 100% !important;
        }
        div.stButton > button:hover { background: #be123c !important; }

        .login-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 2rem; width: 100%; }
        .login-card { width: 100%; max-width: 360px; padding: 14px; border-radius: 10px; background-color: #ffffff !important; border: 2px solid #fbcfe8 !important; text-align: center; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

NEW_GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1b_oAav63v5OVFxJBKOBbCxyW3cVcXu2J6zJCzQUxkCc/export?format=csv&gid=0"
NEW_GOOGLE_SCRIPT_URL = ""

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
    st.markdown('<div class="login-wrapper"><div style="text-align:center; margin-bottom:10px;"><h2>HMB Nuts & Seeds</h2><p style="color:#64748b; font-size:11px;">Thiruverkadu - 📞 9840450113</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-card"><h4 style="color:#881337; margin-bottom:8px; font-size:14px;">Customer Sign In</h4>', unsafe_allow_html=True)
    with st.form("customer_login_form"):
        cust_name = st.text_input("Your Name:")
        cust_phone = "".join([c for c in st.text_input("Mobile Number:", max_chars=10) if c.isdigit()])
        if st.form_submit_button("Proceed to Shop", use_container_width=True):
            if cust_name.strip() and len(cust_phone) == 10:
                st.session_state.logged_in_user = cust_name.strip()
                st.session_state.user_phone = cust_phone.strip()
                st.session_state.user_role = "Customer"
                log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                st.success("✅ Welcome!")
                st.rerun()
            else:
                st.warning("⚠️ Enter valid name and 10-digit mobile number.")
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

st.markdown("""
    <div class="store-header">
        <h1 class="store-title">HMB Nuts & Spices</h1>
        <p class="store-subtitle">Thiruverkadu | Fresh Daily Essentials 📞 9840450113</p>
    </div>
""", unsafe_allow_html=True)

# Tight single-line layout using balanced mobile column widths
user_col, b1, b2, b3 = st.columns([1.1, 0.8, 0.9, 0.8], gap="small")
with user_col: st.markdown(f"👤 <span style='font-size:9px; font-weight:700;'>{st.session_state.logged_in_user}</span>", unsafe_allow_html=True)
with b1:
    if st.button("Shop", use_container_width=True): st.session_state.current_view = "Home"; st.rerun()
with b2:
    if st.button(f"Cart({len(st.session_state.cart)})", use_container_width=True): st.session_state.current_view = "Cart"; st.rerun()
with b3:
    if st.button("Logout", use_container_width=True): st.session_state.clear(); st.rerun()

st.markdown("---")

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

if st.session_state.current_view == "Home":
    st.markdown("##### 📂 Browse Categories")
    if all_categories:
        selected_cat = st.selectbox("Select Category", all_categories, index=all_categories.index(st.session_state.selected_category) if st.session_state.selected_category in all_categories else 0, label_visibility="collapsed")
        if selected_cat != st.session_state.selected_category:
            st.session_state.selected_category = selected_cat
            st.rerun()

    st.markdown("---")
    current_cat = st.session_state.get("selected_category", all_categories[0] if all_categories else "")
    st.markdown(f"##### 🛒 Products in {current_cat}")
    filtered_products = [p for p in product_records if p['category'] == current_cat]
    
    if filtered_products:
        for idx, prod in enumerate(filtered_products):
            q_key = f"qty_{current_cat}_{idx}"
            if q_key not in st.session_state.quantities: st.session_state.quantities[q_key] = 1
            
            with st.container(border=True):
                info_col, action_col = st.columns([2.2, 1.8], gap="small")
                with info_col:
                    st.markdown(f"**{prod['name']}**")
                    st.markdown(f"<span style='color:#e11d48; font-weight:800; font-size:11px;'>₹{prod['price']}</span> <span style='color:#64748b; font-size:9px;'>({prod['description']})</span>", unsafe_allow_html=True)
                with action_col:
                    m_btn, val_col, p_btn = st.columns([1, 1, 1], gap="small")
                    with m_btn:
                        if st.button("-", key=f"minus_{q_key}", use_container_width=True) and st.session_state.quantities[q_key] > 1:
                            st.session_state.quantities[q_key] -= 1; st.rerun()
                    with val_col:
                        st.markdown(f"<div style='text-align:center; font-weight:900; padding-top:2px;'>{st.session_state.quantities[q_key]}</div>", unsafe_allow_html=True)
                    with p_btn:
                        if st.button("+", key=f"plus_{q_key}", use_container_width=True):
                            st.session_state.quantities[q_key] += 1; st.rerun()
                
                if st.button("Add to Cart", key=f"add_cart_{q_key}", use_container_width=True):
                    st.session_state.cart.append({"product": prod['name'], "quantity": f"{st.session_state.quantities[q_key]} Units"})
                    st.success("Added to cart!")
                    st.rerun()
    else:
        st.info("No items found under this category in your spreadsheet.")
else:
    st.subheader("🛒 Your Shopping Cart & Checkout")
    if st.session_state.cart:
        for idx, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([4, 1])
            with c1: st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with c2:
                if st.button("Remove", key=f"rem_item_{idx}", use_container_width=True):
                    st.session_state.cart.pop(idx); st.rerun()
        
        st.markdown("---")
        with st.form("checkout_form"):
            address = st.text_area("Delivery Address:")
            sec_phone = "".join([c for c in st.text_input("Alternative Contact Number:", max_chars=10) if c.isdigit()])
            desc = st.text_input("Special Instructions:")
            if st.form_submit_button("Complete Order", use_container_width=True):
                if address and len(sec_phone) == 10:
                    st.success(process_order_submission(address, sec_phone, desc))
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Provide full delivery address and valid 10-digit alternate phone.")
    else:
        st.info("Your cart is currently empty. Explore categories to add items!")
