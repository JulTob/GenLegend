"""Project-original seed catalogue for NonPlayer tactical Features.

No Monster Manual or 5e.tools prose is copied here.  External adaptations
must enter with explicit provenance through :class:`Feature_Spec`.
"""
#-- Recovered from the pre-wipe bytecode mirror (QST-0134).  The file left by
#-- the 2026-08-29 accident was a broken reconstruction: FEATURE_SPECS was a
#-- flat tuple of loose constants, and FEATURE_TAGS, FEATURES_BY_KEY and
#-- __all__ were all None, which is why no NonPlayer could be granted a
#-- tactical Feature.  The real catalogue survived in
#-- .recovery-vault/_prewipe-pyc-mirror/.  All seventeen entries are back:
#-- their keys, titles, prose, activations, roles, affinities, requirements,
#-- uniqueness groups and Chips are the original's, printed out of the objects
#-- the vaulted bytecode builds rather than typed out by hand.
#--
#-- Does this module own a domain axis (QST-0134)?  No.  It is a Lodge — a
#-- list of entries, like every other Ledger and Lodge in the project.  The
#-- Tags it publishes are minted by FeaturesKit.Build_Feature_Tag, which is
#-- where the axis lives.  A Lodge adds content, never structure.

from __future__ import annotations

from types import MappingProxyType

from AtlasActorLudi.AtlasAlusoris.FeaturesKit import Activation
from AtlasActorLudi.AtlasAlusoris.FeaturesKit import Build_Feature_Tag
from AtlasActorLudi.AtlasAlusoris.FeaturesKit import Chip_Spec
from AtlasActorLudi.AtlasAlusoris.FeaturesKit import Feature_Spec
from AtlasActorLudi.AtlasAlusoris.FeaturesKit import Tactical_Role


CATALOG_VERSION = "npc-tactics-2"
	#-- Stamped onto every Character built from this catalogue, so a saved
	#-- NonPlayer says which edition of the list it was granted from.


