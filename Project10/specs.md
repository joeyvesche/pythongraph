Project 10: Graphs Part 2
=========================

**Due: Thursday, April 21st @ 10:00 pm**

_This is not a team project, do not copy someone else’s work._

_This project is created by Brooke Osterkamp, Andrew Haas, Tanawan Premsri, Andrew McDonald_

## Assignment Overview

### What is A\* Search?

Instead of searching the "next closest" vertex as is done in Dijkstra's algorithm, [A\* Search](https://en.wikipedia.org/wiki/A*_search_algorithm) (A-Star Search) picks the vertex which is "next closest to the goal" by weighting vertices more cleverly.

Recall that in Dijkstra's algorithm, vertices are stored in a priority queue with a priority key equal to the current shortest path to that vertex. If we denote the current shortest path to a vertex *V* by **g(v)**, then on each iteration of Dijkstra's algorithm, we search on the vertex with **min(g(v)).**

A\* search takes the same approach to selecting the next vertex, but instead of setting the priority key of a vertex equal to **g(v)** and selecting **min(g(v))**, it uses the value **f(v)** and selects the vertex with **min(f(v))** where

**f(v) = g(v) + h(v)**

**\= current\_shortest\_path\_to\_v + estimated\_distance\_between\_v\_and\_target**

### In English, Please...

A\* Search prioritizes vertices *V* to search based on the value **f(v)**, which is the sum of

*   **g(v)**, or the current shortest known path to vertex *V*, and
*   **h(v)**, which is the estimated (Euclidean or Taxicab) distance between the vertex *V* and the target vertex you're searching for

The result is that A\* prioritizes vertices to search that (1) are _close to the origin along a known path_ AND which (2) are _in the right direction towards the target._ Vertices with a small **g(v)** are _close to the origin along a known path_ and vertices with a small **h(v)** are _in the right direction towards the target**,**_ so we pick vertices with the smallest sum of these two values.

