import streamlit as st
from state_manager import init_session_state
from ui.styles import get_custom_css
from ui.sidebar import render_sidebar
from ui.stepper import render_stepper
from steps.step1_generate import render_step1
from steps.step2_etl import render_step2
from steps.step3_sessionize import render_step3
from steps.step4_vectorize import render_step4
from steps.step5_train import render_step5
from steps.step6_analysis import render_step6

# Page Config
st.set_page_config(
    page_title="Project Stressed - RCA Education",
    page_icon="🎓",
    layout="wide"
)

# Apply CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

def main():
    init_session_state()
    render_sidebar()
    
    st.title("🎓 Interactive RCA Pipeline")
    st.markdown("Follow the journey of data from raw chaos to actionable insights.")
    
    render_stepper()
    
    # Route to appropriate step
    if st.session_state.current_step == 1:
        render_step1()
    elif st.session_state.current_step == 2:
        render_step2()
    elif st.session_state.current_step == 3:
        render_step3()
    elif st.session_state.current_step == 4:
        render_step4()
    elif st.session_state.current_step == 5:
        render_step5()
    elif st.session_state.current_step == 6:
        render_step6()
    
    # --- SUMMARY ACCORDION ---
    st.markdown("---")
    with st.expander("📂 View All Step Results (Summary)"):
        if st.session_state.raw_logs:
            st.markdown("### 1. Raw Logs")
            st.text(f"Total Lines: {len(st.session_state.raw_logs)}")
        
        if st.session_state.df_events is not None:
            st.markdown("### 2. Structured Data")
            st.dataframe(st.session_state.df_events.head())
            
        if st.session_state.df_sessions is not None:
            st.markdown("### 3. Sessionized Data")
            st.dataframe(st.session_state.df_sessions.head())
            
        if st.session_state.df_ready is not None:
            st.markdown("### 4. Vectorized Data")
            st.dataframe(st.session_state.df_ready.head())

if __name__ == "__main__":
    main()
