from solution import Graph, Vertex
from typing import TypeVar
import random
import gc
from timeit import default_timer
from matplotlib import pyplot as plt

random.seed(331)

T = TypeVar('T')

def graph_gen(num_nodes: int, connectivity: float) -> Graph:
    """
    Creates a graph object sufficient conditions for a_star to be effective
    Nodes will be contained within a circle centered at the origin
    :param num_nodes: number of nodes in the graph
    :param connectivity: probability two nodes will be connected
    :return: the graph generated
    """
    graph = Graph()
    while graph.size < num_nodes:
        x, y = random.randrange(-num_nodes, num_nodes), random.randrange(-num_nodes, num_nodes)
        if (x**2 + y**2) < num_nodes**2:
            graph.vertices[f"{x},{y}"] = Vertex(f"{x},{y}", x, y)
            graph.size += 1

    edges = [(v1,v2) for v1 in graph.vertices for v2 in graph.vertices]
    random.shuffle(edges)
    edges = edges[:int((connectivity*num_nodes*num_nodes + 1)//1)]
    for edge in edges:
        v1, v2 = graph.vertices[edge[0]], graph.vertices[edge[1]]
        weight = (abs(v1.x - v2.x) + abs(v1.y - v2.y))
        weight *= (1 + random.random())
        graph.add_to_graph(edge[0], edge[1], weight)

    return graph

class StackQueue:
    """
    DLL based structure with FIFO and LIFO functionality
    Attributes:
        - FIFO - bool: indicates operation mode for StackQueue
        - self.head  : head of underlying list
        - self.tail  : tail of underlying list
    """
    def __init__(self, FIFO = True):
        """
        Creates a StackQueue
        :param FIFO: indicates operation mode for StackQueue
        :return: None
        """
        self.FIFO = FIFO
        self.head = self.tail = None

    def push(self, val: T) -> None:
        """
        Pushes to top
        :param val: value to insert
        :return: None
        """
        node = type('', (object,), {"val": val, "next": None, "prev": self.tail})
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = self.tail = node

    def pop(self) -> T:
        """
        Pops a value
        :return: the value removed
        """
        if self.head is None:
            return
        elif self.head is self.tail:
            result = self.head.val
            self.head = self.tail = None
        elif self.FIFO:
            result = self.head.val
            self.head = self.head.next
            self.head.prev = None
        else:
            result = self.tail.val
            self.tail = self.tail.prev
            self.tail.next = None
        return result

    def clear(self):
        """
        Resets the structure
        :return: None
        """
        self.head = self.tail = None


def search(graph: Graph, start_id: str, end_id: str, struct: StackQueue) -> bool:
    """
    performs BFS/DFS
    :param graph: the graph to search
    :param start_id: where to begin search
    :param end_id: search target
    :param struct: a StackQueue
    :return: True if a path from start to end exists, else False
    """
    visited = set()
    struct.push(start_id)
    while struct.head is not None:
        v = struct.pop()
        if v == end_id:
            return True
        if v not in visited:
            visited.add(v)
            for vert in graph.vertices[v].adj:
                struct.push(vert)
    return False

def avg_search(graph: Graph, struct: StackQueue) -> float:
    """
    returns the average BFS/DFS search time on a graph
    :param graph: the graph to search
    :param struct: determines which search to perform
    :return: avg search time in seconds
    """
    total = 0.
    pairs = [(v1, v2) for v1 in graph.vertices for v2 in graph.vertices]
    random.shuffle(pairs)
    for i, pair in enumerate(pairs):
        if not i%10:
            struct.clear()
            start = default_timer()
            search(graph, pair[0], pair[1], struct)
            total += default_timer() - start
    return (total*10)/graph.size**2

def test1():
    # Begin plotting
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,8))
    ax1.set_facecolor('ivory')
    ax2.set_facecolor('ivory')
    ax1.title.set_text('BFS Average Time')
    ax2.title.set_text('DFS Average Time')
    ax1.set_xlabel('Graph Size')
    ax2.set_xlabel('Graph Size')
    ax1.set_ylabel('Average Search Time (s)')
    ax2.set_ylabel('Average Search Time (s)')

    # BFS
    ax1.plot(list(range(20,185,15)), [avg_search(graph_gen(size, .001), StackQueue()) for size in range(20,185,15)],
            color='darkblue', label='Connectivity Factor: .001')
    ax1.plot(list(range(20,185,15)), [avg_search(graph_gen(size, .01), StackQueue()) for size in range(20,185,15)],
            color='navy', label='Connectivity Factor: .01')
    ax1.plot(list(range(20,185,15)), [avg_search(graph_gen(size, .05), StackQueue()) for size in range(20,185,15)],
            color='midnightblue', label='Connectivity Factor: .05')

    # DFS
    ax2.plot(list(range(20,185,15)), [avg_search(graph_gen(size, .001), StackQueue()) for size in range(20,185,15)],
            color='orangered', label='Connectivty Factor: .001')
    ax2.plot(list(range(20,185,15)), [avg_search(graph_gen(size, .01), StackQueue()) for size in range(20,185,15)],
            color='red', label='Connectivity Factor: .01')
    ax2.plot(list(range(20,185,15)), [avg_search(graph_gen(size, .05), StackQueue()) for size in range(20,185,15)],
            color='darkred', label='Connectivity Factor: .05')

    ax1.legend(loc='best')
    ax2.legend(loc='best')
    plt.show()

def test2():
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,8))
    ax1.set_facecolor('ivory')
    ax2.set_facecolor('ivory')
    ax1.title.set_text('Dijkstra vs. AStar (Euclidean Dist)')
    ax2.title.set_text('Dijkstra vs. AStar (Taxicab Dist)')
    ax1.set_xlabel('Graph Size')
    ax2.set_xlabel('Graph Size')
    ax1.set_ylabel('Average Search Time (s)')
    ax2.set_ylabel('Average Search Time (s)')

    # generate data
    dijkstra_times = []
    euclidean_astar_times = []
    taxicab_astar_times = []
    for size in range(20, 245, 15):
        graph = graph_gen(size, .075)

        dijkstra_total = 0.
        euclidean_astar_total = 0.
        taxicab_astar_total = 0.
        pairs = [(v1, v2) for v1 in graph.vertices for v2 in graph.vertices]
        random.shuffle(pairs)
        for i, pair in enumerate(pairs):
            if not i%15:
                start = default_timer()
                graph.dijkstra(pair[0], pair[1])
                dijkstra_total += default_timer() - start
                graph.reset_vertices()

                start = default_timer()
                graph.a_star(pair[0], pair[1], Vertex.euclidean_distance)
                euclidean_astar_total += default_timer() - start
                graph.reset_vertices()

                start = default_timer()
                graph.a_star(pair[0], pair[1], Vertex.taxicab_distance)
                taxicab_astar_total += default_timer() - start
                graph.reset_vertices()

        dijkstra_times.append(dijkstra_total*15/size**2)
        euclidean_astar_times.append(euclidean_astar_total*15/size**2)
        taxicab_astar_times.append(taxicab_astar_total*15/size**2)

    ax1.plot(range(20, 245, 15), dijkstra_times, color='red', label='Dijkstra')
    ax1.plot(range(20, 245, 15), euclidean_astar_times, color='blue', label='AStar')

    ax2.plot(range(20, 245, 15), dijkstra_times, color='red', label='Dijkstra')
    ax2.plot(range(20, 245, 15), taxicab_astar_times, color='blue', label='AStar')

    ax1.legend(loc='best')
    ax2.legend(loc='best')
    plt.show()

if __name__ == '__main__':
    #test1()
    test2()
