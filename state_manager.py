import streamlit as st
from pipeline.facade import StressedPipelineFacade

def init_session_state():
    if 'facade' not in st.session_state:
        st.session_state.facade = StressedPipelineFacade()
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'raw_logs' not in st.session_state:
        st.session_state.raw_logs = []
    if 'df_events' not in st.session_state:
        st.session_state.df_events = None
    if 'df_sessions' not in st.session_state:
        st.session_state.df_sessions = None
    if 'df_ready' not in st.session_state:
        st.session_state.df_ready = None
    if 'training_complete' not in st.session_state:
        st.session_state.training_complete = False
