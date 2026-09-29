"""
CharactersKit

Contains:
	Character: shared skeleton (seed, dices, Roll/Dice, dummies)
	Role / Player / NonPlayer: Core role Tags

Seeds: repeatability between calls.
Dice: the Character's owned RNG.
	``dices`` holds the main bag.
	``Roll`` / ``Dice`` draw from it.
	``Dice_Bag`` opens a deterministic bag for one stable purpose.

Expected behaviour

For any character, with Role Tags, say charlie:
```
charlie = Character( name= "Charlie" )

Player( charlie )
Wizard( charlie )
Farmer( charlie )

these should return true:
assert charlie in Player
assert charlie in Wizard
assert "Player" in charlie      # Player is a @Flag: it answers by name

```

"""

from TopKit import Flag, Pre, Report, Tag, TagPreconditionError


def _tag_holds(
		char,
		candidate,
		) -> bool:
	"""Whether this Character already carries the candidate Tag."""
	try:
		return char in candidate
	except TypeError:
		return False


def Report_Of(
		value,
		):
	"""
	A Report that always gives back one fixed value.

	TopKit 0.2.0a3 builds Reports from functions (``@Report def X(tag)``) and
	no longer accepts ``Report( value )``.  A factory that declares Tags from
	data needs the value form, so this wraps the value in a builder.  A plain
	value would mostly do, but a function stored as plain class data becomes
	an Action on the Character; a Report keeps it a plain value on the Tag.
	Proposed upstream in QST-0093.10.
	"""
	def Builder(
			tag,
			):
		return value

	return Report(
		Builder
		)


# ---------------------------------------------------------------------------
# Skeleton
# ---------------------------------------------------------------------------

