import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from clients import build_client
from graph import growth_graph
from rag import seed_demo_data


app = Flask(__name__)
CORS(app)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/run")
def run_workflow():
    data = request.get_json() or {}

    client_id = data.get("client_id", "manufacturing_demo")
    request_text = data.get("request", "").strip()

    if not request_text:
        return jsonify({"error": "request is required"}), 400

    client = build_client(client_id, data)
    run_id = str(uuid.uuid4())

    state = {
        "run_id": run_id,
        "client_id": client_id,
        "request": request_text,
        "client": client,
        "services": [],
        "active_agents": [],
        "research": [],
        "knowledge": [],
        "strategy": "",
        "draft": "",
        "review": "",
        "final_output": "",
        "approved": False,
        "status": "starting",
        "error": "",
    }

    try:
        result = growth_graph.invoke(
            state,
            config={"configurable": {"thread_id": run_id}},
        )

        return jsonify({
            "run_id": run_id,
            "status": result.get("status"),
            "services": result.get("services"),
            "active_agents": result.get("active_agents"),
            "draft": result.get("draft"),
            "review": result.get("review"),
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.post("/api/approve/<run_id>")
def approve(run_id):
    # A production version should load the same LangGraph thread from
    # a persistent checkpointer and resume it with Command(resume=...).
    # This endpoint is the UI contract for that approval action.

    from langgraph.types import Command

    try:
        result = growth_graph.invoke(
            Command(resume={"approved": True}),
            config={"configurable": {"thread_id": run_id}},
        )

        return jsonify({
            "run_id": run_id,
            "status": result.get("status"),
            "content": result.get("final_output"),
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.post("/api/reject/<run_id>")
def reject(run_id):
    from langgraph.types import Command

    try:
        result = growth_graph.invoke(
            Command(resume={"approved": False}),
            config={"configurable": {"thread_id": run_id}},
        )

        return jsonify({
            "run_id": run_id,
            "status": result.get("status"),
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    seed_demo_data()
    app.run(host="0.0.0.0", port=5000, debug=True)
