import math
import random

def make_move(block):
	if block.rotation == "SPLIT":
		return [block.SPLIT_UP(), block.SPLIT_DOWN(),
	       		 block.SPLIT_LEFT(), block.SPLIT_RIGHT(),
				  block.SPLIT_UP_1(), block.SPLIT_DOWN_1(),
	       		   block.SPLIT_LEFT_1(), block.SPLIT_RIGHT_1()]
	return [block.UP(), block.DOWN(),block.LEFT(), block.RIGHT()]


class Node:
	def __init__(self, block, parent) -> None:
		self.block = block
		self.parent = parent
		self.children = []
		self.score = 0
		self.visits = 1


	def select(self):
		if not self.children == []:
			best_child = None
			score = float('-inf')
			c = math.sqrt(2)
			for child in self.children:
				new_score = child.score / child.visits + c * math.sqrt(math.log(self.visits) / child.visits)
				if score < new_score :
					score = new_score
					best_child = child
			return best_child
		


		
	def expand(self):
		self.children = [Node(block, self) for block in make_move(self.block) if block.isValidBlock()]

	def simulate(self):
		i = 0
		queue = []
		queue.append(self.block)
		close = []
		while queue:
			x = random.randint(0,len(queue)-1)
			current = queue.pop(x)

			if current.isGoal():
				return -i

			if current in close:
				continue
			
			close.append(current)

			newBlocks = [block for block in make_move(current) if block.isValidBlock()]
			for block in newBlocks:
				queue.append(block)
			i += 1
			#print(block_.previousMove)
	
	def backpropagate(self, score):
		node = self
		while node is not None:
			node.visits += 1
			node.score += score
			node = node.parent


	
def MonteCarlo(root, max_ite, examined):
	for i in range(max_ite):
		node = root

		#selection
		while node.children:
			node = node.select()
			#print(node.block.previousMove)


			
		#expansion
		if not node.children and not node.block.isGoal():
			node.expand()
		

		#simulation
		score = node.simulate()
		#print(score)
		#backpropagation
		node.backpropagate(score)
	best = max(root.children, key=lambda child: child.visits)

	while best.block in examined:
		try:
			root.children.remove(best)
			best = max(root.children, key=lambda child: child.visits)
		except:
			root.parent.children.remove(root)
			return root.parent
		#best = max(root.children, key=lambda child: child.visits)
	return best

def solve(block):
	root = Node(block, None)
	node = root
	examined = []
	i = 0
	while not node.block.isGoal():
		node = MonteCarlo(node, 10, examined)
		if node.block not in examined:
			examined.append(node.block)
		
		#print(node.block.previousMove)


		#print(node.block.previousMove)
	return node.block