# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# -----------------------------
# 1️⃣ Page Config
# -----------------------------
st.set_page_config(
    page_title="CarInsight Analyzer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# 2️⃣ Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/my_cars.csv")
    return df

df = load_data()

# -----------------------------
# 3️⃣ Sidebar Filters
# -----------------------------

# Custom CSS for sidebar labels
# Custom Sidebar Styling
st.markdown("""
<style>
/* Filter labels above widgets (Brand, Year Range, etc.) */
[data-testid="stSidebar"] label {
  color: #0047AB !important;
  font-weight: 700 !important;
  background: none !important;
}

/* Multiselect "pills" (the red chips) — make them royal blue */
[data-testid="stSidebar"] [data-baseweb="tag"] {
  background-color: #002F6C !important; /* darker pill background */
  border-radius: 8px !important;
  padding: 4px 10px !important;
  display: inline-flex !important;
  align-items: center !important;
  margin: 4px 6px 4px 0 !important;
}

/* Pill text MUST be targeted (span inside the tag) to ensure white text */
[data-testid="stSidebar"] [data-baseweb="tag"] span {
  color: white !important;
  font-weight: 600 !important;
}

/* Make the pill "x" icon white too */
[data-testid="stSidebar"] [data-baseweb="tag"] svg,
[data-testid="stSidebar"] [data-baseweb="tag"] svg path {
  stroke: white !important;
  fill: white !important;
}

/* Slider accent (modern browsers) */
[data-testid="stSidebar"] input[type="range"] {
  accent-color: #0047AB !important;
}
</style>
""", unsafe_allow_html=True)


st.sidebar.header("🔹 Filter Your Data")
st.sidebar.markdown("---")

# Brand Filter
brands = df['car brand'].unique().tolist()
selected_brands = st.sidebar.multiselect("Brand", brands, default=brands)

# Year Filter
min_year = 1970
max_year = 2025
year_range = st.sidebar.slider("Year Range", min_year, max_year, (min_year, max_year))

# Transmission Filter
transmissions = df['transmission'].unique().tolist()
selected_trans = st.sidebar.multiselect("Transmission", transmissions, default=transmissions)

# Drive Filter
drives = df['drive_system'].unique().tolist()
selected_drive = st.sidebar.multiselect("Drive System", drives, default=drives)

# Engine Filter
engines = df['engine_type'].unique().tolist()
selected_engine = st.sidebar.multiselect("Engine Type", engines, default=engines)

# -----------------------------
# 4️⃣ Filter Data
# -----------------------------
filtered_df = df[
    (df['car brand'].isin(selected_brands)) &
    (df['manufacturing year'] >= year_range[0]) &
    (df['manufacturing year'] <= year_range[1]) &
    (df['transmission'].isin(selected_trans)) &
    (df['drive_system'].isin(selected_drive)) &
    (df['engine_type'].isin(selected_engine))
]

# -----------------------------
# 5️⃣ Custom Header (HTML/CSS)
# -----------------------------
header_html = """
<div style="
    background: linear-gradient(135deg, #0B486B 0%, #1E3C72 100%);
    padding: clamp(15px, 4vw, 30px);
    border-radius: 12px;
    color: white;
    text-align: center;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 90%;
    margin: 0 auto;
">
  <h1 style="
      margin: 0;
      font-size: clamp(20px, 5vw, 36px);
      font-weight: bold;
      letter-spacing: 1px; 
      text-transform: uppercase; 
      background: linear-gradient(90deg, #00c6ff, #0072ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  ">🚗 CarInsight Analyzer</h1>
  <p style="
      margin: 8px 0 0 0;
      font-size: clamp(12px, 3vw, 16px);
      color: #D1D1D1;
  ">
      Discover <b>car ratings</b>, spot <b>market trends</b>, and gain <b>insights</b> interactively
  </p>
</div>

"""
st.components.v1.html(header_html, height=160)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# 6️⃣ Metrics
# -----------------------------
metric_col1, metric_col2, metric_col3 = st.columns(3)

metric_style = "font-size: 22px; color: #0B486B;font-weight: bold;background: linear-gradient(145deg, #F5F7FA, #E0E4E8); padding: 20px 25px; border-radius: 12px;text-align: center;box-shadow: 0 8px 20px rgba(11, 72, 107, 0.2);transition: transform 0.3s ease, box-shadow 0.3s ease;max-width: 300px;margin: 10px auto;"

with metric_col1:
    st.markdown(f"<div style='{metric_style}'>✨ Average Rating<br>{round(filtered_df['rating'].mean(),2)}</div>", unsafe_allow_html=True)

with metric_col2:
    st.markdown(f"<div style='{metric_style}'>⚡ Average Horsepower<br>{round(filtered_df['horsepower'].mean(),2)}</div>", unsafe_allow_html=True)

