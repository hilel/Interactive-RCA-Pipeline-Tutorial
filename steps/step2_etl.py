import streamlit as st
from ui.educational_content import get_step2_education
from steps.step2_explanation import render_step2_explanation

def render_step2():
    st.header("Step 2: Extract, Transform, Load (ETL)")
    
    with st.expander("📘 Learn More: The ETL Process", expanded=True):
        st.markdown(get_step2_education(), unsafe_allow_html=True)
        st.info("💡 **Interactive Tip:** Look at the 'Event Name' column below. It's clean text, unlike the raw logs. This is the power of transformation!")
    
    # Code Example Section
    st.markdown("### 💻 Code Implementation")
    st.markdown("""
    **How the Parser Extracts Data:**
    
    The `LogParserAgent.parse()` method uses regex patterns to extract structured information from messy logs:
    """)
    
    code_snippet = r'''def parse(self, raw_text: str) -> StructuredLogEvent:
    # 1. Extract Timestamp: Look for [YYYY-MM-DD HH:MM:SS]
    ts_match = re.search(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]', raw_text)
    timestamp = ts_match.group(1) if ts_match else datetime.now().isoformat()
    
    # 2. Extract Event Name: Look for UseCase_... or Screen_...
    event_match = re.search(r'(UseCase_\w+|Screen_\w+)', raw_text)
    event_name = event_match.group(1) if event_match else "UnknownEvent"
    
    # 3. Extract Order ID: Handle multiple formats
    order_match = re.search(r'Order #?(\d+)|<Order>(\d+)|order_id\W+(\d+)', raw_text)
    if order_match:
        order_id = int(next(g for g in order_match.groups() if g is not None))
    
    return StructuredLogEvent(timestamp=timestamp, event_name=event_name, 
                              order_id=order_id, severity=severity)'''
    
    st.code(code_snippet, language='python')
    
    st.markdown("""
    📁 **View Full Implementation:**
    - <a href="https://github.com/hilel/Interactive-RCA-Pipeline-Tutorial/blob/main/parsers/log_parser.py" target="_blank">parsers/log_parser.py</a> - Parser logic with regex patterns
    - <a href="https://github.com/hilel/Interactive-RCA-Pipeline-Tutorial/blob/main/pipeline/orchestrator.py" target="_blank">pipeline/orchestrator.py</a> - ETL orchestration flow
    """, unsafe_allow_html=True)
    
    # Technical Deep Dive
    render_step2_explanation()
    
    if st.button("Run ETL Process", help="Parse the raw text into a structured table."):
        with st.spinner("Parsing logs..."):
            st.session_state.df_events = st.session_state.facade.process_etl(st.session_state.raw_logs)
            st.success(f"Parsed {len(st.session_state.df_events)} structured events.")
    
    if st.session_state.df_events is not None:
        st.subheader("Structured Data")
        st.dataframe(st.session_state.df_events.head(50))
        
        if st.button("Next: Sessionize"):
            st.session_state.current_step = 3
            st.rerun()
