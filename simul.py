import random as r

import matplotlib.pyplot as plt

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
		return "GameState(" + ", ".join(map(lambda x: x[0] + "=" + str(x[1]),
				[("mood", self.mood), ("taxes",self.taxes), ("healthcare",self.healthcare), ("infected",self.infected),
				 ("dead",self.dead), ("immune", self.immune), ("active", self.active), ("noninfected", self.noninfected)])) + ")"

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

class Infect(Card):
	def apply(self, gamestate):
		gamestate.new_infected = int(gamestate.infected * gamestate.growth + r.random() * 5)
		gamestate.noninfected -= gamestate.new_infected
		if gamestate.noninfected < 0:
			gamestate.new_infected -= (-gamestate.noninfected)
			gamestate.noninfected = 0
		gamestate.infected += gamestate.new_infected
		return gamestate

class Heal(Card):
	def apply(self, gamestate):
		healed = gamestate.healed
		gamestate.infected -= healed
		gamestate.immune += healed
		return gamestate


def loosing(gamestate):
	return gamestate.active >= gamestate.healthcare




def simulate(n):
    healed = []
    infected = []
    new_infected = []
    dead = []
    g = GameState()
    cards = [ActiveCases(), Dying(), Infect(), Healing(), Heal()]
    for i in range(n):
        g = g.clone()
        for el in cards:
            g = el.apply(g)
        print(g)
        healed.append(g.healed)
        infected.append(g.infected)
        new_infected.append(g.new_infected)
        dead.append(g.dead)
    plt.plot(healed, label = 'healed')
    plt.plot(infected, label = 'infected')
    plt.plot(new_infected, label = 'new infected')
    plt.plot(dead, label = 'dead')
    plt.legend()
    plt.show()
simulate(30)
