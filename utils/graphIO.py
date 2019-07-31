import networkx as nx


def mat2gml(source_path, target_path):
    source = open(source_path, 'rb')
    target = open(target_path, 'wb')

    next(source)
    graph = nx.Graph()

    for line in source:
        src, des = line.split()
        src = int(src)
        des = int(des)

        graph.add_edge(src, des)

    nx.write_gml(graph, target, int)

    source.close()
    target.close()


if __name__ == '__main__':
    mat2gml("C:\\Users\\34281\\Desktop\\livemocha\\out.livemocha", "..\\samples\\livemocha.gml")
