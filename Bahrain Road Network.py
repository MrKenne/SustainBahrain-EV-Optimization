import osmnx as ox
from typing import Optional, Union, List

def analyze_osm_network(
    place_name: str = "Bahrain",
    network_type: str = "drive",
    max_nodes: int = 5,
    max_edges: int = 5,
    log_file: Optional[str] = None
) -> None:
    """
    Analyze and display OSM network data for a specified location
    
    Args:
        place_name: Name of location to analyze
        network_type: Type of network ('drive', 'walk', 'bike', etc.)
        max_nodes: Maximum number of nodes to display
        max_edges: Maximum number of edges to display
        log_file: Optional file path to save output
    """
    try:
        # Capture console output if log file is specified
        if log_file:
            import sys
            from contextlib import redirect_stdout
            with open(log_file, 'w') as f, redirect_stdout(f):
                _analyze_network(place_name, network_type, max_nodes, max_edges)
        else:
            _analyze_network(place_name, network_type, max_nodes, max_edges)
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Check location name or internet connection")

def _analyze_network(
    place_name: str,
    network_type: str,
    max_nodes: int,
    max_edges: int
) -> None:
    """Internal network analysis implementation"""
    print(f"Loading {network_type} network for {place_name}...")
    G = ox.graph_from_place(place_name, network_type=network_type)
    
    print("\n" + "="*50)
    print(f"NETWORK ANALYSIS: {place_name.upper()} ({network_type} network)")
    print("="*50)
    
    print(f"\nTotal Nodes: {len(G.nodes):,}")
    print(f"Total Edges: {len(G.edges):,}")
    
    # Node analysis
    print("\n" + "-"*50)
    print(f"NODE ATTRIBUTES (first {max_nodes} nodes)")
    print("-"*50)
    for i, (node_id, data) in enumerate(G.nodes(data=True)):
        if i >= max_nodes:
            break
        print(f"\nNode ID: {node_id}")
        print(f"  • OSM ID: {data.get('osmid', 'N/A')}")
        print(f"  • Latitude: {data.get('y', 'N/A'):.6f}")
        print(f"  • Longitude: {data.get('x', 'N/A'):.6f}")
        print(f"  • Street Count: {data.get('street_count', 'N/A')}")
        
    # Edge analysis
    print("\n" + "-"*50)
    print(f"EDGE ATTRIBUTES (first {max_edges} edges)")
    print("-"*50)
    for i, (u, v, key, data) in enumerate(G.edges(keys=True, data=True)):
        if i >= max_edges:
            break
        print(f"\nEdge: ({u} → {v}, Key: {key})")
        print(f"  • OSM ID: {data.get('osmid', 'N/A')}")
        print(f"  • Length: {data.get('length', 'N/A'):.1f} meters")
        
        # Handle complex highway types
        highway = data.get('highway', [])
        if isinstance(highway, list):
            highway = ", ".join(highway)
        print(f"  • Road Type: {highway or 'N/A'}")
        
        # Handle speed limit variations
        maxspeed = data.get('maxspeed', 'N/A')
        if isinstance(maxspeed, list):
            maxspeed = "/".join(maxspeed)
        print(f"  • Speed Limit: {maxspeed}")
        
        # Additional useful attributes
        print(f"  • Oneway: {data.get('oneway', 'N/A')}")
        print(f"  • Lanes: {data.get('lanes', 'N/A')}")
        print(f"  • Geometry: {data.get('geometry', 'N/A')}")

if __name__ == "__main__":
    # Example usage with configurable parameters
    analyze_osm_network(
        place_name="Bahrain",
        network_type="drive",
        max_nodes=5,
        max_edges=5,
        log_file="bahrain_network_analysis.txt"  # Remove to display in console only
    )