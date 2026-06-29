import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("diabetes.csv")
for col in ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]:
    df[col] = df[col].replace(0, df[col].median())

st.markdown('<p class="section-title">ML Diabetes Risk Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="section-sub">Random Forest classifier trained on clinical measurements to predict diabetes risk.</p>', unsafe_allow_html=True)

# Train model
@st.cache_resource
def train_model():
    df_model = pd.read_csv("diabetes.csv")
    # Replace 0s in clinical cols with median (0 is biologically impossible)
    for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
        df_model[col] = df_model[col].replace(0, df_model[col].median())
    X = df_model.drop('Outcome', axis=1)
    y = df_model['Outcome']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=8)
    model.fit(X_train_sc, y_train)
    acc = accuracy_score(y_test, model.predict(X_test_sc))
    return model, scaler, acc, X_test_sc, y_test, X.columns.tolist()

model, scaler, acc, X_test_sc, y_test, feature_names = train_model()

# Model stats row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Model Accuracy", f"{round(acc*100, 1)}%")
with col2:
    st.metric("Algorithm", "Random Forest")
with col3:
    st.metric("Training Size", f"{int(len(df)*0.8)} patients")

st.markdown("---")

tab1, tab2 = st.tabs(["🔮 Predict My Risk", "📊 Model Performance"])

with tab1:
    st.markdown("### Enter Patient Clinical Values")
    st.markdown('<p class="section-sub">Adjust the values below to get a personalized diabetes risk assessment.</p>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        pregnancies = st.slider("Number of Pregnancies", 0, 17, 1)
        glucose = st.slider("Glucose Level (mg/dL)", 44, 200, 120)
        blood_pressure = st.slider("Blood Pressure (mm Hg)", 24, 122, 70)
        skin_thickness = st.slider("Skin Thickness (mm)", 7, 99, 20)
    with c2:
        insulin = st.slider("Insulin (μU/mL)", 14, 846, 80)
        bmi = st.slider("BMI (kg/m²)", 18.0, 67.0, 25.0, step=0.1)
        dpf = st.slider("Diabetes Pedigree Function", 0.07, 2.42, 0.47, step=0.01)
        age = st.slider("Age (years)", 21, 81, 30)

    if st.button("🩺 Predict Diabetes Risk", use_container_width=True):
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                                 insulin, bmi, dpf, age]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
        prob = model.predict_proba(input_scaled)[0]

        st.markdown("---")
        risk_pct = round(prob[1] * 100, 1)

        if prediction == 1:
            st.error(f"### ⚠️ High Diabetes Risk Detected — {risk_pct}% probability")
            st.markdown("This patient profile shows clinical markers consistent with diabetes. We recommend further diagnostic testing including HbA1c and fasting plasma glucose.")
        else:
            st.success(f"### ✅ Low Diabetes Risk — {risk_pct}% probability")
            st.markdown("This patient profile does not strongly indicate diabetes. Continued healthy lifestyle and routine monitoring are recommended.")

        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            title={'text': "Diabetes Risk Score (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#E05C5C" if risk_pct > 50 else "#4A90D9"},
                'steps': [
                    {'range': [0, 30], 'color': '#D6F5E3'},
                    {'range': [30, 60], 'color': '#FFF3CD'},
                    {'range': [60, 100], 'color': '#4A90D9'}
                ],
                'threshold': {
                    'line': {'color': "#1B2B4B", 'width': 3},
                    'thickness': 0.75,
                    'value': risk_pct
                }
            }
        ))
        fig_gauge.update_layout(
            height=280,
            margin=dict(t=40, b=20, l=20, r=20),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Feature Importance**")
        importances = model.feature_importances_
        fi_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances})
        fi_df = fi_df.sort_values('Importance', ascending=True)

        fig_fi = go.Figure(go.Bar(
            x=fi_df['Importance'],
            y=fi_df['Feature'],
            orientation='h',
            marker_color='#4A90D9'
        ))
        fig_fi.update_layout(
            height=320,
            margin=dict(t=10, b=20, l=20, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(gridcolor='#F0F2F5', title='Importance Score'),
        )
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_b:
        st.markdown("**Confusion Matrix**")
        y_pred = model.predict(X_test_sc)
        cm = confusion_matrix(y_test, y_pred)

        fig_cm = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicted: No', 'Predicted: Yes'],
            y=['Actual: No', 'Actual: Yes'],
            colorscale=[[0, '#EEF2F8'], [1, '#1B2B4B']],
            text=cm,
            texttemplate='%{text}',
            textfont=dict(size=18, color='white'),
            showscale=False
        ))
        fig_cm.update_layout(
            height=320,
            margin=dict(t=10, b=20, l=20, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_cm, use_container_width=True)

    st.markdown("**Classification Report**")
    report = classification_report(y_test, y_pred, target_names=['Non-Diabetic', 'Diabetic'], output_dict=True)
    report_df = pd.DataFrame(report).transpose().round(2)
    st.dataframe(report_df, use_container_width=True)
