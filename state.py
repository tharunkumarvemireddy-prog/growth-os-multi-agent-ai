from typing import TypedDict, Any


class GrowthState(TypedDict, total=False):
    run_id: str
    client_id: str
    request: str

    client: dict[str, Any]
    services: list[str]
    active_agents: list[str]

    research: list[dict]
    knowledge: list[str]

    strategy: str
    draft: str
    review: str

    final_output: str
    approved: bool
    status: str
    error: str
