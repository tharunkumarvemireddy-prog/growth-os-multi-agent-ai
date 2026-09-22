from typing import TypedDict, Any


class GrowthState(TypedDict, total=False):
    run_id: str
    client_id: str
    request: str

    client: dict[str, Any]
    services: list[str]
    service_index: int
    active_agents: list[str]

    content_result: dict[str, Any]
    branding_result: dict[str, Any]
    lead_result: dict[str, Any]

    research: list[dict]
    knowledge: list[str]

    combined_output: str
    review: str

    final_output: str
    approved: bool
    status: str
    error: str
