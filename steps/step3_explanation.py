"""
Step 3 (Sessionization) technical explanation module.
Provides code walkthrough and key insights for the sessionization process.
"""
import streamlit as st


def render_step3_explanation():
    """
    Renders the technical explanation expander for Step 3 (Sessionization).
    Shows code walkthrough and key insights.
    """
    with st.expander("🔧 Technical Deep Dive: Grouping Events into Sessions", expanded=False):
        st.markdown("### Code Walkthrough")
        st.markdown("""
        **Key Technical Concepts:**
        
        - **Grouping by Order ID**: Using Pandas `groupby('order_id')` to cluster all events belonging 
          to the same transaction
        - **Temporal Sorting**: Sorting events by timestamp within each group to ensure chronological order, 
          which is critical for sequential pattern learning
        - **List Aggregation**: Converting flat event rows into sequences (lists) of events per session
        - **Labeling Logic**: Determining success/failure based on presence of the final success event 
          (`Screen_S14`) in the sequence
        """)
        
        st.markdown("### Key Insight")
        st.info("""
        **Why This Matters:** 
        
        Sessionization transforms independent, scattered events into coherent user journeys. Without 
        this step, the LSTM would see a random jumble of events with no context about which events 
        belong together.
        
        Think of it like assembling a jigsaw puzzle - sessionization groups pieces (events) by their 
        picture (order_id) and arranges them in the right order (timestamp). Only then can you see 
        the full image (user journey).
        
        The temporal ordering is crucial: "Login → Error" tells a very different story than 
        "Error → Login". Sessionization preserves this critical sequence information for the AI.
        """)
