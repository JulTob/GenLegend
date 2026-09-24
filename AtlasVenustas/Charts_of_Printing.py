"""
Charts_of_Printing — one Entry or Chip, printed in one medium.

Thought pattern (read this before the code)
	1. The shapes live in ``Compass_of_Features``; this module only prints
	   them. Each medium is one small function with one job:

	       medium   call                  used by
	       html     f"{entry:html}"       the web sheet (also ``str( entry )``)
	       md       f"{entry:md}"         tests, snapshots, a printable sheet
	       json     f"{entry:json}"       the API
	       plain    f"{entry:plain}"      tooltips, logs

	2. Text is Markdown. HTML is made from it by ``markdown-it-py`` (the
	   library Shiny already installs), never by hand. While older text
	   still carries HTML tags, the HTML printer lets them through; the
	   QST-0142 stations remove them family by family.
	3. The HTML keeps the markup the sheet has always used for an Entry
	   (bold title, flavor block, italic rules), so moving to this printer
	   changes nothing a reader sees. The presentation is redesigned later,
	   in one place: here.
	4. Only read Entries and Chips print. One that still holds a reader
	   raises ``Unread_Text`` naming it, instead of printing a function's
	   name onto the sheet.
"""

from __future__ import annotations

import html as html_text
import json
import re

from markdown_it import MarkdownIt

from AtlasVenustas.Compass_of_Features import Chip
from AtlasVenustas.Compass_of_Features import Entry
from AtlasVenustas.Compass_of_Features import Unread_Text


MARKDOWN = MarkdownIt(
		"commonmark",
		{
				"html": True,
				"breaks": False,
				},
		)
	#-- "html": older text still carries tags; let them through until ported.
	#-- "breaks": off.  A single newline is a space, as Markdown and the
	#-- browser both read it; a new paragraph needs a blank line.


MEDIA = (
		"html",
		"md",
		"json",
		"plain",
		)


class Unknown_Medium( ValueError ):
	"""A format spec that is not one of the known media."""


# ---------------------------------------------------------------------------
# Small helpers, one step each
# ---------------------------------------------------------------------------

def Medium_Of(
		spec: str,
		) -> str:
	"""The medium a format spec names; the empty spec means html."""
	medium = ( spec or "html" ).strip().lower()
	if medium == "markdown":
		medium = "md"
	if medium not in MEDIA:
		raise Unknown_Medium(
				f"Unknown medium {spec!r}; use one of {', '.join( MEDIA )}."
				)
	return medium


def Inline_Html(
		markdown: str,
		) -> str:
	"""Markdown for one line of a sheet, as HTML without a paragraph around it."""
	return MARKDOWN.renderInline(
			markdown
			)


def Plain_Text(
		markdown: str,
		) -> str:
	"""Markdown (and any leftover tags) with the markup taken out."""
	without_tags = re.sub(
			r"<[^>]+>",
			"",
			Inline_Html(
					markdown
					),
			)
	return html_text.unescape(
			without_tags
			)


def Require_Read(
		thing,
		what: str,
		) -> None:
	if not thing.Is_Read():
		raise Unread_Text(
				f"{what} still holds a reader; call .Read( character ) first."
				)


# ---------------------------------------------------------------------------
# Entries
# ---------------------------------------------------------------------------

def Entry_As_Html(
		entry: Entry,
		) -> str:
	head = entry.title
	if not head:
		return ""
	if not entry.rules and not entry.flavor:
		return f"<b>{head}</b>"
	rules = Inline_Html(
			entry.rules
			)
	if not entry.flavor:
		return f"<b>{head}:</b> <i>{rules}</i>"
	flavor = Inline_Html(
			entry.flavor
			)
	return (
			f"<b>{head}:</b>\n"
			f'<div class="bc4">{flavor}</div>'
			f"<i>{rules}</i>"
			)


def Entry_As_Markdown(
		entry: Entry,
		) -> str:
	lines = [
			f"### {entry.title}",
			]
		#-- Level three: the sheet's name is ``#`` and its sections ``##``,
		#-- so an Entry sits one step under its section (Julio, 2026-09-24).
	if entry.flavor:
		lines.append(
				f"*{entry.flavor}*"
				)
	if entry.rules:
		lines.append(
				entry.rules
				)
	return "\n\n".join(
			lines
			)


def Entry_As_Json(
		entry: Entry,
		) -> str:
	return json.dumps(
			{
					"title": entry.title,
					"flavor": entry.flavor,
					"rules": entry.rules,
					"section": entry.section.value,
					"level": entry.level,
					},
			ensure_ascii=False,
			)


def Entry_As_Plain(
		entry: Entry,
		) -> str:
	parts = [
			f"{entry.title}.",
			]
	if entry.flavor:
		parts.append(
				Plain_Text(
						entry.flavor
						)
				)
	if entry.rules:
		parts.append(
				Plain_Text(
						entry.rules
						)
				)
	return " ".join(
			parts
			)


ENTRY_PRINTERS = {
		"html": Entry_As_Html,
		"md": Entry_As_Markdown,
		"json": Entry_As_Json,
		"plain": Entry_As_Plain,
		}


def Print_Entry(
		entry: Entry,
		spec: str,
		) -> str:
	Require_Read(
			entry,
			f"Entry {entry.title!r}",
			)
	printer = ENTRY_PRINTERS[
			Medium_Of( spec )
			]
	return printer(
			entry
			)


