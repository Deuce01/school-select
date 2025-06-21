import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="School Data Explorer", layout="wide")

# --- Load Default Data
@st.cache_data(show_spinner=False)
def load_default_data():
    # Use openpyxl engine explicitly
    return pd.read_excel("schools.csv.xlsx", engine="openpyxl")

df = load_default_data()

# --- Title
st.title("📊 School Data Explorer")

# --- Optional: Upload your own file
st.sidebar.header("📤 Optional: Upload Your Own File")
uploaded_file = st.sidebar.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    st.sidebar.success("✅ Custom file loaded!")

# --- Filter Options
st.subheader("🔍 Filter Options")
with st.expander("Click to filter by column"):
    filters = {}
    for col in df.columns:
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) < 100:  # Avoid filtering huge columns
            selected_vals = st.multiselect(f"Filter by {col}", options=sorted(unique_vals), key=col)
            if selected_vals:
                filters[col] = selected_vals

# --- Apply Filters
filtered_df = df.copy()
for col, selected_vals in filters.items():
    filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

# --- Show Table
st.subheader("📋 Filtered Results")
st.dataframe(filtered_df, use_container_width=True)

# --- Convert filtered data to Excel
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output

# --- Download Button
excel_bytes = convert_df_to_excel(filtered_df)
st.download_button(
    label="📥 Export Filtered Data to Excel",
    data=excel_bytes,
    file_name="filtered_school_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
