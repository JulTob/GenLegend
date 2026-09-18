"""Deterministically select and persist an NPC tactical feature loadout."""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring,
#-- all six public docstrings, the failure message, the identity sets and the
#-- selection rules are the original's, word for word; the transcription was
#-- proved instruction for instruction against the vaulted .pyc before this
#-- layout was applied.
#--
#-- Does this module own a domain axis (QST-0134)?  No — it owns a *policy*.
#-- Every Tag already exists: FeaturesKit mints one per catalogue entry, and
#-- the Lodge holds the entries.  What lives here is the answer to "which
#-- three to five of them does this NonPlayer get, and why", which is an
#-- algorithm, not a property.  A Character is not a Selection.
#--
#-- The rule the whole file serves: the generator decides once and stores the
#-- result; the Shiny app only projects what was stored.  Nothing downstream
#-- may re-roll, so every choice here draws from the Character's own Dice Bag
#-- and never from a global RNG.

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable as Iterable_Collection
from collections.abc import Mapping
from random import Random
from re import split
from typing import Iterable

from TagKit import Tags

from AtlasActorLudi.CharactersKit import NonPlayer
from AtlasActorLudi.Map_of_Scores import PB
from AtlasActorLudi.AtlasAlusoris.FeaturesKit import (
		Activation,
		Feature_Grant,
		Feature_Spec,
		)
from AtlasActorLudi.AtlasAlusoris.Lodge_of_NonPlayer_Features import (
		CATALOG_VERSION,
		FEATURE_SPECS,
		FEATURE_TAGS,
		)


_SPELLCASTING_IDENTITIES = frozenset(
		{
				"bard",
				"cleric",
				"druid",
				"mage",
				"paladin",
				"priest",
				"ranger",
				"shaman",
				"sorcerer",
				"warlock",
				"witch",
				"wizard",
				}
		)
	#-- Any of these on a NonPlayer means it casts, whichever axis said so.

_POWER_SOURCE_IDENTITIES = {
		"arcane": frozenset(
				{
						"bard",
						"mage",
						"sorcerer",
						"wizard",
						}
				),
		"divine": frozenset(
				{
						"cleric",
						"paladin",
						"priest",
						}
				),
		"occult": frozenset(
				{
						"cultist",
						"warlock",
						"witch",
						}
				),
		"primal": frozenset(
				{
						"druid",
						"ranger",
						"shaman",
						}
				),
		}
	#-- Where the magic comes from.  A catalogue entry may ask for "arcane"
	#-- without naming every Guild that counts as arcane.

_SPELL_BAGS = ("known_spells", "prepared_spells", "spell_list")
	#-- The three places a Character may keep spells, whatever shape they take.

_MINIMUM_FEATURES = 3
_MAXIMUM_FEATURES = 5
	#-- The loadout stays readable at a table: never fewer than three, never
	#-- more than five, whatever the proficiency bonus says.

_AFFINITY_WEIGHT = 8
	#-- How much one matching affinity is worth against a bare candidate.
	#-- A spec that matches nothing still weighs 1, so nothing is impossible.

_SAME_ACTIVATION_LIMIT = 2
	#-- Past two of a kind, a NonPlayer's turn stops having choices in it.


# ---------------------------------------------------------------------------
#  Reading a Character: what does this creature look like, in words?
# ---------------------------------------------------------------------------

def _tag_names(
		character,
		) -> Iterable[str]:
	"""Yield each active Tag's explicit domain name once."""
	seen = set()

	for leaf in Tags(
			character
			):
		for tag in leaf.Form():
			if tag in seen:
				continue

			seen.add(
					tag
					)

			name = getattr(
					tag,
					"NAME",
					tag.__name__,
					)

			if not isinstance(
					name,
					str,
					):
				continue
			if not name:
				continue
			yield name


def _spell_records(
		value,
		) -> Iterable[object]:
	"""Flatten a spell bag of any shape into the records inside it."""
	#-- A bag may be a list, a dict of lists, a dict of dicts, or one spell.
	#-- Strings and bytes are records, not containers, however iterable.
	if value is None:
		return

	if isinstance(
			value,
			Mapping,
			):
		for nested in value.values():
			yield from _spell_records(
					nested
					)

		return

	if isinstance(
			value,
			Iterable_Collection,
			) and not isinstance(
			value,
			(
					str,
					bytes,
					),
			):
		for nested in value:
			yield from _spell_records(
					nested
					)

		return

	yield value


