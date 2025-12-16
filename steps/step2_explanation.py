"""
Step 2 (ETL) technical explanation module.
Provides code walkthrough and key insights for the ETL process.
"""
import streamlit as st


def render_step2_explanation():
    """
    Renders the technical explanation expander for Step 2 (ETL).
    Shows code walkthrough and key insights.
    """
    with st.expander("🔧 Technical Deep Dive: How ETL Works", expanded=False):
        st.markdown("### Code Walkthrough")
        st.markdown("""
        **Key Technical Concepts:**
        
        - **Regex Pattern Matching**: Using regular expressions to extract structured data from unstructured text
        - **Multi-Format Handling**: Parsing Plain Text, XML, and JSON formats in a single pass
        - **Noise Filtering**: Removing logs without Order IDs to focus on meaningful data
        - **Pydantic Schema Validation**: Ensuring extracted data conforms to a strict structure
        """)
        
        st.markdown("### Key Insight")
        st.info("""
        **Why This Matters:** 
        
        ETL is the foundation of any data pipeline. Without proper parsing, messy logs remain 
        unusable noise. The regex patterns in `LogParserAgent` act as the "intelligence layer" 
        that bridges raw chaos to structured analytics.
        
        In production systems handling millions of logs per hour, efficient ETL can be the difference 
        between real-time insights and stale data. The multi-format handling demonstrated here 
        (Plain Text, XML, JSON) mirrors real legacy systems where different components log in 
        different formats.
        """)
