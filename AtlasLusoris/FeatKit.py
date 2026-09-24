"""
FeatKit

TOP catalogues for Fighting Style feats, General feats, and Epic Boons.
Origin feats stay in FeaturesKit; Invocations stay in InvocationKit.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from TopKit import Imprint, Post, Pre, Record, Tag

from AtlasActorLudi.CharactersKit import Report_Of

from AtlasActorLudi.CharactersKit import Character
from AtlasActorLudi.ProficiencyKit import (
	Commit_Training_Gain,
	Feature_Training_Record,
	New_Feature_Training_Record,
	Training_Batch,
	)
from AtlasLusoris.GuildKit import ability_preference
from AtlasLusoris.FeaturesKit import (
	Feat as Feat_Root,
	grant,
	)

_ABILITY_FULL = {
		"STR": "Strength",
		"DEX": "Dexterity",
		"CON": "Constitution",
		"INT": "Intelligence",
		"WIS": "Wisdom",
		"CHA": "Charisma",
		}

# The catalogue opens a feat with its ability-score clause, in one of three
# shapes: "Increase your Strength or Dexterity by 1, to a maximum of 20.",
# "Increase one ability score of your choice by 1, to a maximum of 20." and
# the Ability Score Improvement wording, which ends "above 20 this way."
# instead.  Matching only the first shape left the other two printing the
# instruction *and* the result, so a sheet said both "Increase one ability
# score" and "Your Wisdom was increased by 1".
_ASI_PREAMBLE = re.compile(
		r"^Increase (?:your|one ability score|two ability scores)\b.*?"
		r"(?:to a maximum of \d+\.|above \d+ this way\.)\s*",
		re.IGNORECASE | re.DOTALL,
		)


class Fighting_Style_Feat(Feat_Root):
	"""Fighting Style feat — requires the Fighting Style class feature."""

	NAME = "Fighting Style Feat"


class General_Feat(Feat_Root):
	"""General feat — ASI replacement from level 4+."""

	NAME = "General Feat"


class Epic_Boon_Feat(Feat_Root):
	"""Epic Boon feat — level 19+."""

	NAME = "Epic Boon"


_FIGHTING_STYLE_DECLARATIONS: list[type[Fighting_Style_Feat]] = []
_GENERAL_FEAT_DECLARATIONS: list[type[General_Feat]] = []
_EPIC_BOON_DECLARATIONS: list[type[Epic_Boon_Feat]] = []


def _class_name(
		name: str,
		) -> str:
	return "".join(
			part.capitalize()
			for part in name.replace(
					"-",
					" ",
					).replace(
					"'",
					"",
					).split()
			)


def _ability_score(
		char,
		key: str,
		) -> int:
	abilities = getattr(
			char,
			"abilities",
			None,
			)
	if abilities is None:
		return 0
	return int(
			getattr(
					abilities,
					key,
					0,
					) or 0
			)


def _raise_stat(
		char,
		key: str,
		amount: int = 1,
		cap: int = 20,
		) -> None:
	abilities = getattr(
			char,
			"abilities",
			None,
			)
	if abilities is None:
		return
	current = int(
			getattr(
					abilities,
					key,
					10,
					) or 10
			)
	new_val = min(
			current + amount,
			cap,
			)
	setattr(
			abilities,
			key,
			new_val,
			)
	# Keep sheet Stats dict in sync when present.
	stats = getattr(
			char,
			"stats",
			None,
			)
	full = _ABILITY_FULL.get(
			key
			)
	if isinstance(
			stats,
			dict,
			) and full:
		stats[full] = new_val


def _sheet_feat_description(
		catalogue_text: str,
		*,
		raised: list[tuple[str, int]] | None = None,
		) -> str:
	"""
	Rewrite feat prose for the sheet: applied ASIs in past tense.

	Ongoing rules stay; the ability-score change reports what happened.
	"""
	body = _ASI_PREAMBLE.sub(
			"",
			(catalogue_text or "").strip(),
			).strip()
	parts: list[str] = []
	for key, amount in raised or []:
		full = _ABILITY_FULL.get(
				key,
				key,
				)
		parts.append(
				f"Your {full} was increased by {amount}."
				)
	if body:
		parts.append(
				body
				)
	# The applied increase is its own paragraph.  It reports what happened to
	# the Character; everything after it is the standing rule, and running the
	# two together made the sheet read as one long sentence.
	return "\n\n".join(
			parts
			)


def _raise_one_of(
		char,
		keys: tuple[str, ...],
		amount: int = 1,
		cap: int = 20,
		) -> str | None:
	viable = [
			key
			for key in keys
			if _ability_score(
					char,
					key,
					) < cap
			]
	if not viable:
		return None
	# Prefer odd scores so a +1 more often changes the modifier.
	odd = [
			key
			for key in viable
			if _ability_score(
					char,
					key,
					) % 2
			]
	pool = odd or viable
	ordered = sorted(
		pool
		)
	# Shuffle first so equally-preferred keys stay reproducible, then let the
	# Character's own preference order decide.  Sorting is stable, so the
	# shuffle survives as the tie-break among abilities nobody asked for.
	char.Dice_Bag(
		"feat.ability."
		+ ".".join(
				keys
				),
		version="1",
		namespace="GenLegendFeat",
		).shuffle(
			ordered
			)
	preference = ability_preference(
		char
		)
	ordered.sort(
		key=lambda name: (
			preference.index(
				name
				)
			if name in preference
			else len(
				preference
				)
			),
		)
	key = ordered[0]
	_raise_stat(
			char,
			key,
			amount=amount,
			cap=cap,
			)
	return key


def _raise_any(
		char,
		amount: int = 1,
		cap: int = 30,
		) -> str | None:
	return _raise_one_of(
			char,
			(
					"STR",
					"DEX",
					"CON",
					"INT",
					"WIS",
					"CHA",
					),
			amount=amount,
			cap=cap,
			)


def _owned_feat_names(
		char,
		) -> set[str]:
	names = {
			getattr(
					feat,
					"name",
					None,
					)
			for feat in (
					getattr(
							char,
							"features",
							None,
							) or []
					)
			}
	return {
			name
			for name in names
			if name
			}


def fighting_styles_known(
		char,
		) -> int:
	"""How many Fighting Style feats this Character should hold."""
	level = int(
			getattr(
					char,
					"level",
					1,
					) or 1
			)
	guild = getattr(
			char,
			"char_class",
			None,
			)
	need = 0
	if guild == "Fighter" and level >= 1:
		need = 1
	elif guild == "Paladin" and level >= 2:
		need = 1
	elif guild == "Ranger" and level >= 2:
		need = 1
	# 2024 Champion — Additional Fighting Style at 7.
	if level >= 7:
		from AtlasLusoris.AtlasOfGuilds.FighterKit import Champion

		if char in Champion:
			need += 1
	return need


def Make_Fighting_Style(
		*,
		name: str,
		description: str,
		guilds: tuple[str, ...] | None = None,
		source: str = "Fighting Style",
		apply: Callable[[Any], None] | None = None,
		chips: tuple[tuple[str, str], ...] = (),
		) -> type[Fighting_Style_Feat]:
	"""Construct one Fighting Style feat Tag."""
	if not name or not name.strip():
		raise ValueError(
				"Make_Fighting_Style: name is required."
				)
	allowed = guilds
	resolved_chips = tuple(
			chips
			)
	style_tag = None

	@Pre
	def Fighting_Style_Feature(
			target,
			):
		return fighting_styles_known(
				target
				) > 0

	@Pre
	def Guild_Allowed(
			target,
			):
		if allowed is None:
			return True
		return getattr(
				target,
				"char_class",
				None,
				) in allowed

	@Imprint
	def Awaken(
			target,
			):
		if name in _owned_feat_names(
				target
				):
			return
		if apply is not None:
			apply(
					target
					)
		grant(
				target,
				name=name,
				description=description,
				source=source,
				level=1,
				chips=resolved_chips,
				)

	style_tag = type(
			_class_name(
					name
					),
			(
					Fighting_Style_Feat,
					),
			{
					"NAME": name,
					"GUILDS": Report_Of(
							allowed
							),
					"SOURCE": Report_Of(
							source
							),
					"Fighting_Style_Feature": Fighting_Style_Feature,
					"Guild_Allowed": Guild_Allowed,
					"Awaken": Awaken,
					"__module__": __name__,
					},
			)
	_FIGHTING_STYLE_DECLARATIONS.append(
			style_tag
			)
	return style_tag


def Make_General_Feat(
		*,
		name: str,
		description: str,
		min_level: int = 4,
		ability_any: tuple[str, ...] | None = None,
		ability_min: int = 13,
		requires_spellcasting: bool = False,
		requires_feat_any: tuple[str, ...] = (),
		requires_weapon_mastery: bool = False,
		redundant_if: Callable[[Any], bool] | None = None,
		repeatable: bool = False,
		asi: tuple[str, ...] | None = None,
		asi_amount: int = 1,
		asi_cap: int = 20,
		source: str = "Feat",
		apply: Callable[[Any], None] | None = None,
		training: (
			Callable[
				[Any, type[General_Feat]],
				Training_Batch,
				]
			| None
			) = None,
		training_record: str | None = None,
		describe_training: (
			Callable[[str, Training_Batch], str]
			| None
			) = None,
		) -> type[General_Feat]:
	"""
	Construct one General feat Tag.

	``requires_feat_any`` and ``requires_weapon_mastery`` declare the feat's
	own prerequisites and are satisfied by ANY declared route, matching how
	2024 prints them ("the X feat or Martial Weapon Proficiency").  Weapon
	Mastery stands in for martial-weapon training: it is the Tag the martial
	guilds drill, so membership marks a Character trained to carry them.

	``redundant_if`` is the other direction, and it exists because this is a
	generator rather than a character builder.  A player may legally take a
	feat that gives them something they already have; a generator that does so
	has simply wasted the pick and printed a line that grants nothing.  The
	rules do not forbid a Barbarian taking Lightly Armored, but nothing should
	ever hand one out.
	"""
	if not name or not name.strip():
		raise ValueError(
				"Make_General_Feat: name is required."
				)
	feat_tag = None
	resolved_training_record = (
		training_record
		or _class_name(
			name
			).casefold()
		)

	@Pre
	def Rank_Reached(
			target,
			):
		return int(
				getattr(
						target,
						"level",
						1,
						) or 1
				) >= min_level

	@Pre
	def Ability_Met(
			target,
			):
		if not ability_any:
			return True
		return any(
				_ability_score(
						target,
						key,
						) >= ability_min
				for key in ability_any
				)

	@Pre
	def Spellcasting_Met(
			target,
			):
		if not requires_spellcasting:
			return True
		return _has_spellcasting(
				target
				)

	@Pre
	def Not_Redundant(
			target,
			):
		if redundant_if is None:
			return True
		return not redundant_if(
				target
				)

	@Pre
	def Prerequisite_Met(
			target,
			):
		if not requires_feat_any and not requires_weapon_mastery:
			return True
		if requires_feat_any and set(
				requires_feat_any
				) & _owned_feat_names(
				target
				):
			return True
		if requires_weapon_mastery:
			from AtlasLusoris.Map_of_Weapon_Masteries import Weapon_Mastery
			return target in Weapon_Mastery
		return False

	@Imprint
	def Awaken(
			target,
			):
		if not repeatable and name in _owned_feat_names(
				target
				):
			return
		training_gain = (
			training(
				target,
				feat_tag,
				)
			if training is not None
			else None
			)

		if (
			training_gain is not None
			and training_gain.feature is not feat_tag
			):
			raise ValueError(
				f"{name} planned training for another Feature Tag."
				)

		raised: list[tuple[str, int]] = []
		if asi:
			key = _raise_one_of(
					target,
					asi,
					amount=asi_amount,
					cap=asi_cap,
					)
			if key:
				raised.append(
						(
								key,
								asi_amount,
								)
						)
		elif asi is None and name == "Ability Score Improvement":
			# Two +1s or one +2 — prefer two distinct scores under cap.
			first = _raise_any(
					target,
					amount=1,
					cap=asi_cap,
					)
			second = _raise_any(
					target,
					amount=1,
					cap=asi_cap,
					)
			if first:
				raised.append(
						(
								first,
								1,
								)
						)
			if second:
				raised.append(
						(
								second,
								1,
								)
						)
		if apply is not None:
			apply(
					target
					)

		if training_gain is not None:
			Commit_Training_Gain(
				target,
				training_gain,
				)

		resolved_description = description

		if (
			training_gain is not None
			and describe_training is not None
			):
			resolved_description = describe_training(
				description,
				training_gain,
				)

		grant(
			target,
			name=name,
			description=_sheet_feat_description(
				resolved_description,
				raised=raised,
				),
			source=source,
			level=min_level,
			)

	namespace = {
		"NAME": name,
		"MIN_LEVEL": Report_Of(
			min_level
			),
		"REPEATABLE": Report_Of(
			repeatable
			),
		"ABILITY_ANY": Report_Of(
			ability_any
			),
		"ABILITY_MIN": Report_Of(
			ability_min
			),
		"REQUIRES_SPELLCASTING": Report_Of(
			requires_spellcasting
			),
		"REQUIRES_FEAT_ANY": Report_Of(
			requires_feat_any
			),
		"REQUIRES_WEAPON_MASTERY": Report_Of(
			requires_weapon_mastery
			),
		"SOURCE": Report_Of(
			source
			),
		"Rank_Reached": Rank_Reached,
		"Ability_Met": Ability_Met,
		"Spellcasting_Met": Spellcasting_Met,
		"Prerequisite_Met": Prerequisite_Met,
		"Not_Redundant": Not_Redundant,
		"Awaken": Awaken,
		"__module__": __name__,
		}

	if training is not None:
		@Record
		def Feature_Training(
				target,
				) -> Feature_Training_Record:
			return New_Feature_Training_Record(
				target,
				feat_tag,
				)

		@Post
		def Has_Feature_Training(
				target,
				):
			return bool(
				getattr(
					target,
					resolved_training_record,
					).gains
				)

		namespace[ resolved_training_record ] = Feature_Training
		namespace[
			f"Has_{_class_name(name)}_Training"
			] = Has_Feature_Training

	feat_tag = type(
		_class_name(
			name
			),
		(
			General_Feat,
			),
		namespace,
		)
	_GENERAL_FEAT_DECLARATIONS.append(
			feat_tag
			)
	return feat_tag


def Make_Epic_Boon(
		*,
		name: str,
		description: str,
		asi: tuple[str, ...] | None = None,
		requires_spellcasting: bool = False,
		source: str = "Epic Boon",
		apply: Callable[[Any], None] | None = None,
		) -> type[Epic_Boon_Feat]:
	"""Construct one Epic Boon feat Tag."""
	if not name or not name.strip():
		raise ValueError(
				"Make_Epic_Boon: name is required."
				)
	boon_tag = None

	@Pre
	def Rank_Reached(
			target,
			):
		return int(
				getattr(
						target,
						"level",
						1,
						) or 1
				) >= 19

	@Pre
	def Spellcasting_Met(
			target,
			):
		if not requires_spellcasting:
			return True
		guild = getattr(
				target,
				"char_class",
				None,
				)
		return guild in {
				"Bard",
				"Cleric",
				"Druid",
				"Paladin",
				"Ranger",
				"Sorcerer",
				"Warlock",
				"Wizard",
				"Artificer",
				} or getattr(
				target,
				"subclass",
				None,
				) == "Eldritch Knight"

	@Imprint
	def Awaken(
			target,
			):
		if name in _owned_feat_names(
				target
				):
			return
		keys = asi or (
				"STR",
				"DEX",
				"CON",
				"INT",
				"WIS",
				"CHA",
				)
		key = _raise_one_of(
				target,
				keys,
				amount=1,
				cap=30,
				)
		raised = [
				(
						key,
						1,
						)
				] if key else []
		if apply is not None:
			apply(
					target
					)
		grant(
				target,
				name=name,
				description=_sheet_feat_description(
						description,
						raised=raised,
						),
				source=source,
				level=19,
				)

	boon_tag = type(
			_class_name(
					name
					),
			(
					Epic_Boon_Feat,
					),
			{
					"NAME": name,
					"REQUIRES_SPELLCASTING": Report_Of(
							requires_spellcasting
							),
					"SOURCE": Report_Of(
							source
							),
					"Rank_Reached": Rank_Reached,
					"Spellcasting_Met": Spellcasting_Met,
					"Awaken": Awaken,
					"__module__": __name__,
					},
			)
	_EPIC_BOON_DECLARATIONS.append(
			boon_tag
			)
	return boon_tag


def all_fighting_styles() -> tuple[type[Fighting_Style_Feat], ...]:
	return tuple(
			_FIGHTING_STYLE_DECLARATIONS
			)


def all_general_feats() -> tuple[type[General_Feat], ...]:
	return tuple(
			_GENERAL_FEAT_DECLARATIONS
			)


def all_epic_boons() -> tuple[type[Epic_Boon_Feat], ...]:
	return tuple(
			_EPIC_BOON_DECLARATIONS
			)


def available_fighting_styles(
		char,
		) -> list[type[Fighting_Style_Feat]]:
	if fighting_styles_known(
			char
			) <= 0:
		return []
	owned = _owned_feat_names(
			char
			)
	guild = getattr(
			char,
			"char_class",
			None,
			)
	found = []
	for tag in _FIGHTING_STYLE_DECLARATIONS:
		if tag.NAME in owned:
			continue
		allowed = getattr(
				tag,
				"GUILDS",
				None,
				)
		if allowed is not None and guild not in allowed:
			continue
		found.append(
				tag
				)
	return found


def _has_spellcasting(
		char,
		) -> bool:
	guild = getattr(
			char,
			"char_class",
			None,
			)
	if guild in {
			"Bard",
			"Cleric",
			"Druid",
			"Paladin",
			"Ranger",
			"Sorcerer",
			"Warlock",
			"Wizard",
			"Artificer",
			}:
		return True
	specialization = getattr(
			char,
			"specialization",
			None,
			) or getattr(
			char,
			"subclass",
			None,
			)

	return specialization in {
		"Eldritch Knight",
		"Arcane Trickster",
		}


def available_general_feats(
		char,
		) -> list[type[General_Feat]]:
	owned = _owned_feat_names(
			char
			)
	level = int(
			getattr(
					char,
					"level",
					1,
					) or 1
			)
	found = []
	for tag in _GENERAL_FEAT_DECLARATIONS:
		min_level = int(
				getattr(
						tag,
						"MIN_LEVEL",
						4,
						) or 4
				)
		if level < min_level:
			continue
		repeatable = bool(
				getattr(
						tag,
						"REPEATABLE",
						False,
						)
				)
		if not repeatable and tag.NAME in owned:
			continue
		ability_any = getattr(
				tag,
				"ABILITY_ANY",
				None,
				)
		ability_min = int(
				getattr(
						tag,
						"ABILITY_MIN",
						13,
						) or 13
				)
		if ability_any and not any(
				_ability_score(
						char,
						key,
						) >= ability_min
				for key in ability_any
				):
			continue
		if getattr(
				tag,
				"REQUIRES_SPELLCASTING",
				False,
				) and not _has_spellcasting(
				char
				):
			continue
		requires_feat_any = getattr(
				tag,
				"REQUIRES_FEAT_ANY",
				(),
				) or ()
		requires_weapon_mastery = bool(
				getattr(
						tag,
						"REQUIRES_WEAPON_MASTERY",
						False,
						)
				)
		if requires_feat_any or requires_weapon_mastery:
			met = bool(
					set(
							requires_feat_any
							) & owned
					)
			if not met and requires_weapon_mastery:
				from AtlasLusoris.Map_of_Weapon_Masteries import Weapon_Mastery
				met = char in Weapon_Mastery
			if not met:
				continue
		found.append(
				tag
				)
	return found


def available_epic_boons(
		char,
		) -> list[type[Epic_Boon_Feat]]:
	owned = _owned_feat_names(
			char
			)
	if int(
			getattr(
					char,
					"level",
					1,
					) or 1
			) < 19:
		return []
	found = []
	for tag in _EPIC_BOON_DECLARATIONS:
		if tag.NAME in owned:
			continue
		if getattr(
				tag,
				"REQUIRES_SPELLCASTING",
				False,
				) and not _has_spellcasting(
				char
				):
			continue
		found.append(
				tag
				)
	return found


def _take_first_that_applies(
		char,
		pool,
		applied,
		):
	"""Apply the first candidate whose own Preconditions accept the Character."""
	chosen = char.Accept(
			pool,
			in_order=True,
			)
	applied.append(
			chosen
			)
	return True


def _stable_available(
		char,
		declarations,
		available,
		bag_purpose: str,
		):
	"""Order a changing eligible pool from one stable declaration order."""
	ordered = sorted(
		declarations,
		key=lambda tag: tag.NAME,
		)
	char.Dice_Bag(
		bag_purpose,
		version="2024",
		namespace="GenLegendFeat",
		).shuffle(
			ordered
			)
	eligible = set(
		available
		)
	return [
		tag
		for tag in ordered
		if tag in eligible
		]


def Apply_Fighting_Styles(
		char,
		n: int | None = None,
		) -> list[type[Fighting_Style_Feat]]:
	"""Grant Fighting Style feats up to the Character's known count."""
	need = fighting_styles_known(
			char
			) if n is None else n
	owned = [
			tag
			for tag in _FIGHTING_STYLE_DECLARATIONS
			if char in tag or tag.NAME in _owned_feat_names(
					char
					)
			]
	applied = list(
			owned
			)
	while len(
			applied
			) < need:
		pool = _stable_available(
			char,
			_FIGHTING_STYLE_DECLARATIONS,
			available_fighting_styles(
					char
					),
			"feat.fighting_style",
				)
		if not pool:
			break
		pick = char.Accept(
				pool,
				in_order=True,
				)
		if pick.NAME in _owned_feat_names(
				char
				) and pick not in applied:
			applied.append(
					pick
					)
		else:
			break
	return applied


