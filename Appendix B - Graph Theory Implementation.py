"""
APPENDIX B: GRAPH THEORY IMPLEMENTATION FOR NETWORK CENTRALITY ANALYSIS

This implementation constructs Bahrain's road network graph and computes centrality measures to prioritize charging station locations based on:
- Betweenness centrality (critical bridging nodes)
- Closeness centrality (minimal average distance)
- Degree centrality (connectivity importance)

Dependencies: networkx (v3.1), matplotlib (v3.7.1)
"""

import networkx as nx

def load_road_network():
    """
    CONSTRUCTS BAHRAIN ROAD NETWORK GRAPH
    
    Returns:
    G : Graph object representing major highways with 
        edge attributes 'weight' and 'length' (km)
    """
    G = nx.Graph()
    
    # Major highways in Bahrain (simplified representation)
    highways = [
        ("Manama", "Muharraq", 7.5),    # Route 1
        ("Manama", "Riffa", 12.3),       # Route 2
        ("Manama", "Hamad Town", 15.8),  # Route 3
        ("Riffa", "Hamad Town", 8.2),    # Route 4
        ("Riffa", "Awali", 10.5),        # Route 5
        ("Muharraq", "Hidd", 6.4),       # Route 6
        ("Manama", "Budaiya", 14.2),     # Route 7
        ("Manama", "Saar", 11.7),        # Route 8
        ("Saar", "Budaiya", 5.3),        # Route 9
        ("Riffa", "Isa Town", 7.8),      # Route 10
        ("Manama", "Isa Town", 9.6),     # Route 11
        ("Hidd", "Sitra", 12.1),         # Route 12
        ("Manama", "Sitra", 8.9)         # Route 13
    ]
    
    # Add edges with distance-based weights
    for source, target, distance in highways:
        G.add_edge(source, target, weight=distance, length=distance)
    
    return G

def calculate_centrality_measures(G):
    """
    COMPUTES CENTRALITY MEASURES FOR NODE PRIORITIZATION
    
    Parameters:
    G : Road network graph
    
    Returns:
    betweenness : Dictionary of betweenness centrality values
    closeness   : Dictionary of closeness centrality values
    degree      : Dictionary of degree centrality values
    """
    # Betweenness centrality (weighted by road length)
    betweenness = nx.betweenness_centrality(G, weight='length')
    
    # Closeness centrality (weighted by road length)
    closeness = nx.closeness_centrality(G, distance='length')
    
    # Degree centrality (unweighted)
    degree = nx.degree_centrality(G)
    
    return betweenness, closeness, degree