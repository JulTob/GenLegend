import random
import AtlasAlusoris.Map_of_NPC as NPC


def select1(
		options,
		weights=None,
		*,
		dice=None,
		):
	"""
	Selects one item from options using weights if provided.

	``dice`` is the Dice Bag the draw comes from (ruling 8, QST-0144.6);
	Map_of_Names hands down the name's own bag. Without one the draw comes
	from the shared random module, as before: the NonPlayer callers
	(Decree 0004, not ported yet) still bring none.
	"""
	source = (
		dice
		if dice is not None
		else random
		)
	if not weights:
		return source.choice(options)
	try:
		result = source.choices(options, weights=weights, k=1)[0]
	except (ValueError, TypeError):
		if len(options) > len(weights):
			weights = list(weights) + [weights[-1]]
			return select1(options, weights, dice=dice)
		if len(options) < len(weights):
			options = list(options) + [options[-1]]
			return select1(options, weights, dice=dice)
		raise
	return result

def Probability(N = 1, out_of = 6):
	"""
	Calculates the probability of N specific outcomes occurring out of a total number of possible outcomes.

	Parameters:
	N (int): The number of desired outcomes (default is 1).
	out_of (int): The total number of possible outcomes (default is 6).

	Returns:
	float: The probability as a decimal between 0 and 1.
	"""
	# Step 1: Ensure inputs are valid.
	if N < 0 or out_of <= 0:
		raise ValueError("N must be non-negative and out_of must be a positive number.")

	if N > out_of:
		raise ValueError("N cannot exceed the total number of outcomes.")

	# Step 2: Calculate probability.
	probability = N / out_of

	# Step 3: Return the result.
	return probability

def flip_coin():
	return roll_check(1,2)

def check(N=1, out_of=6):
	return roll_check(N,out_of)


def roll_check(N=1, out_of=6):
	"""
	Simulates a dice roll and returns True with a probability of N/out_of.

	Parameters:
	N (int): The number of favorable outcomes (default is 1).
	out_of (int): The total number of possible outcomes (default is 6).

	Returns:
	bool: True with a probability of Probability(N,out_of), False otherwise.
	"""
	# Step 1: Validate inputs.
	if N < 0 or out_of <= 0:
		raise ValueError("N must be non-negative and out_of must be a positive number.")

	if N > out_of:
		raise ValueError("N cannot exceed the total number of outcomes.")

	# Step 2: Generate a random number between 0 and 1.
	random_number = random.uniform(0, 1)

	# Step 3: Compare the random number to the probability.
	result = random_number < Probability(N = N, out_of = out_of)

	return result

def round5s(n):
	return (n//5) * 5

def distance(n):
	result = n
	if n<=5: return 5
	elif n<=10: return 10
	elif n<=20: return 20
	elif n<=30: return 30
	elif n<=60: return 60
	elif n<=100: return 100
	elif n<=120: return 120
	elif n<=200: return 200
	elif n<=240: return 240
	return round5s(result)


def getGenus(lusor):
	"""
	Process the input to determine and initialize the genus.

	Args:
		lusor (Genus, NPC or PC): Input object.

	Returns:
		genus [list]: Genus data.
	"""
	if hasattr(lusor, "genus"):  # Assuming Lusor is a class
		genus = lusor.genus
	elif isinstance(lusor, list):  # Assuming Genus is a class or list
		genus = lusor
	else:
		raise TypeError("Input must be a list or a NPC/PC object.")

	return genus


# ---------------------------------------------------------------------------
# Self-test: select1 draws from the Dice Bag it is handed (QST-0144.6)
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
				list(weights),
				k,
				),
			)
		return self.bag.choices(
			pool,
			weights=weights,
			k=k,
			)


def _test_select1_draws_from_the_given_dice():
	"""select1 draws from the dice it is handed; the pool, the weights and k stay what they were."""
	from AtlasActorLudi.CharactersKit import Character

	def fresh_dice():
		return _Recording_Dice(
			Character(
				seed=1,
				).Dice_Bag(
					"identity.name",
					),
			)

	options = ["a", "b", "c"]

	dice = fresh_dice()
	assert select1(options, dice=dice) in options
	assert dice.calls == [("choice", options)], dice.calls

	dice = fresh_dice()
	assert select1(options, [1, 2, 3], dice=dice) in options
	assert dice.calls == [("choices", options, [1, 2, 3], 1)], dice.calls

	#-- A short weights list is padded with its last weight; the dice stay the same.
	dice = fresh_dice()
	assert select1(options, [1, 2], dice=dice) in options
	assert dice.calls[-1] == ("choices", options, [1, 2, 2], 1), dice.calls

	#-- Same bag, same answer: the bag decides, not the process.
	def pick(
			seed,
			):
		return select1(
			list("abcdefgh"),
			dice=Character(
				seed=seed,
				).Dice_Bag(
					"identity.name",
					),
			)

	assert pick(5) == pick(5)


def _test_select1_without_dice_keeps_the_old_behaviour():
	"""No Dice Bag: the shared random module answers, as before the port."""
	options = ["a", "b", "c"]
	assert select1(options) in options
	assert select1(options, [1, 2, 3]) in options


if __name__ == "__main__":
	_test_select1_draws_from_the_given_dice()
	_test_select1_without_dice_keeps_the_old_behaviour()
	print("Map_of_Useful_Functions: self-test passed")