def _structured_spell_values(
		character,
		) -> Iterable[str]:
	"""Every word a Character's spells contribute: names, schools, traditions."""
	fields = getattr(
			character,
			"__dict__",
			{},
			)

	for bag_name in _SPELL_BAGS:
		for spell in _spell_records(
				fields.get(
						bag_name
						)
				):
			if isinstance(
					spell,
					str,
					):
				yield spell

				continue

			for attribute in (
					"name",
					"school",
					"damage_type",
					"tradition",
					):
				value = getattr(
						spell,
						attribute,
						None,
						)

				if not isinstance(
						value,
						str,
						):
					continue

				yield value

			yield from _tag_names(
					spell
					)


def _identity_values(
		character,
		) -> list[str]:
	"""Everything this Character says about itself, before any tidying."""
	values = list(
			_tag_names(
					character
					)
			)

	values.extend(
			_structured_spell_values(
					character
					)
			)

	#-- The compatibility axes: a NonPlayer built before the Tags existed
	#-- still carries these as plain strings, and they still describe it.
	for attribute in (
			"race",
			"species",
			"subrace",
			"char_class",
			"background",
			):
		value = getattr(
				character,
				attribute,
				None,
				)

		if not isinstance(
				value,
				str,
				):
			continue

		values.append(
				value
				)

	return values


def _tokenized(
		values: Iterable[str],
		) -> set[str]:
	"""Each phrase folded to one key, plus each word in it as a key of its own."""
	#-- "Fire Elemental" becomes "fire elemental", "fire" and "elemental", so a
	#-- catalogue entry may ask for any of the three.
	normalized = set()

	for value in values:
		if not value:
			continue

		canonical = value.strip().casefold()
		normalized.add(
				canonical
				)
		normalized.update(
				token
				for token in split(
						"[^a-z0-9]+",
						canonical,
						)
				if token
				)

	return normalized


def _add_magic_keys(
		normalized: set[str],
		) -> None:
	"""If anything here casts, say so in the words a catalogue entry uses."""
	if normalized.intersection(
			_SPELLCASTING_IDENTITIES
			):
		normalized.update(
				{
						"magic",
						"spellcaster",
						}
				)

	for power_source, identities in _POWER_SOURCE_IDENTITIES.items():
		matches = normalized.intersection(
				identities
				)

		if not matches:
			continue

		normalized.add(
				power_source
				)
		normalized.add(
				f"{power_source} magic"
				)

		for identity in matches:
			normalized.add(
					f"{identity} spell list"
					)


def Semantic_Keys(
		character,
		) -> tuple[str, ...]:
	"""Collect canonical Tag names and compatibility identity fields."""
	normalized = _tokenized(
			_identity_values(
					character
					)
			)

	_add_magic_keys(
			normalized,
			)

	return tuple(
			sorted(
					normalized
					)
			)


# ---------------------------------------------------------------------------
#  Judging one catalogue entry against one Character
# ---------------------------------------------------------------------------

def _normalized(
		values: Iterable[str],
		) -> frozenset[str]:
	"""A catalogue entry's words, folded so they compare with a Character's."""
	return frozenset(
			value.casefold()
			for value in values
			)


def _eligible(
		spec: Feature_Spec,
		*,
		level: int,
		semantic_keys: frozenset[str],
		) -> bool:
	"""Whether this Character may be offered this entry at all."""
	required = _normalized(
			spec.requires_any
			)

	excluded = _normalized(
			spec.excludes_any
			)

	if spec.minimum_level > level:
		return False

	if (
		required
		and not required.intersection(
				semantic_keys
				)
		):
		return False

	return not excluded.intersection(
			semantic_keys
			)


def _affinity_matches(
		spec: Feature_Spec,
		semantic_keys: frozenset[str],
		) -> tuple[str, ...]:
	"""Which of this entry's affinities this Character actually answers to."""
	return tuple(
			sorted(
					_normalized(
							spec.affinities
							).intersection(
							semantic_keys
							)
					)
			)


def _weight(
		spec: Feature_Spec,
		semantic_keys: frozenset[str],
		) -> int:
	"""How strongly this entry suits this Character, as a draw weight."""
	return 1 + _AFFINITY_WEIGHT * len(
			_affinity_matches(
					spec,
					semantic_keys,
					)
			)


# ---------------------------------------------------------------------------
#  Choosing a loadout
# ---------------------------------------------------------------------------

