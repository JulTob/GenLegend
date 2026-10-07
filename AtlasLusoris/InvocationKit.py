"""
InvocationKit

Eldritch Invocation Tags — Warlock lessons chosen from a catalogue.
Distinct from Guild Training (class features) and Feats.

An Invocation is declared by what it *does*, not by prose about what it does.
The twenty-eight published invocations are seven shapes wearing different
spell names, so ``Make_Invocation`` takes those shapes as fields:

        at_will=MageArmor          cast it without a slot, as often as you like
        free_cast=WaterBreathing   … once, then a Long Rest
        sense="Truesight 30 feet"  a passive line on the sheet
        choose_cantrip="damage"    mark one of your cantrips as enhanced
        familiar=True              Pact of the Chain's special forms
        origin_feat=True           Lessons of the First Ones
        apply=<callable>           the escape hatch, for the genuinely bespoke

**Prerequisites are Tags, not strings.**  The 2024 text says "Prerequisite:
Pact of the Blade Invocation", so ``requires`` holds that Invocation's Tag and
the gate is ``target in requires``.  Tag membership is the question TagKit
exists to answer; comparing names against two different feature lists was a
workaround for not having asked it.

The catalogue is a Pin Field.  ``Make_Invocation`` builds the Tag with only
its behaviour and pins it with ``Declared_Invocation``, whose Records
(``MIN_LEVEL``, ``REQUIRES``, ``SOURCE``) land on the Tag as Reports;
``all_invocations()`` reads ``Declared_Invocation[:]``, so declaring an
Invocation is the only step that makes it real.

Effects land on plain Character attributes, the same way Backgrounds land
skills: ``at_will_spells``, ``free_cast_spells``, ``senses``, ``enhanced_cantrips``,
``pact_familiar``.  Nothing here simulates combat — this builds a sheet.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from TopKit import Imprint, Pin, Pre, Record, Tag

from AtlasActorLudi.CharactersKit import Character
from AtlasLusoris.FeaturesKit import (
		Invocation as Invocation_Root,
		grant,
		)


class Pact_Capability(
		Tag,
		):
	"""A subsystem an Invocation opens, and that other Invocations require."""


class Pact_Weapon(
		Pact_Capability,
		):
	"""A conjured or bonded weapon answering to Charisma."""


class Pact_Familiar(
		Pact_Capability,
		):
	"""A bound familiar, with forms no ordinary caster may summon."""


class Pact_Tome(
		Pact_Capability,
		):
	"""A Book of Shadows, and whatever is written into it."""


@Pin
class Declared_Invocation(
		Tag,
		):
	"""
	The catalogue of Eldritch Invocations, as a Pin.

	``Make_Invocation`` builds an Invocation Tag with only its behaviour and
	then pins it here, so ``Declared_Invocation[:]`` is the catalogue in
	declaration order and nothing keeps a list beside it.  The Records land
	on the pinned Tag as Reports (``EldritchSmite.MIN_LEVEL``) and are
	validated here, once, for every declarer.
	"""

	@Pre
	def Invocation_Tag_Only(
			target,
			):
		return (
				isinstance(
						target,
						type,
						)
				and issubclass(
						target,
						Invocation_Root,
						)
				and target is not Invocation_Root
				)

	@Record
	def MIN_LEVEL(
			target,
			*,
			min_level=1,
			) -> int:
		"""The Warlock level at which this Invocation opens."""
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
					"Declared_Invocation: min_level must be an integer of "
					f"at least 1, not {min_level!r}."
					)
		return min_level

	@Record
	def REQUIRES(
			target,
			*,
			requires=None,
			) -> str | None:
		"""
		The NAME of the Invocation this one requires, or None.

		Read off whatever ``requires`` holds, as the namespace constant was:
		a prerequisite Tag answers with its NAME, anything else with None.
		The prerequisite itself is kept by ``prerequisite_of``.
		"""
		return getattr(
				requires,
				"NAME",
				None,
				)

	@Record
	def SOURCE(
			target,
			*,
			source="Eldritch Invocation",
			) -> str:
		"""The source line the sheet prints under this Invocation."""
		if (
				not isinstance(
						source,
						str,
						)
				or not source.strip()
				):
			raise ValueError(
					"Declared_Invocation: source must be a non-empty string, "
					f"not {source!r}."
					)
		return source


_PREREQUISITE: dict[type[Invocation_Root], type[Invocation_Root]] = {}


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


def warlock_invocations_known(
		level: int,
		) -> int:
	"""2024 PHB Invocations column."""
	level = max(
			1,
			min(
					20,
					int(
							level or 1
							),
					),
			)
	table = (
			0,
			1,
			3,
			3,
			3,
			5,
			5,
			6,
			6,
			7,
			7,
			7,
			8,
			8,
			8,
			9,
			9,
			9,
			10,
			10,
			10,
			)
	return table[ level ]


def _collect(
		char,
		attribute: str,
		value,
		) -> None:
	"""Append to a list attribute on the Character, creating it if absent."""
	bag = getattr(
			char,
			attribute,
			None,
			)
	if bag is None:
		bag = []
		setattr(
				char,
				attribute,
				bag,
				)
	items = (
			value
			if isinstance(
					value,
					(
							tuple,
							list,
							),
					)
			else (
					value,
					)
			)
	for item in items:
		if item is None:
			continue
		if item not in bag:
			bag.append(
					item
					)


def Make_Invocation(
		*,
		name: str,
		min_level: int = 1,
		description: str,
		requires: type[Tag] | None = None,
		ability: str | tuple[str, ...] | None = None,
		grants: type[Pact_Capability] | tuple[type[Pact_Capability], ...] = (),
		at_will=None,
		free_cast=None,
		sense: str | tuple[str, ...] | None = None,
		choose_cantrip: str | None = None,
		familiar: bool = False,
		origin_feat: bool = False,
		apply: Callable[[Any], None] | None = None,
		source: str = "Eldritch Invocation",
		) -> type[Invocation_Root]:
	"""Construct one Eldritch Invocation Tag."""
	if not name or not name.strip():
		raise ValueError(
				"Make_Invocation: name is required."
				)
	if min_level < 1:
		raise ValueError(
				"Make_Invocation: min_level must be at least 1."
				)
	invocation_tag = None

	@Pre
	def Warlock_Only(
			target,
			):
		from AtlasLusoris.GuildKit import Warlock
		return (
				target in Warlock
				or getattr(
						target,
						"char_class",
						None,
						) == "Warlock"
				)

	@Pre
	def Rank_Reached(
			target,
			):
		from AtlasLusoris.TrainingKit import level_in_guild
		return (
				level_in_guild(
						target,
						"Warlock",
						) >= min_level
				)

	@Pre
	def Prerequisite_Met(
			target,
			):
		return (
				requires is None
				or target in requires
				)

	@Pre
	def Ability_Met(
			target,
			):
		"""
		Some knowledge only opens to one kind of mind.

		An invocation gated on Intelligence is not stronger than one gated on
		Charisma; it is the same tier said in a different language.  Gating
		here also keeps the generator honest: a Warlock who talked their way
		in never draws the one that had to be read.
		"""
		wanted = _ABILITY.get(
				invocation_tag,
				(),
				)
		if not wanted:
			return True
		from AtlasLusoris.Grimoire_of_Spellcasters import (
				warlock_casting_ability,
				)
		return (
				warlock_casting_ability(
						target
						) in wanted
				)

	@Imprint
	def Awaken(
			target,
			):
		existing = (
				getattr(
						target,
						"features",
						None,
						)
				or []
				)
		if any(
				getattr(
						feat,
						"name",
						None,
						) == name
				and getattr(
						feat,
						"source",
						None,
						) == source
				for feat in existing
				):
			return
		grant(
				target,
				name=name,
				description=description,
				source=source,
				level=min_level,
				)
		if at_will is not None:
			_collect(
					target,
					"at_will_spells",
					at_will,
					)
		if free_cast is not None:
			_collect(
					target,
					"free_cast_spells",
					free_cast,
					)
		if sense is not None:
			_collect(
					target,
					"senses",
					sense,
					)
		if choose_cantrip is not None:
			_collect(
					target,
					"enhanced_cantrips",
					(
							(
									name,
									choose_cantrip,
									),
							),
					)
		if familiar:
			from AtlasLusoris.AtlasOfInvocations.Map_of_Familiars import (
					pick_familiar,
					)
			target.pact_familiar = pick_familiar(
					target,
					dice=target.Dice_Bag(
							"Pact_Familiar.familiar"
							),
					)
		if origin_feat:
			target.owed_origin_feats = getattr(
					target,
					"owed_origin_feats",
					0,
					) + 1
		if apply is not None:
			apply(
					target
					)
		bag = getattr(
				target,
				"invocations",
				None,
				)
		if bag is None:
			target.invocations = []
			bag = target.invocations
		if not any(
				getattr(
						item,
						"name",
						None,
						) == name
				for item in bag
				):
			bag.append(
					type(
							"InvocationRef",
							(),
							{
									"name": name,
									"description": description,
									"source": source,
									"level": min_level,
									},
							)()
					)

	granted = (
			(
					grants,
					)
			if isinstance(
					grants,
					type,
					)
			else tuple(
					grants
					)
			)
	invocation_tag = type(
			_class_name(
					name
					),
			(
					Invocation_Root,
					*granted,
					),
			{
					"NAME": name,
					"Warlock_Only": Warlock_Only,
					"Rank_Reached": Rank_Reached,
					"Prerequisite_Met": Prerequisite_Met,
					"Ability_Met": Ability_Met,
					"Awaken": Awaken,
					"__module__": __name__,
					},
			)
	Declared_Invocation(
			invocation_tag,
			min_level=min_level,
			requires=requires,
			source=source,
			)
	if requires is not None:
		_PREREQUISITE[ invocation_tag ] = requires
	if ability is not None:
		_ABILITY[ invocation_tag ] = (
				(
						ability,
						)
				if isinstance(
						ability,
						str,
						)
				else tuple(
						ability
						)
				)
	return invocation_tag


def prerequisite_of(
		tag: type[Invocation_Root],
		) -> type[Invocation_Root] | None:
	"""The Invocation this one requires, if any."""
	return _PREREQUISITE.get(
			tag
			)


def all_invocations() -> tuple[type[Invocation_Root], ...]:
	"""Every declared Invocation, in declaration order: the Pin's Field."""
	return tuple(
			Declared_Invocation[:]
			)


