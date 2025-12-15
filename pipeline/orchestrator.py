"""
Pipeline orchestrator for Project Stressed.
Coordinates the ETL, sessionization, vectorization, training, and reporting.
"""

from typing import List, Dict
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from parsers.log_parser import LogParserAgent
from models.lstm_model import RCA_LSTM


class ProjectStressedPipeline:
    """
    Main pipeline orchestrator that coordinates all stages of the RCA process.
    """
    
    def __init__(self):
        # Initialize the Parser Agent
        self.parser = LogParserAgent()
        
        # Initialize the Vocabulary. 
        # <PAD> (ID 0) is used to fill short sequences so all are same length.
        # <UNK> (ID 1) is used for events we haven't seen before.
        self.event_to_id = {"<PAD>": 0, "<UNK>": 1}
        self.id_to_event = {0: "<PAD>", 1: "<UNK>"}
        
        self.model = None
        # Maximum length of an order sequence to consider. 
        # Shorter orders get padded, longer ones get truncated.
        self.max_seq_len = 15

    # --------------------------------------------------------------------------
    # STEP 1: ETL (Extract, Transform, Load)
    # --------------------------------------------------------------------------
    def run_etl(self, raw_logs: List[str]) -> pd.DataFrame:
        """
        Ingests raw strings, parses them into Objects, converts to DataFrame.
        
        Args:
            raw_logs: List of raw log strings
            
        Returns:
            DataFrame with structured events
        """
        print("Running ETL Process...")
        data = []
        for line in raw_logs:
            # ASK THE PARSER to structure the data
            parsed = self.parser.parse(line)
            
            # We filter out logs that didn't have an Order ID (noise)
            if parsed.order_id:
                # Convert Pydantic object to Python Dict
                row = parsed.dict()
                # Store the RAW log too, so we can trace back later (Debuggability)
                row['raw_log'] = line 
                data.append(row)
                
        return pd.DataFrame(data)

    # --------------------------------------------------------------------------
    # STEP 2: SESSIONIZATION
    # --------------------------------------------------------------------------
    def sessionize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Groups the flat list of events into 'Sessions' based on Order ID.
        This turns a CSV-like structure into a Sequence structure.
        
        Args:
            df: DataFrame with structured events
            
        Returns:
            DataFrame with sessionized data
        """
        print("Sessionizing Data...")
        
        # Ensure timestamp is a true Datetime object for sorting
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Sort is CRITICAL. The LSTM assumes events are in chronological order.
        df = df.sort_values(by=['order_id', 'timestamp'])
        
        # Pandas Magic: Group by ID, and aggregate columns into lists.
        # Result: One row per order, with a list of events like ['Login', 'Auth', ...]
        sessions = df.groupby('order_id').agg({
            'event_name': list,
            'raw_log': list,
            'timestamp': list
        }).reset_index()
        
        # LABELING LOGIC:
        # How do we know if an order failed? 
        # Rule: If "Screen_S14" (Success Screen) is in the event list, it's a 1.
        sessions['label'] = sessions['event_name'].apply(lambda x: 1 if "Screen_S14" in x else 0)
        
        return sessions

    # --------------------------------------------------------------------------
    # STEP 3: VECTORIZATION
    # --------------------------------------------------------------------------
    def prepare_vectors(self, sessions: pd.DataFrame) -> pd.DataFrame:
        """
        Builds the dictionary (Vocabulary) and converts text lists to integer lists.
        
        Args:
            sessions: DataFrame with sessionized data
            
        Returns:
            DataFrame with encoded sequences
        """
        print("Building Vector Vocabulary...")
        
        # 1. Scan all data to find every unique event name
        all_events = set(x for seq in sessions['event_name'] for x in seq)
        
        # 2. Assign a unique ID to each event name
        for event in all_events:
            if event not in self.event_to_id:
                idx = len(self.event_to_id)
                self.event_to_id[event] = idx
                self.id_to_event[idx] = event

        # 3. Helper function to translate a list of strings to a list of ints
        def encode(seq):
            return [self.event_to_id.get(e, 1) for e in seq] # Default to 1 (<UNK>) if not found
        
        # 4. Apply encoding to the dataframe
        sessions['encoded'] = sessions['event_name'].apply(encode)
        return sessions

    # --------------------------------------------------------------------------
    # STEP 4: TRAINING
    # --------------------------------------------------------------------------
    def train_model(self, sessions: pd.DataFrame):
        """
        Prepares tensors and runs the training loop for the LSTM.
        
        Args:
            sessions: DataFrame with encoded sequences
        """
        print("Training Neural Network...")
        
        # Extract the integer lists
        X_list = sessions['encoded'].tolist()
        
        # PADDING: 
        # Deep Learning requires rectangular matrices. We can't have rows of different lengths.
        # We append 0s to short sequences until they reach max_seq_len.
        X_padded = [x[:self.max_seq_len] + [0]*(self.max_seq_len-len(x)) for x in X_list]
        
        # Convert Lists -> PyTorch Tensors (The format the GPU/CPU needs)
        X_tensor = torch.tensor(X_padded, dtype=torch.long)
        # Convert Labels -> Tensor. Unsqueeze(1) changes shape from [100] to [100, 1]
        y_tensor = torch.tensor(sessions['label'].tolist(), dtype=torch.float).unsqueeze(1)
        
        # Instantiate the Model
        # vocab_size = length of our dictionary
        # embedding_dim = 16 (size of the vector representing a word)
        # hidden_dim = 32 (size of the LSTM's memory brain)
        self.model = RCA_LSTM(len(self.event_to_id), 16, 32, 1)
        
        # Loss Function: Binary Cross Entropy (Standard for Yes/No classification)
        criterion = nn.BCELoss()
        
        # Optimizer: Adam (Adaptive Moment Estimation) - standard choice for generic training
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        
        # Training Loop
        self.model.train() # Set mode to train (enables gradient tracking)
        EPOCHS = 10
        
        for i in range(EPOCHS):
            optimizer.zero_grad()           # Clear previous gradients
            output = self.model(X_tensor)   # Forward pass (Make predictions)
            loss = criterion(output, y_tensor) # Calculate error
            loss.backward()                 # Backward pass (Calculate corrections)
            optimizer.step()                # Update weights (Apply corrections)
            
            if i % 2 == 0:
                print(f"Epoch {i}: Loss {loss.item():.4f}")
                
        print(f"Final Training Loss: {loss.item():.4f}")

    # ==========================================================================
    # REPORTING SUITE (The Transparency Layer)
    # ==========================================================================

    def print_system_internals(self):
        """
        DEBUG: Dumps the Vocabulary mapping.
        Shows you exactly which integer ID corresponds to which Event Name.
        """
        print("\n" + "="*60)
        print(" SYSTEM INTERNALS & VOCABULARY DUMP")
        print("="*60)
        
        print(f"Total Unique Events Learned: {len(self.event_to_id)}")
        print(f"{'ID':<5} | {'Event Name':<35}")
        print("-" * 45)
        
        # Sort by ID so it's easy to read
        for eid in sorted(self.id_to_event.keys()):
            name = self.id_to_event[eid]
            print(f"{eid:<5} | {name:<35}")
            
        print("-" * 45)

    def inspect_specific_order(self, sessions: pd.DataFrame, order_id_to_inspect: int = None):
        """
        TRACE: Pick one order and show the complete lifecycle.
        Raw Log -> Parsed Event -> Integer ID.
        
        Args:
            sessions: DataFrame with sessionized data
            order_id_to_inspect: Specific order ID to inspect (optional)
        """
        print("\n" + "="*60)
        print(" SINGLE ORDER DEEP DIVE TRACE")
        print("="*60)

        # If user didn't provide an ID, pick a random FAILED order to study
        if order_id_to_inspect is None:
            failed = sessions[sessions['label'] == 0]
            if not failed.empty:
                row = failed.sample(1).iloc[0]
            else:
                row = sessions.iloc[0] # Fallback if everything succeeded
        else:
            row = sessions[sessions['order_id'] == order_id_to_inspect].iloc[0]

        # Extract data for display
        oid = row['order_id']
        events = row['event_name']
        vectors = row['encoded']
        raws = row['raw_log']
        status = "SUCCESS" if row['label'] == 1 else "FAILURE"

        print(f"Order ID: {oid} | Final Status: [{status}]")
        print(f"Sequence Length: {len(events)} steps\n")
        
        # Table Header
        print(f"{'Step':<4} | {'Vector':<6} | {'Event Name':<30} | {'Original Raw Log Snippet'}")
        print("-" * 100)
        
        # Iterate through the sequence steps
        for i, (evt, vec, raw) in enumerate(zip(events, vectors, raws)):
            # Truncate raw log so it fits on screen
            raw_short = raw[:40] + "..." if len(raw) > 40 else raw
            print(f"{i+1:<4} | {vec:<6} | {evt:<30} | {raw_short}")
            
        print("-" * 100)
        
        # Show what the Neural Network actually sees (Vectors + Padding)
        padded_vec = vectors[:self.max_seq_len] + [0]*(self.max_seq_len-len(vectors))
        print(f"\nTensor Input to LSTM (Padded to {self.max_seq_len}):")
        print(padded_vec)

    def analyze_failures_detailed(self, sessions: pd.DataFrame):
        """
        INSIGHTS: Aggregates failure data to find the 'Smoking Gun'.
        Groups failures by the LAST SUCCESSFUL STEP to identify bottlenecks.
        
        Args:
            sessions: DataFrame with sessionized data
        """
        print("\n" + "="*60)
        print(" ROOT CAUSE AGGREGATION REPORT")
        print("="*60)
        
        # Filter for failed orders only
        failed_orders = sessions[sessions['label'] == 0].copy()
        
        if failed_orders.empty:
            print("No failures to analyze.")
            return

        # Feature Extraction: Get the last event in the list for every failed order
        failed_orders['last_step'] = failed_orders['event_name'].apply(lambda x: x[-1] if x else "No Events")
        
        # Aggregation: Count how many times each step was the 'last step'
        breakdown = failed_orders['last_step'].value_counts().reset_index()
        breakdown.columns = ['Last Successful Step', 'Count']
        
        # Calculate Percentage
        breakdown['Percentage'] = (breakdown['Count'] / len(failed_orders) * 100).round(1)
        
        print(f"Total Failed Orders: {len(failed_orders)}")
        print("\nTop Drop-off Points (Where flows are dying):")
        print(breakdown.to_string(index=False))
        
        # AUTOMATED ANALYSIS LOGIC
        # This simulates an AI giving advice based on the data stats
        print("\n--- AI Insights ---")
        top_fail = breakdown.iloc[0]['Last Successful Step']
        
        if "UseCase_AuthUser" in top_fail:
            print(f"CRITICAL: {breakdown.iloc[0]['Percentage']}% of failures stop at '{top_fail}'.")
            print(">> Insight: High abandonment during Auth. Check SMS Gateway latency or UI glitches on Login.")
        elif "UseCase_CheckDelivery" in top_fail:
             print(f"CRITICAL: {breakdown.iloc[0]['Percentage']}% of failures stop at '{top_fail}'.")
             print(">> Insight: Logistics API might be timing out or rejecting valid addresses.")
        else:
            print(f"Most failures occur at {top_fail}. Investigate logs specifically for this step.")
