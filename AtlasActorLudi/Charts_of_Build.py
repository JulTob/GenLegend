"""
Charts_of_Build — the walk that reads a Character's build from its Tags.

Thought pattern (read this before the code)
	1. Decree 0009: a Character's features are its Tags. Each Tag declares
	   what it gives the sheet as plain class data in its own module:

	       ENTRIES = ( Entry( title, rules, flavor, section=…, level=… ), … )
	       CHIPS   = ( Chip( symbol, label, value ), … )

	   (``AtlasVenustas.Entry`` and ``AtlasVenustas.Chip``, QST-0142.)
	   Nothing about the sheet is stored on the Character.
	2. The **build** is what those declarations say, read now. To find it:

	       for each leaf Tag the Character carries   (TopKit ``Tags``, in
	                                                   application order)
	           for each Tag in the leaf's Form        (TopKit ``Form``,
	                                                   Base first)
	               read what THAT Tag itself declared (its own ``__dict__``,
	                                                   never inherited)

	   A Base shared by two leaves is read once, the first time it is met.
	3. Reading resolves every reader (a function of the Character) through
	   the declaration's own ``Read``, so every number is current. An Entry
	   with no level takes its Tag's ``MIN_LEVEL`` when the Tag has one.
	4. Reading is pure (Decree 0009, point 7). The walk decides nothing,
	   rolls nothing and writes nothing.
	5. Errors are named. A declaration that cannot be read raises
	   ``Build_Read_Error`` naming the Tag and the title or label, never a
	   bare exception from deep inside a reader.
	6. The walk does not order the sheet. Sections and their order belong to
	   the layout that prints the build.

Public surface
	Find_Build(char)   — the Character's build, read now
	Build              — what the walk returns
	Built_Entry        — one read Entry, with the Tag that declared it
	Built_Chip         — one read Chip, with the Tag that declared it
	Build_Read_Error   — a declaration could not be read
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace

from TopKit import Form
from TopKit import Tags

from AtlasVenustas import Chip
from AtlasVenustas import Entry


# ---------------------------------------------------------------------------
# What the walk returns
# ---------------------------------------------------------------------------

@dataclass( frozen=True )
class Built_Entry:
	"""One Entry as read now, and the Tag that declared it."""
	tag: type
	entry: Entry


@dataclass( frozen=True )
class Built_Chip:
	"""One Chip as read now, and the Tag that declared it."""
	tag: type
	chip: Chip


@dataclass( frozen=True )
class Build:
	"""Everything the Character's Tags declare, read at one moment."""
	entries: tuple[Built_Entry, ...]
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

def Own_Declarations(
		tag: type,
		name: str,
		) -> tuple:
	"""What this Tag declared itself under ``name``; never its Base's."""
	return tuple(
			vars( tag ).get(
					name,
					(),
					)
			)


def Own_Entries(
		tag: type,
		) -> tuple:
	return Own_Declarations(
			tag,
			"ENTRIES",
			)


def Own_Chips(
		tag: type,
		) -> tuple:
	return Own_Declarations(
			tag,
			"CHIPS",
			)


# ---------------------------------------------------------------------------
# Step 3: read one declaration against the Character, now
# ---------------------------------------------------------------------------

def Require_Kind(
		tag: type,
		declared,
		kind: type,
		holder: str,
		) -> None:
	"""Refuse anything but the one shape, naming where it was found."""
	if not isinstance(
			declared,
			kind,
			):
		raise Build_Read_Error(
				f"{tag.__name__}.{holder} holds {declared!r}; "
				f"only AtlasVenustas.{kind.__name__} belongs there."
				)


def Tag_Level(
		tag: type,
		) -> int | None:
	"""The level a Tag is gained at, when it says so (``MIN_LEVEL``)."""
	level = getattr(
			tag,
			"MIN_LEVEL",
			None,
			)
	if isinstance(
			level,
			int,
			):
		return level
	return None


def Read_Entry(
		tag: type,
		declared: Entry,
		char,
		) -> Built_Entry:
	"""One declared Entry, with its readers resolved now."""
	Require_Kind(
			tag,
			declared,
			Entry,
			"ENTRIES",
			)
	try:
		read = declared.Read(
				char
				)
	except Exception as error:
		raise Build_Read_Error(
				f"{tag.__name__}: Entry {declared.title!r} could not be read: "
				f"{type( error ).__name__}: {error}"
				) from error
	if read.level is None:
		read = replace(
				read,
				level=Tag_Level( tag ),
				)
	return Built_Entry(
			tag=tag,
			entry=read,
			)


def Read_Chip(
		tag: type,
		declared: Chip,
		char,
		) -> Built_Chip:
	"""One declared Chip, with its value read now."""
	Require_Kind(
			tag,
			declared,
			Chip,
			"CHIPS",
			)
	try:
		read = declared.Read(
				char
				)
	except Exception as error:
		raise Build_Read_Error(
				f"{tag.__name__}: Chip {declared.label!r} could not be read: "
				f"{type( error ).__name__}: {error}"
				) from error
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
	"""The Character's build: every Entry and Chip its Tags declare, read now."""
	entries = []
	chips = []
	for tag in Declaring_Tags( char ):
		for declared in Own_Entries( tag ):
			entries.append(
					Read_Entry(
							tag,
							declared,
							char,
							)
					)
		for declared in Own_Chips( tag ):
			chips.append(
					Read_Chip(
							tag,
							declared,
							char,
							)
					)
	return Build(
			entries=tuple( entries ),
			chips=tuple( chips ),
			)


__all__ = (
		"Build",
		"Build_Read_Error",
		"Built_Chip",
		"Built_Entry",
		"Declaring_Tags",
		"Find_Build",
		"Own_Chips",
		"Own_Entries",
		"Read_Chip",
		"Read_Entry",
		)


# ---------------------------------------------------------------------------
# Self-test:  python -m AtlasActorLudi.Charts_of_Build
# ---------------------------------------------------------------------------

def _self_test() -> None:
	from TopKit import Tag

	from AtlasVenustas import Section

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

	def Lessons_Text(
			char,
			) -> str:
		return f"You have learned **{char.level}** lessons."

	class Lesson( Tag ):
		MIN_LEVEL = 3
		ENTRIES = (
				Entry(
						"Lessons",
						Lessons_Text,
						"*Every scar a teacher.*",
						section=Section.GUILD,
						),
				)

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

	#-- Entries: readers resolved, level taken from the Tag, printable.
	student = Dummy()
	Lesson( student )
	built = Find_Build( student ).entries
	assert len( built ) == 1
	lesson = built[0].entry
	assert lesson.rules == "You have learned **5** lessons.", lesson.rules
	assert lesson.level == 3
	assert lesson.section is Section.GUILD
	assert f"{lesson:md}".startswith( "**Lessons.**" ), f"{lesson:md}"

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
