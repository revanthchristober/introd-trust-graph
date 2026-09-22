# Trust Graph Pathfinder

This repository contains a working demo of a 2-hop/3-hop trust-weighted intro pathfinder. It leverages `NetworkX` for graph routing and `FastAPI` to expose the querying endpoints. 

## Features
- **Trust-Weighted Edges:** Relationships are scored based on frequency and recency of interactions (e.g., from Calendar and Email OAuth data).
- **2-hop/3-hop Routing:** Uses Dijkstra's algorithm to find the optimal path through the trust graph.
- **AI Draft Intro + Guardrails:** Generates a draft introduction and passes it through a guardrail check. The guardrail ensures the AI does not hallucinate or fabricate relationship claims (e.g., claiming "we worked closely" when the data only shows occasional calendar invites).

## Important Limitation: LinkedIn API
> **Honest Disclaimer regarding LinkedIn Data:** 
> The LinkedIn API strictly restricts access to connection graphs via OAuth for third-party developers. It is impossible to natively ingest a user's full LinkedIn connections graph via standard OAuth scopes without violating their Terms of Service. 
> 
> **Workaround:** For this demo (and for production viability), users must manually upload their `Connections.csv` data export, or we rely purely on implicit trust graphs generated from Google Workspace/Microsoft 365 (Gmail & Calendar) where API access is reliably granted and edge-weighting (frequency/recency) is actually much higher signal than a static LinkedIn connection.

## Setup
1. Run `python generate_data.py` to create synthetic test data (since we never use private/real user data for demos).
2. Run `uvicorn main:app --reload` to start the API.
3. Send a POST request to `/find-path` with `{"source_user": "Me", "target_user": "User_20"}`.