def Apply_General_Feats(
		char,
		n: int = 1,
		) -> list[type[General_Feat]]:
	"""Pick ``n`` General feats (ASI replacements)."""
	applied: list[type[General_Feat]] = []
	for _ in range(
			max(
					0,
					n,
					)
			):
		pool = _stable_available(
			char,
			_GENERAL_FEAT_DECLARATIONS,
			available_general_feats(
					char
					),
			"feat.general",
				)
		if not pool:
			break
		_take_first_that_applies(
				char,
				pool,
				applied,
				)
	return applied


def Apply_Epic_Boons(
		char,
		n: int = 1,
		) -> list[type[Epic_Boon_Feat]]:
	"""Pick ``n`` Epic Boon feats."""
	applied: list[type[Epic_Boon_Feat]] = []
	for _ in range(
			max(
					0,
					n,
					)
			):
		pool = _stable_available(
			char,
			_EPIC_BOON_DECLARATIONS,
			available_epic_boons(
					char
					),
			"feat.epic_boon",
				)
		if not pool:
			break
		pick = char.Accept(
				pool,
				in_order=True,
				)
		applied.append(
				pick
				)
	return applied


def _load_feat_maps() -> None:
	import importlib
	importlib.import_module(
			"AtlasLusoris.AtlasOfFeats.Map_of_Fighting_Styles"
			)
	importlib.import_module(
			"AtlasLusoris.AtlasOfFeats.Map_of_General_Feats"
			)
	importlib.import_module(
			"AtlasLusoris.AtlasOfFeats.Map_of_Epic_Boons"
			)


