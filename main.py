import random
import numpy as np
import torch

from pipeline.facade import StressedPipelineFacade


# --- REPRODUCIBILITY SETUP ---
# We set static seeds so that every time you run this script, 
# the "random" data and "random" model initialization is exactly the same.
# This makes debugging much easier.
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)


def main():
    """
    Main execution function for the RCA pipeline.
    """
    print("="*60)
    print(" PROJECT STRESSED: AUTOMATED ROOT CAUSE ANALYSIS")
    print("="*60)
    
    # 1. Instantiate the Facade Class
    facade = StressedPipelineFacade()
    
    # 2. Generate Messy Logs (Simulate 100 orders)
    raw_logs = facade.generate_synthetic_logs(num_orders=100)
    
    # 3. Run ETL (Parse Raw -> Structured DataFrame)
    df_events = facade.process_etl(raw_logs)
    
    # 4. Sessionize (Group Structured Events -> User Journeys)
    df_sessions = facade.create_sessions(df_events)
    
    # 5. Vectorize (Convert Journeys -> Integer Lists)
    df_ready = facade.vectorize_sessions(df_sessions)
    
    # 6. Train the Model (Teach LSTM the patterns)
    facade.train_model(df_ready)
    
    # 7. GENERATE REPORTS
    # A. Show the Vector Dictionary
    print("\n" + "="*60)
    print(" SYSTEM INTERNALS & VOCABULARY DUMP")
    print("="*60)
    
    vocab = facade.get_vocabulary()
    print(f"Total Unique Events Learned: {len(vocab)}")
    print(f"{'ID':<5} | {'Event Name':<35}")
    print("-" * 45)
    
    for eid in sorted(vocab.keys()):
        print(f"{eid:<5} | {vocab[eid]:<35}")
    print("-" * 45)
    
    # B. Deep Dive into one random failed order
    print("\n" + "="*60)
    print(" SINGLE ORDER DEEP DIVE TRACE")
    print("="*60)
    
    order_id = facade.get_random_failed_order(df_ready)
    details = facade.get_order_details(df_ready, order_id)
    
    print(f"Order ID: {details['order_id']} | Final Status: [{details['status']}]")
    print(f"Sequence Length: {len(details['events'])} steps\n")
    
    print(f"{'Step':<4} | {'Vector':<6} | {'Event Name':<30} | {'Original Raw Log Snippet'}")
    print("-" * 100)
    
    for i, (evt, vec, raw) in enumerate(zip(details['events'], details['encoded'], details['raw_logs'])):
        raw_short = raw[:40] + "..." if len(raw) > 40 else raw
        print(f"{i+1:<4} | {vec:<6} | {evt:<30} | {raw_short}")
        
    print("-" * 100)
    
    # C. High-level Failure Analysis
    print("\n" + "="*60)
    print(" ROOT CAUSE AGGREGATION REPORT")
    print("="*60)
    
    breakdown = facade.get_failure_stats(df_ready)
    
    if breakdown.empty:
        print("No failures to analyze.")
    else:
        print("\nTop Drop-off Points (Where flows are dying):")
        print(breakdown.to_string(index=False))
        
        print("\n--- AI Insights ---")
        insight = facade.get_ai_insight(breakdown)
        
        if insight['type'] == 'critical':
            print(insight['message'])
            print(f">> Insight: {insight['insight']}")
        elif insight['type'] == 'warning':
            print(f"{insight['message']} {insight['insight']}")
        else:
            print(insight['message'])
    
    print("\n" + "="*60)
    print(" ANALYSIS COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
