"""
Step 6 (Analysis) technical explanation module.
Provides code walkthrough and key insights for the analysis process.
"""
import streamlit as st


def render_step6_explanation():
    """
    Renders the technical explanation expander for Step 6 (Analysis).
    Shows code walkthrough and key insights.
    """
    with st.expander("🔧 Technical Deep Dive: Root Cause Aggregation", expanded=False):
        st.markdown("### Code Walkthrough")
        st.markdown("""
        **Key Technical Concepts:**
        
        - **Failure Filtering**: Selecting only sessions where `label == 0` (failure) from the dataset
        - **Last Event Extraction**: Identifying the final event that executed successfully before failure 
          using list indexing (`x[-1]`)
        - **Aggregation by Failure Point**: Using `value_counts()` to group and count failures by their 
          last successful step
        - **Percentage Calculation**: Converting raw counts to percentages for easier interpretation of 
          failure distribution
        - **Statistical Ranking**: Sorting failure points by frequency to identify the most critical issues
        """)
        
        st.markdown("### Key Insight")
        st.info("""
        **Why This Matters:** 
        
        This is where all the pipeline work pays off - transforming raw data into actionable intelligence. 
        By aggregating failures at the "last successful step" level, we identify exactly where in the 
        workflow things are breaking.
        
        This statistical approach is more powerful than manually reading logs because it reveals patterns 
        across thousands of transactions. If 70% of failures occur after "UseCase_AuthUser", that's a 
        clear signal to investigate the authentication service.
        
        In production incident response, this analysis typically runs automatically every 5 minutes, 
        feeding dashboards and triggering alerts when failure rates exceed thresholds. It's the 
        difference between reactive debugging and proactive monitoring.
        """)
