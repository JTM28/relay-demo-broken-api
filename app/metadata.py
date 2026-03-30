API_DESCRIPTION = """
Relay Coordination API is a deliberately storage-neutral backend used to simulate how
independently managed agents coordinate around shared work. The current service stops
short of persistence on purpose: contracts, routes, and domain services are in place,
but storage-specific schema design is intentionally deferred.

The key rule is that public API contracts should not assume relational tables,
document collections, embedded records, or join-heavy access patterns. Future agents
can take the same API surface and explore different persistence strategies without
having to rewrite the HTTP layer first.
""".strip()

API_TAGS = [
    {
        "name": "health",
        "description": "Runtime health and seed metadata for the demo service.",
    },
    {
        "name": "items",
        "description": "Backlog items that participating agents are expected to coordinate around.",
    },
    {
        "name": "agents",
        "description": "Profiles for the seeded agents participating in the coordination flow.",
    },
    {
        "name": "sessions",
        "description": "Negotiation sessions plus comparison tools for evaluating competing directions.",
    },
]
