# Trust Graph Pathfinder

This repository contains a working MVP demo of a 2-hop/3-hop trust-weighted intro pathfinder. It leverages `NetworkX` for fast, in-memory graph routing and `FastAPI` to expose the querying endpoints.

## Features
- **Trust-Weighted Edges:** Relationships are scored based on frequency and recency of interactions (e.g., mock Calendar and Email data).
- **2-hop/3-hop Routing:** Uses Dijkstra's algorithm to find the optimal path through the trust graph.
- **Rule-Based Draft Guardrails (MVP):** Generates a template-based draft intro and passes it through a keyword-based rule check. This ensures the draft does not fabricate deep relationships (e.g., claiming "worked closely"). In production, this is designed to be swapped for a robust LLM-based guardrail.

## Important Limitation: LinkedIn API
> **Honest Disclaimer regarding LinkedIn Data:** 
> The LinkedIn API strictly restricts access to connection graphs via OAuth for third-party developers. It is impossible to natively ingest a user's full LinkedIn connections graph via standard OAuth scopes without violating their Terms of Service. 
> 
> **Workaround:** For this demo, we rely on synthetic data mimicking implicit trust graphs generated from Google Workspace/Microsoft 365 (Gmail & Calendar) where API access is granted and edge-weighting (frequency/recency) provides a much higher signal than a static LinkedIn connection.

## Setup
1. Run `python generate_data.py` to create synthetic test data (since we never use private/real user data for demos).
2. Run `uvicorn main:app --reload` to start the API.
3. Send a POST request to `/find-path` with `{"source_user": "Me", "target_user": "User_20"}`.
