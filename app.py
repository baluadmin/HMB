# -*- coding: utf-8 -*-

from datetime import datetime
import os
import pandas as pd
import urllib.parse
import requests
import streamlit as st


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="HMB Nuts & Spices",
    page_icon="🥜",
    layout="centered"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<meta name="viewport"
      content="width=device-width, initial-scale=1.0,
               maximum-scale=1.0, user-scalable=no">

<style>

@import url('https://fonts.googleapis.com/css2?family=Mulish:wght@600;700;800;900&display=swap');


/* =====================================================
   GENERAL PAGE
   ===================================================== */

html, body, [class*="css"] {
    font-family: 'Mulish', sans-serif !important;
    background-color: #f8fafc !important;
}


/* Main Streamlit content */
.block-container {
    padding-top: 0rem !important;
    margin-top: -1rem !important;

    padding-bottom: 0.4rem !important;

    padding-left: 0.4rem !important;
    padding-right: 0.4rem !important;

    max-width: 480px !important;

    margin-left: auto !important;
    margin-right: auto !important;
}


/* Hide Streamlit menus/header/footer */
#MainMenu,
header,
footer,
div[data-testid="stToolbar"] {
    visibility: hidden !important;
    display: none !important;
    height: 0px !important;
}


/* =====================================================
   TWO COLUMN MOBILE LAYOUT
   ===================================================== */

[data-testid="column"] {
    width: 50% !important;
    flex: 1 1 50% !important;
    min-width: 50% !important;
}


/* =====================================================
   BUTTONS
   ===================================================== */

div.stButton > button {
    background: #ffffff !important;

    color: #2563eb !important;

    border: 1px solid #bfdbfe !important;

    font-weight: 800 !important;

    font-size: 11px !important;

    border-radius: 6px !important;

    padding: 5px !important;

    min-height: unset !important;

    width: 100% !important;
}


div.stButton > button:hover {
    background: #f0f9ff !important;
}


/* =====================================================
   FIXED / LOCKED HEADER
   ===================================================== */

.sticky-header {
    position: fixed !important;

    top: 0 !important;

    left: 50% !important;

    transform: translateX(-50%) !important;

    width: min(480px, 100vw) !important;

    z-index: 999999 !important;

    background-color: #f8fafc !important;

    padding: 10px 10px 8px 10px !important;

    margin: 0 !important;

    box-sizing: border-box !important;

    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}


/* =====================================================
   SPACE FOR FIXED HEADER
   ===================================================== */

.header-space {
    height: 125px !important;
    width: 100% !important;
}


/* =====================================================
   SEARCH INPUT
   ===================================================== */

div[data-testid="stTextInput"] input {
    background-color: #eef2f7 !important;

    border: 1px solid #eef2f7 !important;

    border-radius: 8px !important;

    color: #334155 !important;

    font-size: 12px !important;

    height: 40px !important;

    padding-left: 12px !important;
}


/* Search input focus */
div[data-testid="stTextInput"] input:focus {
    border: 1px solid #bfdbfe !important;

    box-shadow: none !important;
}


/* =====================================================
   PRODUCT SCROLL AREA
   ===================================================== */

.scrollable-catalog {
    height: 68vh !important;

    max-height: 68vh !important;

    overflow-y: auto !important;

    overflow-x: hidden !important;

    padding-right: 3px !important;

    padding-bottom: 20px !important;

    -webkit-overflow-scrolling: touch !important;

    scrollbar-width: thin !important;
}


/* Chrome / Edge scrollbar */
.scrollable-catalog::-webkit-scrollbar {
    width: 5px !important;
}


.scrollable-catalog::-webkit-scrollbar-track {
    background: #f1f5f9 !important;
}


.scrollable-catalog::-webkit-scrollbar-thumb {
    background: #cbd5e1 !important;

    border-radius: 10px !important;
}


