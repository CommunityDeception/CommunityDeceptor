from math import log


def __inner_count(value):
    if not value:
        return 0
    else:
        return value * log(value, 2)


def __count_position_entropy_by_pre(edge, pre_position_entropy, total_degree, degree_distribute):
    src, des = edge
    src_now = (degree_distribute[src] + 1) / total_degree
    src_now = __inner_count(src_now)
    src_pre = degree_distribute[src] / total_degree
    src_pre = __inner_count(src_pre)

    des_now = (degree_distribute[des] + 1) / total_degree
    des_now = __inner_count(des_now)
    des_pre = degree_distribute[des] / total_degree
    des_pre = __inner_count(des_pre)

    return pre_position_entropy + (src_pre + des_pre) - des_now - src_now


def __count_resistance_by_pre(pre_resistance, src_des, total_degree, partitions_degree, partitions_volume):
    src, des = src_des

    if src == des:
        vs = partitions_volume[src]
        gs = vs - partitions_degree[src]
        differ = 0 - (vs - gs + 2) / total_degree * log(((vs + 2) / total_degree), 2) + (vs - gs) / total_degree * log(vs / total_degree, 2)

    else:
        src_volume = partitions_volume[src] + 1
        des_volume = partitions_volume[des] + 1

        src_degree = partitions_degree[src]
        des_degree = partitions_degree[des]

        src_pre = src_degree / total_degree * log((src_volume - 1) / total_degree, 2)
        des_pre = des_degree / total_degree * log((des_volume - 1) / total_degree, 2)

        src_now = src_degree / total_degree * log(src_volume / total_degree, 2)
        des_now = des_degree / total_degree * log(des_volume / total_degree, 2)

        differ = src_pre + des_pre - src_now - des_now

    resistance = pre_resistance + differ

    return resistance


def count_security_index_by_pre(pre_count, edge, src_des, total_degree, partitions_degree, partitions_volume, degree_distribute):
    pre_position_entropy, pre_resistance = pre_count
    position_entropy = __count_position_entropy_by_pre(edge, pre_position_entropy, total_degree, degree_distribute)
    resistance = __count_resistance_by_pre(pre_resistance, src_des, total_degree, partitions_degree, partitions_volume)
    security_index = resistance / position_entropy

    return security_index
