"""
Step 1 (Log Generation) technical explanation module.
Provides code walkthrough and key insights for the log generation process.
"""
import streamlit as st


def render_step1_explanation():
    """
    Renders the technical explanation expander for Step 1 (Log Generation).
    Shows code walkthrough and key insights.
    """
    with st.expander("🔧 Technical Deep Dive: Synthetic Data Generation", expanded=False):
        st.markdown("### Code Walkthrough")
        st.markdown("""
        **Key Technical Concepts:**
        
        - **Golden Path Workflow**: A predefined sequence of 9 events representing the ideal successful 
          user journey from Login to Success screen
        - **Failure Injection Probabilities**: 80% success rate and 20% failure rate, with failures 
          occurring at random cutoff points in the workflow
        - **Mixed Log Formats**: Randomly generating logs in Plain Text, XML, and JSON formats to 
          simulate real legacy systems with inconsistent logging
        - **Temporal Jitter**: Adding realistic time delays (1-10 seconds) between events to simulate 
          actual system processing times
        - **Unique Session IDs**: Using incremental Order IDs (1000+) as session identifiers
        """)
        
        st.markdown("### Key Insight")
        st.info("""
        **Why This Matters:** 
        
        Synthetic data generation is critical for testing and education because it provides a controlled, 
        reproducible environment without exposing sensitive production data. The deliberate injection of 
        chaos (mixed formats, random failures) mirrors real-world complexity.
        
        The "golden path" concept is fundamental to RCA - by defining what success *should* look like, 
        we can identify deviations. The LSTM model will eventually learn this golden path by heart and 
        flag anything that deviates from it.
        
        In production, you would replace this generator with real log ingestion from Splunk, Datadog, 
        or CloudWatch, but the downstream pipeline remains identical.
        """)