class Character:
	"""Minimal shared substrate for every Player or NonPlayer Character."""

	def __init__(
			char,
			seed: int = -1,
			level: int = 1,
			):
		"""Construct the Character skeleton."""
		from random import Random

		from AtlasActorLudi.ProficiencyKit import Training_Record

		rng = Random()
		char.seed = int(
			seed
			if seed >= 0
			else rng.randint(
				0,
				2**64,
				)
			)
		char.dices = Random(
			char.seed
			)
		char.level = max(
			1,
			int(
				level
				),
			)
		char.training = Training_Record()

	# --- Dice Methods ----------------------------------------------

	def Roll(
			char,
			D: int = 6,
			N: int = 1,
			modifier: int = 0,
			*,
			dice=None,
			) -> int:
		"""
		Roll N dice with D sides and add a modifier
		from the Character's Dice Bag.

		``dice`` rolls from a named Bag instead of the Character's
		single stream, for a roll whose result must not depend on
		how many other rolls happened first.
		"""
		if N < 1:
			N = 1

		source = (
			dice
			if dice is not None
			else char.dices
			)

		total = 0

		for _ in range(
				N
				):
			if D >= 1:
				total += source.randint(
					1,
					D,
					)
			else:
				total += source.randint(
					D,
					1,
					)

		return total + modifier

	# Alias used in Decree / Dialog prose
	Dice = Roll

	def Roll_Zero(
			char,
			D: int = 6,
			N: int = 1,
			) -> int:
		"""Roll N zero-based dice from this Character's Dice Bag."""
		if N < 1:
			N = 1

		lower = min(
			0,
			D,
			)
		upper = max(
			0,
			D,
			)

		return sum(
			char.dices.randint(
				lower,
				upper,
				)
			for _ in range(
				N
				)
			)

	def __invert__(char):
		"""Reseed this Character's Dice from its fixed seed."""
		char.dices.seed(
			char.seed
			)

		return char.seed

	def New_Score(char):
		"""Roll 4d6 and drop the lowest result."""
		rolls = [
			char.Dice(
				6
				)
			for _ in range(
				4
				)
			]

		return sum(
			sorted(
				rolls
				)[
					1:
					]
			)

	def Pick_Bag(
			char,
			purpose=None,
			*,
			version: str = "1",
			namespace: str = "GenLegend",
			):
		"""
		The Dice Bag one draw should come from, advanced per purpose.

		Successive draws for the same purpose open ``purpose#0``,
		``purpose#1`` and so on. Different purposes stay independent.
		A bare call derives purpose from the caller's module.function.
		"""
		if purpose is None:
			from sys import _getframe

			frame = _getframe(
				2
				)
			purpose = (
				f"{frame.f_globals.get('__name__', '?')}"
				f".{frame.f_code.co_qualname}"
				)

		counts = getattr(
			char,
			"_pick_draws",
			None,
			)

		if counts is None:
			counts = {}
			char._pick_draws = counts

		drawn = counts.get(
			purpose,
			0,
			)
		counts[
			purpose
			] = drawn + 1

		return char.Dice_Bag(
			f"{purpose}#{drawn}",
			version=version,
			namespace=namespace,
			)

	def Pick(
			char,
			ledger,
			weights=None,
			*,
			purpose=None,
			dice=None,
			):
		"""
		Pick one item from a named Dice Bag.

		``dice`` takes an already-opened Bag; ``purpose`` names one to open.
		Neither is required: a bare ``Pick`` still draws deterministically
		via ``Pick_Bag``.
		"""
		if not ledger:
			raise ValueError(
				"Pick: empty ledger"
				)

		source = (
			dice
			if dice is not None
			else char.Pick_Bag(
				purpose
				)
			)

		if weights is None:
			return source.choice(
				list(
					ledger
					)
				)

		return source.choices(
			list(
				ledger
				),
			weights=weights,
			k=1,
			)[
				0
				]

	def Accept(
			char,
			ledger,
			weights=None,
			*,
			purpose=None,
			dice=None,
			imprint=None,
			in_order=False,
			attempts=100,
			):
		"""
		Draw from a pool until a candidate's Preconditions accept
		this Character.

		Each refusal is reported as a Minion bug tree and dropped from
		the remaining ledger. An exhausted pool raises — that is a real
		bug. ``in_order`` walks the ledger as given; otherwise each
		attempt uses ``Pick``. ``imprint`` defaults to ``candidate(char)``.
		"""
		from Minion import report_bug

		remaining = list(
			ledger
			)
		if not remaining:
			raise ValueError(
				"Accept: empty ledger"
				)

		remaining_weights = (
			list(
				weights
				)
			if weights is not None
			else None
			)
		if (
			remaining_weights is not None
			and len(
				remaining_weights
				) != len(
					remaining
					)
			):
			raise ValueError(
				"Accept: weights must match the ledger."
				)

		ceiling = min(
			max(
				1,
				int(
					attempts
					)
				),
			100,
			)
		last_refusal = None

		for _ in range(
				ceiling
				):
			if not remaining:
				break

			candidate = (
				remaining[
					0
					]
				if in_order
				else char.Pick(
					remaining,
					weights=remaining_weights,
					purpose=purpose,
					dice=dice,
					)
				)

			if (
				imprint is None
				and _tag_holds(
					char,
					candidate,
					)
				):
				return candidate

			try:
				if imprint is None:
					candidate(
						char
						)
				else:
					imprint(
						candidate
						)
			except TagPreconditionError as err:
				report_bug(
					err
					)
				last_refusal = err
				index = remaining.index(
					candidate
					)
				remaining.pop(
					index
					)
				if remaining_weights is not None:
					remaining_weights.pop(
						index
						)
				continue

			return candidate

		raise ValueError(
			"No candidate in this pool accepted the Character."
			) from last_refusal

	def Dice_Bag(
			char,
			purpose: str,
			*,
			version: str = "1",
			namespace: str = "GenLegend",
			):
		"""Open a fresh deterministic Dice Bag for one stable purpose."""
		from hashlib import blake2b
		from random import Random

		bag_purpose = str(
			purpose
			).strip()
		bag_version = str(
			version
			).strip()
		bag_namespace = str(
			namespace
			).strip()

		if not bag_purpose:
			raise ValueError(
				"A Character Dice Bag requires a stable purpose."
				)

		if not bag_namespace:
			raise ValueError(
				"A Character Dice Bag requires a namespace."
				)

		material = (
			f"{char.seed}|{bag_purpose}|{bag_version}"
			).encode(
				"utf-8"
				)
		digest = blake2b(
			material,
			digest_size=16,
			person=bag_namespace.encode(
				"utf-8"
				)[
					:16
					],
			).digest()

		return Random(
			int.from_bytes(
				digest,
				"big",
				)
			)


# ---------------------------------------------------------------------------
# Character Tags
# ---------------------------------------------------------------------------

@Flag
class Role(Tag):
	"""Root Tag for a Character's play role.

	Role, Player and NonPlayer are Flags: ``"Player" in char`` answers by
	name.  A Character's first Tag is its Role, and that matters today:
	TopKit 0.2.0a3 installs name lookups only when a Character's first Tag is
	a Flag (QST-0093.10, a Suggest-to-TopKit questa).
	"""

	@Pre
	def is_Character(
			target,
			):
		"""Limit Role Tags to Characters."""
		return isinstance(
			target,
			Character,
			)


@Flag
class Player(Role):
	"""Player-character role."""

	@Pre
	def no_npc(
			target,
			):
		"""Exclude Characters carrying the NonPlayer Shape."""
		assert target not in NonPlayer


@Flag
class NonPlayer(Role):
	"""Non-player Character role."""

	@Pre
	def no_player(
			target,
			):
		"""Exclude Characters carrying the Player Shape."""
		assert target not in Player


# ---------------------------------------------------------------------------
# Focused core suite
# ---------------------------------------------------------------------------

