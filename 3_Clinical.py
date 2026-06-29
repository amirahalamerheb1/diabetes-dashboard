import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv("diabetes.csv")
df_clean = df[(df['Glucose'] > 0) & (df['BloodPressure'] > 0) & (df['BMI'] > 0) & (df['Insulin'] > 0)]

st.markdown('<p class="section-title">Clinical Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Deep dive into clinical measurements and their relationship to diabetes outcomes.</p>', unsafe_allow_html=True)

# Feature selector
feature = st.selectbox(
    "Select clinical variable to explore",
    ['Glucose', 'BMI', 'BloodPressure', 'Insulin', 'DiabetesPedigreeFunction', 'SkinThickness']
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**{feature} Distribution by Outcome**")
    fig_box = go.Figure()
    fig_box.add_trace(go.Box(
        y=df[df['Outcome'] == 0][feature],
        name='Non-Diabetic',
        marker_color='#4A90D9',
        boxmean=True
    ))
    fig_box.add_trace(go.Box(
        y=df[df['Outcome'] == 1][feature],
        name='Diabetic',
        marker_color='#E05C5C',
        boxmean=True
    ))
    fig_box.update_layout(
        yaxis_title=feature,
        height=340,
        margin=dict(t=20, b=20, l=40, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#F0F2F5'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    st.markdown(f"**{feature} vs Glucose (colored by Outcome)**")
    df_plot = df.copy()
    df_plot['Outcome_Label'] = df_plot['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'})
    if feature != 'Glucose':
        fig_scatter = px.scatter(
            df_plot, x=feature, y='Glucose',
            color='Outcome_Label',
            color_discrete_map={'Non-Diabetic': '#4A90D9', 'Diabetic': '#E05C5C'},
            opacity=0.6
        )
    else:
        fig_scatter = px.scatter(
            df_plot, x='BMI', y='Glucose',
            color='Outcome_Label',
            color_discrete_map={'Non-Diabetic': '#4A90D9', 'Diabetic': '#E05C5C'},
            opacity=0.6
        )
    fig_scatter.update_layout(
        height=340,
        margin=dict(t=20, b=20, l=40, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='#F0F2F5'),
        yaxis=dict(gridcolor='#F0F2F5'),
        legend=dict(title='', orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Correlation Heatmap**")
    corr = df.corr(numeric_only=True)
    fig_heat = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        colorscale=[[0, '#4A90D9'], [0.5, '#F8F9FB'], [1, '#E05C5C']],
        zmin=-1, zmax=1,
        text=np.round(corr.values, 2),
        texttemplate='%{text}',
        textfont=dict(size=10)
    ))
    fig_heat.update_layout(
        height=380,
        margin=dict(t=20, b=20, l=100, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with col4:
    st.markdown("**Mean Clinical Values: Diabetic vs Non-Diabetic**")
    features = ['Glucose', 'BMI', 'BloodPressure', 'Insulin', 'Age', 'Pregnancies']
    diabetic_means = df[df['Outcome'] == 1][features].mean()
    non_diabetic_means = df[df['Outcome'] == 0][features].mean()

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Diabetic',
        x=features,
        y=diabetic_means.values,
        marker_color='#E05C5C'
    ))
    fig_bar.add_trace(go.Bar(
        name='Non-Diabetic',
        x=features,
        y=non_diabetic_means.values,
        marker_color='#4A90D9'
    ))
    fig_bar.update_layout(
        barmode='group',
        height=380,
        margin=dict(t=20, b=40, l=40, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='#F0F2F5'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.markdown("**Summary Statistics**")
tab1, tab2 = st.tabs(["Diabetic Patients", "Non-Diabetic Patients"])
with tab1:
    st.dataframe(df[df['Outcome'] == 1].describe().round(2), use_container_width=True)
with tab2:
    st.dataframe(df[df['Outcome'] == 0].describe().round(2), use_container_width=True)
