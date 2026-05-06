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

# Check if we need to navigate to a specific page
if 'nav_to_page' in st.session_state:
    page_index = st.session_state.nav_to_page
    del st.session_state.nav_to_page
else:
    page_index = 0

page = st.sidebar.radio(
    "Select Page",
    ["Home", "User Guide", "Genotype Profiles", "School Detail", "Compare Schools", "Classify New School"],
    index=page_index
)

# Scroll to top on page change
import streamlit.components.v1 as components
components.html(
    """
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
    </script>
    """,
    height=0,
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
            if st.button("View →", key=f"btn_{name}", use_container_width=True):
                st.session_state.nav_to_page = 1  # Genotype Profiles page
                st.session_state.nav_to_genotype = name
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
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    
    # Use the df that's already loaded at the top
    X = df[numeric_cols].values

    # Standardize the data (CRITICAL!)
    scaler_pca = StandardScaler()
    X_scaled_pca = scaler_pca.fit_transform(X)

    # PCA on scaled data
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled_pca)

    # Plot with school labels
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Define colors for each cluster
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    
    # Plot each cluster with different color
    for cluster_id in df['Cluster'].unique():
        cluster_mask = df['Cluster'] == cluster_id
        cluster_points = X_pca[cluster_mask]
        cluster_schools = df[cluster_mask]['School'].values
        
        # Scatter plot
        ax.scatter(cluster_points[:, 0], cluster_points[:, 1], 
                  c=colors[cluster_id], label=f'Cluster {cluster_id}', 
                  s=100, alpha=0.7, edgecolors='black', linewidth=1)
        
        # Add school labels
        for i, school in enumerate(cluster_schools):
            ax.annotate(school,
                       (cluster_points[i, 0], cluster_points[i, 1]),
                       fontsize=8,
                       alpha=0.8,
                       ha='center',
                       xytext=(0, 5),
                       textcoords='offset points')
    
    ax.set_xlabel('Principal Component 1', fontsize=12, fontweight='bold')
    ax.set_ylabel('Principal Component 2', fontsize=12, fontweight='bold')
    ax.set_title('K-Means Clustering (k=5) - PCA Visualization', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
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
                
                # Create a direct link
                st.markdown("---")
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("View Details", type="primary"):
                        # Set BOTH the page AND the genotype
                        st.session_state.nav_to_page = 1  # Index 1 = "Genotype Profiles"
                        st.session_state.nav_to_genotype = genotype_name
                        st.rerun()
                with col2:
                    st.markdown("*Click to see full genotype profile and schools*")
                break
elif page == "User Guide":
    st.markdown('<div class="main-header">User Guide</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">How to Navigate and Use This Dashboard</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ## 📖 Dashboard Overview
    
    This dashboard helps you explore college athletics fanbase types and evaluate prospective partnership schools. 
    Use the **sidebar navigation** to access six key pages, each designed for specific use cases.
    """)
    
    st.markdown("---")
    
    # Feature descriptions in expandable sections
    with st.expander("🏠 HOME - Quick Overview & School Search", expanded=True):
        st.markdown("""
        **What's on this page:**
        - Overview cards for all five genotypes
        - Clustering methodology explanation (PCA + silhouette analysis)
        - Quick school lookup tool
        
        **When to use:**
        - First-time visitors getting oriented
        - Quick genotype identification for a specific school
        - Understanding the clustering methodology
        
        **How to use:**
        1. Scroll through genotype cards to see all five types
        2. Click "View →" buttons to jump directly to detailed profiles
        3. Use the school search dropdown at the bottom
        4. Click "View Details" after searching to see that school's genotype profile
        """)
    
    with st.expander("📊 GENOTYPE PROFILES - Understanding Fanbase Archetypes"):
        st.markdown("""
        **What's on this page:**
        - Detailed behavioral descriptions for each genotype
        - Key demographic and engagement metrics
        - Geographic patterns and alumni composition
        - Complete school lists by genotype
        
        **When to use:**
        - Preparing for meetings with athletic directors
        - Understanding what defines each fanbase type
        - Identifying which schools share similar characteristics
        - Learning about common challenges for each genotype
        
        **How to use:**
        1. Select a genotype from the dropdown menu
        2. Read the "Fanbase Character" section to understand who these fans are
        3. Review the metrics (attendance, donations, social media, earnings)
        4. Note the key characteristics and geographic patterns
        5. Check the complete school list at the bottom
        
        **Example use case:** *"I'm meeting with Iowa State tomorrow. What genotype are they? What challenges do similar schools face?"*
        """)
    
    with st.expander("🎓 SCHOOL DETAIL - Deep-Dive Individual Analysis"):
        st.markdown("""
        **What's on this page:**
        - All 8 clustering metrics for individual schools
        - Interactive alumni geographic distribution maps
        - Genotype assignment for each school
        
        **When to use:**
        - Evaluating a specific partnership candidate
        - Understanding where a school's alumni actually live
        - Comparing a school's metrics to its genotype averages
        - Assessing geographic market fit
        
        **How to use:**
        1. Select any school from the dropdown
        2. Review the 8 clustering metrics in the two-column display
        3. Explore the interactive alumni map:
           - **Darker circles** = higher alumni concentration
           - Use the map's own dropdown to switch between schools
           - Zoom and pan to examine specific regions
        4. Note whether the school shows national scatter or regional concentration
        
        **Example use case:** *"Where do Virginia Tech alumni actually live? Are they concentrated in Virginia or scattered nationally?"*
        """)
    
    with st.expander("⚖️ COMPARE SCHOOLS - Side-by-Side Evaluation"):
        st.markdown("""
        **What's on this page:**
        - Side-by-side comparison of 2-3 schools
        - Comparison table with genotypes and key metrics
        - Individual bar charts for each metric
        
        **When to use:**
        - Choosing between multiple partnership candidates
        - Identifying key differences between similar schools
        - Understanding relative strengths and weaknesses
        
        **How to use:**
        1. Select 2-3 schools from the dropdowns
        2. Review the overview comparison table showing genotypes
        3. Scroll through individual metric bar charts
        4. Identify which school has stronger:
           - Attendance patterns
           - Social media reach
           - Donation capacity
           - Graduate earnings
           - Recent growth trends
        
        **Example use case:** *"We're deciding between Iowa State and Kansas State. How do their fanbases compare?"*
        """)
    
    with st.expander("🔍 CLASSIFY NEW SCHOOL - Predict Genotype for Any School"):
        st.markdown("""
        **What's on this page:**
        - Input form for 8 metrics
        - Nearest-centroid classification algorithm
        - Distance calculations to all five genotypes
        - Expected fanbase characteristics
        
        **When to use:**
        - Evaluating schools not in the original 52-school dataset
        - Assessing private schools (Miami, Stanford, USC, etc.)
        - Hypothetical "what-if" scenarios (e.g., if a school's attendance improves)
        
        **How to use:**
        1. Enter the school name
        2. Input all 8 required metrics:
           - **5-Year Attendance % Change** (e.g., +5.0 or -10.0)
           - **FB Instagram Followers** (in thousands, e.g., 350)
           - **BB Instagram Followers** (in thousands, e.g., 120)
           - **Donation Revenue** (in millions, e.g., 42.5)
           - **Win % Since 2003** (e.g., 58.5)
           - **Graduate Earnings** (in thousands, e.g., 72)
           - **Men's Basketball Attendance %** (e.g., 75.0)
           - **Football Stadium Capacity %** (22-25 average, e.g., 92.0)
        3. Click "Classify School"
        4. Review predicted genotype and distance scores
        
        **Understanding distance scores:**
        - **Lower distance = stronger match** to that genotype
        - Schools with similar distances to multiple genotypes exhibit mixed characteristics
        - Distance > 50 suggests the school doesn't fit existing genotypes well
        
        **Example use case:** *"We're considering Stanford (private school, not in dataset). Based on their metrics, which genotype do they resemble?"*
        """)
    
    st.markdown("---")
    
    st.markdown("## 💡 Best Practices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Recommended Workflow
        
        **For general exploration:**
        1. Start at **Home** to see all genotypes
        2. Explore **Genotype Profiles** to understand archetypes
        3. Dive into **School Detail** for specific schools
        
        **For partnership decisions:**
        1. Identify candidates in **Home** or **Genotype Profiles**
        2. Use **Compare Schools** for side-by-side evaluation
        3. Check **School Detail** for geographic market fit
        4. Use **Classify New School** for schools not in dataset
        """)
    
    with col2:
        st.markdown("""
        ### Tips for Effective Use
        
        ✅ **Save Classification results** - Screenshot distance scores for later reference
        
        ✅ **Use geomaps for market fit** - Geographic patterns reveal whether fanbases match your product's regional needs
        
        ✅ **Compare within genotypes** - Schools in the same genotype may still have important differences
        
        ✅ **Consider trends** - Look at 5-year attendance change to identify improving vs. declining fanbases
        """)
    
    st.markdown("---")
    
    st.markdown("## ❓ Frequently Asked Questions")
    
    with st.expander("Where does the data come from?"):
        st.markdown("""
        All metrics use publicly available data sources:
        - **Attendance data:** NCAA official reports
        - **Donation revenue:** USA Today NCAA Finances Database
        - **Graduate earnings:** U.S. Department of Education College Scorecard
        - **Social media followers:** Verified Instagram accounts (as of 2025)
        - **Win percentage & stadium capacity:** Winsipedia
        
        **Time period:** All metrics represent 2022-2025 averages to smooth year-to-year volatility.
        """)
    
    with st.expander("Why are some schools missing?"):
        st.markdown("""
        We excluded five schools due to missing donation revenue data:
        - Miami
        - Pittsburgh
        - Stanford
        - Syracuse
        - USC
        
        These private institutions do not publicly report athletic department finances. However, you can use the **Classify New School** tool to estimate their genotype if you can obtain their metrics from other sources.
        """)
    
    with st.expander("How accurate is the classification tool?"):
        st.markdown("""
        The nearest-centroid classifier achieves **100% accuracy** when applied to the 52 schools in the training dataset, meaning it perfectly reproduces the k-means cluster assignments.
        
        For new schools not in the dataset, accuracy depends on:
        - How similar the school is to existing genotypes
        - Data quality and recency
        - Whether the school represents a genuinely new fanbase type not captured by our five genotypes
        
        **Interpreting confidence:**
        - Distance < 20: Strong match
        - Distance 20-40: Moderate match
        - Distance > 40: Weak match or mixed characteristics
        """)
    
    with st.expander("Can schools transition between genotypes?"):
        st.markdown("""
        Yes! Fanbases evolve as programs improve or decline. Examples:
        
        - **Illinois** likely transitioned from Disengaged toward Selective Affluent as their football program improved (2019-2024)
        - **Colorado** may be transitioning with recent coaching changes and attendance surges
        - **Nebraska** has maintained Established Traditionalist status despite declining performance, showing loyalty persists
        
        The model reflects a 2022-2025 snapshot. Periodic re-clustering is recommended to capture evolving fanbases.
        """)
    
    with st.expander("How should I use this for partnership decisions?"):
        st.markdown("""
        This dashboard provides **systematic fanbase evaluation**, not definitive partnership recommendations. Use it to:
        
        ✅ **Identify schools with characteristics matching your product** (e.g., affluent alumni, social media reach, donation capacity)
        
        ✅ **Understand what to expect** from partnerships with different genotypes
        
        ✅ **Tailor your pitch** by referencing similar schools and genotype-specific challenges
        
        ✅ **Prioritize outreach** based on data-driven fanbase profiles rather than intuition alone
        
        ❌ Don't use genotypes as the ONLY factor - program leadership, existing partnerships, and strategic fit matter too
        """)
    
    st.markdown("---")
    
    st.markdown("## 📞 Support & Feedback")
    
    st.markdown("""
    **Questions or issues?** Contact the development team or visit our GitHub repository:
    
    🔗 **GitHub:** [Insert your repository URL]
    
    📧 **Contact:** [Insert your email or contact info]
    
    💬 **Feedback welcome!** We're continuously improving this tool based on user input.
    """)
elif page == "Genotype Profiles":
    st.markdown('<div class="main-header">Genotype Profiles</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Check if we navigated here from school lookup button
    if 'nav_to_genotype' in st.session_state:
        default_genotype = st.session_state.nav_to_genotype
        default_index = list(genotypes.keys()).index(default_genotype)
        del st.session_state.nav_to_genotype  # Clear the navigation flag
    else:
        default_index = 0
    
    # Genotype selector (pre-selects if coming from button)
    selected = st.selectbox(
        "Select a genotype to view detailed profile",
        list(genotypes.keys()),
        index=default_index
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
        if school_name:
            # Create new data point
            new_data = pd.DataFrame([[change_5yr, fb_insta, bb_insta, donations, win_pct, earnings, mbb_att, capacity]], 
                                   columns=numeric_cols)
            
            # CRITICAL: Scale the new data using the same scaler
            new_data_scaled = scaler.transform(new_data)
            
            # Predict cluster
            cluster = kmeans.predict(new_data_scaled)[0]
            predicted_genotype = cluster_to_genotype.get(cluster, "Unknown")
            
            st.success(f"🏫 **{school_name}** is classified as: **{predicted_genotype}**")
            
            # Optional: Show distances to each cluster
            st.markdown("---")
            st.markdown("### Distance to Each Genotype")
            st.markdown("*(Lower distance = better match)*")
            
            distances = np.linalg.norm(kmeans.cluster_centers_ - new_data_scaled, axis=1)
            
            for i, (genotype, dist) in enumerate(zip(cluster_to_genotype.values(), distances)):
                marker = " ← **BEST MATCH**" if i == cluster else ""
                st.markdown(f"- **{genotype}**: {dist:.2f}{marker}")
        else:
            st.warning("Please enter a school name")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Fanbase Genotyping Model | Rallyoop, Inc. | CMDA Capstone 2026</p>
</div>
""", unsafe_allow_html=True)
