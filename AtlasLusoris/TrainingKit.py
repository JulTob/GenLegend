"""
TrainingKit

Training Tags are Guild class features — lessons learned by training
in a Guild.  Distinct from Origin Feats, Species Traits, and Invocations.

Thought pattern (read this before the code)
	1. You join a Guild (GuildKit chassis + helpers).
	2. As you gain levels in that Guild, Training Tags awaken.
	3. Each Training is a Tag: semantic membership, plus what it prints
	   as class data (Decree 0009, QST-0142 station 3): one ``ENTRIES``
	   Entry in the Guild section at its ``MIN_LEVEL``, and its ``CHIPS``.
	   The sheet reads them through ``Find_Build``; nothing is written to
	   ``char.features``.  Its table constants (``GUILD_NAME``,
	   ``MIN_LEVEL``, ``PATH``, ``SOURCE``) are Records of the
	   ``Declared_Lesson`` Pin, landed on the Tag as Reports, and the
	   catalogue is that Pin's Field: ``Declared_Lesson[:]``.
	4. Subclass lessons stay out until a later pass — core Guild
	   Trainings first (reference: Fighter Second Wind).

Usage
	from AtlasLusoris.TrainingKit import Second_Wind, Apply_Guild_Trainings
	Apply_Guild(char)           # Fighter
	Apply_Guild_Trainings(char) # stamps Second_Wind, …
	assert char in Second_Wind
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from TopKit import Imprint, Pin, Pre, Record, Tag

from AtlasActorLudi.CharactersKit import Character
from AtlasVenustas import Chip
from AtlasVenustas import Entry
from AtlasVenustas import Section


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


class Training(Tag):
	"""
	A lesson from Guild training (D&D class feature).

	Concrete Trainings carry GUILD_NAME, MIN_LEVEL, PATH and SOURCE as
	Reports, landed by the ``Declared_Lesson`` Pin below.
	"""

	NAME = "Training"

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)

	@Pre
	def Trained_In_Guild(
			target,
			):
		"""Concrete Trainings override; root accepts any Character."""
		return True

	@Imprint
	def Ensure_Feature_Bag(
			target,
			):
		if getattr(
				target,
				"features",
				None,
				) is None:
			target.features = []


@Pin
class Declared_Lesson(Tag):
	"""
	Pin for the Training Tags known to the generator.

	``Make_Training`` applies it to every lesson it builds, so the
	catalogue is this Pin's Field, ``Declared_Lesson[:]``, in declaration
	order: no list is kept beside the Maps, and a lesson is discoverable
	the moment it is declared.  Its Records land on the lesson as Reports,
	readable on the Tag and never on the Character; that is what lets
	``PATH`` hold a Tag class, which as plain class data would have become
	an Action.
	"""

	@Pre
	def Training_Tag_Only(
			target,
			):
		return (
			isinstance(
					target,
					type,
					)
			and issubclass(
					target,
					Training,
					)
			and target is not Training
			)

	@Record
	def GUILD_NAME(
			target,
			*,
			guild_name=None,
			) -> str:
		if (
			not isinstance(
					guild_name,
					str,
					)
			or not guild_name.strip()
			):
			raise ValueError(
					f"{target.__name__}: guild_name must be a non-empty "
					"Guild name."
					)
		return guild_name

	@Record
	def MIN_LEVEL(
			target,
			*,
			min_level=1,
			) -> int:
		if (
			isinstance(
					min_level,
					bool,
					)
			or not isinstance(
					min_level,
					int,
					)
			or min_level < 1
			):
			raise ValueError(
					f"{target.__name__}: min_level must be an integer of "
					"at least 1."
					)
		return min_level

	@Record
	def PATH(
			target,
			*,
			path=None,
			) -> str | type[Tag] | None:
		if path is None:
			return None
		if (
			isinstance(
					path,
					type,
					)
			and issubclass(
					path,
					Tag,
					)
			):
			return path
		resolved = str(
				path
				).strip()
		if not resolved:
			raise ValueError(
					f"{target.__name__}: path, if set, must be a Tag or "
					"a non-empty legacy name."
					)
		return resolved

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
					f"{target.__name__}: source must be a non-empty string."
					)
		return source


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


def level_in_guild(
		char,
		guild_name: str,
		) -> int:
	"""
	How deep the Character has trained in this Guild.

	Single-class Characters use ``char.level``.
	Multiclass Characters prefer ``char.guild_levels``.
	"""
	from AtlasLusoris.GuildKit import (
			Multiclassed,
			guilds_on,
			)

	levels = getattr(
			char,
			"guild_levels",
			None,
			)
	if not isinstance(
			levels,
			dict,
			):
		levels = {}

	primary = getattr(
			char,
			"char_class",
			None,
			)
	character_level = int(
			getattr(
					char,
					"level",
					1,
					) or 1
			)

	if primary == guild_name and char not in Multiclassed:
		return max(
				character_level,
				int(
						levels.get(
								guild_name,
								0,
								)
						),
				)

	if guild_name in levels:
		return int(
				levels[guild_name]
				)

	if primary == guild_name:
		# Multiclassed primary without a ledger entry — fall back to level.
		others = sum(
				int(
						levels.get(
								tag.NAME,
								0,
								)
						)
				for tag in guilds_on(
						char
						)
				if tag.NAME != guild_name
				)
		return max(
				1,
				character_level - others,
				)

	return 0


def Make_Training(
		*,
		name: str,
		guild_name: str,
		min_level: int = 1,
		description: str | Callable[[Any], str] = "",
		chips: Iterable[Chip] = (),
		source: str | None = None,
		apply: Callable[[Any], None] | None = None,
		path: str | type[Tag] | None = None,
		on_sheet: bool = True,
		) -> type[Training]:
	"""
	Construct one Training Tag for a Guild lesson.

	``description`` and chip values may be callables resolved at awaken
	time so numbers (uses, masteries) stay on the Character, not the Tag.

	``path`` gates subclass lessons (e.g. Barbarian Path ``"Berserker"``).
	Core Guild lessons leave ``path`` unset.

	``on_sheet=False`` still awakens the Tag (for identity / Pre gates)
	but skips the Feature Entry — use when another section owns the prose
	(Spellcasting → Spells) or a FeatKit grant names the pick
	(Fighting Style → Archery, …).

	The Tag is built with its behaviour only (gates, Imprint, ``NAME``,
	``ENTRIES``, ``CHIPS``) and then pinned with ``Declared_Lesson``, whose
	Records validate ``guild_name``, ``min_level``, ``path`` and ``source``
	and land them on the Tag as Reports.
	"""
	if not name or not name.strip():
		raise ValueError(
				"Make_Training: name is required."
				)

	resolved_path = path
	if (
		resolved_path is not None
		and not (
			isinstance(
					resolved_path,
					type,
					)
			and issubclass(
					resolved_path,
					Tag,
					)
			)
		):
		resolved_path = str(
			resolved_path
			).strip()
	path_name = (
		resolved_path.NAME
		if (
			isinstance(
					resolved_path,
					type,
					)
			and issubclass(
					resolved_path,
					Tag,
					)
			)
		else resolved_path
		)
	has_path = (
			resolved_path is not None
			and resolved_path != ""
			)
		#-- Never `if resolved_path:`.  A path may be a Tag, and TopKit's
		#-- ``bool( Tag )`` asks whether the Tag has members yet, which at
		#-- import time is always no.
	if has_path and source is None:
		resolved_source = f"Training: {guild_name} ({path_name})"
	else:
		resolved_source = source or f"Training: {guild_name}"
	resolved_chips = tuple(
			chips
			)

	@Pre
	def Trained_In_Guild(
			target,
			):
		from AtlasLusoris.GuildKit import GUILDS
		guild = GUILDS.get(
				guild_name
				)
		if guild is None:
			return False
		return target in guild

	@Pre
	def Rank_Reached(
			target,
			):
		return level_in_guild(
				target,
				guild_name,
				) >= min_level

	@Pre
	def Path_Matched(
			target,
			):
		if resolved_path is None:
			return True
		if (
			isinstance(
					resolved_path,
					type,
					)
			and issubclass(
					resolved_path,
					Tag,
					)
			):
			return target in resolved_path
		return getattr(
				target,
				"subclass",
				None,
				) == resolved_path

	@Imprint
	def Awaken(
			target,
			):
		_awaken_training(
				target,
				apply,
				)

	namespace = {
			"NAME": name,
			"ENTRIES": Training_Entries(
					name,
					description,
					min_level,
					on_sheet,
					),
			"CHIPS": Training_Chips(
					name,
					resolved_chips,
					on_sheet,
					),
			"Trained_In_Guild": Trained_In_Guild,
			"Rank_Reached": Rank_Reached,
			"Path_Matched": Path_Matched,
			"Awaken": Awaken,
			"__module__": __name__,
			}

	training_tag = type(
			_class_name(
					name
					),
			(
					Training,
					),
			namespace,
			)

	Declared_Lesson(
			training_tag,
			guild_name=guild_name,
			min_level=min_level,
			path=resolved_path,
			source=resolved_source,
			)
	return training_tag


def training_path(
		training: type[Training],
		) -> str | type[Tag] | None:
	path = getattr(
			training,
			"PATH",
			None,
			)
	if path is None or path == "":
		return None
	if (
		isinstance(
				path,
				type,
				)
		and issubclass(
				path,
				Tag,
				)
		):
		return path
	return str(
		path
		)


def training_eligible(
		char,
		training: type[Training],
		) -> bool:
	"""Guild rank and optional Path both match."""
	if level_in_guild(
			char,
			training.GUILD_NAME,
			) < training.MIN_LEVEL:
		return False
	path = training_path(
			training
			)
	if path is None:
		return True
	if (
		isinstance(
				path,
				type,
				)
		and issubclass(
				path,
				Tag,
				)
		):
		return char in path
	return getattr(
		char,
		"subclass",
			None,
			) == path


def _resolve(
		value: Any,
		char,
		) -> Any:
	if callable(
			value
			):
		return value(
				char
				)
	return value


OFF_SHEET_TRAININGS = frozenset(
		(
				"Spellcasting",
				"Fighting Style",
				"Additional Fighting Style",
				"Pact Magic",
				)
		)
	#-- These Tags awaken for identity and gates, but another surface owns
	#-- their prose (the Spells section, the Fighting Style feat pick).


def _awaken_training(
		char,
		apply,
		) -> None:
	"""Run the lesson's side effects once, when its Tag is applied."""
	if apply is not None:
		apply(
				char
				)


