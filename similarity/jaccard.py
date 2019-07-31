def __count_common_parts(a_partitions, b_partitions):
    result = 0

    for a_module in a_partitions:
        for b_module in b_partitions:
            a_module = set(a_module)
            b_module = set(b_module)

            intersection_length = len(a_module.intersection(b_module))
            if intersection_length > 1:
                result += intersection_length * (intersection_length - 1) / 2

    return result


def __count_combinations(modules):
    result = 0

    for module in modules:
        length = len(module)
        result += length * (length - 1) / 2

    return result


def count_jaccard_index_and_recall_index(a_partitions, b_partitions):
    r = __count_common_parts(a_partitions, b_partitions)
    p = __count_combinations(a_partitions)
    q = __count_combinations(b_partitions)

    u_v_2r = p + q

    jaccard_index = r / (u_v_2r - r)
    recall_index = r / p

    return jaccard_index, recall_index
