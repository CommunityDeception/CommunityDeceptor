from math import log


def __count_position_entropy(graph):
    total_degree = 2 * len(graph.es)
    position_entropy = 0

    for vertex in graph.vs:
        var = vertex.degree() / total_degree
        position_entropy -= var * log(var, 2)

    return position_entropy


def __count_resistance(graph, partitions):
    total_degree = 2 * graph.ecount()
    resistance = 0

    for part in partitions:
        part_volume = sum(graph.degree(part))
        subgraph = graph.subgraph(part)
        subgraph_degree = 2 * subgraph.ecount()

        resistance -= subgraph_degree / total_degree * log(part_volume / total_degree, 2)

    return resistance


def count_security_index(graph, partitions):
    position_entropy = __count_position_entropy(graph)
    resistance = __count_resistance(graph, partitions)
    security_index = resistance / position_entropy

    return security_index


def count_ratio(out_degree, degree):
    return out_degree / degree


def count_value(x_degree, y_degree, x_out_degree, y_out_degree):
    return x_out_degree / 2 * x_degree*(x_degree - 1) + y_out_degree / 2 * y_degree*(y_degree - 1)