with metric_col3:
    st.markdown(f"<div style='{metric_style}'>🛠 Total Cars<br>{filtered_df.shape[0]}</div>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# 7️⃣ Charts Styling
# -----------------------------

# Numeric Aggregation
numeric_cols = ['rating', 'horsepower', 'torque', 'length', 'height',
                'overall width with mirrors', 'overall width without mirrors',
                'curb weight', 'cargo capacity, all seats In place']

avg_aspects = filtered_df.groupby(['car brand', 'car model'])[numeric_cols].mean().reset_index()

# -----------------------------
# 8️⃣ Brand-level Insights
# -----------------------------
st.markdown("## 🔹 Brand-level Insights")
col1, col2 = st.columns(2)

with col1:
    brand_rating = avg_aspects.groupby("car brand")["rating"].mean().sort_values(ascending=False)
    plt.figure(figsize=(10,6))
    sns.barplot(x=brand_rating.values, y=brand_rating.index, palette="Blues_d")
    plt.title("Average Rating by Car Brand", fontsize=16, color="#0B486B")
    plt.xlabel("Avg Rating")
    plt.ylabel("Car Brand")
    st.pyplot(plt.gcf())

with col2:
    top_cars = filtered_df.groupby("car model")["rating"].mean().reset_index().sort_values(by="rating", ascending=False).head(10)
    plt.figure(figsize=(10,6))
    sns.barplot(data=top_cars, x="rating", y="car model", palette="Blues_d")
    plt.title("Top 10 Cars by Average Expert Rating", fontsize=16, color="#0B486B")
    plt.xlabel("Average Rating")
    plt.ylabel("Car Model")
    st.pyplot(plt.gcf())

# -----------------------------
# 9️⃣ Performance vs Rating
# -----------------------------
st.markdown("## 🔹 Performance vs Rating")
col3, col4 = st.columns(2)

with col3:
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=avg_aspects, x="horsepower", y="rating", hue="car brand", alpha=0.8, s=100)
    plt.title("Horsepower vs Rating", fontsize=16, color="#0B486B")
    plt.xlabel("Horsepower")
    plt.ylabel("Rating")
    st.pyplot(plt.gcf())

with col4:
    def simplify_engine_cyl(x):
        x = str(x).lower()
        if "inline 3" in x: return "Inline 3"
        if "inline 4" in x: return "Inline 4"
        if "inline 5" in x: return "Inline 5"
        if "inline 6" in x: return "Inline 6"
        if "v6" in x: return "V6"
        if "v8" in x: return "V8"
        if "v10" in x: return "V10"
        if "v12" in x: return "V12"
        if "flat 4" in x: return "Flat 4"
        return "Other"

    filtered_df["engine_simple"] = filtered_df["engine_type"].apply(simplify_engine_cyl)
    plt.figure(figsize=(10,6))
    sns.barplot(data=filtered_df, x="engine_simple", y="rating", estimator=np.mean, ci=None, palette="coolwarm")
    plt.title("Engine Type vs Average Rating", fontsize=16, color="#0B486B")
    plt.xlabel("Engine Type")
    plt.ylabel("Average Rating")
    st.pyplot(plt.gcf())

# -----------------------------
# 10️⃣ Transmission & Drive System
# -----------------------------
st.markdown("## 🔹 Transmission & Drive System")
col5, col6 = st.columns(2)

with col5:
    def simplify_transmission(x):
        x = str(x).lower()
        if "auto" in x: return "Automatic"
        if "manual" in x: return "Manual"
        return "Other"

    filtered_df["transmission_simplified"] = filtered_df["transmission"].apply(simplify_transmission)
    plt.figure(figsize=(8,6))
    sns.boxplot(data=filtered_df, x="transmission_simplified", y="rating", palette="Blues")
    plt.title("Transmission Type vs Rating", fontsize=16, color="#0B486B")
    plt.xlabel("Transmission")
    plt.ylabel("Expert Rating")
    st.pyplot(plt.gcf())

with col6:
    plt.figure(figsize=(8,6))
    sns.boxplot(data=filtered_df, x="drive_system", y="rating", palette="Blues")
    plt.title("Drive System vs Rating", fontsize=16, color="#0B486B")
    plt.xlabel("Drive System")
    plt.ylabel("Expert Rating")
    st.pyplot(plt.gcf())

# -----------------------------
# 11️⃣ Size / Comfort vs Rating
# -----------------------------
st.markdown("## 🔹 Size / Comfort vs Rating")
col7, col8 = st.columns(2)

with col7:
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=avg_aspects, x="cargo capacity, all seats In place", y="rating", hue="car brand", alpha=0.7, s=100)
    plt.title("Cargo Capacity vs Rating", fontsize=16, color="#0B486B")
    plt.xlabel("Cargo Capacity (litres)")
    plt.ylabel("Rating")
    st.pyplot(plt.gcf())

with col8:
    yearly_brand_avg = filtered_df.groupby(["manufacturing year", "car brand"])["rating"].mean().reset_index()
    yearly_brand_avg = yearly_brand_avg[(yearly_brand_avg["manufacturing year"] >= 2000) & (yearly_brand_avg["manufacturing year"] <= 2025)]
    plt.figure(figsize=(12,6))
    sns.lineplot(data=yearly_brand_avg, x="manufacturing year", y="rating", hue="car brand", marker="o", linewidth=2.5)
    plt.title("Average Rating Trends by Brand Over Time", fontsize=16, color="#0B486B")
    plt.xlabel("Year")
    plt.ylabel("Average Rating")
    plt.xticks(yearly_brand_avg["manufacturing year"].unique()[::2], rotation=45)
    st.pyplot(plt.gcf())

# -----------------------------
# 12️⃣ Filtered Data Table
# -----------------------------
st.markdown("## 🔹 Filtered Data Table")
st.dataframe(filtered_df.style.set_properties(**{
    'background-color': '#F5F7FA', 'color': '#0B486B', 'border-color': 'white'
}))
