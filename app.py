import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="2025 Blackfriday Deal Finder",
    layout="wide",
    page_icon="💸"
)

# Custom theme for vibrant look
st.markdown(
    """
    <style>
    body {background-color: #f7f6ff;}
    .stApp {background-image: linear-gradient(120deg, #f5a623 0%, #f76f8e 100%);}
    div[data-testid="stSidebar"] {background-color: #2dcefa;}
    h1, .css-1d391kg {color: #f76f8e !important;}
    .stDataFrame {background: #fff7ef;}
    [data-testid="stHeader"] {background: rgba(247,111,142,0.15);}
    .css-17z0b9k {box-shadow: 0 2px 8px #f5a62340;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("### 💥 Find the Hottest 2025 Blackfriday Deals Across Major Stores!")
st.image("https://img.freepik.com/free-vector/colorful-sale-banner_23-2147511902.jpg", use_column_width=True)

# Load data
df = pd.read_excel("2025-Saving-Dollars-and-Sense-Black-Friday-Price-Comparison-Spreadsheet.xlsx")

# Clean data
products = df[df['Price'].notnull() & df['Store'].notnull()].copy()
products['Price'] = pd.to_numeric(products['Price'], errors='coerce')
products = products.dropna(subset=['Price'])

categories = df.loc[(df['Price'].isna()) & (df['Store'].isna()) & df['Unnamed: 0'].notna(), 'Unnamed: 0'].unique()
stores = sorted(products['Store'].dropna().unique())

# Sidebar filters
st.sidebar.markdown("## 🛒 Filter Your Deals")
selected_store = st.sidebar.selectbox("Choose Store", ["All"] + list(stores))
selected_category = st.sidebar.selectbox("Choose Category", ["All"] + list(categories))
search_query = st.sidebar.text_input("Search Product Name")

filtered = products.copy()
if selected_store != "All":
    filtered = filtered[filtered['Store'] == selected_store]
if selected_category != "All":
    filtered = filtered[filtered['Unnamed: 0'].str.contains(selected_category, na=False)]
if search_query:
    filtered = filtered[filtered['Unnamed: 0'].str.contains(search_query, case=False, na=False)]

st.dataframe(filtered[["Unnamed: 0", "Price", "Store", "Notes"]].rename(
    columns={"Unnamed: 0": "Product Name"}),
    use_container_width=True
)

# Vibrant bar chart
store_count = products['Store'].value_counts().reset_index()
chart = alt.Chart(store_count).mark_bar().encode(
    x=alt.X('index:N', title='Store', sort=None),
    y=alt.Y('Store:Q', title='Number of Deals'),
    color=alt.Color('index:N', scale=alt.Scale(scheme='turbo'), legend=None)
).properties(
    title="Deal Count by Store",
    width=650,
    height=350
)
st.altair_chart(chart, use_container_width=True)

st.markdown(
    "<center><b style='color:#f5a623;font-size:21px;'>Enjoy the best deals—no login required! 🎉</b></center>",
    unsafe_allow_html=True
)
