"""
Step 5 (LSTM Training) technical explanation module.
Provides code walkthrough and key insights for the LSTM model training.
"""
import streamlit as st


def render_step5_explanation():
    """
    Renders the technical explanation expander for Step 5 (LSTM Training).
    Shows code walkthrough and key insights.
    """
    with st.expander("🔧 Technical Deep Dive: LSTM Architecture & Training", expanded=False):
        st.markdown("### Code Walkthrough")
        st.markdown("""
        **Key Technical Concepts:**
        
        - **Embedding Layer**: Transforms integer IDs into dense vectors (e.g., 16-dimensional) allowing 
          the model to learn semantic relationships between events
        - **LSTM Memory States**: The hidden state and cell state that carry information across time steps, 
          enabling the model to remember patterns from early in the sequence
        - **Binary Cross Entropy Loss**: The loss function used for binary classification (Success vs Failure), 
          calculated as `-[y*log(ŷ) + (1-y)*log(1-ŷ)]`
        - **Adam Optimizer**: Adaptive learning rate optimization algorithm that adjusts weights based on 
          gradient history
        - **Batch Processing**: Processing multiple sequences simultaneously for computational efficiency
        """)
        
        st.markdown("### Key Insight")
        st.info("""
        **Why This Matters:** 
        
        LSTMs are specifically designed for sequential data where order matters. Unlike traditional 
        neural networks that treat inputs independently, LSTMs maintain an internal "memory" that 
        allows them to learn long-term dependencies.
        
        In the context of RCA, this means the model can learn that "Login → Dashboard → Payment Error" 
        is fundamentally different from "Login → Auth Error" even though both contain errors. The LSTM 
        understands that the *sequence* and *position* of events are critical indicators of root cause.
        
        The supervised learning approach (with explicit SUCCESS/FAILURE labels) is used here for 
        educational clarity. In production systems with unlabeled data, you would use an unsupervised 
        autoencoder approach that learns "normal" patterns and flags deviations as anomalies.
        """)