FEATURE_SPECS = (
	Feature_Spec(
		key="steady_anchor",
		title="Steady Anchor",
		activation=Activation.TRAIT,
		tactical_roles=(
			Tactical_Role.DEFENSE,
			),
		description_template=(
			"When an effect would push, pull, or knock this NPC down, it adds {pb} to the check or save made to resist that movement."
			),
		affinities=(
			"construct",
			"giant",
			"guardian",
			"knight",
			"soldier",
			),
		chips=(
			Chip_Spec(
				key="stability",
				label="Stability",
				value_template="+{pb}",
				icon="⚓",
				),
			),
		),
	Feature_Spec(
		key="coordinated_pressure",
		title="Coordinated Pressure",
		activation=Activation.TRAIT,
		tactical_roles=(
			Tactical_Role.OFFENSE,
			Tactical_Role.COMMAND,
			),
		description_template=(
			"Once each round after this NPC hits a creature, the next ally to hit that creature before this NPC's next turn deals {pb} extra damage."
			),
		affinities=(
			"bard",
			"fighter",
			"hunter",
			"mentor",
			"soldier",
			"spy",
			),
		),
	Feature_Spec(
		key="driving_break",
		title="Driving Break",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.OFFENSE,
			Tactical_Role.CONTROL,
			),
		description_template=(
			"After moving at least 10 feet in a straight line, this NPC makes one attack. On a hit, the target must resist the NPC's save DC or move 10 feet in the same direction."
			),
		affinities=(
			"barbarian",
			"berserker",
			"dragon",
			"fighter",
			"giant",
			"warrior",
			),
		),
	Feature_Spec(
		key="binding_arc",
		title="Binding Arc",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.CONTROL,
			),
		description_template=(
			"Choose a creature within 30 feet. It must resist the NPC's save DC or its speed is reduced by 10 feet until the end of its next turn."
			),
		affinities=(
			"druid",
			"primal",
			"plant",
			"shaman",
			"witch",
			),
		),
	Feature_Spec(
		key="thought_static",
		title="Thought Static",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.DISRUPTION,
			),
		description_template=(
			"One creature within 60 feet must resist the NPC's save DC. On a failure, it subtracts {pb} from its next concentration check before the end of its next turn."
			),
		affinities=(
			"aberration",
			"arcane",
			"mage",
			"occult",
			"spellcaster",
			"warlock",
			"witch",
			"wizard",
			),
		requires_any=(
			"aberration",
			"arcane",
			"mage",
			"occult",
			"spellcaster",
			"warlock",
			"witch",
			"wizard",
			),
		),
	Feature_Spec(
		key="rally_vector",
		title="Rally Vector",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.SUPPORT,
			Tactical_Role.COMMAND,
			),
		description_template=(
			"Choose up to {pb} allies who can hear this NPC. Each chosen ally may move 5 feet without spending its reaction."
			),
		affinities=(
			"bard",
			"cleric",
			"divine",
			"hero",
			"mentor",
			"noble",
			"paladin",
			"priest",
			),
		),
	Feature_Spec(
		key="veil_stride",
		title="Veil Stride",
		activation=Activation.BONUS_ACTION,
		tactical_roles=(
			Tactical_Role.MOBILITY,
			),
		description_template=(
			"This NPC moves up to 10 feet to an unoccupied space it can see. This movement ignores creatures and does not trigger reactions."
			),
		affinities=(
			"fey",
			"fiend",
			"ninja",
			"rogue",
			"spy",
			"trickster",
			"occult",
			"warlock",
			),
		),
	Feature_Spec(
		key="hold_the_angle",
		title="Hold the Angle",
		activation=Activation.BONUS_ACTION,
		tactical_roles=(
			Tactical_Role.DEFENSE,
			Tactical_Role.COMMAND,
			),
		description_template=(
			"Choose an adjacent ally. Until the start of this NPC's next turn, the first attack against that ally is reduced by {pb}."
			),
		affinities=(
			"fighter",
			"guardian",
			"knight",
			"paladin",
			"soldier",
			),
		),
	Feature_Spec(
		key="field_patch",
		title="Field Patch",
		activation=Activation.BONUS_ACTION,
		tactical_roles=(
			Tactical_Role.SUSTAIN,
			Tactical_Role.SUPPORT,
			),
		description_template=(
			"A creature within reach regains {pb} hit points. A creature can benefit from Field Patch only once per encounter."
			),
		affinities=(
			"artisan",
			"crafter",
			"doctor",
			"healer",
			"hermit",
			"priest",
			),
		),
	Feature_Spec(
		key="guarding_intercept",
		title="Guarding Intercept",
		activation=Activation.REACTION,
		tactical_roles=(
			Tactical_Role.DEFENSE,
			Tactical_Role.SUPPORT,
			),
		description_template=(
			"When an ally within 5 feet takes damage, this NPC reduces that damage by {pb} and may exchange places with the ally."
			),
		affinities=(
			"fighter",
			"guardian",
			"knight",
			"paladin",
			"soldier",
			),
		uniqueness_group="protective_reaction",
		),
	Feature_Spec(
		key="counterstep",
		title="Counterstep",
		activation=Activation.REACTION,
		tactical_roles=(
			Tactical_Role.MOBILITY,
			),
		description_template=(
			"When a creature misses this NPC with an attack, the NPC moves up to {pb} × 5 feet without triggering a reaction from that creature."
			),
		affinities=(
			"artist",
			"bard",
			"ninja",
			"rogue",
			"spy",
			"trickster",
			),
		),
	Feature_Spec(
		key="predatory_focus",
		title="Predatory Focus",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.OFFENSE,
			),
		description_template=(
			"Choose one visible creature. Until the end of this NPC's next turn, its first hit against that target deals {pb} extra damage."
			),
		affinities=(
			"beast",
			"dragon",
			"hunter",
			"ranger",
			"vampire",
			),
		),
	Feature_Spec(
		key="prepared_escape",
		title="Prepared Escape",
		activation=Activation.BONUS_ACTION,
		tactical_roles=(
			Tactical_Role.MOBILITY,
			Tactical_Role.UTILITY,
			),
		description_template=(
			"The NPC uses a previously identified route, cover, or distraction. It may Dash or Disengage, but must end the movement farther from its nearest enemy."
			),
		affinities=(
			"bandit",
			"criminal",
			"pirate",
			"traveler",
			"wayfarer",
			),
		),
	Feature_Spec(
		key="tactical_appraisal",
		title="Tactical Appraisal",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.UTILITY,
			Tactical_Role.SUPPORT,
			),
		description_template=(
			"Study one visible creature. The NPC learns whether one chosen defense, save, or movement speed is higher, lower, or equal to its own."
			),
		affinities=(
			"expert",
			"mage",
			"mentor",
			"sage",
			"scholar",
			"scribe",
			"wizard",
			),
		),
	Feature_Spec(
		key="last_reserve",
		title="Last Reserve",
		activation=Activation.REACTION,
		tactical_roles=(
			Tactical_Role.DEFENSE,
			Tactical_Role.SUSTAIN,
			),
		description_template=(
			"When damage would reduce this NPC below half its hit points, it gains {pb} temporary hit points. It can do so once per encounter."
			),
		affinities=(
			"barbarian",
			"berserker",
			"commoner",
			"hero",
			"warrior",
			),
		uniqueness_group="protective_reaction",
		),
	Feature_Spec(
		key="elemental_pressure",
		title="Elemental Pressure",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.OFFENSE,
			Tactical_Role.CONTROL,
			),
		description_template=(
			"Choose a 10-foot area within 60 feet. Creatures in it must resist the NPC's save DC or take {pb} damage and treat the area as difficult terrain until the NPC's next turn."
			),
		affinities=(
			"dragon",
			"druid",
			"elemental",
			"evocation",
			"fire",
			"lightning",
			"primal",
			"shaman",
			"sorcerer",
			),
		requires_any=(
			"dragon",
			"druid",
			"elemental",
			"shaman",
			"sorcerer",
			),
		),
	Feature_Spec(
		key="unstable_formula",
		title="Unstable Formula",
		activation=Activation.ACTION,
		tactical_roles=(
			Tactical_Role.OFFENSE,
			Tactical_Role.UTILITY,
			),
		description_template=(
			"Choose acid, cold, fire, lightning, or thunder. Until the end of the NPC's next turn, one of its attacks deals {pb} extra damage of that type."
			),
		affinities=(
			"arcane",
			"artisan",
			"construct",
			"crafter",
			"evocation",
			"fire",
			"magic",
			"mage",
			"sorcerer",
			"wizard",
			),
		),
	)
	#-- Seventeen entries.  A new one is added here and nowhere else: the
	#-- lookup, the Tags and the export list below all follow from this tuple.


