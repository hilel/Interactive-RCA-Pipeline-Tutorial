import streamlit as st

def render_stepper():
    steps = ["1. Generate Logs", "2. ETL", "3. Sessionize", "4. Vectorize", "5. Train Model", "6. Analysis"]
    
    html = '<div class="step-container">'
    for i, step in enumerate(steps, 1):
        status = "active" if i == st.session_state.current_step else "completed" if i < st.session_state.current_step else ""
        html += f'<div class="step {status}">{step}</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)
