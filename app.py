import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Premium Retail Sales Dashboard", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #f8f9fa; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
    }
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        color: #f8fafc;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }
    h1 { color: #1e3a8a !important; font-weight: 800 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

LOGO_URL = "https://img.icons8.com/color/120/000000/shop.png"
st.sidebar.image(LOGO_URL, width=80)
st.sidebar.title("NexaRetail Corp")
st.sidebar.markdown("*Enterprise Analytics Platform*")
st.sidebar.divider()

sns.set_theme(style="whitegrid")
st.title("📊 Retail Sales Data Analysis & Visualization")
st.markdown("An executive-level interactive analytical system built for retail datasets.")

uploaded_file = st.file_uploader("Upload the Retail Sales CSV file to initialize dashboard analytics", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df["Month"] = df["Date"].dt.month
        df["Month Name"] = df["Date"].dt.month_name()

    st.sidebar.header("🔎 Interactive Filters")

    if "Gender" in df.columns:
        genders = st.sidebar.multiselect(
            "Filter by Gender",
            sorted(df["Gender"].dropna().unique()),
            default=sorted(df["Gender"].dropna().unique()),
        )
        df = df[df["Gender"].isin(genders)]

    if "Product Category" in df.columns:
        categories = st.sidebar.multiselect(
            "Filter by Product Category",
            sorted(df["Product Category"].dropna().unique()),
            default=sorted(df["Product Category"].dropna().unique()),
        )
        df = df[df["Product Category"].isin(categories)]

    st.subheader("📌 Performance Overview (KPIs)")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Transactions", f"{len(df):,}")
    c2.metric("Total Sales Revenue", f"${df['Total Amount'].sum():,.2f}")
    c3.metric("Total Quantity Sold", f"{df['Quantity'].sum():,.0f}")
    c4.metric("Avg. Order Value", f"${df['Total Amount'].mean():,.2f}")
    c5.metric("Avg. Customer Age", f"{df['Age'].mean():.1f} yrs")

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales Performance", "👥 Demographic Analysis", "🔗 Core Relationships", "📋 Data Inventory"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Total Sales Revenue by Product Category")
            category_sales = df.groupby("Product Category")["Total Amount"].sum()
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(category_sales.index, category_sales.values, color=["#3b82f6", "#10b981", "#f59e0b"])
            ax.set_ylabel("Total Sales ($)")
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.subheader("Average Basket Value by Category")
            average_category = df.groupby("Product Category")["Total Amount"].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=average_category.index, y=average_category.values, ax=ax, palette="Blues_r")
            ax.set_ylabel("Average Value ($)")
            st.pyplot(fig)
            plt.close(fig)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Customer Volume Distribution by Gender")
            gender_count = df["Gender"].value_counts()
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(gender_count.values, labels=gender_count.index, autopct="%1.1f%%", colors=["#60a5fa", "#f87171"])
            st.pyplot(fig)
            plt.close(fig)

        with col2:
            st.subheader("Revenue Contribution by Gender")
            gender_sales = df.groupby("Gender")["Total Amount"].sum()
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.bar(gender_sales.index, gender_sales.values, color=["#60a5fa", "#f87171"])
            ax.set_ylabel("Total Sales ($)")
            st.pyplot(fig)
            plt.close(fig)

    with tab3:
        st.subheader("Feature Correlation Heatmap")
        numeric_data = df.select_dtypes(include=np.number)
        correlation = numeric_data.corr()
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(correlation, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
        plt.close(fig)

    with tab4:
        st.subheader("Complete Interactive Raw Dataset View")
        st.dataframe(df, use_container_width=True)

else:
    st.info("Welcome to the portal. Please upload your dataset inside the upload zone to view dynamic statistics.")
