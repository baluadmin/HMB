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
        .block-container { padding-top: 0.8rem !important; padding-bottom: 0.4rem !important; padding-left: 0.4rem !important; padding-right: 0.4rem !important; max-width: 480px !important; margin: auto; }
        #MainMenu, header, footer, div[data-testid="stToolbar"] {visibility: hidden; display: none;}

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
    </style>
""", unsafe_allow_html=True)

NEW_GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1b_oAav63v5OVFxJBKOBbCxyW3cVcXu2J6zJCzQUxkCc/export?format=csv&gid=0"
NEW_GOOGLE_SCRIPT_URL = ""

if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""
if "quantities" not in st.session_state:
    st.session_state.quantities = {}

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
                "description": str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else "1 Pack",
                "image": str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
            })

if not product_records:
    product_records = [
        {"id": "ITM001", "name": "Premium California Almonds", "price": "850", "stock": "50", "category": "Nuts", "image": "", "description": "500g"},
        {"id": "ITM002", "name": "W320 Cashew Nuts", "price": "900", "stock": "40", "category": "Nuts", "image": "", "description": "500g"},
        {"id": "ITM003", "name": "Raw Pumpkin Seeds", "price": "350", "stock": "100", "category": "Seeds", "image": "", "description": "250g"}
    ]

all_categories = sorted(list(set([p['category'] for p in product_records if p['category']])))
if not st.session_state.selected_category or st.session_state.selected_category not in all_categories:
    if all_categories: st.session_state.selected_category = all_categories[0]

# Search Bar
search_query = st.text_input("Search", placeholder="🔍 Search dry fruits, nuts, seeds...", label_visibility="collapsed")

# Category Pill Navigation Buttons
if all_categories:
    cat_cols = st.columns(len(all_categories), gap="small")
    for i, cat in enumerate(all_categories):
        with cat_cols[i]:
            if st.button(cat, key=f"pill_{cat}", use_container_width=True):
                st.session_state.selected_category = cat
                st.rerun()

st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
current_cat = st.session_state.get("selected_category", all_categories[0] if all_categories else "")

if search_query.strip():
    filtered_products = [p for p in product_records if search_query.lower() in p['name'].lower() or search_query.lower() in p['category'].lower()]
else:
    filtered_products = [p for p in product_records if p['category'] == current_cat]

if filtered_products:
    for i in range(0, len(filtered_products), 2):
        cols = st.columns(2, gap="small")
        for j in range(2):
            if i + j < len(filtered_products):
                prod = filtered_products[i + j]
                idx = i + j
                
                raw_price_str = "".join([c for c in str(prod['price']) if c.isdigit() or c == '.'])
                base_price = float(raw_price_str) if raw_price_str else 0.0
                mrp_price = int(base_price * 1.1)
                
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div style="background: #ffffff; border-radius: 8px;">
                                <div style="background: #f1f5f9; height: 110px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8; font-size: 10px; font-weight: 800; margin-bottom: 6px;">
                                    📦 PRODUCT IMG
                                </div>
                                <div style="font-size: 9px; font-weight: 800; color: #64748b; margin-bottom: 2px;">10 MINS</div>
                                <div style="font-weight: 900; font-size: 11px; height: 32px; overflow: hidden; color: #0f172a; line-height: 1.2;">{prod['name']}</div>
                                <div style="color: #64748b; font-size: 10px; margin-top: 2px;">{prod['description']}</div>
                                <div style="color: #059669; font-size: 10px; font-weight: 800; margin-top: 4px;">10% OFF</div>
                                <div style="font-weight: 900; font-size: 13px; color: #0f172a; margin-top: 2px;">₹{int(base_price)} <span style="text-decoration: line-through; color: #94a3b8; font-size: 10px; font-weight: 600;">₹{mrp_price}</span></div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        
                        if st.button("ADD +", key=f"add_app_{idx}", use_container_width=True):
                            st.session_state.cart.append({"product": prod['name'], "quantity": "1 Unit"})
                            st.success("Added!")
                            st.rerun()
else:
    st.info("No items found.")
