import networkx as nx
import matplotlib.pyplot as plt


class collatz_graph:
	def __init__(self):
		#dict of value : node for value
		self.nodes = {1 : self.node(1, 0, True)}
		self.nodes[1].nxt = None

		#greatest depth (iterations needed to reach 1) of any node
		self.max_depth = 0

		#edges for displaying graph
		self.edges = []

	#calculates collatz path for x, determine depths of nodes on path, then determine if x is a terminal node
	def collatz(self, x:int):
		path = self.create_path(x)
		self.mark_depths(path)
		
		#only the starting node of the function can be terminal; the other nodes we traverse, by definition, can be reached from x
		self.nodes[x].is_terminal = self.is_terminal(x)	
		
	#create nodes from x to first already created node, and then traverse from there to 1
	#returns path as list[int]
	def create_path(self, x: int):
		
		#generate nodes until a known node is reached
		cur = x
		path = []
		while cur not in self.nodes:
			self.nodes[cur] = self.node(cur)
			self.nodes[cur].is_terminal = False
			path.append(cur)
			cur = self.nodes[cur].nxt
			
		#add nodes to path until end is reached
		while cur != None:
			path.append(cur)
			cur = self.nodes[cur].nxt
			
		return path
		
	#determine depths of nodes on path 
	def mark_depths(self, path):
		path.reverse()
		
		for i in range(len(path)):
			if self.nodes[path[i]].depth is None:
				self.nodes[path[i]].depth = i
				self.max_depth = max(self.max_depth, i)

	#determine is x is a terminal node
	#a node is terminal if neither of its possible parents are in the graph
	#parents of x can be 2x (which will always be even), or (x-1)//3 if that value is odd
	def is_terminal(self, x):
		no_even_parent = x*2 not in self.nodes
		no_odd_parent = ((x-1)//3 % 2 == 0) or ((x-1)//3 not in self.nodes)
		return no_even_parent and no_odd_parent
		
	#returns list of nodes from x to 1
	def get_path(self, x: int):	
		if x not in self.nodes:
			self.collatz(x)
		
		path = [x]
		while x != 1:
			x = self.nodes[x].nxt
			path.append(x)
		return path
		
	#returns list of terminal nodes, sorted by depth
	def get_terminals(self):
		tn = list(filter(lambda x: self.nodes[x].is_terminal, self.nodes))
		tn.sort(reverse=True, key=(lambda x: self.nodes[x].depth))
		return tn

	#generate and display graph; flip will flip x and y axes if True 
	def display(self, flip = False):

		#add new edges to graph
		for key in self.nodes:
			edge = [key, self.nodes[key].nxt]
			if edge not in self.edges and edge[1] != None:
			  self.edges.append(edge)
		G = nx.DiGraph()
		G.add_edges_from(self.edges)
		
		
		#the number of terminal nodes is the "width" of the graph, and the number of x-positions we need to consider; priority for straight lines up should be given to longer chain, with shorter chain joining longer chain by a diagonal edge? 
		pos = {}
		
		#determine y-position based on depth
		for key in self.nodes:
			pos[key] = [None,self.nodes[key].depth/self.max_depth]
			
		#determine x-position, based on the terminal node that leads to a given node
		tn = self.get_terminals()
		for key in tn:
			for x in self.get_path(key):
				if pos[x][0] == None: #tn is sorted by depth, so when a node is shared between two paths, it stays in line with the longer path
				
					#the longest path is center; paths of descending length increase in distance from center but alternate left and right
					if tn.index(key) % 2 == 0:
						pos[x][0] = (tn.index(key))/len(tn)
					else:
						pos[x][0] = -(tn.index(key)+1)/len(tn)
				else:
					break
					
		#rotates graph 90 degrees counterclockwise
		if flip:
			for key in pos:
				pos[key].reverse()
				pos[key][0] *= -1
				pos[key][1] *= -1
		
		nx.draw_networkx(G, pos)
		plt.show()
		
	class node():
		def __init__(self, value: int, depth: int = None, is_terminal: bool = None):
			self.value = value
			self.depth = depth #determines y-placement
			self.is_terminal = is_terminal #determines x-placement
			
			#note that nxt is an int, not a reference
			self.nxt = value // 2 if value % 2 == 0 else 3 * value + 1