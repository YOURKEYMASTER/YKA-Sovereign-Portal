import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. SETUP: Configure the Brain
# NOTE: Set your API Key in Streamlit Secrets, NOT directly in code
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("YK-A SOVEREIGN // V15 FORENSIC SCANNER")

# 2. INPUT: File Uploader
uploaded_file = st.file_uploader("Upload Specimen Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Specimen Loaded", use_container_width=True)

    # 3. LOGIC: The Forensic Prompt
    if st.button("RUN AI FORENSIC SCAN"):
        with st.spinner("Analyzing phenotypes..."):
            prompt = """
            You are an expert International Betta Congress (IBC) Judge.
            Analyze this image and provide:
            1. IBC Scoring (0-100)
            2. Classification (Pet Grade / Breeder Grade / Show Grade)
            3. Forensic Findings (Finnage, Symmetry, Color saturation)
            Keep the response technical, cold, and precise.
            """
            
            # Send image and prompt to Gemini
            response = model.generate_content([prompt, image])
            
            # 4. OUTPUT: Display results
            st.subheader("FORENSIC REPORT")
            st.write(response.text)
import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP: Configuration
# Ensure you have your API key set in Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception:
    st.error("API Key not found. Please set 'GOOGLE_API_KEY' in Streamlit Secrets.")
    st.stop()

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("YK-A SOVEREIGN // V15 FORENSIC")

# 2. INPUT: Upload
uploaded_file = st.file_uploader("Upload Specimen", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Specimen Loaded", use_container_width=True)

    # 3. LOGIC: The Forensic Protocol
    if st.button("RUN AI FORENSIC SCAN"):
        with st.spinner("Analyzing phenotypes..."):
            try:
                # The "Neural Bridge" Instruction
                prompt = """
                You are a professional Betta fish judge. 
                Analyze this fish for: 
                1. Symmetry (0-100%)
                2. Finnage (1-10)
                3. Color (1-10)
                4. Grade (Pet, Breeder, or Show)
                5. Provide a cold, precise forensic report.
                """
                response = model.generate_content([prompt, image])
                
                # 4. OUTPUT
                st.subheader("FORENSIC REPORT")
                st.write(response.text)
            except Exception as e:
                st.error(f"Analysis Failed: {e}")
