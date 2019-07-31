from anonymization.REM import REMAnonymize
from settings import master
from utils.partitionIO import load_partition


if __name__ == '__main__':
    partitions = load_partition("partitions/email.part")
    graph = partitions.graph
    single_modularity = REMAnonymize(graph=graph, partitions=partitions, **master.GRAPH_SETTINGS)
    single_modularity.run()
