"""
Log parsing agent for Project Stressed.
Simulates LLM-based structured generation using regex heuristics.
"""

import re
from datetime import datetime
from models.schema import StructuredLogEvent


class LogParserAgent:
    """
    In the real 'Project Stressed', this class wraps the 'outlines' library
    calling a local LLM (like Qwen2.5-Coder).
    
    Here, we simulate that intelligence using Regex heuristics so you can run 
    this without a GPU.
    """
    
    def parse(self, raw_text: str) -> StructuredLogEvent:
        """
        Parse raw log text into a structured event.
        
        Args:
            raw_text: Raw log string
            
        Returns:
            StructuredLogEvent object with extracted fields
        """
        # 1. Extract Timestamp: Look for [YYYY-MM-DD HH:MM:SS]
        ts_match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', raw_text)
        timestamp = ts_match.group(1) if ts_match else datetime.now().isoformat()
        
        # 2. Extract Event Name: Look for UseCase_... or Screen_...
        # This is the "Buried Event" logic. The Regex ignores surrounding text.
        event_match = re.search(r'(UseCase_\w+|Screen_\w+)', raw_text)
        event_name = event_match.group(1) if event_match else "UnknownEvent"
        
        # 3. Extract Order ID: Look for "Order #123" or "Order>123" or "order_id': 123"
        order_match = re.search(r'Order #?(\d+)|<Order>(\d+)|order_id\W+(\d+)', raw_text)
        # Regex groups logic: find which group captured the digits
        if order_match:
            # Filter out None values from the groups and take the first match
            order_id = int(next(g for g in order_match.groups() if g is not None))
        else:
            order_id = None
        
        # 4. Extract Severity
        sev_match = re.search(r'\[(INFO|WARN|ERROR)\]', raw_text)
        severity = sev_match.group(1) if sev_match else "INFO"
        
        # Return the strictly typed object
        return StructuredLogEvent(
            timestamp=timestamp, 
            event_name=event_name, 
            order_id=order_id, 
            severity=severity, 
            details="Mock Details"
        )
