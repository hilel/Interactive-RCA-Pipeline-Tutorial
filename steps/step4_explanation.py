"""
Step 4 (Vectorization) technical explanation module.
Provides code walkthrough and key insights for the vectorization process.
"""
import streamlit as st


def render_step4_explanation():
    """
    Renders the technical explanation expander for Step 4 (Vectorization).
    Shows code walkthrough and key insights.
    """
    with st.expander("🔧 Technical Deep Dive: Text-to-Number Transformation", expanded=False):
        st.markdown("### Code Walkthrough")
        st.markdown("""
        **Key Technical Concepts:**
        
        - **Vocabulary Creation**: Building a dictionary that maps each unique event name to a unique integer ID
        - **Special Tokens**: Reserved IDs for `<PAD>` (0) and `<UNK>` (1) to handle padding and unknown events
        - **Sequence Encoding**: Converting text lists like `["Login", "Auth"]` to integer lists like `[2, 5]`
        - **Padding Sequences**: Appending zeros to short sequences so all inputs have the same fixed length 
          (e.g., 15 time steps), which is required for batch processing in neural networks
        - **Handling Unknown Tokens**: Defaulting to ID 1 (`<UNK>`) for events not seen during training
        """)
        
        st.markdown("### Key Insight")
        st.info("""
        **Why This Matters:** 
        
        Neural networks are mathematical functions that operate on matrices of numbers, not strings. 
        Vectorization is the bridge between human-readable logs and machine-processable data.
        
        The vocabulary acts as a "compression dictionary" - instead of storing the string "Screen_Login" 
        (12 bytes) repeatedly, we store the integer 2 (4 bytes), saving memory and computation time.
        
        Padding is essential for batch processing - without fixed-length inputs, you couldn't process 
        multiple sequences simultaneously on a GPU. The LSTM learns to ignore padding tokens (ID 0), 
        focusing only on actual events.
        """)
