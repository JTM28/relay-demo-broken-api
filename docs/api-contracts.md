# API Contracts

This service deliberately separates the public HTTP contract from any future storage model.

## Contract Boundary

- `contracts/` is the public API surface.
- `models/` holds internal in-memory coordination objects used by the app today.
- `schemas/` is intentionally reserved for future persistence-specific shapes and mappings.

That separation keeps the current service flexible enough for later SQL or NoSQL experiments without changing the route contract first.

## Public Resources

- `GET /health` returns runtime metadata and seeded resource counts.
- `GET /items` and `GET /items/{item_id}` expose the work-item surface.
- `GET /agents` and `GET /agents/{agent_id}` expose the agent roster.
- `GET /sessions` and `GET /sessions/{session_id}` expose negotiation sessions.
- `POST /sessions/{session_id}/compare` compares two candidate directions using neutral scoring inputs.

## Design Rule

Public contracts should avoid storage-specific language.

In practice, that means:

- Use opaque identifiers instead of database-shaped keys.
- Keep nested structures focused on the API story, not on relational joins or document embedding.
- Keep comparison inputs generic enough that either persistence direction can adopt them later.
