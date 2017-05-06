from random import randint
from copy import deepcopy
from collections import deque

class Puzzle(object):
	def __init__(self, size):
		self.size = size
		self.box = []
		for i in range(0,self.size):
			self.box.append([])
			for y in range(0,self.size):
				self.box[i].append(i*self.size+y+1)

		self.box[i][y] = 0

		self.empty_px = self.size-1
		self.empty_py = self.size-1

		# print self.box

	def copy(self, p):
		
		self.box = deepcopy(p.box)
		self.empty_px = p.empty_px
		self.empty_py = p.empty_py

		# print self.box

	def move_up(self):

		if (self.empty_py - 1) >= 0:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px][self.empty_py - 1]
			self.box[self.empty_px][self.empty_py - 1] = 0
			self.empty_py -= 1
			# print self.box
			return True
		else:
			return False

	def move_down(self):
		if (self.empty_py + 1) < self.size:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px][self.empty_py + 1]
			self.box[self.empty_px][self.empty_py + 1] = 0
			self.empty_py += 1
			# print self.box
			return True
		else:
			return False

	def move_left(self):
		if (self.empty_px - 1) >= 0:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px - 1][self.empty_py]
			self.box[self.empty_px - 1][self.empty_py] = 0
			self.empty_px -= 1
			# print self.box
			return True
		else:
			return False

	def move_right(self):
		if (self.empty_px + 1) < self.size:
			self.box[self.empty_px][self.empty_py] = self.box[self.empty_px + 1][self.empty_py]
			self.box[self.empty_px + 1][self.empty_py] = 0
			self.empty_px += 1
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
		# print "--I--"
		# print self.box
		# print result
		# print "--F--"
		if result == 1:
			return True
		else:
			return False

	def compare(self, state):
		if self.box == state.box:
			# print "conflict"
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

		print self.box

class Breadth(object):
	
	def __init__(self, initial_state, size):
		
		self.open_nodes = deque([])
		self.visited = []
		self.initial_state = deepcopy(initial_state)
		self.open_nodes.append(self.initial_state)

		self.size = size

	def search(self):
		
		t_open = 1

		t_visited = 0

		while self.open_nodes:

			s = self.open_nodes.popleft()

			self.visited.append(s)
			t_visited += 1

			if s.is_final():
				print "Visited: "+ str(t_visited)
				print "Open: "+ str(t_open)
				return s
			# else: 
				# print "Not final"
			
			# Abre vizinho de cima se possivel
			up = Puzzle(self.size)
			up.copy(s)
			if up.move_up():
				if not self.check_visited(up):
					self.open_nodes.append(up)
					t_open += 1

			# Abre vizinho de baixo se possivel
			down = Puzzle(self.size)
			down.copy(s)
			if down.move_down():
				if not self.check_visited(down):
					self.open_nodes.append(down)
					t_open += 1

			# Abre vizinho da esquerda se possivel
			left = Puzzle(self.size)
			left.copy(s)
			if left.move_left():
				if not self.check_visited(left):
					self.open_nodes.append(left)
					t_open += 1

			# Abre vizinho de direita se possivel
			right = Puzzle(self.size)
			right.copy(s)
			if right.move_right():
				if not self.check_visited(right):
					self.open_nodes.append(right)
					t_open += 1

		return None

	def check_visited(self, state):
		for x in self.visited:
			if x.compare(state):
				return True
		return False

def main():
	print "p: "
	p = Puzzle(3)
	print "p shuffle: "
	p.shuffle(1000)
	print "p: "
	print p.box

	bfs = Breadth(p, 3)
	result = bfs.search()
	if result != None:
		print result.box
	else:
		print "Resposta nao encontrada!"



if __name__ == '__main__':
	main()