FEATURES_BY_KEY = MappingProxyType(
		{
				spec.key: spec
				for spec in FEATURE_SPECS
				}
		)
	#-- Read-only on purpose: a catalogue that callers could edit at runtime
	#-- would make two Characters built from the same seed disagree.


if len(
		FEATURES_BY_KEY
		) != len(
		FEATURE_SPECS
		):
	#-- A repeated key would silently hide an entry, so the module refuses to
	#-- import rather than let the catalogue lie about its own size.
	raise ValueError(
			"NonPlayer tactical Feature keys must be unique."
			)


FEATURE_TAGS = MappingProxyType(
		{
				spec.key: Build_Feature_Tag(
						spec
						)
				for spec in FEATURE_SPECS
				}
		)
	#-- One concrete TOP Tag per entry, minted once at import.


for _tag in FEATURE_TAGS.values():
	globals()[
			_tag.__name__
			] = _tag
	#-- Each minted Tag is also published under its own name, so a caller may
	#-- write `from ...Lodge_of_NonPlayer_Features import NPC_Feature_VeilStride`
	#-- instead of reaching into FEATURE_TAGS.  Nothing does today; flagged for
	#-- QST-0093.3 (delete what nothing imports) rather than removed here,
	#-- because this file is being restored, not redesigned.


__all__ = (
		"CATALOG_VERSION",
		"FEATURES_BY_KEY",
		"FEATURE_SPECS",
		"FEATURE_TAGS",
		*tuple(
				tag.__name__
				for tag in FEATURE_TAGS.values()
				),
		)


class _A_Sheet:
	"""A Character stand-in, so the catalogue can prove it resolves."""

	level = 5


def _self_test() -> None:
	"""The catalogue's own promises: unique, complete, and resolvable."""

	assert len(FEATURE_SPECS) == 17, \
			f"The seed catalogue holds seventeen entries, not {len(FEATURE_SPECS)}."
	assert len(FEATURES_BY_KEY) == len(FEATURE_SPECS), "Every key is its own."
	assert len(FEATURE_TAGS) == len(FEATURE_SPECS), "Every entry mints one Tag."

	for spec in FEATURE_SPECS:
		assert FEATURES_BY_KEY[spec.key] is spec, "The lookup finds the entry."
		assert FEATURE_TAGS[spec.key].SPEC is spec, "The Tag carries the entry."
		assert spec.tactical_roles, f"{spec.key} must say what it is for."
		assert spec.title, f"{spec.key} must have a title to show."

	#-- Every placeholder a description or a Chip names must be one that
	#-- resolution fills in, or the sheet would raise when it rendered.
	for spec in FEATURE_SPECS:
		grant = spec.resolve(
				_A_Sheet(),
				(),
				)
		assert "{" not in grant.description, \
				f"{spec.key} left a placeholder unfilled: {grant.description}"
		for chip in grant.chips:
			assert "{" not in chip.value, \
					f"{spec.key} left a Chip placeholder unfilled: {chip.value}"

	#-- Uniqueness groups exist so two of a kind are not granted together.
	grouped = [spec.key for spec in FEATURE_SPECS if spec.uniqueness_group]
	assert grouped, "At least one group is declared, or the field is dead."

	print(
			f"OK — Lodge_of_NonPlayer_Features self-test ({len(FEATURE_SPECS)} entries)"
			)


if __name__ == "__main__":
	_self_test()
