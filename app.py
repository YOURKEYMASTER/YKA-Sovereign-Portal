import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. FORENSIC ENGINE CONFIGURATION
API_KEY = "AIzaSyBL7pB9xF1dpOklwGmrj8oosPGgNt7agLc"  # Keep the quotes!
genai.configure(api_key=API_KEY)

# Alethia Omega System Instructions
system_prompt = """
You are the Alethia Omega Forensic System, the world's most advanced Betta splendens audit entity. 
Perform an objective, data-driven analysis of fish specimens. 

REASONING PROTOCOL:
1. IDENTIFICATION: Identify phenotype, tail type, and base color.
2. STRUCTURAL AUDIT: Assess symmetry (median line). Analyze finnage integrity.
3. COLORATION AUDIT: Evaluate color saturation, distribution, and iridescent quality.
4. IBC RUBRIC (Score 0-100):
   - Form (0-40)
   - Color (0-40)
   - Condition (0-20)
5. SNI COMPLIANCE: Evaluate local standard adherence.
6. FINAL CLASSIFICATION: [Pet / Breeder / Show - Local / Show - National]

OUTPUT FORMAT:
Use strictly formatted Markdown headers. Be brutal but fair. 
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_prompt
)

# 2. INTERFACE LAYER
st.title("YK-A // ALETHIA OMEGA FORENSIC SCAN")
uploaded_file = st.file_uploader("Upload Specimen", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if st.button("RUN FORENSIC SCAN"):
        with st.spinner("Executing Forensic Audit..."):
            prompt = "Analyze this Betta specimen based on your Forensic Protocol."
            try:
                response = model.generate_content([prompt, image])
                st.subheader("FORENSIC REPORT")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Engine Failure: {e}")
