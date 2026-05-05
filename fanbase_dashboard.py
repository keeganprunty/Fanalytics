import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

@st.cache_data
def load_data():
    return pd.read_csv("power4_attributes(Sheet1).csv")

df = load_data()

bad_schools = ["Miami", "Pitt", "Stanford", "Syracuse", "USC"]
df = df[~df["School"].isin(bad_schools)]

# --- FIXED: Moved this block up so genotype_lookup exists before it is used ---
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

genotype_lookup = {}
for genotype_name, data in genotypes.items():
    for school in data["schools"]:
        genotype_lookup[school] = genotype_name
# ----------------------------------------------------------------------------

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

# WITH THIS:
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[numeric_cols])

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X_scaled)

# Map clusters to genotypes using majority vote
cluster_to_genotype = {}

for cluster_id in df["Cluster"].unique():
    schools_in_cluster = df[df["Cluster"] == cluster_id]["School"]
    mapped = schools_in_cluster.map(genotype_lookup)

    if not mapped.dropna().empty:
        cluster_to_genotype[cluster_id] = mapped.mode()[0]

# Page configuration
st.set_page_config(
    page_title="Fanbase Genotyping System",
    page_icon="🏈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .genotype-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .genotype-card:hover {
        border-color: #1f77b4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background-color: #fff;
    }
    .genotype-title {
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .genotype-count {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .genotype-description {
        color: #444;
        font-size: 1rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_genotype' not in st.session_state:
    st.session_state.selected_genotype = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Sidebar navigation
st.sidebar.title("🏈 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Home", "Genotype Profiles", "School Detail", "Compare Schools", "Classify New School"],
    index=0
)

# Main content
if page == "Home":
    # Header
    st.markdown('<div class="main-header">Fanbase Genotyping System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Power 4 College Athletics - 52 Schools</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Introduction
    st.markdown("""
    ### Select a Genotype to View Demographics
    
    This system categorizes Power 4 college athletics fanbases into five distinct genotypes 
    based on attendance patterns, social media reach, financial support, and demographic characteristics.
    """)
    
    st.markdown("---")
    
    # Genotype cards
    for name, data in genotypes.items():
        col1, col2 = st.columns([5, 1])
        
        with col1:
            st.markdown(f"""
            <div class="genotype-card">
                <div class="genotype-title" style="color: {data['color']};">
                    {name}
                </div>
                <div class="genotype-count">
                    {data['count']} schools
                </div>
                <div class="genotype-description">
                    {data['description']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<a href='#' style='text-decoration:none; color: {data['color']};'>→ Use sidebar</a>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clustering methodology section
    st.markdown("### How We Identified These Genotypes")
    
    st.markdown("""
    We used **k-means clustering** on 8 metrics to identify 5 natural groupings of fanbases:
    - Attendance patterns (5-year change, MBB attendance %)
    - Social media reach (FB & BB Instagram followers)
    - Financial support (donation revenue)
    - Demographics (graduate earnings)
    - Performance (win % since 2003, stadium capacity %)
    """)
    
    # Display clustering visualization
# Display clustering visualization
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

    # Use the df that's already loaded at the top
    X = df[numeric_cols].values

    # Standardize the data (CRITICAL!)
    scaler_pca = StandardScaler()
    X_scaled_pca = scaler_pca.fit_transform(X)

    # PCA on scaled data
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled_pca)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=df['Cluster'], cmap='viridis', s=100)
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_title('K-Means Clustering (k=5) - PCA Visualization')
    plt.colorbar(scatter, label='Cluster')

    st.pyplot(fig)
    
    st.markdown("""
    **Why k=5?** Silhouette analysis revealed that 5 clusters maximize separation between groups 
    while maintaining cohesion within each genotype. The PCA visualization confirms distinct, 
    non-overlapping fanbase archetypes.
    """)
    
    st.markdown("---")
    
    # Search by school
    st.markdown("### Or Search by School")
    
    all_schools = []
    for data in genotypes.values():
        all_schools.extend(data['schools'])
    
    selected_school = st.selectbox(
        "Select a school to see its genotype",
        [""] + sorted(all_schools)
    )
    
    if selected_school:
        # Find which genotype this school belongs to
        for genotype_name, data in genotypes.items():
            if selected_school in data['schools']:
                st.success(f"**{selected_school}** belongs to: **{genotype_name}**")
                if st.button("View Genotype Profile"):
                    st.session_state.selected_genotype = genotype_name
                    st.session_state.page = 'genotype_detail'
                    st.rerun()
                break

elif page == "Genotype Profiles":
    st.markdown('<div class="main-header">Genotype Profiles</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Genotype selector
    selected = st.selectbox(
        "Select a genotype to view detailed profile",
        list(genotypes.keys())
    )
    
    if selected:
        data = genotypes[selected]
        
        st.markdown(f"## {selected}")
        st.markdown(f"**{data['count']} schools** | {data['description']}")
        
        st.markdown("---")
        
        # DETAILED PROFILES
        if selected == "Established Traditionalists":
            st.markdown("### Fanbase Character")
            st.markdown("""
These are traditional college sports families who care deeply about BOTH football and basketball—multi-generational 
supporters including parents who bring children to games, alumni who return for homecoming, and local community members 
who've supported the program for decades. Alumni work in stable middle-class professions (education, healthcare, skilled 
trades), stay regionally connected (60-70% in-state), and scatter across regional hubs rather than coastal metros. The 
fanbase is rooted in tradition and school pride, not bandwagon championship-chasing. Think Nebraska grads in Omaha and 
Lincoln, Kansas grads in Kansas City, Auburn grads across Alabama.
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Alumni Base", "237k avg")
                st.metric("Graduate Earnings", "$73k median")
            with col2:
                st.metric("FB Attendance", "94.8%")
                st.metric("MBB Attendance", "96.6%")
            with col3:
                st.metric("Social Media", "509k total")
                st.metric("Donations", "$31.7M avg")
            
            st.markdown("### Key Characteristics")
            st.markdown("- **UNCONDITIONAL LOYALTY**: High attendance despite moderate winning")
            st.markdown("- **MULTI-SPORT PASSIONATE**: Strong basketball culture alongside football")
            st.markdown("- **Economic class**: Middle to upper-middle ($73k median)")
            st.markdown("- **Geographic pattern**: Regional concentration (60-70% in-state)")
            st.markdown("- **Fanbase composition**: Alumni 40%, Local 30%, Regional 30%")
        
        elif selected == "National Brand Fanatics":
            st.markdown("### Fanbase Character")
            st.markdown("""
These fanbases combine wealthy, passionate alumni (higher-earning professions in business, finance, healthcare leadership) 
with massive numbers of national "Subway Alumni"—fans who never attended but adopted the team due to decades of televised 
success. Alumni scatter everywhere—significant populations in every major U.S. metro from New York to Los Angeles—but the 
national Subway Alumni fanbase extends reach even further (you'll find Alabama fans in Seattle who've never been to Tuscaloosa, 
Ohio State fans in Miami who never attended OSU). The fanbase expects championships, not just competitive seasons, and has 
the donation capacity to fund elite programs. This is truly national brand reach.
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Alumni Base", "310k avg")
                st.metric("Graduate Earnings", "$75k median")
            with col2:
                st.metric("FB Attendance", "101.1%")
                st.metric("Win % (2003)", "71.8%")
            with col3:
                st.metric("Social Media", "1,159k total")
                st.metric("Donations", "$68.6M avg")
            
            st.markdown("### Key Characteristics")
            st.markdown("- **CHAMPIONSHIP EXPECTATIONS**: Elite performance meets elite support")
            st.markdown("- **NATIONAL BRAND**: Massive reach beyond alumni (Subway Alumni effect)")
            st.markdown("- **Economic class**: Middle to upper-middle ($75k median)")
            st.markdown("- **Geographic pattern**: National scatter (40-50% in-state)")
            st.markdown("- **Fanbase composition**: Alumni 25%, Local 35%, National 40%")
        
        elif selected == "Regional Community Loyalists":
            st.markdown("### Fanbase Character")
            st.markdown("""
This fanbase is defined by LOCAL COMMUNITY SUPPORT beyond just alumni—college towns where the university IS the town's identity. 
Local business owners, factory workers, teachers, healthcare professionals, and families who never attended the school treat 
game day as the primary social and cultural event. Alumni work in practical middle-class fields (engineering, education, 
agriculture, skilled trades), stay close to home (70-80% in-state, clustering in state capitals and 1-2 regional hubs), and 
maintain deep ties to the university rather than scattering to coastal cities. Loyalty is unconditional—attendance stays 
strong regardless of record because this is about COMMUNITY IDENTITY, not performance.
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Alumni Base", "241k avg")
                st.metric("Graduate Earnings", "$70k median")
            with col2:
                st.metric("FB Attendance", "96.9%")
                st.metric("MBB Attendance", "66.3%")
            with col3:
                st.metric("Social Media", "379k total")
                st.metric("Donations", "$30.9M avg")
            
            st.markdown("### Key Characteristics")
            st.markdown("- **UNCONDITIONAL LOYALTY**: High attendance despite moderate winning")
            st.markdown("- **COMMUNITY IDENTITY**: Game day is the region's primary cultural event")
            st.markdown("- **Economic class**: Working to middle ($70k median)")
            st.markdown("- **Geographic pattern**: Regional concentration (70-80% in-state)")
            st.markdown("- **Fanbase composition**: Alumni 35%, Local 40%, Regional 25%")
        
        elif selected == "Disengaged Fans":
            st.markdown("### Fanbase Character")
            st.markdown("""
Highly educated, affluent alumni (median earnings $87k+, highest economic class) working in tech, entertainment, finance, 
and professional services, concentrated in West Coast metros (LA, San Francisco Bay, San Diego, Seattle) with scatter to 
New York and Chicago. They're selective about engagement—attending when convenient or when the team performs well, but not 
making football a central identity. The surrounding urban environment offers competing entertainment (pro sports, concerts, 
beaches), so college football doesn't dominate cultural attention like it does in college towns or the South. This fanbase 
values academic prestige over athletic dominance and sees sports as entertainment, not community ritual.
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Alumni Base", "533k avg")
                st.metric("Graduate Earnings", "$87k median")
            with col2:
                st.metric("FB Attendance", "48.8%")
                st.metric("5-Year Change", "-14.2%")
            with col3:
                st.metric("Social Media", "311k total")
                st.metric("Donations", "$15.4M avg")
            
            st.markdown("### Key Characteristics")
            st.markdown("- **SELECTIVE ENGAGEMENT**: Attend when convenient/successful")
            st.markdown("- **DECLINING ATTENDANCE**: -14% over 5 years")
            st.markdown("- **Economic class**: Upper-middle to affluent ($87k median - highest)")
            st.markdown("- **Geographic pattern**: National scatter (West Coast + major metros)")
            st.markdown("- **Fanbase composition**: Alumni 50%, Local 20%, Scattered 30%")
        
        elif selected == "Selective Affluents":
            st.markdown("### Fanbase Character")
            st.markdown("""
Academically-focused alumni (median earnings $94k—highest of all genotypes) working in STEM, finance, consulting, and 
professional services, scattering to major professional hubs (DC, New York, Chicago, San Francisco, Atlanta) for career 
opportunities. Recent program improvement has driven an attendance surge (+21% over 5 years), but this fanbase has 
historically been smaller and less passionate than peers—urban location means competing entertainment reduces football's 
cultural centrality. These are educated professionals who attend when the team is winning or for social/networking purposes, 
exhibiting selective engagement rather than unconditional loyalty. Geographic dispersal reflects professional mobility 
rather than regional loyalty.
            """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Alumni Base", "287k avg")
                st.metric("Graduate Earnings", "$94k median")
            with col2:
                st.metric("FB Attendance", "86.9%")
                st.metric("5-Year Change", "+20.7%")
            with col3:
                st.metric("Social Media", "237k total")
                st.metric("Donations", "$30.3M avg")
            
            st.markdown("### Key Characteristics")
            st.markdown("- **PERFORMANCE-SENSITIVE**: Attendance tracks recent success closely")
            st.markdown("- **RECENT SURGE**: +21% attendance growth over 5 years")
            st.markdown("- **Economic class**: Upper-middle to affluent ($94k median - HIGHEST)")
            st.markdown("- **Geographic pattern**: National scatter (professional hubs)")
            st.markdown("- **Fanbase composition**: Alumni 50%, Local 20%, Scattered 30%")
        
        st.markdown("---")
        st.markdown("### Schools in this Genotype")
        
        # Display schools in columns
        cols = st.columns(3)
        for i, school in enumerate(sorted(data['schools'])):
            with cols[i % 3]:
                st.markdown(f"• {school}")

elif page == "School Detail":
    st.markdown('<div class="main-header">School Detail</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    all_schools = []
    for data in genotypes.values():
        all_schools.extend(data['schools'])
    
    selected_school = st.selectbox(
        "Select a school",
        sorted(all_schools)
    )
    
    if selected_school:
        # Find genotype
        for genotype_name, data in genotypes.items():
            if selected_school in data['schools']:
                st.markdown(f"## {selected_school}")
                st.markdown(f"**Genotype:** {genotype_name}")
                st.markdown("---")
                
                # ALUMNI MAP
                st.markdown("### Where Alumni Live")
                st.markdown("Interactive map showing alumni concentration by city. Darker circles = higher concentration. Use the dropdown in the map to view different schools.")
                
                try:
                    import streamlit.components.v1 as components
                    with open("school_city_radius_map.html", "r", encoding="utf-8") as f:
                        html_content = f.read()
                    
                    components.html(html_content, height=600, scrolling=True)
                except:
                    st.info("📍 Interactive alumni map will appear here after uploading school_city_radius_map.html to GitHub")
                
                st.markdown("---")
                st.markdown("### Additional School Metrics")

                school_row = df[df["School"] == selected_school]

                if not school_row.empty:
                    row = school_row.iloc[0]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("5-Year Attendance Change", f"{row['5_Year_Pct_Change']}%")
                        st.metric("FB Instagram (K)", row["Instagram_Followers_FB (Thousands)"])
                        st.metric("BB Instagram (K)", row["Instagram_Followers_BB (Thousands)"])
                        st.metric("Donations ($M)", row["Donation_Revenue (Millions)"])
                        st.metric("Living Alumni (K)", row["Alumni_amount"])

                    with col2:
                        st.metric("Win % Since 2003", f"{row['Win_Pct_Since_2003']}%")
                        st.metric("Graduate Earnings ($K)", row["Graduate_Earnings(Thousands)"])
                        st.metric("MBB Attendance %", f"{row['Attendence_Pct_MBB']}%")
                        st.metric("Stadium Capacity %", f"{row['Football_Stadium_Capacity(22-25)']}%")
                else:
                    st.error("School not found in dataset")
                
                break

elif page == "Compare Schools":
    st.markdown('<div class="main-header">Compare Schools</div>', unsafe_allow_html=True)
    st.markdown("---")

    all_schools = []
    for data in genotypes.values():
        all_schools.extend(data['schools'])

    col1, col2, col3 = st.columns(3)

    with col1:
        school1 = st.selectbox("School 1", [""] + sorted(all_schools), key="compare1")

    with col2:
        school2 = st.selectbox("School 2", [""] + sorted(all_schools), key="compare2")

    with col3:
        school3 = st.selectbox("School 3 (optional)", [""] + sorted(all_schools), key="compare3")

    selected = [s for s in [school1, school2, school3] if s]

    compare_df = df[df["School"].isin(selected)].copy()

    if not compare_df.empty:
        compare_df["Genotype"] = compare_df["School"].map(genotype_lookup)

        st.subheader("School Comparison Overview")
        display_cols = ["School", "Genotype", "5_Year_Pct_Change", "Instagram_Followers_FB (Thousands)", "Donation_Revenue (Millions)", "Win_Pct_Since_2003", "Graduate_Earnings(Thousands)"]
        st.dataframe(compare_df[display_cols].set_index("School"))

        st.subheader("Attribute Comparison")
        pretty_names = {
            "5_Year_Pct_Change": "5-Year Change (%)",
            "Instagram_Followers_FB (Thousands)": "FB Instagram (K)",
            "Instagram_Followers_BB (Thousands)": "BB Instagram (K)",
            "Donation_Revenue (Millions)": "Donations ($M)",
            "Win_Pct_Since_2003": "Win %",
            "Graduate_Earnings(Thousands)": "Earnings ($K)",
            "Attendence_Pct_MBB": "MBB Attendance %",
            "Football_Stadium_Capacity(22-25)": "Stadium Capacity %"
        }

        for col in numeric_cols:
            chart_df = compare_df.set_index("School")[[col]]
            chart_df = chart_df.rename(columns={col: pretty_names[col]})
            st.markdown(f"#### {pretty_names[col]}")
            st.bar_chart(chart_df)

elif page == "Classify New School":
    st.markdown('<div class="main-header">Classify a New School</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### Enter Metrics for a New Partner School")
    
    col1, col2 = st.columns(2)
    with col1:
        school_name = st.text_input("School Name", "")
        change_5yr = st.number_input("5-Year Attendance % Change", -50.0, 50.0, 0.0, 0.1)
        fb_insta = st.number_input("FB Instagram Followers (thousands)", 0, 2000, 300)
        bb_insta = st.number_input("BB Instagram Followers (thousands)", 0, 500, 100)
        donations = st.number_input("Donation Revenue ($ millions)", 0, 150, 35)
    
    with col2:
        win_pct = st.number_input("Win % Since 2003", 0.0, 100.0, 55.0, 0.1)
        earnings = st.number_input("Graduate Earnings ($ thousands)", 40, 150, 70)
        mbb_att = st.number_input("Men's Basketball Attendance %", 0.0, 100.0, 65.0, 0.1)
        capacity = st.number_input("Football Stadium Capacity %", 0.0, 110.0, 85.0, 0.1)
    
    if st.button("Classify School", type="primary"):
        new_data = pd.DataFrame([[change_5yr, fb_insta, bb_insta, donations, win_pct, earnings, mbb_att, capacity]], columns=numeric_cols)
        cluster = kmeans.predict(new_data)[0]
        predicted_genotype = cluster_to_genotype.get(cluster, "Unknown")
        st.success(f"🏫 **{school_name}** is classified as: **{predicted_genotype}**")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Fanbase Genotyping Model | Rallyoop, Inc. | CMDA Capstone 2026</p>
</div>
""", unsafe_allow_html=True)
