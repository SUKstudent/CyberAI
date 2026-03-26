import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import joblib

# Multilingual Dataset (English + Hindi + Kannada)
data = {
    "text": [
        # PASSWORD
        "I shared my password",
        "How to create strong password",
        "मेरा पासवर्ड सुरक्षित है?",
        "पासवर्ड कैसे बनाएं",
        "ನಾನು ಪಾಸ್‌ವರ್ಡ್ ಹಂಚಿಕೊಂಡೆ",
        "ಬಲವಾದ ಪಾಸ್‌ವರ್ಡ್ ಹೇಗೆ ಮಾಡುವುದು",

        # OTP
        "Someone asked my OTP",
        "Bank asking OTP",
        "ओटीपी किसी को देना चाहिए?",
        "बैंक ने ओटीपी मांगा",
        "ಯಾರೋ OTP ಕೇಳುತ್ತಿದ್ದಾರೆ",
        "ಬ್ಯಾಂಕ್ OTP ಕೇಳುತ್ತದೆಯೇ",

        # PHISHING
        "I got a suspicious link",
        "Unknown message with link",
        "अज्ञात लिंक आया",
        "यह लिंक सुरक्षित है?",
        "ಅಪರಿಚಿತ ಲಿಂಕ್ ಬಂದಿದೆ",
        "ಈ ಲಿಂಕ್ ಸುರಕ್ಷಿತವೇ",

        # CALL
        "Fraud call asking money",
        "Call asking personal details",
        "धोखाधड़ी कॉल आया",
        "कॉल पैसे मांग रहा है",
        "ಮೋಸ ಕರೆ ಬಂದಿದೆ",
        "ಕಾಲ್ ಹಣ ಕೇಳುತ್ತಿದೆ"
    ],

    "label": [
        "password","password","password","password","password","password",
        "otp","otp","otp","otp","otp","otp",
        "phishing","phishing","phishing","phishing","phishing","phishing",
        "call","call","call","call","call","call"
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

# ML Pipeline
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", MultinomialNB())
])

# Train model
model.fit(X_train, y_train)

# Test accuracy
accuracy = model.score(X_test, y_test)
print("✅ Model Accuracy:", accuracy)

# Save model
joblib.dump(model, "cyber_model.pkl")
print("✅ Model saved as cyber_model.pkl")