def Training_Entries(
		name: str,
		description,
		min_level: int,
		on_sheet: bool,
		) -> tuple[Entry, ...]:
	"""
	What a Training prints in the Guild section: one Entry, or none.

	``description`` may be a reader of the Character. The build resolves
	it when the sheet is read, not when the Training awakens, because
	Trainings awaken in level order and a level-20 capstone can still change
	the numbers a level-14 Entry quotes.
	"""
	if not on_sheet or name in OFF_SHEET_TRAININGS:
		return ()
	return (
			Entry(
					name,
					description,
					section=Section.GUILD,
					level=min_level,
					),
			)


def Training_Chips(
		name: str,
		chips: tuple[Chip, ...],
		on_sheet: bool,
		) -> tuple[Chip, ...]:
	"""What a Training puts on the rail: its Chips, unless it is off the sheet."""
	if not on_sheet or name in OFF_SHEET_TRAININGS:
		return ()
	return chips


def trainings_for(
		guild_name: str,
		) -> tuple[type[Training], ...]:
	"""All Training Tags declared for one Guild, by min level."""
	found = [
			tag
			for tag in Declared_Lesson[:]
			if tag.GUILD_NAME == guild_name
			]
	found.sort(
			key=lambda tag: (
					tag.MIN_LEVEL,
					tag.NAME,
					)
			)
	return tuple(
			found
			)


