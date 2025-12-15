"""
Data generation utilities for Project Stressed.
Simulates messy log data from legacy .NET/Angular systems.
"""

import random
from typing import List
from datetime import datetime, timedelta


def generate_messy_logs(num_orders=100) -> List[str]:
    """
    Generates a list of raw string logs mimicking a legacy .NET/Angular environment.
    It mixes Plain Text, XML payloads, and JSON payloads.
    
    Args:
        num_orders: Number of orders to simulate
        
    Returns:
        List of raw log strings
    """
    logs = []
    
    # The "Happy Path" - The sequence of events a successful order MUST follow.
    # The LSTM will eventually learn this sequence by heart.
    workflow_steps = [
        "Screen_Login",                      # 0. User hits Angular Login
        "UseCase_AuthUser",                  # 1. Backend Auth Check
        "Screen_Dashboard",                  # 2. User sees Dashboard
        "UseCase_CheckCustomerEligibility",  # 3. Backend checks rules
        "Screen_ProductSelect",              # 4. User picks item
        "UseCase_CheckDelivery",             # 5. Backend calls Logistics API
        "Screen_Review",                     # 6. User reviews cart
        "UseCase_SubmitOrder",               # 7. Final Submission
        "Screen_S14"                         # 8. SUCCESS STATE
    ]
    
    print(f"Generating synthetic logs for {num_orders} orders...")
    
    for i in range(num_orders):
        # Create a unique integer ID for this order. 
        # This will be our "Session Key" later.
        order_id = 1000 + i
        
        # Decide Fate: 80% Success, 20% Failure
        # If failure, we pick a random step to stop at (before the end).
        is_success = random.random() > 0.2
        cutoff = len(workflow_steps) if is_success else random.randint(1, len(workflow_steps)-1)
        
        # Start time for this specific order sequence (24 hours ago)
        current_time = datetime.now() - timedelta(hours=24) + timedelta(minutes=i*5)
        
        # Loop through the steps up to the cutoff point
        for step_idx, step in enumerate(workflow_steps[:cutoff]):
            
            # Increment time slightly so logs aren't instantaneous (realistic jitter)
            current_time += timedelta(seconds=random.randint(1, 10))
            ts_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            
            # --- CHAOS ENGINE: RANDOMIZE LOG FORMAT ---
            # This simulates your "Messy Data" problem.
            # The parser will have to handle all 3 formats.
            format_type = random.choice(['text', 'xml', 'json'])
            
            if format_type == 'text':
                # Standard legacy logging: Just a sentence.
                log_line = f"[{ts_str}] [INFO] [Thread-{random.randint(1,9)}] User executing {step} for Order #{order_id}. Processing..."
            
            elif format_type == 'xml':
                # XML Payload buried in text: Common in old SOAP/Enterprise services.
                log_line = f"[{ts_str}] [INFO] [Backend] TraceID: {random.randint(900,999)}. Running {step}. Payload: <Order>{order_id}</Order><State>Active</State>."
            
            elif format_type == 'json':
                # JSON Payload: Common in newer REST APIs.
                log_line = f"[{ts_str}] [INFO] [API] Context: {{'action': '{step}', 'order_id': {order_id}, 'meta': 'retry_0'}}"
                
            logs.append(log_line)
            
        # If it failed, we add a generic error log at the end to signify the crash.
        if not is_success:
            current_time += timedelta(seconds=2)
            ts_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            logs.append(f"[{ts_str}] [ERROR] [System] Order #{order_id} failed to transition. Logic Timeout.")

    # Return the raw list of strings
    return logs