def Dice_Bag(
		character,
		purpose: str,
		*,
		catalog_version: str = CATALOG_VERSION,
		) -> Random:
	"""Open the Character Dice Bag for one versioned NPC purpose."""
	#-- Versioned by the catalogue: when the entries change, the draw changes
	#-- with them, rather than a new catalogue silently reusing old rolls.
	return character.Dice_Bag(
			purpose,
			version=catalog_version,
			namespace="GenLegendNPC",
			)


def Feature_Count(
		character,
		) -> int:
	"""Use level-based PB with an explicit readable three-to-five clamp."""
	level = max(
			1,
			int(
					getattr(
							character,
							"level",
							1,
							)
					),
			)

	return max(
			_MINIMUM_FEATURES,
			min(
					_MAXIMUM_FEATURES,
					PB(
							level
							),
					),
			)


def _weighted_pick(
		candidates: list[Feature_Spec],
		*,
		semantic_keys: frozenset[str],
		dice: Random,
		) -> Feature_Spec:
	"""One entry drawn from the pool, favouring the ones that suit."""
	return dice.choices(
			candidates,
			weights=[
					_weight(
							spec,
							semantic_keys,
							)
					for spec in candidates
					],
			k=1,
			)[
			0
			]


def _available(
		candidates: list[Feature_Spec],
		selected: list[Feature_Spec],
		) -> list[Feature_Spec]:
	"""The entries still open: not already taken, and not a second of a kind."""
	selected_keys = {
			spec.key
			for spec in selected
			}

	uniqueness_groups = {
			spec.uniqueness_group
			for spec in selected
			if spec.uniqueness_group
			}

	return [
			spec
			for spec in candidates
			if spec.key not in selected_keys
			and (
					not spec.uniqueness_group
					or spec.uniqueness_group not in uniqueness_groups
					)
			]


def _eligible_candidates(
		catalogue: Iterable[Feature_Spec],
		level: int,
		semantic_keys: frozenset[str],
		) -> list[Feature_Spec]:
	"""Every entry this Character qualifies for, in a fixed order."""
	#-- Sorted by key, not by catalogue order: the draw must not change when
	#-- somebody inserts a new entry in the middle of the Lodge.
	return sorted(
			(
					spec
					for spec in catalogue
					if _eligible(
							spec,
							level=level,
							semantic_keys=semantic_keys,
							)
					),
			key=lambda spec: spec.key,
			)


def _carries_an_action(
		selected: list[Feature_Spec],
		) -> bool:
	"""Whether the loadout so far gives this NonPlayer something to do."""
	return any(
			spec.activation == Activation.ACTION
			for spec in selected
			)


def _roles_already_covered(
		selected: list[Feature_Spec],
		) -> set:
	"""Every battlefield purpose the loadout so far already serves."""
	return {
			role
			for spec in selected
			for role in spec.tactical_roles
			}


def _next_pool(
		remaining: list[Feature_Spec],
		selected: list[Feature_Spec],
		) -> list[Feature_Spec]:
	"""The pool the next draw comes from: varied first, then merely unused."""
	#-- Three preferences, each falling back to the next: an entry serving a
	#-- purpose nothing else serves; failing that, one whose activation is not
	#-- already doubled; failing that, whatever is left.
	roles = _roles_already_covered(
			selected,
			)

	varied = [
			spec
			for spec in remaining
			if any(
					role not in roles
					for role in spec.tactical_roles
					)
			]

	activation_counts = Counter(
			spec.activation
			for spec in selected
			)

	lightly_used = [
			spec
			for spec in (
					varied
					or remaining
					)
			if activation_counts[
					spec.activation
					] < _SAME_ACTIVATION_LIMIT
			]

	return (
		lightly_used
		or varied
		or remaining
		)


