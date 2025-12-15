# Project Stressed: Automated Root Cause Analysis Pipeline

## Overview

Project Stressed is an automated root cause analysis system that converts messy, unstructured logs into actionable insights using deep learning.

## Project Structure

```
Stressed Pipeline/
├── main.py                    # Main execution script
├── stressed.py                # Original monolithic implementation (kept for reference)
├── requirements.txt           # Python dependencies
│
├── models/                    # Data models and neural networks
│   ├── __init__.py
│   ├── schema.py             # Pydantic schema definitions
│   └── lstm_model.py         # LSTM neural network implementation
│
├── parsers/                   # Log parsing components
│   ├── __init__.py
│   └── log_parser.py         # Log parsing agent
│
├── utils/                     # Utility functions
│   ├── __init__.py
│   └── data_generator.py     # Synthetic log data generator
│
└── pipeline/                  # Pipeline orchestration
    ├── __init__.py
    └── orchestrator.py       # Main pipeline coordinator

```

## Architecture

The system follows a 5-stage ETL-A pipeline:

1. **Ingestion**: Generate/load messy logs
2. **Parsing**: Convert unstructured text to structured events
3. **Sessionization**: Group events into user journeys
4. **Vectorization**: Convert text to numerical sequences
5. **Analysis**: Train LSTM model and generate insights

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run the complete pipeline:

```bash
python main.py
```

### Run the original monolithic version:

```bash
python stressed.py
```

## Key Components

### Models (`models/`)
- **schema.py**: Defines `StructuredLogEvent` Pydantic model
- **lstm_model.py**: Implements `RCA_LSTM` neural network

### Parsers (`parsers/`)
- **log_parser.py**: `LogParserAgent` extracts structured data from messy logs

### Utils (`utils/`)
- **data_generator.py**: Generates synthetic log data for testing

### Pipeline (`pipeline/`)
- **orchestrator.py**: `ProjectStressedPipeline` coordinates all stages

## Features

- ✅ Handles mixed log formats (Text, XML, JSON)
- ✅ LSTM-based sequence analysis
- ✅ Automated failure clustering
- ✅ Detailed trace reports
- ✅ Root cause identification

## Output

The pipeline generates three types of reports:

1. **System Internals**: Vocabulary mapping (Event → ID)
2. **Order Deep Dive**: Step-by-step trace of specific orders
3. **Root Cause Report**: Aggregated failure analysis with AI insights

## Next Steps

- Integrate real LLM for parsing (uncomment `outlines` in requirements.txt)
- Connect to production ELK/SQL data sources
- Deploy with Docker for GPU acceleration
- Implement weekly model retraining

## License

Internal use only - Senior ML/AI Specialist
