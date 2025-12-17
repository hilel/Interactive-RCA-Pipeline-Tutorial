import streamlit as st
import time
from ui.educational_content import get_step1_education
from steps.step1_explanation import render_step1_explanation

def render_step1():
    st.header("Step 1: Generate Synthetic Logs")
    
    with st.expander("📘 Learn More: Why Synthetic Data?", expanded=True):
        st.markdown(get_step1_education(), unsafe_allow_html=True)
    
    # Code Example Section
    st.markdown("### 💻 Code Implementation")
    st.markdown("""
    **The Golden Path Workflow:**
    
    The generator defines a sequence of events that represent a successful order:
    """)
    
    code_snippet = '''# The "Happy Path" - Sequence a successful order MUST follow
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

# Decide Fate: 80% Success, 20% Failure
is_success = random.random() > 0.2
cutoff = len(workflow_steps) if is_success else random.randint(1, len(workflow_steps)-1)

# Generate logs for each step up to cutoff, randomizing format
for step in workflow_steps[:cutoff]:
    format_type = random.choice(['text', 'xml', 'json'])
    # ... generate log line in chosen format'''
    
    st.code(code_snippet, language='python')
    
    st.markdown("""
    📁 **View Full Implementation:**
    - <a href="https://github.com/hilel/Interactive-RCA-Pipeline-Tutorial/blob/main/utils/data_generator.py" target="_blank">utils/data_generator.py</a> - Complete synthetic log generation
    """, unsafe_allow_html=True)
    
    # Technical Deep Dive
    render_step1_explanation()
    
    num_orders = st.slider("Number of Orders to Simulate", 10, 500, 100, help="More orders = better training data, but slower processing.")
    
    if st.button("Generate Logs", help="Click to run the simulation engine."):
        with st.spinner("Generating logs..."):
            st.session_state.raw_logs = st.session_state.facade.generate_synthetic_logs(num_orders=num_orders)
            time.sleep(0.5)
            st.success(f"Generated {len(st.session_state.raw_logs)} log lines.")
    
    if st.session_state.raw_logs:
        st.subheader("Raw Log Preview")
        st.text_area("Logs", "\n".join(st.session_state.raw_logs[:20]) + "\n...", height=300)
        
        if st.button("Next: Run ETL"):
            st.session_state.current_step = 2
            st.rerun()
