import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import config  # This pulls from your config.py file

# --- CONFIGURATION ---
st.set_page_config(page_title="YKA Sovereign Portal", layout="wide")
st.title("YKA_SOVEREIGN_V15_HARDENED")

# --- FORENSIC PROCESSING ENGINE ---
def process_specimen(frame):
    """
    Analyzes the specimen for geometric traits.
    Returns: Area, Perimeter, and processed image for visualization.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        main_fish = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(main_fish)
        perimeter = cv2.arcLength(main_fish, True)
        # Draw the outline on the frame
        cv2.drawContours(frame, [main_fish], -1, (0, 255, 0), 2)
        return area, perimeter, frame
    return 0, 0, frame

# --- SIDEBAR: KNOWLEDGE INTEGRATION ---
with st.sidebar.header("Forensic Parameters"):
    st.write("System Status: Online")
    with st.expander("Pioneer Zero Metrics"):
        st.json(config.PIONEER_ZERO)
    with st.expander("Taxonomy Map"):
        st.write(config.TAXONOMY_MAP)
    caudal_sensitivity = st.sidebar.slider("Caudal Sensitivity", 0, 100, 50)
    st.sidebar.info("Protocols: Active.")

# --- INGESTION LAYER ---
uploaded_file = st.file_uploader("Upload Specimen", type=['png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'])

if uploaded_file is not None:
    file_type = uploaded_file.type
    
    if file_type.startswith('video'):
        st.video(uploaded_file)
        uploaded_file.seek(0)
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        tfile.close()
        
        cap = cv2.VideoCapture(tfile.name)
        ret, frame = cap.read()
        cap.release()
        os.unlink(tfile.name)
    else:
        # Load image for processing
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, 1)

    # --- EXECUTION ---
    if 'frame' in locals():
        st.success("[SYSTEM]: Forensic Engine Initialized.")
        area, perimeter, analyzed_frame = process_specimen(frame)
        
        # Display Results
        col1, col2 = st.columns(2)
        with col1:
            st.image(cv2.cvtColor(analyzed_frame, cv2.COLOR_BGR2RGB), caption="Analyzed Specimen")
        with col2:
            st.write("### [FORENSIC DATA]")
            st.write(f"**Specimen Area:** {area} px²")
            st.write(f"**Perimeter:** {perimeter:.2f} px")
            st.write(f"**Caudal Anchor (Standard):** {config.PIONEER_ZERO['Caudal_Spread']}°")
            st.success("Verdict: Forensic Analysis Complete.")
else:
    st.warning("System: Awaiting Specimen Input.")
