# -*- coding: utf-8 -*-

import pydot

class Node():
# self.pos list structure
	def __init__(self, pos = "", parent = None, depth = 0):
		self.pos = map(int, list(pos))
		self.parent = parent
		self.depth = depth

# 9のindexを返す
	def __nine_index__(self):
		ans = 0
		for i in self.pos:
			if i == 9:
				return ans
			else:
				ans += 1

# 上に移動
	def __up__(self, nine_pos, pos):
		pp = []
		for i in range(9):
			pp.append(pos[i])

		if nine_pos <= 2:
			return None
		else:
			pp[nine_pos] = pp[nine_pos - 3]
			pp[nine_pos - 3] = 9
			return pp

# 下に移動
	def __down__(self, nine_pos, pos):
		pp = []
		for i in range(9):
			pp.append(pos[i])

		if nine_pos >= 6:
			return None
		else:
			pp[nine_pos] = pp[nine_pos + 3]
			pp[nine_pos + 3] = 9
			return pp

# 左に移動
	def __left__(self, nine_pos, pos):
		pp = []
		for i in range(9):
			pp.append(pos[i])

		if nine_pos % 3 == 0:
			return None
		else:
			pp[nine_pos] = pp[nine_pos - 1]
			pp[nine_pos - 1] = 9
			return pp

# 右に移動
	def __right__(self, nine_pos, pos):
		pp = []
		for i in range(9):
			pp.append(pos[i])

		if nine_pos % 3 == 2:
			return None
		else:
			pp[nine_pos] = pp[nine_pos + 1]
			pp[nine_pos + 1] = 9
			return pp

# for example ... pos_list = [1,3,4,2,6,5,8,9,7]
# convert to this ... "134265897"
	def to_String(self, pos_list):
		ret = ""
		for i in pos_list:
			ret += str(i)
		return ret

# number of mismatched tiles
	def h1(self):
		ret = 0
		goal = [1,2,3,4,5,6,7,8,9]
		for i in range(9):
			if self.pos[i] != goal[i]:
				ret += 1
		if self.pos[8] != 9:
			ret -= 1
		return ret

# manhattan distance
	def h2(self):
		ret = 0
		md = ((0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(0,2),(1,2),(2,2))
		for i in range(9):
			if self.pos[i] != 9:
				ret = ret + abs(md[i][0] - md[self.pos[i]-1][0]) + abs(md[i][1] - md[self.pos[i]-1][1])
		return ret


	def g(self):
		return self.depth

	def f(self):
		return self.h1() + self.g()
		#return self.h2() + self.g()

# 図に表示する用に成形する
	def print_node(self, count = 0):
		if count != 0:
			self.count = count
		ret = '(' + str(self.f()) + ') (' + str(self.count) + ')\n'
		for i in range(9):
			if self.pos[i] == 9:
				ret += ' '
			else:
				ret += str(self.pos[i])
			if i == 2 or i == 5:
				ret += '\n'
			if i % 3 == 0 or i % 3 == 1:
				ret += '|'
		return ret


# ４方向に拡張する
# listで返す
	def expand(self):
		nine = self.__nine_index__()
		pos = self.pos
		ret = []
		if self.__up__(nine, pos):
			up = Node(pos = self.to_String(self.__up__(nine, pos)), parent = self, depth = self.depth + 1)
			ret.append(up)
		if self.__down__(nine, pos):
			down = Node(pos = self.to_String(self.__down__(nine, pos)), parent = self, depth = self.depth + 1)
			ret.append(down)
		if self.__left__(nine, pos):
			left = Node(pos = self.to_String(self.__left__(nine, pos)), parent = self, depth = self.depth + 1)
			ret.append(left)
		if self.__right__(nine, pos):
			right = Node(pos = self.to_String(self.__right__(nine, pos)), parent = self, depth = self.depth + 1)
			ret.append(right)
		return ret



if __name__ == '__main__':
	start = Node(pos = "139428765")
	g = pydot.Dot('A-Star', graph_type='digraph')
	g.set_rankdir('UD')

	count = 1
	opend = [[start, start.to_String(start.pos)]]
	closed = []

	while len(opend) != 0:
		# sort
		opend.sort(cmp = lambda x, y: cmp(x[0].f(), y[0].f()))
		expand = opend.pop(0)
		expand_node = expand[0]
		expand_state = expand[1]
		closed.append([expand_node, expand_node.to_String(expand_node.pos)])

		# startノードなら特別な処理
		if expand_node == start:
			node = pydot.Node(start.print_node(count))
			g.add_node(node)
			count += 1

		# goal
		if expand_node.to_String(expand_node.pos) == "123456789":
			break

		# other
		succ = expand_node.expand()
		for i in succ:
			# not opned and not closed
			if i.to_String(i.pos) not in [j[1] for j in opend] and i.to_String(i.pos) not in [j[1] for j in closed]:
				opend.append([i, i.to_String(i.pos)])
				g.add_edge(pydot.Edge(expand_node.print_node(), i.print_node(count)))
				count += 1

			# opend
			if i.to_String(i.pos) in [j[1] for j in opend]:
				index = 0
				for j in range(len(opend)):
					if i.to_String(i.pos) == opend[j][1]:
						index = j
						break
				if opend[index][0].f() > i.f():
					opend.pop(index)
					opend.append([i, i.to_String(i.pos)])
					g.add_edge(pydot.Edge(expand_node.print_node(), i.print_node(count)))
					count += 1

			# closed
			if i.to_String(i.pos) in [j[1] for j in closed]:
				index = 0
				# closeにある配置のindexを取得する
				for j in range(len(closed)):
					if i.to_String(i.pos) == closed[j][1]:
						index = j
						break
				# そのindexのf()とこのiのf()を比較して小さければopenにいれる
				if closed[index][0].f() > i.f():
					closed.pop(index)
					opend.append([i, i.to_String(i.pos)])
					g.add_edge(pydot.Edge(expand_node.print_node(), i.print_node(count)))
					count += 1

	print(g.to_string())





