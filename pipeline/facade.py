from typing import List, Dict, Any
import pandas as pd
from pipeline.orchestrator import ProjectStressedPipeline
from utils.data_generator import generate_messy_logs

class StressedPipelineFacade:
    """
    A Facade class to simplify interaction with the Project Stressed Pipeline.
    It encapsulates the complexity of the orchestrator and data generator,
    providing a clean API for the UI or other consumers.
    """

    def __init__(self):
        self.pipeline = ProjectStressedPipeline()

    def generate_synthetic_logs(self, num_orders: int = 100) -> List[str]:
        """
        Generates synthetic messy logs.
        """
        return generate_messy_logs(num_orders=num_orders)

    def process_etl(self, raw_logs: List[str]) -> pd.DataFrame:
        """
        Runs the ETL process to convert raw logs into a structured DataFrame.
        """
        return self.pipeline.run_etl(raw_logs)

    def create_sessions(self, df_events: pd.DataFrame) -> pd.DataFrame:
        """
        Groups events into user sessions.
        """
        return self.pipeline.sessionize_data(df_events)

    def vectorize_sessions(self, df_sessions: pd.DataFrame) -> pd.DataFrame:
        """
        Converts session data into vectors for the model.
        """
        return self.pipeline.prepare_vectors(df_sessions)

    def train_model(self, df_ready: pd.DataFrame):
        """
        Trains the LSTM model on the prepared data.
        """
        self.pipeline.train_model(df_ready)

    def get_vocabulary(self) -> Dict[int, str]:
        """
        Returns the vocabulary mapping (ID -> Event Name).
        """
        return self.pipeline.id_to_event

    def get_failure_stats(self, df_ready: pd.DataFrame) -> pd.DataFrame:
        """
        Analyzes failures and returns a DataFrame with statistics.
        """
        failed_orders = df_ready[df_ready['label'] == 0].copy()
        if failed_orders.empty:
            return pd.DataFrame(columns=['Last Successful Step', 'Count', 'Percentage'])
        
        # Get the last event before failure (or "UnknownEvent" if empty)
        failed_orders['last_step'] = failed_orders['event_name'].apply(
            lambda x: x[-1] if (isinstance(x, list) and len(x) > 0) else "UnknownEvent"
        )
        breakdown = failed_orders['last_step'].value_counts().reset_index()
        breakdown.columns = ['Last Successful Step', 'Count']
        breakdown['Percentage'] = (breakdown['Count'] / len(failed_orders) * 100).round(1)
        return breakdown

    def get_order_details(self, df_ready: pd.DataFrame, order_id: int) -> Dict[str, Any]:
        """
        Retrieves details for a specific order.
        """
        row = df_ready[df_ready['order_id'] == order_id].iloc[0]
        return {
            'order_id': row['order_id'],
            'status': "SUCCESS" if row['label'] == 1 else "FAILURE",
            'events': row['event_name'],
            'raw_logs': row['raw_log'],
            'encoded': row['encoded']
        }

    def get_random_failed_order(self, df_ready: pd.DataFrame) -> int:
        """
        Returns the ID of a random failed order.
        """
        failed = df_ready[df_ready['label'] == 0]
        if not failed.empty:
            return failed.sample(1).iloc[0]['order_id']
        # Fallback to any order if no failures
        return df_ready.iloc[0]['order_id']

    def get_ai_insight(self, breakdown: pd.DataFrame) -> Dict[str, str]:
        """
        Generates AI insights based on failure statistics.
        """
        if breakdown.empty:
            return {"type": "success", "message": "No failures detected.", "insight": ""}
        
        top_fail = breakdown.iloc[0]['Last Successful Step']
        percentage = breakdown.iloc[0]['Percentage']
        
        if "UseCase_AuthUser" in top_fail:
            return {
                "type": "critical",
                "message": f"CRITICAL: {percentage}% of failures stop at '{top_fail}'.",
                "insight": "High abandonment during Auth. Check SMS Gateway latency or UI glitches on Login."
            }
        elif "UseCase_CheckDelivery" in top_fail:
             return {
                "type": "critical",
                "message": f"CRITICAL: {percentage}% of failures stop at '{top_fail}'.",
                "insight": "Logistics API might be timing out or rejecting valid addresses."
             }
        else:
            return {
                "type": "warning",
                "message": f"Most failures occur at {top_fail}.",
                "insight": "Investigate logs specifically for this step."
            }
