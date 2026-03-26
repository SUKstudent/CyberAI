# app.py
import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image
from utils import scenarios

# ---------- Function to display centered images ----------
def display_centered_image(image_path, width=250):
    try:
        img = Image.open(image_path)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img, width=width)
    except Exception as e:
        st.warning(f"Image not found or failed to load: {e}")

# ---------- Audio function ----------
def speak_streamlit(text, lang_code="en"):
    tts = gTTS(text=text, lang=lang_code)
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format="audio/mp3")

# ---------- Load model ----------
model_path = "cyber_model.pkl"
model_loaded = False
try:
    model = joblib.load(model_path)
    model_loaded = True
except Exception as e:
    st.error(f"⚠️ Model not found or error loading: {e}")

def predict_category(text):
    if not model_loaded:
        speak_streamlit("Model not loaded. Cannot predict.", lang_code="en")
        return "unknown"
    return model.predict([text])[0]

# ---------- Feedback dictionary ----------
feedback_dict = {
    "phishing":{"English":"⚠️ Phishing! Avoid links","Hindi":"⚠️ फ़िशिंग! लिंक से बचें","Kannada":"⚠️ ಫಿಶಿಂಗ್! ಲಿಂಕ್ ತಪ್ಪಿಸಿ"},
    "malware":{"English":"⚠️ Malware detected! Do not install","Hindi":"⚠️ मैलवेयर! इंस्टॉल न करें","Kannada":"⚠️ ಮಾಲ್ವೇರ್ ಕಂಡುಬಂದಿದೆ! ಸ್ಥಾಪಿಸಬೇಡಿ"},
    "ransomware":{"English":"⚠️ Ransomware! Do not pay","Hindi":"⚠️ रैनसमवेयर! भुगतान न करें","Kannada":"⚠️ ರ್ಯಾನ್ಸಮ್‌ವೇರ್! ಪಾವತಿ ಮಾಡಬೇಡಿ"},
    "social_engineering":{"English":"⚠️ Social Engineering! Be alert","Hindi":"⚠️ सोशल इंजिनियरिंग! सतर्क रहें","Kannada":"⚠️ ಸಾಮಾಜಿಕ ಎಂಜಿನಿಯರಿಂಗ್! ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"},
    "password_attack":{"English":"⚠️ Password attack! Keep strong","Hindi":"⚠️ पासवर्ड हमला! मजबूत रखें","Kannada":"⚠️ ಪಾಸ್‌ವರ್ಡ್ ದಾಳಿ! ಬಲವಾಗಿ ಇಡಿ"},
    "otp_fraud":{"English":"⚠️ OTP Fraud! Never share","Hindi":"⚠️ OTP धोखाधड़ी! साझा न करें","Kannada":"⚠️ OTP ಮೋಸ! ಹಂಚಬೇಡಿ"},
    "lottery_scam":{"English":"⚠️ Lottery Scam! Ignore","Hindi":"⚠️ लॉटरी धोखाधड़ी! अनदेखा करें","Kannada":"⚠️ ಲಾಟರಿ ಮೋಸ! ನಿರ್ಲಕ್ಷ್ಯ ಮಾಡಿ"},
    "fake_app":{"English":"⚠️ Fake App! Do not install","Hindi":"⚠️ नकली ऐप! इंस्टॉल न करें","Kannada":"⚠️ ನಕಲಿ ಅಪ್ಲಿಕೇಶನ್! ಸ್ಥಾಪಿಸಬೇಡಿ"},
    "financial_fraud":{"English":"⚠️ Financial Fraud! Be alert","Hindi":"⚠️ वित्तीय धोखाधड़ी! सतर्क रहें","Kannada":"⚠️ ಹಣಕಾಸು ಮೋಸ! ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"},
    "spyware_adware":{"English":"⚠️ Spyware/Adware! Be careful","Hindi":"⚠️ स्पाईवेयर/एडवेयर! सावधान रहें","Kannada":"⚠️ ಸ್ಪೈವೇರ್/ಆಡ್ವೇರ್! ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"}
}