_ABILITY: dict[type, tuple[str, ...]] = {}


def invocation_abilities(
		tag: type[Invocation_Root],
		) -> tuple[str, ...]:
	"""The spellcasting abilities this Invocation opens to, empty for any."""
	return _ABILITY.get(
			tag,
			(),
			)


def invocation_eligible(
		char,
		tag: type[Invocation_Root],
		) -> bool:
	"""Whether this Character could take the Invocation right now."""
	from AtlasLusoris.TrainingKit import level_in_guild
	if (
			level_in_guild(
					char,
					"Warlock",
					) < tag.MIN_LEVEL
			):
		return False
	wanted = _ABILITY.get(
			tag,
			(),
			)
	if wanted:
		from AtlasLusoris.Grimoire_of_Spellcasters import (
				warlock_casting_ability,
				)
		if warlock_casting_ability(
				char
				) not in wanted:
			return False
	requires = _PREREQUISITE.get(
			tag
			)
	return (
			requires is None
			or char in requires
			)


def available_invocations(
		char,
		) -> list[type[Invocation_Root]]:
	owned = {
			tag.NAME
			for tag in Declared_Invocation[:]
			if char in tag
			}
	found = []
	for tag in Declared_Invocation[:]:
		if tag.NAME in owned:
			continue
		if not invocation_eligible(
				char,
				tag,
				):
			continue
		found.append(
				tag
				)
	return found


