import re
from enum import Enum


class Log(object):
    class LOG_TYPE(Enum):
        ADVANCE = 'Advance'
        NORMAL = 'Normal'
        RANDOM = 'Random'

    class LOG_ATTR(Enum):
        LOG_TYPE = 'log_type'
        START_TIME = 'start_time'
        GRAPH_NAME = 'graph_name'
        GRAPH_INFO = 'graph_info'
        FUNCTION = 'function'
        ADD_EDGES = 'add_edges'
        LOG_INTERVAL = 'log_interval'
        PARTITIONS_NUM = 'partitions'
        JACCARD = 'jaccard'
        SECURITY = 'security'
        RECALL = 'recall'
        NMI = 'nmi'
        MODULARITY = 'modularity'
        END_TIME = 'end_time'
        TIME_COST = 'time_cost'

    def __init__(self, raw_data_list):
        self.__raw_data_list = raw_data_list

        self.head_log_type = None
        self.head_start_time = None
        self.head_graph_name = None
        self.head_graph_info = None
        self.head_function = None
        self.head_add_edges = None
        self.head_log_interval = None
        self.head_partitions_num = None

        self.jaccard_index_list = list()
        self.security_index_list = list()
        self.recall_index_list = list()
        self.nmi_index_list = list()
        self.modularity_list = list()

        self.tail_end_time = None
        self.tail_time_cost = None

        self.__preprocess()

    def __preprocess(self):
        self.__analysis_head(self.__raw_data_list[0])
        self.__analysis_content(self.__raw_data_list[1])
        self.__analysis_tail(self.__raw_data_list[2])

    def __analysis_head(self, plain_text):
        raw_data_list = plain_text.split('\n')

        self.head_log_type = raw_data_list[0]
        self.head_start_time = raw_data_list[1].split(" : ")[1]
        self.head_graph_name = raw_data_list[2].split("/")[1]
        self.head_graph_info = raw_data_list[3].split(" : ")[1]
        self.head_add_edges = int(raw_data_list[4].split(": ")[1])
        self.head_function = raw_data_list[5].split(" : ")[1]
        self.head_log_interval = int(raw_data_list[7].split("  : ")[1])
        self.head_partitions_num = int(raw_data_list[8].split(": ")[1])

    def __analysis_tail(self, plain_text):
        raw_data_list = plain_text.split('\n')

        self.tail_end_time = raw_data_list[0].split(" : ")[1]
        self.tail_time_cost = float(raw_data_list[1].strip().split(':')[1].strip('s'))

    def __analysis_content(self, plain_text):
        raw_data_list = plain_text.split('\n')

        for line in raw_data_list:
            if not line:
                continue
            jaccard, recall, security, modularity, nmi = re.findall("\((.*?)\)", line)
            self.jaccard_index_list.append(float(jaccard))
            self.recall_index_list.append(float(recall))
            self.security_index_list.append(float(security))
            self.modularity_list.append(float(modularity))
            self.nmi_index_list.append(float(nmi))
