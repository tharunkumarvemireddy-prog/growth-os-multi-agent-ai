# Interview Architecture

```text
                         CLIENT PORTAL
                              |
                         Streamlit UI
                              |
                         Flask REST API
                              |
                       LangGraph Router
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
      CONTENT MARKETING  PERSONAL BRANDING  LEAD GENERATION
          |                  |                  |
      +---+---+          +---+---+          +---+---+
      |       |          |       |          |       |
 Strategy   Creation    Brand   Personal  Lead    Lead
 Research  Distribution Strategy Content  Research Engagement
      |       |          |       |          |       |
      +-------+----------+-------+----------+-------+
                              |
                         Shared RAG
                              |
                       Review / Guardrails
                              |
                       HUMAN APPROVAL
                              |
                    External execution layer
                    LinkedIn / Email / CRM
```

## Important design

The six agents are business capabilities. They are not created per client.

A client changes:
- industry
- audience
- brand voice
- business goal
- selected services
- client knowledge
- compliance rules
- available tools

The same agents therefore work for manufacturing, fintech, healthcare, SaaS,
real estate or another domain.

## Why RAG is shared

RAG supplies client-specific knowledge to whichever service is running.
The client_id filter prevents cross-client retrieval.

## Why HITL is shared

The final external action is paused until a human approves it. This is useful
for publishing, outreach and other actions where an incorrect AI action could
affect the client.
