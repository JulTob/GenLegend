"""Deterministic adapters for legacy NonPlayer sheet projections.

New TOP Features are already persisted grants.  This Map isolates the few
remaining legacy generators so Shiny can project each result repeatedly
without rerolling it or sharing RNG state between sessions.
"""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring,
#-- both public docstrings, both failure messages, the eleven Action names and
#-- the projection version are the original's, word for word; the
#-- transcription was proved instruction for instruction against the vaulted
#-- .pyc before this layout was applied.
#--
#-- Does this module own a domain axis (QST-0134)?  No.  It is a shim with one
#-- job, and the job is about *time*, not about what a Character is: a legacy
#-- renderer rolls dice when the page asks it to, so the same page rendered
#-- twice would show two different NonPlayers.  This Map lends each renderer a
#-- Dice Bag of its own, remembers what it produced, and hands the Character
#-- its own dice back untouched.  Nothing here is a property; it is plumbing,
#-- and it exists to be deleted when the last legacy renderer is gone.

from __future__ import annotations

from collections.abc import Callable
from contextlib import contextmanager

from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Features import Dice_Bag


Legacy_Renderer = Callable[[object], object]
	#-- A renderer takes the Character and returns whatever the sheet shows.

_PROJECTION_VERSION = "legacy-sheet-2"
	#-- Bumping this re-rolls every legacy section, on purpose.

_MISSING = object()
	#-- Distinguishes "the Character has no such attribute" from "it is None".

_CACHE_FIELD = "_legacy_sheet_sections"
	#-- Where a Character keeps what its legacy renderers already produced.


_ATTRIBUTE_ACTIONS = {
		"ideal": "ResolveIdeal",
		"languages": "ResolveLanguages",
		"passive_perception": "ResolvePassivePerception",
		"plothook": "ResolvePlotHook",
		"resistances": "ResolveResistances",
		"senses": "ResolveSenses",
		"simple_attacks": "SimpleAttack",
		"special_attack": "SpecialAttack",
		"spells": "Magic",
		"story": "SetMyStory",
		"trait": "ResolveTrait",
		}
	#-- The eleven sheet fields still produced by an Action on the Character
	#-- rather than by a Tag.  Each entry is one thing left to migrate.


def Section_Cache(
		character,
		) -> dict:
	"""The Character's record of what its legacy renderers already produced."""
	cache = getattr(
			character,
			_CACHE_FIELD,
			None,
			)

	if cache is None:
		cache = {}
		setattr(
				character,
				_CACHE_FIELD,
				cache,
				)

	return cache


@contextmanager
def Borrowed_Dice(
		character,
		dice_bag,
		):
	"""Lend the Character one Dice Bag, then give its own back untouched."""
	#-- Untouched means both the object and its position in the sequence: a
	#-- renderer that rolls must not advance the Character's own dice, or the
	#-- next thing generated would differ merely because a page was rendered.
	character_dice = getattr(
			character,
			"dices",
			None,
			)

	character_dice_state = (
		character_dice.getstate()
		if character_dice is not None
		else None
		)

	character.dices = dice_bag

	try:
		yield
	finally:
		character.dices = character_dice

		if (
			character_dice is not None
			and character_dice_state is not None
			):
			character_dice.setstate(
					character_dice_state
					)


def Resolve_Legacy_Section(
		character,
		section: str,
		renderer: Legacy_Renderer,
		) -> object:
	"""Resolve and cache one transitional sheet section from its Dice Bag."""
	if not section:
		raise ValueError(
				"A legacy NonPlayer section requires a stable name."
				)

	if not callable(
			renderer
			):
		raise TypeError(
				f"Renderer for {section!r} must be callable."
				)

	cache = Section_Cache(
			character,
			)

	if section in cache:
		return cache[
				section
				]

	dice_bag = Dice_Bag(
			character,
			f"npc.sheet.{section}",
			catalog_version=_PROJECTION_VERSION,
			)

	with Borrowed_Dice(
			character,
			dice_bag,
			):
		result = renderer(
				character
				)

	cache[
			section
			] = result

	return result


