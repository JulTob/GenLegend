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

from collections.abc import Mapping

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
	A Report that always gives back one fixed value, for a value that is a Tag or a function.

	A plain value written on a Tag class (``NAME = "Rage"``, a number, a
	tuple) already is a Report in effect: readable on the Tag, never on the
	Character.  Write those as plain class data (Julio, Dialog 0027,
	2026-10-05: "supposed to be just a normal report"; QST-0144.2).

	A Tag class or a function stored as plain class data is different: TopKit
	turns a callable into an Action on the Character.  Wrap only those, so
	the Tag keeps them as a value: a Training's ``PATH`` (a Tag), a
	Background's ``ORIGIN_FEAT`` (a Tag), a Specialization's generic
	``reports=`` hook (anything).
	"""
	def Builder(
			tag,
			):
		return value

	return Report(
		Builder
		)


class Field_Index(Mapping):
	"""
	A read-only Mapping that is a live view of a Pin's Field.

	A Pin's Field (``Declared_Guild[:]``) is the catalogue of a family, in
	declaration order.  Readers that want it by name get one of these instead
	of a second dictionary: ``index`` reads the Field and keys it, and every
	read calls it again, so a Tag is in the Mapping the moment it is pinned
	and nothing is listed twice (QST-0144.5).  ``GUILDS`` and ``MANEUVERS``
	are Field_Index views keyed by NAME: ``GUILDS[ name ]``, ``name in GUILDS``
	and ``sorted( GUILDS )`` keep their spelling and never hold a copy.
	"""

	__slots__ = (
		"_index",
		)

	def __init__(
			view,
			index,
			):
		view._index = index

	def __getitem__(
			view,
			key,
			):
		return view._index()[ key ]

	def __iter__(
			view,
			):
		return iter(
				view._index()
				)

	def __len__(
			view,
			):
		return len(
				view._index()
				)

	def __repr__(
			view,
			) -> str:
		return f"{type( view ).__name__}({dict( view )!r})"


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

	def Pick(
			char,
			ledger,
			weights=None,
			*,
			purpose=None,
			dice=None,
			):
		"""
		Pick one item from a Dice Bag named by the Tag that offers the choice.

		``dice`` takes an already-opened Bag (open it once when one choice
		draws several times); ``purpose`` opens ``char.Dice_Bag( purpose )``
		fresh for this one draw.  One of the two is required: a bare Pick
		is refused, because a purpose nobody wrote would have to be derived
		from the caller's frame, and that moved draws whenever code moved
		(ruling 8, Dialog 0027; QST-0144.6).
		"""
		if not ledger:
			raise ValueError(
				"Pick: empty ledger"
				)

		if dice is None and purpose is None:
			raise ValueError(
				"Pick: name the Dice Bag. Pass dice=char.Dice_Bag( "
				"\"<Tag>.<choice>\" ) or purpose=\"<Tag>.<choice>\"; "
				"every choice of a Character draws from a bag named by the "
				"Tag that offers it (QST-0144.6)."
				)

		source = (
			dice
			if dice is not None
			else char.Dice_Bag(
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
	name.  A Character's first Tag is its Role, by design: everything after
	it may ask what the Character is for.  (Until TopKit 0.2.0a4 the order
	was also load-bearing, because a Flag applied after another Tag did not
	answer by name: QST-0093.10 §1, fixed upstream.)
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

	#-- A bare draw is refused: nobody derives a purpose for it.
	try:
		first.Pick(
			(
				"North",
				"South",
				),
			)
	except ValueError as refusal:
		assert "QST-0144.6" in str(
			refusal
			)
	else:
		raise AssertionError(
			"a bare Pick must be refused"
			)
	assert not hasattr(
		first,
		"Pick_Bag",
		)

	#-- purpose= opens the named bag fresh: the same answer every time.
	by_purpose = tuple(
		first.Pick(
			(
				"North",
				"South",
				"East",
				"West",
				),
			purpose="identity.direction",
			)
		for _ in range(
			3
			)
		)
	assert len(
		set(
			by_purpose
			)
		) == 1
	assert by_purpose[ 0 ] == first.Pick(
		(
			"North",
			"South",
			"East",
			"West",
			),
		dice=first.Dice_Bag(
			"identity.direction"
			),
		)


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
