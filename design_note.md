# Trust Graph Architecture: 1-Page Design Note

**Prompt:** *"If you had to redesign LinkedIn to work only through trust graphs, what would you build first?"*

If I were to redesign LinkedIn purely around trust graphs, the very first thing I would build is a **Consent-Based, Implicit Edge-Weighting Engine**.

### 1. The Core Problem: Explicit Connections are Dead
LinkedIn's fatal flaw is that a "connection" is binary. A connection could be your co-founder of 10 years, or a random recruiter who spammed you yesterday. In a pure trust graph, binary connections are useless. 

### 2. The MVP Solution: Implicit Signals (NetworkX)
Instead of asking users to click "Connect", the trust graph ingests data (Gmail, Calendar) to map implicit relationships based on Frequency and Recency.
For the MVP, this is modeled using **NetworkX** for fast, in-memory edge traversal, inverting the trust score to calculate the shortest (highest-trust) path. 

### 3. The Pathfinding Logic (2-hop / 3-hop)
A FastAPI microservice runs a shortest-path algorithm (Dijkstra) across the graph. It strictly limits traversal to a maximum of 3 hops, as anything beyond a 3-hop intro degrades trust exponentially.

### 4. The "Immune System" Guardrail (Rule-Based to LLM)
Graph data is incredibly susceptible to poisoning (e.g., automated marketing newsletters).
In this MVP, we implement a **Rule-Based Guardrail** that checks the generated draft intro against fabricated relationship claims (e.g., blocking phrases like "worked closely" if the edge weight doesn't support it). 
        
**Production Scaling:** In a production environment, this NetworkX architecture scales to **Neo4j**, and the rule-based checker is replaced by a **mid-flight LLM Guardrail Layer** (similar to the AI safety layer at Elloe AI) to sanitize ingestion and dynamically enforce truthfulness in intro drafts.

### Conclusion
By building this foundation, we create a defensible data moat. We aren't just mapping who knows who; we are quantifying *trust*, sanitizing it against noise, and regulating how that trust is invoked.
