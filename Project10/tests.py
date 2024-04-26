import unittest, string, math, random, cProfile
from xml.dom import minidom
from numpy import matrix

from solution import Graph, Vertex

class GraphTests(unittest.TestCase):
    """
    Begin Graph Part 1 Tests
    """

    def test_deg(self):

        # (1) test a-->b and a-->c
        vertex = Vertex('a')
        vertex.adj['b'] = 1
        self.assertEqual(vertex.deg(), 1)
        vertex.adj['c'] = 3
        assert vertex.deg() == 2

        # (2) test a-->letter for all letters in alphabet
        vertex = Vertex('a')
        for i, char in enumerate(string.ascii_lowercase):
            self.assertEqual(vertex.deg(), i)
            vertex.adj[char] = i

    def test_get_outgoing_edges(self):

        # (1) test a-->b and a-->c
        vertex = Vertex('a')
        solution = {('b', 1), ('c', 2)}
        vertex.adj['b'] = 1
        vertex.adj['c'] = 2
        subject = vertex.get_outgoing_edges()
        self.assertEqual(subject, solution)

        # (2) test empty case
        vertex = Vertex('a')
        solution = set()
        subject = vertex.get_outgoing_edges()
        self.assertEqual(subject, solution)

        # (3) test a-->letter for all letters in alphabet
        for i, char in enumerate(string.ascii_lowercase):
            vertex.adj[char] = i
            solution.add((char, i))
        subject = vertex.get_outgoing_edges()
        self.assertEqual(subject, solution)

    def test_get_vertex_by_id(self):

        graph = Graph()

        # (1) test basic vertex object
        vertex_a = Vertex('a')
        graph.vertices['a'] = vertex_a
        subject = graph.get_vertex_by_id('a')
        self.assertEqual(subject, vertex_a)

        # (2) test empty case
        subject = graph.get_vertex_by_id('b')
        self.assertIsNone(subject)

        # (3) test case with adjacencies
        vertex_b = Vertex('b')
        for i, char in enumerate(string.ascii_lowercase):
            vertex_b.adj[char] = i
        graph.vertices['b'] = vertex_b
        subject = graph.get_vertex_by_id('b')
        self.assertEqual(subject, vertex_b)

    def test_get_all_vertices(self):

        graph = Graph()
        solution = set()

        # (1) test empty graph
        subject = graph.get_all_vertices()
        self.assertEqual(subject, solution)

        # (2) test single vertex
        vertex = Vertex('$')
        graph.vertices['$'] = vertex
        solution.add(vertex)
        subject = graph.get_all_vertices()
        self.assertEqual(subject, solution)

        # (3) test multiple vertices
        graph = Graph()
        solution = set()
        for i, char in enumerate(string.ascii_lowercase):
            vertex = Vertex(char)
            graph.vertices[char] = vertex
            solution.add(vertex)
        subject = graph.get_all_vertices()
        self.assertEqual(subject, solution)

    def test_get_edge_by_ids(self):

        graph = Graph()

        # (1) neither end vertex exists
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(subject)

        # (2) one end vertex exists
        graph.vertices['a'] = Vertex('a')
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(subject)

        # (3) both end vertices exist, but no edge
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertIsNone(subject)

        # (4) a -> b exists but b -> a does not
        graph.vertices.get('a').adj['b'] = 331
        subject = graph.get_edge_by_ids('a', 'b')
        self.assertEqual(subject, ('a', 'b', 331))
        subject = graph.get_edge_by_ids('b', 'a')
        self.assertIsNone(subject)

        # (5) connect all vertices to center vertex and return all edges
        graph.vertices['$'] = Vertex('$')
        for i, char in enumerate(string.ascii_lowercase):
            graph.vertices[char] = Vertex(char)
            graph.vertices.get('$').adj[char] = i
        for i, char in enumerate(string.ascii_lowercase):
            subject = graph.get_edge_by_ids('$', char)
            self.assertEqual(subject, ('$', char, i))

    def test_get_all_edges(self):

        graph = Graph()

        # (1) test empty graph
        subject = graph.get_all_edges()
        self.assertEqual(subject, set())

        # (2) test graph with vertices but no edges
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        subject = graph.get_all_edges()
        self.assertEqual(subject, set())

        # (3) test graph with one edge
        graph.vertices.get('a').adj['b'] = 331
        subject = graph.get_all_edges()
        self.assertEqual(subject, {('a', 'b', 331)})

        # (4) test graph with two edges
        graph = Graph()
        graph.vertices['a'] = Vertex('a')
        graph.vertices['b'] = Vertex('b')
        graph.vertices.get('a').adj['b'] = 331
        graph.vertices.get('b').adj['a'] = 1855
        subject = graph.get_all_edges()
        solution = {('a', 'b', 331), ('b', 'a', 1855)}
        self.assertEqual(subject, solution)

        # (5) test entire alphabet graph
        graph = Graph()
        solution = set()
        for i, char in enumerate(string.ascii_lowercase):
            graph.vertices[char] = Vertex(char)
            for j, jar in enumerate(string.ascii_lowercase):
                if i != j:
                    graph.vertices.get(char).adj[jar] = 26 * i + j
                    solution.add((char, jar, 26 * i + j))

        subject = graph.get_all_edges()
        self.assertEqual(subject, solution)

    """
    End of Graphs Part 1 Tests
    """

    """
    Begin Graph Part 2 Tests
    """

    def test_dijkstra_basic(self):
        """Basic Test cases"""
        graph = Graph()

        # # (1) test on empty graph
        # subject = graph.dijkstra('a', 'b')
        # self.assertEqual(subject, ([], 0))
        #
        # # (2) test on graph missing begin or dest
        # graph.add_to_graph('a')
        # subject = graph.dijkstra('a', 'b')
        # self.assertEqual(subject, ([], 0))
        # subject = graph.dijkstra('b', 'a')
        # self.assertEqual(subject, ([], 0))
        #
        # # (3) test on single edge
        # graph = Graph()
        # graph.add_to_graph('a', 'b', 331)
        # subject = graph.dijkstra('a', 'b')
        # self.assertEqual(subject, (['a', 'b'], 331))
        #
        # # (4) test on two edges
        # graph = Graph()
        # graph.add_to_graph('a', 'b', 331)
        # graph.add_to_graph('b', 'c', 100)
        # subject = graph.dijkstra('a', 'c')
        # self.assertEqual(subject, (['a', 'b', 'c'], 431))
        #
        # # (4) test where no path exists
        # graph = Graph()
        # graph.add_to_graph('a', 'b')
        # subject = graph.dijkstra('b', 'a')
        # self.assertEqual(subject, ([], 0))

        # === (A) Grid graph tests ===#
        graph = Graph()

        # (1) test on nxn grid from corner to corner: should shoot diagonal
        # (shortest path is unique, so each heuristic will return the same path)
        grid_size = 5
        for x in range(grid_size):
            for y in range(grid_size):
                idx = f"{x},{y}"
                graph.vertices[idx] = Vertex(idx, x, y)
        for x in range(grid_size):
            for y in range(grid_size):
                if x < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y}", 1)
                    graph.add_to_graph(f"{x + 1},{y}", f"{x},{y}", 1)
                if y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x},{y + 1}", 1)
                    graph.add_to_graph(f"{x},{y + 1}", f"{x},{y}", 1)
                if x < grid_size - 1 and y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", math.sqrt(2))
                    graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", math.sqrt(2))

        subject = graph.dijkstra('0,0', '4,4')
        self.assertEqual(subject[0], ['0,0', '1,1', '2,2', '3,3', '4,4'])
        self.assertAlmostEqual(subject[1], (grid_size - 1) * math.sqrt(2))
        graph.reset_vertices()

        # (2) test on nxn grid with penalty for shooting diagonal
        # (shortest path is not unique, so each heuristic will return a different path)
        for x in range(grid_size - 1):
            for y in range(grid_size - 1):
                graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", 3)
                graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", 3)

        subject = graph.dijkstra('0,0', '4,4')
        self.assertEqual(subject, (['0,0', '1,0', '2,0', '3,0', '4,0', '4,1', '4,2', '4,3', '4,4'], 8))
        graph.reset_vertices()

    def test_dijkstra_comprehensive(self):
        # === (B) Tollway graph tests ===#
        graph = Graph(csvf='test_csvs/astar/tollway_graph_csv.csv')
        # now must set of coordinates for each vertex:
        positions = [(0, 0), (2, 0), (4, 0), (7, 0), (10, 0), (12, 0), (2, 5), (6, 4), (12, 5), (5, 9), (8, 8), (12, 8),
                     (8, 10), (0, 2),
                     (4, 2), (9, 2), (9, -2), (7, 6), (8, 11), (14, 8)]

        for index, v_id in enumerate(list(graph.vertices)):
            graph.vertices[v_id].x, graph.vertices[v_id].y = positions[index]

        # (3) test Franklin Grove to Northbrook shortest path in both directions
        # (shortest path is unique, so each heuristic will return the same path)
        subject = graph.dijkstra('Franklin Grove', 'Northbrook')
        solution = (['Franklin Grove', 'A', 'B', 'G', 'J', 'M', 'Northbrook'], 22)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

        subject = graph.dijkstra('Northbrook', 'Franklin Grove')
        solution = (['Northbrook', 'M', 'J', 'G', 'B', 'A', 'Franklin Grove'], 22)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

        # (4) test Franklin Grove to Joliet shortest path - bypass slow path
        # (shortest path is unique, so each heuristic will return the same path)
        subject = graph.dijkstra('Franklin Grove', 'Joliet')
        solution = (['Franklin Grove', 'A', 'B', 'G', 'H', 'D', 'E', 'Joliet'], 35)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

        subject = graph.dijkstra('Joliet', 'Franklin Grove')
        solution = (['Joliet', 'E', 'D', 'H', 'G', 'B', 'A', 'Franklin Grove'], 35)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

        # (5) test Joliet to Chicago shortest path - bypass slow path
        # (shortest path is unique, so each heuristic will return the same path)
        subject = graph.dijkstra('Joliet', 'Chicago')
        solution = (['Joliet', 'E', 'D', 'H', 'G', 'J', 'K', 'L', 'Chicago'], 35)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

        subject = graph.dijkstra('Chicago', 'Joliet')
        solution = (['Chicago', 'L', 'K', 'J', 'G', 'H', 'D', 'E', 'Joliet'], 35)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

        # (6) test Northbrook to Belvidere - despite equal path lengths, A* heuristic will always prefer search to the left
        # (both heuristics will prefer the same path)
        subject = graph.dijkstra('Northbrook', 'Belvidere')
        solution = (['Northbrook', 'M', 'J', 'K', 'Belvidere'], 8)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

        subject = graph.dijkstra('Belvidere', 'Northbrook')
        solution = (['Belvidere', 'K', 'J', 'M', 'Northbrook'], 8)
        self.assertEqual(subject, solution)
        graph.reset_vertices()

    def test_a_star_basic(self):

        # === Edge Cases === #

        # (1) test on empty graph
        graph = Graph()
        subject = graph.a_star('a', 'b', lambda v1, v2 : 0)
        self.assertEqual(subject, ([], 0))

        # (2) start/end vertex does not exist
        graph = Graph()
        graph.add_to_graph('a')
        # (2.1) start vertex
        subject = graph.a_star('b','a', lambda v1, v2 : 0)
        self.assertEqual(subject, ([], 0))
        # (2.2) end vertex
        subject = graph.a_star('a', 'b', lambda v1, v2 : 0)
        self.assertEqual(subject, ([], 0))

        # (3) test for path which does not exist
        graph = Graph()
        graph.add_to_graph('a', 'b')
        subject = graph.a_star('b', 'a', lambda v1, v2 : 0)
        self.assertEqual(subject, ([], 0))


        # === (A) Grid graph tests ===#
        graph = Graph()

        # (1) test on nxn grid from corner to corner: should shoot diagonal
        # (shortest path is unique, so each heuristic will return the same path)
        grid_size = 5
        for x in range(grid_size):
            for y in range(grid_size):
                idx = f"{x},{y}"
                graph.vertices[idx] = Vertex(idx, x, y)
        for x in range(grid_size):
            for y in range(grid_size):
                if x < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y}", 1)
                    graph.add_to_graph(f"{x + 1},{y}", f"{x},{y}", 1)
                if y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x},{y + 1}", 1)
                    graph.add_to_graph(f"{x},{y + 1}", f"{x},{y}", 1)
                if x < grid_size - 1 and y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", math.sqrt(2))
                    graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", math.sqrt(2))

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            subject = graph.a_star('0,0', '4,4', metric)
            self.assertEqual(subject[0], ['0,0', '1,1', '2,2', '3,3', '4,4'])
            self.assertAlmostEqual(subject[1], (grid_size - 1) * math.sqrt(2))
            graph.reset_vertices()

        # (2) test on nxn grid with penalty for shooting diagonal
        # (shortest path is not unique, so each heuristic will return a different path)
        for x in range(grid_size - 1):
            for y in range(grid_size - 1):
                graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", 3)
                graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", 3)

        subject = graph.a_star('0,0', '4,4', Vertex.euclidean_distance)
        self.assertEqual(subject, (['0,0', '1,0', '1,1', '2,1', '2,2', '3,2', '3,3', '4,3', '4,4'], 8))
        graph.reset_vertices()
        subject = graph.a_star('0,0', '4,4', Vertex.taxicab_distance)
        self.assertEqual(subject, (['0,0', '1,0', '2,0', '3,0', '4,0', '4,1', '4,2', '4,3', '4,4'], 8))
        graph.reset_vertices()

        # === (B) Tollway graph tests ===#
        graph = Graph(csvf='test_csvs/astar/tollway_graph_csv.csv')
        # now must set of coordinates for each vertex:
        positions = [(0, 0), (2, 0), (4, 0), (7, 0), (10, 0), (12, 0), (2, 5), (6, 4), (12, 5), (5, 9), (8, 8), (12, 8),
                     (8, 10), (0, 2),
                     (4, 2), (9, 2), (9, -2), (7, 6), (8, 11), (14, 8)]

        for index, v_id in enumerate(list(graph.vertices)):
            graph.vertices[v_id].x, graph.vertices[v_id].y = positions[index]

        # UMCOMMENT TO SEE PLOT
        # graph.plot_show = True
        # graph.plot()

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            # (3) test Franklin Grove to Northbrook shortest path in both directions
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Franklin Grove', 'Northbrook', metric)
            solution = (['Franklin Grove', 'A', 'B', 'G', 'J', 'M', 'Northbrook'], 22)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

            subject = graph.a_star('Northbrook', 'Franklin Grove', metric)
            solution = (['Northbrook', 'M', 'J', 'G', 'B', 'A', 'Franklin Grove'], 22)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

            # (4) test Franklin Grove to Joliet shortest path - bypass expensive tollway path
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Franklin Grove', 'Joliet', metric)
            solution = (['Franklin Grove', 'A', 'B', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

            subject = graph.a_star('Joliet', 'Franklin Grove', metric)
            solution = (['Joliet', 'E', 'D', 'H', 'G', 'B', 'A', 'Franklin Grove'], 35)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

            # (5) test Joliet to Chicago shortest path - bypass expensive tollway path
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Joliet', 'Chicago', metric)
            solution = (['Joliet', 'E', 'D', 'H', 'G', 'J', 'K', 'L', 'Chicago'], 35)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

            subject = graph.a_star('Chicago', 'Joliet', metric)
            solution = (['Chicago', 'L', 'K', 'J', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

            # (6) test Northbrook to Belvidere - despite equal path lengths, A* heuristic will always prefer search to the left
            # (both heuristics will prefer the same path)
            subject = graph.a_star('Northbrook', 'Belvidere', metric)
            solution = (['Northbrook', 'M', 'J', 'K', 'Belvidere'], 8)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

            subject = graph.a_star('Belvidere', 'Northbrook', metric)
            solution = (['Belvidere', 'K', 'J', 'M', 'Northbrook'], 8)
            self.assertEqual(subject, solution)
            graph.reset_vertices()

    def test_a_star_comprehensive(self):

        # === (C) Random graph tests ===#
        # (1) initialize vertices of Euclidean and Taxicab weighted random graphs
        random.seed(331)
        probability = 0.5  # probability that two vertices are connected
        e_graph, t_graph = Graph(), Graph()
        vertices = []
        for s in string.ascii_lowercase:
            x, y = random.randint(0, 100), random.randint(0, 100)
            vertex = Vertex(s, x, y)
            vertices.append(vertex)
            e_graph.vertices[s], t_graph.vertices[s] = vertex, vertex
            e_graph.size += 1
            t_graph.size += 1

        # (2) construct adjacency matrix with edges weighted by appropriate distance metric
        e_matrix = [[None] + [s for s in string.ascii_lowercase]]
        t_matrix = [[None] + [s for s in string.ascii_lowercase]]
        for i in range(1, len(e_matrix[0])):
            e_row = [e_matrix[0][i]]
            t_row = [t_matrix[0][i]]
            for j in range(1, len(e_matrix[0])):
                connect = (random.random() < probability)  # connect if random draw in (0,1) < probability
                e_weighted_dist, t_weighted_dist = None, None
                if i != j and connect:
                    e_dist = vertices[i - 1].euclidean_distance(vertices[j - 1])
                    t_dist = vertices[i - 1].taxicab_distance(vertices[j - 1])
                    weight = (random.randint(1, 10))  # choose a random weight between 1 and 9
                    e_weighted_dist = e_dist * weight  # create realistic weighted dist
                    t_weighted_dist = t_dist * weight  # create realistic weighted dist
                e_row.append(e_weighted_dist)
                t_row.append(t_weighted_dist)
            e_matrix.append(e_row)
            t_matrix.append(t_row)
        e_graph.matrix2graph(e_matrix)
        t_graph.matrix2graph(t_matrix)

        # (3) define helper function to check validity of search result
        def is_valid_path(graph, search_result):
            path, dist = search_result
            length = 0
            for i in range(len(path) - 1):
                begin, end = path[i], path[i + 1]
                edge = graph.get_edge_by_ids(begin, end)
                if edge is None:
                    return False  # path contains some edge not in the graph
                length += edge[2]
            return length == dist  # path consists of valid edges: return whether length matches

        # (4) test all 26 x 26 pairwise A* traversals across random matrix and ensure they return valid paths w/o error
        for begin in vertices:
            for end in vertices:
                if begin != end:
                    subject = e_graph.a_star(begin.id, end.id, Vertex.euclidean_distance)
                    self.assertTrue(is_valid_path(e_graph, subject))
                    e_graph.reset_vertices()

                    subject = t_graph.a_star(begin.id, end.id, Vertex.taxicab_distance)
                    self.assertTrue(is_valid_path(t_graph, subject))
                    t_graph.reset_vertices()

    def test_feedback_xml_validity(self):

        path = "feedback.xml"
        xml_doc = minidom.parse(path)
        response = {}
        tags = ["netid", "feedback", "difficulty", "time", "citations", "type", "number"]

        # Assert that we can access all tags
        for tag in tags:
            raw = xml_doc.getElementsByTagName(tag)[0].firstChild.nodeValue
            lines = [s.strip() for s in raw.split("\n")]  # If multiple lines, strip each line
            clean = " ".join(lines).strip()  # Rejoin lines with spaces and strip leading space
            self.assertNotEqual("REPLACE", clean)  # Make sure entry was edited
            response[tag] = clean  # Save each entry

        # Assert that difficulty is a float between 0-10
        difficulty_float = float(response["difficulty"])
        self.assertGreaterEqual(difficulty_float, 0.0)
        self.assertLessEqual(difficulty_float, 10.0)

        # Assert that hours is a float between 0-100 (hopefully it didn't take 100 hours!)
        time_float = float(response["time"])
        self.assertGreaterEqual(time_float, 0.0)
        self.assertLessEqual(time_float, 100.0)

        # Assert assignment type and number was not changed
        self.assertEqual("Project", response["type"])
        self.assertEqual("10", response["number"])

    # def test_profile(self):
    #
    #     # use this testcase to evaluate your code's performance
    #     # replace function call inside string with any testcase to analyze
    #     print(cProfile.runctx("self.test_a_star_comprehensive()", globals(), locals()))

    """
    End Graph Part 2 Tests
    """

    """
    Begin PriorityQueue Tests (NOT FOR MIMIR - just for local development)
    """

    # def test_apq(self):
    #
    #     pq = PriorityQueue()
    #
    #     # test basics and ensure vertices are visited when popped
    #     for i, char in enumerate(string.ascii_lowercase):
    #         pq.push(-i, Vertex(char))
    #     for i, char in enumerate(reversed(string.ascii_lowercase)):
    #         priority, vertex = pq.pop()
    #         assert priority == -25+i
    #         assert vertex.id == char
    #         assert vertex.visited
    #
    #     # test updating and ensure vertices are visited when popped
    #     for i, char in enumerate(string.ascii_lowercase):
    #         pq.push(i, Vertex(char))
    #     pq.update(-1, Vertex('z'))
    #     pq.update(100, Vertex('a'))
    #     priority, vertex = pq.pop()
    #     assert (priority, vertex.id, vertex.visited) == (-1, 'z', True)
    #     for i, char in enumerate(string.ascii_lowercase):
    #         if char != 'a' and char != 'z':
    #             priority, vertex = pq.pop()
    #             assert (priority, vertex.id, vertex.visited) == (i, char, True)
    #     priority, vertex = pq.pop()
    #     assert (priority, vertex.id, vertex.visited) == (100, 'a', True)
    #     assert pq.empty()   # assert trailing vertices are popped off properly
    #
    #     # test to ensure Nones are popped off of the end (see SS20 Piazza post for concerns)
    #     pq = PriorityQueue()
    #     for i, char in enumerate(string.ascii_lowercase):
    #         pq.push(i, Vertex(char))
    #     for i, char in enumerate(string.ascii_lowercase):
    #         pq.update(-i, Vertex(char))     # will force earlier nodes to be set to None and pushed to end of list
    #     for i, char in enumerate(reversed(string.ascii_lowercase)):
    #         priority, vertex = pq.pop()
    #         assert priority == -25+i
    #         assert vertex.id == char
    #         assert vertex.visited
    #     assert pq.empty()  # assert trailing vertices are popped off properly

    """
    End AStarPriorityQueue Tests
    """


if __name__ == '__main__':
    unittest.main()

# def test_add_to_graph(self):
#
#     graph = Graph()
#
#     # (1) test creation of first vertex
#     graph.add_to_graph('a')
#     self.assertEqual(graph.size, 1)
#     subject = graph.get_all_vertices()
#     self.assertEqual(subject, {Vertex('a')})
#
#     # (2) test creation of second vertex
#     graph.add_to_graph('b')
#     self.assertEqual(graph.size, 2)
#     subject = graph.get_all_vertices()
#     self.assertEqual(subject, {Vertex('a'), Vertex('b')})
#
#     # (3) test creation of edge a-->b between existing vertices
#     graph.add_to_graph('a', 'b', 331)
#     self.assertEqual(graph.size, 2)
#     subject = graph.get_all_edges()
#     self.assertEqual(subject, {('a', 'b', 331)})
#
#     # (4) test creation of edge b-->a between existing vertices in opposite direction
#     graph.add_to_graph('b', 'a', 1855)
#     self.assertEqual(graph.size, 2)
#     subject = graph.get_all_edges()
#     self.assertEqual(subject, {('a', 'b', 331), ('b', 'a', 1855)})
#
#     # (5) test update of existing edge weight
#     graph.add_to_graph('a', 'b', 2020)
#     self.assertEqual(graph.size, 2)
#     subject = graph.get_all_edges()
#     self.assertEqual(subject, {('a', 'b', 2020), ('b', 'a', 1855)})
#
#     # (6) test creation of edge between existing begin and non-existing destination
#     graph.add_to_graph('a', 'c', 123)
#     self.assertEqual(graph.size, 3)
#     subject = graph.get_all_edges()
#     self.assertEqual(subject, {('a', 'b', 2020), ('b', 'a', 1855), ('a', 'c', 123)})
#
#     # (7) test creation of edge between non-existent begin and existent destination
#     graph.add_to_graph('d', 'c', 345)
#     self.assertEqual(graph.size, 4)
#     subject = graph.get_all_edges()
#     self.assertEqual(subject, {('a', 'b', 2020), ('b', 'a', 1855), ('a', 'c', 123), ('d', 'c', 345)})
#
#     # (8) test creation of edge between non-existent begin and non-existent destination
#     graph.add_to_graph('x', 'y', 999)
#     self.assertEqual(graph.size, 6)
#     subject = graph.get_all_edges()
#     self.assertEqual(subject,
#                      {('a', 'b', 2020), ('b', 'a', 1855), ('a', 'c', 123), ('d', 'c', 345), ('x', 'y', 999)})
#
#     # (9) test on entire alphabet graph
#     graph = Graph()
#     solution = set()
#     for i, char in enumerate(string.ascii_lowercase):
#         for j, jar in enumerate(string.ascii_lowercase):
#             if i != j:
#                 graph.add_to_graph(char, jar, 26 * i + j)
#                 solution.add((char, jar, 26 * i + j))
#
#     self.assertEqual(graph.size, 26)
#     subject = graph.get_all_edges()
#     self.assertEqual(subject, solution)
#
# def test_matrix2graph(self):
#     graph = Graph()
#
#     # (1) test empty matrix
#     matrix = [[]]
#     graph.matrix2graph(matrix)
#     self.assertEqual(graph.size, 0)
#     v_subject = graph.get_all_vertices()
#     self.assertEqual(v_subject, set())
#     e_subject = graph.get_all_edges()
#     self.assertEqual(e_subject, set())
#
#     # (2) test single vertex with no connection
#     matrix = [[None, 'a'],
#               ['a', None]]
#     graph.matrix2graph(matrix)
#     self.assertEqual(graph.size, 1)
#     v_subject = graph.get_all_vertices()
#     self.assertEqual(v_subject, {Vertex('a')})
#     e_subject = graph.get_all_edges()
#     self.assertEqual(e_subject, set())
#
#     # (3) test single vertex with connection
#     graph = Graph()
#     matrix = [[None, 'a'],
#               ['a', 331]]
#     graph.matrix2graph(matrix)
#     self.assertEqual(graph.size, 1)
#     e_subject = graph.get_all_edges()
#     self.assertEqual(e_subject, {('a', 'a', 331)})
#
#     # (4) test two vertices with no connection
#     graph = Graph()
#     matrix = [[None, 'a', 'b'],
#               ['a', None, None],
#               ['b', None, None]]
#     graph.matrix2graph(matrix)
#     self.assertEqual(graph.size, 2)
#     v_subject = graph.get_all_vertices()
#     self.assertEqual(v_subject, {Vertex('a'), Vertex('b')})
#     e_subject = graph.get_all_edges()
#     self.assertEqual(e_subject, set())
#
#     # (5) test two vertices with two-way connection
#     graph = Graph()
#     matrix = [[None, 'a', 'b'],
#               ['a', None, 100],
#               ['b', 200, None]]
#     graph.matrix2graph(matrix)
#     self.assertEqual(graph.size, 2)
#     e_subject = graph.get_all_edges()
#     self.assertEqual(e_subject, {('a', 'b', 100), ('b', 'a', 200)})
#
#     # (6) test on entire alphabet graph
#     matrix = [[None]]
#     e_solution = set()
#     for i, char in enumerate(string.ascii_lowercase):
#         matrix.append([char])
#         for j, jar in enumerate(string.ascii_lowercase):
#             if i == 0:
#                 matrix[0].append(jar)
#             if i != j:
#                 matrix[i + 1].append(26 * i + j)
#                 e_solution.add((char, jar, 26 * i + j))
#             else:
#                 matrix[i + 1].append(None)
#     graph.matrix2graph(matrix)
#     e_subject = graph.get_all_edges()
#     self.assertEqual(e_subject, e_solution)

# def test_graph2matrix(self):

#     graph = Graph()

# (1) test empty graph
#     subject = graph.graph2matrix()
#     self.assertIsNone(subject)

# (2) test single vertex with no connection
#     matrix = [[None, 'a'],
#               ['a', None]]
#     graph.matrix2graph(matrix)
#     subject = graph.graph2matrix()
#     self.assertEqual(subject, matrix)
#
#     # (3) test single vertex with connection
#     graph = Graph()
#     matrix = [[None, 'a'],
#               ['a', 331]]
#     graph.matrix2graph(matrix)
#     subject = graph.graph2matrix()
#     self.assertEqual(subject, matrix)
#
#     # (4) test two vertices with no connection
#     graph = Graph()
#     matrix = [[None, 'a', 'b'],
#               ['a', None, None],
#               ['b', None, None]]
#     graph.matrix2graph(matrix)
#     subject = graph.graph2matrix()
#     self.assertEqual(subject, matrix)
#
#     # (5) test two vertices with 2-way connection
#     graph = Graph()
#     matrix = [[None, 'a', 'b'],
#               ['a', None, 100],
#               ['b', 200, None]]
#     graph.matrix2graph(matrix)
#     subject = graph.graph2matrix()
#     self.assertEqual(subject, matrix)
#
#     # (6) test on entire alphabet graph
#     matrix = [[None]]
#     for i, char in enumerate(string.ascii_lowercase):
#         matrix.append([char])
#         for j, jar in enumerate(string.ascii_lowercase):
#             if i == 0:
#                 matrix[0].append(jar)
#             if i != j:
#                 matrix[i+1].append(26 * i + j)
#             else:
#                 matrix[i+1].append(None)
#     graph.matrix2graph(matrix)
#     subject = graph.graph2matrix()
#     self.assertEqual(subject, matrix)
#
# def test_equivalence_relation(self):
#
#     # (1) test empty Graph
#     graph = Graph()
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 0)
#     self.assertEqual(graph, Graph())
#
#     # (2) test single vertex, not self connected
#     matrix = [[None, 'a'],
#               ['a', None]]
#     graph.matrix2graph(matrix)
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 1)
#     new_matrix = graph.graph2matrix()
#     self.assertEqual(new_matrix, [[None, 'a'],
#                                   ['a', 1]])
#
#     # (3) test to ensure known equivalence relation is not modified
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 0)
#
#     # (4) bigger matrix, symmetry check
#     graph = Graph()
#     matrix = [[None, 'a', 'b'],
#               ['a', None, None],
#               ['b', 1, None]]
#     graph.matrix2graph(matrix)
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 3)
#     new_matrix = graph.graph2matrix()
#     self.assertEqual(new_matrix, [[None, 'a', 'b'],
#                                   ['a', 1, 1],
#                                   ['b', 1, 1]])
#
# def test_equivalence_relation_comprehensive(self):
#
#     # Note, random_graph_equirelation files are graphs with 52 vertices. They're big.
#     # These graphs have varying levels of connectedness. 0.5 for graph 1, 0.1 for graph 2, 0.8 for graph 3.
#     # Graph four added later, 0.01 chance of connection.
#
#     # (1) make eqr on 0.5 probability random graph
#     graph = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_1.csv')
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 1363)
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 0)
#     solution = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_1_solution.csv')
#     self.assertEqual(graph, solution)
#
#     # (2) make eqr on 0.1 probability random graph
#     graph = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_2.csv')
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 2445)
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 0)
#     solution = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_2_solution.csv')
#     self.assertEqual(graph, solution)
#
#     # (3) make eqr on 0.8 probability random graph
#     graph = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_3.csv')
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 544)
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 0)
#     solution = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_3_solution.csv')
#     self.assertEqual(graph, solution)
#
#     # (4) make eqr on 0.01 probability random graph
#     graph = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_4.csv')
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 267)
#     count = graph.make_equivalence_relation()
#     self.assertEqual(count, 0)
#     solution = Graph(csvf='test_csvs/equirelation/random_graph_equirelation_4_solution.csv')
#     self.assertEqual(graph, solution)
