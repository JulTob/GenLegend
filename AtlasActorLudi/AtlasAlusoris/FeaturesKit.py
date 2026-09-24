"""Structured tactical Feature contracts for NonPlayer Characters.

The generator stores resolved grants.  The Shiny app only projects those
grants as Entries and optional Chips; it performs no tactical selection.
"""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring,
#-- every class and method docstring, all four failure messages, the Enum
#-- values and the minted class-name shape are the original's, word for word;
#-- the transcription was proved instruction for instruction against the
#-- vaulted .pyc before this layout was applied.
#--
#-- Does this module own a domain axis (QST-0134)?  Yes — and it already says
#-- so in TOP.  Tactical_Feature is a Tag, gated by @Pre to NonPlayers only,
#-- and it keeps its own bags through @Imprint; Build_Feature_Tag mints one
#-- concrete Tag per catalogue entry.  Nothing was added here, because nothing
#-- was missing.
#--
#-- What is deliberately NOT a Tag: Activation and Tactical_Role.  Those
#-- describe a *Feature*, not a Character — no Character is an Offense — so
#-- they stay ordinary Python, as the TOP guide asks ("the host: ordinary
#-- Python.  TOP never asks you to change it").

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from TopKit import Imprint, Pre, Tag

from AtlasActorLudi.CharactersKit import NonPlayer
from AtlasActorLudi.Map_of_Scores import PB


PROJECT_ORIGINAL_BASIS = "project-original"
	#-- Written here by the project; nobody else's rights are involved.

SRD_ADAPTATION_BASIS = "srd-adaptation"
	#-- Adapted from the SRD, which obliges us to cite it completely.

RIGHTS_BASES = {
		PROJECT_ORIGINAL_BASIS,
		SRD_ADAPTATION_BASIS,
		}
	#-- The only two ways a catalogue entry may come to exist.

SRD_LICENSE = "CC-BY-4.0"
	#-- The one licence an SRD adaptation may be published under.


class Activation(str, Enum):
	"""Where a tactical Feature belongs in a creature's action economy."""

	TRAIT = "Trait"
	ACTION = "Action"
	BONUS_ACTION = "Bonus Action"
	REACTION = "Reaction"

	def __str__(
			self,
			) -> str:
		return self.value


class Tactical_Role(str, Enum):
	"""The battlefield purpose served by a tactical Feature."""

	OFFENSE = "Offense"
	DEFENSE = "Defense"
	CONTROL = "Control"
	MOBILITY = "Mobility"
	DISRUPTION = "Disruption"
	SUPPORT = "Support"
	COMMAND = "Command"
	SUSTAIN = "Sustain"
	UTILITY = "Utility"

	def __str__(
			self,
			) -> str:
		return self.value


@dataclass(
		frozen=True,
		slots=True,
		)
class Provenance:
	"""Rights and review record for one catalogue entry."""

	rights_basis: str
	license_expression: str
	source_title: str
	source_version: str = ""
	source_url: str = ""
	source_locator: str = ""
	adaptation_note: str = ""

	def Cites_Its_Source(
			self,
			) -> bool:
		"""Whether an adaptation carries every part of its citation."""
		return (
			self.license_expression == SRD_LICENSE
			and bool(self.source_version)
			and bool(self.source_url)
			and bool(self.source_locator)
			)

	def __post_init__(
			self,
			) -> None:
		if self.rights_basis not in RIGHTS_BASES:
			raise ValueError(
					"Feature provenance must be project-original or srd-adaptation."
					)

		if (
			self.rights_basis == SRD_ADAPTATION_BASIS
			and not self.Cites_Its_Source()
			):
			raise ValueError(
					"An SRD adaptation requires CC-BY-4.0, version, URL, and source locator."
					)


PROJECT_ORIGINAL = Provenance(
		rights_basis=PROJECT_ORIGINAL_BASIS,
		license_expression="NOASSERTION",
		source_title="Gen Legend original tactical catalogue",
		)
	#-- The record every entry written here carries, unless it says otherwise.


@dataclass(
		frozen=True,
		slots=True,
		)
class Chip_Spec:
	"""Optional brief sheet value contributed by a tactical Feature."""

	key: str
	label: str
	value_template: str
	icon: str = "⚙️"


@dataclass(
		frozen=True,
		slots=True,
		)
