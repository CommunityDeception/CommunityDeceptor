from math import log


def __count_pre_position_entropy(graph):
    total_degree = 2 * graph.ecount() + 2
    pre_position_entropy = 0

    for node in graph.vs:
        var = graph.degree(node) / total_degree
        pre_position_entropy -= var * log(var, 2)

    return pre_position_entropy


def __count_pre_resistance(graph, partitions, partitions_degree, partitions_volume):
    total_degree = 2 * graph.ecount() + 2
    resistance = 0

    for index, part in enumerate(partitions):
        part_volume = partitions_volume[index]
        part_degree = partitions_degree[index]

        resistance -= part_degree / total_degree * log(part_volume / total_degree, 2)

    return resistance


def count_pre_security_index(graph, partitions, partitions_degree, partitions_volume):
    pre_position_entropy = __count_pre_position_entropy(graph)
    pre_resistance = __count_pre_resistance(graph, partitions, partitions_degree, partitions_volume)

    return pre_position_entropy, pre_resistance
