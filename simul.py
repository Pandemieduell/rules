import random as r

class GameState:
	"""docstring for GameState"""
	def __init__(self, mood = 100, taxes = 100, healthcare = 28000,
			new_infected = 1, dead = 0, immune = 0, active = 0, noninfected = int(83e6), growth = 1.33):
		self.mood = mood
		self.taxes = taxes
		self.healthcare = healthcare
		self.new_infected = new_infected
		self.infected = new_infected
		self.dead = dead
		self.immune = immune
		self.active = active
		self.noninfected = noninfected
		self.previous = None
		self.growth = growth
		self.healed = 0
		
	def clone(self):
		g = GameState(self.mood, self.taxes, self.healthcare, self.infected,
			self.dead, self.immune, self.active, self.noninfected)
		g.previous = self
		return g

	def __repr__(self):
		return "GameState(" + ", ".join(map(lambda x: str(x), [self.mood, self.taxes, self.healthcare, self.infected,
			self.dead, self.immune, self.active, self.noninfected])) + ")"

class Card:
	def apply(self, gamestate):
		return gamestate

class ActiveCases(Card):
	def apply(self, gamestate):
		gamestate.active = int(gamestate.infected * 0.05)
		return gamestate

def get_prev_n(gamestate, n):
	for i in range(n):
		if gamestate.previous == None: return None
		gamestate = gamestate.previous
	return gamestate

class Dying(Card):
	def apply(self, gamestate):
		dying = int(get_prev_n(gamestate, 14).new_infected * 0.02 + 0.5) if get_prev_n(gamestate, 14) else 0
		gamestate.dead += dying
		gamestate.new_infected -= dying
		return gamestate

class Healing(Card):
	def apply(self, gamestate):
		gamestate.healed = get_prev_n(gamestate, 18).new_infected if get_prev_n(gamestate, 18) else 0
		return gamestate

def loosing(gamestate):
	return gamestate.active >= gamestate.healthcare


def simulate(n):
	g = GameState()
	cards = [ActiveCases(), Dying()]
	for i in range(n):
		g = g.clone()
		for el in cards:
			g = el.apply(g)
		g.new_infected = int(g.infected * g.growth + r.random() * 5)
		g.infected += g.new_infected
		healed = g.healed
		g.infected -= healed
		g.immune += healed
		print(g)

simulate(6)