def Apply_Warlock_Invocations(
		char,
		) -> list[type[Invocation_Root]]:
	"""
	Pick Eldritch Invocations up to the 2024 known count.

	Prerequisite chains are resolved by multi-pass picking.
	"""
	from AtlasLusoris.GuildKit import Warlock
	from AtlasLusoris.TrainingKit import level_in_guild
	if (
			char not in Warlock
			and getattr(
					char,
					"char_class",
					None,
					) != "Warlock"
			):
		return []
	need = warlock_invocations_known(
			level_in_guild(
					char,
					"Warlock",
					)
			or getattr(
					char,
					"level",
					1,
					)
			)
	applied = []
	already = [
			tag
			for tag in Declared_Invocation[:]
			if char in tag
			]
	applied.extend(
			already
			)
	dice = char.Dice_Bag(
			"Eldritch_Invocations.choice"
			)
		#-- one bag for the whole set of invocations, the one the lesson
		#-- Eldritch_Invocations names (QST-0144.6); opened once, drawn from
		#-- at every pass
	while len(
			applied
			) < need:
		pool = available_invocations(
				char
				)
		if not pool:
			break
		pick = char.Accept(
				pool,
				dice=dice,
				)
		if (
				char in pick
				and pick not in applied
				):
			applied.append(
					pick
					)
		else:
			break
	Settle_Invocations(
			char
			)
	return applied


