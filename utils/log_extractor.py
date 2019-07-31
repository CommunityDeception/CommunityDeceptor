from utils.log import Log
from collections import defaultdict


class LogExtractor(object):
    def __init__(self, path):
        self.__log_path = path
        self.__result = list()

        self.__preprocess()

    def __start(self):
        self.__log = open(self.__log_path, "r")

    def __quit(self):
        self.__log.close()

    def __get_section(self):
        pass

    def __analysis(self):
        log = self.__log
        plain_text = ''

        for line in log:
            if line.strip():
                plain_text += line

        raw_data = [line for line in plain_text.split("=" * 60 + "\n") if line]
        assert not len(raw_data) % 3

        sections = [raw_data[i: i + 3] for i in range(0, len(raw_data), 3)]

        for sec in sections:
            log = Log(sec)
            self.__result.append(log)

    def __get_attrs(self, log_type):
        result = defaultdict(list)
        count = 0

        for log in self.__result:
            if log_type in log.head_log_type:
                result['jaccard'].append(log.jaccard_index_list)
                result['recall'].append(log.recall_index_list)
                result['security'].append(log.security_index_list)
                result['modularity'].append(log.modularity_list)
                result['nmi'].append(log.nmi_index_list)
                count += 1

        return result, count

    def get_average(self, log_type):
        data, size = self.__get_attrs(log_type)
        average = defaultdict(list)
        for key in data.keys():
            attr = data[key]

            for i in range(len(attr[0])):
                var = sum([j[i] for j in attr]) / size
                average[key].append(round(var, 6))

        return average

    def __preprocess(self):
        self.__start()
        self.__analysis()
        self.__quit()


if __name__ == '__main__':
    log_extractor = LogExtractor('../logs/jazz_infomap_1000_10_30.log')
    print(log_extractor.get_average('Advance'))