def _self_test():
	from AtlasLusoris.GuildKit import Apply_Guild

	assert len(
			all_fighting_styles()
			) >= 10
	assert len(
			all_general_feats()
			) >= 40
	assert len(
			all_epic_boons()
			) >= 12

	fighter = Character(
			seed=2
			)
	fighter.level = 5
	fighter.char_class = "Fighter"
	fighter.subclass = "Champion"
	Apply_Guild(
			fighter
			)
	styles = Apply_Fighting_Styles(
			fighter
			)
	assert len(
			styles
			) >= 1
	feats = Apply_General_Feats(
			fighter,
			n=2,
			)
	assert len(
			feats
			) == 2

	warlock = Character(
			seed=3
			)
	warlock.level = 19
	warlock.char_class = "Warlock"
	Apply_Guild(
			warlock
			)
	boons = Apply_Epic_Boons(
			warlock,
			n=1,
			)
	assert len(
			boons
			) == 1
	print(
			"OK — FeatKit self-test:",
			[tag.NAME for tag in styles],
			[tag.NAME for tag in feats],
			[tag.NAME for tag in boons],
			)


if __name__ == "__main__":
	from AtlasLusoris.FeatKit import _self_test as _package_self_test
	_package_self_test()
else:
	_load_feat_maps()
