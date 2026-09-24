"""
Charts_of_Build — the walk that reads a Character's build from its Tags.

Thought pattern (read this before the code)
	1. Decree 0009: a Character's features are its Tags. Each Tag declares
	   what it gives the sheet as plain class data in its own module. Nothing
	   about the sheet is stored on the Character.
	2. The **build** is what those declarations say, read now. To find it:

	       for each leaf Tag the Character carries   (TopKit ``Tags``, in
	                                                   application order)
	           for each Tag in the leaf's Form        (TopKit ``Form``,
	                                                   Base first)
	               read what THAT Tag itself declared (its own ``__dict__``,
	                                                   never inherited)

	   A Base shared by two leaves is read once, the first time it is met.
	3. This first slice reads **Chips** only (``CHIPS``). A Chip is an
	   ``AtlasVenustas.Chip( symbol, label, value )``; a value that is a
	   function is called with the Character at read time, so the number is
	   always current. Entries (``ENTRIES``) join the walk once their shape
	   is settled (QST-0093.14, question 1).
	4. Reading is pure (Decree 0009, point 7). The walk decides nothing,
	   rolls nothing and writes nothing.
	5. Errors are named. A Chip that cannot be read raises
	   ``Build_Read_Error`` naming the Tag and the Chip, never a bare
	   exception from deep inside a value function.

Public surface
	Find_Build(char)   — the Character's build, read now
	Build              — what the walk returns
	Built_Chip         — one Chip, with the Tag that declared it
	Build_Read_Error   — a declaration could not be read
"""

from __future__ import annotations

from dataclasses import dataclass

from TopKit import Form
from TopKit import Tags

from AtlasVenustas import Chip


# ---------------------------------------------------------------------------
# What the walk returns
# ---------------------------------------------------------------------------

@dataclass( frozen=True )
class Built_Chip:
	"""One Chip as read now, and the Tag that declared it."""
	tag: type
	chip: Chip


@dataclass( frozen=True )
class Build:
	"""Everything the Character's Tags declare, read at one moment."""
	chips: tuple[Built_Chip, ...]


class Build_Read_Error( Exception ):
	"""A Tag's declaration could not be read for this Character."""


# ---------------------------------------------------------------------------
# Step 1: which Tags to read, in order, each once
# ---------------------------------------------------------------------------

def Declaring_Tags(
		char,
		) -> tuple[type, ...]:
	"""Every Tag in every carried leaf's Form, Base first, each once."""
	ordered = []
	seen = set()
	for leaf in Tags( char ):
		for tag in Form( leaf ):
			if tag in seen:
				continue
			seen.add( tag )
			ordered.append( tag )
	return tuple( ordered )


# ---------------------------------------------------------------------------
# Step 2: what one Tag itself declared
# ---------------------------------------------------------------------------

def Own_Chips(
		tag: type,
		) -> tuple:
	"""The Chips this Tag declared itself; a Shape never repeats its Base's."""
	return tuple(
			vars( tag ).get(
					"CHIPS",
					(),
					)
			)


# ---------------------------------------------------------------------------
# Step 3: read one declaration against the Character, now
# ---------------------------------------------------------------------------

def Read_Value(
		value,
		char,
		):
	"""A plain value as it is; a function, called with the Character."""
	if callable( value ):
		return value( char )
	return value


def Read_Chip(
		tag: type,
		declared: Chip,
		char,
		) -> Built_Chip:
	"""One declared Chip, with its value read now."""
	if not isinstance(
			declared,
			Chip,
			):
		raise Build_Read_Error(
				f"{tag.__name__}.CHIPS holds {declared!r}; "
				"a Chip is AtlasVenustas.Chip( symbol, label, value )."
				)
	try:
		value = Read_Value(
				declared.value,
				char,
				)
	except Exception as error:
		raise Build_Read_Error(
				f"{tag.__name__}: Chip {declared.label!r} could not be read: "
				f"{type( error ).__name__}: {error}"
				) from error
	read = Chip(
			declared.symbol,
			declared.label,
			value,
			extra_class=declared.extra_class,
			kind=declared.kind,
			)
	return Built_Chip(
			tag=tag,
			chip=read,
			)


# ---------------------------------------------------------------------------
# The walk
# ---------------------------------------------------------------------------

def Find_Build(
		char,
		) -> Build:
	"""The Character's build: every Chip its Tags declare, read now."""
	chips = []
	for tag in Declaring_Tags( char ):
		for declared in Own_Chips( tag ):
			chips.append(
					Read_Chip(
							tag,
							declared,
							char,
							)
					)
	return Build(
			chips=tuple( chips ),
			)


__all__ = (
		"Build",
		"Build_Read_Error",
		"Built_Chip",
		"Declaring_Tags",
		"Find_Build",
		"Own_Chips",
		"Read_Chip",
		"Read_Value",
		)


# ---------------------------------------------------------------------------
# Self-test:  python -m AtlasActorLudi.Charts_of_Build
# ---------------------------------------------------------------------------

def _self_test() -> None:
	from TopKit import Tag

	class Dummy:
		level = 5

	def Twice_The_Level(
			char,
			) -> int:
		return 2 * char.level

	class Family( Tag ):
		CHIPS = (
				Chip(
						"🏠",
						"Family",
						"Base",
						),
				)

	class Elder( Family ):
		CHIPS = (
				Chip(
						"🧓",
						"Elder",
						Twice_The_Level,
						),
				)

	class Younger( Family ):
		pass
			#-- Declares nothing: it must not repeat its Base's Chip.

	class Broken( Tag ):
		CHIPS = (
				Chip(
						"💥",
						"Broken",
						lambda char: char.missing,
						),
				)

	#-- Base first, each Tag once, only its own Chips, values read now.
	someone = Dummy()
	Elder( someone )
	Younger( someone )
	assert Declaring_Tags( someone ) == ( Family, Elder, Younger )
	labels = [
			built.chip.label
			for built in Find_Build( someone ).chips
			]
	assert labels == [ "Family", "Elder" ], labels
	assert Find_Build( someone ).chips[1].chip.value == 10

	#-- Nothing is stored: a new level is a new reading.
	someone.level = 7
	assert Find_Build( someone ).chips[1].chip.value == 14

	#-- A Chip that cannot be read names its Tag and its label.
	other = Dummy()
	Broken( other )
	try:
		Find_Build( other )
	except Build_Read_Error as error:
		assert "Broken" in str( error )
	else:
		raise AssertionError( "a broken Chip was read in silence" )

	#-- A real Character: the Unarmored Defense Tag's Chip agrees with the
	#-- number the gear rules use.
	import contextlib
	import io

	from AtlasActorLudi.Map_of_Character_Generation import summon_player
	from AtlasLusoris.AtlasOfFeatures.Unarmored_Defense import (
			Unarmored_Armour_Class,
			Unarmored_Defense,
			)

	quiet = io.StringIO()
	with contextlib.redirect_stdout( quiet ), contextlib.redirect_stderr( quiet ):
		barbarian = summon_player(
				seed=1,
				level=3,
				guild="Barbarian",
				)
	unarmored = [
			built.chip
			for built in Find_Build( barbarian ).chips
			if built.tag is Unarmored_Defense
			]
	assert len( unarmored ) == 1, unarmored
	assert unarmored[0].value == Unarmored_Armour_Class( barbarian )

	print( "Charts_of_Build: all checks passed." )


if __name__ == "__main__":
	_self_test()
