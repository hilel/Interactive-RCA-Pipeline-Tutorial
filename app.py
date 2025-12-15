import streamlit as st
import pandas as pd
import plotly.express as px
from pipeline.facade import StressedPipelineFacade
import time

# Page Config
st.set_page_config(
    page_title="Project Stressed - RCA Education",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for Stepper and Educational Elements
st.markdown("""
<style>
    .step-container {
        display: flex;
        justify_content: space-between;
        margin-bottom: 20px;
    }
    .step {
        background-color: #f0f2f6;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        color: #31333F;
        flex: 1;
        text-align: center;
        margin: 0 5px;
    }
    .step.active {
        background-color: #ff4b4b;
        color: white;
    }
    .step.completed {
        background-color: #d1d5db;
        color: #31333F;
    }
    .educational-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00a8e8;
        margin-bottom: 15px;
        color: #1a1a1a;
    }
    .key-concept {
        background-color: #fff4e6;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
        color: #1a1a1a;
    }
    .tech-detail {
        background-color: #f3e5f5;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #9c27b0;
        margin: 10px 0;
        color: #1a1a1a;
    }
    .analogy-box {
        background-color: #e8f5e9;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
        font-style: italic;
        color: #1a1a1a;
    }
    .challenge-box {
        background-color: #ffebee;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
        color: #1a1a1a;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    if 'facade' not in st.session_state:
        st.session_state.facade = StressedPipelineFacade()
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'raw_logs' not in st.session_state:
        st.session_state.raw_logs = []
    if 'df_events' not in st.session_state:
        st.session_state.df_events = None
    if 'df_sessions' not in st.session_state:
        st.session_state.df_sessions = None
    if 'df_ready' not in st.session_state:
        st.session_state.df_ready = None
    if 'training_complete' not in st.session_state:
        st.session_state.training_complete = False

def render_stepper():
    steps = ["1. Generate Logs", "2. ETL", "3. Sessionize", "4. Vectorize", "5. Train Model", "6. Analysis"]
    
    html = '<div class="step-container">'
    for i, step in enumerate(steps, 1):
        status = "active" if i == st.session_state.current_step else "completed" if i < st.session_state.current_step else ""
        html += f'<div class="step {status}">{step}</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

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

def main():
    init_session_state()
    render_sidebar()
    
    st.title("🎓 Interactive RCA Pipeline")
    st.markdown("Follow the journey of data from raw chaos to actionable insights.")
    
    render_stepper()
    
    # --- STEP 1: GENERATE LOGS ---
    if st.session_state.current_step == 1:
        st.header("Step 1: Generate Synthetic Logs")
        
        with st.expander("📘 Learn More: Why Synthetic Data?", expanded=True):
            st.markdown("""
            <div class="key-concept">
            <strong>🎯 What is this?</strong><br>
            In the real world, you would pull logs from <strong>Splunk</strong>, <strong>Datadog</strong>, or plain text files. 
            Here, we use a <strong>Generator</strong> to create fake data that looks exactly like a messy legacy system.
            </div>
            
            <div class="tech-detail">
            <strong>🔧 Why do we need it?</strong>
            <ul>
                <li><strong>Safe Testing:</strong> Test our pipeline without needing access to production servers or risking real data.</li>
                <li><strong>Controlled Chaos:</strong> Deliberately inject "bugs" (failed transactions) to see if our AI finds them.</li>
                <li><strong>Reproducibility:</strong> Same input = same output. Essential for debugging and education.</li>
            </ul>
            </div>
            
            <div class="analogy-box">
            <strong>💡 Real-World Analogy:</strong><br>
            Think of this like a flight simulator for pilots. You wouldn't want to learn how to handle emergencies 
            in a real plane! Similarly, we practice RCA on synthetic logs before deploying to production.
            </div>
            
            <div class="challenge-box">
            <strong>⚠️ The Challenge:</strong><br>
            Notice how the logs are a mix of <code>[INFO]</code> text, <code>XML</code> tags, and <code>JSON</code> objects. 
            This is called <strong>Unstructured Data</strong> - the nightmare of every data engineer! Our ETL pipeline 
            must handle ALL these formats simultaneously.
            </div>
            """, unsafe_allow_html=True)
        
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

    # --- STEP 2: ETL ---
    elif st.session_state.current_step == 2:
        st.header("Step 2: Extract, Transform, Load (ETL)")
        
        with st.expander("📘 Learn More: The ETL Process", expanded=True):
            st.markdown("""
            <div class="key-concept">
            <strong>🎯 ETL: The Foundation of Data Engineering</strong><br>
            ETL stands for <strong>Extract, Transform, Load</strong> - the process of converting chaos into order.
            </div>
            
            <div class="tech-detail">
            <strong>📥 E (Extract):</strong> Read the raw text lines from various sources.<br>
            <ul>
                <li>In production: Tails log files, queries databases, calls APIs</li>
                <li>Here: Processes our synthetic log strings</li>
            </ul>
            
            <strong>🔄 T (Transform):</strong> Use <strong>Regex (Regular Expressions)</strong> to find patterns.<br>
            <ul>
                <li><strong>Goal:</strong> Extract <code>Timestamp</code>, <code>Order ID</code>, and <code>Event Name</code></li>
                <li><strong>Technique:</strong> Pattern matching with expressions like <code>\\[INFO\\].*order_id=(\\d+)</code></li>
                <li><strong>Challenge:</strong> Handling XML, JSON, and plain text formats in a single pass</li>
            </ul>
            
            <strong>📊 L (Load):</strong> Store clean data in a Pandas DataFrame (think Excel on steroids).<br>
            <ul>
                <li>Enables fast queries and analysis</li>
                <li>Standardizes column names and data types</li>
                <li>Prepares data for the next pipeline stage</li>
            </ul>
            </div>
            
            <div class="analogy-box">
            <strong>💡 Real-World Analogy:</strong><br>
            Imagine receiving mail from 100 countries, each with different address formats. ETL is like having 
            a smart sorting system that can read any format and organize everything into a standard filing cabinet.
            </div>
            """, unsafe_allow_html=True)
            st.info("💡 **Interactive Tip:** Look at the 'Event Name' column below. It's clean text, unlike the raw logs. This is the power of transformation!")
        
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

    # --- STEP 3: SESSIONIZE ---
    elif st.session_state.current_step == 3:
        st.header("Step 3: Sessionization")
        
        with st.expander("📘 Learn More: What is a Session?", expanded=True):
            st.markdown("""
            <div class="challenge-box">
            <strong>❓ The Problem:</strong><br>
            The ETL table is just a flat list of events. It doesn't tell us <em>who</em> did <em>what</em> in <em>what order</em>.
            Without context, a single event like "Payment Failed" is meaningless. Did the user even log in first?
            </div>
            
            <div class="key-concept">
            <strong>🎯 The Solution: Sessionization</strong><br>
            We group all related events together using a common identifier (<code>Order ID</code> in our case).
            This creates a <strong>temporal sequence</strong> - a story with a beginning, middle, and end.
            </div>
            
            <div class="tech-detail">
            <strong>🔧 Technical Implementation:</strong><br>
            <ul>
                <li><strong>Group By:</strong> SQL-style operation - <code>GROUP BY order_id</code></li>
                <li><strong>Sorting:</strong> Within each group, sort by timestamp (chronological order)</li>
                <li><strong>Aggregation:</strong> Collect all event names into a list/sequence</li>
                <li><strong>Labeling:</strong> Mark session as SUCCESS or FAILURE based on final event</li>
            </ul>
            </div>
            
            <div class="analogy-box">
            <strong>💡 Visual Analogy:</strong><br>
            Imagine a mixed-up pile of photos from 10 different vacations, all in one box. 
            <strong>Sessionization</strong> is like sorting them into 10 separate photo albums (one per vacation), 
            then arranging each album's photos chronologically. Now each album tells a coherent story!
            </div>
            
            <div class="educational-box">
            <strong>🎓 Why This Matters for AI:</strong><br>
            Machine learning algorithms (especially LSTMs) need <strong>sequences</strong> to learn patterns. 
            A random list of events has no predictive power. But a sequence like:<br>
            <code>[Login → Auth → Dashboard → Checkout → Payment]</code><br>
            teaches the AI what a "successful journey" looks like.
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Sessionize Data", help="Group events by Order ID."):
            with st.spinner("Grouping events..."):
                st.session_state.df_sessions = st.session_state.facade.create_sessions(st.session_state.df_events)
                st.success(f"Created {len(st.session_state.df_sessions)} user sessions.")
        
        if st.session_state.df_sessions is not None:
            st.subheader("User Journeys")
            st.dataframe(st.session_state.df_sessions[['order_id', 'event_name', 'label']].head(20))
            
            if st.button("Next: Vectorize"):
                st.session_state.current_step = 4
                st.rerun()

    # --- STEP 4: VECTORIZE ---
    elif st.session_state.current_step == 4:
        st.header("Step 4: Vectorization")
        
        with st.expander("📘 Learn More: Computers Don't Read English", expanded=True):
            st.markdown("""
            <div class="key-concept">
            <strong>🎯 The Core Problem:</strong><br>
            Neural Networks are mathematical engines. They operate on <strong>matrices of numbers</strong>, not text strings. 
            We must bridge the gap between human language ("Screen_Login") and machine mathematics (the number 2).
            </div>
            
            <div class="tech-detail">
            <strong>🔧 Step 1: Tokenization</strong><br>
            We create a <strong>vocabulary dictionary</strong> where every unique event gets a unique integer ID.<br>
            <ul>
                <li><code>PAD</code> (padding) → <code>0</code> (reserved for empty space)</li>
                <li><code>UNKNOWN</code> → <code>1</code> (reserved for new events)</li>
                <li><code>Screen_Login</code> → <code>2</code></li>
                <li><code>UseCase_Auth</code> → <code>5</code></li>
                <li><code>Screen_Dashboard</code> → <code>7</code></li>
            </ul>
            This is called <strong>Integer Encoding</strong> or <strong>Label Encoding</strong>.
            </div>
            
            <div class="tech-detail">
            <strong>🔧 Step 2: Sequence Encoding</strong><br>
            Convert entire sessions from text lists to integer lists:<br>
            <code>["Screen_Login", "UseCase_Auth", "Screen_Dashboard"]</code><br>
            becomes<br>
            <code>[2, 5, 7]</code>
            </div>
            
            <div class="tech-detail">
            <strong>🔧 Step 3: Padding</strong><br>
            Neural networks require <strong>fixed-length inputs</strong> (like fixed-size images).<br>
            <ul>
                <li><strong>Problem:</strong> Some sessions have 5 events, others have 15</li>
                <li><strong>Solution:</strong> Pick a max length (e.g., 20) and pad short sequences with <code>0</code>s</li>
                <li><strong>Example:</strong> <code>[2, 5, 7]</code> → <code>[2, 5, 7, 0, 0, 0, ..., 0]</code> (20 total)</li>
            </ul>
            </div>
            
            <div class="analogy-box">
            <strong>💡 Real-World Analogy:</strong><br>
            Think of a music playlist. Spotify doesn't store song names as text - it uses numeric IDs. 
            "Bohemian Rhapsody" might be ID 123456. Your playlist <code>[123456, 789012, 345678]</code> is 
            efficiently stored and processed, just like our event sequences!
            </div>
            
            <div class="educational-box">
            <strong>🎓 Advanced Concept: Word Embeddings</strong><br>
            Later, these integers become <strong>dense vectors</strong> (e.g., 128 floating-point numbers) through an 
            <strong>Embedding Layer</strong>. This allows the AI to learn that "Login" and "Authentication" are semantically similar.
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Prepare Vectors", help="Convert text lists to integer lists."):
            with st.spinner("Encoding sequences..."):
                st.session_state.df_ready = st.session_state.facade.vectorize_sessions(st.session_state.df_sessions)
                st.success("Vectorization complete.")
        
        if st.session_state.df_ready is not None:
            st.subheader("Deep Dive: Text vs. Numbers")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Human Readable (Text)**")
                st.write(st.session_state.df_ready['event_name'].iloc[0])
            with col2:
                st.markdown("**Machine Readable (Vector)**")
                st.write(st.session_state.df_ready['encoded'].iloc[0])
            
            st.subheader("Vocabulary Map")
            vocab = st.session_state.facade.get_vocabulary()
            st.json(vocab)
            
            if st.button("Next: Train Model"):
                st.session_state.current_step = 5
                st.rerun()

    # --- STEP 5: TRAIN MODEL ---
    elif st.session_state.current_step == 5:
        st.header("Step 5: Train LSTM Model")
        
        with st.expander("📘 Learn More: The Brain (LSTM)", expanded=True):
            st.markdown("""
            <div class="key-concept">
            <strong>🧠 LSTM (Long Short-Term Memory)</strong><br>
            A specialized type of <strong>Recurrent Neural Network (RNN)</strong> designed specifically for sequential data. 
            Unlike traditional neural networks that treat each input independently, LSTMs <strong>remember context</strong> 
            from earlier in the sequence.
            </div>
            
            <div class="tech-detail">
            <strong>🔧 Why LSTM? (Not just a regular neural network)</strong><br>
            <ul>
                <li><strong>Memory Cells:</strong> Internal state that carries information across time steps</li>
                <li><strong>Gates:</strong> Forget Gate, Input Gate, Output Gate - control what information to keep/discard</li>
                <li><strong>Vanishing Gradient Solution:</strong> Can learn long-term dependencies (e.g., event 1 affecting event 15)</li>
                <li><strong>Perfect for:</strong> Text, time series, logs, DNA sequences, music</li>
            </ul>
            </div>
            
            <div class="tech-detail">
            <strong>🎓 The Training Process (Supervised Learning):</strong><br>
            <ol>
                <li><strong>Forward Pass:</strong> Show the model a sequence → <code>[Login, Auth, Dashboard, ...]</code></li>
                <li><strong>Label:</strong> Tell it the ground truth → <code>Success (1)</code> or <code>Failure (0)</code></li>
                <li><strong>Prediction:</strong> Model outputs its guess → e.g., <code>0.92</code> (92% confident it's success)</li>
                <li><strong>Loss Calculation:</strong> Measure error using Binary Cross-Entropy:<br>
                    <code>Loss = -[y*log(ŷ) + (1-y)*log(1-ŷ)]</code></li>
                <li><strong>Backward Pass:</strong> Calculate gradients (how much each weight contributed to the error)</li>
                <li><strong>Update Weights:</strong> Use <strong>Adam Optimizer</strong> to adjust weights in the direction that reduces loss</li>
            </ol>
            </div>
            
            <div class="key-concept">
            <strong>📈 Key Training Terms:</strong><br>
            <ul>
                <li><strong>Epoch:</strong> One complete pass through the entire dataset</li>
                <li><strong>Batch:</strong> A subset of data processed together (e.g., 32 sequences at once)</li>
                <li><strong>Learning Rate:</strong> How big the weight update steps are (too big = unstable, too small = slow)</li>
                <li><strong>Validation Split:</strong> Hold out 20% of data to test if the model is overfitting</li>
            </ul>
            </div>
            
            <div class="analogy-box">
            <strong>💡 Learning Analogy:</strong><br>
            Imagine teaching a child to recognize dangerous situations:<br>
            <strong>You:</strong> "If you see [Dark Alley] → [Stranger Approaching] → [Offering Candy], run away!"<br>
            <strong>Child:</strong> Guesses "Safe" (wrong!)<br>
            <strong>You:</strong> "No, that's dangerous! Remember the pattern."<br>
            After 10 examples (<em>epochs</em>), the child learns the pattern. That's supervised learning!
            </div>
            
            <div class="educational-box">
            <strong>🎯 What the Model Learns:</strong><br>
            The LSTM learns the <strong>"Happy Path"</strong> - the typical sequence of events that leads to success. 
            Anything that deviates significantly (e.g., skips authentication, unexpected error events) will have a 
            <strong>high anomaly score</strong>, flagging it for investigation.
            </div>
            
            <div class="challenge-box">
            <strong>⚠️ VERY IMPORTANT: The Labeling Problem</strong><br>
            Our current approach uses <strong>supervised learning</strong> - we tell the AI which orders succeeded and which failed. 
            But in production with truly messy logs:<br>
            <ul>
                <li><strong>Problem 1:</strong> You often don't have labeled failures (who manually labels millions of logs?)</li>
                <li><strong>Problem 2:</strong> Unknown failure modes won't be detected (the AI only knows failures it was trained on)</li>
                <li><strong>Problem 3:</strong> New bugs look like nothing you've seen before (zero-day failures)</li>
            </ul>
            <strong>📌 This is a critical limitation for real-world deployment!</strong>
            </div>
            
            <div class="tech-detail">
            <strong>🔧 Production Solution: Unsupervised Learning (Autoencoder-LSTM)</strong><br>
            For real messy logs without labels, use this approach:<br>
            <ul>
                <li><strong>Step 1:</strong> Train LSTM to <strong>predict the next event</strong> in a sequence (self-supervised)</li>
                <li><strong>Step 2:</strong> Feed it <strong>only successful logs</strong> (the "happy path" - easier to identify)</li>
                <li><strong>Step 3:</strong> In production, measure <strong>prediction error / reconstruction loss</strong></li>
                <li><strong>Step 4:</strong> High error = sequence doesn't match normal patterns = <strong>ANOMALY 🚨</strong></li>
            </ul>
            <strong>Example in Action:</strong><br>
            ✅ Normal: <code>[Login → Auth → Dashboard → Checkout → Payment]</code> → Low error (0.05) → No alert<br>
            🚨 Anomaly: <code>[Login → Dashboard → Error_500]</code> → High error (0.85) → <strong>ALERT! Investigate!</strong>
            </div>
            
            <div class="educational-box">
            <strong>📊 Supervised vs. Unsupervised Comparison:</strong><br>
            <table style="width:100%; border-collapse: collapse; margin-top: 10px; color: #1a1a1a;">
                <tr style="background-color: #d0d0d0;">
                    <th style="padding: 8px; border: 1px solid #999;">Approach</th>
                    <th style="padding: 8px; border: 1px solid #999;">Needs Labels?</th>
                    <th style="padding: 8px; border: 1px solid #999;">Detects Unknown Bugs?</th>
                    <th style="padding: 8px; border: 1px solid #999;">Best Use Case</th>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #999;"><strong>Supervised (Our Demo)</strong></td>
                    <td style="padding: 8px; border: 1px solid #999;">✅ Yes (SUCCESS/FAILURE)</td>
                    <td style="padding: 8px; border: 1px solid #999;">❌ No</td>
                    <td style="padding: 8px; border: 1px solid #999;">Educational, Controlled Tests</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #999;"><strong>Unsupervised (Autoencoder)</strong></td>
                    <td style="padding: 8px; border: 1px solid #999;">❌ No</td>
                    <td style="padding: 8px; border: 1px solid #999;">✅ Yes</td>
                    <td style="padding: 8px; border: 1px solid #999;">Production, Real Messy Logs</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #999;"><strong>Semi-Supervised (Hybrid)</strong></td>
                    <td style="padding: 8px; border: 1px solid #999;">⚠️ Partial (Success only)</td>
                    <td style="padding: 8px; border: 1px solid #999;">✅ Yes</td>
                    <td style="padding: 8px; border: 1px solid #999;">Best of Both Worlds</td>
                </tr>
            </table>
            <br>
            <strong>💡 Key Takeaway:</strong> This demo uses supervised learning for <em>educational clarity</em>. 
            In production, you'd implement an <strong>unsupervised autoencoder</strong> that learns normal patterns 
            and flags anything unusual, even if it's never seen that failure before!
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Train Model", help="Start the neural network training loop."):
            with st.spinner("Training in progress..."):
                st.session_state.facade.train_model(st.session_state.df_ready)
                st.session_state.training_complete = True
            
            st.success("Training Complete! The model now understands the 'Happy Path'.")
            
        if st.session_state.training_complete:
            if st.button("Next: Analysis & Insights"):
                st.session_state.current_step = 6
                st.rerun()

    # --- STEP 6: ANALYSIS ---
    elif st.session_state.current_step == 6:
        st.header("Step 6: Analysis & Insights")
        
        with st.expander("📘 Learn More: Root Cause Analysis", expanded=True):
            st.markdown("""
            <div class="key-concept">
            <strong>🎯 The Ultimate Goal: Finding the Smoking Gun</strong><br>
            After all the data processing and model training, we finally answer the question: 
            <strong>"Why are orders failing?"</strong> This is where data science meets real-world impact.
            </div>
            
            <div class="tech-detail">
            <strong>🔍 Analysis Methodology:</strong><br>
            <ol>
                <li><strong>Failure Aggregation:</strong> Group all failed sessions together</li>
                <li><strong>Pattern Detection:</strong> Identify the <strong>last successful step</strong> before failure</li>
                <li><strong>Statistical Analysis:</strong> Count frequency of each failure point</li>
                <li><strong>Root Cause Hypothesis:</strong> The most common failure point = likely culprit</li>
            </ol>
            </div>
            
            <div class="analogy-box">
            <strong>💡 Detective Analogy:</strong><br>
            Imagine 100 car accidents all happening at the same intersection. You don't need to be Sherlock Holmes 
            to realize there's probably a broken traffic light at that spot! Similarly, if 90% of order failures 
            happen right after <code>UseCase_AuthUser</code>, the Auth Service is likely broken.
            </div>
            
            <div class="educational-box">
            <strong>📊 What You'll See Below:</strong><br>
            <ul>
                <li><strong>Bar Chart:</strong> Visual representation of failure concentration points</li>
                <li><strong>AI Insight:</strong> Automated interpretation of the statistical patterns</li>
                <li><strong>Deep Dive Tool:</strong> Forensic analysis of individual order journeys</li>
            </ul>
            This transforms raw data into <strong>actionable intelligence</strong> for DevOps teams.
            </div>
            """, unsafe_allow_html=True)
        
        # 1. Failure Analysis
        st.subheader("📊 Root Cause Aggregation")
        
        st.markdown("""
        <div class="tech-detail">
        <strong>🔧 How This Works:</strong><br>
        <ol>
            <li><strong>Filter Failures:</strong> Select only sessions where <code>label == 0</code> (failure)</li>
            <li><strong>Extract Last Success:</strong> For each failed session, find the last event that executed successfully</li>
            <li><strong>Group & Count:</strong> Aggregate failures by their last successful step using <code>GROUP BY</code></li>
            <li><strong>Sort by Frequency:</strong> Rank failure points from most to least common</li>
        </ol>
        The resulting chart shows <strong>failure concentration</strong> - where the system is hemorrhaging orders.
        </div>
        """, unsafe_allow_html=True)
        
        breakdown = st.session_state.facade.get_failure_stats(st.session_state.df_ready)
        
        if not breakdown.empty:
            # Option to show all events or top 5
            show_all = st.checkbox("Show all events (with horizontal scroll)", value=False)
            
            if show_all:
                # Show all events with horizontal scroll
                chart_data = breakdown
                # Create distinct colors for each event
                colors = px.colors.qualitative.Plotly + px.colors.qualitative.Set3
                color_map = {event: colors[i % len(colors)] for i, event in enumerate(chart_data['Last Successful Step'])}
                
                fig = px.bar(chart_data, 
                            x='Last Successful Step', 
                            y='Count',
                            title=f"Where are orders failing? (All {len(chart_data)} events)",
                            color='Last Successful Step',
                            color_discrete_map=color_map,
                            labels={'Count': 'Number of Failures'},
                            hover_data=['Percentage'])
                
                # Enable horizontal scrolling by setting fixed width
                fig.update_layout(
                    xaxis={'categoryorder': 'total descending'},
                    width=max(800, len(chart_data) * 80),  # Dynamic width based on number of events
                    height=500,
                    showlegend=False,
                    xaxis_tickangle=-45
                )
                
                # Display with horizontal scroll
                st.plotly_chart(fig, use_container_width=False)
            else:
                # Show top 5 most common events with distinct colors
                top_n = min(5, len(breakdown))
                chart_data = breakdown.head(top_n)
                
                # Create distinct colors for each event
                colors = ['#FF4B4B', '#FF8C42', '#FFA07A', '#FFB6C1', '#FFD700']
                color_map = {event: colors[i] for i, event in enumerate(chart_data['Last Successful Step'])}
                
                fig = px.bar(chart_data, 
                            x='Last Successful Step', 
                            y='Count',
                            title=f"Where are orders failing? (Top {top_n} events)",
                            color='Last Successful Step',
                            color_discrete_map=color_map,
                            labels={'Count': 'Number of Failures'},
                            hover_data=['Percentage'])
                
                fig.update_layout(
                    xaxis={'categoryorder': 'total descending'},
                    showlegend=True,
                    xaxis_tickangle=-45,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Show summary statistics
            st.markdown("### 📋 Failure Distribution Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Failed Orders", breakdown['Count'].sum())
            with col2:
                st.metric("Unique Failure Points", len(breakdown))
            with col3:
                st.metric("Most Common Failure", f"{breakdown.iloc[0]['Percentage']:.1f}%")
            
            # Show detailed breakdown table
            with st.expander("📊 View Detailed Breakdown Table"):
                st.dataframe(breakdown, use_container_width=True)
            
            st.markdown("""
            <div class="educational-box">
            <strong>📈 Reading the Chart:</strong><br>
            <ul>
                <li><strong>X-Axis:</strong> The last step that completed successfully before the order failed</li>
                <li><strong>Y-Axis:</strong> Number of failures at that point</li>
                <li><strong>Color Intensity:</strong> Darker red = more failures (hotter problem)</li>
                <li><strong>Tallest Bar:</strong> Your #1 suspect - investigate this component first!</li>
            </ul>
            <strong>Real-World Action:</strong> DevOps would immediately check logs, server health, and recent deployments 
            for the service corresponding to the tallest bar.
            </div>
            """, unsafe_allow_html=True)
            
            # Insights
            st.markdown("### 💡 AI-Powered Insight")
            
            st.markdown("""
            <div class="tech-detail">
            <strong>🤖 How AI Insight Works:</strong><br>
            The system analyzes the statistical distribution and applies business logic:<br>
            <ul>
                <li><strong>Critical (🔴):</strong> >50% of failures at one point = systemic issue</li>
                <li><strong>Warning (🟡):</strong> 30-50% concentration = investigate this component</li>
                <li><strong>Info (🟢):</strong> Distributed failures = no single root cause (or data insufficient)</li>
            </ul>
            This automated triage helps prioritize incident response.
            </div>
            """, unsafe_allow_html=True)
            
            insight = st.session_state.facade.get_ai_insight(breakdown)
            
            if insight['type'] == 'critical':
                st.error(f"**{insight['message']}**")
                st.write(f"Potential Root Cause: {insight['insight']}")
            elif insight['type'] == 'warning':
                st.warning(f"{insight['message']} {insight['insight']}")
            else:
                st.info(insight['message'])
                
        else:
            st.success("✅ No failures detected in this batch! System is healthy.")

        # 2. Deep Dive
        st.markdown("---")
        st.subheader("🔬 Single Order Deep Dive (Forensic Analysis)")
        
        st.markdown("""
        <div class="key-concept">
        <strong>🎯 Forensic Investigation:</strong><br>
        While aggregation shows <em>trends</em>, sometimes you need to examine a <strong>single order's journey</strong> 
        in detail - like reading a patient's medical chart or debugging a specific error in code.
        </div>
        
        <div class="tech-detail">
        <strong>🔧 What This Tool Does:</strong><br>
        <ul>
            <li><strong>End-to-End Trace:</strong> Shows every event the order touched, in chronological order</li>
            <li><strong>Raw Log Context:</strong> Displays the actual log line that generated each event (for debugging)</li>
            <li><strong>Timeline Visualization:</strong> Step-by-step journey with timestamps</li>
            <li><strong>Status Flag:</strong> Instant visual confirmation of success vs. failure</li>
        </ul>
        <strong>Use Case:</strong> When a VIP customer complains their order failed, you can trace exactly what happened.
        </div>
        """, unsafe_allow_html=True)
        
        st.info("👇 Select an order to trace its exact path through the system.")
        order_id = st.selectbox("Select Order ID to Inspect", st.session_state.df_ready['order_id'].unique())
        
        if order_id:
            details = st.session_state.facade.get_order_details(st.session_state.df_ready, order_id)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Order ID", str(details['order_id']))
            with col2:
                status = "✅ SUCCESS" if details['status'] == "SUCCESS" else "❌ FAILURE"
                st.metric("Status", status)
            
            # Timeline Visualization
            st.markdown("""
            <div class="educational-box">
            <strong>📜 Order Timeline:</strong><br>
            Each row represents one event in the order's lifecycle. Read top-to-bottom to see the chronological flow.
            <ul>
                <li><strong>Step:</strong> Sequence number (helps identify where in the journey you are)</li>
                <li><strong>Event:</strong> Clean, human-readable event name (from ETL transformation)</li>
                <li><strong>Raw Log:</strong> Original messy log line (for technical debugging)</li>
            </ul>
            <strong>Pro Tip:</strong> Compare successful orders to failed ones to spot the divergence point!
            </div>
            """, unsafe_allow_html=True)
            
            timeline_data = []
            for i, (evt, r) in enumerate(zip(details['events'], details['raw_logs'])):
                timeline_data.append({"Step": i+1, "Event": evt, "Raw Log": r})
            
            st.table(pd.DataFrame(timeline_data))
            
            # Additional context
            if details['status'] == "FAILURE":
                st.markdown("""
                <div class="challenge-box">
                <strong>🔴 Failure Analysis:</strong><br>
                This order failed. Notice where the sequence stops - that's your failure point. 
                In a real system, you'd now:<br>
                <ol>
                    <li>Check server logs for that timestamp</li>
                    <li>Verify the health of the service that handles this event</li>
                    <li>Look for exceptions, timeouts, or resource exhaustion</li>
                    <li>Check if this correlates with a recent deployment</li>
                </ol>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="analogy-box">
                <strong>✅ Success Pattern:</strong><br>
                This order completed successfully. Use this as a <strong>baseline</strong> to compare against failed orders. 
                The "happy path" is your reference model for how things should work.
                </div>
                """, unsafe_allow_html=True)
            insight = st.session_state.facade.get_ai_insight(breakdown)
            
            if insight['type'] == 'critical':
                st.error(f"**{insight['message']}**")
                st.write(f"Potential Root Cause: {insight['insight']}")
            elif insight['type'] == 'warning':
                st.warning(f"{insight['message']} {insight['insight']}")
            else:
                st.info(insight['message'])
                
        else:
            st.success("✅ No failures detected in this batch! System is healthy.")

        if st.button("Restart Analysis"):
            st.session_state.current_step = 1
            st.session_state.raw_logs = []
            st.session_state.df_events = None
            st.session_state.df_sessions = None
            st.session_state.df_ready = None
            st.session_state.training_complete = False
            st.rerun()

    # --- SUMMARY ACCORDION ---
    st.markdown("---")
    with st.expander("📂 View All Step Results (Summary)"):
        if st.session_state.raw_logs:
            st.markdown("### 1. Raw Logs")
            st.text(f"Total Lines: {len(st.session_state.raw_logs)}")
        
        if st.session_state.df_events is not None:
            st.markdown("### 2. Structured Data")
            st.dataframe(st.session_state.df_events.head())
            
        if st.session_state.df_sessions is not None:
            st.markdown("### 3. Sessionized Data")
            st.dataframe(st.session_state.df_sessions.head())
            
        if st.session_state.df_ready is not None:
            st.markdown("### 4. Vectorized Data")
            st.dataframe(st.session_state.df_ready.head())

if __name__ == "__main__":
    main()
