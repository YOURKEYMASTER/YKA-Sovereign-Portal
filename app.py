import streamlit as st
import cv2
import numpy as np
import tempfile
import os
import config  # Importing your knowledge core

st.set_page_config(page_title="YKA Sovereign Portal", layout="wide")
st.title("YKA_SOVEREIGN_V15_HARDENED")

# SIDEBAR: DATA INTEGRATION
with st.sidebar.expander("System Knowledge"):
    st.write("Pioneer Zero Metrics:", config.MANIFEST_DATA["PIONEER_ZERO"])
    st.write("Taxonomy Translation:", config.TAXONOMY_MAP)

# FORENSIC ENGINE
uploaded_file = st.file_uploader("Upload Specimen", type=['png', 'jpg', 'mp4', 'mov'])

if uploaded_file is not None:
    file_type = uploaded_file.type
    
    if file_type.startswith('video'):
        st.video(uploaded_file)
        
        # Immediate extraction
        uploaded_file.seek(0)
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        tfile.close()
        
        cap = cv2.VideoCapture(tfile.name)
        ret, frame = cap.read()
        
        if ret:
            st.success("Frame buffer operational.")
            # Perform basic Forensic Analysis
            st.image(frame, channels="BGR", caption="Specimen Frame - Ready for Analysis")
        
        cap.release()
        os.unlink(tfile.name)
    else:
        st.image(uploaded_file, use_column_width=True)
        st.write("System: Specimen Awaiting Forensic Processing.")
