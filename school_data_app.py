import streamlit as st
import pandas as pd

st.set_page_config(page_title="School Data Explorer", layout="wide")

# --- Title
st.title("📊 School Data Explorer")

# --- Upload Excel File
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.success("File uploaded successfully!")

    # --- Filter Options
    st.subheader("🔍 Filter Options")
    with st.expander("Click to filter by column"):
        columns = df.columns.tolist()
        filters = {}
        for col in columns:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) < 100:  # avoid drop-downs for large cardinality
                selected = st.multiselect(f"Filter by {col}", options=sorted(unique_vals), key=col)
                if selected:
                    filters[col] = selected

    # --- Apply Filters
    filtered_df = df.copy()
    for col, vals in filters.items():
        filtered_df = filtered_df[filtered_df[col].isin(vals)]

    # --- Display Table
    st.subheader("📋 Filtered Results")
    st.dataframe(filtered_df, use_container_width=True)

    # --- Export Button
    st.download_button(
        label="📥 Export Filtered Data to Excel",
        data=filtered_df.to_excel(index=False, engine='openpyxl'),
        file_name="filtered_school_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Please upload an Excel (.xlsx) file to get started.")
