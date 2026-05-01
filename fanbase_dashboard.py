import streamlit as st
import pandas as pd
import numpy as np

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

# Genotype data
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
        "schools": ["Arizona", "Arkansas", "Auburn", "Indiana", "Iowa State", 
                   "Kansas", "Kentucky", "Michigan State", "Nebraska", "North Carolina", 
                   "Purdue", "Rutgers", "Wisconsin"]
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
            if st.button("View →", key=name, use_container_width=True):
                st.session_state.selected_genotype = name
                st.session_state.page = 'genotype_detail'
                st.rerun()
    
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
    try:
        st.image("fanbase_cluster.png", use_column_width=True)
        st.caption("Left: PCA visualization showing 5 distinct genotypes | Right: Silhouette analysis confirming k=5 optimal cluster separation")
    except:
        st.info("📊 Clustering visualizations will appear here after you upload clustering_visualization.png to GitHub")
    
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
        
        # Placeholder for detailed profile
        st.info("📊 Detailed demographic profiles coming soon...")
        
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
                
                st.info("📊 School-specific metrics coming soon...")
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
    
    if school1 and school2:
        st.markdown("---")
        st.info("📊 Side-by-side comparison coming soon...")

elif page == "Classify New School":
    st.markdown('<div class="main-header">Classify a New School</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    ### Enter Metrics for a New Partner School
    
    Input the following 8 metrics to classify the school into one of the 5 genotypes:
    """)
    
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
        st.markdown("---")
        st.info("🔍 Classification tool coming soon...")
        st.markdown(f"**{school_name}** would be classified based on nearest-centroid approach")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Fanbase Genotyping Model | Rallyoop, Inc. | CMDA Capstone 2026</p>
</div>
""", unsafe_allow_html=True)
