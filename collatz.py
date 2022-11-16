import networkx as nx
import matplotlib.pyplot as plt


nodes = {}
max_depth = 0

class node():
	def __init__(self, value: int, depth: int = None, is_terminal: bool = None):
		self.value = value
		self.depth = depth #used to determine y-placement
		self.is_terminal = is_terminal #will be used to determine x-placement
		
		#note that nxt is an int, not a node
		self.nxt = value // 2 if value % 2 == 0 else 3 * value + 1

#calculates collatz path for x, then depth of all new nodes
def collatz(x:int):
	#find path
	start = x
	while x not in nodes and x != 1:
		print(x)
		nodes[x] = node(x)
		x = nodes[x].nxt
	x = start
	
	#determine depth of path
	path = find_path(x)
	print(path)
	path.reverse()
	path = path[1:]
	
	global max_depth
	for i in range(len(path)):
		if nodes[path[i]].depth is None:
			nodes[path[i]].depth = i+1
			max_depth = max(max_depth, i+1)
	
	
#returns list of nodes from x to 1
#will throw an exception if x is not includes in nodes; use collatz(x) first
def find_path(x: int):	
	path = [x]
	while x != 1:
		x = nodes[x].nxt
		path.append(x)
	return path

edges = []
#generate and display graph 
def display():
	#add new edges to graph
	for key in nodes:
		edge = [key, nodes[key].nxt]
		if edge not in edges:
		  edges.append(edge)
	G = nx.DiGraph()
	G.add_edges_from(edges)
	
	
	#the number of terminal nodes is the "width" of the graph, and the number of x-positions we need to consider; priority for straight lines up should be given to longer chain, with shorter chain joining longer chain by a diagonal edge? 
	pos = {}
	for key in nodes:
		pos[key] = [1 - key/max(nodes),nodes[key].depth/max_depth]
	pos[1] = [1, 0]
		
	nx.draw_networkx(G, pos)
	plt.show()