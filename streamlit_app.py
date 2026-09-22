import requests
import streamlit as st


API_URL = "http://127.0.0.1:5000"

st.set_page_config(
    page_title="Growth OS",
    page_icon="G",
    layout="wide",
)

st.title("Growth OS")
st.caption(
    "Multi-agent platform for Content Marketing, Personal Branding and Lead Generation"
)

with st.sidebar:
    st.header("Client")

    client_id = st.selectbox(
        "Demo client",
        ["manufacturing_demo", "fintech_demo"],
    )

    if client_id == "manufacturing_demo":
        industry = "manufacturing"
        audience = "plant managers, operations leaders, procurement teams"
        voice = "technical, practical and professional"
    else:
        industry = "fintech"
        audience = "CFOs, CTOs, banking leaders, fintech founders"
        voice = "analytical, trustworthy and clear"

    industry = st.text_input("Industry", industry)
    audience = st.text_input("Audience", audience)
    voice = st.text_input("Brand voice", voice)

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
    )

    goal = st.text_input(
        "Business goal",
        "Build authority and generate qualified opportunities.",
    )

st.subheader("Growth request")

request_text = st.text_area(
    "What should the Growth OS do?",
    placeholder=(
        "Example: Build a LinkedIn campaign about how AI is "
        "improving predictive maintenance."
    ),
    height=130,
)

if st.button("Run Growth OS", type="primary"):
    if not services:
        st.warning("Select at least one service.")
        st.stop()

    if not request_text.strip():
        st.warning("Enter a request.")
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

    with st.spinner("Running selected agents..."):
        response = requests.post(
            f"{API_URL}/api/run",
            json=payload,
            timeout=180,
        )

    if response.ok:
        st.session_state["result"] = response.json()
    else:
        st.error(response.text)

result = st.session_state.get("result")

if result:
    st.divider()

    st.subheader("Workflow")

    st.write(
        " → ".join(result.get("active_agents", []))
        + " → RAG → Review → Human Approval"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Selected services",
            len(result.get("services", [])),
        )

    with col2:
        st.metric(
            "Active agents",
            len(result.get("active_agents", [])),
        )

    st.subheader("Generated output")

    st.text_area(
        "Draft",
        result.get("draft", ""),
        height=330,
    )

    st.subheader("Review")

    st.text_area(
        "Review Agent",
        result.get("review", ""),
        height=180,
    )

    st.subheader("Human approval")

    run_id = result.get("run_id")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Approve"):
            response = requests.post(
                f"{API_URL}/api/approve/{run_id}",
                timeout=60,
            )

            if response.ok:
                st.success("Approved.")
                st.write(response.json().get("content", ""))

    with col2:
        if st.button("Reject"):
            response = requests.post(
                f"{API_URL}/api/reject/{run_id}",
                timeout=60,
            )

            if response.ok:
                st.warning("Rejected and returned to the workflow.")
