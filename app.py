import os
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from langgraph.types import Command

from clients import build_client
from graph import growth_graph
from rag import seed_demo_data


app = Flask(__name__)
CORS(app)

# Seed demo client knowledge when the API process starts.
# In production this would be loaded from the persistent tenant knowledge store.
seed_demo_data()


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "growth-os-api"
    })


@app.get("/")
def home():
    return jsonify({
        "service": "Growth OS API",
        "status": "running"
    })


@app.post("/api/run")
def run_workflow():
    data = request.get_json() or {}

    client_id = data.get(
        "client_id",
        "manufacturing_demo"
    )

    request_text = data.get(
        "request",
        ""
    ).strip()

    if not request_text:
        return jsonify({
            "error": "request is required"
        }), 400

    services = data.get("services") or []

    if not services:
        return jsonify({
            "error": "Select at least one service."
        }), 400

    client = build_client(
        client_id,
        data
    )

    run_id = str(uuid.uuid4())

    state = {
        "run_id": run_id,
        "client_id": client_id,
        "request": request_text,
        "client": client,
        "services": [],
        "service_index": 0,
        "active_agents": [],
        "content_result": {},
        "branding_result": {},
        "lead_result": {},
        "research": [],
        "knowledge": [],
        "combined_output": "",
        "review": "",
        "final_output": "",
        "approved": False,
        "status": "starting",
        "error": "",
    }

    try:
        result = growth_graph.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": run_id
                }
            },
        )

        return jsonify({
            "run_id": run_id,
            "status": result.get("status"),
            "services": result.get("services"),
            "active_agents": result.get("active_agents"),
            "draft": result.get("combined_output", ""),
            "review": result.get("review", ""),
            "interrupted": result.get("status") != "approved",
        })

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500


def resume_workflow(run_id, approved):
    try:
        result = growth_graph.invoke(
            Command(
                resume={
                    "approved": approved
                }
            ),
            config={
                "configurable": {
                    "thread_id": run_id
                }
            },
        )

        return jsonify({
            "run_id": run_id,
            "status": result.get("status"),
            "content": result.get("final_output", ""),
        })

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500


@app.post("/api/approve/<run_id>")
def approve(run_id):
    return resume_workflow(
        run_id,
        True
    )


@app.post("/api/reject/<run_id>")
def reject(run_id):
    return resume_workflow(
        run_id,
        False
    )


if __name__ == "__main__":
    port = int(
        os.getenv(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
