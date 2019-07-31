import logging.config
import sys
import time
from typing import List

from igraph import Graph
from igraph.clustering import VertexClustering

from settings import master
from similarity.jaccard import count_jaccard_index_and_recall_index
from utils.counter_pre import count_security_index_by_pre
from utils.pre_counter import count_pre_security_index
from utils.timer import time_mark

logging.config.dictConfig(master.LOGGING_SETTINGS)
logger = logging.getLogger('normal')


class REMAnonymize(object):
    def __init__(self, graph, edges_sum, detection_func, func_args, interval, partitions, path, **kwargs):
        self.__graph: Graph = graph
        self.__edges_sum = edges_sum
        self.__detection_func = detection_func
        self.__func_args: dict = func_args
        self.__interval = interval
        self.__partitions: VertexClustering = partitions
        self.__path = path

        self.__start_time = time.time()
        self.__total_edge_set: set = set()
        self.__partitions_degree: List[int] = list()
        self.__partitions_volume: List[int] = list()
        self.__degree_distribute: List[int] = list()
        self.__sorted_partitions: List[List[int]] = list()
        self.__partitions_num = 0
        self.__available_edges = list()
        self.__end_time = None

    def __start(self):
        logger.info("=" * 60)
        logger.info("REMAnonymize")
        logger.info(f'Time : {time_mark(self.__start_time)}')
        logger.info(f'Graph: {self.__path}')
        logger.info(f'Info : {self.__graph.vcount()} {self.__graph.ecount()}')
        logger.info(f'Edges: {self.__edges_sum}')
        logger.info(f'Func : {self.__detection_func.__name__}')
        logger.info(f'Args : {self.__func_args}')
        logger.info(f'Gap  : {self.__interval}')
        logger.info(f'Parts: {len(self.__partitions)}')
        logger.info("=" * 60)

    def __quit(self):
        self.__end_time = time.time()
        logger.info("=" * 60)
        logger.info(f'Time : {time_mark(self.__end_time)}')
        logger.info(f'Total: {(self.__end_time - self.__start_time): 10.4f} s')
        logger.info("=" * 60)
        logger.info("\n\n")

    def __preprocess(self):
        self.__total_edge_set = set(self.__graph.get_edgelist())
        self.__partitions_num = len(self.__partitions)
        self.__degree_distribute = self.__graph.degree(self.__graph.vs)

        self.__set_necessary_info()

    def __set_necessary_info(self):
        for index, part in enumerate(self.__partitions):
            subgraph: Graph = self.__partitions.subgraph(index)
            self.__partitions_degree.append(2 * subgraph.ecount())
            self.__partitions_volume.append(sum(self.__graph.degree(part)))
            self.__sorted_partitions.append(sorted(part, key=lambda x: self.__graph.degree(x)))

    def __get_available_edges(self):
        available_edges = list()
        degree_distribute = self.__degree_distribute

        for si in range(self.__partitions_num):
            for ti in range(si, self.__partitions_num):

                s_order, t_order = self.__sorted_partitions[si], self.__sorted_partitions[ti]

                u, v = s_order[0], t_order[0]
                if degree_distribute[u] > degree_distribute[v]:
                    u, v = v, u
                    s_order, t_order = t_order, s_order

                u_neighbors = set(self.__graph.neighbors(u))

                for node in t_order:
                    if node not in u_neighbors:
                        v = node
                        break

                du, dv = degree_distribute[u], degree_distribute[v]
                upper_bound = du + dv

                for i in t_order:
                    if degree_distribute[i] >= dv:
                        edge = (u, v) if u < v else (v, u)
                        available_edges.append(edge)
                        break

                    else:
                        i_neighbors = set(self.__graph.neighbors(i))

                        for j in s_order:
                            if j not in i_neighbors:
                                break

                        di, dj = degree_distribute[i], degree_distribute[j]
                        if di + dj < upper_bound:
                            edge = (i, j) if i < j else (j, i)
                            if edge not in self.__total_edge_set:
                                available_edges.append(edge)

        self.__available_edges = available_edges

    def __choose_edge(self):
        self.__get_available_edges()

        partitions = self.__partitions
        optimal_edge = None
        edge_partitions = None
        min_security = sys.maxsize
        total_degree = 2 * self.__graph.ecount()
        degree_distribute = self.__degree_distribute
        membership = partitions.membership

        pre_count = count_pre_security_index(self.__graph, partitions, self.__partitions_degree, self.__partitions_volume)

        for edge in self.__available_edges:
            src_des = (membership[edge[0]], membership[edge[1]])
            security_index = count_security_index_by_pre(pre_count, edge, src_des, total_degree + 2, self.__partitions_degree, self.__partitions_volume, degree_distribute)

            if security_index < min_security:
                min_security = security_index
                optimal_edge = edge
                edge_partitions = src_des

        self.__graph.add_edge(*optimal_edge)
        self.__total_edge_set.add(optimal_edge)
        self.__partitions_volume[edge_partitions[0]] += 1
        self.__partitions_volume[edge_partitions[1]] += 1
        self.__degree_distribute[optimal_edge[0]] += 1
        self.__degree_distribute[optimal_edge[1]] += 1

        self.__sorted_partitions[edge_partitions[0]].sort(key=lambda x: self.__graph.degree(x))
        self.__sorted_partitions[edge_partitions[1]].sort(key=lambda x: self.__graph.degree(x))

        return min_security

    def __should_count(self, count):
        return divmod(count, self.__interval)[1]

    def __anonymize(self):
        edge_sum = self.__edges_sum
        pre_partitions = self.__partitions
        count = 1

        while count <= edge_sum:
            try:
                security_index = self.__choose_edge()
            except ValueError:
                logger.info(f'{count:<5d} Not enough edges to add.')
                return -1

            if not self.__should_count(count):
                fin_partitions = self.__detection_func(self.__graph, **self.__func_args)

                jaccard_index, recall_index = count_jaccard_index_and_recall_index(pre_partitions, fin_partitions)
                modularity = self.__graph.modularity(pre_partitions.membership)
                NMI = pre_partitions.compare_to(fin_partitions, method="NMI")

                logger.info(f"{count:<5d} jaccard index: ({jaccard_index:8.7f}), recall index: ({recall_index:8.7f}), "
                            f"security_index: ({security_index:8.7f}), modularity: ({modularity:8.7f}), NMI: ({NMI:8.7f})")

            count += 1

    def run(self):
        self.__preprocess()
        self.__start()
        self.__anonymize()
        self.__quit()