def Select_Feature_Specs(
		character,
		catalogue: Iterable[Feature_Spec] = FEATURE_SPECS,
		) -> tuple[Feature_Spec, ...]:
	"""Select unique, varied specs without consuming any global RNG."""
	semantic_keys = frozenset(
			Semantic_Keys(
					character
					)
			)

	level = max(
			1,
			int(
					getattr(
							character,
							"level",
							1,
							)
					),
			)

	candidates = _eligible_candidates(
			catalogue,
			level,
			semantic_keys,
			)

	target = min(
			Feature_Count(
					character
					),
			len(
					candidates
					),
			)

	if target == 0:
		return ()

	dice = Dice_Bag(
			character,
			"npc.features",
			)

	selected = []

	#-- First, something that suits this creature in particular.
	influenced = [
			spec
			for spec in candidates
			if _affinity_matches(
					spec,
					semantic_keys,
					)
			]

	if influenced:
		selected.append(
				_weighted_pick(
						influenced,
						semantic_keys=semantic_keys,
						dice=dice,
						)
				)

	#-- Then, if there is still room, make sure it can act on its turn.
	if (
		len(selected) < target
		and not _carries_an_action(selected)
		):
		action_candidates = [
				spec
				for spec in _available(
						candidates,
						selected,
						)
				if spec.activation == Activation.ACTION
				]

		if action_candidates:
			selected.append(
					_weighted_pick(
							action_candidates,
							semantic_keys=semantic_keys,
							dice=dice,
							)
					)

	#-- Then fill the rest, preferring variety over repetition.
	while len(selected) < target:
		remaining = _available(
				candidates,
				selected,
				)

		if not remaining:
			break

		selected.append(
				_weighted_pick(
						_next_pool(
								remaining,
								selected,
								),
						semantic_keys=semantic_keys,
						dice=dice,
						)
				)

	return tuple(
			selected
			)


# ---------------------------------------------------------------------------
#  Writing the loadout onto the Character
# ---------------------------------------------------------------------------

def Apply_NonPlayer_Features(
		character,
		) -> tuple[Feature_Grant, ...]:
	"""Select once, apply semantic Feature Tags, and freeze resolved grants."""
	if character not in NonPlayer:
		raise ValueError(
				"NPC tactical Features require the NonPlayer role."
				)

	existing = getattr(
			character,
			"npc_features",
			None,
			)

	#-- Idempotent on purpose: a Character asked twice keeps the first answer,
	#-- so a page that re-renders does not re-roll the loadout.
	if existing:
		return tuple(
				existing
				)

	character.npc_features = []
	semantic_keys = frozenset(
			Semantic_Keys(
					character
					)
			)

	for spec in Select_Feature_Specs(
			character
			):
		contributing_tags = _affinity_matches(
				spec,
				semantic_keys,
				)

		tag = FEATURE_TAGS[
				spec.key
				]

		if character not in tag:
			tag(
					character,
					contributing_tags=contributing_tags,
					)

	#-- Frozen once applied: what the sheet shows is what was decided here.
	character.npc_features = tuple(
			character.npc_features
			)

	character.npc_feature_catalog_version = CATALOG_VERSION

	return character.npc_features


__all__ = (
		"Apply_NonPlayer_Features",
		"Feature_Count",
		"Dice_Bag",
		"Select_Feature_Specs",
		"Semantic_Keys",
		)


class _A_Spellbook:
	"""One spell record, carrying the four words the reader looks for."""

	def __init__(
			self,
			name,
			school=None,
			damage_type=None,
			tradition=None,
			):
		self.name = name
		self.school = school
		self.damage_type = damage_type
		self.tradition = tradition


def _a_nonplayer(**fields):
	"""One NonPlayer to select a loadout for, built from a fixed seed."""
	from AtlasActorLudi.CharactersKit import Character

	who = Character(
			seed=fields.pop("seed", 11),
			level=fields.pop("level", 5),
			)
	for key, value in fields.items():
		setattr(who, key, value)
	NonPlayer(who)
	return who


def _test_reading_a_character() -> None:
	"""A Character's words become keys a catalogue entry can ask for."""
	keys = Semantic_Keys(
			_a_nonplayer(char_class="Wizard", race="Fire Elemental"),
			)

	assert "wizard" in keys, "A Guild is one of the words."
	assert "fire elemental" in keys, "So is a whole Race name."
	assert "fire" in keys and "elemental" in keys, \
			"And each word within it, so an entry may ask for either."
	assert "arcane" in keys, "A Wizard's magic has a source, and it is named."
	assert "arcane magic" in keys and "wizard spell list" in keys
	assert "magic" in keys and "spellcaster" in keys, \
			"Anything that casts says so plainly."

	#-- A Cleric is divine, not arcane; the sources do not bleed.
	divine = Semantic_Keys(
			_a_nonplayer(char_class="Cleric"),
			)
	assert "divine" in divine and "arcane" not in divine

	#-- Nothing that casts, nothing claimed.
	mundane = Semantic_Keys(
			_a_nonplayer(char_class="Fighter", race="Human"),
			)
	assert "magic" not in mundane and "spellcaster" not in mundane

	assert keys == tuple(sorted(keys)), "The keys come back in a fixed order."


