import streamlit as st
import pandas as pd
import plotly.express as px
from ui.educational_content import get_step6_education

def render_step6():
    st.header("Step 6: Analysis & Insights")
    
    with st.expander("📘 Learn More: Root Cause Analysis", expanded=True):
        st.markdown(get_step6_education(), unsafe_allow_html=True)
    
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

    if st.button("Restart Analysis"):
        st.session_state.current_step = 1
        st.session_state.raw_logs = []
        st.session_state.df_events = None
        st.session_state.df_sessions = None
        st.session_state.df_ready = None
        st.session_state.training_complete = False
        st.rerun()
