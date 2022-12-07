import random

class board:
	def __init__(self,random=False,length=6,avalanche=True,pieces=[]):
		self.length = length
		self.avalanche = avalanche
		self.won = False
		if not random:
			self.pieces = [4] * (length * 2 + 2)
			self.pieces[length] = 0
			self.pieces[length * 2 + 1] = 0
		else:
			if len(pieces) != (length * 2 + 2):
				raise Exception("Not enough holes intialized")
			self.pieces = pieces
		if sum(self.pieces) != 48:
			raise Exception("Wrong number of pieces")
	
	def print(self,p1=True):
		if p1:
			print(f" {self.pieces[-1]} ")
			for x in range(self.length):
				print(f"{self.pieces[x]} {self.pieces[2 * self.length - x]}")
			print(f" {self.pieces[self.length]} ")
		else:
			print(f" {self.pieces[self.length]} ")
			for x in reversed(range(self.length)):
				print(f"{self.pieces[2 * self.length - x]} {self.pieces[x]}")
			print(f" {self.pieces[-1]} ")

	def move(self,idx,p1=True,cascade=False):
		if cascade == False:
			if sum(self.pieces[:self.length]) == 0 or sum(self.pieces[self.length+1:-1]) == 0:
				self.won = True
				return
		if idx < 0 or idx == self.length or idx > self.length * 2:
			return 0
		if cascade == False:
			if p1:
				if idx >= self.length:
					return 0
			else:
				if idx <= self.length:
					return 0
		beads = self.pieces[idx]
		if beads == 0:
			return 0
		self.pieces[idx] = 0
		while beads:
			idx += 1
			if p1:
				if idx == self.length * 2 + 1:
					idx += 1
			else:
				if idx == self.length:
					idx += 1
			idx %= 14
			self.pieces[idx] += 1
			beads -= 1
		if idx == self.length or idx == self.length * 2 + 1:
			return 1
		if self.avalanche:
			if self.pieces[idx] > 2:
				self.move(idx,p1,True)
	
	def copy(self):
		return board(True,self.length,self.avalanche,[x for x in self.pieces])

class player:
	def __init__(self,p1=True):
		self.p1 = p1

	def findpossiblemoves(self,b):
		moves = []
		if self.p1:
			for x in range(b.length):
				if b.pieces[x] > 0:
					moves.append(x)
		else:
			for x in range(b.length+1,b.length*2+1):
				if b.pieces[x] > 0:
					moves.append(x)
		return moves
	
	def findbestmove(self,b):
		moves = self.findpossiblemoves(b)
		scores = {}
		for x in moves:
			c = b.copy()
			if c.move(x,self.p1,False) == 0:
				c.move(self.findbestmove(c),self.p1,False)
			scores[x] = c.pieces[b.length] if self.p1 else c.pieces[-1]
		besti,besty = [0],0
		for i,y in scores.items():
			if y > besty:
				besti,besty = [i],y
			elif y == besty:
				besti.append(i)
		return random.choice(besti)

class game:
	def __init__(self,players=0,random=False,length=6,avalanche=True,pieces=[]):
		self.board=board(random,length,avalanche,pieces)
		self.num_players=players
		if players < 2:
			self.player2 = player(False)
		if players == 0:
			self.player1 = player(True)

	def persontomove(self,p1):
		if self.num_players == 0:
			return False
		if p1 or self.num_players == 2:
			return True
		return False

	def playgame(self):
		p1 = True
		while not self.board.won:
			self.board.print()
			if self.persontomove(p1):
				print(f"{'p1' if p1 else 'p2'} to move")
				m = self.board.move(int(input("Your move: ")),p1)
			else:
				p = self.player1 if p1 else self.player2
				m = self.board.move(p.findbestmove(self.board),p1,False)
			if m == 1:
				print("Bonus move")
			elif m == 0:
				print("Illegal move")
			elif m == None:
				p1 ^= True
		p1_score = self.board.pieces[self.board.length]
		p2_score = self.board.pieces[self.board.length * 2 + 1]
		self.board.print()
		if p1_score > p2_score:
			print(f"Player 1 wins {p1_score} to {p2_score}")
		elif p2_score > p1_score:
			print(f"Player 2 wins {p2_score} to {p1_score}")
		else:
			print(f"Game tied {p1_score} to {p2_score}")

g = game(0)
g.playgame()
