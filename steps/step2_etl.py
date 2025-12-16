import streamlit as st
from ui.educational_content import get_step2_education

def render_step2():
    st.header("Step 2: Extract, Transform, Load (ETL)")
    
    with st.expander("📘 Learn More: The ETL Process", expanded=True):
        st.markdown(get_step2_education(), unsafe_allow_html=True)
        st.info("💡 **Interactive Tip:** Look at the 'Event Name' column below. It's clean text, unlike the raw logs. This is the power of transformation!")
    
    if st.button("Run ETL Process", help="Parse the raw text into a structured table."):
        with st.spinner("Parsing logs..."):
            st.session_state.df_events = st.session_state.facade.process_etl(st.session_state.raw_logs)
            st.success(f"Parsed {len(st.session_state.df_events)} structured events.")
    
    if st.session_state.df_events is not None:
        st.subheader("Structured Data")
        st.dataframe(st.session_state.df_events.head(50))
        
        if st.button("Next: Sessionize"):
            st.session_state.current_step = 3
            st.rerun()
