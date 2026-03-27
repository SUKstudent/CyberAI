# app.py
import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image

# ---------- Page Config ----------
st.set_page_config(page_title="AI Cyber Safety Teacher", layout="centered")

# ---------- Function to display centered images ----------
def display_centered_image(image_path, width=250):
    try:
        img = Image.open(image_path)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(img, width=width)
    except:
        st.warning("⚠️ Image not found")

# ---------- Audio function ----------
def speak_streamlit(text, lang_code="en"):
    try:
        tts = gTTS(text=text, lang=lang_code)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        st.audio(mp3_fp, format="audio/mp3")
    except:
        st.warning("⚠️ Audio not supported")

# ---------- Load ML model ----------
model_path = "cyber_model.pkl"
model_loaded = False

try:
    model = joblib.load(model_path)
    model_loaded = True
except:
    st.sidebar.warning("⚠️ ML Model not loaded (using smart detection)")

# ---------- Smart Prediction Function ----------
def predict_category(text):
    text = text.lower()

    # Rule-based detection (FAST + WORKING)
    if "otp" in text:
        return "otp_fraud"
    elif "lottery" in text or "won" in text or "prize" in text:
        return "lottery_scam"
    elif "password" in text or "login" in text:
        return "password_attack"
    elif "install" in text or "apk" in text or "app" in text:
        return "fake_app"
    elif "pay" in text or "money" in text or "transfer" in text:
        return "financial_fraud"
    elif "encrypted" in text or "ransom" in text:
        return "ransomware"
    elif "spy" in text or "track" in text or "monitor" in text:
        return "spyware_adware"
    elif "urgent" in text or "call me" in text or "help me" in text:
        return "social_engineering"
    elif "click" in text or "link" in text:
        return "phishing"

    # ML fallback
    if model_loaded:
        return model.predict([text])[0]

    return "unknown"

# ---------- Feedback dictionary ----------
feedback_dict = {
    "phishing": {"English":"⚠️ Phishing! Avoid clicking unknown links",
                 "Hindi":"⚠️ फ़िशिंग! अज्ञात लिंक पर क्लिक न करें",
                 "Kannada":"⚠️ ಫಿಶಿಂಗ್! ಅಪರಿಚಿತ ಲಿಂಕ್ ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ"},

    "malware": {"English":"⚠️ Malware detected! Do not install unknown files",
                "Hindi":"⚠️ मैलवेयर! अज्ञात फ़ाइल इंस्टॉल न करें",
                "Kannada":"⚠️ ಮಾಲ್ವೇರ್! ಅಪರಿಚಿತ ಫೈಲ್ ಸ್ಥಾಪಿಸಬೇಡಿ"},

    "ransomware": {"English":"⚠️ Ransomware! Do not pay money",
                   "Hindi":"⚠️ रैनसमवेयर! पैसे न दें",
                   "Kannada":"⚠️ ರ್ಯಾನ್ಸಮ್‌ವೇರ್! ಹಣ ಕೊಡಬೇಡಿ"},

    "social_engineering": {"English":"⚠️ Social Engineering! Stay alert",
                           "Hindi":"⚠️ सोशल इंजीनियरिंग! सतर्क रहें",
                           "Kannada":"⚠️ ಸಾಮಾಜಿಕ ಎಂಜಿನಿಯರಿಂಗ್! ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"},

    "password_attack": {"English":"⚠️ Password attack! Use strong passwords",
                        "Hindi":"⚠️ पासवर्ड हमला! मजबूत पासवर्ड रखें",
                        "Kannada":"⚠️ ಪಾಸ್‌ವರ್ಡ್ ದಾಳಿ! ಬಲವಾದ ಪಾಸ್‌ವರ್ಡ್ ಬಳಸಿ"},

    "otp_fraud": {"English":"⚠️ OTP Fraud! Never share your OTP",
                  "Hindi":"⚠️ OTP धोखाधड़ी! OTP साझा न करें",
                  "Kannada":"⚠️ OTP ಮೋಸ! OTP ಹಂಚಬೇಡಿ"},

    "lottery_scam": {"English":"⚠️ Lottery Scam! Ignore fake prizes",
                     "Hindi":"⚠️ लॉटरी धोखाधड़ी! नकली इनाम से बचें",
                     "Kannada":"⚠️ ಲಾಟರಿ ಮೋಸ! ನಕಲಿ ಬಹುಮಾನವನ್ನು ನಿರ್ಲಕ್ಷ್ಯ ಮಾಡಿ"},

    "fake_app": {"English":"⚠️ Fake App! Install only from trusted sources",
                 "Hindi":"⚠️ नकली ऐप! केवल विश्वसनीय स्रोत से इंस्टॉल करें",
                 "Kannada":"⚠️ ನಕಲಿ ಆಪ್! ವಿಶ್ವಾಸಾರ್ಹ ಮೂಲಗಳಿಂದ ಮಾತ್ರ ಸ್ಥಾಪಿಸಿ"},

    "financial_fraud": {"English":"⚠️ Financial Fraud! Be careful with money transfers",
                        "Hindi":"⚠️ वित्तीय धोखाधड़ी! पैसे ट्रांसफर में सावधानी रखें",
                        "Kannada":"⚠️ ಹಣಕಾಸು ಮೋಸ! ಹಣ ವರ್ಗಾವಣೆಯಲ್ಲಿ ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"},

    "spyware_adware": {"English":"⚠️ Spyware/Adware! Protect your privacy",
                       "Hindi":"⚠️ स्पाईवेयर/एडवेयर! अपनी गोपनीयता सुरक्षित रखें",
                       "Kannada":"⚠️ ಸ್ಪೈವೇರ್/ಆಡ್ವೇರ್! ನಿಮ್ಮ ಗೌಪ್ಯತೆ ಕಾಪಾಡಿ"}
}

