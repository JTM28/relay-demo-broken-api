# Relay Coordination API

Relay Coordination API is a storage-neutral FastAPI service for simulating how independently owned agents negotiate architecture decisions before any persistence layer exists.

The live HTTP surface is defined in `contracts/`. `schemas/` is intentionally reserved for future persistence-specific work, so later SQL or NoSQL branches can diverge without rewriting the public API first.

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API docs.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Returns service metadata, seed version, and seeded resource counts. |
| `GET` | `/items` | Lists the seeded work items used for the demo flow. |
| `GET` | `/items/{item_id}` | Returns a single seeded work item. |
| `GET` | `/agents` | Lists the seeded agent roster. |
| `GET` | `/agents/{agent_id}` | Returns a single seeded agent profile. |
| `GET` | `/sessions` | Lists the seeded negotiation sessions. |
| `GET` | `/sessions/{session_id}` | Returns a single seeded negotiation session. |
| `POST` | `/sessions/{session_id}/compare` | Compares two candidate directions with neutral scoring inputs. |

## Architecture

The app is split so the API, domain logic, and contract layer stay separate without implying a persistence model:

`main.py` -> `app.create_app()` -> `api/router.py` -> route modules -> services -> in-memory domain state

Public request and response models live in `contracts/`. Internal seed data and coordination objects live in `models/`. The `schemas/` package is left empty on purpose until a future storage layer needs its own mapping shapes.

## Storage Policy

All state is in memory for now.

That leaves the storage decision open so later work can go in either direction:

- A relational path if the workload benefits from structured records and transactional workflows.
- A document-oriented path if evolving session payloads turn out to be the better fit.

No database code, ORM code, or persistence wiring is present in this repo yet.

## Testing

```bash
pytest
```

The test suite exercises the live API contract end to end, including the compare endpoint and the OpenAPI surface.
