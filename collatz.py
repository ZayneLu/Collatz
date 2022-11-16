import networkx as nx
import matplotlib.pyplot as plt


nodes = {}
max_depth = 0

def collatz(x:int):
	#find path
	start = x
	while x not in nodes and x != 1:
		print(x)
		nxt = next(x)
		nodes[x] = (nxt, None)
		x = nxt
	x = start
	
	#determine depth of path
	path = find_path(x)
	print(path)
	path.reverse()
	path = path[1:]
	
	global max_depth
	for i in range(len(path)):
		if nodes[path[i]][1] is None:
			nodes[path[i]] = (nodes[path[i]][0], i+1)
			max_depth = max(max_depth, i+1)
	
	
def find_path(x):	
	path = [x]
	while x != 1:
		x = nodes[x][0]
		path.append(x)
	return path

def next(x: int):
	return x//2 if x%2==0 else 3*x+1
	

edges = []
def display():
	#add new edges to graph
	for key in nodes:
		edge = [key, nodes[key][0]]
		if edge not in edges:
		  edges.append(edge)
	G = nx.DiGraph()
	G.add_edges_from(edges)
	
    
    #the number of terminal nodes is the "width" of the graph, and the number of x-positions we need to consider; priority for straight lines up should be given to longer chain, with shorter chain joining longer chain by a diagonal edge? 
	pos = {}
	for key in nodes:
		pos[key] = [1 - key/max(nodes),nodes[key][1]/max_depth]
	pos[1] = [1, 0]
		
	nx.draw_networkx(G, pos)
	plt.show()

collatz(7)
collatz(15)
collatz(128)
display()