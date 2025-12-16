def get_step1_education():
    return """
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
"""

def get_step2_education():
    return """
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
"""

def get_step3_education():
    return """
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
"""

def get_step4_education():
    return """
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
"""

def get_step5_education():
    return """
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
"""

def get_step6_education():
    return """
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
"""
