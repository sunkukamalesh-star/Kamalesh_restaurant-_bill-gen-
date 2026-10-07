import streamlit as st
from datetime import datetime
import random


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Restaurant POS & Billing",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# RESTAURANT DETAILS
# =========================================================

RESTAURANT_NAME = "SAVORY TABLE"
RESTAURANT_TAGLINE = "Restaurant Point of Sale & Billing System"
RESTAURANT_ADDRESS = "Main Road, Hyderabad, Telangana"
RESTAURANT_PHONE = "+91 98765 43210"
RESTAURANT_EMAIL = "savorytable@example.com"
RESTAURANT_GSTIN = "36ABCDE1234F1Z5"   # Demo GSTIN


# =========================================================
# MENU
# =========================================================

MENU = {
    "Starters": {
        "Paneer Tikka": {
            "price": 220,
            "type": "VEG"
        },
        "Chicken 65": {
            "price": 260,
            "type": "NON-VEG"
        },
        "Veg Manchurian": {
            "price": 190,
            "type": "VEG"
        },
        "Crispy Corn": {
            "price": 180,
            "type": "VEG"
        }
    },

    "Main Course": {
        "Paneer Butter Masala": {
            "price": 280,
            "type": "VEG"
        },
        "Chicken Curry": {
            "price": 320,
            "type": "NON-VEG"
        },
        "Butter Chicken": {
            "price": 340,
            "type": "NON-VEG"
        },
        "Veg Biryani": {
            "price": 240,
            "type": "VEG"
        },
        "Chicken Biryani": {
            "price": 300,
            "type": "NON-VEG"
        }
    },

    "Breads": {
        "Butter Naan": {
            "price": 60,
            "type": "VEG"
        },
        "Garlic Naan": {
            "price": 80,
            "type": "VEG"
        },
        "Tandoori Roti": {
            "price": 40,
            "type": "VEG"
        }
    },

    "Beverages": {
        "Fresh Lime Soda": {
            "price": 90,
            "type": "VEG"
        },
        "Cold Coffee": {
            "price": 130,
            "type": "VEG"
        },
        "Fresh Orange Juice": {
            "price": 120,
            "type": "VEG"
        },
        "Mineral Water": {
            "price": 40,
            "type": "VEG"
        }
    },

    "Desserts": {
        "Gulab Jamun": {
            "price": 100,
            "type": "VEG"
        },
        "Brownie with Ice Cream": {
            "price": 180,
            "type": "VEG"
        },
        "Vanilla Ice Cream": {
            "price": 120,
            "type": "VEG"
        }
    }
}


# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "bill" not in st.session_state:
    st.session_state.bill = None

if "invoice_number" not in st.session_state:
    st.session_state.invoice_number = 1001


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def money(value):
    """Format amount as Indian Rupees."""
    return f"₹{value:,.2f}"


def generate_invoice_number():
    """Generate next invoice number."""
    number = st.session_state.invoice_number
    st.session_state.invoice_number += 1
    return f"INV-{number}"


def add_item(item_name, price):
    """Add item to cart or increase quantity."""
    if item_name in st.session_state.cart:
        st.session_state.cart[item_name]["qty"] += 1
    else:
        st.session_state.cart[item_name] = {
            "price": price,
            "qty": 1
        }


def increase_item(item_name):
    """Increase item quantity."""
    if item_name in st.session_state.cart:
        st.session_state.cart[item_name]["qty"] += 1


def decrease_item(item_name):
    """Decrease item quantity."""
    if item_name in st.session_state.cart:

        st.session_state.cart[item_name]["qty"] -= 1

        if st.session_state.cart[item_name]["qty"] <= 0:
            del st.session_state.cart[item_name]


def delete_item(item_name):
    """Remove item completely."""
    if item_name in st.session_state.cart:
        del st.session_state.cart[item_name]


def clear_order():
    """Clear cart and current bill."""
    st.session_state.cart = {}
    st.session_state.bill = None


def calculate_bill(tax_percent, discount_percent):

    subtotal = 0

    for item in st.session_state.cart.values():
        subtotal += item["price"] * item["qty"]

    discount = subtotal * discount_percent / 100

    taxable_amount = subtotal - discount

    tax_amount = taxable_amount * tax_percent / 100

    cgst = tax_amount / 2
    sgst = tax_amount / 2

    grand_total = taxable_amount + tax_amount

    return {
        "subtotal": subtotal,
        "discount": discount,
        "taxable": taxable_amount,
        "tax": tax_amount,
        "cgst": cgst,
        "sgst": sgst,
        "grand_total": grand_total
    }


