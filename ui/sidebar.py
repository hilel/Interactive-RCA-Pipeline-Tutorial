import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🎓 Project Stressed")
        st.markdown("### Automated Root Cause Analysis (RCA)")
        st.info(
            "**Goal:** Automatically find out *why* a system is failing by looking at logs, "
            "without human intervention."
        )
        
        st.markdown("---")
        st.markdown("### 📚 The Big Picture")
        st.markdown("""
        1. **Logs are Messy**: Systems output text, XML, JSON.
        2. **Structure is Key**: We need to convert mess -> tables.
        3. **Context Matters**: A single log means nothing. A *sequence* of logs tells a story.
        4. **AI Pattern Matching**: Neural Networks (LSTMs) learn what a "good" story looks like.
        5. **Anomaly Detection**: Anything that doesn't look like a "good" story is a bug.
        """)
        
        st.markdown("---")
        st.markdown("### 🔗 Resources")
        st.markdown("- [What is RCA?](https://en.wikipedia.org/wiki/Root_cause_analysis)")
        st.markdown("- [LSTM Networks Explained](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)")
        st.markdown("- [Streamlit Documentation](https://docs.streamlit.io/)")
