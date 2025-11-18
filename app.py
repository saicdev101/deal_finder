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
    # Path to your Excel file in repo
    df = pd.read_excel(
        "2025-Saving-Dollars-and-Sense-Black-Friday-Price-Comparison-Spreadsheet.xlsx"
    )
    return df

df = load_data()

# Ensure all columns are clean strings
for col in df.columns:
    df[col] = df[col].astype(str)

# -----------------------------------
# Dashboard Title
# -----------------------------------
st.title("🛍️ Black Friday Price Comparison Dashboard")
st.markdown("### Quickly compare stores, categories, and deals for Black Friday 2025.")

# -----------------------------------
# Filters Section
# -----------------------------------
st.markdown("### 🔎 Filters")

col1, col2, col3, col4 = st.columns([2, 2, 2, 3])

with col1:
    store_filter = st.selectbox(
        "Store",
        options=["All"] + sorted(df["Store"].unique())
    )

with col2:
    category_filter = st.selectbox(
        "Category",
        options=["All"] + sorted(df["Category"].unique())
    )

with col3:
    subcat_filter = st.selectbox(
        "Sub Category",
        options=["All"] + sorted(df["Sub Category"].unique())
    )

with col4:
    search_term = st.text_input(
        "Search Product",
        placeholder="Type part of a product name..."
    )

# -----------------------------------
# Apply Filters
# -----------------------------------
filtered_df = df.copy()

if store_filter != "All":
    filtered_df = filtered_df[filtered_df["Store"] == store_filter]

if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]

if subcat_filter != "All":
    filtered_df = filtered_df[filtered_df["Sub Category"] == subcat_filter]

if search_term.strip():
    filtered_df = filtered_df[
        filtered_df["Product"].str.contains(search_term, case=False, na=False)
    ]

# -----------------------------------
# Results Table (Scrollable)
# -----------------------------------
st.markdown("### 📊 Results")
st.write(f"Showing **{len(filtered_df)}** matching products")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500  # Scrollable table
)