# =========================================================
# CUSTOM SIMPLE CSS
# Only styling - NO HTML CARDS / NO HTML MENU
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #777777;
        font-size: 16px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.title("🍽️ SAVORY TABLE")
st.caption(RESTAURANT_TAGLINE)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🧾 Order Details")

    customer_name = st.text_input(
        "Customer Name",
        placeholder="Enter customer name"
    )

    customer_mobile = st.text_input(
        "Mobile Number",
        placeholder="Enter mobile number"
    )

    order_type = st.selectbox(
        "Order Type",
        [
            "Dine In",
            "Take Away",
            "Delivery"
        ]
    )

    table_number = ""

    if order_type == "Dine In":

        table_number = st.text_input(
            "Table Number",
            placeholder="Example: T12"
        )

    payment_mode = st.selectbox(
        "Payment Mode",
        [
            "Cash",
            "UPI",
            "Card",
            "Credit"
        ]
    )

    st.divider()

    st.subheader("Tax & Discount")

    tax_percent = st.number_input(
        "GST / Tax %",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.5
    )

    discount_percent = st.number_input(
        "Discount %",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=0.5
    )

    st.divider()

    if st.button(
        "🗑️ Clear Current Order",
        use_container_width=True
    ):
        clear_order()
        st.rerun()


# =========================================================
# MAIN LAYOUT
# =========================================================

menu_column, cart_column = st.columns(
    [1.7, 1],
    gap="large"
)


# =========================================================
# MENU SECTION
# =========================================================

with menu_column:

    st.header("🍴 Menu")

    selected_category = st.selectbox(
        "Select Category",
        list(MENU.keys())
    )

    st.subheader(selected_category)

    selected_items = MENU[selected_category]

    for item_name, item_data in selected_items.items():

        price = item_data["price"]
        food_type = item_data["type"]

        # Native Streamlit container.
        # NO HTML INSIDE.
        with st.container(border=True):

            item_col, price_col, button_col = st.columns(
                [4, 2, 1.4],
                vertical_alignment="center"
            )

            with item_col:

                st.markdown(
                    f"**{item_name}**"
                )

                if food_type == "VEG":
                    st.caption("🟢 VEG")
                else:
                    st.caption("🔴 NON-VEG")

            with price_col:

                st.write(
                    f"**{money(price)}**"
                )

            with button_col:

                if st.button(
                    "➕ Add",
                    key=f"add_{selected_category}_{item_name}",
                    use_container_width=True
                ):

                    add_item(
                        item_name,
                        price
                    )

                    st.rerun()


# =========================================================
# CART SECTION
# =========================================================

with cart_column:

    st.header("🛒 Current Order")

    if len(st.session_state.cart) == 0:

        st.info(
            "Your cart is empty.\n\n"
            "Select an item from the menu and click Add."
        )

    else:

        for item_name, item_data in list(
            st.session_state.cart.items()
        ):

            price = item_data["price"]
            qty = item_data["qty"]
            item_total = price * qty

            with st.container(border=True):

                st.write(f"**{item_name}**")

                st.caption(
                    f"{money(price)} × {qty}"
                )

                control_col1, control_col2, control_col3, control_col4 = st.columns(
                    [1, 1, 1, 1]
                )

                with control_col1:

                    if st.button(
                        "➖",
                        key=f"minus_{item_name}",
                        use_container_width=True
                    ):

                        decrease_item(item_name)
                        st.rerun()

                with control_col2:

                    st.write(
                        f"Qty: **{qty}**"
                    )

                with control_col3:

                    if st.button(
                        "➕",
                        key=f"plus_{item_name}",
                        use_container_width=True
                    ):

                        increase_item(item_name)
                        st.rerun()

                with control_col4:

                    if st.button(
                        "🗑️",
                        key=f"delete_{item_name}",
                        use_container_width=True
                    ):

                        delete_item(item_name)
                        st.rerun()

                st.write(
                    f"**Item Total: {money(item_total)}**"
                )


# =========================================================
# BILL CALCULATION
# =========================================================

bill_values = calculate_bill(
    tax_percent,
    discount_percent
)


# =========================================================
# BILL SUMMARY
# =========================================================

st.divider()

st.header("💰 Bill Summary")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.metric(
        "Subtotal",
        money(bill_values["subtotal"])
    )

with summary_col2:
    st.metric(
        "Discount",
        money(bill_values["discount"])
    )

with summary_col3:
    st.metric(
        "Tax",
        money(bill_values["tax"])
    )

with summary_col4:
    st.metric(
        "Grand Total",
        money(bill_values["grand_total"])
    )


# =========================================================
# GENERATE BILL
# =========================================================

st.divider()

