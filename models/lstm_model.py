"""
LSTM Neural Network Model for Project Stressed.
Implements the Deep Learning component for sequence analysis.
"""

import torch
import torch.nn as nn


class RCA_LSTM(nn.Module):
    """
    A PyTorch Module implementing a Long Short-Term Memory network.
    LSTM is chosen because it has 'Cell State' (Memory) which allows it to 
    remember if 'User was New' 10 steps ago.
    """
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(RCA_LSTM, self).__init__()
        
        # Layer 1: Embedding
        # Converts an integer ID (e.g., 5) into a vector of floats (e.g., [0.1, -0.5, ...])
        # This allows the model to learn semantic similarity between events.
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        
        # Layer 2: LSTM
        # batch_first=True means the input tensor shape is (Batch_Size, Sequence_Length, Dimensions)
        # This layer processes the sequence step-by-step, updating its internal memory.
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        
        # Layer 3: Fully Connected (Linear)
        # Takes the final hidden state of the LSTM and maps it to the output dimension (1).
        # It essentially asks: "Given this memory state, is this a success or failure?"
        self.fc = nn.Linear(hidden_dim, output_dim)
        
        # Layer 4: Sigmoid Activation
        # Squashes the output between 0 and 1 (Probability).
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        """
        Forward pass through the network.
        
        Args:
            x: Input tensor of shape (batch_size, sequence_length)
            
        Returns:
            Probability tensor of shape (batch_size, 1)
        """
        # 1. Turn IDs into Vectors
        embedded = self.embedding(x) 
        
        # 2. Run the LSTM over the sequence
        # 'out' is output at every step. 'hidden' is the state at the LAST step.
        # We only care about the final state (did the order finish?).
        _, (hidden, cell) = self.lstm(embedded)
        
        # 3. Take the last hidden state.
        # hidden shape is (1, batch_size, hidden_dim). Squeeze removes the '1'.
        final_state = hidden.squeeze(0)
        
        # 4. Produce prediction
        return self.sigmoid(self.fc(final_state))
