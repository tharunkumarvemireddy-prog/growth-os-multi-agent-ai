# Deployment

## Architecture

Streamlit Community Cloud hosts the UI.

Render hosts the Flask API.

```text
Browser
  |
  v
Streamlit
  |
  | HTTPS
  v
Flask API on Render
  |
  v
LangGraph
  |
  +-- 6 reusable business agents
  +-- Chroma RAG
  +-- Review
  +-- Human approval
  +-- LangSmith tracing
```

## Render

Connect this GitHub repository to Render as a Web Service.

Build:

```text
pip install -r requirements.txt
```

Start:

```text
gunicorn app:app
```

Add:
- OPENAI_API_KEY
- TAVILY_API_KEY
- LANGSMITH_TRACING=true
- LANGSMITH_API_KEY
- LANGSMITH_PROJECT=growth-os
- MODEL_NAME=gpt-4o-mini
- TEMPERATURE=0.4

After deployment, test:

```text
https://YOUR-RENDER-URL/health
```

Expected:

```json
{"service":"growth-os-api","status":"ok"}
```

## Streamlit Community Cloud

Use:

```text
streamlit_app.py
```

as the entrypoint.

Add a Streamlit secret:

```toml
API_URL = "https://YOUR-RENDER-URL"
```

The frontend will then call the Render API.

## Important

Do not put API keys into GitHub.

Use Render environment variables and Streamlit secrets.
