import streamlit as st
import joblib
import numpy as np
import pandas as pd
import plotly.express as px

#Load model vào RAM
@st.cache_resource
def load_my_model():
    return joblib.load('NHOM7_THUNDER (1).pkl')

#Cấu hình
st.set_page_config(page_title="Green Suggestor", page_icon="🌱", layout="centered")

#CSS
st.markdown("""
    <style>
    [data-testid="stForm"] {
        background-color: #FFFDD0;
        padding: 15px 20px !important; /* Thu nhỏ padding trên dưới */
        margin-bottom: -5px !important; /* Đẩy thành phần phía dưới lên gần hơn */
    }
    [data-testid="stVerticalBlock"] {
        gap: 0.8rem !important; /* Chỉnh khoảng cách mặc định giữa các widget của Streamlit */
    }
    .stMarkdown {
        margin-bottom: -10px !important;
    }
    .stWidgetLabel p {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 60px !important;
        margin-bottom: 0px !important;
    }
    button[kind="primaryFormSubmit"] {
        background-color: blue !important;
        font-weight: bold !important;
        color: white !important; 
        border-radius: 10px !important;
        border: 2px solid #D1D1D1;
        width: 100%;
        margin-top: 15px !important;
        margin-bottom: 0px !important;
    }
    input {
        font-size: 18px !important;
    }

    [data-testid="stNotification"], .stAlert {
        background-color: red !important;
        border-radius: 10px !important;
        min-height: unset !important; /* Cho phép khung thu nhỏ theo chữ */
        padding: 5px 20px !important; /* Chỉnh độ gầy/béo của thanh đỏ ở đây */
    }

    [data-testid="stNotificationContent"] div {
        margin: 0px !important;
        padding: 0px !important;
    }

    .stAlert h3 {
        color: white !important;
        font-weight: bold !important;
        font-size: 28px !important;
        /* Quan trọng: Xóa sạch khoảng trống trên dưới của chữ */
        margin-top: -10px !important;
        margin-bottom: 10px !important;
        padding: 0px !important;
        line-height: 1.0 !important; /* Thu hẹp dòng chữ */
    }

    [data-testid="stNotification"] svg {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

#Logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo3.jpg", use_container_width=8000)
    except:
        st.warning("Không thấy logo")

st.markdown("<h1 style='text-align: center; color: #1B4D3E; margin-top: -10px;'>SmartCrop Analyzer</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1E90FF; margin-top: 5px; margin-bottom: -15px;' font-size: 30px; font-style: italic;'>Powered by Green Suggestor - 22VLDT</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: black; margin-top: 35px; margin-bottom: 8px;' font-size: 30px; font-style: italic;'>For more details, please contact Bao Le</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left; color: black; margin-bottom: -15px;' font-size: 30px; font-style: italic;'>Email: baoboaphysics2115@gmail.com</p>", unsafe_allow_html=True)
st.divider()
st.markdown("<p style='text-align: left; color: black; margin-top: 0px; margin-bottom: 20px;' font-size: 30px; font-style: italic;'>Enter environmental data for personalized crop suggestions:</p>", unsafe_allow_html=True)

#Form nhập liệu
with st.form("my_form"):
    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Nitrogen Content (N)", min_value=0.0, max_value=200.0, value=30.0, step=1.0)
        p = st.number_input("Phosphorus Content (P)", min_value=0.0, max_value=200.0, value=10.0, step=1.0)
        k = st.number_input("Potassium Content (K) ", min_value=0.0, max_value=300.0, value=10.0, step=1.0)
        ph = st.number_input("pH Value", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
    with col2:
        temp = st.number_input("Temperature (°C)", min_value=0.0, max_value=60.0, value=30.0, step=1.0)
        hum = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
        rain = st.number_input("Rainfall (mm)", min_value=0.0, max_value=3000.0, value=100.0, step=1.0)
    
    submit = st.form_submit_button("RESULTS")

# Dự đoán
if submit:
    try:
        model = load_my_model()
        input_df = pd.DataFrame([[n, p, k, temp, hum, ph, rain]], 
                                columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        
        prediction = model.predict(input_df)
        pred_en = str(prediction[0]).strip().lower()

        crop_map_vi = {
            "apple": "Táo", "banana": "Chuối", "blackgram": "Đậu đen", "chickpea": "Đậu gà",
            "coconut": "Dừa", "coffee": "Cà phê", "cotton": "Bông vải", "grapes": "Nho",
            "jute": "Cây đay", "kidneybeans": "Đậu thận", "lentil": "Đậu lăng", "maize": "Ngô",
            "mango": "Xoài", "mothbeans": "Đậu bướm", "mungbean": "Đậu xanh", "muskmelon": "Dưa lưới",
            "orange": "Cam", "papaya": "Đu đủ", "pigeonpeas": "Đậu triều", "pomegranate": "Lựu",
            "rice": "Lúa", "watermelon": "Dưa hấu"
        }
        
        pred_vi = crop_map_vi.get(pred_en, pred_en.capitalize())
        st.balloons()
        st.success(f"### Suggestion: {pred_en.upper()} - {pred_vi}")
        
        # ĐỒ THỊ
        st.divider()
        prob = model.predict_proba(input_df)[0]
        all_classes = model.classes_

        formatted_names = [f"{c.upper()} - {crop_map_vi.get(c.lower(), c.capitalize())}" for c in all_classes]
        df_prob = pd.DataFrame({
            'Crop': formatted_names,
            'Probabilities (%)': prob * 100
        })

        # Top 3, >= 10%
        df_filtered = df_prob[df_prob['Probabilities (%)'] >= 10]
        df_top3 = df_filtered.sort_values(by='Probabilities (%)', ascending=False).head(3)

        if not df_top3.empty:
            st.subheader("Most Suitable Crops:")
            
            # Biểu đồ Plotly
            fig = px.bar(
                df_top3, 
                x='Crop', 
                y='Probabilities (%)',
                color='Crop', 
                text='Probabilities (%)', 
                labels={'Probabilities (%)': 'Probability (%)'},
                color_discrete_sequence=px.colors.qualitative.Safe
            )

            # Layout
            fig.update_layout(
                font=dict(
                    family="Arial, sans-serif",
                    size=16,
                    color="black"
                ),
                title={
                    'text': "<b>TOP CROP PREDICTION ANALYSIS</b>",
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': {'size': 20}
                },
                xaxis=dict(
                    title="<b>Crop Types</b>",
                    tickfont=dict(size=18, color='black')
                ),
                yaxis=dict(
                    title="<b>Confidence (%)</b>",
                    tickfont=dict(size=16),
                    range=[0, 110]
                ),
                showlegend=False,
                height=450
            )

            fig.update_traces(
                texttemplate='<b>%{text:.2f}%</b>', 
                textposition='outside',
                textfont=dict(size=18, color='black') 
            )
            
            st.plotly_chart(fig, use_container_width=True, key="crop_chart_top3")

            st.subheader("Detailed:")
            st.dataframe(
                df_top3,
                column_config={
                    "Crop": st.column_config.TextColumn("Crop", width="medium"),
                    "Probabilities (%)": st.column_config.NumberColumn("Confident", format="%.2f%%", width="small")
                },
                hide_index=True,
                use_container_width=False 
            )
        else:
            st.warning("No crop matches")
        
    except Exception as e:
        st.error(f"System Error: {e}")