# ---------- Navigation ----------
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Welcome","Cyber Attack Details","Demo / Analyze"])

# ---------- Welcome Page ----------
if page=="Welcome":
    display_centered_image("welcome_image.jpeg", width=350)

    # Language selector BELOW image
    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
    lang_code = lang_map_code[lang]

    st.header("👋 Welcome to AI Cyber Safety Teacher")
    welcome_msg = {
        "English":"Welcome to AI Cyber Safety Teacher! Learn how to stay safe online.",
        "Hindi":"AI साइबर सुरक्षा शिक्षक में आपका स्वागत है! ऑनलाइन सुरक्षित रहें।",
        "Kannada":"AI ಸೈಬರ್ ಸೆಕ್ಯುರಿಟಿ ಟೀಚರ್‌ಗೆ ಸ್ವಾಗತ! ಆನ್‌ಲೈನ್ ಸುರಕ್ಷಿತವಾಗಿ ಇರಲು ಕಲಿಯಿರಿ."
    }
    st.write(welcome_msg[lang])
    speak_streamlit(welcome_msg[lang], lang_code=lang_code)

# ---------- Cyber Attack Details ----------
elif page=="Cyber Attack Details":
    display_centered_image("ai_teacher_logo.jpeg", width=250)

    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
    lang_code = lang_map_code[lang]

    st.header("📌 Cyber Attack Types")

    attack_details = {
        "phishing": {
            "English": "Messages trying to steal your passwords or personal info via fake links.",
            "Hindi": "संदेश जो आपके पासवर्ड या व्यक्तिगत जानकारी को नकली लिंक के माध्यम से चुराने की कोशिश करते हैं।",
            "Kannada": "ತಪ್ಪು ಲಿಂಕ್ ಮೂಲಕ ನಿಮ್ಮ ಪಾಸ್ವರ್ಡ್ ಅಥವಾ ವೈಯಕ್ತಿಕ ಮಾಹಿತಿಯನ್ನು ಕದಿಯಲು ಪ್ರಯತ್ನಿಸುವ ಸಂದೇಶಗಳು."
        },
        "malware": {
            "English": "Software that harms your device or steals data.",
            "Hindi": "सॉफ़्टवेयर जो आपके डिवाइस को नुकसान पहुंचाता है या डेटा चुराता है।",
            "Kannada": "ನಿಮ್ಮ ಸಾಧನಕ್ಕೆ ಹಾನಿ ಮಾಡುವ ಅಥವಾ ಡೇಟಾವನ್ನು ಕದಿಯುವ ಸಾಫ್ಟ್‌ವೇರ್."
        }
    }

    for key, desc_dict in attack_details.items():
        st.write(f"• {key.title()}: {desc_dict[lang]}")
        speak_streamlit(f"{key.title()}: {desc_dict[lang]}", lang_code=lang_code)

# ---------- Demo / Analyze ----------
elif page=="Demo / Analyze":
    display_centered_image("ai_teacher_logo.jpeg", width=250)

    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
    lang_code = lang_map_code[lang]

    st.header("🔍 Demo / Manual Message Analysis")

    user_input = st.text_area("📩 Enter message / call content", height=150)

    col1, col2 = st.columns(2)
    with col1:
        check = st.button("🔍 Analyze")
    with col2:
        clear = st.button("🧹 Clear")

    if clear:
        st.experimental_rerun()

    if check:
        if user_input.strip() == "":
            st.warning("⚠️ Please enter some text")
            speak_streamlit("Please enter some text to analyze.", lang_code=lang_code)
        else:
            category = predict_category(user_input)
            feedback = feedback_dict.get(
                category,
                {"English":"Be cautious","Hindi":"सतर्क रहें","Kannada":"ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"}
            )[lang]

            st.error(feedback)
            speak_streamlit(feedback, lang_code=lang_code)
