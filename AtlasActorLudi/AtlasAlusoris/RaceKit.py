"""
RaceKit

NonPlayer boundary from legacy Race choices into shared Species and canonical
Creature Type Tags.

Race is a generator request, not a mixed TOP Geometry. A Dwarf request applies
the shared Dwarf Species Shape; an Aberration request applies the Aberration
Creature Type. The ``race`` string remains only as a compatibility projection
for the legacy Alusoris maps and Nomina providers.
"""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring,
#-- the Apply_Race docstring, both failure messages, the dice namespace and the
#-- two seeded self-tests are the original's, word for word, read out of the
#-- vaulted .pyc; the layout and the named steps follow today's Canon.
#--
#-- Does this module own a domain axis (QST-0134)?  No — and the docstring
#-- above already says why.  A Race is a *request*, and every Tag the request
#-- resolves to already lives in SpeciesKit: the Species Shapes, the Creature
#-- Types, Undead, Vampire.  Inventing a Race Tag here would be a second name
#-- for a Shape that exists, which is the mixed Geometry this file was written
#-- to prevent.  What this file owns is the translation, and Apply_Race is now
#-- five named steps so that each one can be read on its own line.

from AtlasActorLudi.AtlasAlusoris.Map_of_Races import (
		Creature_Type_For_Race,
		race_weights,
		)
from AtlasActorLudi.SpeciesKit import Apply_Creature_Type
from AtlasActorLudi.SpeciesKit import Apply_Species
from AtlasActorLudi.SpeciesKit import Resolve_Creature_Type
from AtlasActorLudi.SpeciesKit import Resolve_Species
from AtlasActorLudi.SpeciesKit import Undead
from AtlasActorLudi.SpeciesKit import Vampire


RACE_CHOICES = tuple(
		race_weights
		)
	#-- Every Race a NonPlayer request may name, in the Map's own order.

ANY = "random"
	#-- What a request says when it expresses no preference.  Compared folded,
	#-- so "Random", "RANDOM" and "  random  " all mean the same thing.


def _random_race(
		character,
		) -> str:
	"""One Race drawn from the Map's weights, on the Character's own dice."""
	dice_bag = character.Dice_Bag(
			"identity.nonplayer.race",
			version="1",
			namespace="GenLegendActor",
			)

	return dice_bag.choices(
			RACE_CHOICES,
			weights=tuple(
					race_weights[
							race
							]
					for race in RACE_CHOICES
					),
			k=1,
			)[
			0
			]


def _species_for(race):
	"""The shared Species Shape this Race names, or nothing if it names none."""
	try:
		return Resolve_Species(race)
	except ValueError:
		return None


def Expresses_No_Preference(race) -> bool:
	"""Whether this request leaves the Race to the dice."""
	#-- A request that is neither None nor text is malformed, not open.  It is
	#-- carried forward unchanged so that the Map refuses it by name, which
	#-- tells the caller what was wrong; rolling dice for it would hide a bug.
	if race is None:
		return True

	if not isinstance(
			race,
			str,
			):
		return False

	return race.strip().casefold() == ANY


def Requested_Race(
		character,
		race,
		) -> str:
	"""The Race this request names: the one asked for, or one drawn for it."""
	if Expresses_No_Preference(race):
		return _random_race(character)

	return str(race).strip()


def Agreed_Creature_Type(
		race: str,
		creature_type,
		):
	"""The Creature Type to apply, refusing a request that contradicts the Race."""
	#-- A Race carries its Creature Type in the Map.  A caller may name one too,
	#-- but only the same one: a Dwarf who is asked to be Undead is a mistake in
	#-- the request, not a Character to build.
	expected_type = Resolve_Creature_Type(
			Creature_Type_For_Race(
					race
					)
			)

	if creature_type is None:
		return expected_type

	selected_type = Resolve_Creature_Type(
			creature_type,
			)

	if selected_type is not expected_type:
		raise ValueError(
				f"{race!r} requires Creature Type "
				f"{expected_type.__name__!r}, not "
				f"{selected_type.__name__!r}."
				)

	return selected_type


def Guard_One_Race_Only(
		character,
		race: str,
		) -> None:
	"""Refuse a second, different Race request on a Character that has one."""
	current_race = getattr(
			character,
			"race",
			None,
			)

	if (
		current_race is not None
		and current_race != race
		):
		raise ValueError(
				"A Character cannot carry two NonPlayer Race requests: "
				f"{current_race!r} and {race!r}."
				)