class Chip_Grant:
	"""Resolved Chip projected by the sheet without further calculation."""

	key: str
	label: str
	value: str
	icon: str
	source_feature: str


@dataclass(
		frozen=True,
		slots=True,
		)
class Feature_Grant:
	"""One selected and fully resolved NPC sheet Entry."""

	key: str
	name: str
	description: str
	activation: Activation
	tactical_roles: tuple[Tactical_Role, ...]
	source: str
	level: int
	contributing_tags: tuple[str, ...]
	chips: tuple[Chip_Grant, ...]
	provenance: Provenance


def Is_A_Stable_Key(
		key: str,
		) -> bool:
	"""Whether a key can be written in a file and matched again unchanged."""
	#-- Lower snake case, nothing else: a key is compared, stored and shared,
	#-- so anything that two writers could spell differently is refused.
	if not key:
		return False

	if key.casefold() != key:
		return False

	return " " not in key


@dataclass(
		frozen=True,
		slots=True,
		)
class Feature_Spec:
	"""Immutable catalogue entry resolved only after selection."""

	key: str
	title: str
	activation: Activation
	tactical_roles: tuple[Tactical_Role, ...]
	description_template: str
	affinities: tuple[str, ...] = ()
	requires_any: tuple[str, ...] = ()
	excludes_any: tuple[str, ...] = ()
	uniqueness_group: str = ""
	minimum_level: int = 1
	chips: tuple[Chip_Spec, ...] = ()
	provenance: Provenance = PROJECT_ORIGINAL

	def __post_init__(
			self,
			) -> None:
		if not Is_A_Stable_Key(self.key):
			raise ValueError(
					f"Feature key must be stable lower snake case: {self.key!r}."
					)

		if not self.tactical_roles:
			raise ValueError(
					f"Feature {self.key!r} requires a tactical role."
					)

		if self.minimum_level < 1:
			raise ValueError(
					f"Feature {self.key!r} has an invalid minimum level."
					)

	def Placeholders_For(
			self,
			character,
			) -> dict[str, int]:
		"""The numbers a description may name: this Character's level and PB."""
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
		return {
				"level": level,
				"pb": PB(
						level
						),
				}

	def Resolved_Chips(
			self,
			values: dict[str, int],
			) -> tuple[Chip_Grant, ...]:
		"""Every Chip this entry offers, with its placeholders spelled out."""
		return tuple(
				Chip_Grant(
						key=chip.key,
						label=chip.label,
						value=chip.value_template.format(
								**values
								),
						icon=chip.icon,
						source_feature=self.key,
						)
				for chip in self.chips
				)

	def resolve(
			self,
			character,
			contributing_tags: tuple[str, ...],
			) -> Feature_Grant:
		"""Resolve PB and level placeholders after this spec is selected."""
		values = self.Placeholders_For(
				character,
				)

		return Feature_Grant(
				key=self.key,
				name=self.title,
				description=self.description_template.format(
						**values
						),
				activation=self.activation,
				tactical_roles=self.tactical_roles,
				source=self.provenance.source_title,
				level=values["level"],
				contributing_tags=contributing_tags,
				chips=self.Resolved_Chips(
						values,
						),
				provenance=self.provenance,
				)


def Give_Feature_Bags(
		character,
		) -> None:
	"""Give a Character the two lists a granted Feature is filed in."""
	#-- Two bags, not one: `features` is the sheet's whole list and may hold
	#-- entries from elsewhere, while `npc_features` holds only these grants
	#-- and is what a repeat grant is checked against.
	if getattr(
			character,
			"features",
			None,
			) is None:
		character.features = []

	if getattr(
			character,
			"npc_features",
			None,
			) is None:
		character.npc_features = []


class Tactical_Feature(Tag):
	"""Root Tag for selected tactical Features on NonPlayer Characters."""

	NAME = "NPC Tactical Feature"
	SPEC: Feature_Spec | None = None

	@Pre
	def Requires_NonPlayer(
			target,
			) -> bool:
		return target in NonPlayer

	@Imprint
	def Ensure_Feature_Bags(
			target,
			) -> None:
		Give_Feature_Bags(
				target,
				)


def Tag_Name_For(
		key: str,
		) -> str:
	"""The class name a catalogue key is minted under: pack_tactics → …PackTactics."""
	return "NPC_Feature_" + "".join(
			part.title()
			for part in key.split(
					"_"
					)
			)


