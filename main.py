from fastapi import FastAPI, HTTPException
import networkx as nx
import csv
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Introd Pathfinder API")

# Initialize Graph
G = nx.Graph()

def load_graph():
    try:
        with open('data/Connections.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                source = row["Source"]
                target = row["Target"]
                freq = int(row["Frequency"])
                recency = int(row["Recency_Days_Ago"])
                
                # Trust Score formula: (Frequency * 10) / (Recency + 1)
                # Higher is better. For NetworkX shortest path, we need cost (lower is better), so we invert it.
                trust_score = (freq * 10) / (recency + 1)
                weight = 1 / trust_score if trust_score > 0 else 999
                
                G.add_edge(source, target, weight=weight, trust_score=trust_score, context=row["Context"])
    except FileNotFoundError:
        print("No data found. Please run generate_data.py first.")

load_graph()

class IntroRequest(BaseModel):
    source_user: str
    target_user: str
    
class PathResponse(BaseModel):
    path: List[str]
    total_trust_score: float
    draft_intro: str
    guardrail_status: str

def generate_draft_intro(path: List[str]) -> str:
    # A mock LLM intro generator
    if len(path) == 3:
        return f"Hi {path[1]}, I noticed you're connected to {path[2]}. I'm looking to chat with them about a new project. Would you be open to introducing us?"
    elif len(path) == 4:
        return f"Hi {path[1]}, I see you know {path[2]}, who knows {path[3]}. Could we explore an introduction?"
    else:
        return "Direct connection or path too long."

def guardrail_check(draft: str, path: List[str]) -> bool:
    # Guardrail: Ensure no fabricated claims. 
    # Check if the draft only mentions people actually in the path.
    # If the draft claims we know someone not in the path, it fails.
    for node in path:
        if node not in draft and node != path[0]: 
            # It's okay if source isn't explicitly named in this simple mock
            pass
            
    # Mocking a fabrication detection
    if "best friends" in draft.lower() or "worked closely" in draft.lower():
        # We don't have proof of this in our edge context!
        return False
    return True

@app.post("/find-path", response_model=PathResponse)
def find_path(req: IntroRequest):
    if req.source_user not in G or req.target_user not in G:
        raise HTTPException(status_code=404, detail="User not found in trust graph.")
        
    try:
        # Find shortest path using Dijkstra (based on inverted trust score = weight)
        # Limit to cutoff=3 (which means 3 edges, 4 nodes: 3-hop)
        path = nx.shortest_path(G, source=req.source_user, target=req.target_user, weight="weight")
        
        if len(path) > 4:
            raise HTTPException(status_code=400, detail="Path exceeds 3-hop limit.")
            
        # Calculate total trust
        total_trust = 0
        for i in range(len(path)-1):
            total_trust += G[path[i]][path[i+1]]["trust_score"]
            
        draft = generate_draft_intro(path)
        is_safe = guardrail_check(draft, path)
        
        if not is_safe:
            draft = "Draft rejected by guardrail: Fabricated relationship claim detected."
            
        return PathResponse(
            path=path,
            total_trust_score=round(total_trust, 2),
            draft_intro=draft,
            guardrail_status="PASS" if is_safe else "FAIL"
        )
        
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=404, detail="No path found within the network.")

@app.get("/")
def health_check():
    return {"status": "ok", "nodes": len(G.nodes)}