def Apply_Identity(
		character,
		race: str,
		):
	"""Apply what this Race *is*, and answer with the Tag that says so."""
	#-- Three kinds of request, in the order they are recognised: a shared
	#-- Species Shape; the Vampire, who is a Creature Type and a Shape at once;
	#-- and a bare Creature Type such as Aberration, named directly.
	species = _species_for(race)

	if species is not None:
		return Apply_Species(
				character,
				species,
				)

	if race == "Vampire":
		Apply_Creature_Type(
				character,
				Undead,
				)

		if character not in Vampire:
			Vampire(character)

		return Vampire

	return Apply_Creature_Type(
			character,
			race,
			)


def Apply_Race(
		character,
		race=None,
		creature_type=None,
		):
	"""Resolve one NonPlayer Race request into shared semantic Tags."""
	selected_race = Requested_Race(
			character,
			race,
			)
	selected_type = Agreed_Creature_Type(
			selected_race,
			creature_type,
			)

	Guard_One_Race_Only(
			character,
			selected_race,
			)

	identity_tag = Apply_Identity(
			character,
			selected_race,
			)

	Apply_Creature_Type(
			character,
			selected_type,
			)

	#-- The projection the legacy Alusoris maps and the Nomina providers read.
	#-- It is a record of the request, not a Tag, and nothing derives from it.
	character.race = selected_race
	character.creature_type = selected_type.__name__

	return identity_tag


__all__ = (
		"Apply_Race",
		"RACE_CHOICES",
		)


def _test_species_race() -> None:
	"""A Dwarf request applies the shared Dwarf Shape and its Creature Type."""
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.SpeciesKit import Dwarf
	from AtlasActorLudi.SpeciesKit import Humanoid

	character = Character(
			seed=401,
			)
	tag = Apply_Race(
			character,
			"Dwarf",
			)

	assert tag is Dwarf, "A Species request answers with its Species Shape."
	assert character in Dwarf, "The Shape is worn, not merely named."
	assert character in Humanoid, "A Dwarf is a Humanoid by its Creature Type."
	assert character.race == "Dwarf", "The projection records the request."
	assert character.creature_type == "Humanoid", "So does the Creature Type."


def _test_monster_race() -> None:
	"""A Vampire request applies both the Undead Type and the Vampire Shape."""
	from AtlasActorLudi.CharactersKit import Character

	character = Character(
			seed=409,
			)
	tag = Apply_Race(
			character,
			"Vampire",
			)

	assert tag is Vampire, "A Vampire request answers with the Vampire Tag."
	assert character in Vampire, "The Vampire Shape is worn."
	assert character in Undead, "A Vampire is Undead by its Creature Type."
	assert character.race == "Vampire", "The projection records the request."
	assert character.creature_type == "Undead", "So does the Creature Type."


def _test_random_race() -> None:
	"""A request with no preference draws one Race, and draws it repeatably."""
	from AtlasActorLudi.CharactersKit import Character

	for asked in (None, "Random", "random", "  RANDOM  ", "RaNdOm"):
		first = Apply_Race(
				Character(seed=413),
				asked,
				)
		again = Apply_Race(
				Character(seed=413),
				asked,
				)
		assert first is again, \
				f"{asked!r} must draw the same Race from the same seed."

	drawn = Character(seed=413)
	Apply_Race(drawn)
	assert drawn.race in RACE_CHOICES, \
			"A drawn Race is one the Map offers."

	#-- A request that is not text is malformed, not open: it is refused by
	#-- name rather than quietly replaced with a roll.
	try:
		Apply_Race(
				Character(seed=413),
				17,
				)
	except ValueError as refusal:
		assert "17" in str(refusal), \
				f"A malformed request must name itself: {refusal}"
	else:
		raise AssertionError(
				"A Race request of 17 should have been refused."
				)


def _test_refusals() -> None:
	"""The two requests this boundary refuses, and why."""
	from AtlasActorLudi.CharactersKit import Character

	contradiction = Character(seed=421)
	try:
		Apply_Race(
				contradiction,
				"Dwarf",
				Undead,
				)
	except ValueError as refusal:
		assert "requires Creature Type" in str(refusal), \
				f"A contradicted Type must say so: {refusal}"
	else:
		raise AssertionError(
				"A Dwarf asked to be Undead should have been refused."
				)

	twice = Character(seed=421)
	Apply_Race(
			twice,
			"Dwarf",
			)
	try:
		Apply_Race(
				twice,
				"Elf",
				)
	except ValueError as refusal:
		assert "two NonPlayer Race requests" in str(refusal), \
				f"A second Race must say so: {refusal}"
	else:
		raise AssertionError(
				"A second, different Race should have been refused."
				)

	#-- The same Race twice is not a contradiction; it is the same request.
	Apply_Race(
			twice,
			"Dwarf",
			)


def _self_test() -> None:
	_test_species_race()
	_test_monster_race()
	_test_random_race()
	_test_refusals()
	print("OK — Alusoris RaceKit self-test")


if __name__ == "__main__":
	_self_test()
