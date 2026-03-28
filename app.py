# app.py
import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image
import speech_recognition as sr

# ---------- Function to display centered images ----------
def display_centered_image(image_path, width=250):
    try:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(image_path, width=width)
    except Exception as e:
        st.warning(f"Image not found or failed to load: {e}")

# ---------- TTS + Robot Animation ----------
def speak_streamlit(text, lang_code="en"):
    # Display talking robot animation
    display_centered_image("robot_talking.gif", width=150)
    
    # Convert text to speech
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

# ---------- Cyber Attack Types ----------
attack_names = {
    "phishing":{"English":"Phishing","Hindi":"फ़िशिंग","Kannada":"ಫಿಶಿಂಗ್"},
    "malware":{"English":"Malware","Hindi":"मैलवेयर","Kannada":"ಮ್ಯಾಲ್ವೇರ್"},
    "ransomware":{"English":"Ransomware","Hindi":"रैनसमवेयर","Kannada":"ರೆನ್ಸಮ್‌ವೇರ್"},
    "social_engineering":{"English":"Social Engineering","Hindi":"सोशल इंजीनियरिंग","Kannada":"ಸೋಶಿಯಲ್ ಇಂಜಿನಿಯರಿಂಗ್"},
    "password_attack":{"English":"Password Attack","Hindi":"पासवर्ड हमला","Kannada":"ಪಾಸ್ವರ್ಡ್ ದಾಳಿ"},
    "otp_fraud":{"English":"OTP Fraud","Hindi":"OTP धोखा","Kannada":"OTP ಮೋಸ"},
    "lottery_scam":{"English":"Lottery Scam","Hindi":"लॉटरी घोटाला","Kannada":"ಲಾಟರಿ ಮೋಸ"},
    "fake_app":{"English":"Fake App","Hindi":"नकली ऐप","Kannada":"ನಕಲಿ ಆಪ್"},
    "financial_fraud":{"English":"Financial Fraud","Hindi":"वित्तीय धोखा","Kannada":"ಹಣಕಾಸು ಮೋಸ"},
    "spyware_adware":{"English":"Spyware / Adware","Hindi":"स्पायवेयर / एडवेयर","Kannada":"ಸ್ಪೈವೇರ್ / ಆಡ್ವೇರ್"}
}

# ---------- Navigation ----------
st.sidebar.header("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Welcome","Cyber Attack Details","Demo / Analyze"])

# ---------- Welcome Page ----------
if page=="Welcome":
    display_centered_image("welcome_animation.gif", width=400)
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
    for key, names in attack_names.items():
        st.write(f"• {names[lang]}")
        speak_streamlit(f"{names[lang]} detected", lang_code=lang_code)

# ---------- Demo / Analyze ----------
elif page=="Demo / Analyze":
    display_centered_image("ai_teacher_logo.jpeg", width=250)
    lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
    lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
    lang_code = lang_map_code[lang]

    st.header("🔍 Analyze Message")

    # Text input
    user_input = st.text_area("📩 Enter message", height=150)

    # Voice input
    st.write("🎤 Or click to record voice message:")
    if st.button("🎙️ Record Voice"):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            st.info("Listening... Speak now.")
            audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            user_input = recognizer.recognize_google(audio, language=lang_code)
            st.success(f"📝 You said: {user_input}")
        except:
            st.error("Voice not recognized, try again.")

    if st.button("🔍 Analyze"):
        if user_input.strip()=="":
            st.warning("⚠️ Please enter text or speak.")
        else:
            category = predict_category(user_input)
            type_name = attack_names.get(category, {"English":"Unknown","Hindi":"अज्ञात","Kannada":"ಅಜ್ಞಾನ"})[lang]
            st.info(f"🛡️ Detected Cyber Attack Type: {type_name}")
            feedback = feedback_dict.get(category, {"English":"Be cautious","Hindi":"सतर्क रहें","Kannada":"ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"})[lang]
            st.error(feedback)
            speak_streamlit(feedback, lang_code=lang_code)
