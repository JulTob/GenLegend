"""
MetamagicKit

Metamagic options as Tags: the ways a Sorcerer reshapes a spell while casting
it.  Distinct from Guild Training (the lesson that teaches Metamagic) and from
Spells (what gets reshaped).

Every option edits one parameter of a spell, and nothing else:

	range          Distant Spell
	duration       Extended Spell
	casting time   Quickened Spell
	targets        Twinned Spell
	saving throw   Careful Spell, Heightened Spell
	damage         Empowered Spell, Transmuted Spell
	attack roll    Seeking Spell
	components     Subtle Spell

So an option is declared by what it costs and what it changes, not by prose
about itself.  ``Build_Metamagic`` takes those as fields and returns a Shape of
the ``Metamagic`` root.  A Character carries the options it knows as Tag
memberships: ``character in Quickened_Spell`` is the whole question, and the
sheet names exactly the options the Dice Bag chose.

Applying an option is a Tagging, so it must happen outside every other Tag's
Imprint.  TagKit refuses to Tag a Target that is still mid-application, which
is why ``Apply_Metamagic`` is called from a Specialization's ``after`` rite
and never from inside a Training's ``apply``.
"""

from __future__ import annotations

from collections.abc import Callable
from types import MappingProxyType
from typing import Any

from TagKit import Pre, Report, Tag

from AtlasActorLudi.CharactersKit import Character


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


class Metamagic(Tag):
	"""One way of reshaping a spell, paid for in Sorcery Points."""

	NAME = "Metamagic"

	@Pre
	def Character_Only(
			target,
			) -> bool:
		return isinstance(
				target,
				Character,
				)

	@Pre
	def Font_Of_Magic_Opened(
			target,
			) -> bool:
		"""Metamagic is paid in Sorcery Points, and those open at Sorcerer 2."""
		from AtlasLusoris.TrainingKit import level_in_guild
		return level_in_guild(
				target,
				"Sorcerer",
				) >= 2


_METAMAGIC_TAGS: dict[str, type[Metamagic]] = {}


def _class_name(
		name: str,
		) -> str:
	return "_".join(
			part.capitalize()
			for part in name.split()
			)


def Build_Metamagic(
		*,
		name: str,
		cost: int,
		rule: str | Callable[[Any], str],
		stacks: bool = False,
		) -> type[Metamagic]:
	"""
	Construct one Metamagic option Tag.

	``cost`` is in Sorcery Points.  ``rule`` is the option's rule text, or a
	callable taking the Character when the text quotes a number the sheet
	already knows.  ``stacks`` marks the two options the rules let ride on a
	spell that another option has already reshaped.
	"""
	if not name or not name.strip():
		raise ValueError(
				"Build_Metamagic: name is required."
				)
	if name in _METAMAGIC_TAGS:
		raise ValueError(
				f"Build_Metamagic: {name!r} is already declared."
				)
	if cost < 1:
		raise ValueError(
				f"Build_Metamagic: {name!r} must cost at least 1 Sorcery "
				f"Point, not {cost!r}."
				)
	if not rule:
		raise ValueError(
				f"Build_Metamagic: {name!r} needs its rule text."
				)

	option = type(
			_class_name(
					name
					),
			(
					Metamagic,
					),
			{
					"__doc__": f"{name}, a Metamagic option.",
					"__module__": __name__,
					"NAME": name,
					"COST": Report(
							cost
							),
					"RULE": Report(
							rule
							),
					"STACKS": Report(
							stacks
							),
					},
			)
	_METAMAGIC_TAGS[
			name
			] = option
	return option


# ---------------------------------------------------------------------------
# Rules that quote the Character
# ---------------------------------------------------------------------------


def _charisma_modifier(
		char,
		) -> int:
	"""The Charisma modifier, never below one, as the options count it."""
	from AtlasActorLudi.Map_of_Scores import Modifier
	scores = getattr(
			char,
			"AS",
			None,
			)
	charisma = getattr(
			scores,
			"CHA",
			10,
			)
	return max(
			1,
			Modifier(
					charisma
					),
			)


def _careful_rule(
		char,
		) -> str:
	count = _charisma_modifier(
			char
			)
	return (
		"When you cast a spell that forces other creatures to make a saving "
		f"throw, choose up to <b>{count}</b> of them (your Charisma modifier). "
		"Each chosen creature automatically succeeds on its saving throw "
		"against the spell, and takes no damage if it would normally take "
		"half damage on a success."
		)


def _empowered_rule(
		char,
		) -> str:
	count = _charisma_modifier(
			char
			)
	return (
		"When you roll damage for a spell, you reroll up to "
		f"<b>{count}</b> of the damage dice (your Charisma modifier) and use "
		"the new rolls. You can do this even when another option has "
		"already reshaped the spell."
		)


# ---------------------------------------------------------------------------
# The ten options (PHB 2024)
# ---------------------------------------------------------------------------


Careful_Spell = Build_Metamagic(
		name="Careful Spell",
		cost=1,
		rule=_careful_rule,
		)

Distant_Spell = Build_Metamagic(
		name="Distant Spell",
		cost=1,
		rule=(
			"When you cast a spell with a range of at least 5 feet, you "
			"double its range. When you cast a spell with a range of Touch, "
			"its range becomes 30 feet."
			),
		)

Empowered_Spell = Build_Metamagic(
		name="Empowered Spell",
		cost=1,
		rule=_empowered_rule,
		stacks=True,
		)

