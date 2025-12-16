import streamlit as st
from ui.educational_content import get_step3_education

def render_step3():
    st.header("Step 3: Sessionization")
    
    with st.expander("📘 Learn More: What is a Session?", expanded=True):
        st.markdown(get_step3_education(), unsafe_allow_html=True)
    
    if st.button("Sessionize Data", help="Group events by Order ID."):
        with st.spinner("Grouping events..."):
            st.session_state.df_sessions = st.session_state.facade.create_sessions(st.session_state.df_events)
            st.success(f"Created {len(st.session_state.df_sessions)} user sessions.")
    
    if st.session_state.df_sessions is not None:
        st.subheader("User Journeys")
        st.dataframe(st.session_state.df_sessions[['order_id', 'event_name', 'label']].head(20))
        
        if st.button("Next: Vectorize"):
            st.session_state.current_step = 4
            st.rerun()