def _test_reading_spells_of_any_shape() -> None:
	"""A spell bag is read whether it is a list, a dict, or one record."""
	from_strings = Semantic_Keys(
			_a_nonplayer(known_spells=["Fireball", "Shield"]),
			)
	assert "fireball" in from_strings and "shield" in from_strings

	nested = Semantic_Keys(
			_a_nonplayer(prepared_spells={ "1": ["Bless"], "2": { "a": ["Aid"] } }),
			)
	assert "bless" in nested and "aid" in nested, "However deep the bag goes."

	structured = Semantic_Keys(
			_a_nonplayer(
					spell_list=[
							_A_Spellbook(
									"Ice Knife",
									school="Conjuration",
									damage_type="cold",
									tradition="arcane",
									),
							],
					),
			)
	for word in ("ice knife", "conjuration", "cold", "arcane"):
		assert word in structured, f"{word!r} should be read off the spell."

	#-- A bag that is empty, missing or nonsense is simply not read.
	for bag in (None, [], "", 7, [None, 7]):
		Semantic_Keys(
				_a_nonplayer(known_spells=bag),
				)


def _test_how_many_features() -> None:
	"""Three at low levels, five at high, never outside that."""
	counts = {
			level: Feature_Count(
					_a_nonplayer(level=level),
					)
			for level in (1, 4, 5, 8, 9, 12, 13, 16, 17, 20)
			}
	assert set(counts.values()) <= { _MINIMUM_FEATURES, _MAXIMUM_FEATURES } | { 4 }, \
			f"A loadout size escaped the clamp: {counts}"
	assert min(counts.values()) >= _MINIMUM_FEATURES
	assert max(counts.values()) <= _MAXIMUM_FEATURES
	assert counts[1] == _MINIMUM_FEATURES, "Proficiency 2 clamps up to three."
	assert counts[20] == _MAXIMUM_FEATURES, "Proficiency 6 clamps down to five."


def _test_the_loadout_is_decided_once() -> None:
	"""The same NonPlayer gets the same loadout, and only ever one."""
	first = [
			spec.key
			for spec in Select_Feature_Specs(
					_a_nonplayer(seed=42, level=9, char_class="Wizard"),
					)
			]
	again = [
			spec.key
			for spec in Select_Feature_Specs(
					_a_nonplayer(seed=42, level=9, char_class="Wizard"),
					)
			]
	assert first == again, "The same seed must give the same loadout."
	assert len(first) == len(set(first)), f"An entry was chosen twice: {first}"

	#-- Two of the same uniqueness group never appear together.
	groups = [
			spec.uniqueness_group
			for spec in Select_Feature_Specs(
					_a_nonplayer(seed=42, level=20, char_class="Fighter"),
					)
			if spec.uniqueness_group
			]
	assert len(groups) == len(set(groups)), \
			f"Two of one kind were both chosen: {groups}"

	#-- Nothing to choose from means nothing chosen, not a failure.
	assert Select_Feature_Specs(
			_a_nonplayer(seed=1),
			(),
			) == ()


def _test_applying_the_loadout() -> None:
	"""Applying writes resolved grants once, and refuses a Player."""
	from AtlasActorLudi.CharactersKit import Character

	npc = _a_nonplayer(seed=7, level=9, char_class="Cleric")
	grants = Apply_NonPlayer_Features(
			npc,
			)

	assert grants, "A level-nine Cleric receives a loadout."
	assert isinstance(npc.npc_features, tuple), "The loadout is frozen once written."
	assert npc.npc_feature_catalog_version == CATALOG_VERSION, \
			"The sheet records which catalogue it was built from."

	for grant in grants:
		assert "{" not in grant.description, \
				f"{grant.key} reached the sheet with a placeholder: {grant.description}"

	#-- Asked again, it keeps the first answer rather than re-rolling.
	assert Apply_NonPlayer_Features(npc) == grants

	#-- A Player has no NonPlayer role, and is told so.
	player = Character(seed=7, level=9)
	try:
		Apply_NonPlayer_Features(player)
	except ValueError as refusal:
		assert "require the NonPlayer role" in str(refusal), \
				f"A Player was refused, but not for the right reason: {refusal}"
	else:
		raise AssertionError(
				"A Player should not receive NonPlayer tactical Features."
				)


def _self_test() -> None:
	_test_reading_a_character()
	_test_reading_spells_of_any_shape()
	_test_how_many_features()
	_test_the_loadout_is_decided_once()
	_test_applying_the_loadout()
	print("OK — Alusoris Map_of_NonPlayer_Features self-test")


if __name__ == "__main__":
	_self_test()
