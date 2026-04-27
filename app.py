import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ARCHITECTURE CONFIGURATION
st.set_page_config(page_title="Alethia Omega", layout="wide")

st.title("YK-A // ALETHIA OMEGA FORENSIC PORTAL")
st.sidebar.header("System Settings")

# 2. KEY INPUT (PERSISTENT)
# This allows you to update your API key without editing the file code ever again.
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 3. SPECIMEN INGESTION
uploaded_file = st.file_uploader("Upload Fish Specimen (JPEG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Specimen Ingested", use_container_width=True)
    
    # 4. EXECUTION BRIDGE
    # This button connects the image to the model ONLY when you are ready.
    if st.button("RUN FORENSIC SCAN"):
        if not api_key:
            st.error("System Error: API Key missing in Sidebar.")
        else:
            with st.spinner("Calibrating Alethia Omega Protocol..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    
                    # Hardened Logic Prompt
                    prompt = """
                    Analyze this Betta specimen as an expert judge. 
                    1. ID: Phenotype/Tail Type.
                    2. Structural Audit: Symmetry, finnage.
                    3. IBC Scorecard: Score Form, Color, Condition (0-100 scale).
                    4. Verdict: Pet, Breeder, or Show-Class.
                    Output in structured Markdown.
                    """
                    
                    response = model.generate_content([prompt, image])
                    st.subheader("FORENSIC REPORT")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Engine Failure: {e}")
else:
    st.info("System Ready. Awaiting Specimen.")
