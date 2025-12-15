# Architecture Decision Record: Automated Root Cause Analysis

## Project Stressed: Hybrid AI Pipeline for Legacy Order Flows

**Document Status:** ✅ Approved for Prototype  
**Date:** December 5, 2025  
**Author:** Senior ML/AI Specialist  
**Target Stack:** .NET Backend / Angular Frontend / Mixed Legacy Logs

---

## Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Comparative Technology Analysis](#2-comparative-technology-analysis)
3. [Detailed Technical Architecture](#3-detailed-technical-architecture)
4. [Implementation Guide & Code Strategy](#4-implementation-guide--code-strategy)
5. [Operational Maintenance & Risk Mitigation](#5-operational-maintenance--risk-mitigation)
6. ["Day 1" Action Plan](#6-day-1-action-plan)
7. [Conclusion](#7-conclusion)

---

## 1. Executive Summary

### 1.1 The Business Problem

The current order processing system functions as a complex, stateful "assembly line" where orders must traverse a specific sequence of screens (Angular) and backend UseCases (.NET) to reach a successful state (Screen S14).

**Key Challenges:**

- **Visibility Gap:** While we capture logs in ELK, we lack automated insight into why orders fail
- **The Data Barrier:** Logs are "hostile" to analysis—mixed formats (XML, JSON, Text) buried in natural language strings, preventing standard parsing
- **Operational Cost:** Engineers spend hours manually tracing logs to determine if a failure was "User Abandonment" vs. "System Error"

### 1.2 The Proposed Solution

We propose a **Hybrid AI Pipeline** that moves beyond simple keyword searching (Regex) to **Semantic Sequence Analysis**.

- **Layer 1 (The Translator):** Uses Structured Generation (LLMs + Pydantic) to normalize messy logs into clean JSON
- **Layer 2 (The Analyst):** Uses Sequence Modeling (LSTM Neural Networks) to learn the "grammar" of a valid order and detect structural anomalies

### 1.3 Feasibility Verdict

✅ **GO.** The technology stack (`outlines` + PyTorch) is mature enough to handle this local workload without requiring external cloud APIs, ensuring data privacy and low latency.

---
## 2. Comparative Technology Analysis

We evaluated three approaches to solving the "Buried Event" and "Logic Detection" problems.

| Methodology | Handling "Messy" Data | Detecting "Logic" Errors | Maintenance Cost | Verdict |
|-------------|----------------------|-------------------------|------------------|---------|
| **A. Regex / Grok** | ❌ Fail. Requires unique rules for XML, JSON, and Text variations. Extremely brittle. | ❌ None. Cannot track state (New vs. Existing user). | 🔴 High. Constant rule updates required. | ❌ **Reject** |
| **B. RAG (Vector DB)** | ⚠️ Weak. Good at finding text, but struggles to "read" structure or detect missing steps. | ⚠️ Weak. Hallucinates when data is absent (Negative Logic). | 🟢 Low. Easy to setup, but low precision. | ❌ **Reject** |
| **C. Structured Gen + LSTM** | ✅ Excellent. LLM extracts schemas regardless of format. | ✅ Excellent. LSTM has "memory" to track user journey context. | 🟡 Medium. Requires ML model retraining. | ✅ **Recommended** |

---
## 3. Detailed Technical Architecture

The system follows a strict **5-stage ETL-A** (Extract, Transform, Load, Analyze) pipeline.

### Stage 1: Ingestion (The Raw Stream)

- **Source:** ElasticSearch (ELK) or SQL Audits Table
- **Filter Strategy:** Apply a "Pre-Filter" to discard DEBUG or TRACE noise. Only ingest INFO/WARN/ERROR logs related to transaction flows
- **Volume:** Configured to process the previous 24 hours of data in a nightly batch

### Stage 2: The Parser Engine (Structured Generation)

This is the **most innovative component**. Instead of writing code to parse text, we use an LLM constrained by a schema.

- **Technology:** `outlines` library + Qwen2.5-Coder-7B (Quantized)
- **Mechanism:** The LLM reads a messy line like `[INFO] Executing UseCase_Auth...` and forces it into a strict JSON object
- **Outcome:** 100% standardized data, solving the "Buried Event" problem

### Stage 3: Sessionization (Context Builder)

- **Logic:** Group clean events by `Order_ID`
- **Sorting:** Strictly chronological (Time-Series)
- **Labeling:**
  - **Success (1):** Sequence contains `"Screen_S14"`
## 4. Implementation Guide & Code Strategy

### 4.1 Schema Definition (The Contract)

You must define the "Shape" of your data using Pydantic. This is the bridge between your messy logs and the AI.

```python
class StructuredLogEvent(BaseModel):
    timestamp: str
    event_name: str = Field(..., description="The technical UseCase or Screen ID")
    order_id: Optional[int] = Field(..., description="The unique Order ID")
    severity: Literal["INFO", "WARN", "ERROR"]
```

### 4.2 The LSTM Model Topology

The neural network should be **simple but effective**. We do not need a Transformer (like GPT) here; an LSTM is faster and better suited for simple sequence steps.

| Layer | Configuration | Purpose |
|-------|--------------|---------|
| **Embedding Layer** | Vocab Size → 16 dims | Captures relationships (e.g., `AuthSMS` and `AuthEmail` are similar) |
| **LSTM Layer** | Hidden Size 32 | Captures the "Story" of the order |
| **Output Layer** | Sigmoid | Outputs a single probability score (0.0 to 1.0) |

### 4.3 Root Cause Reporting Logic

The model provides the prediction, but the reporting logic explains the "Why".

**Cluster Failures:** Do not report 500 individual errors.

**Aggregation Logic:**
1. Filter all `is_success == 0`
2. Extract the `last_step` for each
3. Group by `last_step`

**Insight Generation:**  
*"40% of failures stopped at `UseCase_CheckDelivery`. Investigate Logistics Service."*
## 5. Operational Maintenance & Risk Mitigation

### 5.1 Context Window Management

**Risk:** A single failed order generates 5,000 log lines (loops/retries), blowing the context window.

**Mitigation:** Implement "Smart Chunking" in Stage 1:
- Discard repeated log lines (deduplication)
- Prioritize logs with `UseCase_` or `Screen_` keywords
- Truncate the middle of massive stack traces, keeping only the header and footer

### 5.2 Model Drift

**Risk:** The application changes (new features added), and the LSTM starts flagging valid new flows as "Anomalies."
## 6. "Day 1" Action Plan

To start this project immediately without boiling the ocean:

### Step-by-Step Implementation

| Step | Action | Deliverable |
|------|--------|------------|
| **1** | **Data Dump** | Extract 1,000 log lines (CSV) covering 50 different Order_IDs from yesterday |
| **2** | **Prototype Parser** | Run the provided Python script (using the Mock Parser mode initially) to verify the Pydantic Schema captures your specific "Buried Events" |
| **3** | **Vocabulary Audit** | Review the generated dictionary. Are `UseCase_Auth` and `UseCase_Authentication` appearing as two different things? (If so, refine the Regex/Schema) |
| **4** | **Pilot Run** | Train the LSTM on this micro-dataset and check if it correctly flags a known failed order |

---

## 7. Conclusion

This architecture transforms **Log Analysis** from a *search problem* (finding a needle in a haystack) to a *pattern recognition problem* (noticing the needle is missing).

### Key Benefits

- **By leveraging Structured Generation**, we solve the data quality issue that plagues legacy systems
- **By leveraging LSTMs**, we solve the complexity issue of stateful order flows

This is a **robust, modern solution** tailored for the specific constraints of your .NET/Angular environment.

---

**Status:** 🚀 Ready for Prototype Implementation  
**Next Review Date:** December 12, 2025
| **Minimum** | 1x NVIDIA GPU (8GB+ VRAM) | For the Parser |
| **Optimization** | 4-bit quantization (`bitsandbytes`) | Fit the 7B parameter LLM into consumer-grade hardware (e.g., RTX 3060 or higher) |

---
Group by last_step.
Insight Generation: "40% of failures stopped at UseCase_CheckDelivery. Investigate Logistics Service."
5. Operational Maintenance & Risk Mitigation
5.1 Context Window Management
Risk: A single failed order generates 5,000 log lines (loops/retries), blowing the context window.
Mitigation: Implement "Smart Chunking" in Stage 1.
Discard repeated log lines (deduplication).
Prioritize logs with UseCase_ or Screen_ keywords.
Truncate the middle of massive stack traces, keeping only the header and footer.
5.2 Model Drift
Risk: The application changes (new features added), and the LSTM starts flagging valid new flows as "Anomalies."
Mitigation: Automated Weekly Retraining.
The pipeline should re-learn the vocabulary and re-train the LSTM weights every Sunday night using the previous week's data. This keeps the AI synchronized with the Codebase.
5.3 Hardware Requirements
Minimum: 1x NVIDIA GPU (8GB+ VRAM) for the Parser.
Optimization: Use 4-bit quantization (bitsandbytes) to fit the 7B parameter LLM into consumer-grade hardware (e.g., RTX 3060 or higher).
6. "Day 1" Action Plan
To start this project immediately without boiling the ocean:
Data Dump: Extract 1,000 log lines (CSV) covering 50 different Order_IDs from yesterday.
Prototype Parser: Run the provided Python script (using the Mock Parser mode initially) to verify the Pydantic Schema captures your specific "Buried Events".
Vocabulary Audit: Review the generated dictionary. Are UseCase_Auth and UseCase_Authentication appearing as two different things? (If so, refine the Regex/Schema).
Pilot Run: Train the LSTM on this micro-dataset and check if it correctly flags a known failed order.
7. Conclusion
This architecture transforms Log Analysis from a search problem (finding a needle in a haystack) to a pattern recognition problem (noticing the needle is missing).
By leveraging Structured Generation, we solve the data quality issue that plagues legacy systems. By leveraging LSTMs, we solve the complexity issue of stateful order flows. This is a robust, modern solution tailored for the specific constraints of your .NET/Angular environment.
