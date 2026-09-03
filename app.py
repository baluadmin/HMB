from datetime import datetime
import csv
import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="HMB Nuts and Seeds", page_icon="🥜", layout="wide")

st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Mulish:wght@700;800;900&display=swap');
        html, body, [class*="css"] { font-family: 'Mulish', sans-serif !important; font-size: 14px !important; }
        .stApp { background-color: #fff5f8 !important; }
        .block-container { padding: 0.3rem 0.4rem !important; max-width: 100% !important; }
        #MainMenu, header, footer, div[data-testid="stToolbar"], section[data-testid="stStatusWidget"] {visibility: hidden; display: none;}
        
        .brand-banner {
            background: linear-gradient(135deg, #ffe4e6 0%, #fbcfe8 100%);
            padding: 6px 8px; border-radius: 8px; text-align: center; margin-bottom: 4px; border: 1px solid #fbcfe8;
        }
        .brand-banner .brand-title { font-size: 18px !important; font-weight: 900 !important; color: #831843 !important; margin: 0 0 2px 0; text-transform: lowercase; }
        .brand-banner .brand-phone { font-size: 12px !important; font-weight: 800 !important; color: #9d174d !important; margin: 0; }

        div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #ffe4e6 0%, #fbcfe8 100%) !important;
            color: #0f172a !important; border: 1px solid #f472b6 !important; font-weight: 800 !important; font-size: 12px !important; border-radius: 6px !important; width: 100% !important;
        }

        @media (max-width: 768px) {
            div[data-testid="stHorizontalBlock"] { flex-direction: column !important; flex-wrap: wrap !important; }
            div[data-testid="stHorizontalBlock"] > div[data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; min-width: 100% !important; padding: 2px 0px !important; }
        }
        .login-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 1.5rem; width: 100%; }
        .login-card { width: 100%; max-width: 380px; padding: 12px; border-radius: 10px; background-color: #ffffff !important; border: 2px solid #fbcfe8 !important; text-align: center; margin: 0 auto; }
    </style>
""", unsafe_allow_html=True)

if "logged_in_user" not in st.session_state:
    st.session_state.update({
        "logged_in_user": None, "user_phone": None, "user_role": None,
        "cart": [], "current_view": "Home", "selected_menu": "Nuts",
        "product_page": 0, "quantities": {}
    })

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzq1vB7RSGZA8aM5QOOxpSKxN06vEpYs14Yupx687pWZ4KNa0bkvAEO12QJQZ_v88DT/exec"

def log_login_to_sheet(name, phone):
    try:
        requests.post(GOOGLE_SCRIPT_URL, json={"Type": "Login", "Customer_Name": name, "Primary_Phone": phone})
    except Exception:
        pass

if not st.session_state.logged_in_user:
    st.markdown('<div class="login-wrapper"><div style="text-align:center; margin-bottom:15px;"><h1>hmb nuts and seeds</h1><p>Thiruverkadu - 📞 9840450113</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-card"><h3>Customer Portal Login</h3>', unsafe_allow_html=True)
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

st.markdown('<div class="brand-banner"><h1 class="brand-title">hmb nuts and seeds thiruverkadu</h1><p class="brand-phone">📞 Mobile: 9840450113</p></div>', unsafe_allow_html=True)

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
        df = pd.read_csv("https://docs.google.com/spreadsheets/d/1zXy8vwQtv2h5PooBLLEfVHAI_-aNBJK2K44kEMvczLQ/export?format=csv")
        df.to_csv("inventory.csv", index=False)
        return df
    except Exception:
        return pd.read_csv("inventory.csv") if os.path.exists("inventory.csv") else pd.DataFrame()

inv_df = load_inventory_from_sheet()
product_records = []
if not inv_df.empty:
    for _, row in inv_df.iterrows():
        product_records.append({
            "id": str(row.iloc[0]), "name": str(row.iloc[1]), "category": str(row.iloc[2]),
            "stock": str(row.iloc[3]), "price": str(row.iloc[4]),
            "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "",
            "image": str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
        })

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Premium California Almonds", "price": "850", "stock": "50", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM002", "name": "W320 Cashew Nuts", "price": "900", "stock": "40", "category": "Nuts", "image": "", "description": ""},
        {"id": "ITM005", "name": "Raw Pumpkin Seeds", "price": "350", "stock": "200", "category": "Seeds", "image": "", "description": ""},
        {"id": "ITM009", "name": "Afghani Dried Black Raisins", "price": "450", "stock": "45", "category": "Dry Fruits", "image": "", "description": ""},
        {"id": "ITM012", "name": "Mixed Dry Fruits Gift Box", "price": "1500", "stock": "60", "category": "Gift Box", "image": "", "description": ""}
    ]

def process_cart_checkout(address, secondary_phone, description):
    if not st.session_state.cart: return "Your cart is empty."
    cart_summary = ", ".join([f"{i['quantity']} of {i['product']}" for i in st.session_state.cart])
    try:
        requests.post(GOOGLE_SCRIPT_URL, json={
            "Type": "Order", "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Customer_Name": st.session_state.logged_in_user, "Primary_Phone": st.session_state.user_phone,
            "Items": cart_summary, "Address": address, "Secondary_Phone": secondary_phone, "Description": description
        })
    except Exception:
        pass
    st.session_state.cart = []
    return f"Order placed for: {cart_summary}."

if st.session_state.current_view == "Home":
    col_menu, col_items = st.columns([1.1, 2.4], gap="small")
    with col_menu:
        st.markdown("#### Menu")
        for cat in set([p['category'] for p in product_records]):
            if st.button(cat, key=f"menu_btn_{cat}", use_container_width=True):
                st.session_state.update({"selected_menu": cat, "product_page": 0})
                st.rerun()

    with col_items:
        current_cat = st.session_state.get("selected_menu", "Nuts")
        st.markdown(f"#### {current_cat}")
        filtered = [p for p in product_records if p['category'] == current_cat]
        
        if filtered:
            per_page = 5
            total_pages = max(1, (len(filtered) + per_page - 1) // per_page)
            if st.session_state.product_page >= total_pages: st.session_state.product_page = 0
            
            for idx, prod in enumerate(filtered[st.session_state.product_page * per_page : (st.session_state.product_page + 1) * per_page]):
                q_key = f"qty_{current_cat}_{idx}"
                if q_key not in st.session_state.quantities: st.session_state.quantities[q_key] = 1
                
                with st.container(border=True):
                    st.markdown(f"**{prod['name']}** — **₹{prod['price']}**")
                    q_m, q_d, q_p = st.columns([1, 1, 1], gap="small")
                    with q_m:
                        if st.button("-", key=f"m_{q_key}", use_container_width=True) and st.session_state.quantities[q_key] > 1:
                            st.session_state.quantities[q_key] -= 1; st.rerun()
                    with q_d: st.markdown(f"<div style='text-align:center;'>{st.session_state.quantities[q_key]}</div>", unsafe_allow_html=True)
                    with q_p:
                        if st.button("+", key=f"p_{q_key}", use_container_width=True):
                            st.session_state.quantities[q_key] += 1; st.rerun()
                    
                    if st.button("Add to Cart", key=f"add_{q_key}", use_container_width=True):
                        st.session_state.cart.append({"product": prod['name'], "quantity": f"{st.session_state.quantities[q_key]} Units"})
                        st.success("Added!")
                        st.rerun()
            
            if total_pages > 1:
                p_prev, p_inf, p_nxt = st.columns([1, 2, 1], gap="small")
                with p_prev:
                    if st.button("⬅ Prev", use_container_width=True) and st.session_state.product_page > 0:
                        st.session_state.product_page -= 1; st.rerun()
                with p_inf: st.markdown(f"<p style='text-align:center;'>Page {st.session_state.product_page + 1}/{total_pages}</p>", unsafe_allow_html=True)
                with p_nxt:
                    if st.button("Next ➡", use_container_width=True) and st.session_state.product_page < total_pages - 1:
                        st.session_state.product_page += 1; st.rerun()
        else:
            st.info("No items found.")
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