generate_col, reset_col = st.columns(2)

with generate_col:

    if st.button(
        "🧾 Generate Bill",
        type="primary",
        use_container_width=True
    ):

        if len(st.session_state.cart) == 0:

            st.error(
                "Please add at least one item before generating the bill."
            )

        else:

            invoice_number = generate_invoice_number()

            st.session_state.bill = {
                "invoice_number": invoice_number,
                "date": datetime.now().strftime(
                    "%d-%m-%Y"
                ),
                "time": datetime.now().strftime(
                    "%I:%M %p"
                ),
                "customer_name": customer_name or "Walk-in Customer",
                "customer_mobile": customer_mobile or "-",
                "order_type": order_type,
                "table_number": table_number or "-",
                "payment_mode": payment_mode,
                "tax_percent": tax_percent,
                "discount_percent": discount_percent,
                "cart": {
                    name: data.copy()
                    for name, data in st.session_state.cart.items()
                },
                "subtotal": bill_values["subtotal"],
                "discount": bill_values["discount"],
                "taxable": bill_values["taxable"],
                "tax": bill_values["tax"],
                "cgst": bill_values["cgst"],
                "sgst": bill_values["sgst"],
                "grand_total": bill_values["grand_total"]
            }

            st.success(
                f"Bill {invoice_number} generated successfully!"
            )

with reset_col:

    if st.button(
        "🆕 New Order",
        use_container_width=True
    ):

        clear_order()
        st.rerun()


# =========================================================
# GENERATED INVOICE
# =========================================================

if st.session_state.bill is not None:

    bill = st.session_state.bill

    st.divider()

    st.header("🧾 Generated Invoice")

    # Restaurant information
    with st.container(border=True):

        st.title(RESTAURANT_NAME)

        st.write(RESTAURANT_TAGLINE)

        st.write(
            f"{RESTAURANT_ADDRESS}  |  "
            f"Phone: {RESTAURANT_PHONE}"
        )

        st.write(
            f"Email: {RESTAURANT_EMAIL}"
        )

        st.write(
            f"GSTIN: {RESTAURANT_GSTIN}"
        )

        st.divider()

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:

            st.write(
                f"**Invoice No:** {bill['invoice_number']}"
            )

            st.write(
                f"**Date:** {bill['date']}"
            )

        with info_col2:

            st.write(
                f"**Time:** {bill['time']}"
            )

            st.write(
                f"**Order Type:** {bill['order_type']}"
            )

        with info_col3:

            st.write(
                f"**Customer:** {bill['customer_name']}"
            )

            st.write(
                f"**Payment:** {bill['payment_mode']}"
            )

        if bill["order_type"] == "Dine In":

            st.write(
                f"**Table:** {bill['table_number']}"
            )


    # =====================================================
    # INVOICE ITEMS
    # =====================================================

    st.subheader("Items")

    # Header
    h1, h2, h3, h4 = st.columns(
        [4, 1, 2, 2]
    )

    with h1:
        st.write("**Item**")

    with h2:
        st.write("**Qty**")

    with h3:
        st.write("**Rate**")

    with h4:
        st.write("**Amount**")


    st.divider()


    # Items
    for item_name, item_data in bill["cart"].items():

        qty = item_data["qty"]
        price = item_data["price"]
        amount = qty * price

        c1, c2, c3, c4 = st.columns(
            [4, 1, 2, 2]
        )

        with c1:
            st.write(item_name)

        with c2:
            st.write(qty)

        with c3:
            st.write(money(price))

        with c4:
            st.write(money(amount))


    # =====================================================
    # TOTALS
    # =====================================================

    st.divider()

    total_left, total_right = st.columns(
        [3, 1]
    )

    with total_left:

        st.write(
            f"**Subtotal:** {money(bill['subtotal'])}"
        )

        st.write(
            f"**Discount ({bill['discount_percent']}%):** "
            f"{money(bill['discount'])}"
        )

        st.write(
            f"**Taxable Amount:** {money(bill['taxable'])}"
        )

        st.write(
            f"**CGST:** {money(bill['cgst'])}"
        )

        st.write(
            f"**SGST:** {money(bill['sgst'])}"
        )

        st.write(
            f"**Total Tax:** {money(bill['tax'])}"
        )

    with total_right:

        st.metric(
            "GRAND TOTAL",
            money(bill["grand_total"])
        )


    # =====================================================
    # FOOTER
    # =====================================================

    st.divider()

    st.success(
        "Thank you for dining with us! ❤️"
    )

    st.caption(
        "This is a computer-generated invoice."
    )

    st.info(
        "To print this invoice, use your browser's "
        "Print option (Ctrl + P)."
    )