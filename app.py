import streamlit as st
import pandas as pd
import plotly.express as px
from analysis import load_data, clean_data, channel_analysis, csat_analysis, shift_analysis, tenure_analysis

# إعداد الصفحة
st.set_page_config(page_title="Customer Support Dashboard", layout="wide")
st.title("📞 Customer Support Business Insights")

# تحميل وتنظيف البيانات
df = load_data()
df = clean_data(df)

# ------------------------
# ✅ Sidebar Filters
# ------------------------
st.sidebar.header("📊 Filters")

# تاريخ
df['Survey_response_Date'] = pd.to_datetime(df['Survey_response_Date'])

min_date = df['Survey_response_Date'].min()
max_date = df['Survey_response_Date'].max()

selected_date_range = st.sidebar.date_input("Filter by Survey Date", [min_date, max_date])

# قناة
channels = df['channel_name'].dropna().unique().tolist()
selected_channels = st.sidebar.multiselect("Select Channels", channels, default=channels)

# شيفت
shifts = df['Agent Shift'].dropna().unique().tolist()
selected_shifts = st.sidebar.multiselect("Select Shifts", shifts, default=shifts)

# ------------------------
# ✅ Apply Filters
# ------------------------
filtered_df = df[
    (df['Survey_response_Date'].dt.date >= selected_date_range[0]) &
    (df['Survey_response_Date'].dt.date <= selected_date_range[1]) &
    (df['channel_name'].isin(selected_channels)) &
    (df['Agent Shift'].isin(selected_shifts))
]

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview", 
    "📞 Channels", 
    "⭐ CSAT Scores", 
    "🕓 Agent Shifts", 
    "🎯 Tenure Buckets", 
    "📈 CSAT Over Time",
    "🗂️ Raw Data"
])

# ----------------------------------------
# 📊 Overview Tab
with tab1:
    st.header("📊 Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tickets", len(filtered_df))
    col2.metric("Unique Categories", filtered_df['category'].nunique())
    col3.metric("Avg CSAT Score", round(filtered_df['CSAT Score'].mean(), 2))

    st.subheader("Tickets per Category")
    category_counts = filtered_df['category'].value_counts()
    fig1 = px.bar(category_counts, 
                  x=category_counts.index, 
                  y=category_counts.values, 
                  title="Tickets by Category", 
                  labels={"x": "Category", "y": "Count"})
    st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------------
# 📞 Channels Tab
with tab2:
    st.header("📞 Channel Analysis")
    channel_counts = channel_analysis(filtered_df)
    fig2 = px.pie(names=channel_counts.index, 
                  values=channel_counts.values, 
                  title="Distribution of Support Channels")
    st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------
# ⭐ CSAT Scores Tab
with tab3:
    st.header("⭐ Customer Satisfaction (CSAT) Score")
    csat_counts = csat_analysis(filtered_df)
    fig3 = px.bar(x=csat_counts.index.astype(str), 
                  y=csat_counts.values, 
                  labels={"x": "CSAT Score", "y": "Count"}, 
                  title="CSAT Score Distribution")
    st.plotly_chart(fig3, use_container_width=True)

# ----------------------------------------
# 🕓 Shifts Tab
with tab4:
    st.header("🕓 Agent Shift Analysis")
    shift_counts = shift_analysis(filtered_df)
    fig4 = px.bar(x=shift_counts.index, 
                  y=shift_counts.values, 
                  labels={"x": "Shift", "y": "Count"}, 
                  title="Tickets Handled per Shift")
    st.plotly_chart(fig4, use_container_width=True)

# ----------------------------------------
# 🎯 Tenure Tab
with tab5:
    st.header("🎯 Agent Tenure Analysis")
    tenure_counts = tenure_analysis(filtered_df)
    fig5 = px.bar(x=tenure_counts.index, 
                  y=tenure_counts.values, 
                  labels={"x": "Tenure", "y": "Count"}, 
                  title="Tickets Handled by Agent Experience Level")
    st.plotly_chart(fig5, use_container_width=True)

# ----------------------------------------
# 📈 CSAT Over Time
with tab6:
    st.header("📈 CSAT Score Over Time")
    ts = filtered_df.groupby(filtered_df['Survey_response_Date'].dt.date)['CSAT Score'].mean()
    fig6 = px.line(ts, title="Average CSAT Over Time", labels={"x": "Date", "y": "Average CSAT Score"})
    st.plotly_chart(fig6, use_container_width=True)

# ----------------------------------------
# 🗂️ Raw Data Tab
with tab7:
    st.header("🗂️ Filtered Data")
    st.dataframe(filtered_df)

    with st.expander("⬇️ Download Filtered Data"):
        st.download_button("Download CSV", data=filtered_df.to_csv(index=False), file_name="filtered_data.csv")

# ----------------------------------------

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by [Ahmed Hassan Ali](https://yourwebsite.com)")





