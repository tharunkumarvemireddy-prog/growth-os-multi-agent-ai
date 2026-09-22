# Growth OS - 6 Agent Multi-Agent AI Platform

A practical Growth OS MVP for clients from different industries.

## Business services

Clients can select any combination of:
- Content Marketing
- Personal Branding
- Lead Generation

## Six reusable agents

### Content Marketing
1. Content Strategy & Research Agent
2. Content Creation & Distribution Agent

### Personal Branding
3. Personal Brand Strategy Agent
4. Personal Content Agent

### Lead Generation
5. Lead Research & Qualification Agent
6. Lead Engagement Agent

RAG, guardrails, review and human approval are shared platform capabilities.

## Architecture

```text
Streamlit
    |
    v
Flask REST API
    |
    v
LangGraph Router
    |
    +--> Content Marketing
    |      +--> Strategy/Research Agent
    |      +--> Creation/Distribution Agent
    |
    +--> Personal Branding
    |      +--> Brand Strategy Agent
    |      +--> Personal Content Agent
    |
    +--> Lead Generation
           +--> Research/Qualification Agent
           +--> Engagement Agent
                    |
                    v
              Shared RAG
                    |
                    v
             Review / Guardrails
                    |
                    v
             HUMAN APPROVAL
                    |
                    v
        Publish / CRM / Outreach
```

## Run locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Put API keys in `.env`.

Terminal 1:
```bash
python app.py
```

Terminal 2:
```bash
streamlit run streamlit_app.py
```

## LangSmith

Set:
```text
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
LANGCHAIN_PROJECT=growth-os
```

LangGraph/LangChain calls will then be traceable.

## RAG

The demo uses ChromaDB. Client-specific documents are stored with a client_id
metadata field so one client cannot retrieve another client's knowledge.

For a production system, add document upload, parsing, chunking and embeddings
before inserting documents.

## Human in the loop

The graph uses LangGraph interrupt() before the final external action.
The API resumes the same thread with an approval decision.

## RAGAS

Run:
```bash
python evaluation/ragas_eval.py
```

The evaluation dataset is intentionally small for the demo. A production
evaluation should contain representative questions for each client/domain.

## Production improvements

- PostgreSQL for clients, services, runs and approvals
- Redis + Celery/RQ for background work
- persistent LangGraph checkpointer
- S3/object storage for documents
- OAuth/JWT and tenant-level authorization
- real LinkedIn/email/CRM adapters
- secrets manager
- rate limiting
- audit logs
- automated tests and CI/CD
