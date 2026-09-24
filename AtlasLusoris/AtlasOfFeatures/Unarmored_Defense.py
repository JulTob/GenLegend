"""
Unarmored Defense — one Tag for every "no armour, better Armor Class" feature.

Thought pattern (read this before the code)
	1. Three Guild features share one rule. With no armour on, the base
	   Armor Class is 10 + Dexterity modifier + one more ability modifier.
	   Only two things change from source to source:

	       Source                     Ability   Shield allowed?
	       Barbarian                  CON       yes
	       Monk                       WIS       no
	       Bard, College of Dance     CHA       no

	2. So there is ONE Tag, and the source gives those two facts as inputs:

	       Unarmored_Defense( char, ability="CON", shield_allowed=True )

	   The Tag keeps them as two Records on the Character. Every reader
	   below (the gear rules, the Armor Class, the sheet's Chip) asks the
	   Tag; nobody computes the formula a second time.
	3. A Character has Unarmored Defense once. TopKit does nothing when an
	   active Tag is applied again, so the first source wins and a second
	   one changes nothing. That is the 2024 rule for a Character who gets
	   the feature from two Guilds.
	4. Reading is pure (Decree 0009, point 7). The readers decide nothing
	   and roll nothing.
	5. Does the Character have it?  Ask TopKit: ``char in Unarmored_Defense``.
	   No helper wraps that question.

Gear policy (Julio, 2026-09-24): the generator hands out NO armour
	The rules let a Character with Unarmored Defense put armour on; the
	feature just stops working while it is worn. The generator does not
	offer it anyway. A Monk or a Barbarian in plate breaks the fantasy the
	feature is there to sell, and a player who wants armour can still buy
	some during play. So, when the generator outfits a Character:

	    armour     never, whatever the Guild's armour training says;
	    a Shield   only when the source allows one (``shield_allowed``):
	               yes for a Barbarian, no for a Monk or a dancer.

	The gear rules that apply this live in
	``AtlasInventarium/Map_of_Gear_Proficiency.py``
	(``unarmoured_refuses_armour``, ``unarmoured_refuses_shield``).

Public surface
	Unarmored_Defense(char, ability=…, shield_allowed=…)  — the Tag
	Unarmored_Ability(char)              — the extra ability, or None
	Shield_Voids_Unarmored_Defense(char) — would a Shield turn it off?
	Unarmored_Armour_Class(char)         — the Armor Class with nothing on
"""

from __future__ import annotations

from TopKit import Imprint
from TopKit import Pre
from TopKit import Record
from TopKit import Tag

from AtlasVenustas import Chip


ABILITIES = (
		"STR",
		"DEX",
		"CON",
		"INT",
		"WIS",
		"CHA",
		)


LEGACY_SKILL_FOR_ABILITY = {
		"CON": "Unarmed_Barb",
		"WIS": "Unarmed_Monk",
		"CHA": "Unarmed_Dance",
		}
	#-- A bridge, not a rule.  The legacy skills table still lists
	#-- "Unarmed Defense" among the armour proficiencies, and it has one
	#-- slot per source.  The Tag marks the matching slot so the sheet's
	#-- proficiency line does not change.  No rule reads these slots any
	#-- more.  The bridge goes when the proficiency list is read from the
	#-- Tags (QST-0093.12, question 4).


# ---------------------------------------------------------------------------
# Small readers of the Character (one step each)
# ---------------------------------------------------------------------------

def _score(
		char,
		ability: str,
		) -> int:
	"""The Character's score in one ability, or 10 when it has none yet."""
	scores = getattr(
			char,
			"AS",
			None,
			)
	if scores is None:
		return 10
	return int(
			getattr(
					scores,
					ability,
					10,
					)
			)


def _modifier(
		score: int,
		) -> int:
	return ( score - 10 ) // 2


def _mark_legacy_skill(
		char,
		ability: str,
		) -> None:
	"""Mark the legacy skills-table slot for this ability, when it has one."""
	slot_name = LEGACY_SKILL_FOR_ABILITY.get(
			ability
			)
	if slot_name is None:
		return
	skills = getattr(
			char,
			"skills",
			None,
			)
	slot = getattr(
			skills,
			slot_name,
			None,
			)
	mark = getattr(
			slot,
			"set_proficiency",
			None,
			)
	if mark is None:
		return
	mark()


# ---------------------------------------------------------------------------
# The Tag
# ---------------------------------------------------------------------------

class Unarmored_Defense( Tag ):
	"""With no armour on, AC is 10 + Dexterity + one more ability."""

	NAME = "Unarmored Defense"

	@Pre
	def Knows_The_Ability(
			target,
			ability,
			):
		return ability in ABILITIES

	@Pre
	def Says_Whether_A_Shield_Is_Allowed(
			target,
			shield_allowed,
			):
		return isinstance(
				shield_allowed,
				bool,
				)

	@Record
	def unarmored_defense_ability(
			target,
			*,
			ability,
			) -> str:
		return ability

	@Record
	def unarmored_defense_allows_shield(
			target,
			*,
			shield_allowed,
			) -> bool:
		return shield_allowed

	@Imprint
	def Mark_The_Legacy_Skills_Table(
			target,
			ability,
			):
		_mark_legacy_skill(
				target,
				ability,
				)