def training_covers(
		guild_name: str,
		training_name: str,
		) -> bool:
	"""True when a TOP Training owns this lesson (legacy Maps may skip)."""
	return any(
			tag.NAME == training_name
			for tag in trainings_for(
					guild_name
					)
			)


def has_training_catalogue(
		guild_name: str,
		) -> bool:
	return bool(
			trainings_for(
					guild_name
					)
			)


def covered_training_names(
		char,
		) -> set[str]:
	"""
	Lesson names this Character can already receive from TOP Training.
	Legacy Progression should skip these to avoid duplicate sheet lines.
	Path-gated lessons only cover when the Path matches.
	"""
	from AtlasLusoris.GuildKit import guilds_on

	names: set[str] = set()
	guild_names = {
			tag.NAME
			for tag in guilds_on(
					char
					)
			}
	primary = getattr(
			char,
			"char_class",
			None,
			)
	if primary:
		guild_names.add(
				primary
				)
	for guild_name in guild_names:
		for training in trainings_for(
				guild_name
				):
			if not training_eligible(
					char,
					training,
					):
				continue
			names.add(
					training.NAME
					)
	return names


def filter_legacy_features(
		char,
		features: Iterable,
		) -> list:
	"""Drop legacy Features already covered by Training or Guild description."""
	covered = covered_training_names(
			char
			)
	specialization = getattr(
			char,
			"specialization",
			None,
			)
	# GuildKit Specializations publish the patron voice via ``extends=`` /
	# ``heading=`` into the composed Guild Entry. Legacy Map_of_Classes
	# Training still emits a second "{Patron} Patron" blurbs with the old
	# "Your pact draws on…" text — drop those so Julio's transcription wins.
	patron_heading = (
		f"{specialization} Patron"
		if specialization
		else None
		)
	kept = []
	for feat in features:
		name = getattr(
				feat,
				"name",
				None,
				)
		if name in covered:
			continue
		if patron_heading and name == patron_heading:
			continue
		kept.append(
				feat
				)
	return kept