def _test_rng_determinism():
	"""Seed fully determines the Dice Bag; inversion reseeds it."""
	a = Character(
		seed=42
		)
	b = Character(
		seed=42
		)
	sequence = [
		a.Roll(
			20
			)
		for _ in range(
			5
			)
		]

	assert sequence == [
		b.Roll(
			20
			)
		for _ in range(
			5
			)
		]
	assert all(
		1 <= result <= 20
		for result in sequence
		)
	assert isinstance(
		a.seed,
		int,
		)
	assert (~a) == 42
	assert [
		a.Roll(
			20
			)
		for _ in range(
			5
			)
		] == sequence


def _test_roll_shape():
	"""Roll honors D, N, and modifier; Dice is the alias."""
	assert Character.Dice is Character.Roll
	assert Character(
		seed=1
		).Roll(
			D=1,
			N=3,
			) == 3
	assert Character(
		seed=1
		).Roll(
			D=1,
			N=0,
			) == 1
	assert Character(
		seed=1
		).Roll(
			D=6,
			N=1,
			modifier=100,
			) >= 101
	assert 0 <= Character(
		seed=1
		).Roll_Zero(
			D=6,
			N=4,
			) <= 24
	assert -12 <= Character(
		seed=1
		).Roll_Zero(
			D=-3,
			N=4,
			) <= 0


def _test_dice_bags():
	"""Purpose Dice Bags are stable, isolated, and level-independent."""
	first = Character(
		seed=91,
		level=1,
		)
	progressed = Character(
		seed=91,
		level=20,
		)
	dice_state = first.dices.getstate()
	first_bag = first.Dice_Bag(
		"identity.story"
		)
	progressed_bag = progressed.Dice_Bag(
		"identity.story"
		)

	first_values = tuple(
		first_bag.randint(
			1,
			20,
			)
		for _ in range(
			4
			)
		)
	progressed_values = tuple(
		progressed_bag.randint(
			1,
			20,
			)
		for _ in range(
			4
			)
		)

	assert first_values == progressed_values
	assert first.dices.getstate() == dice_state

	first_choice = first.Pick(
		(
			"North",
			"South",
			),
		dice=first.Dice_Bag(
			"identity.direction"
			),
		)
	progressed_choice = progressed.Pick(
		(
			"North",
			"South",
			),
		dice=progressed.Dice_Bag(
			"identity.direction"
			),
		)

	assert first_choice == progressed_choice
	assert first.dices.getstate() == dice_state


def _test_level():
	"""Level clamps to at least one and remains explicit state."""
	assert Character(
		level=0
		).level == 1
	assert Character(
		level=3
		).level == 3

	character = Character(
		seed=1,
		level=2,
		)

	assert character.level == 2
	assert character.level <= 3
	assert character.level >= 1


def _test_tag_queries():
	"""Semantic membership is queried through Tags."""
	character = Character(
		seed=7,
		level=1,
		)

	assert character not in Player
	assert character not in Role


def _test_player_role():
	"""Role membership includes the Shape and its Base."""
	hero = Character(
		seed=5,
		level=2,
		)
	Player(
		hero
		)

	assert hero in Player and hero in Role
	assert Player in hero and Role in hero
	assert "Player" in hero and "Role" in hero
	assert "player" not in hero
		#-- A Flag answers to its exact class name: case matters.
	assert "Wizard" not in hero


def _test_is_character_contract():
	"""The Role precondition rolls back tagging a non-Character."""
	class NotACharacter:
		pass

	try:
		Player(
			NotACharacter()
			)
	except Exception as error:
		assert isinstance(
			error,
			TagPreconditionError,
			)
	else:
		raise AssertionError(
			"Player must reject a non-Character"
			)


def _test_spaced_name():
	"""Python Tag identity stays separate from a display-name Report."""
	class Eldritch_Knight(Role):
		NAME = "Eldritch Knight"

	knight = Character(
		seed=7
		)
	Eldritch_Knight(
		knight
		)

	assert knight in Eldritch_Knight and knight in Role
	assert "Role" in knight
	assert "Eldritch_Knight" not in knight
		#-- Not a Flag, so it does not answer by name.
	assert Eldritch_Knight.NAME == "Eldritch Knight"
	assert "Eldritch Knight" not in knight
		#-- NAME is for display only; it is never a lookup word.


def _test_nonplayer_role():
	"""NonPlayer uses canonical Tag identity; aliases belong in Maps."""
	npc = Character(
		seed=3
		)
	NonPlayer(
		npc
		)

	assert npc in NonPlayer
	assert NonPlayer in npc and Player not in npc
	assert "NonPlayer" in npc
	assert "NPC" not in npc


def _self_test():
	"""Run the focused core suite."""
	_test_rng_determinism()
	_test_roll_shape()
	_test_dice_bags()
	_test_level()
	_test_tag_queries()
	_test_player_role()
	_test_is_character_contract()
	_test_spaced_name()
	_test_nonplayer_role()

	print(
		"OK — CharactersKit self-test"
		)


if __name__ == "__main__":
	_self_test()
