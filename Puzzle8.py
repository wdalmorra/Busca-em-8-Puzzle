from random import randint
from copy import deepcopy
from collections import deque
import sys

class Puzzle(object):
	def __init__(self, size):

		self.path = []
		
		self.size = size
		self.box = []

		self.box_f = []

		for i in range(0,self.size):
			self.box.append([])
			for y in range(0,self.size):
				self.box[i].append(i*self.size+y+1)

		self.box[i][y] = 0

		self.empty_px = self.size-1
		self.empty_py = self.size-1

		self.depth = 0

		# print self.box

	def setBoxFather(self, box):
		self.box_f = deepcopy(box)

	def setDepth(self, f_depth):
		self.depth = f_depth + 1

	def copy(self, p):

		self.box = deepcopy(p.box)
		self.empty_px = p.empty_px
		self.empty_py = p.empty_py
		self.path.extend(p.path)

		# print self.box

	def move_left(self):

		if (self.empty_py - 1) >= 0:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px][self.empty_py - 1]
			self.box[self.empty_px][self.empty_py - 1] = 0
			self.empty_py -= 1
			self.path.append([self.empty_px, self.empty_py])
			# print self.box
			return True
		else:
			return False

	def move_right(self):
		if (self.empty_py + 1) < self.size:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px][self.empty_py + 1]
			self.box[self.empty_px][self.empty_py + 1] = 0
			self.empty_py += 1
			self.path.append([self.empty_px, self.empty_py])
			# print self.box
			return True
		else:
			return False

	def move_up(self):
		if (self.empty_px - 1) >= 0:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px - 1][self.empty_py]
			self.box[self.empty_px - 1][self.empty_py] = 0
			self.empty_px -= 1
			self.path.append([self.empty_px, self.empty_py])
			# print self.box
			return True
		else:
			return False

	def move_down(self):
		if (self.empty_px + 1) < self.size:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px + 1][self.empty_py]
			self.box[self.empty_px + 1][self.empty_py] = 0
			self.empty_px += 1
			self.path.append([self.empty_px, self.empty_py])
			# print self.box
			return True
		else:
			return False

	def is_final(self):
		result = 0
		for i in xrange(self.size):
			for j in xrange(self.size):
				if self.box[i][j] != ((i*self.size)+j+1):
					result += 1

		if result == 1:
			return True
		else:
			return False

	def shuffle(self, max_it):
		cont = 0;
		while cont < max_it:
			
			vertical = randint(0,1)
			greater = randint(0,1)
			happened = False

			if vertical == 1:
				if greater == 1:
					if (self.empty_py + 1) < self.size:
						self.box[self.empty_px][self.empty_py] = self.box[self.empty_px][self.empty_py + 1]
						self.box[self.empty_px][self.empty_py + 1] = 0
						self.empty_py += 1
						happened = True
				else:
					if (self.empty_py - 1) >= 0:
						self.box[self.empty_px][self.empty_py] = self.box[self.empty_px][self.empty_py - 1]
						self.box[self.empty_px][self.empty_py - 1] = 0
						self.empty_py -= 1
						happened = True
			else:
				if greater == 1:
					if (self.empty_px + 1) < self.size:
						self.box[self.empty_px][self.empty_py] = self.box[self.empty_px + 1][self.empty_py]
						self.box[self.empty_px + 1][self.empty_py] = 0
						self.empty_px += 1
						happened = True
				else:
					if (self.empty_px - 1) >= 0:
						self.box[self.empty_px][self.empty_py] = self.box[self.empty_px - 1][self.empty_py]
						self.box[self.empty_px - 1][self.empty_py] = 0
						self.empty_px -= 1
						happened = True
			if happened:
				cont += 1


