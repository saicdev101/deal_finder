import streamlit as st
import pandas as pd

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Black Friday Price Comparison Dashboard",
    layout="wide"
)

# -----------------------------------
# Load Data
# -----------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("2025-Saving-Dollars-and-Sense-Black-Friday-Price-Comparison-Spreadsheet.xlsx")
    return df

df = load_data()

# Convert columns to string type
for col in df.columns:
    df[col] = df[col].astype(str)

# -----------------------------------
# Initialize Session State for Filters
# -----------------------------------
default_values = {
    "store_filter": "All",
    "category_filter": "All",
    "subcat_filter": "All",
    "search_term": ""
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------------
# Reset Filters Handler
# -----------------------------------
def reset_filters():
    for key, value in default_values.items():
        st.session_state[key] = value

# -----------------------------------
# Dashboard Title
# -----------------------------------
st.title("🛍️ Black Friday Price Comparison Dashboard")
st.markdown("### Quickly compare stores, categories, and deals for Black Friday 2025.")

# -----------------------------------
# Filters Section
# -----------------------------------
st.markdown("### 🔎 Filters")

# Add reset button at the top right of filters row
reset_col, _ = st.columns([1, 8])
with reset_col:
    st.button("🔄 Reset Filters", on_click=reset_filters)

col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

with col1:
    store_filter = st.selectbox(
        "Store",
        options=["All"] + sorted(df["Store"].unique()),
        key="store_filter"
    )

with col2:
    category_filter = st.selectbox(
        "Category",
        options=["All"] + sorted(df["Category"].unique()),
        key="category_filter"
    )

with col3:
    subcat_filter = st.selectbox(
        "Sub Category",
        options=["All"] + sorted(df["Sub Category"].unique()),
        key="subcat_filter"
    )

with col4:
    search_term = st.text_input(
        "Search Product",
        placeholder="Type part of a product name...",
        key="search_term"
    )

# -----------------------------------
# Apply Filters
# -----------------------------------
filtered_df = df.copy()

if st.session_state.store_filter != "All":
    filtered_df = filtered_df[filtered_df["Store"] == st.session_state.store_filter]

if st.session_state.category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == st.session_state.category_filter]

if st.session_state.subcat_filter != "All":
    filtered_df = filtered_df[filtered_df["Sub Category"] == st.session_state.subcat_filter]

if st.session_state.search_term.strip():
    filtered_df = filtered_df[
        filtered_df["Product"].str.contains(st.session_state.search_term, case=False, na=False)
    ]

# -----------------------------------
# Results Table
# -----------------------------------
st.markdown("### 📊 Results")
st.write(f"Showing **{len(filtered_df)}** matching products")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)
