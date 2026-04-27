import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==============================================================================
# CALIBRATION SECTION: UPDATE THIS VARIABLE BASED ON YOUR 'model_audit.py' RESULT
# If your audit said 'models/gemini-1.5-pro', put 'gemini-1.5-pro' here.
MODEL_NAME = "gemini-1.5-pro" 
# ==============================================================================

st.set_page_config(page_title="Alethia Omega Forensic Portal", layout="wide")

st.title("YK-A // ALETHIA OMEGA FORENSIC PORTAL")
st.sidebar.header("System Calibration")

api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

def run_forensic_audit(image, api_key):
    genai.configure(api_key=api_key)
    # Using the configurable MODEL_NAME variable
    model = genai.GenerativeModel(MODEL_NAME)
    
    system_instruction = """
    You are the Alethia Omega Forensic System. 
    Analyze the uploaded Betta specimen. 
    Provide: 
    1. Identification (Phenotype, Tail Type, Color)
    2. Structural Audit (Symmetry/Median Line)
    3. Coloration Audit (Saturation/Iridescence)
    4. IBC Scorecard (Form/Color/Condition - 0 to 100 scale)
    5. Final Verdict (Pet/Breeder/Show Class)
    Output in clean, structured Markdown. Be data-driven.
    """
    
    response = model.generate_content([system_instruction, image])
    return response.text

uploaded_file = st.file_uploader("Upload Specimen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Specimen Ingested", use_container_width=True)
    
    st.write("---")
    
    if st.button("EXECUTE FORENSIC ANALYSIS"):
        if not api_key:
            st.error("System Failure: API Key Required.")
        else:
            with st.spinner("Executing Alethia Omega Protocol..."):
                try:
                    result = run_forensic_audit(image, api_key)
                    st.subheader("FORENSIC REPORT")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Engine Failure: {str(e)}")
                    st.info(f"Check your API Key settings. Current Target Model: {MODEL_NAME}")
else:
    st.info("System Online. Awaiting Specimen Ingestion.")