class Depth(object):
	
	def __init__(self, initial_state, size, max_depth):
		
		self.open_nodes = []
		self.visited = []
		self.initial_state = deepcopy(initial_state)
		self.open_nodes.append(self.initial_state)

		self.size = size
		self.max_depth = max_depth

	def search(self):
		
		max_open = 1

		# t_visited = 0

		while self.open_nodes:

			if len(self.open_nodes) > max_open:
				max_open = len(self.open_nodes)

			s = self.open_nodes.pop()

			# self.visited.append(s.box)
			# t_visited += 1

			if s.is_final():
				# print "Visited: "+ str(t_visited)
				print "Open: "+ str(max_open)
				return s
			
			if s.depth < self.max_depth:
				# Abre vizinho de cima se possivel
				up = Puzzle(self.size)
				up.copy(s)
				if up.move_up():
					# if not up.box in self.visited: 
					if not up.box == s.box_f:
						up.setBoxFather(s.box)
						up.setDepth(s.depth)
						self.open_nodes.append(up)
						# t_open += 1

				# Abre vizinho da esquerda se possivel
				left = Puzzle(self.size)
				left.copy(s)
				if left.move_left():
					# if not left.box in self.visited: 
					if not left.box == s.box_f:
						left.setBoxFather(s.box)
						left.setDepth(s.depth)
						self.open_nodes.append(left)
						# t_open += 1

				# Abre vizinho de baixo se possivel
				down = Puzzle(self.size)
				down.copy(s)
				if down.move_down():
					# if not down.box in self.visited: 
					if not down.box == s.box_f:
						down.setBoxFather(s.box)
						down.setDepth(s.depth)
						self.open_nodes.append(down)
						# t_open += 1

				# Abre vizinho de direita se possivel
				right = Puzzle(self.size)
				right.copy(s)
				if right.move_right():
					# if not right.box in self.visited: 
					if not right.box == s.box_f:
						right.setBoxFather(s.box)
						right.setDepth(s.depth)
						self.open_nodes.append(right)
						# t_open += 1

		return None


class Breadth(object):
	
	def __init__(self, initial_state, size):
		
		self.open_nodes = deque([])
		self.visited = []
		self.initial_state = deepcopy(initial_state)
		self.open_nodes.append(self.initial_state)

		self.size = size

	def search(self):
		
		max_open = 1

		# t_visited = 0

		while self.open_nodes:

			if len(self.open_nodes) > max_open:
				max_open = len(self.open_nodes)


			s = self.open_nodes.popleft()

			# self.visited.append(s.box)
			# t_visited += 1

			if s.is_final():
				# print "Visited: "+ str(t_visited)
				print "Open: "+ str(max_open)
				return s
			
			# Abre vizinho de cima se possivel
			up = Puzzle(self.size)
			up.copy(s)
			if up.move_up():
				# if not up.box in self.visited: 
				if not up.box == s.box_f:
					up.setBoxFather(s.box) 
					self.open_nodes.append(up)
					# t_open += 1
			
			# Abre vizinho da esquerda se possivel
			left = Puzzle(self.size)
			left.copy(s)
			if left.move_left():
				# if not left.box in self.visited: 
				if not left.box == s.box_f:
					left.setBoxFather(s.box)
					self.open_nodes.append(left)
					# t_open += 1

			# Abre vizinho de baixo se possivel
			down = Puzzle(self.size)
			down.copy(s)
			if down.move_down():
				# if not down.box in self.visited: 
				if not down.box == s.box_f:
					down.setBoxFather(s.box)
					self.open_nodes.append(down)
					# t_open += 1


			# Abre vizinho de direita se possivel
			right = Puzzle(self.size)
			right.copy(s)
			if right.move_right():
				# if not right.box in self.visited: 
				if not right.box == s.box_f:
					right.setBoxFather(s.box)
					self.open_nodes.append(right)
					# t_open += 1

		return None


