import streamlit as st
import cv2
import numpy as np
import time

# --- SYSTEM CONFIG ---
st.set_page_config(page_title="YKA Sovereign Portal", layout="wide")
st.title("YKA_SOVEREIGN_V15_HARDENED")

# --- FORENSIC ENGINE ---
def process_specimen(frame):
    # Ensure color space is valid
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        main_fish = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(main_fish)
        perimeter = cv2.arcLength(main_fish, True)
        return area, perimeter
    return 0.0, 0.0

# --- UI LAYER ---
uploaded_file = st.file_uploader("Upload Specimen", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, 1)
    
    if frame is not None:
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_column_width=True)
        
        if st.button("RUN FORENSIC AUDIT"):
            with st.spinner("Processing..."):
                area, perimeter = process_specimen(frame)
                
                st.subheader("RAW FORENSICS")
                st.write(f"- AREA: {area:.0f} px")
                st.write(f"- PERIMETER: {perimeter:.1f} px")
                
                st.subheader("SHOKUNIN VERDICT")
                if area > 100:
                    st.success("STATUS: GO | Geometric integrity confirmed.")
                else:
                    st.error("STATUS: NO-GO | Structural anomaly detected.")
    else:
        st.error("Frame capture failed. Check file format.")
else:
    st.info("System Awaiting Ingestion.")