def Apply_Guild_Trainings(
		char,
		) -> list[type[Training]]:
	"""
	Awaken every Training the Character has earned in their Guilds.

	Safe to call when a Guild has no catalogue yet — returns [].
	"""
	from AtlasLusoris.GuildKit import guilds_on

	applied: list[type[Training]] = []
	guild_names = {
			tag.NAME
			for tag in guilds_on(
					char
					)
			}
	# Primary string fallback before Guild Tag stamp (defensive).
	primary = getattr(
			char,
			"char_class",
			None,
			)
	if primary:
		guild_names.add(
				primary
				)

	# Hot-reload / long-lived app workers can import TrainingKit before a
	# Guild's Map lands. Reload catalogues once if a known Guild is empty.
	for guild_name in sorted(
			guild_names
			):
		if guild_name and not trainings_for(
				guild_name
				) and guild_name in {
						"Artificer",
						"Barbarian",
						"Bard",
						"Cleric",
						"Druid",
						"Fighter",
						"Monk",
						"Paladin",
						"Ranger",
						"Rogue",
						"Sorcerer",
						"Warlock",
						"Wizard",
						}:
			_load_training_maps()
			break

	for guild_name in sorted(
			guild_names
			):
		for training in trainings_for(
				guild_name
				):
			if not training_eligible(
					char,
					training,
					):
				continue
			if char not in training:
				training(
						char
						)
			if char in training:
				applied.append(
						training
						)
	return applied


# ---------------------------------------------------------------------------
# Catalogue Maps declare here
# ---------------------------------------------------------------------------

