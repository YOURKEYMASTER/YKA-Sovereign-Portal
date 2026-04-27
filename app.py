import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. DIRECT CONFIG (No subfolders)
API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI
st.title("YK-A SOVEREIGN // V17 DIRECT")

uploaded_file = st.file_uploader("Upload Specimen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Specimen Loaded", use_container_width=True)

    if st.button("RUN AI FORENSIC SCAN"):
        with st.spinner("Analyzing phenotypes..."):
            prompt = """
            You are an expert Betta judge. Analyze this fish.
            Provide: IBC Score (0-100), Classification, and Forensic Notes.
            """
            try:
                response = model.generate_content([prompt, image])
                st.subheader("FORENSIC REPORT")
                st.write(response.text)
            except Exception as e:
                st.error(f"Analysis Error: {e}")
