def get_custom_css():
    return """
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
"""
