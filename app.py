import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import config  # The Authority

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="YKA Sovereign Judge", layout="wide")
st.title("YK-A SOVEREIGN JUDGE // MASTER CORE 2026")

# --- FORENSIC AUDIT ENGINE ---
def run_forensic_audit(frame):
    # 1. Extraction (Simplified Analysis)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Simulated metrics based on PIONEER_ZERO keys
    area = np.count_nonzero(gray) / 1000 
    
    # 2. Comparison against config.PIONEER_ZERO
    target_spread = config.PIONEER_ZERO['Caudal_Spread']
    
    # Simple drift calculation
    drift = abs(target_spread - (area / 10)) 
    
    # 3. Verdict Logic
    is_go = drift < 10.0
    
    # 4. Classification Mapping from config.PHENOTYPES
    # Defaulting to HMPK if compliant
    classification = "HMPK" if is_go else "CULL"
    data = config.PHENOTYPES.get(classification, {"Type": "Unknown"})
    
    return is_go, classification, data['Type'], drift

# --- UI LAYER ---
uploaded_file = st.file_uploader("INGEST_SPECIMEN (IMAGE/VIDEO)", type=['png', 'jpg', 'jpeg', 'mp4', 'mov'])

if uploaded_file:
    # Buffer handling
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    ret, frame = cap.read()
    cap.release()
    os.unlink(tfile.name)
    
    if ret:
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_column_width=True)
        
        if st.button("EXECUTE AUDIT"):
            is_go, name, grade, drift = run_forensic_audit(frame)
            
            # --- DASHBOARD OUTPUT ---
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("STATUS", "GO" if is_go else "NO-GO")
            col2.metric("CLASSIFICATION", name)
            col3.metric("DRIFT_INDEX", f"{drift:.2f}")
            
            st.subheader("AUDIT REPORT")
            st.write(f"**GRADE:** {grade}")
            
            if is_go:
                st.success("AUDIT PASSED: SPECIMEN ALIGNED WITH PIONEER ZERO.")
            else:
                st.error("AUDIT FAILED: Structural drift detected.")
    else:
        st.error("Frame capture failed. Check file format.")

else:
    st.info("System Awaiting Ingestion.")
