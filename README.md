# SHL Assessment Recommendation System

## Overview

This project implements an AI-powered SHL Assessment Recommendation System that recommends the most relevant SHL assessments from natural language queries or job descriptions.

The system combines semantic retrieval, conversation memory, rule-based filtering, and a Large Language Model (Google Gemini) to provide accurate recommendations while ensuring that only assessments available in the SHL Product Catalog are returned.

---

## Features

- Natural language assessment recommendation
- Semantic search using Sentence Transformers
- FAISS vector similarity search
- Multi-turn conversation support
- Clarification questions for ambiguous queries
- Assessment comparison
- Prompt injection protection
- FastAPI REST API
- Interactive Swagger documentation

---

## Technology Stack

- Python
- FastAPI
- Google Gemini
- Sentence Transformers
- FAISS
- NumPy
- Pydantic

---

## Project Structure

```text
app/
    api.py
    chatbot.py
    clarification.py
    config.py
    guardrails.py
    llm.py
    main.py
    memory.py
    models.py
    recommendation.py
    retriever.py
    utils.py

vector_store/
    metadata.pkl
    shl.index

tests/

catalog.json

requirements.txt

README.md
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd shl-ai-recommender
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
GEMINI_API_KEY=YOUR_API_KEY
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

# API

## Health Check

```
GET /health
```

Example Response

```json
{
  "status": "ok"
}
```

---

## Recommendation Endpoint

```
POST /chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Senior Java Developer"
    }
  ]
}
```

Example Response

```json
{
  "response": "...",
  "recommendations": [
    {
      "name": "Core Java (Advanced Level) (New)",
      "url": "...",
      "reason": "Suitable for Knowledge & Skills"
    }
  ],
  "needs_clarification": false
}
```

---

## Approach

The recommendation pipeline consists of the following stages:

1. Validate the user query using guardrails.
2. Detect whether clarification is required.
3. Retrieve relevant assessments using semantic search.
4. Apply keyword-based re-ranking.
5. Prioritize assessments based on detected role and experience level.
6. Generate the final response using Google Gemini while restricting responses to retrieved SHL catalog entries.
7. Return recommendations in JSON format.

---

## Evaluation

The system was evaluated using representative SHL recommendation queries, including:

- Java Developer
- Python Developer
- Graduate Sales
- Assessment comparison
- Prompt injection attempts
- Multi-turn conversations

The implementation supports the evaluation methodology described in the SHL assignment (Recall@K and MAP@K) and is designed to recommend up to 10 relevant assessments from the SHL Product Catalog. :contentReference[oaicite:1]{index=1}

---

## Deliverables

- FastAPI REST API
- JSON Recommendation Endpoint
- SHL Assessment Recommendation Engine
- GitHub Repository
- Interactive Swagger Documentation