# ---------------------------------------------------------------------------
# Chips
# ---------------------------------------------------------------------------

def Chip_As_Html(
		chip: Chip,
		) -> str:
	style = "npc-box stat-chip"
	if chip.kind:
		style = f"{style} {chip.kind}-chip"
	return (
			f'<div class="{style}">'
			f'<div class="symbol">{chip.symbol}</div>'
			f'<div class="record">{chip.label}</div>'
			f'<div class="value">{chip.value}</div>'
			"</div>"
			)


def Chip_As_Markdown(
		chip: Chip,
		) -> str:
	head = f"{chip.symbol} " if chip.symbol else ""
	return f"{head}**{chip.label}:** {chip.value}"


def Chip_As_Json(
		chip: Chip,
		) -> str:
	return json.dumps(
			{
					"symbol": chip.symbol,
					"label": chip.label,
					"value": chip.value,
					},
			ensure_ascii=False,
			default=str,
			)


def Chip_As_Plain(
		chip: Chip,
		) -> str:
	return f"{chip.label}: {chip.value}"


CHIP_PRINTERS = {
		"html": Chip_As_Html,
		"md": Chip_As_Markdown,
		"json": Chip_As_Json,
		"plain": Chip_As_Plain,
		}


def Print_Chip(
		chip: Chip,
		spec: str,
		) -> str:
	Require_Read(
			chip,
			f"Chip {chip.label!r}",
			)
	printer = CHIP_PRINTERS[
			Medium_Of( spec )
			]
	return printer(
			chip
			)


__all__ = (
		"Chip_As_Html",
		"Chip_As_Json",
		"Chip_As_Markdown",
		"Chip_As_Plain",
		"Entry_As_Html",
		"Entry_As_Json",
		"Entry_As_Markdown",
		"Entry_As_Plain",
		"MEDIA",
		"Print_Chip",
		"Print_Entry",
		"Unknown_Medium",
		)


# ---------------------------------------------------------------------------
# Self-test:  python -m AtlasVenustas.Charts_of_Printing
# ---------------------------------------------------------------------------

def _self_test() -> None:
	from AtlasVenustas.Compass_of_Features import Section
	from AtlasVenustas.Charts_of_Printing import Unknown_Medium
		#-- By package path: run as ``python -m``, this file is also
		#-- ``__main__``, and the printers raise the package's class.

	keen = Entry(
			"Keen Smell",
			"Advantage on **Perception** checks that rely on smell.",
			"Nose to the wind.",
			section=Section.SPECIES,
			level=1,
			)

	#-- One Entry, four media.
	assert f"{keen:html}" == (
			"<b>Keen Smell:</b>\n"
			'<div class="bc4">Nose to the wind.</div>'
			"<i>Advantage on <strong>Perception</strong> checks that rely on smell.</i>"
			), f"{keen:html}"
	assert f"{keen:md}" == (
			"### Keen Smell\n\n"
			"*Nose to the wind.*\n\n"
			"Advantage on **Perception** checks that rely on smell."
			), f"{keen:md}"
	assert json.loads( f"{keen:json}" ) == {
			"title": "Keen Smell",
			"flavor": "Nose to the wind.",
			"rules": "Advantage on **Perception** checks that rely on smell.",
			"section": "Species",
			"level": 1,
			}
	assert f"{keen:plain}" == (
			"Keen Smell. Nose to the wind. "
			"Advantage on Perception checks that rely on smell."
			), f"{keen:plain}"
	assert str( keen ) == f"{keen:html}" == f"{keen}"

	#-- A title alone, and a title with rules only.
	assert f"{Entry( 'Shield' ):html}" == "<b>Shield</b>"
	assert f"{Entry( 'Shield', '+2 AC' ):html}" == "<b>Shield:</b> <i>+2 AC</i>"

	#-- One Chip, four media, and its style family.
	ac = Chip(
			"🛡️",
			"Armor Class",
			16,
			)
	assert f"{ac:md}" == "🛡️ **Armor Class:** 16"
	assert f"{ac:plain}" == "Armor Class: 16"
	assert json.loads( f"{ac:json}" ) == {
			"symbol": "🛡️",
			"label": "Armor Class",
			"value": 16,
			}
	assert 'class="npc-box stat-chip"' in f"{ac:html}"
	magic = Chip(
			"✨",
			"Spell DC",
			13,
			kind="magic",
			)
	assert 'class="npc-box stat-chip magic-chip"' in f"{magic:html}"

	#-- A reader must be read before it prints, and says so by name.
	live = Entry(
			"Rage",
			lambda character: f"You can rage **{character}** times.",
			)
	try:
		f"{live:md}"
	except Unread_Text as error:
		assert "Rage" in str( error )
	else:
		raise AssertionError( "an unread Entry printed" )
	assert f"{live.Read( 3 ):md}".endswith( "You can rage **3** times." )

	#-- An unknown medium is refused by name.
	try:
		f"{keen:pdf}"
	except Unknown_Medium as error:
		assert "pdf" in str( error )
	else:
		raise AssertionError( "an unknown medium printed" )

	print( "Charts_of_Printing: all checks passed." )


if __name__ == "__main__":
	_self_test()
