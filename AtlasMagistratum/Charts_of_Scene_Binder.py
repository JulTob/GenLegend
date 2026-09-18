"""Bind a DM Character to Epica and shape Companion scene data.

Attach the framing Character to an Adventure, draw an inspiration card, and
return presentation-neutral scene records. The Shiny frontline renders them.

Philosophy: the DM Character is morally open — villain, Quest Master, contested
guardian, or any figure whose will frames the session. Cards pressure the table
around that will; they do not assume evil.
"""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring
#-- and the two public docstrings that had one are the original's, word for
#-- word, read out of the vaulted .pyc; the layout, the named steps and the
#-- two missing docstrings follow today's Canon.
#--
#-- Does this module own a domain axis (QST-0134)?  No.  Every Tag it would
#-- want already exists: Area and Lair are Adventure Tags in AtlasEpica, and
#-- the Character is a Character.  What is missing between them is not a
#-- property but a translation, and a translation is ordinary Python.  This
#-- file is the seam between Epica's story syntax and the Companion's screen:
#-- it hands a Character to the Oracle, and it hands the Oracle's cards back
#-- as plain records the frontline can read without importing AtlasEpica.

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from AtlasActorLudi.CharactersKit import Character
from AtlasEpica.Grimoire_of_Adventure import Forge_Oracle
from AtlasEpica.Map_of_Scenes import frame_briefing, inspiration_card


DEFAULT_LEVEL = 5
	#-- The tier a session frames at when neither caller nor Character says.

DEFAULT_SEED = 0
	#-- The draw a Character without a seed of its own is framed from.


def Framing_Level(
		dm_character: Character,
		level: int | None,
		) -> int:
	"""The tier to frame at: the caller's word, the Character's, or the default."""
	if level is not None:
		return int(level)

	own = getattr(
			dm_character,
			"level",
			DEFAULT_LEVEL,
			)
	return int(
			own or DEFAULT_LEVEL
			)


def Framing_Seed(
		dm_character: Character,
		) -> int:
	"""The draw this session is framed from: the Character's seed."""
	return int(
			getattr(
					dm_character,
					"seed",
					DEFAULT_SEED,
					)
			)


def bind_dm_character(
		dm_character: Character,
		*,
		level: int | None = None,
		) -> Any:
	"""Collapse Area/Lair for this DM Character — returns the Adventure Target."""
	return Forge_Oracle(
			dm_character,
			seed=Framing_Seed(dm_character),
			level=Framing_Level(
					dm_character,
					level,
					),
			)


bind_bbeg = bind_dm_character
	#-- The name this rite carried before the DM Character stopped being assumed
	#-- evil (QST-0081.9).  Kept so an older caller still binds.


def briefing_for(
		adventure: Any,
		) -> str:
	"""The Game Master's frame for this Adventure: who, Area, Lair."""
	return frame_briefing(
			adventure,
			)


def draw_inspiration(
		adventure: Any,
		) -> SimpleNamespace:
	"""One inspiration card as a namespace the Companion UI can render."""
	return card_as_namespace(
			inspiration_card(
					adventure,
					)
			)


def Occupants_Of(
		card: dict[str, Any],
		) -> list[SimpleNamespace]:
	"""The figures standing in a scene, each as a record the screen can read."""
	return [
			SimpleNamespace(**occupant)
			for occupant in card.get(
					"occupants",
					[],
					)
			]


def card_as_namespace(
		card: dict[str, Any],
		) -> SimpleNamespace:
	"""One scene card turned from a dictionary into a record with named fields."""
	#-- The frontline reads attributes, not keys, and must not have to know
	#-- which keys Epica happens to fill.  Every field is named here, so a card
	#-- that arrives short still renders instead of raising.
	return SimpleNamespace(
			title=card.get("title", ""),
			prose=card.get("prose", ""),
			kind=card.get("kind", ""),
			occupants=Occupants_Of(card),
			area=card.get("area"),
			lair=card.get("lair"),
			hooks=card.get("hooks", []),
			)


__all__ = (
		"bind_bbeg",
		"bind_dm_character",
		"briefing_for",
		"card_as_namespace",
		"draw_inspiration",
		)


def _self_test() -> None:
	"""The shaping rites, proven without summoning an Adventure."""
	#-- What this cannot prove: that a card is worth reading.  That is the
	#-- Oracle's business, and Map_of_Scenes carries its own proof of it.  What
	#-- this file owns is the shape handed to the screen, so the shape is what
	#-- is checked.

	#-- The original's own proof, kept word for word (recovered from the .pyc).
	ns = card_as_namespace(
			{
					"title": "Test",
					"prose": "A line.",
					"kind": "beat",
					"occupants": [],
					"hooks": [],
					}
			)
	assert ns.title == "Test"

	#-- A card that arrives short still renders: every field is named.
	empty = card_as_namespace({})
	assert empty.title == "", "A missing title reads as no title."
	assert empty.prose == "", "A missing line reads as no line."
	assert empty.kind == "", "A missing kind reads as no kind."
	assert empty.occupants == [], "An empty scene has nobody in it."
	assert empty.area is None, "An unplaced card names no Area."
	assert empty.lair is None, "An unplaced card names no Lair."
	assert empty.hooks == [], "A card with no hooks offers none."

	#-- Occupants arrive as dictionaries and leave as records.
	peopled = card_as_namespace(
			{
					"occupants": [
							{ "name": "Hessa", "kind": "scene" },
							],
					}
			)
	assert peopled.occupants[0].name == "Hessa", "An occupant keeps its name."
	assert peopled.occupants[0].kind == "scene", "An occupant keeps its part."

	#-- The old name still binds to the same rite.
	assert bind_bbeg is bind_dm_character, \
			"The pre-rename name must not drift from the rite it aliases."

	#-- The tier a session frames at, from each of its three sources.
	told = SimpleNamespace(level=3, seed=11)
	assert Framing_Level(told, 9) == 9, "The caller's word wins."
	assert Framing_Level(told, None) == 3, "Then the Character's own tier."
	assert Framing_Level(SimpleNamespace(), None) == DEFAULT_LEVEL, \
			"A Character with no tier frames at the default."
	assert Framing_Level(SimpleNamespace(level=0), None) == DEFAULT_LEVEL, \
			"Level zero is no tier at all, not a tier of zero."

	#-- The draw a session is framed from.
	assert Framing_Seed(told) == 11, "A Character is framed from its own seed."
	assert Framing_Seed(SimpleNamespace()) == DEFAULT_SEED, \
			"A Character with no seed is framed from the default draw."

	print(
			"OK — Charts_of_Scene_Binder self-test (the shapes; the Oracle is Map_of_Scenes)"
			)


if __name__ == "__main__":
	_self_test()
