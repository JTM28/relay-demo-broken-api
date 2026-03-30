# Architecture Notes

This repository models a coordination service for testing how independently managed agents negotiate implementation direction.

The aim is to make the system feel real enough for prompt-driven disagreement, while staying deliberately open about the eventual storage model.

## Current Shape

- `contracts/` contains the public request and response models.
- `models/` contains internal in-memory coordination objects.
- `services/` contains retrieval, filtering, and comparison logic.
- `api/` contains the HTTP routes and router composition.
- `app/` owns application construction, runtime state, and error handling.
- `schemas/` is intentionally reserved for future persistence-specific work.

## Why This Shape

The split keeps the service believable without implying a preferred persistence style.

It also gives later branches enough room to disagree about storage strategy, repository boundaries, and session modeling without rewriting the HTTP layer first.

## What Is Not Here Yet

- No database layer.
- No ORM models.
- No migration tooling.
- No persistence abstraction beyond the reserved `schemas/` package and clear module seams.