[We strongly recommend you watch this video to build your intuition behind A\* Search!](https://www.youtube.com/watch?v=ySN5Wnu88nE)

\[A\* is extremely versatile. Here we use Euclidean and Taxicab distances to prioritize certain directions of search, but note that any [metric](https://en.wikipedia.org/wiki/Metric_(mathematics)#Definition) **h(v, target)** could be used should the need arise. See [here](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) for more information on situations where different metrics may be practical.\]
For additional information on Graphs, Shortest path and A* please go to [D2L-Week-10-11](https://d2l.msu.edu/d2l/le/content/1676253/Home)
![AStarGif.gif](https://s3.amazonaws.com/mimirplatform.production/files/002f64b5-cafa-4531-8dc8-e56f0e0de6e6/AStarGif.gif)

Assignment Notes
----------------

*   A plotting function is provided to help you visualize the progression of various search algorithms
    *   Be sure to read the specs explaining **plot()**
    *   If you don't want to use it, just comment out the related import statements and **plot()** function
*   Python allows representation of the value infinity using **float('inf')**
*   No negative edge weights will ever be added to the graph
    *   All edge weights are numeric values greater than or equal to zero
*   Time complexities are specified in terms of *V* and *E*, where *V* represents the number of vertices in the graph and *E* represents the number of edges in a graph
    *   Recall that E is bounded above by *V*^2; a graph has *E* = *V*^2 edges if and only if every vertex is connected to every other vertex
*   Recall that **list.insert(0, element)** and **list.pop(0)** are both _O(N)_ calls on a Python list
    *   Recall that python's 'lists' are not lists in the more common sense of the word: linked lists. They are dynamically managed tuples, stored in memory as contiguous arrays of pointers to elements elsewhere in memory. This allows indexing into a 'list' in constant time. The downside of this, however, is that adding to a python 'list' at a specific index, _i,_ requires shifting the pointer to every element past _i_ by one in the underlying array: a linear operation.
    *   Be careful when implementing **dijkstra, astar,** and the Application Problem to ensure you do not break time complexity by popping or inserting from the front of a list when reconstructing a path
    *   Instead of inserting into / popping from the front of the list, simply append to or pop from the end, then reverse the list _once_ at the end
        *   If you have N calls to **list.insert(0, element)**, that is _O(N^2)_
        *   If you instead have N calls to **list.append(element)**, followed by a single call to **list.reverse()**, that is _O(N)_
        *   Both methods will result in the same list being constructed, but the second is far more efficient

## Assignment Specifications

### class Vertex

Represents a vertex object, the building block of a graph.

**_DO NOT MODIFY the following attributes/functions_**

*   **Attributes**
    *   **id:** A string used to uniquely identify a vertex
    *   **adj:** A dictionary of type **{other\_id : number}** which represents the connections of a vertex to other vertices; the existence of an entry with key **other\_i****d** indicates connection from this vertex to the vertex with id **other\_id** by an edge with weight **number**
        *   Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures traversals will select the next neighbor to visit deterministically
    *   **visited:** A boolean flag used in search algorithms to indicate that the vertex has been visited
    *   **x:** The x-position of a vertex (used in assignment) (defaults to zero)
    *   **y:** The y-position of a vertex (used in assignment) (defaults to zero)
*   **\_\_init\_\_(self, idx: str, x: float=0, y: float=0) -> None:**  
    *   Constructs a Vertex object
*   **\_\_eq\_\_(self, other: Vertex) -> bool:**
    *   Compares this vertex for equality with another vertex
*   **\_\_repr\_\_(self) -> str:**
    *   Represents the vertex as a string for debugging
*   **\_\_str\_\_(self) -> str:**
    *   Represents the vertex as a string for debugging
*   **\_\_hash\_\_(self) -> int:**
    *   Allows the vertex to be hashed into a set; used in unit tests

**_USE the following function however you'd like_**

*   **deg(self) -> int:**
    *   Returns the number of outgoing edges from this vertex; i.e., the outgoing degree of this vertex
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_outgoing\_edges(self) -> Set\[Tuple\[str, float\]\]:**
    *   Returns a **set** of tuples representing outgoing edges from this vertex
    *   Edges are represented as tuples **(other\_id, weight)** where
        *   **other\_id** is the unique string id of the destination vertex
        *   **weight** is the weight of the edge connecting this vertex to the other vertex
    *   Returns an empty set if this vertex has no outgoing edges
    *   _Time Complexity: O(degV)_
    *   _Space Complexity: O(degV)_
*   **euclidean\_distance(self, other: Vertex) -> float:**
    *   Returns the [euclidean distance](http://rosalind.info/glossary/euclidean-distance/) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
    *   Used in AStar
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **taxicab\_distance(self, other: Vertex) -> float:**
    *   Returns the [taxicab distance](https://en.wikipedia.org/wiki/Taxicab_geometry) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
    *   Used in AStar
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_

### class Graph

Represents a graph object

**_DO NOT MODIFY the following attributes/functions_**

* **Attributes**
    *   **size:** The number of vertices in the graph
    *   **vertices:** A dictionary of type **{id : Vertex}** storing the vertices of the graph, where **id** represents the unique string id of a **Vertex** object
        *   Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures **get\_edges(self)** and **get\_vertices(self)** will return deterministically ordered lists
    *   **plot\_show**: If true, calls to **plot()** display a rendering of the graph in matplotlib; if false, all calls to **plot()** are ignored (see **plot()** below)
    *   **plot\_delay**: Length of delay in **plot()** (see **plot()** below)
* **\_\_init\_\_(self, plt\_show: bool=False) -> None:**  
    *   Constructs a Graph object
    *   Sets **self.plot\_show** to False by default
* **\_\_eq\_\_(self, other: Graph) -> bool:**
    *   Compares this graph for equality with another graph
* **\_\_repr\_\_(self) -> str:**
    *   Represents the graph as a string for debugging
* **\_\_str\_\_(self) -> str:**
    *   Represents the graph as a string for debugging
* **add\_to\_graph(self, start\_id: str, dest\_id: str=None, weight: float=0) -> float:**
    *   Adds a vertex / vertices / edge to the graph
        *   Adds a vertex with id **start\_id** to the graph if no such vertex exists
        *   Adds a vertex with id **dest\_id** to the graph if no such vertex exists and **dest\_id** is not None
        *   Adds an edge with weight **weight** if **dest\_id** is not None
    *   If a vertex with id **start\_id** or **dest\_id** already exists in the graph, this function will not overwrite that vertex with a new one
    *   If an edge already exists from vertex with id **start\_id** to vertex with id **dest\_id**, this function will overwrite the weight of that edge
* **matrix2graph(self, matrix: Matrix) -> None:**
    *   Constructs a graph from a given adjacency matrix representation
    *   **matrix** is guaranteed to be a square 2D list (i.e. list of lists where # rows = # columns), of size **\[V+1\]** x **\[V+1\]**
        *   **matrix\[0\]\[0\]** is None
        *   The first row and first column of **matrix** hold string ids of vertices to be added to the graph and are symmetric, i.e. **matrix\[i\]\[0\] = matrix\[0\]\[i\]** for i = 1, ..., n
        *   **matrix\[i\]\[j\]** is None if no edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]**
        *   **matrix\[i\]\[j\]** is a **number** if an edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]** with weight **number**
* **graph2matrix(self) -> None:**
    *   Constructs and returns an adjacency matrix from a graph
    *   The output matches the format of matrices described in **matrix2graph**
    *   If the graph is empty, returns **None**
* **graph2csv(self, filepath: str) -> None:**
    *   Encodes the graph (if non-empty) in a csv file at the given location

* **reset\_vertices(self) -> None:**
    * Resets visited flags to False of all vertices within the graph
    * Used in unit tests to reset graphs between tests
    * Time Complexity: O(V)
    * Space Complexity: O(V)
* **get\_vertex\_by\_id(self, v\_id: str) -> Vertex:**
    * Returns the vertex object with id v_id if it exists in the graph
    * Returns None if no vertex with unique id v_id exists
    * Time Complexity: O(1)
    * Space Complexity: O(1)
* **get\_all\_vertices(self) -> Set\[Vertex\]:**
    * Returns a set of all Vertex objects held in the graph
    * Returns an empty set if no vertices are held in the graph
    * Time Complexity: O(V)
    * Space Complexity: O(V)
* **get\_edge\_by\_ids(self, begin\_id: str, end\_id: str) -> Tuple\[str, str, float\]:**
    * Returns the edge connecting the vertex with id begin_id to the vertex with id end_id in a tuple of the form (begin_id, end_id, weight)
    * If the edge or either of the associated vertices does not exist in the graph, returns None
    * Time Complexity: O(1)
    * Space Complexity: O(1)
* **get\_all\_edges(self) -> Set\[Tuple\[str, str, float\]\]:**
    * Returns a set of tuples representing all edges within the graph
    * Edges are represented as tuples (begin_id, end_id, weight) where
      * begin_id is the unique string id of the starting vertex
      * end_id is the unique string id of the starting vertex
      * weight is the weight of the edge connecitng the starting vertex to the destination vertex
    * Returns an empty set if the graph is empty
    * Time Complexity: O(V+E)
    * Space Complexity: O(E)
* **build_path(self, back_edges: Dict[str, str], begin_id: str, end_id: str) -> Tuple[List[str], float]:**
    * Given a dictionary of back-edges (a mapping of vertex id to predecessor vertex id), reconstructs the path from start_id to end_id and computes the total distance
    * Returns tuple of the form ([path], distance) where
[path] is a list of vertex id strings beginning with begin_id, terminating with end_id, and including the ids of all intermediate vertices connecting the two
distance is the sum of the weights of the edges along the [path] traveled
    * Handle the cases where no path exists from vertex with id begin_id to vertex with end_id or if one of the vertices does not exist
    * Time Complexity: O(V)
    * Space Complexity: O(V)

**_USE the following function however you'd like_**

*   **plot(self) -> None:**
    *   Renders a visual representation of the graph using matplotlib and displays graphic in PyCharm
        *   [Follow this tutorial to install matplotlib and numpy if you do not have them](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html), or follow the tooltip auto-suggested by PyCharm
    *   Provided for use in debugging
    *   If you call this in your searches and **self.****plot\_show** is true, the search process will be animated in successive plot renderings (with time between frames controlled by **self.plot\_delay**)
    *   Not tested in any testcases
        *   All testcase graphs are constructed with **self.plot\_show** set to False
    *   If vertices have (x,y) coordinates specified, they will be plotted at those locations
    *   If vertices do not have (x,y) coordinates specified, they will be plotted at a random point on the unit circle
    *   To install the necessary packages (matplotlib and numpy), follow the auto-suggestions provided by PyCharm
    *   Vertices and edges are labeled; edges are color-coded by weight
        *   If a bi-directional edge exists between vertices, two color-coded weights will be displayed

![sample_plot.png](https://s3.amazonaws.com/mimirplatform.production/files/0aec2496-150a-4b85-b86f-142f235fe4ba/sample_plot.png)

*   **reset\_vertices(self) -> None:**
    *   Resets visited flags of all vertices within the graph
    *   Used in unit tests to reset graph between searches
    *   _Time Complexity: O(V)_
    *   _Space Complexity: O(V)_
*   **get\_vertex(self, vertex\_id: str) -> Vertex:**  
    *   Returns the Vertex object with id **vertex\_id** if it exists in the graph
    *   Returns None if no vertex with unique id **vertex\_id** exists
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_vertices(self) -> Set\[Vertex\]:**  
    *   Returns a **set** of all Vertex objects held in the graph
    *   Returns an empty set if no vertices are held in the graph
    *   _Time Complexity: O(V)_
    *   _Space Complexity: O(V)_
*   **get\_edge(self, start\_id: str, dest\_id: str) -> Tuple\[str, str, float\]:**  
    *   Returns the edge connecting the vertex with id **start\_id** to the vertex with id **dest\_id** in a tuple of the form **(start\_id, dest\_id, weight)**
    *   If the edge or either of the associated vertices does not exist in the graph, returns **None**
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_edges(self) -> Set\[Tuple\[str, str, float\]\]:**
    *   Returns a **set** of tuples representing all edges within the graph
    *   Edges are represented as tuples **(start\_id, other\_id, weight)** where
        *   **start\_id** is the unique string id of the starting vertex
        *   **other\_id** is the unique string id of the destination vertex
        *   **weight** is the weight of the edge connecting the starting vertex to the destination vertex
    *   Returns an empty set if the graph is empty
    *   _Time Complexity: O(V+E)_
    *   _Space Complexity: O(E)_

**_IMPLEMENT the following functions_**

*   **dijkstra(self, begin\_id: str, end\_id: str) -> Tuple\[List\[str\], float\]:**
    *   Perform a dijkstra search beginning at vertex with id **begin\_id** and terminating at vertex with id **end\_id**
    *   As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get\_edges()) to ensure neighbors are visited in proper order
    *   Returns tuple of the form **(\[path\], distance)** where
        *   **\[path\]** is a list of vertex id strings beginning with **begin\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        *   **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    *   If no path exists from vertex with id **begin\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    *   Guaranteed that **begin\_id != end\_id** (since that would be a trivial path)
    *   Because our adjacency maps use [insertion ordering](https://stackoverflow.com/a/57072435), neighbors will be visited in a deterministic order, and thus you do not need to worry about the order in which you visit neighbor vertices at the same depth
    *   Use the given PriorityQueue class to simplify priority key updates in a search priority queue
    *   _Time Complexity: O((E + V) log V)_
    *   _Space Complexity: O(V)_
*   **a\_star(self, begin\_id: str, end\_id: str, metric: Callable\[\[Vertex, Vertex\], float\]) -> Tuple\[List\[str\], float\]**
    * Perform an A\* search beginning at vertex with id **begin\_id** and terminating at vertex with id **end\_id**
    * As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get\_edges()) to ensure neighbors are visited in proper order
    * Use the **metric** parameter to estimate h(v), the remaining distance, at each vertex
        *   This is a callable parameter and will always be **Vertex.euclidean\_distance** or **Vertex.taxicab\_distance**
    * Returns tuple of the form **(\[path\], distance)** where
        *   **\[path\]** is a list of vertex id strings beginning with **begin\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        *   **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * If no path exists from vertex with id **begin\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    * Guaranteed that **begin\_id != end\_id** (since that would be a trivial path)
    * Recall that vertices are prioritized in increasing order of **f(v) = g(v) + h(v)**, where
        *   **g(v)** is the shortest known path to this vertex
        *   **h(v)** is the Euclidean distance from *V* to the target vertex
    * Use the given PriorityQueue class to simplify priority key updates in a search priority queue
    * **Implementations of this function which do not utilize the heuristic metric will not receive any credit, visible and hidden testcases included.**
        *   **Do not simply implement Dijkstra's Algorithm**
    * _Time Complexity: O((E + V)log(V))_
    * _Space Complexity: O(V)_

To simplify the operation of updating a priority key in your search priority queue, use the following given class.

### class PriorityQueue

_DO NOT MODIFY the following attributes/functions_

*   **Attributes**
    *   **data:** Underlying data list of priority queue
    *   **locator:** Dictionary to locate vertices within the priority queue
    *   **counter:** Used to break ties between vertices
*   **\_\_init\_\_(self)**  
    *   Constructs an AStarPriorityQueue object
*   **\_\_repr\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **\_\_str\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **empty(self)**
    *   Returns boolean indicating whether priority queue is empty
*   **push(self, priority, vertex)**  
    *   Push the **vertex** object onto the priority queue with a given **priority** key
    *   This priority queue has been specially designed to hold Vertex objects as values ranked by priority keys; be sure you push Vertex objects and NOT vertex id strings onto the queue
*   **pop(self)**  
    *   Visit, remove and return the Vertex object with the highest priority (i.e. lowest priority key) as a **(priority, vertex)** tuple
*   **update(self, new\_priority, vertex)**
    *   Update the priority of the **vertex** object in the queue to have a **new\_priority**

Application Problem
-------------------

After finishing your school year for the summer, you decide to take a vacation to the lovely toll-ridden city of Chicago - modeled by a road network with **v vertices and e edges.** After cleaning out your dorm room, you find you have **m EZ-pass coupons** to spend that cover the cost of **half of any toll segment**, i.e., you have m EZ-pass coupons which effectively set the toll of a road segment to HALF.

Your goal is to devise an algorithm to find a route from point **A** to point **B** on the toll roads of Chicago for the cheapest possible overall toll for your vacation.

*   **tollways\_algorithm(self, start\_id: str, target\_id: str, coupons: int) -> Tuple\[float, float\]**
    * Perform an toll algorithm beginning at vertex with id **start\_id** and terminating at vertex with id **target\_id**
    * Assume the distance between paths is the cost of going from one to another
    * As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get\_edges()) to ensure neighbors are visited in proper order
    * The **coupon** parameter is the maximum number of coupons
        *   This parameter will always be an integer
    * Returns tuple of the form **(cost, coupons)** where
        *   **cost** is the cost of the best path beginning with **start\_id**, terminating with **target\_id**
        *   When halfing coupon cost use [integer division](https://www.geeksforgeeks.org/division-operator-in-python/)
        *   float('inf') should be used for positive infinity
        *   **coupons** is the sum of the number of coupons used along the best path traveled
    * If no path exists from vertex with id **start\_id** to vertex with **target\_id** or if one of the vertices does not exist, returns tuple **(None,None)**
    * Guaranteed that **start\_id != target\_id** (since that would be a trivial path)
    * Use the given TollWayPriorityQueue class to simplify priority key updates in a search priority queue
    * _Time Complexity: O((C\*V+E)\*log(V\*C)), C is the number of coupons_
    * _Space Complexity: O(V*C), C is the number of coupons_
    * You can only use 1 coupon per edge
      * consider A -- 100 -- B -- 2 -- C example with 2 coupons, you can't apply both coupons to the 100 edge, you would have to apply 1 coupon to each, so the best you could do would be cost 51
    * **HINTS**: 
      * Use priority queue and dictionary similar to Dijkstra's but storing {cost, coupons used to reach the node, node} rather than just {distance, node}
      * When constructing the dictionary and priority queue think of a matrix V vertices rows by C columns starting at 0 coupons, similar to [Cartesian Product](https://en.wikipedia.org/wiki/Cartesian_product)

To simplify the operation of updating a priority key in your search priority queue, use the following given class.

### class TollWayPriorityQueue:

_DO NOT MODIFY the following attributes/functions_

*   **Attributes**
    *   **data:** Underlying data list of priority queue
    *   **locator:** Dictionary to locate vertices within the priority queue
    *   **counter:** Used to break ties between vertices
*   **\_\_init\_\_(self)**  
    *   Constructs an TollWayPriorityQueue object
*   **\_\_repr\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **\_\_str\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **empty(self)**
    *   Returns boolean indicating whether priority queue is empty
*   **push(self, priority, vertex)**  
    *   Push the **vertex** object onto the priority queue with a given **priority** key
    *   This priority queue has been specially designed to hold Vertex objects as values ranked by priority keys; be sure you push Vertex objects and NOT vertex id strings onto the queue
*   **pop(self)**  
    *   Visit, remove and return the Vertex object with the highest priority (i.e. lowest priority key) as a **(priority, vertex)** tuple
*   **update(self, new_priority: float, new_coupon: int, vertex: Vertex)**
    *   Update the priority of the **vertex** object in the queue to have a **new\_priority**

### Examples

Use the map below of the Chicago Tollways,

Letters A-M represent toll booths, and the stars are cities you are visiting.

![](https://i.imgur.com/2YGrgyd.png)

and below is a modified and simplified version of the map represented as a graph.

![](https://i.imgur.com/pIl48tT.png)
![](https://i.imgur.com/WkWDXBs.jpg)

Note: maps/graphs may not be accurate to actual tollway maps.

#### Examples for a\_star

*   **a\_star('Franklin Grove', 'Northbrook')** would return
    *   (\['Franklin', 'A', 'B', 'G', 'J', 'M', 'Northbrook'\], 22)
    *   This finds the same optimal path as Dijkstra
*   **a\_star('Franklin Grove', 'Joliet')** would return
    *   (\['Franklin Grove', 'A', 'B', 'G', 'H', 'D', 'E', 'Joliet'\], 35)
    *   This finds the optimal path (note that BFS would find a sub-optimal path of path length 37)
*   **a\_star('Northbrook', 'Belvidere')** would return
    *   (\['Northbrook', 'M', 'J', 'K', 'Belvidere'\], 8)
    *   Although two equally-optimal paths exist, A\* chooses the one that's closer to the straight line connecting the Cafeteria to the Med Bay

#### Examples for tollways\_algorthim

* For Test 3: **tollways\_algorithm('A', 'C', 1)** would return
    *   (3,1) aka (cost, coupon)
    *   We only can spend one coupon. It is applied on the path A->C which costs 6. The coupon halfs the cost, 6/2 = 3.
* For Test 3: **tollways\_algorithm('A', 'D', 1)** would return
    * (5,1)
    * The path A->B costs 2 then B->D cost 6. We can only use one coupon so applied to the higher cost toll. Therefore 2 (A->B)+3 (B->D with coupon) = 5.
    * The following is the steps of the data structure updating through Test 3
    * ![](https://i.imgur.com/dph3eus.jpg)
* For Test 4: **tollways\_algorithm('A', 'C', 2)** would return
    *   We have a direct path from A->C that costs 4. Only need one coupon.

* For Test 4: **tollways\_algorithm('A', 'E', 2)** would return
    
    *   (3,2) aka (cost, coupon)
    *   We only can spend two coupons. The path is from A->B (2) and B->E (5). 1(A->B) + (5(B->E)//2) (integer division - no remainder) = 1+2 = 3
* For Test 7: **tollways\_algorithm('Franklin Grove', 'Chicago', 5)**  City by Coupon Number Data Table for debugging
  ![](https://i.imgur.com/Zp4F1ML.jpg)
## Writing Application Problem
    
*   **Complete the questions below - copy and paste them into a word doc - and include this pdf  document as you are submitting your Project10 on Mimir.**
*   Use project10 comparison.py file to answer questions
*   Matplotlib installation resources: [how-to-install-matplotlib-in-python](https://www.tutorialspoint.com/how-to-install-matplotlib-in-python) and [install python packages on PyCharm](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html)
*   **Writing Questions**
    *   Question 1 (2pts): Run the first test (test1) from comparison.py file and include the figure produced here.
    *   Question 2 (2pts): The time complexity of both breadth-first and depth-first graph searches is O(|V | + |E|), where V is the set of vertices of the graph, and E is the set of edges. In the figure produced above, the ”connectivity factor” of a graph is the probability that given any two vertices, say v1 and v2, there exists an edge from v1 to v2. Note that in a fully-connected graph, where every vertex is connected to every other vertex, we have E=V^2. Why in the figure above does BFS/DFS performance appear linear for small connectivity factors, but not so far larger factors?
    *   Question 3 (2pts): Run the second test (test2) and include the figure produced here.
    *   Question 4 (2pts): Notice that AStar search notably outperforms Dijkstras algorithm on the graphs provided. In one or two sentences, informally explain why. What does AStar take advantage of?
    *   Question 5 (2pts): Suppose you were to call the AStar search as follows: What issues(s) may this cause?
        
            graph.a_star(vertex_1, vertex_2, metric = lambda v1, v2 : random.rand()) 

## Submission

### Deliverables:

Be sure to upload the following deliverables in a .zip folder to Mimir by 10:00 pm EST, on Thursday, April 21st.

Your .zip folder can contain other files (for example, description.md and tests.py), but must include (at least) the following:

    |- Project10.zip
        |— Project10/
            |— feedback.xml     (for project feedback, make sure to fill this out)
            |— __init__.py      (for proper testcase loading)       
            |— solution.py      (contains your solution source code)
            |— project10.pdf    (contains your written solution)
    

### Grading

The following 100-point rubric will be used to determine your grade on Project 10

* Policies
  * **Making all of these policies bold or italic would get too visually fatiguing but read them all because they're important!**
  * Using a different algorithm than the one specified for some function will result in the loss of all automated and manual points for that function.
  * You will not receive any points on this project if you use Python's built-in sorting functions or sorting functions imported from any library.
  * You will not receive any points on the project if you use any list-reversing function such as reversed, list.reverse, or a homemade alternative to these. You must sort the lists in ascending or descending order directly.

* Tests (70)
  * Test feedback.xml:\_\_/3
  * Test coding standard:\_\_/3
  * **dijkstra:**\_\_/14
    * **dijkstra_basic:**\_\_/7
    * **dijkstra_comprehensive:**\_\_/7
  * **a\_star**:\_\_/20
    * **a_star_basic:**\_\_/10
    * **a_star_comprehensive:**\_\_/10
  * **tollways\_algorithm**:\_\_/20
    * **application_basic:**\_\_/10
    * **application_comprehensive:**\_\_/10

* Manual (30)

  * Time and space complexity points are **all-or-nothing** for each function. If you fail to meet time or space complexity in a given function, you do not receive manual points for that function. (30)
  * Manual points for each function require passing all tests for that function, except for the comprehensive tests.
  * Use of non-local in any function will result with loss of manual points for that function.
  * Time & Space Complexity (30)
    * M1 - **dijkstra** :\_\_/10
      * _Time Complexity: O((E + V)log(V))_ 
      * _Space Complexity: O(V)_
    * M2 - **a\_star**: \_\_/10
      * _Time Complexity: O((E + V)log(V))_ 
      * _Space Complexity: O(V)_
    * M3 - **tollways\_algorithm**:\_\_/10
      * _Time Complexity: O((C*V+E)*log(V\*C)), C is the number of coupons_ 
      * _Space Complexity: O(V*C), C is the number of coupons_
    * M4 - **WRITING ASSIGNMENT**:\_\_/10

### Congratulations on Finishing your Last Project! 
* [What time is it?!](https://youtu.be/3hOP7qPDyI4)