_TRAINING_MAP_MODULES = (
		"Map_of_Artificer_Training",
		"Map_of_Barbarian_Training",
		"Map_of_Bard_Training",
		"Map_of_Cleric_Training",
		"Map_of_Druid_Training",
		"Map_of_Fighter_Training",
		"Map_of_Monk_Training",
		"Map_of_Paladin_Training",
		"Map_of_Ranger_Training",
		"Map_of_Rogue_Training",
		"Map_of_Sorcerer_Training",
		"Map_of_Warlock_Training",
		"Map_of_Wizard_Training",
		)


def _load_training_maps() -> None:
	# Local import keeps GuildKit free of TrainingKit at import time.
	import importlib

	for module_name in _TRAINING_MAP_MODULES:
		importlib.import_module(
				f"AtlasLusoris.AtlasOfTraining.{module_name}"
				)


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def Built_Titles(
		char,
		) -> list[str]:
	"""The titles of the Guild Entries the Character's build prints."""
	from AtlasActorLudi.Charts_of_Build import Find_Build
	return [
			built.entry.title
			for built in Find_Build( char ).entries
			if built.entry.section is Section.GUILD
			]


def Built_Chip_Values(
		char,
		tag: type[Training],
		) -> dict:
	"""One Training's Chips, read now, as label → value."""
	from AtlasActorLudi.Charts_of_Build import Find_Build
	return {
			built.chip.label: built.chip.value
			for built in Find_Build( char ).chips
			if built.tag is tag
			}


def Lessons_By_Map() -> tuple[type[Training], ...]:
	"""
	Every lesson the Maps hold by name.

	The catalogue read the long way round, Map by Map and name by name.
	The self-test holds the Pin Field against it: the Field holds nothing
	the Maps do not name, and the Maps name nothing the Field lacks.
	"""
	import sys

	found: list[type[Training]] = []
	for module_name in _TRAINING_MAP_MODULES:
		module = sys.modules[
				f"AtlasLusoris.AtlasOfTraining.{module_name}"
				]
		for value in vars(
				module
				).values():
			if (
				isinstance(
						value,
						type,
						)
				and issubclass(
						value,
						Training,
						)
				and value is not Training
				and value not in found
				):
				found.append(
						value
						)
	return tuple(
			found
			)