def Build_Feature_Tag(
		spec: Feature_Spec,
		) -> type[Tactical_Feature]:
	"""Build one concrete TOP Tag around an immutable catalogue entry."""
	@Imprint
	def Carry_Resolved_Grant(
			target,
			contributing_tags=(),
			) -> None:
		Carry_Feature_Grant(
				target,
				spec.resolve(
						target,
						tuple(
								contributing_tags
								),
						),
				)

	return type(
			Tag_Name_For(spec.key),
			(
					Tactical_Feature,
					),
			{
					"NAME": spec.title,
					"SPEC": spec,
					"__doc__": f"Tactical Feature Tag for {spec.title}.",
					"__module__": __name__,
					"Carry_Resolved_Grant": Carry_Resolved_Grant,
					},
			)


def Already_Granted(
		character,
		grant: Feature_Grant,
		) -> bool:
	"""Whether this Character already carries a grant under the same key."""
	return any(
			current.key == grant.key
			for current in character.npc_features
			)


def Carry_Feature_Grant(
		character,
		grant: Feature_Grant,
		) -> None:
	"""Persist one resolved grant once, preserving catalogue order."""
	Give_Feature_Bags(
			character,
			)

	if Already_Granted(
			character,
			grant,
			):
		return

	character.npc_features.append(
			grant,
			)
	character.features.append(
			grant,
			)


__all__ = (
		"Activation",
		"Build_Feature_Tag",
		"Carry_Feature_Grant",
		"Chip_Grant",
		"Chip_Spec",
		"Feature_Grant",
		"Feature_Spec",
		"PROJECT_ORIGINAL",
		"Provenance",
		"Tactical_Feature",
		"Tactical_Role",
		)


def _a_spec(**changes) -> Feature_Spec:
	"""A plain catalogue entry, for the checks below to vary one part of."""
	fields = {
			"key": "pack_tactics",
			"title": "Pack Tactics",
			"activation": Activation.TRAIT,
			"tactical_roles": (Tactical_Role.OFFENSE,),
			"description_template": "Advantage while an ally is near (+{pb}).",
			}
	fields.update(changes)
	return Feature_Spec(**fields)


class _A_Sheet:
	"""The least a Character can be and still be filed a grant."""

	def __init__(self, level=1):
		self.level = level


def _test_the_enums_read_as_their_words() -> None:
	"""An Activation or a Role prints the words the sheet shows."""
	assert str(Activation.BONUS_ACTION) == "Bonus Action"
	assert str(Tactical_Role.DISRUPTION) == "Disruption"
	assert f"{Activation.TRAIT}" == "Trait", "An f-string reads the same."


def _test_provenance() -> None:
	"""A catalogue entry must say where it came from, completely."""
	assert PROJECT_ORIGINAL.rights_basis == PROJECT_ORIGINAL_BASIS
	assert not PROJECT_ORIGINAL.Cites_Its_Source(), \
			"Our own writing cites nobody, and is not asked to."

	cited = Provenance(
			rights_basis=SRD_ADAPTATION_BASIS,
			license_expression=SRD_LICENSE,
			source_title="SRD 5.2",
			source_version="5.2",
			source_url="https://example.test/srd",
			source_locator="p. 12",
			)
	assert cited.Cites_Its_Source(), "A complete citation is accepted."

	refusals = (
			( { "rights_basis": "borrowed" },
				"project-original or srd-adaptation" ),
			( { "rights_basis": SRD_ADAPTATION_BASIS },
				"requires CC-BY-4.0" ),
			( { "rights_basis": SRD_ADAPTATION_BASIS,
				"license_expression": SRD_LICENSE,
				"source_version": "5.2" },
				"requires CC-BY-4.0" ),
			)
	for changes, expected in refusals:
		fields = {
				"rights_basis": PROJECT_ORIGINAL_BASIS,
				"license_expression": "NOASSERTION",
				"source_title": "t",
				}
		fields.update(changes)
		try:
			Provenance(**fields)
		except ValueError as refusal:
			assert expected in str(refusal), \
					f"{changes} was refused, but not for {expected!r}: {refusal}"
		else:
			raise AssertionError(
					f"{changes} should have been refused."
					)