class ItetariveDeapth(object):
	def __init__(self, initial_state, size):
		
		self.open_nodes = []
		self.visited = []
		self.initial_state = deepcopy(initial_state)

		self.size = size

	def search(self):

		max_open = 0

		# t_visited = 0

		depth = 0
		
		while True:

			self.open_nodes = []
			# self.visited = []
			self.open_nodes.append(self.initial_state)

			while self.open_nodes:

				if len(self.open_nodes) > max_open:
					max_open = len(self.open_nodes)

				s = self.open_nodes.pop()

				# self.visited.append(s.box)
				# t_visited += 1

				if s.is_final():
					# print "Visited: "+ str(t_visited)
					print "Open: "+ str(max_open)
					return s

				if s.depth < depth:
				
					# Abre vizinho de cima se possivel
					up = Puzzle(self.size)
					up.copy(s)
					if up.move_up():
						# if not up.box in self.visited: 
						if not up.box == s.box_f:
							up.setBoxFather(s.box)
							up.setDepth(s.depth)
							self.open_nodes.append(up)
							# t_open += 1

					# Abre vizinho da esquerda se possivel
					left = Puzzle(self.size)
					left.copy(s)
					if left.move_left():
						# if not left.box in self.visited: 
						if not left.box == s.box_f:
							left.setBoxFather(s.box)
							left.setDepth(s.depth)
							self.open_nodes.append(left)
							# t_open += 1

					# Abre vizinho de baixo se possivel
					down = Puzzle(self.size)
					down.copy(s)
					if down.move_down():
						# if not down.box in self.visited: 
						if not down.box == s.box_f:
							down.setBoxFather(s.box)
							down.setDepth(s.depth)
							self.open_nodes.append(down)
							# t_open += 1

					# Abre vizinho de direita se possivel
					right = Puzzle(self.size)
					right.copy(s)
					if right.move_right():
						# if not right.box in self.visited: 
						if not right.box == s.box_f:
							right.setBoxFather(s.box)
							right.setDepth(s.depth)
							self.open_nodes.append(right)
							# t_open += 1
			depth += 1
			# print depth
		return None
		
		

def print_box(box):
	for x in box:
		print x
	print ""

def print_result(path, i_state, empty_p):
	
	print_box(i_state)

	for x in path:
		i_state[empty_p[0]][empty_p[1]] = i_state[x[0]][x[1]]
		i_state[x[0]][x[1]] = 0
		print_box(i_state)
		empty_p[0] = x[0]
		empty_p[1] = x[1]


