# A non-directed graph. An edge between v1 and v2 can be used in both directions
class Graph:

    def __init__(self):

        # a dictionary where vertex is the key and the value is a set of incident edges
        self.vertices = {} # empty dictionary for now

        # a dictionary where the edge is the key and the value is a tuple of
        # two vertices
        self.edges = {} # empty dictionary for now

    def addVertex(self,v):
        if v not in self.vertices.keys():
            # put v in as the key, the value is an empty set
            self.vertices[v] = set([])

    def addEdge(self, edge, v1, v2):
        if edge not in self.edges.keys():
            # put edge in as the key. the value is the pair (a tuple) of vertices
            self.edges[edge] = (v1, v2)
            self.addVertex(v1)
            self.addVertex(v2)
            self.getIncidentEdges(v1).add(edge)
            self.getIncidentEdges(v2).add(edge)

    def getEdges(self):
        # return the keys of the edges dictionary
        return self.edges.keys()

    def getVertices(self):
        # return the keys of the vertices dictionary
        return self.vertices.keys()

    def getIncomingEdges(self, v):
        # the incoming edges are just the incident edges
        return self.getIncidentEdges(v)

    def getOutgoingEdges(self, v):
        # the outgoing edges are just the incident edges
        return self.getIncidentEdges(v)

    def getIncidentEdges(self, v):
        # self.vertices[v] value is a Set of incident edges
        return self.vertices[v]

    # for a vertex v, find all vertices that are connected to v with one edge
    def getAdjacentVertices(self, v):
        adj = set([])
        for edge in self.getIncidentEdges(v):
            for ep in self.getEndpoints(edge):
                if v != ep: # don't add v
                    adj.add(ep)
        return adj

    def getEndpoints(self, edge):
        # returns a tuple of the 2 vertex endpoints for the given edge  (v1,v2)
        return self.edges[edge]

    def __str__(self):
        return "vertices:"+str(self.vertices)+"\n"+"edges:"+str(self.edges)

# a directed graph. Edges have one direction from v1 to v2
class DiGraph(Graph):
    def __init__(self):
        Graph.__init__(self)

    def addVertex(self,v):
        if v not in self.vertices.keys():
            # put v in as the key, the value is a tuple of 2 empty sets
            # first is for incoming edges, second is for outgoing edges
            self.vertices[v] = (set([]),set([]))

    def getIncomingEdges(self, v):
        # self.vertices[v] value is a tuple of 2 Sets.
        # the first set [0] is the incoming edges
        return self.vertices[v][0]

    def getOutgoingEdges(self, v):
        # self.vertices[v] value is a tuple of 2 Sets.
        # the second set [1] is the outgoing edges
        return self.vertices[v][1]

    def getIncidentEdges(self, v):
        # the union of the incoming and outgoing edges
        return self.getIncomingEdges(v) | self.getOutgoingEdges(v)
            #self.getIncomingEdges(v).union(self.getOutgoingEdges(v))

    def addEdge(self, edge, v1, v2):
        self.edges[edge] = (v1, v2)  # put v1 and v2 into a tuple and make it the value for edge in the dictionary
        self.addVertex(v1)
        self.addVertex(v2)
        self.getOutgoingEdges(v1).add(edge)
        self.getIncomingEdges(v2).add(edge)

    def getAdjacentVertices(self, v):
        adj = set([])
        # for directed graph, only use outgoing edges
        for edge in self.getOutgoingEdges(v):
            for ep in self.getEndpoints(edge):
                if v != ep:
                    adj.add(ep)
        return adj


g = DiGraph()

g.addEdge("a", 1, 2) # add an edge named 'a' that connects vertex 1 and 2
g.addEdge("b", 2, 3) # add an edge named 'b' that connects vertex 2 and 3
g.addEdge("c", 1, 3)
g.addEdge("d", 3, 1)

print str(g)

print "vertices:"+str(g.getVertices())

print "edges:"+str(g.getEdges())

print 'outgoing for 1:'+str(g.getOutgoingEdges(1))
print 'incoming for 1:'+str(g.getIncomingEdges(1))
print 'incident for 1:'+str(g.getIncidentEdges(1))

print 'adjacent to 1:'+str(g.getAdjacentVertices(1))
print 'adjacent to 2:'+str(g.getAdjacentVertices(2))
print 'adjacent to 3:'+str(g.getAdjacentVertices(3))

g = Graph()

g.addEdge("a", 1, 2) # add an edge named 'a' that connects vertex 1 and 2
g.addEdge("b", 2, 3) # add an edge named 'b' that connects vertex 2 and 3
g.addEdge("c", 1, 3)
g.addEdge("d", 3, 1)

print str(g)

print "vertices:"+str(g.getVertices())

print "edges:"+str(g.getEdges())

print 'outgoing for 1:'+str(g.getOutgoingEdges(1))
print 'incoming for 1:'+str(g.getIncomingEdges(1))
print 'incident for 1:'+str(g.getIncidentEdges(1))


print 'adjacent to 1:'+str(g.getAdjacentVertices(1))
print 'adjacent to 2:'+str(g.getAdjacentVertices(2))
print 'adjacent to 3:'+str(g.getAdjacentVertices(3))