Extended_Spell = Build_Metamagic(
		name="Extended Spell",
		cost=1,
		rule=(
			"When you cast a spell whose duration is 1 minute or longer, you "
			"double that duration, to a maximum of 24 hours. If the spell "
			"requires Concentration, you have Advantage on saving throws to "
			"keep it."
			),
		)

Heightened_Spell = Build_Metamagic(
		name="Heightened Spell",
		cost=2,
		rule=(
			"When you cast a spell that forces a creature to make a saving "
			"throw, one target of the spell has Disadvantage on its saving "
			"throws against it."
			),
		)

Quickened_Spell = Build_Metamagic(
		name="Quickened Spell",
		cost=2,
		rule=(
			"When you cast a spell with a casting time of an action, you cast "
			"it as a Bonus Action instead. You can't do this if you have "
			"already cast a level 1+ spell this turn, and after doing it you "
			"can't cast another level 1+ spell this turn."
			),
		)

Seeking_Spell = Build_Metamagic(
		name="Seeking Spell",
		cost=1,
		rule=(
			"When you miss with a spell attack roll, you reroll the d20 and "
			"use the new roll. You can do this even when another option has "
			"already reshaped the spell."
			),
		stacks=True,
		)

Subtle_Spell = Build_Metamagic(
		name="Subtle Spell",
		cost=1,
		rule=(
			"When you cast a spell, you cast it without Verbal, Somatic or "
			"Material components, except Material components the spell "
			"consumes or that have a listed cost."
			),
		)

Transmuted_Spell = Build_Metamagic(
		name="Transmuted Spell",
		cost=1,
		rule=(
			"When you cast a spell that deals Acid, Cold, Fire, Lightning, "
			"Poison or Thunder damage, you change that damage to another type "
			"from the same list."
			),
		)

Twinned_Spell = Build_Metamagic(
		name="Twinned Spell",
		cost=1,
		rule=(
			"When you cast a spell that could target one more creature if "
			"cast with a higher-level spell slot, such as Charm Person, you "
			"raise the spell's effective level by 1."
			),
		)


METAMAGIC = MappingProxyType(
		_METAMAGIC_TAGS
		)


# ---------------------------------------------------------------------------
# Choosing, carrying, and reading
# ---------------------------------------------------------------------------


def Resolve_Metamagic(
		char,
		count: int,
		) -> tuple[str, ...]:
	"""
	The first ``count`` options in this Character's own stable order.

	The order is one shuffle of the catalogue from a named Dice Bag, so it
	does not depend on how many other draws happened first.  A Sorcerer who
	knows four options knows the same first two they would have known at
	level 2: gaining options adds to the list and never swaps it.
	"""
	if count < 0:
		raise ValueError(
				f"Resolve_Metamagic: count must not be negative, not {count!r}."
				)
	order = list(
			METAMAGIC
			)
	dice = char.Dice_Bag(
			"sorcerer.metamagic",
			version="1",
			namespace="GenLegendSorcerer",
			)
	dice.shuffle(
			order
			)
	return tuple(
			order[
				:count
				]
			)


def Apply_Metamagic(
		char,
		count: int,
		) -> tuple[type[Metamagic], ...]:
	"""
	Carry the options this Character has learned, ``count`` in all.

	Must be called outside any other Tag's Imprint.  A top-up: options
	already carried are kept, and calling it twice changes nothing.
	"""
	for name in Resolve_Metamagic(
			char,
			count,
			):
		option = METAMAGIC[
				name
				]
		if char not in option:
			option(
					char
					)
	return Find_Metamagic(
			char
			)


def Find_Metamagic(
		char,
		) -> tuple[type[Metamagic], ...]:
	"""The options this Character carries, in the catalogue's order."""
	return tuple(
			option
			for option in METAMAGIC.values()
			if char in option
			)


def Describe_Metamagic(
		option: type[Metamagic],
		char,
		) -> str:
	"""One option as the sheet prints it: name, cost, then its rule."""
	rule = option.RULE
	text = (
		rule(
				char
				)
		if callable(
				rule
				)
		else rule
		)
	points = (
		"1 Sorcery Point"
		if option.COST == 1
		else f"{option.COST} Sorcery Points"
		)
	return f"<b>{option.NAME}</b> ({points}). {text}"


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _self_test() -> None:
	assert len(
			METAMAGIC
			) == 10
	assert {
			name
			for name, option in METAMAGIC.items()
			if option.COST == 2
			} == {
			"Heightened Spell",
			"Quickened Spell",
			}
	assert {
			name
			for name, option in METAMAGIC.items()
			if option.STACKS
			} == {
			"Empowered Spell",
			"Seeking Spell",
			}
	for option in METAMAGIC.values():
		assert issubclass(
				option,
				Metamagic,
				)
		assert "—" not in Describe_Metamagic(
				option,
				Character(
						seed=1
						),
				), option.NAME

	stranger = Character(
			seed=7
			)
	stranger.level = 5
	stranger.char_class = "Fighter"
	try:
		Quickened_Spell(
				stranger
				)
	except Exception:
		pass
	assert stranger not in Quickened_Spell, (
		"A Fighter must not be able to carry Metamagic."
		)
	print(
			"OK — MetamagicKit self-test"
			)


if __name__ == "__main__":
	from AtlasLusoris.MetamagicKit import _self_test as _package_self_test
	_package_self_test()
