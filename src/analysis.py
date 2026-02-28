import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
import os
import networkx as nx
import igraph as ig


def load_starwars_data(file="starwars-full-interactions-allCharacters-merged.json"):
    workspace_root = Path.cwd().parent
    file_path = workspace_root / "data" / "starwars" / file

    # Load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return data

def load_starwars_graph(file="starwars-full-interactions-allCharacters-merged.json", directed=False):
    """
    Load a graph from the given JSON file into a NetworkX graph.

    Parameters:
        json_path (str): Path to JSON file.
        directed (bool): Whether to create a directed graph.

    Returns:
        networkx.Graph or networkx.DiGraph
    """
    data = load_starwars_data(file)

    G = nx.DiGraph() if directed else nx.Graph()

    # Add nodes using character names as IDs
    for node in data["nodes"]:
        G.add_node(
            node["name"],
            value=node.get("value"),
            colour=node.get("colour")
        )

    # Add edges using name lookup
    for link in data["links"]:
        source_name = data["nodes"][link["source"]]["name"]
        target_name = data["nodes"][link["target"]]["name"]

        G.add_edge(
            source_name,
            target_name,
            weight=link.get("value", 1)
        )

    return G


def load_starwars_igraph(file="starwars-full-interactions-allCharacters-merged.json", directed=False):
    """
    Load a graph from the given JSON file into an igraph graph.

    Parameters:
        file (str): Path to JSON file.
        directed (bool): Whether to create a directed graph.

    Returns:
        igraph.Graph
    """
    data = load_starwars_data(file)

    # Create edge list with weights
    edges = []
    weights = []
    for link in data["links"]:
        edges.append((link["source"], link["target"]))
        weights.append(link.get("value", 1))

    # Create igraph from edge list
    G = ig.Graph(len(data["nodes"]), edges, directed=directed)

    # Add vertex attributes (names)
    vertex_names = [node["name"] for node in data["nodes"]]
    G.vs["name"] = vertex_names
    G.vs["value"] = [node.get("value") for node in data["nodes"]]

    # Add edge weights
    G.es["weight"] = weights

    return G