import streamlit as st
from ui.educational_content import get_step3_education
from steps.step3_explanation import render_step3_explanation

def render_step3():
    st.header("Step 3: Sessionization")
    
    with st.expander("📘 Learn More: What is a Session?", expanded=True):
        st.markdown(get_step3_education(), unsafe_allow_html=True)
    
    # Code Example Section
    st.markdown("### 💻 Code Implementation")
    st.markdown("""
    **Grouping Events by Order ID:**
    
    The sessionization process groups flat events into temporal sequences:
    """)
    
    code_snippet = '''def sessionize_data(self, df: pd.DataFrame) -> pd.DataFrame:
    # 1. Ensure timestamp is datetime for proper sorting
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 2. Sort by order_id and timestamp (chronological order is CRITICAL)
    df = df.sort_values(by=['order_id', 'timestamp'])
    
    # 3. Group by Order ID and aggregate into lists
    sessions = df.groupby('order_id').agg({
        'event_name': list,      # ['Login', 'Auth', 'Dashboard', ...]
        'raw_log': list,         # Original log lines for traceability
        'timestamp': list        # Timestamps for each event
    }).reset_index()
    
    # 4. Label as Success (1) or Failure (0) based on final event
    sessions['label'] = sessions['event_name'].apply(
        lambda x: 1 if "Screen_S14" in x else 0
    )
    
    return sessions'''
    
    st.code(code_snippet, language='python')
    
    st.markdown("""
    📁 **View Full Implementation:**
    - <a href="https://github.com/hilel/Interactive-RCA-Pipeline-Tutorial/blob/main/pipeline/orchestrator.py" target="_blank">pipeline/orchestrator.py</a> - Sessionization logic (lines 68-100)
    """, unsafe_allow_html=True)
    
    # Technical Deep Dive
    render_step3_explanation()
    
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
