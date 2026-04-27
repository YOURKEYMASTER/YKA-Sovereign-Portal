import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. SETUP
st.set_page_config(page_title="Alethia Omega Forensic Portal", layout="wide")
st.title("YK-A // ALETHIA OMEGA FORENSIC PORTAL")

# 2. CALIBRATION (If gemini-1.5-pro fails, try 'gemini-pro')
MODEL_NAME = "gemini-1.5-pro" 

# 3. SIDEBAR
st.sidebar.header("System Calibration")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# 4. FORENSIC ENGINE
def run_forensic_audit(image, api_key):
    genai.configure(api_key=api_key)
    
    # Debug: Print available models to your terminal console for diagnosis
    # Check your terminal (where you ran 'streamlit run') for this list
    print("--- DIAGNOSTIC: AVAILABLE MODELS ---")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"AVAILABLE: {m.name}")
            
    # Initialize the model
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
    Output in clean, structured Markdown.
    """
    
    response = model.generate_content([system_instruction, image])
    return response.text

# 5. UI
uploaded_file = st.file_uploader("Upload Specimen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Specimen Ingested", use_container_width=True)
    
    if st.button("EXECUTE FORENSIC ANALYSIS"):
        if not api_key:
            st.error("System Failure: API Key Required.")
        else:
            try:
                with st.spinner("Executing Alethia Omega Protocol..."):
                    result = run_forensic_audit(image, api_key)
                    st.subheader("FORENSIC REPORT")
                    st.markdown(result)
            except Exception as e:
                st.error(f"Engine Failure: {str(e)}")
                st.info(f"The system failed to call {MODEL_NAME}. Check your terminal for the 'DIAGNOSTIC' list and update the MODEL_NAME variable in app.py to a model listed as 'AVAILABLE'.")
