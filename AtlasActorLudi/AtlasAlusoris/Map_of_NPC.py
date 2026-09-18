"""
Map of NPCs
Handles NPC generation for D&D 5e.
"""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring,
#-- the contract and the three failure messages are the original's, word for
#-- word, read out of the vaulted .pyc; the layout and the named helper follow
#-- today's Canon.  Nothing here owns a domain axis — it validates a request
#-- and delegates — so no Tag is invented for it.

from __future__ import annotations

from AtlasActorLudi.AtlasAlusoris.Grimoire_of_NPC import NPC
from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Generation import (
		summon_nonplayer_list,
		)


ANY = "Random"
	#-- What the form sends when the table expresses no preference.


def Chosen(
		selection: str,
		) -> str | None:
	"""The request a selection stands for: a name, or nothing at all."""
	return None if selection == ANY else selection


def generate_npcs(
		selected_race: str = ANY,
		selected_background: str = ANY,
		count: int = 10,
		seed: int | None = None,
		level: int = 10,
		):
	"""
	Generate NPCs from the selected Race and Background.

	Preconditions:
	>>      <selected_race> should be a valid race string or "Random".
	>>      <selected_background> should be a valid Background or "Random".
	>>      <count> should be an integer >= 1.

	Postconditions:
	<<      Returns generated Characters from the canonical NonPlayer route.
	"""
	assert isinstance(selected_race, str), \
			"Precondition failed: selected_race must be a string."
	assert isinstance(selected_background, str), \
			"Precondition failed: selected_background must be a string."
	assert isinstance(count, int) and count >= 1, \
			"Precondition failed: count must be an integer >= 1."

	return summon_nonplayer_list(
			race=Chosen(selected_race),
			background=Chosen(selected_background),
			count=count,
			seed=seed,
			level=level,
			)


__all__ = (
		"NPC",
		"generate_npcs",
		)


def _self_test() -> None:
	"""The contract, proven.  Generation itself is QST-0075 (see below)."""
	#-- What this cannot prove: that NPCs actually generate.  summon_nonplayer
	#-- fails on every call today (Repairs-Ledger A1), so a test that summoned
	#-- one would fail for a reason this module is not responsible for.  The
	#-- contract is what this file owns, and the contract is what is checked.

	assert Chosen(ANY) is None, "Random stands for no preference at all."
	assert Chosen("Elf") == "Elf", "A named Race passes through unchanged."
	assert Chosen("") == "", "Only the sentinel is special."

	refusals = (
			( { "selected_race": 7 }, "selected_race must be a string" ),
			( { "selected_background": None }, "selected_background must be a string" ),
			( { "count": 0 }, "count must be an integer >= 1" ),
			( { "count": "many" }, "count must be an integer >= 1" ),
			)

	for request, expected in refusals:
		try:
			generate_npcs(**request)
		except AssertionError as refusal:
			assert expected in str(refusal), (
					f"{request} was refused, but not for {expected!r}: {refusal}"
					)
		else:
			raise AssertionError(
					f"{request} should have been refused."
					)

	print(
			"OK — Map_of_NPC self-test (the contract; generation is QST-0075)"
			)


if __name__ == "__main__":
	_self_test()
