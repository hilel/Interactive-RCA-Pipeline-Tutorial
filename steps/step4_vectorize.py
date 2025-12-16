import streamlit as st
from ui.educational_content import get_step4_education
from steps.step4_explanation import render_step4_explanation

def render_step4():
    st.header("Step 4: Vectorization")
    
    with st.expander("📘 Learn More: Computers Don't Read English", expanded=True):
        st.markdown(get_step4_education(), unsafe_allow_html=True)
    
    # Code Example Section
    st.markdown("### 💻 Code Implementation")
    st.markdown("""
    **Building the Vocabulary and Encoding Sequences:**
    
    This process converts text events into integers and pads them to a fixed length:
    """)
    
    code_snippet = '''def prepare_vectors(self, sessions: pd.DataFrame) -> pd.DataFrame:
    # Initialize vocabulary with special tokens
    self.event_to_id = {"<PAD>": 0, "<UNK>": 1}
    
    # 1. Build vocabulary: assign unique ID to each event
    all_events = set(x for seq in sessions['event_name'] for x in seq)
    for event in all_events:
        if event not in self.event_to_id:
            idx = len(self.event_to_id)
            self.event_to_id[event] = idx
    
    # 2. Encode sequences: text -> integers
    def encode(seq):
        return [self.event_to_id.get(e, 1) for e in seq]  # Default to <UNK>
    
    sessions['encoded'] = sessions['event_name'].apply(encode)
    
    # 3. Padding example (done during training):
    # [2, 5, 7] -> [2, 5, 7, 0, 0, 0, ..., 0]  (padded to max_seq_len)
    X_padded = [x[:max_seq_len] + [0]*(max_seq_len-len(x)) for x in X_list]
    
    return sessions'''
    
    st.code(code_snippet, language='python')
    
    st.markdown("""
    📁 **View Full Implementation:**
    - <a href="https://github.com/hilel/Interactive-RCA-Pipeline-Tutorial/blob/main/pipeline/orchestrator.py" target="_blank">pipeline/orchestrator.py</a> - Vectorization logic (lines 105-133)
    """, unsafe_allow_html=True)
    
    # Technical Deep Dive
    render_step4_explanation()
    
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
