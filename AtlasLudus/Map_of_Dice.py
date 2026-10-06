# AtlasLudus/Map_of_dice.py

# Define a custom error class for Map_of_dice.py
class DiceError(Exception):
    """Base exception for Dice-related errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

### Dice and Rolling Functions ###
import app.random as random
import re



def Dice(D: int = 6, N: int = 1, modifier: int = 0, *, dice=None) -> int:
	'''	Cartography '''
	"""
	Rolls N dices with D sides each.
	If D is 0, simulates a coin flip.
	Adds the base modifier to the result.

	``dice`` is an opened Dice Bag (a random.Random) the roll draws from:
	a Character's roll passes the bag it opened for that purpose
	(ruling 8, QST-0144.6).  Without it the roll falls back to the shared
	app.random stream, which only code outside a Character's build may use.

	Preconditions:
	-	D >= 0 (Number of sides on each die)
	-	N > 0 (Number of dice)
	-	modifier is an integer.

	Postconditions:
	-	Returns the sum of the rolls plus the modifier.
	"""
	if N<1: 	N = 1
	source = random if dice is None else dice
	roll = 0

	for _ in range(N):
		if D >= 1:
			throwing = source.randint(1, D)
		else:
			throwing = source.randint(D, 1)
		roll += throwing
	#print(f"Rolling {N}d{D}: {roll}")
	result = roll + modifier

	if not isinstance(result, int):
		raise DiceError(f"Unexpected result type: {type(result)}. Expected int.")
	return result

def Roll(text: str = "1d20", *, dice=None) -> int:
	"""	Interprets a dice roll string (e.g., '2d6 + 3')
	and executes the roll.
	``dice`` is the opened Dice Bag handed on to Dice().
	Preconditions:
	-	Text is a string in 'NdM + X' format.
	Postconditions:
	-	Returns the result of the roll.
	"""
	if not isinstance(text, str): raise DiceError("Input must be a string.")

	match = re.match(r'(\d+)d(\d+)(?:\s*\+\s*(\d+))?', text)
	if not match:
		raise DiceError(f"Invalid dice roll format: {text}")

	# Extracting the values
	num_dice = int(match.group(1))
	num_sides = int(match.group(2))
	modifier = match.group(3)

	if modifier:
		modifier = int(modifier)
	else:
		modifier = 0


	result = Dice(D = num_sides, N = num_dice, modifier = modifier, dice = dice)
	if not isinstance(result, int): raise DiceError("Dice result not an integer.")
	return result

def Dizero(D: int = 6, N: int = 1) -> int:
	"""	Rolls a dice with sides 0 to D.
	Preconditions:
	-	D and N are integers
	- 	N is positive.
	Postconditions:
	-	Returns the sum of the rolls.
	"""
	if not isinstance(D, int): raise DiceError("D must be an integer.")
	if not isinstance(N, int) and N > 0: raise DiceError("N must be a positive integer.")

	roll = 0
	for m in range(N):
		if D < 0:
			throwing = random.randint(D, 0)
		else:
			throwing = random.randint(0, D)
		roll += throwing
	result = roll
	if not isinstance(result, int): raise DiceError("Output must be an integer.")
	return result

def SelectDx(d=0, pb=2):
	if d == 0:
		result = random.choice(
			["D4",	"D6",	"D8",	"D10"]
			)
		return result
	return f"D{d}"

def New_Stat():
	rolls = [Dice(6) for _ in range(4)]
	return sum(sorted(rolls)[1:])


if __name__ == "__main__":
	from random import Random

	#-- a roll from an opened bag is the bag's own stream: it replays per
	#-- bag and stays inside the die
	first = [Dice(6, dice=Random(7)) for _ in range(5)]
	second = [Dice(6, dice=Random(7)) for _ in range(5)]
	assert first == second, (first, second)
	assert all(1 <= value <= 6 for value in first), first

	bag = Random(1)
	expected = 2 + sum(bag.randint(1, 8) for _ in range(3))
	assert Dice(8, N=3, modifier=2, dice=Random(1)) == expected

	#-- Roll parses the text and rolls from the same bag
	assert Roll("3d8 + 2", dice=Random(1)) == expected
	assert 1 <= Roll("1d20", dice=Random(3)) <= 20

	#-- the coin flip (D = 0) draws from the bag too
	assert Dice(0, dice=Random(2)) in (0, 1)

	#-- without a bag the shared stream still answers: combat code outside
	#-- a Character's build keeps it for now (QST-0144.6)
	assert 1 <= Dice(6) <= 6

	print("OK - Map_of_Dice: a roll draws from the Dice Bag it is given.")
