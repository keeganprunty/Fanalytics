# Fanbase Genotyping Dashboard

An interactive Streamlit dashboard that classifies Power 4 college athletics fanbases into five distinct genotypes based on attendance patterns, social media engagement, financial support, and demographic characteristics.

**Project Partner:** Rallyoop, Inc. (Stealth-Mode Startup)  
**Academic Institution:** Virginia Tech CMDA Capstone 2026  
**Team:** Fanalytics

🔗 **[View Live Dashboard](https://your-app-url.streamlit.app)** *(Replace with your actual Streamlit URL)*

---

## 📊 Overview

This dashboard analyzes **52 Power 4 universities** using 8 clustering metrics to identify natural fanbase groupings. The system helps athletic departments and sports tech companies understand fanbase DNA for targeted engagement strategies.

### Five Genotypes Identified:

1. **National Brand Fanatics** (11 schools) - Elite programs with massive reach and championship culture
2. **Regional Community Loyalists** (22 schools) - College towns with unconditional local support
3. **Established Traditionalists** (13 schools) - Multi-sport passionate fans across football and basketball
4. **Disengaged Fans** (2 schools) - High-earning alumni with declining attendance
5. **Selective Affluents** (4 schools) - Highest earnings with recent attendance surge

---

## 🎯 Features

### 1. **Home Page**
- Overview of all five genotypes
- K-means clustering methodology explanation
- PCA and silhouette analysis visualizations
- Quick school lookup

### 2. **Genotype Profiles**
- Detailed behavioral descriptions for each fanbase type
- Key demographic and engagement metrics
- Geographic patterns and alumni composition
- Complete school lists by genotype

### 3. **School Detail**
- Individual school metrics across all 8 clustering dimensions
- Interactive alumni geographic distribution maps
- Genotype assignment for each school

### 4. **Compare Schools**
- Side-by-side comparison of 2-3 schools
- Automated identification of key differences
- Full metric comparison tables

### 5. **Classify New School**
- Nearest-centroid classification tool
- Input 8 metrics for any Power 4 school
- Distance calculations to all genotypes
- Expected fanbase characteristics based on classification

---

## 📁 Repository Structure

```
fanbase-genotyping-dashboard/
├── fanbase_dashboard.py              # Main Streamlit application
├── power4_attributes_fin.csv         # Dataset with all school metrics
├── school_city_radius_map.html       # Interactive alumni location maps
├── clustering_visualization.png      # PCA + Silhouette analysis charts
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## 🚀 Quick Start

### View the Live Dashboard

Visit **[your-dashboard-url.streamlit.app](https://your-app-url.streamlit.app)** to interact with the dashboard immediately.

### Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/fanbase-genotyping-dashboard.git
   cd fanbase-genotyping-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run fanbase_dashboard.py
   ```

4. **Open in browser:**
   - The dashboard will automatically open at `http://localhost:8501`

---

## 📊 Data & Methodology

### Clustering Metrics (8 dimensions)

**Attendance Patterns:**
- Football attendance percentage (4-year average, 2022-2025)
- 5-year attendance change percentage
- Men's basketball attendance percentage

**Social Media Engagement:**
- Football Instagram followers (thousands)
- Basketball Instagram followers (thousands)

**Financial Support:**
- Annual athletic donation revenue (millions)

**Demographics:**
- Graduate median earnings (thousands)

**Performance Context:**
- Win percentage since 2003
- Stadium capacity percentage

### Data Sources

All metrics derived from publicly available sources:
- **Attendance**: NCAA official reports, university athletics websites
- **Social Media**: Instagram verified accounts (as of 2025)
- **Financial**: USA Today NCAA Finances Database, university reports
- **Demographics**: College Scorecard (Department of Education), Linkedin
- **Performance**: Winsipedia, Sports-Reference

### Methodology

- **Algorithm**: K-means clustering (k=5)
- **Validation**: Silhouette analysis (optimal separation at k=5)
- **Dimensionality Reduction**: PCA for visualization
- **Classification**: Nearest-centroid approach for new schools

**52 Public schools analyzed** (1 excluded due to missing donation data: Pitt)

---

## 🎓 Use Cases

### For Athletic Departments
- Understand your fanbase DNA relative to peer institutions
- Benchmark engagement metrics against similar genotypes
- Identify growth opportunities based on fanbase transitions

### For Rallyoop
- Assisting Rallyoop in partnering with schools using these public insights to gain more advanced private institutional data
- Customize go-to-market strategies by genotype
- Prioritize partnership opportunities based on fanbase characteristics

### For Researchers
- Explore patterns in college sports fan behavior
- Analyze demographic and geographic trends in alumni engagement
- Study the relationship between performance and fan loyalty across different contexts

---

## 🛠️ Technical Stack

- **Frontend**: Streamlit 1.31.0
- **Data Processing**: Pandas 2.2.0, NumPy 1.26.3
- **Mapping**: Folium (embedded HTML)
- **Deployment**: Streamlit Cloud
- **Version Control**: GitHub

---

## 📝 Project Background

This dashboard was developed as part of a capstone project for **Rallyoop, Inc.**, a stealth-mode startup revolutionizing fan monetization in college athletics. The project aimed to create a scalable fanbase genotyping model using publicly available proxy metrics, enabling data-driven engagement strategies without requiring individual fan-level data.

**Team Fanalytics** built this system to provide athletic departments and sports technology companies with actionable insights into fanbase composition and behavior patterns.

---

## 👥 Team

**Team Fanalytics** - Virginia Tech CMDA 2026

*Project Sponsor:* Chris Brown, Anothony Beverina, Rallyoop, Inc.

---

## 🤝 Acknowledgments

- **Rallyoop, Inc.** for project sponsorship and industry guidance
- **Virginia Tech CMDA Program** for academic support
- **Public data providers** (NCAA, USA Today, Department of Education, Winsipedia)

---

## 🔄 Updates

### Version 1.0 (May 2026)
- Initial release with 52 Power 4 schools
- Five genotypes identified via k-means clustering
- Interactive comparison and classification tools
- Alumni geographic distribution maps
---