/* =====================================================
   PRODUCT CARDS
   ===================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 8px !important;
}


/* Product ADD button */
div.stButton > button {
    transition: 0.15s ease !important;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media screen and (max-width: 480px) {

    .sticky-header {
        width: 100vw !important;

        padding-left: 10px !important;

        padding-right: 10px !important;
    }

    .block-container {
        max-width: 100vw !important;

        padding-left: 0.4rem !important;

        padding-right: 0.4rem !important;
    }

    .header-space {
        height: 125px !important;
    }

    .scrollable-catalog {
        height: 68vh !important;

        max-height: 68vh !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SETTINGS
# =========================================================

NEW_GOOGLE_SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1b_oAav63v5OVFxJBKOBbCxyW3cVcXu2J6zJCzQUxkCc/"
    "export?format=csv&gid=0"
)

OWNER_PHONE_NUMBER = "9840450113"


# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if not isinstance(st.session_state.cart, list):
    st.session_state.cart = []


if "search_query" not in st.session_state:
    st.session_state.search_query = ""


if "current_view" not in st.session_state:
    st.session_state.current_view = "Shop"


# =========================================================
# LOAD GOOGLE SHEET INVENTORY
# =========================================================

@st.cache_data(ttl=2)
def load_shop_inventory():

    try:

        if NEW_GOOGLE_SHEET_CSV_URL:

            df = pd.read_csv(
                NEW_GOOGLE_SHEET_CSV_URL
            )

            df.to_csv(
                "inventory.csv",
                index=False
            )

            return df

        else:

            if os.path.exists("inventory.csv"):

                return pd.read_csv(
                    "inventory.csv"
                )

            return pd.DataFrame()

    except Exception:

        if os.path.exists("inventory.csv"):

            return pd.read_csv(
                "inventory.csv"
            )

        return pd.DataFrame()


# =========================================================
# CREATE PRODUCT RECORDS
# =========================================================

inv_df = load_shop_inventory()

product_records = []


if not inv_df.empty:

    for _, row in inv_df.iterrows():

        if (
            len(row) > 4
            and pd.notna(row.iloc[0])
            and pd.notna(row.iloc[1])
            and str(row.iloc[0]).strip() != "id"
        ):

            product_records.append({

                "id": str(row.iloc[0]),

                "name": str(row.iloc[1]),

                "category": (
                    str(row.iloc[2]).strip()
                ),

                "stock": str(row.iloc[3]),

                "price": str(row.iloc[4]),

                "description": (
                    str(row.iloc[5]).strip()
                    if len(row) > 5
                    and pd.notna(row.iloc[5])
                    else "1 Pack"
                ),

                "image": (
                    str(row.iloc[6]).strip()
                    if len(row) > 6
                    and pd.notna(row.iloc[6])
                    else ""
                )

            })


# =========================================================
# DEFAULT PRODUCTS
# =========================================================

if not product_records:

    product_records = [

        {
            "id": "ITM001",
            "name": "Premium California Almonds",
            "price": "850",
            "stock": "50",
            "category": "Nuts",
            "image": "",
            "description": "500g"
        },

        {
            "id": "ITM002",
            "name": "W320 Cashew Nuts",
            "price": "900",
            "stock": "40",
            "category": "Nuts",
            "image": "",
            "description": "500g"
        },

        {
            "id": "ITM003",
            "name": "Raw Pumpkin Seeds",
            "price": "350",
            "stock": "100",
            "category": "Seeds",
            "image": "",
            "description": "250g"
        }

    ]


# =========================================================
# CART VIEW
# =========================================================

if st.session_state.current_view == "Cart":

    st.markdown(
        "### Your Shopping Cart & Checkout"
    )


    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    if not isinstance(
        st.session_state.cart,
        list
    ):

        st.session_state.cart = []


    # -----------------------------------------------------
    # CART HAS ITEMS
    # -----------------------------------------------------

    if st.session_state.cart:

        for idx, item in enumerate(
            st.session_state.cart
        ):

            c1, c2 = st.columns(
                [3, 1],
                gap="small"
            )


            with c1:

                st.markdown(
                    f"- **{item.get('product', 'Item')}** "
                    f"({item.get('quantity', '1 Unit')})"
                )


            with c2:

                if st.button(
                    "Remove Item",
                    key=f"rem_{idx}",
                    use_container_width=True
                ):

                    st.session_state.cart.pop(
                        idx
                    )

                    st.rerun()


        st.markdown(
            "<hr style='margin: 8px 0;'>",
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # CHECKOUT
        # -------------------------------------------------

        st.markdown(
            "### Secure Checkout Form"
        )


        with st.form(
            "checkout_form"
        ):

            delivery_address = st.text_area(
                "Delivery Address:"
            )


            alt_contact = st.text_input(
                "Alternative Contact Number:"
            )


            custom_desc = st.text_area(
                "Product Specifications / Custom Description:"
            )


            submitted = st.form_submit_button(
                "Complete Order",
                use_container_width=True
            )


            # ---------------------------------------------
            # ORDER SUBMITTED
            # ---------------------------------------------

            if submitted:

                if (
                    delivery_address.strip()
                    and alt_contact.strip()
                ):

                    cart_summary = ", ".join(

                        [
                            f"{i.get('quantity', '1 Unit')} "
                            f"of {i.get('product', 'Item')}"
                            for i in st.session_state.cart
                        ]

                    )


                    wa_message = (
                        "*New Order - HMB Nuts & Seeds*\n\n"
                        f"*Items:* {cart_summary}\n"
                        f"*Address:* {delivery_address}\n"
                        f"*Contact:* {alt_contact}\n"
                        f"*Note:* {custom_desc}"
                    )


                    encoded_message = urllib.parse.quote(
                        wa_message
                    )


                    wa_link = (
                        "https://api.whatsapp.com/send?"
                        f"phone=91{OWNER_PHONE_NUMBER}"
                        f"&text={encoded_message}"
                    )


                    st.markdown(
                        f"""
                        <a href="{wa_link}"
                           target="_blank"
                           rel="noopener noreferrer"
                           style="text-decoration:none;">

                            <div style="
                                background:#22c55e;
                                color:white;
                                text-align:center;
                                font-weight:800;
                                font-size:13px;
                                border-radius:6px;
                                padding:12px;
                                width:100%;
                                margin-top:8px;
                                cursor:pointer;
                            ">

                                📲 Tap Here to Send Order
                                to WhatsApp Now

                            </div>

                        </a>
                        """,
                        unsafe_allow_html=True
                    )


                    st.session_state.cart = []

                    st.session_state.search_query = ""


                else:

                    st.warning(
                        "Please fill in both the delivery "
                        "address and alternative contact number."
                    )


        # -------------------------------------------------
        # RETURN TO SHOP
        # -------------------------------------------------

        if st.button(
            "Return to Shop",
            use_container_width=True
        ):

            st.session_state.search_query = ""

            st.session_state.current_view = "Shop"

            st.rerun()


    # -----------------------------------------------------
    # EMPTY CART
    # -----------------------------------------------------

    else:

        st.info(
            "Your cart is empty."
        )


        if st.button(
            "Back to Shop",
            use_container_width=True
        ):

            st.session_state.search_query = ""

            st.session_state.current_view = "Shop"

            st.rerun()


# =========================================================
# SHOP VIEW
# =========================================================

else:

    # =====================================================
    # FIXED HEADER START
    # =====================================================

    st.markdown(
        '<div class="sticky-header">',
        unsafe_allow_html=True
    )


    # =====================================================
    # SHOP NAME + CART
    # =====================================================

    top_col1, top_col2 = st.columns(
        [3, 1],
        gap="small"
    )


    # -----------------------------------------------------
    # SHOP BUTTON
    # -----------------------------------------------------

    with top_col1:

        if st.button(
            "🥜 HMB Nuts & Seeds",
            key="home_btn",
            use_container_width=True
        ):

            st.session_state.current_view = "Shop"

            st.session_state.search_query = ""

            st.rerun()


    # -----------------------------------------------------
    # CART BUTTON
    # -----------------------------------------------------

    with top_col2:

        if not isinstance(
            st.session_state.cart,
            list
        ):

            st.session_state.cart = []


        cart_count = len(
            st.session_state.cart
        )


        if st.button(
            f"🛒 Cart ({cart_count})",
            use_container_width=True
        ):

            st.session_state.current_view = "Cart"

            st.rerun()


    # =====================================================
    # DIVIDER
    # =====================================================

    st.markdown(
        """
        <hr style="
            margin:4px 0 6px 0;
            border:none;
            border-top:1px solid #e2e8f0;
        ">
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # SEARCH BAR
    # =====================================================

    srch_c1, srch_c2 = st.columns(
        [4, 1],
        gap="small"
    )


    # -----------------------------------------------------
    # SEARCH INPUT
    # -----------------------------------------------------

    with srch_c1:

        search_query = st.text_input(

            "Search",

            value=st.session_state.search_query,

            placeholder=(
                "🔍 Search dry fruits, nuts, seeds..."
            ),

            label_visibility="collapsed"

        )


    # -----------------------------------------------------
    # CLEAR BUTTON
    # -----------------------------------------------------

    with srch_c2:

        if st.button(
            "Clear",
            key="clear_search_btn",
            use_container_width=True
        ):

            st.session_state.search_query = ""

            st.rerun()


    # =====================================================
    # UPDATE SEARCH
    # =====================================================

    if (
        search_query
        != st.session_state.search_query
    ):

        st.session_state.search_query = search_query

        st.rerun()


    active_query = (
        st.session_state.search_query
        .strip()
        .lower()
    )


    # =====================================================
    # PRODUCT SEARCH FUNCTION
    # =====================================================

    def get_matching_products(
        query,
        products
    ):

        if not query:

            return products


        exact_matches = []

        fuzzy_matches = []


        for p in products:

            name_lower = (
                p["name"].lower()
            )

            cat_lower = (
                p["category"].lower()
            )


            # ---------------------------------------------
            # EXACT SEARCH
            # ---------------------------------------------

            if (
                query in name_lower
                or query in cat_lower
            ):

                exact_matches.append(p)


            # ---------------------------------------------
            # FUZZY SEARCH
            # ---------------------------------------------

            else:

                query_chars = set(query)

                name_chars = set(
                    name_lower
                )

                common_chars = (
                    query_chars
                    .intersection(name_chars)
                )


                if len(common_chars) >= max(
                    1,
                    len(query_chars) - 2
                ):

                    fuzzy_matches.append(p)


        # =================================================
        # REMOVE DUPLICATES
        # =================================================

        seen_ids = set()

        final_list = []


        for p in (
            exact_matches
            + fuzzy_matches
        ):

            if p["id"] not in seen_ids:

                seen_ids.add(
                    p["id"]
                )

                final_list.append(p)


        return final_list


    # =====================================================
    # SEARCH SUGGESTIONS
    # =====================================================

    matching_suggestions = []


    if active_query:

        matching_suggestions = (
            get_matching_products(
                active_query,
                product_records
            )
        )


    # =====================================================
    # SEARCH DROPDOWN
    # =====================================================

    if (
        matching_suggestions
        and active_query
        != matching_suggestions[0]["name"].lower()
    ):

        st.markdown(
            """
            <div style="
                background:#ffffff;
                border:1px solid #e2e8f0;
                border-radius:8px;
                margin-bottom:4px;
                box-shadow:0 4px 12px
                rgba(0,0,0,0.05);
                overflow:hidden;
            ">
            """,
            unsafe_allow_html=True
        )


        for idx, prod in enumerate(
            matching_suggestions[:6]
        ):

            sug_col1, sug_col2 = st.columns(
                [1, 6],
                gap="small"
            )


            with sug_col1:

                st.markdown(
                    """
                    <div style="
                        background:#f1f5f9;
                        width:32px;
                        height:32px;
                        border-radius:6px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:10px;
                        margin:4px auto;
                    ">
                        📦
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            with sug_col2:

                if st.button(
                    prod["name"],
                    key=f"dropdown_sug_{idx}",
                    use_container_width=True
                ):

                    st.session_state.search_query = (
                        prod["name"]
                    )

                    st.rerun()


        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # FIXED HEADER END
    # =====================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # =====================================================
    # IMPORTANT:
    # SPACE BELOW FIXED HEADER
    # =====================================================

    st.markdown(
        """
        <div class="header-space"></div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # FILTER PRODUCTS
    # =====================================================

    if not active_query:

        filtered_products = product_records

    else:

        filtered_products = (
            get_matching_products(
                active_query,
                product_records
            )
        )


    # =====================================================
    # PRODUCT SCROLL AREA
    # =====================================================

    st.markdown(
        '<div class="scrollable-catalog">',
        unsafe_allow_html=True
    )


    # =====================================================
    # DISPLAY PRODUCTS
    # =====================================================

    if filtered_products:

        for i in range(
            0,
            len(filtered_products),
            2
        ):

            cols = st.columns(
                2,
                gap="small"
            )


            for j in range(2):

                if (
                    i + j
                    < len(filtered_products)
                ):

                    prod = (
                        filtered_products[i + j]
                    )


                    idx = i + j


                    # =====================================
                    # PRICE
                    # =====================================

                    raw_price_str = "".join(

                        [
                            c
                            for c in str(
                                prod["price"]
                            )
                            if c.isdigit()
                            or c == "."
                        ]

                    )


                    try:

                        base_price = float(
                            raw_price_str
                        )

                    except:

                        base_price = 0.0


                    mrp_price = int(
                        base_price * 1.1
                    )


                    # =====================================
                    # PRODUCT CARD
                    # =====================================

                    with cols[j]:

                        with st.container(
                            border=True
                        ):

                            # -----------------------------
                            # PRODUCT DETAILS
                            # -----------------------------

                            st.markdown(

                                f"""
                                <div style="
                                    background:#ffffff;
                                    border-radius:8px;
                                ">

                                    <div style="
                                        background:#f1f5f9;
                                        height:110px;
                                        border-radius:8px;
                                        display:flex;
                                        align-items:center;
                                        justify-content:center;
                                        color:#94a3b8;
                                        font-size:10px;
                                        font-weight:800;
                                        margin-bottom:6px;
                                    ">

                                        📦 PRODUCT IMG

                                    </div>


                                    <div style="
                                        font-size:9px;
                                        font-weight:800;
                                        color:#64748b;
                                        margin-bottom:2px;
                                    ">

                                        10 MINS

                                    </div>


                                    <div style="
                                        font-weight:900;
                                        font-size:11px;
                                        height:32px;
                                        overflow:hidden;
                                        color:#0f172a;
                                        line-height:1.2;
                                    ">

                                        {prod["name"]}

                                    </div>


                                    <div style="
                                        color:#64748b;
                                        font-size:10px;
                                        margin-top:2px;
                                    ">

                                        {prod["description"]}

                                    </div>


                                    <div style="
                                        color:#059669;
                                        font-size:10px;
                                        font-weight:800;
                                        margin-top:4px;
                                    ">

                                        10% OFF

                                    </div>


                                    <div style="
                                        font-weight:900;
                                        font-size:13px;
                                        color:#0f172a;
                                        margin-top:2px;
                                    ">

                                        ₹{int(base_price)}

                                        <span style="
                                            text-decoration:line-through;
                                            color:#94a3b8;
                                            font-size:10px;
                                            font-weight:600;
                                        ">

                                            ₹{mrp_price}

                                        </span>

                                    </div>

                                </div>
                                """,

                                unsafe_allow_html=True
                            )


                            # =================================
                            # ADD TO CART
                            # =================================

                            if st.button(
                                "ADD +",
                                key=f"add_app_{idx}",
                                use_container_width=True
                            ):

                                if (
                                    "cart"
                                    not in st.session_state
                                    or not isinstance(
                                        st.session_state.cart,
                                        list
                                    )
                                ):

                                    st.session_state.cart = []


                                st.session_state.cart.append({

                                    "product": (
                                        prod["name"]
                                    ),

                                    "quantity": (
                                        "1 Unit"
                                    )

                                })


                                st.success(
                                    "Added!"
                                )


                                st.rerun()


    # =====================================================
    # NO PRODUCTS
    # =====================================================

    else:

        st.info(
            "No items found."
        )


    # =====================================================
    # END PRODUCT SCROLL AREA
    # =====================================================

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )
