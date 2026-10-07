# Markov baseline – Nothing fancy, just works
from collections import defaultdict, Counter

class MarkovNameGenerator:
	"""
	Minimal tri-gram (order-3) Markov name generator.
	Usage:
		gen  = MarkovNameGenerator(training_names, dice=char.Dice_Bag("identity.name"))
		name = gen.generate_name()

	``dice`` is the Dice Bag every step of the walk draws from: the start
	state, each next character and the fallback training name (ruling 8,
	QST-0144.6). The name hands down its one bag; nothing here reaches the
	shared generator.
	"""

	def __init__(
			self,
			names,
			order: int = 4,
			*,
			dice,
			):
		self.order = order
		self.dice = dice
		self.model = defaultdict(Counter)   # state -> {next_char: count}
		self.starts = []                    # states seen at word-start
		self._train([n.lower() for n in names if isinstance(n, str)])

	# ── training ────────────────────────────────────────────────
	def _train(self, names):
		for nm in names:
			padded = "^" * self.order + nm + "$"
			for i in range(len(padded) - self.order):
				state = padded[i : i + self.order]
				nxt   = padded[i + self.order]
				self.model[state][nxt] += 1
				if i == 0:
					self.starts.append(state)

	# ── helpers ────────────────────────────────────────────────
	def _weighted_pick(self, counter: Counter) -> str:
		chars, weights = zip(*counter.items())
		return self.dice.choices(chars, weights=weights, k=1)[0]

	# ── public API ─────────────────────────────────────────────
	def generate_name(self, min_len=4, max_len=10, attempts=10) -> str:
		"""
		Make a new name.  Falls back to a random training name after
		<attempts> failed tries (too short / too long).
		"""
		for _ in range(attempts):
			state = self.dice.choice(self.starts)
			out   = ""
			while True:
				nxt = self._weighted_pick(self.model[state])
				if nxt == "$":                    # reached end token
					if min_len <= len(out) <= max_len:
						return out.capitalize()
					break                         # length bad → retry
				out   += nxt
				state  = state[1:] + nxt
				if len(out) >= max_len:           # hard cap (safety)
					break
		# fallback
		return self.dice.choice(self.starts).replace("^", "").capitalize()


def save_markov_as_py(gen: MarkovNameGenerator,
					race: str,
					folder: str = "Atlas_of_Markov") -> str:
	"""
	Persist <race>.py with three variables:
		order, chain, starting_states
	"""
	os.makedirs(folder, exist_ok=True)
	path = Path(folder) / f"{race}.py"
	with path.open("w", encoding="utf8") as f:
		f.write(f"# Auto-generated Markov model for {race}\n")
		f.write(f"order = {gen.order}\n")
		f.write(f"chain = {json.dumps({k: dict(c) for k,c in gen.model.items()})}\n")
		f.write(f"starting_states = {json.dumps(gen.starts)}\n")
	return str(path)


"""
Legacy

class MarkovNameGenerator:
	def __init__(self, names, order=random.randint(1, 6)):
		self.names = [name.lower() for name in names if isinstance(name, str)]
		self.order = order
		self.chain = defaultdict(Counter)
		self.starting_states = []
		self.populate_markov_chain()

	def ends_well(self, name):
		return (
			len(name) > 2
			and name[-1] in 'aeioulnrst'
			and not name.endswith(('kk', 'rr', 'zz'))
			)

	def populate_markov_chain(self):
		for name in self.names:
			padded_name = ('^' * self.order) + name + '$'
			for i in range(len(padded_name) - self.order):
				state = padded_name[i:i + self.order]
				next_char = padded_name[i + self.order]
				self.chain[state][next_char] += 1
				if i == 0:
					self.starting_states.append(state)

	def _weighted_random_choice(self, counter):
		choices, weights = zip(*counter.items())
		return random.choices(choices, weights=weights)[0]

	def generate_name(self, min_length=4, max_length=10, max_attempts=20):
		vowels = 'aeiou'
		consonants = 'bcdfghjklmnpqrstvwxyz'

		for attempt in range(max_attempts):
			state = random.choice(self.starting_states)
			name = ''
			consecutive_vowels = consecutive_consonants = 0

			while True:
				next_char = self._weighted_random_choice(self.chain[state])

				if next_char == '$':
					if min_length <= len(name) <= max_length:
						break  # Valid end
					else:
						# Too short, retry from start
						state = random.choice(self.starting_states)
						name = ''
						consecutive_vowels = consecutive_consonants = 0
						continue

				# Avoid triple repeating letters
				if len(name) >= 2 and next_char == name[-1] == name[-2]:
					continue

				# Enforce vowel/consonant balance
				if next_char in vowels:
					consecutive_vowels += 1
					consecutive_consonants = 0
					if consecutive_vowels > 2:
						continue
				elif next_char in consonants:
					consecutive_consonants += 1
					consecutive_vowels = 0
					if consecutive_consonants > 3:
						continue
				else:
					consecutive_vowels = consecutive_consonants = 0

				name += next_char
				state = state[1:] + next_char

				if len(name) >= max_length:
					break  # Forcefully truncate long names

			name = name.capitalize()
			if is_valid_name(name, "Markov"):
				return name

		# After max attempts, fallback to random choice
		fallback = random.choice(self.names).capitalize()
		return fallback
"""


# ---------------------------------------------------------------------------
# Self-test: the walk draws from the Dice Bag it is handed (QST-0144.6)
# ---------------------------------------------------------------------------


class _Recording_Dice:
	"""A Dice Bag that remembers every pool it was asked to draw from."""

	def __init__(
			self,
			bag,
			):
		self.bag = bag
		self.calls = []

	def choice(
			self,
			pool,
			):
		self.calls.append(
			(
				"choice",
				list(pool),
				),
			)
		return self.bag.choice(
			pool,
			)

	def choices(
			self,
			pool,
			weights=None,
			k=1,
			):
		self.calls.append(
			(
				"choices",
				list(pool),
				k,
				),
			)
		return self.bag.choices(
			pool,
			weights=weights,
			k=k,
			)


_PROBE_NAMES = (
	"Caderan", "Zurvan", "Artemisia", "Celestia", "Elyria",
	"Serafina", "Taran", "Vanora", "Kaelan", "Rianon",
	)


def _test_markov_draws_from_the_given_dice():
	"""Every draw of the walk comes from the dice; the pools are the model's own; the shared stream never moves."""
	import random
	from AtlasActorLudi.CharactersKit import Character

	stdlib_state = random.getstate()
	dice = _Recording_Dice(
		Character(
			seed=3,
			).Dice_Bag(
				"identity.name",
				),
		)
	generator = MarkovNameGenerator(
		_PROBE_NAMES,
		dice=dice,
		)
	name = generator.generate_name()

	assert random.getstate() == stdlib_state, "the stdlib stream moved"
	assert name and name == name.capitalize(), name
	assert dice.calls, "the walk drew nothing"
	next_characters = set("abcdefghijklmnopqrstuvwxyz$")
	for call in dice.calls:
		if call[0] == "choice":
			assert call[1] == generator.starts, call
		else:
			kind, pool, k = call
			assert k == 1, call
			assert set(pool) <= next_characters, call


def _test_markov_is_keyed_by_the_bag():
	"""Same seed, same walk: the bag decides, not the process."""
	from AtlasActorLudi.CharactersKit import Character

	def walk(
			seed,
			):
		return MarkovNameGenerator(
			_PROBE_NAMES,
			dice=Character(
				seed=seed,
				).Dice_Bag(
					"identity.name",
					),
			).generate_name()

	assert walk(3) == walk(3)
	assert any(
		walk(seed) != walk(3)
		for seed in range(4, 12)
		)


if __name__ == "__main__":
	_test_markov_draws_from_the_given_dice()
	_test_markov_is_keyed_by_the_bag()
	print("Map_of_Markov: self-test passed")
