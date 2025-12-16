import streamlit as st
import time
from ui.educational_content import get_step1_education

def render_step1():
    st.header("Step 1: Generate Synthetic Logs")
    
    with st.expander("📘 Learn More: Why Synthetic Data?", expanded=True):
        st.markdown(get_step1_education(), unsafe_allow_html=True)
    
    num_orders = st.slider("Number of Orders to Simulate", 10, 500, 100, help="More orders = better training data, but slower processing.")
    
    if st.button("Generate Logs", help="Click to run the simulation engine."):
        with st.spinner("Generating logs..."):
            st.session_state.raw_logs = st.session_state.facade.generate_synthetic_logs(num_orders=num_orders)
            time.sleep(0.5)
            st.success(f"Generated {len(st.session_state.raw_logs)} log lines.")
    
    if st.session_state.raw_logs:
        st.subheader("Raw Log Preview")
        st.text_area("Logs", "\n".join(st.session_state.raw_logs[:20]) + "\n...", height=300)
        
        if st.button("Next: Run ETL"):
            st.session_state.current_step = 2
            st.rerun()
