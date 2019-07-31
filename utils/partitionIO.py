import pickle

from igraph import Graph
from igraph.clustering import VertexClustering


def save_partitions(file_path, graph_path: str, partitions: VertexClustering):
    result = {
        "graph_path": graph_path,
        "membership": partitions.membership
    }  # raw format

    with open(file_path, "wb") as file:
        pickle.dump(result, file)


def load_partition(file_path, graph: Graph = None) -> VertexClustering:
    with open(file_path, "rb") as file:
        result = pickle.load(file)

        if not graph:
            graph = Graph.Read_GML(result["graph_path"])

    return VertexClustering(graph=graph, membership=result['membership'])
