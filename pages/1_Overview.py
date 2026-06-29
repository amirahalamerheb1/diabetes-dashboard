import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("diabetes.csv")

st.markdown('<p class="hero-title">Diabetes Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">A clinical intelligence tool for understanding diabetes burden, patient risk profiles, and predictive diagnostics.</p>', unsafe_allow_html=True)

# KPI Row
total = len(df)
diabetic = df['Outcome'].sum()
non_diabetic = total - diabetic
prevalence = round((diabetic / total) * 100, 1)
avg_glucose = round(df[df['Outcome'] == 1]['Glucose'].mean(), 1)
avg_bmi = round(df[df['Outcome'] == 1]['BMI'].mean(), 1)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total}</div>
        <div class="kpi-label">Total Patients</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{prevalence}%</div>
        <div class="kpi-label">Diabetes Prevalence</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_glucose}</div>
        <div class="kpi-label">Avg Glucose (Diabetic)</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_bmi}</div>
        <div class="kpi-label">Avg BMI (Diabetic)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown('<p class="section-title">Outcome Distribution</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Diabetic vs non-diabetic patients</p>', unsafe_allow_html=True)
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Non-Diabetic", "Diabetic"],
        values=[non_diabetic, diabetic],
        hole=0.6,
        marker_colors=["#4A90D9", "#E05C5C"],
        textinfo='percent+label',
        textfont_size=13
    )])
    fig_pie.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=False,
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.markdown('<p class="section-title">Glucose Distribution by Outcome</p>', unsafe_allow_html=True)
    st.markdown('<p class="section-sub">Glucose levels are the strongest single predictor of diabetes</p>', unsafe_allow_html=True)
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=df[df['Outcome'] == 0]['Glucose'],
        name='Non-Diabetic',
        marker_color='#4A90D9',
        opacity=0.7,
        nbinsx=30
    ))
    fig_hist.add_trace(go.Histogram(
        x=df[df['Outcome'] == 1]['Glucose'],
        name='Diabetic',
        marker_color='#E05C5C',
        opacity=0.7,
        nbinsx=30
    ))
    fig_hist.update_layout(
        barmode='overlay',
        xaxis_title='Glucose Level (mg/dL)',
        yaxis_title='Count',
        height=280,
        margin=dict(t=10, b=40, l=40, r=10),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#F0F2F5'),
        yaxis=dict(gridcolor='#F0F2F5')
    )
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")
st.markdown('<p class="section-title">About This Dataset</p>', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.info("**Source:** Pima Indian Diabetes Dataset (National Institute of Diabetes and Digestive and Kidney Diseases)")
with col_b:
    st.info("**Population:** Female patients of Pima Indian heritage, age ≥ 21")
with col_c:
    st.info("**Features:** 8 clinical variables including glucose, BMI, insulin, blood pressure, and more")

st.markdown("### 🌍 Global Context")
col1g, col2g, col3g = st.columns(3)
with col1g:
    st.metric("People with Diabetes Worldwide", "537 Million", "↑ 16% since 2019")
with col2g:
    st.metric("Annual Deaths Attributed", "6.7 Million", "Every 5 seconds")
with col3g:
    st.metric("Projected by 2045", "783 Million", "+46% increase")
