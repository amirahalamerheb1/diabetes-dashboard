import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown('<p class="section-title">Global Diabetes Burden</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Worldwide diabetes prevalence among adults (20–79 years). Source: IDF Diabetes Atlas 2021.</p>', unsafe_allow_html=True)

# IDF Diabetes Atlas 2021 - prevalence % among adults 20-79
global_data = {
    "Afghanistan": 8.8, "Albania": 9.8, "Algeria": 6.4, "Angola": 5.2,
    "Argentina": 6.5, "Armenia": 7.1, "Australia": 5.1, "Austria": 6.0,
    "Azerbaijan": 7.1, "Bahrain": 16.1, "Bangladesh": 8.4, "Belarus": 6.9,
    "Belgium": 5.8, "Bolivia": 7.0, "Brazil": 10.4, "Bulgaria": 8.8,
    "Cambodia": 4.5, "Cameroon": 6.7, "Canada": 7.4, "Chad": 5.2,
    "Chile": 8.5, "China": 10.6, "Colombia": 6.8, "Congo": 5.2,
    "Croatia": 7.5, "Cuba": 9.3, "Czech Republic": 7.8, "Denmark": 6.1,
    "Dominican Republic": 9.5, "Ecuador": 6.5, "Egypt": 17.2, "Ethiopia": 4.5,
    "Finland": 5.8, "France": 5.8, "Germany": 8.3, "Ghana": 5.0,
    "Greece": 8.6, "Guatemala": 8.8, "Honduras": 8.4, "Hungary": 8.6,
    "India": 9.6, "Indonesia": 6.0, "Iran": 9.6, "Iraq": 8.8,
    "Ireland": 4.8, "Israel": 8.0, "Italy": 7.3, "Jamaica": 12.0,
    "Japan": 5.7, "Jordan": 13.8, "Kazakhstan": 6.6, "Kenya": 3.5,
    "Kuwait": 16.4, "Lebanon": 8.8, "Libya": 9.3, "Malaysia": 16.8,
    "Mexico": 13.1, "Morocco": 8.6, "Mozambique": 4.0, "Myanmar": 5.5,
    "Nepal": 5.5, "Netherlands": 5.4, "New Zealand": 7.3, "Nigeria": 5.7,
    "Norway": 5.0, "Oman": 12.3, "Pakistan": 9.0, "Panama": 9.0,
    "Paraguay": 7.5, "Peru": 6.7, "Philippines": 7.1, "Poland": 8.3,
    "Portugal": 9.9, "Qatar": 15.4, "Romania": 9.0, "Russia": 6.2,
    "Saudi Arabia": 18.0, "Senegal": 3.3, "Serbia": 9.1, "Singapore": 8.8,
    "Slovakia": 8.0, "South Africa": 9.5, "South Korea": 7.0, "Spain": 7.2,
    "Sri Lanka": 7.8, "Sudan": 9.0, "Sweden": 5.2, "Switzerland": 5.9,
    "Syria": 8.4, "Tanzania": 5.1, "Thailand": 7.5, "Tunisia": 9.6,
    "Turkey": 12.1, "Uganda": 3.0, "Ukraine": 6.9, "United Arab Emirates": 15.4,
    "United Kingdom": 4.4, "United States": 10.7, "Uruguay": 6.2,
    "Uzbekistan": 6.4, "Venezuela": 7.7, "Vietnam": 5.7, "Yemen": 7.4,
    "Zambia": 3.5, "Zimbabwe": 4.7
}

df_map = pd.DataFrame(list(global_data.items()), columns=['Country', 'Prevalence'])

# Filter
st.markdown("### 🗺️ Prevalence Map")
threshold = st.slider("Highlight countries with prevalence above (%)", 0, 20, 0)
df_filtered = df_map[df_map['Prevalence'] >= threshold] if threshold > 0 else df_map

fig_map = px.choropleth(
    df_filtered,
    locations='Country',
    locationmode='country names',
    color='Prevalence',
    color_continuous_scale=[
        [0, '#D6E8FF'],
        [0.3, '#C4B5FD'],
        [0.6, '#C0392B'],
        [1, '#7B0000']
    ],
    range_color=[0, 20],
    labels={'Prevalence': 'Prevalence (%)'},
    title=''
)
fig_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor='#E0E5EC',
        showland=True,
        landcolor='#F8F9FB',
        showocean=True,
        oceancolor='#EEF2F8',
        projection_type='natural earth'
    ),
    height=480,
    margin=dict(t=10, b=10, l=0, r=0),
    paper_bgcolor='rgba(0,0,0,0)',
    coloraxis_colorbar=dict(
        title='Prevalence (%)',
        ticksuffix='%'
    )
)
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### Top 10 Highest Prevalence Countries")
    top10 = df_map.nlargest(10, 'Prevalence').reset_index(drop=True)
    top10.index += 1
    top10.columns = ['Country', 'Prevalence (%)']
    st.dataframe(top10, use_container_width=True)

with col2:
    st.markdown("### Regional Averages")
    regional = {
        'Middle East & N. Africa': df_map[df_map['Country'].isin(['Saudi Arabia','Egypt','UAE','Qatar','Kuwait','Jordan','Iran','Iraq','Lebanon','Syria','Tunisia','Morocco','Libya','Yemen'])]['Prevalence'].mean(),
        'North America': df_map[df_map['Country'].isin(['United States','Canada','Mexico'])]['Prevalence'].mean(),
        'Asia Pacific': df_map[df_map['Country'].isin(['China','India','Japan','South Korea','Malaysia','Philippines','Indonesia','Thailand','Vietnam','Bangladesh','Pakistan'])]['Prevalence'].mean(),
        'Europe': df_map[df_map['Country'].isin(['Germany','France','Italy','Spain','UK','Poland','Romania','Greece','Hungary','Bulgaria'])]['Prevalence'].mean(),
        'Sub-Saharan Africa': df_map[df_map['Country'].isin(['Nigeria','Kenya','Ethiopia','Tanzania','Uganda','Ghana','Cameroon','Angola','Mozambique','Zimbabwe'])]['Prevalence'].mean(),
        'Latin America': df_map[df_map['Country'].isin(['Brazil','Argentina','Colombia','Chile','Peru','Venezuela','Ecuador','Bolivia'])]['Prevalence'].mean(),
    }
    df_regional = pd.DataFrame(list(regional.items()), columns=['Region', 'Avg Prevalence (%)']).round(1).sort_values('Avg Prevalence (%)', ascending=False)
    st.dataframe(df_regional.reset_index(drop=True), use_container_width=True)

st.markdown("---")
st.info("📊 **Source:** International Diabetes Federation (IDF) Diabetes Atlas, 10th Edition, 2021. Prevalence shown among adults aged 20–79 years.")