def Settle_Invocations(
		char,
		) -> list:
	"""
	Grant what Invocations promised but could not deliver themselves.

	TagKit forbids applying a Tag to a Target that is already mid-application,
	so Lessons of the First Ones records a debt instead of granting its Origin
	feat inline.  This settles it from outside any Imprint.
	"""
	from AtlasLusoris.FeaturesKit import Grant_Origin_Feat
	owed = int(
			getattr(
					char,
					"owed_origin_feats",
					0,
					)
			)
	granted = []
	while owed > 0:
		granted.append(
				Grant_Origin_Feat(
						char,
						source="Invocation — Lessons of the First Ones",
						)
				)
		owed -= 1
	char.owed_origin_feats = 0
	return granted


def _load_invocation_maps() -> None:
	import importlib
	importlib.import_module(
			"AtlasLusoris.AtlasOfInvocations.Map_of_Eldritch_Invocations"
			)


def _self_test():
	from AtlasLusoris.GuildKit import Apply_Guild
	char = Character(
			seed=1
			)
	char.level = 5
	char.char_class = "Warlock"
	Apply_Guild(
			char
			)
	assert len(
			all_invocations()
			) >= 28
	#-- The catalogue is the Pin's Field: the Map's declarations, in the
	#-- order they were written, and nothing else.
	from AtlasLusoris.AtlasOfInvocations import Map_of_Eldritch_Invocations
	declared = tuple(
			value
			for value in vars(
					Map_of_Eldritch_Invocations
					).values()
			if isinstance(
					value,
					type,
					)
			and issubclass(
					value,
					Invocation_Root,
					)
			)
	assert len(
			declared
			) == 28
	assert tuple(
			Declared_Invocation[:]
			) == declared
	assert all_invocations() == declared
	#-- The Reports answer what the namespace constants used to.
	for tag in declared:
		assert tag in Declared_Invocation
		assert tag.MIN_LEVEL >= 1
		assert tag.REQUIRES == getattr(
				prerequisite_of(
						tag
						),
				"NAME",
				None,
				)
		assert tag.SOURCE == "Eldritch Invocation"
	#-- available_invocations reads the same Field: a first-rank Warlock
	#-- sees exactly the first-rank lessons.
	novice = Character(
			seed=1
			)
	novice.level = 1
	novice.char_class = "Warlock"
	Apply_Guild(
			novice
			)
	assert [
			tag.NAME
			for tag in available_invocations(
					novice
					)
			] == [
			tag.NAME
			for tag in declared
			if tag.MIN_LEVEL <= 1
			]
	picked = Apply_Warlock_Invocations(
			char
			)
	assert len(
			picked
			) == 5
	names = [
			tag.NAME
			for tag in picked
			]
	assert len(
			names
			) == len(
			set(
					names
					)
			)
	print(
			"OK — InvocationKit self-test:",
			names,
			)


if __name__ == "__main__":
	from AtlasLusoris.InvocationKit import _self_test as _package_self_test
	_package_self_test()
else:
	_load_invocation_maps()
