import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import config  # Importing your self-contained knowledge core

# PAGE ARCHITECTURE
st.set_page_config(page_title="YKA Sovereign Portal", layout="wide")
st.title("YKA_SOVEREIGN_V15_HARDENED")

# SIDEBAR: KNOWLEDGE INTEGRATION
with st.sidebar.header("Forensic Parameters"):
    st.write("System Status: Online")
    
    # Live Reference from Knowledge Core
    with st.expander("Pioneer Zero Metrics"):
        st.json(config.PIONEER_ZERO)
    
    with st.expander("Taxonomy Map"):
        st.write(config.TAXONOMY_MAP)

    caudal_sensitivity = st.sidebar.slider("Caudal Sensitivity", 0, 100, 50)
    st.sidebar.info("Protocols initialized: Biological/Geometric Mode.")

# INGESTION LAYER
uploaded_file = st.file_uploader("Upload Specimen", type=['png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'])

if uploaded_file is not None:
    file_type = uploaded_file.type
    
    # --- IMAGE PROTOCOL ---
    if file_type.startswith('image'):
        st.image(uploaded_file, caption="Specimen Ingested", use_column_width=True)
        st.write("### [SYSTEM]: Image Specimen detected. Ready for analysis.")
        
    # --- VIDEO PROTOCOL ---
    elif file_type.startswith('video'):
        st.video(uploaded_file)
        st.write("### [SYSTEM]: Initializing Forensic Buffer...")
        
        # 1. Pointer reset
        uploaded_file.seek(0)
        
        # 2. Temp file creation
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        tfile.close()
        
        # 3. OpenCV Processing
        cap = cv2.VideoCapture(tfile.name)
        ret, frame = cap.read()
        
        if ret:
            st.success("Frame buffer operational.")
            st.image(frame, channels="BGR", caption="Specimen Frame - Initialized")
        else:
            st.error("Frame capture failed. Check file integrity.")
        
        cap.release()
        os.unlink(tfile.name) # Immediate cleanup
    
    st.success("[SHOKUNIN VERDICT]: System Ready for Geometric Calculation.")
else:
    st.warning("System: Awaiting Specimen Input.")
