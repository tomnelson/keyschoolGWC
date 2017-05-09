class Graph:
    def __init__(self):
        # vertices is a dictionary that maps a vertex to a tuple of 2 sets: incoming and outgoing edges
        self.vertices = {}
        # edges is a dictionary that maps an edge to a tuple of 2 vertices that the edge connects
        self.edges = {}

    def addVertex(self,v):
        if v not in self.vertices:
          # put v in the dictionary with a value that is a tuple of 2 empty sets (for in and out edges)
          self.vertices[v] = (set([]),set([]))          

    def addEdge(self, edge, v1, v2):
        if edge not in self.edges:
          self.edges[edge] = (v1, v2) # put v1 and v2 into a tuple and make it the value for edge in the dictionary
          if v1 not in self.vertices.keys():
              self.addVertex(v1)
          if v2 not in self.vertices.keys():
              self.addVertex(v2)
          # this is an undirected graph so every edge is both incoming and outgoing
          self.vertices[v1][0].add(edge) # add edge to incoming set for v1
          self.vertices[v1][1].add(edge) # add edge to outgoing set for v1
          self.vertices[v2][0].add(edge) # add edge to incoming set for v2
          self.vertices[v2][1].add(edge) # add edge to outgoing set got v2

    def getEdges(self):
        # the keys in the edges dictionary contain all edges for this graph
        return self.edges.keys()

    def getVertices(self):
        # the keys for the vertices dictionary contain all vertices for this graph
        return self.vertices.keys()

    # the incoming edges for v are the first [0] set in its value tuple (incomingset,outgoingset)
    def getIncomingEdges(self, v):
        return self.vertices[v][0]

    # the outgoind edges for v are the second [1] set in its value tuple (incomingset,outgoingset)
    def getOutgoingEdges(self, v):
        return self.vertices[v][1]

    def __str__(self):
        return "v:"+str(self.vertices)+" "+"e:"+str(self.edges)

class DiGraph(Graph):
    def __init__(self):
        Graph.__init__(self)

    # because this is a directed graph, an edge from v1 to v2 is outgoing only for v1 and incoming only for v2
    def addEdge(self, edge, v1, v2):
        self.edges[edge] = (v1, v2) # put v1 and v2 into a tuple and make it the value for edge in the dictionary
        if v1 not in self.vertices.keys():
            self.addVertex(v1)
        if v2 not in self.vertices.keys():
            self.addVertex(v2)
        self.vertices[v1][1].add(edge) # edge is outgoing for v1
        self.vertices[v2][0].add(edge) # edge is incoming for v2


g = DiGraph()

g.addEdge("a", 1, 2)
g.addEdge("b", 2, 3)
g.addEdge("c", 1, 3)
g.addEdge("d", 3, 1)

print str(g)

print "vertices:"+str(g.getVertices())

print "edges:"+str(g.getEdges())

print 'outgoing for 1:'+str(g.getOutgoingEdges(1))
print 'incoming for 1:'+str(g.getIncomingEdges(1))
