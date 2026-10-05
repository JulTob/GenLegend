"""
FeatKit

TOP catalogues for Fighting Style feats, General feats, and Epic Boons.
Origin feats stay in FeaturesKit; Invocations stay in InvocationKit.

The catalogue is the Field of the ``Declared_Feat`` Pin: each factory builds
its feat Tag with only its behaviour and pins it, and the three families are
that one Field read by root.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from TopKit import Imprint, Pin, Post, Pre, Record, Tag

from AtlasVenustas import Chip

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


_FEAT_ROOTS = (
		Fighting_Style_Feat,
		General_Feat,
		Epic_Boon_Feat,
		)


def _distinct_names(
		values,
		what: str,
		) -> tuple[str, ...]:
	"""A tuple of distinct, non-empty names, or the ValueError naming ``what``."""
	resolved = tuple(
			values or ()
			)
	if any(
			not isinstance(
					value,
					str,
					)
			or not value.strip()
			for value in resolved
			):
		raise ValueError(
				f"{what} must be non-empty strings, not {resolved!r}."
				)
	if len(
			set(
					resolved
					)
			) != len(
					resolved
					):
		raise ValueError(
				f"{what} cannot list one entry twice: {resolved!r}."
				)
	return resolved


def _yes_or_no(
		value,
		what: str,
		) -> bool:
	if not isinstance(
			value,
			bool,
			):
		raise ValueError(
				f"{what} must be True or False, not {value!r}."
				)
	return value


def _positive_integer(
		value,
		what: str,
		) -> int:
	if (
		isinstance(
				value,
				bool,
				)
		or not isinstance(
				value,
				int,
				)
		or value < 1
		):
		raise ValueError(
				f"{what} must be a positive integer, not {value!r}."
				)
	return value


@Pin
class Declared_Feat(Tag):
	"""
	Root Pin for the feats this Kit catalogues.

	A feat is catalogued by applying this Pin *to the feat Tag*, and
	``Declared_Feat[:]`` is then the catalogue, in declaration order.  The
	three families are that one Field read by root: ``all_fighting_styles``,
	``all_general_feats`` and ``all_epic_boons`` each filter it on their own
	root Tag, so nothing is listed twice and a new feat is real the moment
	its factory pins it.

	The constants the factories used to write into a class namespace are
	Records here.  Each is validated once, at the pin, and lands on the feat
	Tag as a Report (``Archery.GUILDS``, ``Chef.MIN_LEVEL``).  A Record whose
	input the pin does not give keeps its default.
	"""

	@Pre
	def Feat_Tag_Only(
			target,
			):
		return (
			isinstance(
					target,
					type,
					)
			and issubclass(
					target,
					_FEAT_ROOTS,
					)
			and target not in _FEAT_ROOTS
			)

	@Record
	def GUILDS(
			target,
			*,
			guilds=None,
			) -> tuple[str, ...] | None:
		"""Guild names allowed the feat; None leaves every Guild in."""
		if guilds is None:
			return None
		return _distinct_names(
				guilds,
				"Feat Guild names",
				)

	@Record
	def SOURCE(
			target,
			*,
			source=None,
			) -> str:
		if (
			not isinstance(
					source,
					str,
					)
			or not source.strip()
			):
			raise ValueError(
					f"A feat source must be non-empty text, not {source!r}."
					)
		return source

	@Record
	def MIN_LEVEL(
			target,
			*,
			min_level=None,
			) -> int | None:
		"""
		The level floor a General feat declares.

		Fighting Styles and Epic Boons gate their level in their factory
		and declare none here, so the Report stays None for them.
		"""
		if min_level is None:
			return None
		return _positive_integer(
				min_level,
				"A feat minimum level",
				)

	@Record
	def REPEATABLE(
			target,
			*,
			repeatable=False,
			) -> bool:
		return _yes_or_no(
				repeatable,
				"REPEATABLE",
				)

	@Record
	def ABILITY_ANY(
			target,
			*,
			ability_any=None,
			) -> tuple[str, ...] | None:
		"""Ability keys of which one must reach ABILITY_MIN; None asks nothing."""
		if ability_any is None:
			return None
		resolved = _distinct_names(
				ability_any,
				"Feat ability prerequisites",
				)
		unknown = tuple(
				key
				for key in resolved
				if key not in _ABILITY_FULL
				)
		if unknown:
			raise ValueError(
					f"Feat ability prerequisites name no ability: {unknown!r}; "
					f"expected keys among {tuple( _ABILITY_FULL )!r}."
					)
		return resolved

	@Record
	def ABILITY_MIN(
			target,
			*,
			ability_min=13,
			) -> int:
		return _positive_integer(
				ability_min,
				"A feat ability minimum",
				)

	@Record
	def REQUIRES_SPELLCASTING(
			target,
			*,
			requires_spellcasting=False,
			) -> bool:
		return _yes_or_no(
				requires_spellcasting,
				"REQUIRES_SPELLCASTING",
				)

	@Record
	def REQUIRES_FEAT_ANY(
			target,
			*,
			requires_feat_any=(),
			) -> tuple[str, ...]:
		"""Feat NAMEs of which owning any one satisfies the prerequisite."""
		return _distinct_names(
				requires_feat_any,
				"Feat prerequisite feat names",
				)

	@Record
	def REQUIRES_WEAPON_MASTERY(
			target,
			*,
			requires_weapon_mastery=False,
			) -> bool:
		return _yes_or_no(
				requires_weapon_mastery,
				"REQUIRES_WEAPON_MASTERY",
				)


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
		chips: tuple[Chip, ...] = (),
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
					"Fighting_Style_Feature": Fighting_Style_Feature,
					"Guild_Allowed": Guild_Allowed,
					"Awaken": Awaken,
					"__module__": __name__,
					},
			)
	Declared_Feat(
			style_tag,
			guilds=allowed,
			source=source,
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
	Declared_Feat(
		feat_tag,
		min_level=min_level,
		repeatable=repeatable,
		ability_any=ability_any,
		ability_min=ability_min,
		requires_spellcasting=requires_spellcasting,
		requires_feat_any=requires_feat_any,
		requires_weapon_mastery=requires_weapon_mastery,
		source=source,
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
					"Rank_Reached": Rank_Reached,
					"Spellcasting_Met": Spellcasting_Met,
					"Awaken": Awaken,
					"__module__": __name__,
					},
			)
	Declared_Feat(
			boon_tag,
			requires_spellcasting=requires_spellcasting,
			source=source,
			)
	return boon_tag


def _feats_of_kind(
		root,
		) -> tuple:
	"""One family of the catalogue: the Field, read by its root Tag."""
	return tuple(
			tag
			for tag in Declared_Feat[:]
			if issubclass(
					tag,
					root,
					)
			)


def all_fighting_styles() -> tuple[type[Fighting_Style_Feat], ...]:
	"""Every declared Fighting Style feat, in declaration order."""
	return _feats_of_kind(
			Fighting_Style_Feat
			)


def all_general_feats() -> tuple[type[General_Feat], ...]:
	"""Every declared General feat, in declaration order."""
	return _feats_of_kind(
			General_Feat
			)


def all_epic_boons() -> tuple[type[Epic_Boon_Feat], ...]:
	"""Every declared Epic Boon, in declaration order."""
	return _feats_of_kind(
			Epic_Boon_Feat
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
	for tag in all_fighting_styles():
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
	for tag in all_general_feats():
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
	for tag in all_epic_boons():
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
			for tag in all_fighting_styles()
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
			all_fighting_styles(),
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
			all_general_feats(),
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
			all_epic_boons(),
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

	#-- QST-0144.5: the catalogue is the Pin's Field.  Each family is that
	#-- Field read by root, in the order its Map declares it (the order the
	#-- registry lists kept), every pinned Tag is in exactly one family, and
	#-- the roots themselves are not catalogued.
	from AtlasLusoris.AtlasOfFeats import Map_of_Epic_Boons
	from AtlasLusoris.AtlasOfFeats import Map_of_Fighting_Styles
	from AtlasLusoris.AtlasOfFeats import Map_of_General_Feats
	from TopKit import TagCompositionError

	def declared_in(
			module,
			root,
			):
		return tuple(
				dict.fromkeys(
						value
						for value in vars(
								module
								).values()
						if (
							isinstance(
									value,
									type,
									)
							and issubclass(
									value,
									root,
									)
							and value is not root
							)
						)
				)

	assert all_fighting_styles() == declared_in(
			Map_of_Fighting_Styles,
			Fighting_Style_Feat,
			)
	assert all_general_feats() == declared_in(
			Map_of_General_Feats,
			General_Feat,
			)
	assert all_epic_boons() == declared_in(
			Map_of_Epic_Boons,
			Epic_Boon_Feat,
			)
	assert len(
			Declared_Feat[:]
			) == (
			len( all_fighting_styles() )
			+ len( all_general_feats() )
			+ len( all_epic_boons() )
			)
	assert not any(
			root in Declared_Feat
			for root in _FEAT_ROOTS
			)

	#-- The constants the factories wrote are Reports now, with the values
	#-- the Maps declare, and a default where a Map says nothing.
	assert Map_of_Fighting_Styles.Archery.GUILDS is None
	assert Map_of_Fighting_Styles.Archery.SOURCE == "Fighting Style"
	assert Map_of_Fighting_Styles.BlessedWarrior.GUILDS == (
			"Paladin",
			)
	assert Map_of_General_Feats.Grappler.MIN_LEVEL == 4
	assert Map_of_General_Feats.Grappler.ABILITY_ANY == (
			"STR",
			"DEX",
			)
	assert Map_of_General_Feats.Grappler.ABILITY_MIN == 13
	assert Map_of_General_Feats.Grappler.SOURCE == "Feat"
	assert Map_of_General_Feats.ElementalAdept.REPEATABLE is True
	assert Map_of_General_Feats.ElementalAdept.REQUIRES_SPELLCASTING is True
	assert Map_of_General_Feats.FieldMarshal.REQUIRES_FEAT_ANY == (
			"Field Lieutenant",
			"Martial Weapon Training",
			)
	assert Map_of_General_Feats.FieldMarshal.REQUIRES_WEAPON_MASTERY is True
	assert Map_of_Epic_Boons.BoonOfFate.SOURCE == "Epic Boon"
	assert Map_of_Epic_Boons.BoonOfFate.REQUIRES_SPELLCASTING is False
	assert all(
			tag.MIN_LEVEL is None
			for tag in all_fighting_styles() + all_epic_boons()
			)

	#-- A declaration the Records refuse never joins the Field.
	catalogued = tuple(
			Declared_Feat[:]
			)
	try:
		Make_General_Feat(
				name="Unfounded",
				description="A feat with no level floor at all.",
				min_level=0,
				)
	except TagCompositionError:
		pass
	else:
		raise AssertionError(
				"Declared_Feat accepted a General feat with min_level=0."
				)
	assert tuple(
			Declared_Feat[:]
			) == catalogued

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
	#-- The accessors answer as they did before the port (QST-0144.5):
	#-- the same picks for the same seeds.
	assert [
			tag.NAME
			for tag in styles
			] == [
			"Interception",
			]
	assert [
			tag.NAME
			for tag in feats
			] == [
			"Skill Expert",
			"Martial Weapon Training",
			]
	assert [
			tag.NAME
			for tag in boons
			] == [
			"Boon of Recovery",
			]
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