def _test_the_catalogue_entry_guards_itself() -> None:
	"""A malformed entry is refused where it is written, not where it is used."""
	assert Is_A_Stable_Key("pack_tactics")
	for unstable in ("", "Pack_Tactics", "pack tactics", "PACK"):
		assert not Is_A_Stable_Key(unstable), f"{unstable!r} is not a stable key."

	refusals = (
			( { "key": "Pack Tactics" }, "stable lower snake case" ),
			( { "key": "" }, "stable lower snake case" ),
			( { "tactical_roles": () }, "requires a tactical role" ),
			( { "minimum_level": 0 }, "invalid minimum level" ),
			( { "minimum_level": -3 }, "invalid minimum level" ),
			)
	for changes, expected in refusals:
		try:
			_a_spec(**changes)
		except ValueError as refusal:
			assert expected in str(refusal), \
					f"{changes} was refused, but not for {expected!r}: {refusal}"
		else:
			raise AssertionError(
					f"{changes} should have been refused."
					)


def _test_resolution_fills_the_placeholders() -> None:
	"""A selected entry becomes a grant with its numbers already worked out."""
	spec = _a_spec(
			chips=(
					Chip_Spec(
							key="reach",
							label="Reach",
							value_template="{pb} ft",
							),
					),
			)
	grant = spec.resolve(
			_A_Sheet(level=5),
			("Wolf", "Hunter"),
			)

	assert grant.key == "pack_tactics"
	assert grant.name == "Pack Tactics"
	assert grant.level == 5
	assert grant.description == "Advantage while an ally is near (+3).", \
			f"Level 5 carries a proficiency bonus of 3: {grant.description}"
	assert grant.contributing_tags == ("Wolf", "Hunter")
	assert grant.source == PROJECT_ORIGINAL.source_title
	assert grant.chips[0].value == "3 ft", "A Chip is resolved the same way."
	assert grant.chips[0].source_feature == "pack_tactics", \
			"A Chip remembers which Feature offered it."

	#-- A sheet with no level, or a nonsense one, still resolves at level 1.
	assert spec.resolve(_A_Sheet(level=0), ()).level == 1
	assert spec.Placeholders_For(_A_Sheet(level=-4)) == { "level": 1, "pb": 2 }


def _test_the_minted_tag() -> None:
	"""One catalogue entry mints one Tag, named after its key."""
	assert Tag_Name_For("pack_tactics") == "NPC_Feature_PackTactics"
	assert Tag_Name_For("aura") == "NPC_Feature_Aura"

	spec = _a_spec()
	minted = Build_Feature_Tag(spec)

	assert minted.__name__ == "NPC_Feature_PackTactics"
	assert minted.SPEC is spec, "The Tag carries the entry it was built from."
	assert minted.NAME == "Pack Tactics"
	assert minted.__doc__ == "Tactical Feature Tag for Pack Tactics."
	assert issubclass(minted, Tactical_Feature), "Every Feature Tag is one of these."


def _test_a_grant_is_filed_once() -> None:
	"""The same Feature granted twice is written down once, in order."""
	sheet = _A_Sheet(level=3)
	first = _a_spec().resolve(sheet, ())
	second = _a_spec(title="Renamed").resolve(sheet, ())
	other = _a_spec(key="aura", title="Aura").resolve(sheet, ())

	Carry_Feature_Grant(sheet, first)
	Carry_Feature_Grant(sheet, second)
	Carry_Feature_Grant(sheet, other)

	assert [g.key for g in sheet.npc_features] == ["pack_tactics", "aura"], \
			"A repeat under the same key is ignored, and order is the order granted."
	assert sheet.features == sheet.npc_features, \
			"Both bags carry the same grants when nothing else filled them."
	assert sheet.npc_features[0].name == "Pack Tactics", \
			"The first grant stands; the repeat does not overwrite it."

	#-- A sheet with no bags at all gets them.
	bare = _A_Sheet()
	Carry_Feature_Grant(bare, first)
	assert bare.features and bare.npc_features


def _self_test() -> None:
	_test_the_enums_read_as_their_words()
	_test_provenance()
	_test_the_catalogue_entry_guards_itself()
	_test_resolution_fills_the_placeholders()
	_test_the_minted_tag()
	_test_a_grant_is_filed_once()
	print("OK — Alusoris FeaturesKit self-test")


if __name__ == "__main__":
	_self_test()
