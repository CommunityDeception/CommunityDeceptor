from math import sqrt


def count_max_proportion(source_community, now_partition):
    source_community = set(source_community)
    source_size = len(source_community)
    max_proportion = 0

    for target_community in now_partition:
        target_community = set(target_community)
        target_size = len(target_community)
        proportion = len(source_community.intersection(target_community)) / sqrt(source_size * target_size)

        if max_proportion < proportion:
            max_proportion = proportion

    return max_proportion