def main(argv):

	max_shuffle = 50

	# print "p: "
	p = Puzzle(3)
	# print "p shuffle: "
	# p.shuffle(max_shuffle)
	

	# 8 PASSOS
	# p.box = [[0, 2, 3],[1, 6, 8],[4, 7, 5]]
	# p.empty_px = 0
	# p.empty_py = 0

	# p.box = [[4, 1, 3],[7, 2, 6],[5, 8, 0]]
	# p.empty_px = 2
	# p.empty_py = 2

	# p.box = [[4, 1, 3],[7, 0, 6],[5, 2, 8]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[2, 4, 3],[1, 8, 5],[0, 7, 6]]
	# p.empty_px = 2
	# p.empty_py = 0

	# p.box = [[2, 3, 6],[1, 5, 8],[4, 7, 0]]
	# p.empty_px = 2
	# p.empty_py = 2


	# 10 PASSOS
	# p.box = [[1, 3, 6],[2, 0, 8],[4, 7, 5]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[1, 2, 3],[6, 0, 8],[5, 4, 7]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[1, 3, 5],[8, 2, 6],[4, 7, 0]]
	# p.empty_px = 2
	# p.empty_py = 2

	# p.box = [[1, 4, 2],[7, 0, 3],[5, 8, 6]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[1, 3, 0],[4, 6, 5],[7, 2, 8]]
	# p.empty_px = 0
	# p.empty_py = 2


	# 12 PASSOS
	# p.box = [[1, 3, 0],[7, 2, 8],[6, 4, 5]]
	# p.empty_px = 0
	# p.empty_py = 2

	# p.box = [[5, 1, 6],[3, 0, 2],[4, 7, 8]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[1, 3, 5],[7, 0, 6],[8, 2, 4]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[4, 3, 0],[2, 8, 5],[1, 7, 6]]
	# p.empty_px = 0
	# p.empty_py = 2

	# p.box = [[1, 2, 0],[4, 7, 3],[8, 5, 6]]
	# p.empty_px = 0
	# p.empty_py = 2

	
	# 14 PASSOS
	# p.box = [[1, 4, 2],[7, 0, 6],[8, 5, 3]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[6, 2, 0],[1, 4, 5],[7, 8, 3]]
	# p.empty_px = 0
	# p.empty_py = 2

	# p.box = [[3, 5, 6],[4, 1, 2],[0, 7, 8]]
	# p.empty_px = 2
	# p.empty_py = 0

	# p.box = [[2, 3, 5],[8, 4, 6],[1, 7, 0]]
	# p.empty_px = 2
	# p.empty_py = 2

	# p.box = [[7, 5, 1],[2, 0, 3],[8, 4, 6]]
	# p.empty_px = 1
	# p.empty_py = 1


	# 16 PASSOS
	# p.box = [[1, 2, 4],[8, 7, 5],[0, 6, 3]]
	# p.empty_px = 2
	# p.empty_py = 0

	# p.box = [[0, 7, 4],[1, 5, 3],[8, 2, 6]]
	# p.empty_px = 0
	# p.empty_py = 0

	# p.box = [[4, 3, 6],[1, 7, 8],[2, 5, 0]]
	# p.empty_px = 2
	# p.empty_py = 2

	# p.box = [[1, 5, 6],[2, 0, 8],[4, 3, 7]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[1, 2, 3],[4, 7, 5],[0, 6, 8]]
	# p.empty_px = 2
	# p.empty_py = 0


	# 18 PASSOS
	# p.box = [[5, 1, 7],[4, 3, 2],[8, 6, 0]]
	# p.empty_px = 2
	# p.empty_py = 2

	# p.box = [[0, 1, 3],[8, 2, 6],[7, 4, 5]]
	# p.empty_px = 0
	# p.empty_py = 0

	# p.box = [[5, 8, 2],[4, 0, 7],[6, 1, 3]]
	# p.empty_px = 1
	# p.empty_py = 1

	# p.box = [[4, 1, 8],[3, 2, 5],[0, 7, 6]]
	# p.empty_px = 2
	# p.empty_py = 0

	# p.box = [[4, 3, 0],[7, 5, 2],[8, 1, 6]]
	# p.empty_px = 0
	# p.empty_py = 2


	# 20 PASSOS
	# p.box = [[7, 3, 0],[2, 4, 8],[1, 6, 5]]
	# p.empty_px = 0
	# p.empty_py = 2

	# p.box = [[1, 4, 0],[3, 8, 2],[7, 6, 5]]
	# p.empty_px = 0
	# p.empty_py = 2

	# p.box = [[1, 2, 6],[8, 7, 4],[0, 5, 3]]
	# p.empty_px = 2
	# p.empty_py = 0

	# p.box = [[2, 5, 0],[1, 8, 7],[4, 3, 6]]
	# p.empty_px = 0
	# p.empty_py = 2

	p.box = [[3, 1, 2],[4, 0, 5],[6, 7, 8]]
	p.empty_px = 1
	p.empty_py = 1




	# p.box = [[8,6,7],[2,5,4],[3,0,1]]  # 31 passos
	# p.empty_px = 2
	# p.empty_py = 1








	
	# print "p: "
	# print_box(p.box)
	print argv[1]
	if argv[1] == "1":
		bfs = Breadth(p, 3)
		result = bfs.search()
	elif argv[1] == "2":
		dfs = Depth(p, 3, max_shuffle)
		result = dfs.search()
	else:
		idfs = ItetariveDeapth(p, 3)
		result = idfs.search()
	

	# print_result(result.path, p.box, [p.empty_px, p.empty_py])

	if result != None:
		print "Resposta Encontrada"
		print "Numero de Passos: " + str(len(result.path))
	else:
		print "Resposta Nao Encontrada!"



if __name__ == '__main__':
	main(sys.argv)