# ---------- Sidebar Navigation ----------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Welcome", "Cyber Attack Details", "Demo / Analyze"])

# ---------- Welcome Page ----------
if page == "Welcome":
    display_centered_image("welcome_image.jpeg", 350)

    lang = st.selectbox("🌐 Select Language", ["English", "Hindi", "Kannada"])
    lang_code = {"English":"en","Hindi":"hi","Kannada":"kn"}[lang]

    st.title("👋 AI Cyber Safety Teacher")

    msg = {
        "English":"Learn how to stay safe online!",
        "Hindi":"ऑनलाइन सुरक्षित रहना सीखें!",
        "Kannada":"ಆನ್‌ಲೈನ್ ಸುರಕ್ಷಿತವಾಗಿರಲು ಕಲಿಯಿರಿ!"
    }

    st.write(msg[lang])
    speak_streamlit(msg[lang], lang_code)

# ---------- Cyber Attack Details ----------
elif page == "Cyber Attack Details":
    display_centered_image("ai_teacher_logo.jpeg", 250)

    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_code = {"English":"en","Hindi":"hi","Kannada":"kn"}[lang]

    st.title("📚 Cyber Attack Types")

    details = {
        "phishing":"Fake links to steal data",
        "malware":"Harmful software",
        "ransomware":"Locks files for money",
        "otp_fraud":"Steals OTP",
        "lottery_scam":"Fake winnings",
        "fake_app":"Malicious apps",
        "financial_fraud":"Money scams",
        "social_engineering":"Tricks people",
        "password_attack":"Steals passwords",
        "spyware_adware":"Tracks your activity"
    }

    for k, v in details.items():
        st.write(f"• {k}: {v}")
        speak_streamlit(f"{k}: {v}", lang_code)

# ---------- Demo Page ----------
elif page == "Demo / Analyze":
    display_centered_image("ai_teacher_logo.jpeg", 250)

    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_code = {"English":"en","Hindi":"hi","Kannada":"kn"}[lang]

    st.title("🔍 Analyze Message")

    text = st.text_area("📩 Enter message", height=150)

    col1, col2 = st.columns(2)
    analyze = col1.button("Analyze")
    clear = col2.button("Clear")

    if clear:
        st.rerun()

    if analyze:
        if text.strip() == "":
            st.warning("Enter text")
            speak_streamlit("Please enter text", lang_code)
        else:
            category = predict_category(text)
            feedback = feedback_dict.get(category,
                        {"English":"Be cautious",
                         "Hindi":"सतर्क रहें",
                         "Kannada":"ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"})[lang]

            st.error(feedback)
            speak_streamlit(feedback, lang_code)