# ---------------------------------------------------------------------------
# Readers: everything the rest of the generator needs to know
# ---------------------------------------------------------------------------

def Unarmored_Ability(
		char,
		) -> str | None:
	"""The ability added to Dexterity, or None without the feature."""
	if char not in Unarmored_Defense:
		return None
	return char.unarmored_defense_ability


def Shield_Voids_Unarmored_Defense(
		char,
		) -> bool:
	"""True when the Character has the feature and a Shield turns it off."""
	if char not in Unarmored_Defense:
		return False
	return not char.unarmored_defense_allows_shield


def Unarmored_Armour_Class(
		char,
		) -> int:
	"""
	The Armor Class with nothing on.

	Everyone has 10 + Dexterity. With the feature, the Character may use
	10 + Dexterity + the Tag's ability instead, and takes the better of the
	two: a low score never makes the feature a penalty.
	"""
	dexterity = _modifier(
			_score(
					char,
					"DEX",
					)
			)
	plain = 10 + dexterity

	ability = Unarmored_Ability( char )
	if ability is None:
		return plain

	bonus = _modifier(
			_score(
					char,
					ability,
					)
			)
	return max(
			plain,
			plain + bonus,
			)


# ---------------------------------------------------------------------------
# What the Tag gives the sheet (Decree 0009, point 1): a Chip, no prose.
# The prose stays with each source, because each source words it its own way.
# ---------------------------------------------------------------------------

Unarmored_Defense.CHIPS = (
		Chip(
				"🛡️",
				"Unarmored AC",
				Unarmored_Armour_Class,
				),
		)
	#-- Set after the class, because the Chip's value is a reader defined
	#-- below the Tag.  It is plain class data all the same.
	#-- The shape is ``AtlasVenustas.Chip( symbol, label, value )``, the one
	#-- QST-0141 recommends; the value is resolved when the build is read.


__all__ = (
		"Shield_Voids_Unarmored_Defense",
		"Unarmored_Ability",
		"Unarmored_Armour_Class",
		"Unarmored_Defense",
		)


# ---------------------------------------------------------------------------
# Self-test:  python -m AtlasLusoris.AtlasOfFeatures.Unarmored_Defense
# ---------------------------------------------------------------------------

def _self_test() -> None:
	from TopKit import TagPreconditionError

	class Scores:
		DEX = 14
		CON = 16
		WIS = 8
		CHA = 16

	class Dummy:
		def __init__(
				self,
				):
			self.AS = Scores()

	#-- Nobody: plain 10 + Dexterity.
	plain = Dummy()
	assert plain not in Unarmored_Defense
	assert Unarmored_Armour_Class( plain ) == 12
	assert Shield_Voids_Unarmored_Defense( plain ) is False

	#-- Barbarian: Constitution, and a Shield is fine.
	barbarian = Dummy()
	Unarmored_Defense(
			barbarian,
			ability="CON",
			shield_allowed=True,
			)
	assert barbarian in Unarmored_Defense
	assert Unarmored_Ability( barbarian ) == "CON"
	assert Unarmored_Armour_Class( barbarian ) == 15
	assert Shield_Voids_Unarmored_Defense( barbarian ) is False

	#-- Dancer: Charisma, and a Shield turns it off.
	dancer = Dummy()
	Unarmored_Defense(
			dancer,
			ability="CHA",
			shield_allowed=False,
			)
	assert Unarmored_Armour_Class( dancer ) == 15
	assert Shield_Voids_Unarmored_Defense( dancer ) is True

	#-- Monk with a low Wisdom: the feature is never a penalty.
	monk = Dummy()
	Unarmored_Defense(
			monk,
			ability="WIS",
			shield_allowed=False,
			)
	assert Unarmored_Armour_Class( monk ) == 12

	#-- Once per Character: a second source changes nothing.
	Unarmored_Defense(
			barbarian,
			ability="WIS",
			shield_allowed=False,
			)
	assert Unarmored_Ability( barbarian ) == "CON"
	assert Shield_Voids_Unarmored_Defense( barbarian ) is False

	#-- A wrong ability, or a missing input, is refused at the door.
	for inputs in (
			{ "ability": "LUCK", "shield_allowed": True },
			{ "ability": "CON" },
			{ "shield_allowed": True },
			):
		stranger = Dummy()
		try:
			Unarmored_Defense(
					stranger,
					**inputs,
					)
		except TagPreconditionError:
			pass
		else:
			raise AssertionError(
					f"Unarmored_Defense accepted {inputs}"
					)
		assert stranger not in Unarmored_Defense

	#-- The Chip reads the same function the gear rules read.
	chip = Unarmored_Defense.CHIPS[0]
	assert chip.value( dancer ) == Unarmored_Armour_Class( dancer )

	print( "Unarmored_Defense: all checks passed." )


if __name__ == "__main__":
	_self_test()
