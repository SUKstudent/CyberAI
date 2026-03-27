import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image
import pytesseract

# ---------- CONFIG ----------
st.set_page_config(page_title="Cyber Safety AI", layout="centered")

# ---------- IMAGE DISPLAY ----------
def display_centered_image(image_path, width=250):
    try:
        img = Image.open(image_path)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img, width=width)
    except:
        pass

# ---------- AUDIO ----------
def speak(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp)
    except:
        st.warning("Audio not supported")

# ---------- LOAD MODEL ----------
model_loaded = False
try:
    model = joblib.load("cyber_model.pkl")
    model_loaded = True
except:
    st.sidebar.warning("ML model not loaded")

# ---------- OCR FUNCTION ----------
def extract_text_from_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except:
        return ""

# ---------- PREDICTION ----------
def predict_category(text):
    text = text.lower()

    if "otp" in text:
        return "otp_fraud"
    elif "lottery" in text or "won" in text:
        return "lottery_scam"
    elif "password" in text:
        return "password_attack"
    elif "install" in text or "apk" in text:
        return "fake_app"
    elif "pay" in text or "money" in text:
        return "financial_fraud"
    elif "ransom" in text or "encrypted" in text:
        return "ransomware"
    elif "track" in text:
        return "spyware_adware"
    elif "urgent" in text:
        return "social_engineering"
    elif "link" in text or "click" in text:
        return "phishing"

    if model_loaded:
        return model.predict([text])[0]

    return "unknown"

# ---------- FEEDBACK ----------
feedback_dict = {
    "otp_fraud":{
        "English":"This message is asking for OTP. Do NOT share it.",
        "Hindi":"यह OTP मांग रहा है। साझा न करें।",
        "Kannada":"ಇದು OTP ಕೇಳುತ್ತಿದೆ. ಹಂಚಬೇಡಿ."
    },
    "phishing":{
        "English":"This message has a suspicious link. Do NOT click.",
        "Hindi":"इसमें संदिग्ध लिंक है। क्लिक न करें।",
        "Kannada":"ಇದರಲ್ಲಿ ಅನುಮಾನಾಸ್ಪದ ಲಿಂಕ್ ಇದೆ. ಕ್ಲಿಕ್ ಮಾಡಬೇಡಿ."
    },
    "lottery_scam":{
        "English":"Fake prize message. Ignore it.",
        "Hindi":"यह नकली इनाम है। अनदेखा करें।",
        "Kannada":"ಇದು ನಕಲಿ ಬಹುಮಾನ. ನಿರ್ಲಕ್ಷ್ಯ ಮಾಡಿ."
    },
    "malware":{
        "English":"This may harm your phone. Do not open.",
        "Hindi":"यह आपके फोन को नुकसान पहुंचा सकता है।",
        "Kannada":"ಇದು ನಿಮ್ಮ ಫೋನ್‌ಗೆ ಹಾನಿ ಮಾಡಬಹುದು."
    }
}

# ---------- NAVIGATION ----------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go", ["Home","Analyze"])

# ---------- HOME ----------
if page == "Home":
    st.title("AI Cyber Safety Teacher")

# ---------- ANALYZE ----------
elif page == "Analyze":
    st.title("Analyze Message")

    lang = st.selectbox("Language", ["English","Hindi","Kannada"])
    lang_code = {"English":"en","Hindi":"hi","Kannada":"kn"}[lang]

    # -------- TEXT INPUT --------
    text_input = st.text_area("Enter message")

    # -------- IMAGE INPUT --------
    uploaded_file = st.file_uploader("Upload screenshot (WhatsApp / Email)", type=["png","jpg","jpeg"])

    extracted_text = ""

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image")

        extracted_text = extract_text_from_image(image)
        st.write("📄 Extracted Text:", extracted_text)

    # -------- BUTTON --------
    if st.button("Analyze"):

        final_text = text_input if text_input else extracted_text

        if final_text.strip() == "":
            st.warning("No input provided")
        else:
            category = predict_category(final_text)

            feedback = feedback_dict.get(
                category,
                {
                    "English":"Be careful",
                    "Hindi":"सतर्क रहें",
                    "Kannada":"ಎಚ್ಚರಿಕೆ ವಹಿಸಿ"
                }
            )[lang]

            st.error("🚨 " + feedback)
            speak(feedback, lang_code)
