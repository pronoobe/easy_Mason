from copy import deepcopy
from itertools import combinations

import networkx as nx


class signal_graph(object):
    def __init__(self, node_num):
        self.graph = nx.DiGraph()
        nodes = [x for x in range(1, node_num + 1)]
        super().__init__()
        self.graph.add_nodes_from(nodes)
        self.transfer_func = None
        self._graph_plot = nx.DiGraph()
        self._graph_plot.add_nodes_from(nodes)

    def set_link(self, from_node, to_node, transfer_function):
        self.add_edge(from_node, to_node, weight=transfer_function)

    @staticmethod
    def is_dependent(loop_list):
        list_len = len(loop_list)
        for i in range(list_len):
            list1 = loop_list[i]
            for j in range(list_len):
                if j != i:
                    list2 = loop_list[j]
                    for node in list2:
                        if node in list1:
                            return False
        return True

    @staticmethod
    def path_loop_dependent(path, loop):
        for i in path:
            if i in loop:
                return False
        return True

    def find_all_dependent_ring(self, rings: list):
        res = [[] for _ in range(len(rings) + 1)]
        list_len = len(rings)
        for i in range(2, list_len + 1):
            prob_rings = list(combinations(rings, i))
            for ring in prob_rings:
                # pprint(ring)
                if self.is_dependent(ring):
                    # print(11111111)
                    res[i].append(ring)
        return res

    @staticmethod
    def warp_res(single_loops, res_init):
        """
        包装结果
        :param single_loops:
        :param res_init:
        :return:
        """
        for i, loop in enumerate(single_loops):
            single_loops[i] = [loop]
        res_init[1] = single_loops
        return res_init

    def get_path_delta(self, path, loop_res):
        """
        第二步
        :param path:
        :param loop_res:
        :return:
        """
        res = deepcopy(loop_res)
        for i, dependent_conditions in enumerate(loop_res):
            for j, loops in enumerate(dependent_conditions):
                for k, loop in enumerate(loops):
                    res[i][j] = list(res[i][j])
                    if not self.path_loop_dependent(path, loop):
                        res[i][j] = []
        return self.get_loop_delta(dependent_loops=res)

    def get_upper_delta(self, from_node, to_node):
        res = []
        paths, loops = list(nx.all_simple_paths(self.graph, from_node, to_node)), list(nx.simple_cycles(self.graph))
        all_loop_conditions = self.find_all_dependent_ring(loops)
        all_loop_conditions = self.warp_res(deepcopy(loops), deepcopy(all_loop_conditions))
        # pprint(all_loop_conditions)
        for path in paths:
            res.append(self.get_path_delta(path, all_loop_conditions))
            # pprint(get_path_delta(path, all_loop_conditions))
        res_expr = 0
        path_expr = []
        for i in paths:
            single_path_expr = 1
            for j in range(len(i) - 1):
                single_path_expr *= self.graph.get_edge_data(i[j], i[j + 1])['weight']
            path_expr.append(single_path_expr)
        for i in range(len(res)):
            res_expr += path_expr[i] * res[i]
        return res_expr

    def get_loop_delta(self, dependent_loops=None):
        loops = list(nx.simple_cycles(self.graph))
        if dependent_loops is None:
            dependent_loops = self.warp_res(deepcopy(loops), deepcopy(list(self.find_all_dependent_ring(loops))))
        delta = 1
        # pprint(dependent_loops)
        for j, single_condition_loops in enumerate(dependent_loops):
            if len(single_condition_loops) != 0:
                single_condition_res = 1
                for loops_group in single_condition_loops:
                    single_loop_res = 1
                    for loop in loops_group:
                        for i in range(len(loop) - 1):
                            single_loop_res *= self.graph.get_edge_data(loop[i], loop[i + 1])['weight']
                        single_loop_res *= self.graph.get_edge_data(loop[-1], loop[0])['weight']
                    if single_loop_res != 1:
                        single_condition_res += single_loop_res
                if j % 2 == 0:
                    single_condition_res *= -1
                if single_condition_res != 1:
                    delta += single_condition_res
        return 1 - delta

    def add_edge(self, x, y, weight=1):
        print(f"added transfer function {weight} from {x} to {y}")
        self.graph.add_edge(x, y, weight=weight)
        self._graph_plot.add_edge(x, y, weight=str(weight))

    def get_transfer_function(self, x, y):
        self.transfer_func = self.get_upper_delta(x, y) / self.get_loop_delta()
        return self.transfer_func

    def __repr__(self):
        if self.transfer_func:
            return f"mason graph contains {len(list(self.graph.nodes))} nodes \n transfer function is {str(self.transfer_func)}"
        else:
            return f"mason_graph contains {len(list(self.graph.nodes))} nodes \n transfer function unknown"

    def __str__(self):
        if self.transfer_func:
            from sympy import latex
            return latex(self.transfer_func)

    def plot(self):
        import matplotlib.pyplot as plt
        ax = plt.subplot(111)
        plt.figure(figsize=(10, 5))
        ax.text(-0.2, 0.2, r"$" + str(self) + r"$", fontsize=20, color="red")
        plt.show()

if __name__ == '__main__':
    from pprint import pprint

    pprint = pprint
    from sympy import Symbol

    G = signal_graph(9)
    G.add_edge(1, 2, 1)
    G.add_edge(2, 3, Symbol("G1"))
    G.add_edge(3, 4, Symbol("G2"))
    G.add_edge(4, 5, Symbol("G3"))
    G.add_edge(5, 6, Symbol("G4"))
    G.add_edge(6, 7, Symbol("G5"))
    G.add_edge(7, 8, Symbol("G6"))
    G.add_edge(8, 9, 1)
    G.add_edge(2, 4, Symbol("G7"))
    G.add_edge(3, 7, Symbol("G8"))
    G.add_edge(4, 3, -Symbol("H1"))
    G.add_edge(7, 4, -Symbol("H4"))
    G.add_edge(6, 5, -Symbol("H2"))
    G.add_edge(8, 7, -Symbol("H3"))
    G.add_edge(8, 2, -Symbol("H5"))
    # loops = list(nx.simple_cycles(G.graph))
    # sc = list(nx.simple_cycles(G.graph))
    # pprint(list(G.find_all_dependent_ring(loops)))
    # r = G.get_loop_delta()
    # print(G.get_loop_delta())
    G.get_transfer_function(1, 9)
    # gs = str(G)
    # G.plot()
    from sympy import init_printing as ppprint
    ppprint(use_unicode=True)
    print(G.transfer_func)
    # print(str(G))
    # pprint(r)