def _self_test():
	import gc

	from AtlasLusoris.GuildKit import (
			Apply_Guild,
			GUILDS,
			)
	from AtlasLusoris.AtlasOfTraining.Map_of_Fighter_Training import (
			Combat_Superiority,
			Second_Wind,
			Weapon_Mastery,
			)

	gc.collect()
		#-- The Field holds its Tags weakly.  The Maps hold every lesson by
		#-- name, so a collection must take nothing from the catalogue.
	lessons = tuple(
			Training.__subclasses__()
			)
		#-- Every Training ever built, in build order: what the registry
		#-- list used to hold.  Build order follows the import graph (a Map's
		#-- own imports can land another Map first), not the Map list.
	assert lessons
	assert tuple(
			Declared_Lesson[:]
			) == lessons
		#-- The Field is the old catalogue, in order.
	assert set(
			Lessons_By_Map()
			) == set(
					lessons
					)
		#-- Each lesson is named by its Map; none is built outside one.
	assert all(
			tag in Declared_Lesson
			for tag in lessons
			)
	assert Training not in Declared_Lesson

	for guild_name in GUILDS:
		expected = tuple(
				sorted(
						(
							tag
							for tag in lessons
							if tag.GUILD_NAME == guild_name
							),
						key=lambda tag: (
								tag.MIN_LEVEL,
								tag.NAME,
								),
						)
				)
		assert trainings_for(
				guild_name
				) == expected, guild_name
		assert has_training_catalogue(
				guild_name
				) == bool(
						expected
						), guild_name
		for tag in expected:
			assert training_covers(
					guild_name,
					tag.NAME,
					), tag.NAME
	assert trainings_for(
			"No Such Guild"
			) == ()
	assert not has_training_catalogue(
			"No Such Guild"
			)

	#-- The Records landed as Reports on each Tag, of the declared kinds.
	for tag in lessons:
		assert isinstance(
				tag.GUILD_NAME,
				str,
				) and tag.GUILD_NAME
		assert isinstance(
				tag.MIN_LEVEL,
				int,
				) and tag.MIN_LEVEL >= 1
		assert isinstance(
				tag.SOURCE,
				str,
				) and tag.SOURCE
		assert (
			tag.PATH is None
			or isinstance(
					tag.PATH,
					str,
					)
			or issubclass(
					tag.PATH,
					Tag,
					)
			)
	assert Second_Wind.PATH is None
	assert issubclass(
			Combat_Superiority.PATH,
			Tag,
			)
		#-- A Tag class held by a Pin Record stays a value on the Tag.

	for guild_name in GUILDS:
		assert has_training_catalogue(
				guild_name
				), guild_name

	char = Character(
			seed=1
			)
	char.level = 1
	char.char_class = "Fighter"
	Apply_Guild(
			char
			)
	applied = Apply_Guild_Trainings(
			char
			)
	assert Second_Wind in applied
	assert char in Second_Wind and char in Weapon_Mastery
	assert char in Training
	assert not hasattr(
			char,
			"PATH",
			) and not hasattr(
					char,
					"GUILD_NAME",
					)
		#-- Pin Records are Reports of the Tag, never Actions on the Character.
	names = Built_Titles(
			char
			)
	assert "Second Wind" in names
	assert "Weapon Mastery" in names
	second_wind_chips = Built_Chip_Values(
			char,
			Second_Wind,
			)
	assert second_wind_chips == { "2nd Wind Uses": 2 }, second_wind_chips

	char.level = 4
	Apply_Guild_Trainings(
			char
			)
	names = Built_Titles(
			char
			)
	assert "Action Surge" in names
	assert names.count(
			"Second Wind"
			) == 1
	#-- Same rank again: nothing new, and nothing printed twice.
	before = Built_Titles(
			char
			)
	Apply_Guild_Trainings(
			char
			)
	assert Built_Titles(
			char
			) == before
	#-- Training writes nothing to char.features any more.
	assert not any(
			getattr(
					feat,
					"source",
					"",
					).startswith(
					"Training"
					)
			for feat in getattr(
					char,
					"features",
					[],
					) or []
			)

	assert training_covers(
			"Fighter",
			"Second Wind",
			)
	assert training_covers(
			"Artificer",
			"Tinker's Magic",
			)
	assert "Second Wind" in covered_training_names(
			char
			)

	from AtlasLusoris.AtlasOfTraining.Map_of_Barbarian_Training import (
			Frenzy,
			Rage,
			)

	barb = Character(
			seed=2
			)
	barb.level = 6
	barb.char_class = "Barbarian"
	barb.subclass = "Berserker"
	Apply_Guild(
			barb
			)
	barb_applied = Apply_Guild_Trainings(
			barb
			)
	assert Rage in barb_applied and Frenzy in barb_applied
	assert Rage.PATH is None and Frenzy.PATH == "Berserker"
	rage_chips = Built_Chip_Values(
			barb,
			Rage,
			)
	assert rage_chips[ "Rage Uses" ] == 4, rage_chips
	assert rage_chips[ "Rage Damage" ] == 2, rage_chips

	other = Character(
			seed=3
			)
	other.level = 6
	other.char_class = "Barbarian"
	other.subclass = "Wild Heart"
	Apply_Guild(
			other
			)
	other_names = [
			tag.NAME
			for tag in Apply_Guild_Trainings(
					other
					)
			]
	assert "Rage" in other_names
	assert "Frenzy" not in other_names

	print(
			"OK — TrainingKit self-test"
			)


# Avoid dual-import when this file is run as __main__ (python -m …).
if __name__ == "__main__":
	from AtlasLusoris.TrainingKit import _self_test as _package_self_test
	_package_self_test()
else:
	_load_training_maps()
