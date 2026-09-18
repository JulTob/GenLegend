"""Session path rites for the DM Companion — NPC import URLs and `dm/<level>/<seed>`."""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring
#-- and the three public docstrings are the original's, word for word, read out
#-- of the vaulted .pyc; the layout and the named steps follow today's Canon.
#--
#-- Does this module own a domain axis (QST-0134)?  No.  An address is not
#-- something a Character *is*, so nothing here becomes a Tag.  This file does
#-- one job: translate between an address a browser wrote and a request the
#-- generator understands.  The NPC half of that job already lives in
#-- Map_of_NonPlayer_Paths; only the Game Master's half is ours.

from __future__ import annotations

from typing import Any
from urllib.parse import unquote, urlparse

from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Paths import (
		parse_nonplayer_path,
		)


DM_MARK = "dm"
	#-- The word that opens a Game Master's address: `dm/<level>/<seed>`.

DM_SEGMENTS = 3
	#-- How many segments that address needs: the mark, the level, the seed.


def Segments(
		text: str,
		) -> list[str]:
	"""An address cut at its slashes, with the empty pieces dropped."""
	return [
			segment
			for segment in text.split("/")
			if segment
			]


def Bare_Path(
		raw: str | None,
		) -> str:
	"""The path part of an address, whether it came as URL, hash, or path."""
	text = (raw or "").strip()
	if text.startswith("http"):
		text = urlparse(text).path or ""
	return text.lstrip("#")


def Decoded_Segments(
		raw: str | None,
		) -> list[str]:
	"""An address reduced to its segments, with percent-escapes spelled out."""
	return [
			unquote(segment)
			for segment in Segments(
					Bare_Path(raw)
					)
			]


def Speaks_For_A_Game_Master(
		segments: list[str],
		) -> bool:
	"""Whether these segments open with the Game Master's mark."""
	if len(segments) < DM_SEGMENTS:
		return False
	return segments[0].lower() == DM_MARK


def Game_Master_Request(
		segments: list[str],
		) -> dict[str, Any] | None:
	"""The request a `dm/<level>/<seed>` address stands for, or nothing at all."""
	#-- Race and Archetype are named and left empty on purpose: a Game Master's
	#-- address carries no such choice, and the caller reads the same four keys
	#-- whichever half of this module answered.
	if not Speaks_For_A_Game_Master(segments):
		return None

	try:
		level = int(segments[1])
		seed = int(segments[2])
	except (TypeError, ValueError):
		return None

	return {
			"level": level,
			"seed": seed,
			"race": None,
			"archetype": None,
			}


def parse_npc_or_dm_path(
		raw: str,
		) -> dict[str, Any] | None:
	"""Parse `/npc/Race/Background/level/seed` or `/dm/level/seed`."""
	nonplayer = parse_nonplayer_path(
			raw,
			)

	if nonplayer is not None:
		return nonplayer

	return Game_Master_Request(
			Decoded_Segments(
					raw
					)
			)


def dm_session_hash(
		level: int,
		seed: int,
		) -> str:
	"""Shareable hash fragment body: `dm/<level>/<seed>` (no leading slash)."""
	return f"{DM_MARK}/{int(level)}/{int(seed)}"


def asgi_dm_redirect_target(
		pathname: str,
		*,
		canonical_base: str,
		) -> str | None:
	"""If pathname is a bare `/dm/<level>/<seed>` path, return hash redirect location."""
	#-- The tail is read raw, not percent-decoded, so that the address handed
	#-- back is the one the browser sent.  `parse_npc_or_dm_path` does decode,
	#-- so `/dm/5/%34%32` is refused here and accepted there.  That asymmetry
	#-- is the original's; it is recorded, not repaired, until QST-0134 closes.
	path = pathname or ""
	opening = f"/{DM_MARK}/"

	if opening not in path:
		return None

	tail = path[
			path.find(opening) + 1:
			]

	if Game_Master_Request(
			Segments(tail)
			) is None:
		return None

	base = canonical_base or "/"
	return f"{base}#{tail}"


__all__ = (
		"asgi_dm_redirect_target",
		"dm_session_hash",
		"parse_npc_or_dm_path",
		)


def _self_test() -> None:
	"""The four addresses this module must read, and the ones it must refuse."""

	#-- The original's own proof, kept word for word (recovered from the .pyc).
	assert parse_npc_or_dm_path("/dm/5/42") == {
			"level": 5,
			"seed": 42,
			"race": None,
			"archetype": None,
			}
	assert parse_npc_or_dm_path("/npc/Elf/Wizard/3/99")["seed"] == 99
	assert dm_session_hash(5, 42) == "dm/5/42"
	assert asgi_dm_redirect_target(
			"/app/dm/5/42",
			canonical_base="/app/",
			) == "/app/#dm/5/42"

	#-- One address, however it is written.
	for spelling in (
			"dm/5/42",
			"/dm/5/42",
			"#dm/5/42",
			"#/dm/5/42",
			"https://example.test/dm/5/42",
			"  /DM/5/42  ",
			):
		assert parse_npc_or_dm_path(spelling) == parse_npc_or_dm_path("/dm/5/42"), \
				f"{spelling!r} should read as the same session."

	#-- What is not a Game Master's address.
	for refusal in (
			"",
			None,
			"/dm/5",
			"/dm/five/42",
			"/dm//42",
			"/ledger/5/42",
			):
		assert parse_npc_or_dm_path(refusal) is None, \
				f"{refusal!r} should not read as a session."

	#-- The hash a shared session is written with, read back whole.
	assert parse_npc_or_dm_path(
			dm_session_hash(7, 1234)
			) == {
			"level": 7,
			"seed": 1234,
			"race": None,
			"archetype": None,
			}

	#-- The redirect only fires on a bare path, and keeps the mount it was given.
	assert asgi_dm_redirect_target(
			"/dm/1/2",
			canonical_base="",
			) == "/#dm/1/2"
	assert asgi_dm_redirect_target(
			"/app/ledger/1/2",
			canonical_base="/app/",
			) is None
	assert asgi_dm_redirect_target(
			"/app/dm/1",
			canonical_base="/app/",
			) is None

	#-- An NPC address still belongs to the NPC half, not to ours.
	imported = parse_npc_or_dm_path("/npc/Elf/Wizard/3/99")
	assert imported["race"] == "Elf", "The NPC half answers first."

	print(
			"OK — Map_of_Session_Paths self-test"
			)


if __name__ == "__main__":
	_self_test()
