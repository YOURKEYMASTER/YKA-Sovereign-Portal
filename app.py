import streamlit as st
import cv2
import numpy as np
import config # Ensure this is in the same folder

st.set_page_config(page_title="YKA Forensic Judge", layout="wide")
st.title("YK-A SOVEREIGN JUDGE // DEBUGGER MODE")

def run_diagnostic_audit(frame):
    # 1. FORENSIC CALCULATIONS
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    area = np.count_nonzero(gray) / 1000
    
    # 2. COMPARISON (Using your config)
    target = config.PIONEER_ZERO['Caudal_Spread']
    # If the fish is "small" in the frame, the drift will always be huge
    current_val = area 
    drift = abs(target - current_val)
    
    # 3. LOGIC (More lenient for testing)
    # If drift is < 50, we call it Show Grade, else it's a Cull
    status = "GO" if drift < 50 else "NO-GO"
    classification = "HMPK" if status == "GO" else "CULL"
    
    return status, classification, drift, target, current_val

uploaded_file = st.file_uploader("INGEST_SPECIMEN", type=['jpg', 'png'])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    
    if st.button("EXECUTE AUDIT"):
        status, name, drift, target, current = run_diagnostic_audit(frame)
        
        # --- UI DISPLAY ---
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("VERDICT", status)
            st.metric("CLASSIFICATION", name)
        
        with col2:
            st.write("### DIAGNOSTIC LOG")
            st.write(f"Target Spread: {target}")
            st.write(f"Measured Metric: {current:.2f}")
            st.write(f"Calculated Drift: {drift:.2f}")
            
        # Fix for "Unknown Grade"
        grade_info = config.PHENOTYPES.get(name, {"Type": "Standard Grade"})
        st.write(f"**GRADE:** {grade_info['Type']}")
