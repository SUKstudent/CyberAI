# app.py
import streamlit as st
import joblib
import io
from gtts import gTTS
from PIL import Image
import pytesseract
import numpy as np
import cv2

# ------------------ Tesseract Path (Windows) ------------------
# Uncomment if running locally on Windows
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ------------------ Display Centered Image ------------------
def display_centered_image(image_path, width=250):
    try:
        img = Image.open(image_path)
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(img, width=width)
    except Exception as e:
        st.warning(f"Image not found: {e}")

# ------------------ Text to Speech ------------------
def speak_streamlit(text, lang_code="en"):
    try:
        tts = gTTS(text=text, lang=lang_code)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        st.audio(mp3_fp, format="audio/mp3")
    except Exception:
        st.warning("Audio generation failed.")

# ------------------ Load Model ------------------
model_loaded = False
try:
    model = joblib.load("cyber_model.pkl")
    model_loaded = True
except Exception as e:
    st.error(f"⚠️ Model load error: {e}")

def predict_category(text):
    if not model_loaded:
        return "unknown"
    try:
        return model.predict([text])[0]
    except Exception:
        return "unknown"

# ------------------ OCR Function ------------------
def extract_text_from_image(image):
    try:
        img = np.array(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(gray, config=config)
        return text
    except Exception:
        return ""

# ------------------ Feedback ------------------
feedback_dict = {
    "phishing":"This message contains a suspicious link. Do NOT click it.",
    "malware":"This file or link can harm your phone. Do NOT open it.",
    "ransomware":"Your device may be locked for money. Do NOT pay anything.",
    "social_engineering":"Someone is trying to trick you. Do NOT trust easily.",
    "password_attack":"Someone is trying to get your password. Keep it safe.",
    "otp_fraud":"This message is asking for OTP. Do NOT share it.",
    "lottery_scam":"Fake lottery message. Ignore it.",
    "fake_app":"This app is not safe. Do not install it.",
    "financial_fraud":"This message is trying to steal your money.",
    "spyware_adware":"This may track your activity secretly."
}

# ------------------ Navigation ------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to:", ["Welcome","Demo / Analyze"])

# ------------------ Welcome Page ------------------
if page == "Welcome":
    st.title("👋 AI Cyber Safety Teacher")
    display_centered_image("welcome_image.jpeg", width=350)
    st.write("Learn to detect cyber threats easily!")
    speak_streamlit("Welcome to AI Cyber Safety Teacher! Learn to stay safe online.")

# ------------------ Demo / Analyze ------------------
elif page == "Demo / Analyze":
    st.header("🔍 Analyze Message / Screenshot")
    display_centered_image("ai_teacher_logo.jpeg", width=250)

    user_input = st.text_area("📩 Enter message / call content", height=150)

    uploaded_file = st.file_uploader("📷 Upload Screenshot (WhatsApp / Email)", type=["png","jpg","jpeg"])
    extracted_text = ""

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Screenshot")

        with st.spinner("Reading text from image..."):
            extracted_text = extract_text_from_image(image)

        if not extracted_text or len(extracted_text.strip()) < 5:
            st.warning("⚠️ Could not read text clearly. Try a better image or type manually.")
        else:
            st.success("✅ Text extracted successfully")
            st.write("📄 Extracted text:", extracted_text)

    col1, col2 = st.columns(2)

    with col1:
        analyze = st.button("🔍 Analyze")
    with col2:
        if st.button("🧹 Clear"):
            st.experimental_rerun()

    if analyze:
        final_text = user_input if user_input.strip() else extracted_text

        if not final_text or len(final_text.strip()) < 5:
            st.warning("⚠️ Please enter valid text")
            speak_streamlit("Please enter some text to analyze.")
        else:
            with st.spinner("Analyzing..."):
                category = predict_category(final_text)

            feedback = feedback_dict.get(category, "Be cautious!")
            st.error(feedback)
            st.success(f"Detected Type: {category}")
            speak_streamlit(feedback)
