# app.py
import streamlit as st
import joblib
import io
from gtts import gTTS
from utils import scenarios

# ---------- Function to play audio ----------
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

# ---------- Streamlit UI ----------
st.set_page_config(page_title="AI Cyber Safety Teacher", page_icon="🛡️")
st.title("🛡️ AI Cyber Safety Teacher")

# ---------- Language Selection ----------
lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
lang_map_code = {"English":"en","Hindi":"hi","Kannada":"kn"}
lang_code = lang_map_code[lang]

# ---------- Welcome Audio ----------
welcome_msg = {
    "English":"Welcome to AI Cyber Safety Teacher! Learn how to stay safe online.",
    "Hindi":"AI साइबर सुरक्षा शिक्षक में आपका स्वागत है! ऑनलाइन सुरक्षित रहें।",
    "Kannada":"AI ಸೈಬರ್ ಸೆಕ್ಯುರಿಟಿ ಟೀಚರ್‌ಗೆ ಸ್ವಾಗತ! ಆನ್‌ಲೈನ್ ಸುರಕ್ಷಿತವಾಗಿ ಇರಲು ಕಲಿಯಿರಿ."
}
speak_streamlit(welcome_msg[lang], lang_code=lang_code)

st.markdown("---")

# ---------- Next Page: Explain Attack Types ----------
st.header("📌 Cyber Attack Types")
attack_details = {
    "phishing": "Messages trying to steal your passwords or personal info via fake links.",
    "malware": "Software that harms your device or steals data.",
    "ransomware": "Locks your files and demands money to unlock.",
    "social_engineering": "Tricks people to share confidential info.",
    "password_attack": "Attempts to guess or steal your passwords.",
    "otp_fraud": "Fraud involving stealing your OTP.",
    "lottery_scam": "Fake lottery messages trying to steal info or money.",
    "fake_app": "Apps pretending to be real to steal data.",
    "financial_fraud": "Fraud related to bank transfers or money.",
    "spyware_adware": "Apps secretly tracking or showing unwanted ads."
}
for key, desc in attack_details.items():
    st.write(f"• {key.replace('_',' ').title()}: {desc}")
    speak_streamlit(f"{key.replace('_',' ').title()}: {desc}", lang_code=lang_code)

st.markdown("---")

# ---------- Demo / User Input ----------
demo_mode = st.checkbox("💡 Demo Mode")
demo_messages = {
    "phishing":"Click this suspicious link to claim prize",
    "malware":"Install this app to get reward",
    "ransomware":"Your files locked, pay to unlock",
    "social_engineering":"Call asking OTP for verification",
    "password_attack":"Someone asking for password",
    "otp_fraud":"Someone asked my OTP",
    "lottery_scam":"You won a lottery you never entered",
    "fake_app":"Install this fake banking app",
    "financial_fraud":"Bank transfer requested from unknown",
    "spyware_adware":"App is secretly tracking your device"
}
attack_type = st.selectbox("🔎 Select Demo Attack Type", list(demo_messages.keys()))
user_input = demo_messages[attack_type] if demo_mode else st.text_area("📩 Enter message / call content")

col1,col2 = st.columns(2)
with col1: check = st.button("🔍 Analyze")
with col2: clear = st.button("🧹 Clear")
if clear: st.experimental_rerun()

if check or demo_mode:
    if user_input.strip()=="":
        st.warning("⚠️ Please enter some text")
        speak_streamlit("Please enter some text to analyze.", lang_code=lang_code)
    else:
        category = predict_category(user_input)
        feedback = feedback_dict.get(category, {"English":"Be cautious","Hindi":"सतर्क रहें","Kannada":"ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"})[lang]
        st.error(feedback)
        speak_streamlit(feedback, lang_code=lang_code)

st.markdown("---")

# ---------- Cyber Awareness Tips ----------
st.header("📚 Cyber Awareness Tips")
tips = {
    "English":["Never share OTP or PIN","Avoid unknown links","Banks never ask passwords","Install apps from trusted sources","Verify messages before clicking"],
    "Hindi":["OTP या PIN कभी साझा न करें","अज्ञात लिंक से बचें","बैंक कभी पासवर्ड नहीं मांगते","विश्वसनीय स्रोत से ऐप इंस्टॉल करें","संदेश सत्यापित करें"],
    "Kannada":["OTP ಅಥವಾ PIN ಯಾರಿಗೂ ಹಂಚಬೇಡಿ","ಅಪರಿಚಿತ ಲಿಂಕ್ ತಪ್ಪಿಸಿ","ಬ್ಯಾಂಕ್ ಪಾಸ್‌ವರ್ಡ್ ಕೇಳುವುದಿಲ್ಲ","ನಂಬನೀಯ ಮೂಲದಿಂದ ಅಪ್ಲಿಕೇಶನ್ ಸ್ಥಾಪಿಸಿ","ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ"]
}
for tip in tips[lang]:
    st.write("•", tip)
    speak_streamlit(tip, lang_code=lang_code)

st.markdown("---")

# ---------- Interactive Quiz ----------
st.header("🧠 Cyber Awareness Quiz (Yes/No)")
if st.button("Start Quiz"):
    correct = 0
    for s in scenarios.scenarios:
        speak_streamlit(s["scenario"], lang_code=lang_code)
        user_ans = st.radio(s["scenario"], ["yes","no"], key=scenarios.scenarios.index(s))
        if user_ans==s["answer"]:
            st.success("✅ "+s["explanation"])
            speak_streamlit("Correct! "+s["explanation"], lang_code=lang_code)
            correct+=1
        else:
            st.error("❌ "+s["explanation"])
            speak_streamlit("Wrong! "+s["explanation"], lang_code=lang_code)
    st.subheader(f"Your Score: {correct}/{len(scenarios.scenarios)}")
    speak_streamlit(f"Your Score is {correct} out of {len(scenarios.scenarios)}", lang_code=lang_code)

st.markdown("---")
st.caption("Final Year Project | AI Cyber Safety for Illiterate Users")
