import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("diabetes.csv")
for col in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
    df[col] = df[col].replace(0, df[col].median())

st.markdown('<p class="section-title">Demographics & Risk Profiles</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Exploring how age, pregnancies, and lifestyle factors relate to diabetes risk.</p>', unsafe_allow_html=True)

# Age groups
bins = [20, 30, 40, 50, 60, 70, 82]
labels = ['21–30', '31–40', '41–50', '51–60', '61–70', '71+']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)

age_stats = df.groupby('AgeGroup', observed=True).agg(
    Total=('Outcome', 'count'),
    Diabetic=('Outcome', 'sum')
).reset_index()
age_stats['Rate'] = round((age_stats['Diabetic'] / age_stats['Total']) * 100, 1)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Diabetes Rate by Age Group**")
    fig_age = go.Figure()
    fig_age.add_bar(
        x=age_stats['AgeGroup'].astype(str),
        y=age_stats['Rate'],
        marker_color='#E05C5C',
        text=age_stats['Rate'].astype(str) + '%',
        textposition='outside'
    )
    fig_age.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Diabetes Rate (%)',
        height=320,
        margin=dict(t=20, b=40, l=40, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#F0F2F5', range=[0, 80]),
        xaxis=dict(gridcolor='#F0F2F5')
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    st.markdown("**Patient Count by Age Group**")
    fig_count = go.Figure()
    fig_count.add_bar(
        x=age_stats['AgeGroup'].astype(str),
        y=age_stats['Total'] - age_stats['Diabetic'],
        name='Non-Diabetic',
        marker_color='#4A90D9'
    )
    fig_count.add_bar(
        x=age_stats['AgeGroup'].astype(str),
        y=age_stats['Diabetic'],
        name='Diabetic',
        marker_color='#E05C5C'
    )
    fig_count.update_layout(
        barmode='stack',
        xaxis_title='Age Group',
        yaxis_title='Number of Patients',
        height=320,
        margin=dict(t=20, b=40, l=40, r=10),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#F0F2F5'),
        xaxis=dict(gridcolor='#F0F2F5')
    )
    st.plotly_chart(fig_count, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Pregnancies vs Diabetes Rate**")
    preg_stats = df.groupby('Pregnancies').agg(
        Total=('Outcome', 'count'),
        Diabetic=('Outcome', 'sum')
    ).reset_index()
    preg_stats['Rate'] = round((preg_stats['Diabetic'] / preg_stats['Total']) * 100, 1)
    preg_stats = preg_stats[preg_stats['Total'] >= 5]

    fig_preg = go.Figure()
    fig_preg.add_scatter(
        x=preg_stats['Pregnancies'],
        y=preg_stats['Rate'],
        mode='lines+markers',
        line=dict(color='#E05C5C', width=2.5),
        marker=dict(size=8, color='#E05C5C')
    )
    fig_preg.update_layout(
        xaxis_title='Number of Pregnancies',
        yaxis_title='Diabetes Rate (%)',
        height=300,
        margin=dict(t=20, b=40, l=40, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#F0F2F5'),
        xaxis=dict(gridcolor='#F0F2F5')
    )
    st.plotly_chart(fig_preg, use_container_width=True)

with col4:
    st.markdown("**BMI Category Distribution by Outcome**")
    bmi_bins = [0, 18.5, 25, 30, 100]
    bmi_labels = ['Underweight', 'Normal', 'Overweight', 'Obese']
    df['BMIGroup'] = pd.cut(df['BMI'], bins=bmi_bins, labels=bmi_labels)

    bmi_stats = df.groupby(['BMIGroup', 'Outcome'], observed=True).size().reset_index(name='Count')
    bmi_stats['Label'] = bmi_stats['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'})

    fig_bmi = px.bar(
        bmi_stats, x='BMIGroup', y='Count', color='Label',
        color_discrete_map={'Non-Diabetic': '#4A90D9', 'Diabetic': '#E05C5C'},
        barmode='group'
    )
    fig_bmi.update_layout(
        xaxis_title='BMI Category',
        yaxis_title='Count',
        height=300,
        margin=dict(t=20, b=40, l=40, r=10),
        legend=dict(title='', orientation='h', yanchor='bottom', y=1.02),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#F0F2F5'),
        xaxis=dict(gridcolor='#F0F2F5')
    )
    st.plotly_chart(fig_bmi, use_container_width=True)

st.markdown("---")
st.markdown("**Key Insight**")
st.success("Diabetes risk increases sharply with age and number of pregnancies. Patients aged 61–70 show the highest prevalence rate, while obesity is present in the majority of diabetic cases.")