def Resolve_Legacy_Attribute(
		character,
		attribute: str,
		default: object = "-",
		) -> object:
	"""Read a Record or materialize one through its explicit Agent Action."""
	current = getattr(
			character,
			attribute,
			_MISSING,
			)

	#-- Already a value, and not still a method waiting to be called: that is
	#-- the answer, and asking again would be asking the sheet to change.
	if (
		current is not _MISSING
		and not callable(current)
		):
		return current

	action_name = _ATTRIBUTE_ACTIONS.get(
			attribute
			)

	if action_name is None:
		return default

	action = getattr(
			character,
			action_name,
			None,
			)

	if not callable(
			action
			):
		return default

	result = Resolve_Legacy_Section(
			character,
			f"attribute.{attribute}",
			lambda _: action(),
			)

	#-- Written back onto the Character, so the second read is a plain read.
	setattr(
			character,
			attribute,
			result,
			)

	return result


__all__ = (
		"Resolve_Legacy_Attribute",
		"Resolve_Legacy_Section",
		)


def _self_test() -> None:
	"""Rendering twice gives one answer, and never moves the Character's dice."""
	from AtlasActorLudi.CharactersKit import Character

	#-- The original's own proof, kept (recovered from the .pyc).
	character = Character(
			seed=41,
			)

	original_state = character.dices.getstate()

	first = Resolve_Legacy_Section(
			character,
			"test",
			lambda target: target.Roll(
					20
					),
			)

	second = Resolve_Legacy_Section(
			character,
			"test",
			lambda target: target.Roll(
					20
					),
			)

	assert first == second, \
			f"The same section rendered twice must not change: {first} then {second}"
	assert character.dices.getstate() == original_state, \
			"Rendering must leave the Character's own dice exactly where they were."

	#-- Two sections are two answers, each remembered under its own name.
	rolls = [
			Resolve_Legacy_Section(
					character,
					name,
					lambda target: target.Roll(
							1000
							),
					)
			for name in ("a", "b", "c")
			]
	assert [
			Resolve_Legacy_Section(
					character,
					name,
					lambda target: target.Roll(
							1000
							),
					)
			for name in ("a", "b", "c")
			] == rolls, "Each section keeps its own first answer."

	#-- Two Characters from the same seed project the same sheet.
	twin = Character(
			seed=41,
			)
	assert Resolve_Legacy_Section(
			twin,
			"test",
			lambda target: target.Roll(
					20
					),
			) == first, "The same seed must project the same sheet."

	#-- A renderer that raises leaves the Character's dice as it found them.
	before = character.dices.getstate()
	try:
		Resolve_Legacy_Section(
				character,
				"angry",
				lambda target: 1 / 0,
				)
	except ZeroDivisionError:
		pass
	else:
		raise AssertionError(
				"A renderer that raises should not be swallowed."
				)
	assert character.dices.getstate() == before, \
			"A failed render must still hand the Character's dice back."
	assert "angry" not in Section_Cache(character), \
			"A failed render records nothing."

	#-- What the section rite refuses.
	refusals = (
			( ("", lambda target: 1), ValueError, "requires a stable name" ),
			( (None, lambda target: 1), ValueError, "requires a stable name" ),
			( ("named", "not callable"), TypeError, "must be callable" ),
			)
	for (section, renderer), kind, expected in refusals:
		try:
			Resolve_Legacy_Section(
					character,
					section,
					renderer,
					)
		except kind as refusal:
			assert expected in str(refusal), \
					f"{section!r} was refused, but not for {expected!r}: {refusal}"
		else:
			raise AssertionError(
					f"{section!r} with {renderer!r} should have been refused."
					)

	#-- The attribute rite: a plain value is returned as it stands.
	class _A_Sheet:
		ideal = "Freedom"

	assert Resolve_Legacy_Attribute(_A_Sheet(), "ideal") == "Freedom"

	#-- An attribute nothing knows how to make falls back to the default.
	assert Resolve_Legacy_Attribute(_A_Sheet(), "unheard_of") == "-"
	assert Resolve_Legacy_Attribute(_A_Sheet(), "unheard_of", None) is None

	#-- An attribute with a known Action, but no Action on this Character.
	assert Resolve_Legacy_Attribute(_A_Sheet(), "trait") == "-"

	print(
			"OK — NonPlayer projections use isolated Character Dice Bags"
			)


if __name__ == "__main__":
	_self_test()
