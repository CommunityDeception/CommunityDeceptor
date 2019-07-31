from igraph import Graph
from utils.partitionIO import save_partitions
from settings.master import GRAPH_SETTINGS


def pre_process():
    graph = Graph.Read_GML(GRAPH_SETTINGS['path'])
    partitions = GRAPH_SETTINGS['detection_func'](graph, **GRAPH_SETTINGS['func_args'])
    graph_name = GRAPH_SETTINGS['path'].split("/")[1].split(".")[0]
    save_partitions(f"partitions/{graph_name}.part", GRAPH_SETTINGS['path'], partitions)
