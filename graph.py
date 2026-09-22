from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command

from state import GrowthState
from tools import web_search, research_query
from rag import kb
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE


llm = (
    ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        api_key=OPENAI_API_KEY,
    )
    if OPENAI_API_KEY
    else None
)


def ask(prompt):
    if not llm:
        return "OPENAI_API_KEY is missing. Add it to .env."
    return llm.invoke(prompt).content


# ---------------------------------------------------------
# SERVICE ROUTER
# ---------------------------------------------------------

def route_services(state: GrowthState):
    services = state["client"].get("services", [])

    agents = []

    if "content_marketing" in services:
        agents += [
            "content_strategy_research",
            "content_creation_distribution",
        ]

    if "personal_branding" in services:
        agents += [
            "brand_strategy",
            "personal_content",
        ]

    if "lead_generation" in services:
        agents += [
            "lead_research_qualification",
            "lead_engagement",
        ]

    state["services"] = services
    state["active_agents"] = agents
    state["status"] = "services_routed"
    return state


# =========================================================
# CONTENT MARKETING
# =========================================================

def content_strategy_research(state):
    client = state["client"]

    results = web_search(
        research_query(client, state["request"])
    )

    state["research"] = results

    state["strategy"] = ask(f"""
Create a simple content strategy.

Industry: {client['industry']}
Audience: {client['audience']}
Brand voice: {client['brand_voice']}
Goal: {client['goal']}
Request: {state['request']}

Use the research below:
{results}

Return:
- content angle
- 3 key points
- suggested CTA
- facts that should be verified
""")

    return state


def content_creation_distribution(state):
    client = state["client"]

    state["draft"] = ask(f"""
Create a professional marketing content draft.

Client: {client['name']}
Industry: {client['industry']}
Audience: {client['audience']}
Brand voice: {client['brand_voice']}
Goal: {client['goal']}

Strategy:
{state.get('strategy', '')}

Research:
{state.get('research', [])}

Request:
{state['request']}

Make it useful and specific to this industry.
Do not invent facts.
End with a natural CTA.
""")

    return state


# =========================================================
# PERSONAL BRANDING
# =========================================================

def brand_strategy(state):
    client = state["client"]

    state["strategy"] = ask(f"""
Create a personal branding strategy for a founder or executive.

Industry: {client['industry']}
Target audience: {client['audience']}
Brand voice: {client['brand_voice']}
Business goal: {client['goal']}
Request: {state['request']}

Return:
- positioning
- 3 thought-leadership themes
- audience pain points
- content angle
- CTA
""")

    return state


def personal_content(state):
    client = state["client"]

    state["draft"] = ask(f"""
Create a founder/executive thought-leadership post.

Industry: {client['industry']}
Audience: {client['audience']}
Voice: {client['brand_voice']}

Strategy:
{state.get('strategy', '')}

Client knowledge:
{state.get('knowledge', [])}

Request:
{state['request']}

Make the writing natural, specific and credible.
Do not invent personal achievements or facts.
""")

    return state


# =========================================================
# LEAD GENERATION
# =========================================================

def lead_research_qualification(state):
    client = state["client"]

    results = web_search(
        research_query(client, state["request"])
        + " target companies prospects decision makers"
    )

    state["research"] = results

    state["strategy"] = ask(f"""
Define an ICP and lead qualification approach.

Industry: {client['industry']}
Audience: {client['audience']}
Goal: {client['goal']}
Request: {state['request']}

Research:
{results}

Return:
- ICP
- qualification criteria
- useful signals
- fields that should be captured
""")

    return state


def lead_engagement(state):
    client = state["client"]

    state["draft"] = ask(f"""
Create a personalized B2B lead engagement campaign.

Client industry: {client['industry']}
Target audience: {client['audience']}
Brand voice: {client['brand_voice']}

Qualification strategy:
{state.get('strategy', '')}

Request:
{state['request']}

Create:
1. short outreach message
2. follow-up message
3. useful CTA

Do not pretend that a prospect has a relationship with the sender.
Do not invent prospect-specific facts.
""")

    return state


# =========================================================
# SHARED RAG
# =========================================================

def rag_agent(state):
    state["knowledge"] = kb.search(
        state["client_id"],
        state["request"],
        k=4,
    )

    return state


# =========================================================
# SHARED REVIEW
# =========================================================

def review_agent(state):
    client = state["client"]

    state["review"] = ask(f"""
Review this AI-generated business output.

Industry: {client['industry']}
Audience: {client['audience']}
Rules: {client.get('rules', [])}

Output:
{state.get('draft', '')}

Check:
- industry relevance
- unsupported claims
- hallucinations
- brand voice
- compliance
- usefulness

Return exactly:
DECISION: APPROVE
or
DECISION: REVISE

Then give short reasons.
""")

    return state


# =========================================================
# HUMAN IN THE LOOP
# =========================================================

def human_approval(state: GrowthState):
    decision = interrupt({
        "type": "human_approval",
        "message": "Approve this output before external execution?",
        "draft": state.get("draft", ""),
        "review": state.get("review", ""),
    })

    if decision.get("approved") is True:
        state["approved"] = True
        state["final_output"] = state.get("draft", "")
        state["status"] = "approved"
    else:
        state["approved"] = False
        state["status"] = "rejected"

    return state


# =========================================================
# GRAPH
# =========================================================

def build_graph():
    g = StateGraph(GrowthState)

    g.add_node("route_services", route_services)

    g.add_node(
        "content_strategy_research",
        content_strategy_research,
    )
    g.add_node(
        "content_creation_distribution",
        content_creation_distribution,
    )

    g.add_node("brand_strategy", brand_strategy)
    g.add_node("personal_content", personal_content)

    g.add_node(
        "lead_research_qualification",
        lead_research_qualification,
    )
    g.add_node(
        "lead_engagement",
        lead_engagement,
    )

    g.add_node("rag", rag_agent)
    g.add_node("review", review_agent)
    g.add_node("human_approval", human_approval)

    g.add_edge(START, "route_services")

    # Conditional routing based on selected services.
    def next_nodes(state):
        services = state.get("services", [])
        nodes = []

        if "content_marketing" in services:
            nodes.append("content_strategy_research")

        if "personal_branding" in services:
            nodes.append("brand_strategy")

        if "lead_generation" in services:
            nodes.append("lead_research_qualification")

        return nodes

    g.add_conditional_edges(
        "route_services",
        next_nodes,
    )

    g.add_edge(
        "content_strategy_research",
        "content_creation_distribution",
    )
    g.add_edge(
        "content_creation_distribution",
        "rag",
    )

    g.add_edge("brand_strategy", "personal_content")
    g.add_edge("personal_content", "rag")

    g.add_edge(
        "lead_research_qualification",
        "lead_engagement",
    )
    g.add_edge("lead_engagement", "rag")

    # When multiple service branches converge, LangGraph will execute
    # the downstream node when the required upstream paths complete.
    g.add_edge("rag", "review")
    g.add_edge("review", "human_approval")
    g.add_edge("human_approval", END)

    return g.compile()


growth_graph = build_graph()
