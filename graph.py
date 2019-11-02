class Graph():
  def __init__(self):
    self.vertices = []

  def createVertex(self, nodeId, value):
    self.vertices.append(Node(nodeId, value))

  def findNode(self, nodeId):
    return next((node for node in self.vertices if node.id == nodeId), None)

  def createEdge(self, fromId, toId):
    fromNode = self.findNode(fromId)
    toNode = self.findNode(toId)
 
    fromNode.next.add(toNode)
    toNode.prev.add(fromNode)

  def createEdges(self):
    for node in self.vertices:
      if isinstance(node.value, tuple):
        self.createEdge(node.id, node.value)
      else:
        node.cachedValue = node.value

  def updateEdges(self, node, value):
    for child in node.next:
      child.prev.remove(node)
    
    node.next = set()
    if isinstance(value, tuple):
      self.createEdge(node.id, value)

  def dfs(self, node, visited, processNode, reverse = False):
    visited.add(node.id)
    nextList = node.next
    if reverse == True:
      nextList = node.prev
    
    for child in nextList:
      if child.id not in visited:
        self.dfs(child, visited, processNode, reverse)

    #visited.add(node.id)
    processNode(node)

class Node():
  def __init__(self, id, value):
    self.id = id
    self.value = value
    self.next = set()
    self.prev = set()
    self.cachedValue = None

class Dag():
  def __init__(self):
    self.graph = Graph()

  def print(self):
    for vertex in self.graph.vertices: 
      print(vertex.id, vertex.cachedValue, list(map(lambda node: node.id, vertex.next)))

  def processNode(self, node):
    if len(node.next) > 0:
      print('Calculating', node.id)
      node.cachedValue = sum(map(lambda child: child.cachedValue, node.next))

  def updateNode(self, nodeId, value):
    print('Updating', nodeId, value)
    
    node = self.graph.findNode(nodeId)
    node.value = value
    visited = set()
    def processNode(child):
      child.cachedValue = None

    self.graph.dfs(node, visited, processNode, True)
    if isinstance(value, int):
      node.cachedValue = value
    
    self.graph.updateEdges(node, value)

    self.processVertices()
  
  def processVertices(self):
    stack = []
    def processNode(node):
      stack.append(node)

    for vertex in self.graph.vertices:
      if vertex.cachedValue == None:
        visited = set() 
        self.graph.dfs(vertex, visited, processNode)

    for node in filter(lambda child: child.cachedValue == None,stack):
      self.processNode(node)

def main():
  data = [
    [0, 0, 0, (4,3), 0],
    [0, 5, 0, 0, 0],
    [0, 0, 3, 0, 0],
    [0, (1,1), 0, 0, 0],
    [0, 0, (2,2), (3,1), 0],
  ]

  dag = Dag()
  for (rowIdx, row) in enumerate(data):
    for (colIdx, col) in enumerate(row):
      dag.graph.createVertex((rowIdx, colIdx), col)
    
  dag.graph.createEdges()
  
  dag.processVertices()

  dag.print()

  dag.updateNode((1, 1), 9)

  dag.updateNode((2, 2), 1)
 
  dag.print()
  dag.updateNode((2, 2), (1, 1))
  
  dag.print()
  dag.updateNode((1, 1), 0)
  dag.print()
  dag.updateNode((4,4), 32)
  dag.print()
  dag.updateNode((1,1),(4,4))
  dag.print()
  dag.updateNode((3,1),(2,0))
  dag.print()
main()
