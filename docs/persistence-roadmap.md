# Persistence Roadmap

The current implementation keeps all state in memory so the API can be exercised immediately and the storage direction can stay open.

## Future Direction A: Relational

Use this path if the workload eventually needs:

- Transactional workflows.
- Strongly structured records for items, agents, and sessions.
- Reporting-style queries over normalized data.

## Future Direction B: Document-Oriented

Use this path if the workload eventually needs:

- Flexible session payloads that evolve as negotiation data changes.
- Fewer joins when session state becomes deeply nested.
- Fast iteration on mixed-structure records.

## Decision Principle

Do not let the public contract pick the storage backend early.

The repo is intentionally shaped so either direction can be explored later without changing the HTTP surface first.
