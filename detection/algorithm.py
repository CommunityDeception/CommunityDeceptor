import random
import louvain as lv


def louvain(graph):
    lv.set_rng_seed(random.randint(1, 100000))
    raw_partitions = lv.find_partition(graph, lv.ModularityVertexPartition)

    return raw_partitions


def fast_greedy(graph):
    raw_partitions = graph.community_fastgreedy().as_clustering()

    return raw_partitions


def edge_betweenness(graph, **kwargs):
    raw_partitions = graph.community_edge_betweenness(**kwargs).as_clustering()

    return raw_partitions


def label_propagation(graph):
    raw_partitions = graph.community_label_propagation()

    return raw_partitions


def info_map(graph, **kwargs):
    raw_partitions = graph.community_infomap(**kwargs)

    return raw_partitions


def spinglass(graph, **kwargs):
    raw_partitions = graph.community_spinglass(**kwargs)

    return raw_partitions


def walk_trap(graph, **kwargs):
    raw_partitions = graph.community_walktrap(**kwargs).as_clustering()

    return raw_partitions


def leading_eigenvector(graph, **kwargs):
    raw_partitions = graph.community_leading_eigenvector(**kwargs)

    return raw_partitions
