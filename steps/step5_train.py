import streamlit as st
from ui.educational_content import get_step5_education
from steps.step5_explanation import render_step5_explanation

def render_step5():
    st.header("Step 5: Train LSTM Model")
    
    with st.expander("📘 Learn More: The Brain (LSTM)", expanded=True):
        st.markdown(get_step5_education(), unsafe_allow_html=True)
    
    # Code Example Section
    st.markdown("### 💻 Code Implementation")
    st.markdown("""
    **LSTM Neural Network Architecture:**
    
    The model consists of 4 layers that transform integer sequences into success/failure predictions:
    """)
    
    code_snippet = '''class RCA_LSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(RCA_LSTM, self).__init__()
        
        # Layer 1: Embedding - Convert integers to dense vectors
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # Layer 2: LSTM - Process sequences with memory
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        
        # Layer 3: Fully Connected - Map to output
        self.fc = nn.Linear(hidden_dim, output_dim)
        
        # Layer 4: Sigmoid - Convert to probability (0-1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        embedded = self.embedding(x)
        _, (hidden, cell) = self.lstm(embedded)
        final_state = hidden.squeeze(0)
        return self.sigmoid(self.fc(final_state))'''
    
    st.code(code_snippet, language='python')
    
    st.markdown("---")
    st.markdown("**Training Loop:**")
    
    training_snippet = '''# Training Loop (from orchestrator.py)
for epoch in range(EPOCHS):
    optimizer.zero_grad()           # Clear previous gradients
    output = self.model(X_tensor)   # Forward pass
    loss = criterion(output, y_tensor)  # Calculate error (BCE Loss)
    loss.backward()                 # Backward pass (compute gradients)
    optimizer.step()                # Update weights'''
    
    st.code(training_snippet, language='python')
    
    st.markdown("""
    📁 **View Full Implementation:**
    - <a href="https://github.com/hilel/Interactive-RCA-Pipeline-Tutorial/blob/main/models/lstm_model.py" target="_blank">models/lstm_model.py</a> - Neural network architecture
    - <a href="https://github.com/hilel/Interactive-RCA-Pipeline-Tutorial/blob/main/pipeline/orchestrator.py" target="_blank">pipeline/orchestrator.py</a> - Training logic (lines 138-186)
    """, unsafe_allow_html=True)
    
    # Technical Deep Dive
    render_step5_explanation()
    
    if st.button("Train Model", help="Start the neural network training loop."):
        with st.spinner("Training in progress..."):
            st.session_state.facade.train_model(st.session_state.df_ready)
            st.session_state.training_complete = True
        
        st.success("Training Complete! The model now understands the 'Happy Path'.")
        
    if st.session_state.training_complete:
        if st.button("Next: Analysis & Insights"):
            st.session_state.current_step = 6
            st.rerun()
