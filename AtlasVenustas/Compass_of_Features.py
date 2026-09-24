"""
Compass_of_Features — the two things a sheet shows: Entries and Chips.

Thought pattern (read this before the code)
	1. A sheet has two columns (Julio, 2026-09-24).
	       The big column holds ENTRIES: a title, a flavor line, the rules.
	       The small column holds CHIPS:  a symbol, a label, a value.
	   Nothing else is printed. Where an Entry sits (its section) and when it
	   was gained (its level) are metadata: they order the sheet, they are
	   never printed as text.
	2. Text is Markdown, never HTML. Markdown is what a person writes most
	   easily, and every medium can be printed from it: HTML for the web
	   sheet, Markdown for tests, JSON for the API.
	3. A text or a value may be a READER: a function of the Character that
	   returns it, so a number is always current ("your AC is **15**").
	   ``Read( character )`` resolves every reader and returns a new Entry or
	   Chip holding plain text only. Reading is pure (Decree 0009, point 7).
	4. Printing is formatting. ``f"{entry:html}"``, ``f"{entry:md}"``,
	   ``f"{entry:json}"``; the same for a Chip. The printers live in
	   ``Charts_of_Printing``; this module only declares the shapes. Only a
	   read Entry or Chip can be printed: printing one that still holds a
	   reader raises ``Unread_Text``, naming it.
	5. Both are frozen dataclasses: declared once, as plain class data on a
	   Tag (``ENTRIES = ( Entry( … ), )``), never changed afterwards.

Public surface
	Section                 — the sheet's sections, in the approved order
	Entry(title, rules, flavor, *, section, level)
	Chip(symbol, label, value, *, kind)
	Unread_Text             — a reader was printed before it was read
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace
from enum import Enum
from typing import Any
from typing import Callable
from typing import Union


Reader = Callable[
		[ Any ],
		Any,
		]
Text = Union[
		str,
		Reader,
		]
	#-- A plain Markdown string, or a function of the Character returning one.


class Section( Enum ):
	"""Where an Entry sits on the sheet. The order is the printed order."""

	SPECIES = "Species"
	BACKGROUND = "Background"
	GUILD = "Guild"
	FEATS = "Feats"
	PROFICIENCIES = "Proficiencies"
	EQUIPMENT = "Equipment"
	BACKSTORY = "Backstory"
	MAGIC = "Magic"
	OTHERS = "Others"
		#-- Approved by Julio, 2026-09-24 (Dialog 0026 R3, QST-0093.14).


SECTION_ORDER = tuple(
		Section
		)


class Unread_Text( Exception ):
	"""A reader was printed before ``Read( character )`` resolved it."""


# ---------------------------------------------------------------------------
# One step each: is it a reader, and read it
# ---------------------------------------------------------------------------

def Is_Reader(
		text,
		) -> bool:
	return callable( text )


def Read_Text(
		text,
		character,
		):
	"""A plain value as it is; a reader, called with the Character."""
	if Is_Reader( text ):
		return text( character )
	return text


# ---------------------------------------------------------------------------
# The Entry
# ---------------------------------------------------------------------------

@dataclass( frozen=True )
class Entry:
	"""A feature in the big column: title, flavor, rules."""

	title: str
	rules: Text = ""
		#-- What it does.  Markdown, or a reader.
	flavor: Text = ""
		#-- The fantasy line, printed in italics.  Markdown, or a reader.
	section: Section = Section.OTHERS
		#-- Metadata: where it sits.  Never printed as text.
	level: int | None = None
		#-- Metadata: the level it was gained at; orders a section.

	def Is_Read(
			self,
			) -> bool:
		return not (
				Is_Reader( self.rules )
				or Is_Reader( self.flavor )
				)

	def Read(
			self,
			character,
			) -> "Entry":
		"""The same Entry, with every reader resolved against the Character."""
		return replace(
				self,
				rules=str(
						Read_Text(
								self.rules,
								character,
								)
						),
				flavor=str(
						Read_Text(
								self.flavor,
								character,
								)
						),
				)

	def __format__(
			self,
			spec: str,
			) -> str:
		from AtlasVenustas.Charts_of_Printing import Print_Entry
		return Print_Entry(
				self,
				spec,
				)

	def __str__(
			self,
			) -> str:
		return format(
				self,
				"html",
				)


# ---------------------------------------------------------------------------
# The Chip
# ---------------------------------------------------------------------------

@dataclass( frozen=True )
class Chip:
	"""A value in the small column: symbol, label, value."""

	symbol: str
	label: str
	value: Any = ""
		#-- A plain value, or a reader.
	kind: str = ""
		#-- Metadata: a family of Chips the sheet styles alike ("magic").
		#-- Never printed as text.

	def Is_Read(
			self,
			) -> bool:
		return not Is_Reader( self.value )

	def Read(
			self,
			character,
			) -> "Chip":
		"""The same Chip, with its value read against the Character."""
		return replace(
				self,
				value=Read_Text(
						self.value,
						character,
						),
				)

	def __format__(
			self,
			spec: str,
			) -> str:
		from AtlasVenustas.Charts_of_Printing import Print_Chip
		return Print_Chip(
				self,
				spec,
				)

	def __str__(
			self,
			) -> str:
		return format(
				self,
				"html",
				)


__all__ = (
		"Chip",
		"Entry",
		"Is_Reader",
		"Read_Text",
		"SECTION_ORDER",
		"Section",
		"Text",
		"Unread_Text",
		)
