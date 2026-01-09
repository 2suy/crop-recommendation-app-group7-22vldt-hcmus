import streamlit as st
import joblib
import numpy as np
import pandas as pd

#Load model vào RAM
@st.cache_resource
def load_my_model():
    #File .pkl nằm cùng thư mục file .py
    return joblib.load('NHOM7_THUNDER (1).pkl')

#Cấu hình trang
st.set_page_config(page_title="NHÓM 7 <NUÔI CÂY>", page_icon="🌱", layout="centered")

#CSS Custom
st.markdown("""
    <style>
    [data-testid="stForm"] {
        background-color: #FFFDD0;
        padding: 15px 20px !important; /* Thu nhỏ padding trên dưới */
        margin-bottom: -5px !important; /* Đẩy thành phần phía dưới lên gần hơn */
    }
    /* Giảm khoảng cách của toàn bộ khối nội dung */
    [data-testid="stVerticalBlock"] {
        gap: 0.7rem !important; /* Giảm khoảng cách mặc định giữa các widget của Streamlit */
    }
    .stMarkdown {
        margin-bottom: -10px !important;
    }
    .stWidgetLabel p {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 20px !important;
        margin-bottom: 0px !important;
    }
    button[kind="primaryFormSubmit"] {
        background-color: #FF0000 !important;
        color: white !important; 
        border-radius: 10px !important;
        border: 2px solid #D1D1D1;
        width: 100%;
        margin-top: 0px !important;
        margin-bottom: 0px !important;
    }
    input {
        font-size: 18px !important;
    }
    /* Khoảng cách của vùng kết quả (Success box) */
    .stAlert {
        padding-top: 3px !important;
        padding-bottom: 3px !important;
    }
    </style>
    """, unsafe_allow_html=True)

#Logo và Tiêu đề
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo3.jpg", use_container_width=8000)
    except:
        st.warning("Không tìm thấy file logo3.jpg")

st.markdown("<h4 style='text-align: center; color: #1B4D3E; margin-top: -10px;'>HỆ THỐNG ỨNG DỤNG MACHINE LEARNING</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #1B4D3E; margin-top: -7px;'>TRONG PHÂN TÍCH ĐẤT VÀ KHÍ HẬU CHO LỰA CHỌN CÂY TRỒNG</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1E90FF; margin-top: 3px; margin-bottom: -15px;' font-size: 30px; font-style: italic;'>Một sản phẩm của Nhóm 7 - 22VLDT</p>", unsafe_allow_html=True)
st.divider()#đường kẻ ngang
st.write("Nhập thông số điều kiện khí hậu và dinh dưỡng đất để chúng tôi gợi ý cây trồng phù hợp cho bạn")

#Form nhập liệu
with st.form("my_form"):
    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Nồng độ Nito (N)", min_value=0.0, max_value=200.0, value=90.0, step=1.0)
        p = st.number_input("Nồng độ Photpho (P)", min_value=0.0, max_value=200.0, value=42.0, step=1.0)
        k = st.number_input("Nồng độ Kali (K)", min_value=0.0, max_value=300.0, value=43.0, step=1.0)
        ph = st.number_input("Độ pH đất", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
    with col2:
        temp = st.number_input("Nhiệt độ (°C)", min_value=0.0, max_value=60.0, value=25.0, step=1.0)
        hum = st.number_input("Độ ẩm (%)", min_value=0.0, max_value=100.0, value=80.0, step=1.0)
        rain = st.number_input("Lượng mưa (mm)", min_value=0.0, max_value=3000.0, value=200.0, step=1.0)
    
    submit = st.form_submit_button("XEM KẾT QUẢ")

#Dự đoán
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
        st.success(f"### Giống cây gợi ý:  {pred_en} - {pred_vi}")
        
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")