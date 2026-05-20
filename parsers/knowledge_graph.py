"""
Knowledge Graph Visualization
Builds an interactive network showing how surveillance capitalism works.
Highlights the circular path: User → AI Project → Anxiety → Advertiser → Demographics → User
"""

import sys
import json
from pathlib import Path
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
from utils import load_json

# Windows encoding fix
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def build_knowledge_graph():
    """Build interactive knowledge graph from surveillance data"""

    # Load all data sources
    instagram_data = load_json("../output/instagram_data.json")
    google_data = load_json("../output/google_data.json")
    ai_data = load_json("../output/ai_data.json")
    user_features = load_json("../output/user_feature_matrix.json")

    # Try to load embeddings if available
    embeddings_path = Path("../output/embeddings_ollama.json")
    embeddings_data = load_json(str(embeddings_path)) if embeddings_path.exists() else None

    # Create directed graph
    G = nx.DiGraph()

    # ═══════════════════════════════════════════════════════════
    # STEP 1: Add central USER node
    # ═══════════════════════════════════════════════════════════
    G.add_node("YOU",
               node_type="user",
               color="#ff0000",
               size=40,
               title="Central surveillance target")

    # ═══════════════════════════════════════════════════════════
    # STEP 2: Add LOCATION nodes
    # ═══════════════════════════════════════════════════════════
    locations = instagram_data.get("locations", [])
    for loc in locations[:10]:  # Limit to top 10
        if loc and loc != "Usage explanation":
            node_id = f"LOC_{loc}"
            G.add_node(node_id,
                      label=loc,
                      node_type="location",
                      color="#3498db",
                      size=15,
                      title=f"Location tracked: {loc}")
            G.add_edge("YOU", node_id, label="VISITED", color="#3498db")

    # ═══════════════════════════════════════════════════════════
    # STEP 3: Add SEARCH_TERM nodes (Instagram + Google)
    # ═══════════════════════════════════════════════════════════
    # Instagram searches
    instagram_searches = instagram_data.get("recent_searches", [])
    for search in instagram_searches[:15]:  # Top 15
        query = search.get("query", "")
        if query:
            node_id = f"SEARCH_{query}"
            G.add_node(node_id,
                      label=query,
                      node_type="search",
                      color="#f1c40f",
                      size=12,
                      title=f"Instagram search: {query}")
            G.add_edge("YOU", node_id, label="SEARCHED", color="#f1c40f")

    # Google searches
    google_searches = google_data.get("google_searches", [])
    for search in google_searches[:15]:  # Top 15
        query = search.get("value", "")
        if query:
            node_id = f"SEARCH_{query[:50]}"  # Truncate long queries
            G.add_node(node_id,
                      label=query[:50],
                      node_type="search",
                      color="#f39c12",
                      size=12,
                      title=f"Google search: {query}")
            G.add_edge("YOU", node_id, label="SEARCHED", color="#f39c12")

    # ═══════════════════════════════════════════════════════════
    # STEP 4: Add YOUTUBE_VIDEO nodes
    # ═══════════════════════════════════════════════════════════
    youtube_videos = google_data.get("youtube_watched", [])
    for video in youtube_videos[:20]:  # Top 20
        title = video.get("value", "")
        if title:
            node_id = f"VIDEO_{title[:40]}"
            G.add_node(node_id,
                      label=title[:40],
                      node_type="video",
                      color="#2ecc71",
                      size=12,
                      title=f"YouTube: {title}")
            G.add_edge("YOU", node_id, label="WATCHED", color="#2ecc71")

    # ═══════════════════════════════════════════════════════════
    # STEP 5: Add DEMOGRAPHIC nodes
    # ═══════════════════════════════════════════════════════════
    demographics = instagram_data.get("ad_categories", [])
    for demo in demographics:
        if demo:
            node_id = f"DEMO_{demo}"
            G.add_node(node_id,
                      label=demo,
                      node_type="demographic",
                      color="#9b59b6",
                      size=18,
                      title=f"Demographic profile: {demo}")
            G.add_edge("YOU", node_id, label="PROFILED_AS", color="#9b59b6")

    # ═══════════════════════════════════════════════════════════
    # STEP 6: Add ADVERTISER nodes (top 30)
    # ═══════════════════════════════════════════════════════════
    advertisers = instagram_data.get("advertisers_sample", [])[:30]

    # Map advertisers to their likely target demographics
    advertiser_targeting = {
        "LinkedIn APAC": ["Education level: Associate or Bachelors Degree", "Engaged shoppers"],
        "Final Round AI": ["Education level: Associate or Bachelors Degree"],
        "BookMyShow": ["Engaged shoppers"],
        "Cashify": ["Potential mobile network or device change", "Engaged shoppers"],
        "Tanishq": ["Engaged shoppers"],
        "The Souled Store": ["Engaged shoppers"],
        "Foxtale": ["Engaged shoppers"],
        "Rare Rabbit": ["Engaged shoppers"],
    }

    for advertiser in advertisers:
        if advertiser:
            node_id = f"ADV_{advertiser}"
            G.add_node(node_id,
                      label=advertiser,
                      node_type="advertiser",
                      color="#e67e22",
                      size=16,
                      title=f"Advertiser: {advertiser}")

            # Connect advertisers to demographics they target
            targets = advertiser_targeting.get(advertiser, ["Engaged shoppers"])
            for demo in targets:
                demo_node = f"DEMO_{demo}"
                if G.has_node(demo_node):
                    G.add_edge(node_id, demo_node, label="TARGETS", color="#e67e22")

    # ═══════════════════════════════════════════════════════════
    # STEP 7: Add AI_PROJECT nodes with anxiety markers
    # ═══════════════════════════════════════════════════════════
    gemini_files = ai_data.get("gemini_files", [])

    # Focus on files with anxiety markers
    ai_projects = [f for f in gemini_files if f.get("anxiety_markers")]

    for project in ai_projects[:15]:  # Top 15 projects
        file_name = project.get("file", "")
        markers = project.get("anxiety_markers", [])

        if file_name and markers:
            node_id = f"PROJECT_{file_name}"
            G.add_node(node_id,
                      label=file_name[:30],
                      node_type="ai_project",
                      color="#000000",
                      size=14,
                      title=f"AI Project: {file_name}\nReveals: {', '.join(markers)}")
            G.add_edge("YOU", node_id, label="BUILT", color="#000000")

            # Connect to anxiety markers
            for marker in markers:
                marker_node = f"ANXIETY_{marker}"
                if not G.has_node(marker_node):
                    G.add_node(marker_node,
                              label=marker.replace("_", " ").title(),
                              node_type="anxiety",
                              color="#8b0000",
                              size=20,
                              title=f"Anxiety signal: {marker}")

                G.add_edge(node_id, marker_node, label="REVEALS", color="#8b0000")

    # ═══════════════════════════════════════════════════════════
    # STEP 8: Add ANXIETY_MARKER nodes and connect to advertisers
    # ═══════════════════════════════════════════════════════════
    anxiety_markers = ai_data.get("behavioral_inference", {}).get("anxiety_markers_detected", {})

    # Map anxiety markers to relevant advertisers
    anxiety_to_advertisers = {
        "job_hunting": ["LinkedIn APAC", "Final Round AI"],
        "ai_building": ["Replit"],
        "finance_quant": [],
        "mlops_devops": [],
        "skill_gaps": []
    }

    for marker, count in anxiety_markers.items():
        marker_node = f"ANXIETY_{marker}"

        # Ensure anxiety node exists
        if not G.has_node(marker_node):
            G.add_node(marker_node,
                      label=marker.replace("_", " ").title(),
                      node_type="anxiety",
                      color="#8b0000",
                      size=20,
                      title=f"Anxiety signal: {marker} (detected {count}x)")

        # Connect anxiety to relevant advertisers
        relevant_advertisers = anxiety_to_advertisers.get(marker, [])
        for adv in relevant_advertisers:
            adv_node = f"ADV_{adv}"
            if G.has_node(adv_node):
                G.add_edge(marker_node, adv_node, label="TRIGGERS", color="#8b0000")

    # ═══════════════════════════════════════════════════════════
    # STEP 9: HIGHLIGHT THE CIRCULAR SURVEILLANCE PATH IN RED
    # ═══════════════════════════════════════════════════════════
    # The key loop: YOU → betterme ai interviewer → job_hunting → LinkedIn → Educated → YOU

    circular_path = [
        ("YOU", "PROJECT_betterme ai interviewer", "BUILT"),
        ("PROJECT_betterme ai interviewer", "ANXIETY_job_hunting", "REVEALS"),
        ("ANXIETY_job_hunting", "ADV_LinkedIn APAC", "TRIGGERS"),
        ("ADV_LinkedIn APAC", "DEMO_Education level: Associate or Bachelors Degree", "TARGETS"),
        ("DEMO_Education level: Associate or Bachelors Degree", "YOU", "PROFILED_AS")
    ]

    # Add these edges with RED color and thicker width
    for source, target, label in circular_path:
        if G.has_node(source) and G.has_node(target):
            # Remove existing edge if present
            if G.has_edge(source, target):
                G.remove_edge(source, target)

            # Add RED surveillance loop edge
            G.add_edge(source, target,
                      label=label,
                      color="#ff0000",
                      width=4,
                      title="🔴 SURVEILLANCE LOOP")

    # ═══════════════════════════════════════════════════════════
    # STEP 10: Create interactive visualization with Pyvis
    # ═══════════════════════════════════════════════════════════
    net = Network(height="900px",
                  width="100%",
                  bgcolor="#0a0a0a",
                  font_color="white",
                  directed=True)

    # Configure physics for better layout
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "stabilization": {
                "enabled": true,
                "iterations": 100
            },
            "barnesHut": {
                "gravitationalConstant": -8000,
                "centralGravity": 0.3,
                "springLength": 200,
                "springConstant": 0.04
            }
        },
        "nodes": {
            "font": {
                "size": 14,
                "color": "white"
            },
            "borderWidth": 2,
            "borderWidthSelected": 4
        },
        "edges": {
            "arrows": {
                "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                }
            },
            "smooth": {
                "enabled": true,
                "type": "continuous"
            }
        }
    }
    """)

    # Add nodes and edges from NetworkX graph
    for node, attrs in G.nodes(data=True):
        net.add_node(node,
                    label=attrs.get('label', node),
                    color=attrs.get('color', '#cccccc'),
                    size=attrs.get('size', 10),
                    title=attrs.get('title', node))

    for source, target, attrs in G.edges(data=True):
        net.add_edge(source, target,
                    label=attrs.get('label', ''),
                    color=attrs.get('color', '#666666'),
                    width=attrs.get('width', 1),
                    title=attrs.get('title', ''))

    # Save the visualization
    output_path = "../output/knowledge_graph.html"
    net.save_graph(output_path)

    # Print statistics
    print("\n" + "="*60)
    print("KNOWLEDGE GRAPH GENERATED")
    print("="*60)
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    print(f"\nNode breakdown:")
    node_types = defaultdict(int)
    for _, attrs in G.nodes(data=True):
        node_types[attrs.get('node_type', 'unknown')] += 1
    for node_type, count in sorted(node_types.items()):
        print(f"  {node_type}: {count}")
    print(f"\nKnowledge graph saved to {output_path}")
    print("\nRED SURVEILLANCE LOOP HIGHLIGHTED:")
    print("   YOU -> AI Project -> Anxiety -> Advertiser -> Demographics -> YOU")
    print("="*60 + "\n")

if __name__ == "__main__":
    build_knowledge_graph()
