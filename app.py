import streamlit as st
import pyttsx3
import joblib
from utils import scenarios

# ---------- Voice Engine ----------
engine = pyttsx3.init()
engine.setProperty('rate', 150)
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# ---------- Load Model ----------
try:
    model = joblib.load("cyber_model.pkl")
    model_loaded = True
except:
    st.error("⚠️ Model not found! Run train.py first.")
    model_loaded = False

def predict_category(text):
    if model_loaded:
        return model.predict([text])[0]
    return None

# ---------- Feedback Dictionary ----------
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
st.set_page_config(page_title="Cyber AI Teacher", page_icon="🛡️")
st.title("🛡️ AI Cyber Safety Teacher")
st.markdown("### Protecting Everyone from Cyber Frauds")

lang = st.selectbox("🌐 Select Language", ["English","Hindi","Kannada"])
demo_mode = st.checkbox("💡 Demo Mode")

st.markdown("---")

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

col1, col2 = st.columns(2)
with col1: check = st.button("🔍 Analyze")
with col2: clear = st.button("🧹 Clear")

if clear:
    st.experimental_rerun()

if check or demo_mode:
    if not model_loaded:
        st.warning("⚠️ Model not loaded. Train the model first.")
    elif user_input.strip() == "":
        st.warning("⚠️ Please enter some text")
    else:
        category = predict_category(user_input)
        feedback = feedback_dict.get(category, {"English":"⚠️ Be cautious","Hindi":"⚠️ सतर्क रहें","Kannada":"⚠️ ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"})[lang]
        st.error(feedback)
        speak(feedback)

# ---------- Awareness ----------
st.markdown("---")
st.header("📚 Cyber Awareness Tips")
tips = {
    "English":["Never share OTP or PIN","Avoid unknown links","Banks never ask passwords","Install apps from trusted sources","Verify messages before clicking"],
    "Hindi":["OTP या PIN कभी साझा न करें","अज्ञात लिंक से बचें","बैंक कभी पासवर्ड नहीं मांगते","विश्वसनीय स्रोत से ऐप इंस्टॉल करें","संदेश सत्यापित करें"],
    "Kannada":["OTP ಅಥವಾ PIN ಯಾರಿಗೂ ಹಂಚಬೇಡಿ","ಅಪರಿಚಿತ ಲಿಂಕ್ ತಪ್ಪಿಸಿ","ಬ್ಯಾಂಕ್ ಪಾಸ್‌ವರ್ಡ್ ಕೇಳುವುದಿಲ್ಲ","ನಂಬನೀಯ ಮೂಲದಿಂದ ಅಪ್ಲಿಕೇಶನ್ ಸ್ಥಾಪಿಸಿ","ಸಂದೇಶ ಪರಿಶೀಲಿಸಿ"]
}
for tip in tips[lang]:
    st.write("•", tip)

# ---------- Interactive Quiz ----------
st.markdown("---")
st.header("🧠 Cyber Awareness Quiz (Yes/No)")

if st.button("Start Quiz"):
    correct = 0
    for s in scenarios.scenarios:
        user_ans = st.radio(s["scenario"], ["yes","no"], key=s["scenario"])
        if user_ans==s["answer"]:
            st.success("✅ Correct: "+s["explanation"])
            correct+=1
        else:
            st.error("❌ Wrong: "+s["explanation"])
    st.subheader(f"Your Score: {correct}/{len(scenarios.scenarios)}")
    speak(f"Your Score is {correct} out of {len(scenarios.scenarios)}")

st.markdown("---")
st.caption("Final Year Project | AI Cyber Safety for Illiterate Users")
