# Trust Graph Architecture: 1-Page Design Note

**Prompt:** *"If you had to redesign LinkedIn to work only through trust graphs, what would you build first?"*

If I were to redesign LinkedIn purely around trust graphs, the very first thing I would build is a **Consent-Based, Implicit Edge-Weighting Engine protected by an LLM Guardrail Layer**.

### 1. The Core Problem: Explicit Connections are Dead
LinkedIn's fatal flaw is that a "connection" is binary. A connection could be your co-founder of 10 years, or a random recruiter who spammed you yesterday. In a pure trust graph, binary connections are useless. 

### 2. The Solution: Implicit Signals (Neo4j + Vector Embeddings)
Instead of asking users to click "Connect", the trust graph would ingest OAuth data (Gmail, Calendar) to map implicit relationships.
- **Frequency:** How often do they email?
- **Recency:** When was the last meeting?
- **Duration:** Are they 15-minute intro calls, or recurring 2-hour strategic syncs?

These signals are converted into edge weights. Using **Neo4j**, we can map these nodes. But to make them contextually aware, we encode the interaction metadata (e.g., industry, project names from calendar titles) into **Vector Embeddings**. 

### 3. The Pathfinding Logic (2-hop / 3-hop)
When a user wants an intro, a FastAPI microservice runs a shortest-path algorithm (like Dijkstra's or A*) across the Neo4j graph, inverted for trust weight (higher trust = lower path cost). It limits traversal to a maximum of 3 hops, as anything beyond a 3-hop intro degrades trust exponentially.

### 4. The Critical Component: The LLM Guardrail (The "Immune System")
Graph data is incredibly susceptible to poisoning. An automated marketing newsletter sending you 500 emails could falsely trigger a high "Frequency" edge weight.
This is where the **LLM Guardrail Layer** comes in—functioning much like the AI safety layer built at Elloe AI:
1. **Ingestion Sanitization:** The LLM evaluates the context of the OAuth data and strips out recurring internal team meetings and automated emails before they ever enter the graph database.
2. **Output Enforcement:** When generating the draft intro, the guardrail actively checks the AI's output against the Neo4j ground-truth data. It enforces a strict rule: *No fabricated relationship claims.* If the AI drafts "Since you guys worked closely together," but the graph only shows one 15-minute meeting, the guardrail rejects and rewrites the draft.

### Conclusion
By building this first, we create a defensible data moat. We aren't just mapping who knows who; we are quantifying *trust*, sanitizing it against noise, and strictly regulating how that trust is invoked.
