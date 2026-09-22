import os
import requests
import streamlit as st


API_URL = st.secrets.get(
    "API_URL",
    os.getenv(
        "API_URL",
        "http://127.0.0.1:5000"
    )
)


st.set_page_config(
    page_title="Growth OS",
    page_icon="🚀",
    layout="wide",
)


st.title("🚀 Growth OS")
st.caption(
    "AI-powered Content Marketing, Personal Branding "
    "and Lead Generation platform"
)


with st.sidebar:

    st.header("Client")

    client_id = st.selectbox(
        "Demo client",
        [
            "manufacturing_demo",
            "fintech_demo",
        ],
    )

    if client_id == "manufacturing_demo":
        default_industry = "manufacturing"
        default_audience = (
            "plant managers, operations leaders, "
            "procurement teams"
        )
        default_voice = (
            "technical, practical and professional"
        )
    else:
        default_industry = "fintech"
        default_audience = (
            "CFOs, CTOs, banking leaders, "
            "fintech founders"
        )
        default_voice = (
            "analytical, trustworthy and clear"
        )

    industry = st.text_input(
        "Industry",
        default_industry
    )

    audience = st.text_input(
        "Audience",
        default_audience
    )

    voice = st.text_input(
        "Brand voice",
        default_voice
    )

    services = st.multiselect(
        "Services",
        [
            "content_marketing",
            "personal_branding",
            "lead_generation",
        ],
        default=[
            "content_marketing",
            "personal_branding",
        ],
        format_func=lambda x: x.replace(
            "_", " "
        ).title(),
    )

    goal = st.text_input(
        "Business goal",
        "Build authority and generate qualified opportunities.",
    )


st.subheader("Growth request")

request_text = st.text_area(
    "What should Growth OS do?",
    placeholder=(
        "Example: Build a LinkedIn campaign about "
        "how AI is improving predictive maintenance."
    ),
    height=130,
)


if st.button(
    "Run Growth OS",
    type="primary",
):

    if not services:
        st.warning(
            "Select at least one service."
        )
        st.stop()

    if not request_text.strip():
        st.warning(
            "Enter a request."
        )
        st.stop()

    payload = {
        "client_id": client_id,
        "industry": industry,
        "audience": audience,
        "brand_voice": voice,
        "goal": goal,
        "services": services,
        "request": request_text,
    }

    try:
        with st.spinner(
            "Running the selected agents..."
        ):
            response = requests.post(
                f"{API_URL}/api/run",
                json=payload,
                timeout=180,
            )

        if response.ok:
            st.session_state["result"] = response.json()
        else:
            st.error(
                f"Backend error: {response.text}"
            )

    except requests.RequestException as exc:
        st.error(
            f"Could not connect to Flask API: {exc}"
        )


result = st.session_state.get("result")


if result:

    st.divider()

    st.subheader("Agent workflow")

    agents = result.get(
        "active_agents",
        []
    )

    if agents:
        st.code(
            " → ".join(agents)
            + " → RAG → Review → HITL"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Services",
            len(
                result.get(
                    "services",
                    []
                )
            ),
        )

    with col2:
        st.metric(
            "Agents",
            len(agents)
        )

    with col3:
        st.metric(
            "Status",
            result.get(
                "status",
                "unknown"
            ),
        )

    st.subheader("Generated output")

    st.text_area(
        "Draft",
        result.get(
            "draft",
            ""
        ),
        height=360,
    )

    st.subheader("Review Agent")

    st.text_area(
        "Quality review",
        result.get(
            "review",
            ""
        ),
        height=180,
    )

    st.subheader(
        "Human approval"
    )

    run_id = result.get(
        "run_id"
    )

    st.info(
        "The workflow pauses before external execution. "
        "Approve only after reviewing the generated content."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Approve",
            use_container_width=True,
        ):

            try:
                response = requests.post(
                    f"{API_URL}/api/approve/{run_id}",
                    timeout=60,
                )

                if response.ok:
                    data = response.json()
                    st.success(
                        "Human approval received."
                    )
                    st.text_area(
                        "Approved output",
                        data.get(
                            "content",
                            ""
                        ),
                        height=300,
                    )
                else:
                    st.error(
                        response.text
                    )

            except requests.RequestException as exc:
                st.error(str(exc))

    with col2:

        if st.button(
            "❌ Reject",
            use_container_width=True,
        ):

            try:
                response = requests.post(
                    f"{API_URL}/api/reject/{run_id}",
                    timeout=60,
                )

                if response.ok:
                    st.warning(
                        "Output rejected by human reviewer."
                    )
                else:
                    st.error(
                        response.text
                    )

            except requests.RequestException as exc:
                st.error(str(exc))


st.divider()

st.caption(
    "Growth OS | LangGraph + RAG + HITL + LangSmith + RAGAS"
)
