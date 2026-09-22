# Demo configuration.
# In production this belongs in PostgreSQL.

CLIENTS = {
    "manufacturing_demo": {
        "name": "ABC Industrial Systems",
        "industry": "manufacturing",
        "audience": ["plant managers", "operations leaders", "procurement teams"],
        "brand_voice": "technical, practical and professional",
        "goal": "Build B2B authority and generate qualified opportunities.",
        "services": ["content_marketing", "personal_branding", "lead_generation"],
        "rules": [
            "Do not invent product specifications.",
            "Do not make unsupported performance claims."
        ],
    },
    "fintech_demo": {
        "name": "XYZ Financial Technologies",
        "industry": "fintech",
        "audience": ["CFOs", "CTOs", "banking leaders", "fintech founders"],
        "brand_voice": "analytical, trustworthy and clear",
        "goal": "Build authority around digital payments and fraud prevention.",
        "services": ["content_marketing", "personal_branding"],
        "rules": [
            "Do not provide financial advice.",
            "Do not invent regulatory claims."
        ],
    },
}


def get_client(client_id):
    return CLIENTS.get(client_id)


def build_client(client_id, data):
    base = get_client(client_id)

    if not base:
        base = {
            "name": client_id,
            "industry": "general",
            "audience": [],
            "brand_voice": "professional",
            "goal": "Build awareness and generate useful business content.",
            "services": ["content_marketing"],
            "rules": [],
        }

    client = dict(base)

    # UI values can override demo values. In production validate these
    # against the authenticated tenant.
    client["industry"] = data.get("industry") or client["industry"]
    client["audience"] = [
        x.strip() for x in data.get("audience", "").split(",") if x.strip()
    ] or client["audience"]
    client["brand_voice"] = data.get("brand_voice") or client["brand_voice"]
    client["goal"] = data.get("goal") or client["goal"]

    requested = data.get("services")
    if requested:
        client["services"] = requested

    return client
