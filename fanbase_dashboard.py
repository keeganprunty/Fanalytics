import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Fanbase Genotyping System",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DATA LOADING & CLEANING
@st.cache_data
def load_data():
    # Ensure this file is in the same directory as your script
    return pd.read_csv("power4_attributes(Sheet1).csv")

df = load_data()

bad_schools = ["Miami", "Pitt", "Stanford", "Syracuse", "USC"]
df = df[~df["School"].isin(bad_schools)]

# 3. GENOTYPE DEFINITIONS (Moved up to prevent NameError)
genotypes = {
    "National Brand Fanatics": {
        "count": 11,
        "description": "Elite programs with massive national reach and championship culture",
        "color": "#3498db",
        "schools": ["Alabama", "Clemson", "Florida", "Georgia", "LSU", "Michigan", 
                   "Ohio State", "Oklahoma", "Tennessee", "Texas", "Texas A&M"]
    },
    "Regional Community Loyalists": {
        "count": 22,
        "description": "College towns with strong local support and unconditional loyalty",
        "color": "#2ecc71",
        "schools": ["Arizona State", "Cincinnati", "Colorado", "Florida State", 
                   "Iowa", "Iowa State", "Kansas State", "Louisville", "Minnesota", 
                   "Mississippi State", "Missouri", "NC State", "Oklahoma State", 
                   "Ole Miss", "Oregon", "Penn State", "South Carolina", "Texas Tech", 
                   "UCF", "Utah", "Virginia Tech", "Washington", "West Virginia"]
    },
    "Established Traditionalists": {
        "count": 13,
        "description": "Multi-sport fans where basketball matters alongside football",
        "color": "#e74c3c",
        "schools": ["Arizona", "Arkansas", "Auburn", "Indiana", "Kansas", "Kentucky", 
                   "Michigan State", "Nebraska", "North Carolina", "Purdue", "Rutgers", "Wisconsin"]
    },
    "Disengaged Fans": {
        "count": 2,
        "description": "High earnings with declining attendance and low engagement",
        "color": "#f39c12",
        "schools": ["California", "UCLA"]
    },
    "Selective Affluents": {
        "count": 4,
        "description": "Highest earnings with recent attendance surge and selective engagement",
        "color": "#9b59b6",
        "schools": ["Georgia Tech", "Illinois", "Maryland", "Virginia"]
    }
}

# Build lookup: school -> genotype name
genotype_lookup = {}
for genotype_name, data in genotypes.items():
    for school in data["schools"]:
        genotype_lookup[school] = genotype_name

# 4. K-MEANS CLUSTERING LOGIC
numeric_cols = [
    "5_Year_Pct_Change",
    "Instagram_Followers_FB (Thousands)",
    "Instagram_Followers_BB (Thousands)",
    "Donation_Revenue (Millions)",
    "Win_Pct_Since_2003",
    "Graduate_Earnings(Thousands)",
    "Attendence_Pct_MBB",
    "Football_Stadium_Capacity(22-25)"
]

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(df[numeric_cols])

# Map clusters to genotypes using majority vote of schools within the cluster
cluster_to_genotype = {}
for cluster_id in df["Cluster"].unique():
    schools_in_cluster = df[df["Cluster"] == cluster_id]["School"]
    mapped = schools_in_cluster.map(genotype_lookup)
    
    if not mapped.dropna().empty:
        cluster_to_genotype[cluster_id] = mapped.mode()[0]

# 5. CUSTOM CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: bold; text-align: center; color: #1f77b4; margin-bottom: 0.5rem; }
    .sub-header { font-size: 1.2rem; text-align: center; color: #666; margin-bottom: 2rem; }
    .genotype-card { padding: 1.5rem; border-radius: 10px; border: 2px solid #e0e0e0; margin-bottom: 1rem; background-color: #f9f9f9; }
    .genotype-title { font-size: 1.4rem; font-weight: bold; margin-bottom: 0.5rem; }
    .genotype-count { color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🏈 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Home", "Genotype Profiles", "School Detail", "Compare Schools", "Classify New School"]
)

# 6. PAGE CONTENT
if page == "Home":
    st.markdown('<div class="main-header">Fanbase Genotyping System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Power 4 College Athletics - 52 Schools</div>', unsafe_allow_html=True)
    
    st.markdown("### Select a Genotype to View Demographics")
    for name, data in genotypes.items():
        st.markdown(f"""
        <div class="genotype-card">
            <div class="genotype-title" style="color: {data['color']};">{name}</div>
            <div class="genotype-count">{data['count']} schools</div>
            <div>{data['description']}</div>
        </div>
        """, unsafe_allow_html=True)

elif page == "Genotype Profiles":
    st.header("Genotype Profiles")
    selected = st.selectbox("Select a genotype", list(genotypes.keys()))
    if selected:
        data = genotypes[selected]
        st.subheader(selected)
        st.write(data['description'])
        st.write("### Schools:")
        st.write(", ".join(sorted(data['schools'])))

elif page == "School Detail":
    st.header("School Detail")
    all_schools = sorted(genotype_lookup.keys())
    selected_school = st.selectbox("Select a school", all_schools)
    
    if selected_school:
        school_row = df[df["School"] == selected_school]
        if not school_row.empty:
            row = school_row.iloc[0]
            st.metric("Genotype", genotype_lookup[selected_school])
            col1, col2 = st.columns(2)
            col1.metric("Win % Since 2003", f"{row['Win_Pct_Since_2003']}%")
            col2.metric("Donations ($M)", f"${row['Donation_Revenue (Millions)']}M")

elif page == "Compare Schools":
    st.header("Compare Schools")
    all_schools = sorted(genotype_lookup.keys())
    selected_schools = st.multiselect("Select schools to compare", all_schools, max_selections=3)
    
    if selected_schools:
        compare_df = df[df["School"].isin(selected_schools)].copy()
        compare_df["Genotype"] = compare_df["School"].map(genotype_lookup)
        st.dataframe(compare_df.set_index("School"))

elif page == "Classify New School":
    st.header("Classify a New School")
    col1, col2 = st.columns(2)
    with col1:
        s_name = st.text_input("School Name")
        change = st.number_input("5-Year Attendance % Change", value=0.0)
        fb_in = st.number_input("FB Instagram Followers (K)", value=100)
        bb_in = st.number_input("BB Instagram Followers (K)", value=50)
    with col2:
        don = st.number_input("Donation Revenue ($M)", value=20.0)
        win = st.number_input("Win %", value=50.0)
        earn = st.number_input("Graduate Earnings ($K)", value=60)
        mbb_a = st.number_input("MBB Attendance %", value=70.0)
        cap = st.number_input("Stadium Capacity %", value=80.0)

    if st.button("Classify School", type="primary"):
        new_row = np.array([[change, fb_in, bb_in, don, win, earn, mbb_a, cap]])
        pred_cluster = kmeans.predict(new_row)[0]
        result = cluster_to_genotype.get(pred_cluster, "Unknown Pattern")
        st.success(f"**{s_name}** is classified as: **{result}**")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>Fanbase Genotyping Model | Rallyoop, Inc. | CMDA Capstone 2026</div>", unsafe_allow_html=True)
