import streamlit as st
from ui.educational_content import get_step4_education

def render_step4():
    st.header("Step 4: Vectorization")
    
    with st.expander("📘 Learn More: Computers Don't Read English", expanded=True):
        st.markdown(get_step4_education(), unsafe_allow_html=True)
    
    if st.button("Prepare Vectors", help="Convert text lists to integer lists."):
        with st.spinner("Encoding sequences..."):
            st.session_state.df_ready = st.session_state.facade.vectorize_sessions(st.session_state.df_sessions)
            st.success("Vectorization complete.")
    
    if st.session_state.df_ready is not None:
        st.subheader("Deep Dive: Text vs. Numbers")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Human Readable (Text)**")
            st.write(st.session_state.df_ready['event_name'].iloc[0])
        with col2:
            st.markdown("**Machine Readable (Vector)**")
            st.write(st.session_state.df_ready['encoded'].iloc[0])
        
        st.subheader("Vocabulary Map")
        vocab = st.session_state.facade.get_vocabulary()
        st.json(vocab)
        
        if st.button("Next: Train Model"):
            st.session_state.current_step = 5
            st.rerun()
