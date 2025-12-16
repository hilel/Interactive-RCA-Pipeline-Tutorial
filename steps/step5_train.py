import streamlit as st
from ui.educational_content import get_step5_education

def render_step5():
    st.header("Step 5: Train LSTM Model")
    
    with st.expander("📘 Learn More: The Brain (LSTM)", expanded=True):
        st.markdown(get_step5_education(), unsafe_allow_html=True)
    
    if st.button("Train Model", help="Start the neural network training loop."):
        with st.spinner("Training in progress..."):
            st.session_state.facade.train_model(st.session_state.df_ready)
            st.session_state.training_complete = True
        
        st.success("Training Complete! The model now understands the 'Happy Path'.")
        
    if st.session_state.training_complete:
        if st.button("Next: Analysis & Insights"):
            st.session_state.current_step = 6
            st.rerun()
