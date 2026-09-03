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
        @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@700;800;900&display=swap');
        html, body, [class*="css"] { font-family: 'Mulish', sans-serif !important; font-size: 12px !important; }
        .stApp { background-color: #fff5f8 !important; }
        .block-container { padding: 0.4rem 0.6rem !important; max-width: 100% !important; }
        #MainMenu, header, footer, div[data-testid="stToolbar"], section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        
        .brand-banner {
            background: linear-gradient(135deg, #ffe4e6 0%, #fbcfe8 100%);
            padding: 6px 8px; border-radius: 6px; text-align: center; margin-bottom: 6px; border: 1px solid #fbcfe8; width: 100%; box-sizing: border-box;
        }
        .brand-banner .brand-title { font-size: 15px !important; font-weight: 900 !important; color: #831843 !important; margin: 0; text-transform: lowercase; }
        .brand-banner .brand-phone { font-size: 10px !important; font-weight: 800 !important; color: #9d174d !important; margin: 0; }

        div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #ffe4e6 0%, #fbcfe8 100%) !important;
            color: #0f172a !important; border: 1px solid #f472b6 !important; font-weight: 800 !important; font-size: 11px !important; border-radius: 4px !important; width: 100% !important; padding: 6px !important;
        }

        .login-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 1rem; width: 100%; }
        .login-card { width: 100%; max-width: 360px; padding: 10px; border-radius: 8px; background-color: #ffffff !important; border: 2px solid #fbcfe8 !important; text-align: center; margin: 0 auto; }
    </style>
""", unsafe_allow_html=True)

NEW_GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1b_oAav63v5OVFxJBKOBbCxyW3cVcXu2J6zJCzQUxkCc/export?format=csv&gid=0"
NEW_GOOGLE_SCRIPT_URL = ""

if "logged_in_user" not in st.session_state:
    st.session_state.update({
        "logged_in_user": None, "user_phone": None, "user_role": None,
        "cart": [], "current_view": "Home", "selected_menu": "", "quantities": {}
    })

def log_login_to_sheet(name, phone):
    if not NEW_GOOGLE_SCRIPT_URL:
        return
    try:
        requests.post(NEW_GOOGLE_SCRIPT_URL, json={"Type": "Login", "Customer_Name": name, "Primary_Phone": phone})
    except Exception:
        pass

if not st.session_state.logged_in_user:
    st.markdown('<div class="login-wrapper"><div style="text-align:center; margin-bottom:10px;"><h2>hmb nuts and seeds</h2><p>Thiruverkadu - 📞 9840450113</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-card"><h4>Customer Portal Login</h4>', unsafe_allow_html=True)
    with st.form("customer_direct_login_center"):
        cust_name = st.text_input("Your Name:")
        cust_phone = "".join([c for c in st.text_input("Mobile Number:", max_chars=10) if c.isdigit()])
        if st.form_submit_button("Secure Login", use_container_width=True):
            if cust_name.strip() and len(cust_phone) == 10:
                st.session_state.update({"logged_in_user": cust_name.strip(), "user_phone": cust_phone.strip(), "user_role": "Customer"})
                log_login_to_sheet(cust_name.strip(), cust_phone.strip())
                st.success("✅ Login Successful!")
                st.rerun()
            else:
                st.warning("⚠️ Provide a valid name and 10-digit mobile number.")
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

st.markdown('<div class="brand-banner"><h1 class="brand-title">hmb nuts and seeds thiruverkadu</h1><p class="brand-phone">📞 9840450113</p></div>', unsafe_allow_html=True)

top_comm, top_c1, top_c2, top_c3 = st.columns([1.5, 1, 1, 1], gap="small")
with top_comm: st.markdown(f"👋 **{st.session_state.logged_in_user}**")
with top_c1:
    if st.button("Home", use_container_width=True): st.session_state.current_view = "Home"; st.rerun()
with top_c2:
    if st.button(f"Cart({len(st.session_state.cart)})", use_container_width=True): st.session_state.current_view = "Cart"; st.rerun()
with top_c3:
    if st.button("Logout", use_container_width=True): st.session_state.clear(); st.rerun()

st.markdown("---")

@st.cache_data(ttl=2)
def load_inventory_from_sheet():
    try:
        if NEW_GOOGLE_SHEET_CSV_URL:
            df = pd.read_csv(NEW_GOOGLE_SHEET_CSV_URL)
            df.to_csv("inventory.csv", index=False)
            return df
        else:
            return pd.read_csv("inventory.csv") if os.path.exists("inventory.csv") else pd.DataFrame()
    except Exception:
        return pd.read_csv("inventory.csv") if os.path.exists("inventory.csv") else pd.DataFrame()

inv_df = load_inventory_from_sheet()
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
        {"id": "ITM001", "name": "Premium California Almonds", "price": "850", "stock": "50", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM002", "name": "W320 Cashew Nuts", "price": "900", "stock": "40", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM005", "name": "Raw Pumpkin Seeds", "price": "350", "stock": "200", "category": "Seeds", "image": "", "description": ""}
    ]

all_categories = sorted(list(set([p['category'] for p in product_records if p['category']])))
if not st.session_state.selected_menu or st.session_state.selected_menu not in all_categories:
    if all_categories:
        st.session_state.selected_menu = all_categories[0]

def process_cart_checkout(address, secondary_phone, description):
    if not st.session_state.cart: return "Your cart is empty."
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
    return f"Order placed for: {cart_summary}."

if st.session_state.current_view == "Home":
    st.markdown("##### Select Category")
    if all_categories:
        # Horizontal radio selection fits mobile screens perfectly without breaking layout
        selected_cat = st.radio("Categories", all_categories, index=all_categories.index(st.session_state.selected_menu) if st.session_state.selected_menu in all_categories else 0, horizontal=True, label_visibility="collapsed")
        if selected_cat != st.session_state.selected_menu:
            st.session_state.selected_menu = selected_cat
            st.rerun()
            
    st.markdown("---")
    current_cat = st.session_state.get("selected_menu", all_categories[0] if all_categories else "")
    st.markdown(f"##### Products: {current_cat}")
    filtered = [p for p in product_records if p['category'] == current_cat]
    
    if filtered:
        for idx, prod in enumerate(filtered):
            q_key = f"qty_{current_cat}_{idx}"
            if q_key not in st.session_state.quantities: st.session_state.quantities[q_key] = 1
            
            with st.container(border=True):
                pc1, pc2 = st.columns([2.0, 2.0], gap="small")
                with pc1:
                    st.markdown(f"**{prod['name']}**<br><span style='color:#64748b;'>₹{prod['price']}</span>", unsafe_allow_html=True)
                with pc2:
                    q_m, q_d, q_p = st.columns([1, 1, 1], gap="small")
                    with q_m:
                        if st.button("-", key=f"m_{q_key}", use_container_width=True) and st.session_state.quantities[q_key] > 1:
                            st.session_state.quantities[q_key] -= 1; st.rerun()
                    with q_d: st.markdown(f"<div style='text-align:center; font-weight:800; padding-top:2px;'>{st.session_state.quantities[q_key]}</div>", unsafe_allow_html=True)
                    with q_p:
                        if st.button("+", key=f"p_{q_key}", use_container_width=True):
                            st.session_state.quantities[q_key] += 1; st.rerun()
                
                if st.button("Add to Cart", key=f"add_{q_key}", use_container_width=True):
                    st.session_state.cart.append({"product": prod['name'], "quantity": f"{st.session_state.quantities[q_key]} Units"})
                    st.success("Added!")
                    st.rerun()
    else:
        st.info("No items found in this category.")
else:
    st.subheader("🛒 Your Shopping Cart & Checkout")
    if st.session_state.cart:
        for idx, item in enumerate(st.session_state.cart):
            c1, c2 = st.columns([4, 1])
            with c1: st.markdown(f"- **{item['product']}** ({item['quantity']})")
            with c2:
                if st.button("Remove", key=f"rem_{idx}", use_container_width=True):
                    st.session_state.cart.pop(idx); st.rerun()
        
        st.markdown("---")
        with st.form("checkout_form"):
            address = st.text_area("Delivery Address:")
            sec_phone = "".join([c for c in st.text_input("Alternative Contact Number:", max_chars=10) if c.isdigit()])
            desc = st.text_input("Product Specifications:")
            if st.form_submit_button("Complete Order", use_container_width=True):
                if address and len(sec_phone) == 10:
                    st.success(process_cart_checkout(address, sec_phone, desc))
                    st.session_state.current_view = "Home"
                    st.rerun()
                else:
                    st.warning("⚠️ Provide address and valid 10-digit alternate phone.")
    else:
      st.info("Your cart is empty.")
