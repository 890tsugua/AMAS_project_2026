import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
import os
import networkx as nx
import igraph as ig
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler


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

def load_plot_config():
    # Time to plot. Chat wrote a mpl config:
    mpl.rcParams.update({
        # Use LaTeX for all text rendering
        "text.usetex": True,

        # Match LaTeX default font
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],

        # Font sizes (11pt article standard)
        "font.size": 12,
        "axes.titlesize": 12,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,

        # Figure layout
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "figure.autolayout": False,

        # Lines and markers
        "lines.linewidth": 1.5,
        "lines.markersize": 5,

        # Axes styling
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": False,
    })

    FIGSIZE_SINGLE = (3.4, 2.5)   # inches
    FIGSIZE_DOUBLE = (6.8, 3.5)
    FIGSIZE_MEDIUM = (1.3 * FIGSIZE_SINGLE[0], 1.3 * FIGSIZE_SINGLE[1])
    FIGSIZE_SINGLE_SQUARE = (3.4, 3.4)
    FIGSIZE_MEDIUM_SQUARE = (3.4 * 1.3, 3.4 * 1.3)

    cmap = plt.get_cmap("tab10")
    colors = cmap(np.linspace(0, 1, 10))

    mpl.rcParams['axes.prop_cycle'] = cycler(color=colors)
    COL = plt.rcParams['axes.prop_cycle'].by_key()['color']

    return {
        "FIGSIZE_SINGLE": FIGSIZE_SINGLE,
        "FIGSIZE_DOUBLE": FIGSIZE_DOUBLE,
        "FIGSIZE_MEDIUM": FIGSIZE_MEDIUM,
        "FIGSIZE_SINGLE_SQUARE": FIGSIZE_SINGLE_SQUARE,
        "FIGSIZE_MEDIUM_SQUARE": FIGSIZE_MEDIUM_SQUARE,
        "COL": COL
    }
