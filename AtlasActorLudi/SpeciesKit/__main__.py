"""Run the SpeciesKit contract checks beside the package."""

from TopKit import TagImprintError
from TopKit import TagPreconditionError

from AtlasActorLudi.CharactersKit import Character
from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores
from AtlasActorLudi.Grimoire_of_Skills import Char_Skills
from AtlasActorLudi.Map_of_Scores import PB
from AtlasActorLudi.SpeciesKit import Aasimar
from AtlasActorLudi.SpeciesKit import Abyssal
from AtlasActorLudi.SpeciesKit import Apply_Species
from AtlasActorLudi.SpeciesKit import Available
from AtlasActorLudi.SpeciesKit import Chthonic
from AtlasActorLudi.SpeciesKit import Current_Heritage
from AtlasActorLudi.SpeciesKit import Declared_Species
from AtlasActorLudi.SpeciesKit import Dwarf
from AtlasActorLudi.SpeciesKit import Dark_Elf
from AtlasActorLudi.SpeciesKit import Elf
from AtlasActorLudi.SpeciesKit import ELF_HERITAGES
from AtlasActorLudi.SpeciesKit import Fiend
from AtlasActorLudi.SpeciesKit import Find_Heritage
from AtlasActorLudi.SpeciesKit import Find_Species
from AtlasActorLudi.SpeciesKit import Find_Subspecies
from AtlasActorLudi.SpeciesKit import Forest_Gnome
from AtlasActorLudi.SpeciesKit import Gnome
from AtlasActorLudi.SpeciesKit import GNOME_HERITAGES
from AtlasActorLudi.SpeciesKit import Gnomish_Cunning
from AtlasActorLudi.SpeciesKit import Goliath
from AtlasActorLudi.SpeciesKit import Halfling
from AtlasActorLudi.SpeciesKit import HERITAGE_CHOICES
from AtlasActorLudi.SpeciesKit import HERITAGES_BY_SPECIES
from AtlasActorLudi.SpeciesKit import Heritage
from AtlasActorLudi.SpeciesKit import High_Elf
from AtlasActorLudi.SpeciesKit import Humanoid
from AtlasActorLudi.SpeciesKit import Human
from AtlasActorLudi.SpeciesKit import NONPLAYER_SPECIES
from AtlasActorLudi.SpeciesKit import NonPlayer_Only
from AtlasActorLudi.SpeciesKit import Orc
from AtlasActorLudi.SpeciesKit import Infernal
from AtlasActorLudi.SpeciesKit import PLAYABLE_SPECIES
from AtlasActorLudi.SpeciesKit import Player_Handbook_2024
from AtlasActorLudi.SpeciesKit import Resolve_Species_Features
from AtlasActorLudi.SpeciesKit import Rock_Gnome
from AtlasActorLudi.SpeciesKit import SPECIES_WEIGHTS
from AtlasActorLudi.SpeciesKit import Species
from AtlasActorLudi.SpeciesKit import TIEFLING_HERITAGES
from AtlasActorLudi.SpeciesKit import Tiefling
from AtlasActorLudi.SpeciesKit import Wood_Elf
from AtlasActorLudi.SpeciesKit.Aasimar import AASIMAR_REVELATIONS
from AtlasActorLudi.SpeciesKit.Aasimar import Celestial_Resistance
from AtlasActorLudi.SpeciesKit.Aasimar import Celestial_Revelation
from AtlasActorLudi.SpeciesKit.Aasimar import Current_Revelation
from AtlasActorLudi.SpeciesKit.Aasimar import Healing_Hands
from AtlasActorLudi.SpeciesKit.Aasimar import Talarian_Wings
from AtlasActorLudi.SpeciesKit.Aasimar import Inner_Radiance
from AtlasActorLudi.SpeciesKit.Aasimar import Light_Bearer
from AtlasActorLudi.SpeciesKit.Aasimar import Necrotic_Shroud
from AtlasActorLudi.SpeciesKit.Goliaths import Clouds_Jaunt
from AtlasActorLudi.SpeciesKit.Goliaths import Current_Giant_Heritage
from AtlasActorLudi.SpeciesKit.Goliaths import Fires_Burn
from AtlasActorLudi.SpeciesKit.Goliaths import Frosts_Chill
from AtlasActorLudi.SpeciesKit.Goliaths import Giant_Heritage
from AtlasActorLudi.SpeciesKit.Goliaths import GOLIATH_GIANT_HERITAGES
from AtlasActorLudi.SpeciesKit.Goliaths import Hills_Tumble
from AtlasActorLudi.SpeciesKit.Goliaths import Large_Form
from AtlasActorLudi.SpeciesKit.Goliaths import Powerful_Build
from AtlasActorLudi.SpeciesKit.Goliaths import Stones_Endurance
from AtlasActorLudi.SpeciesKit.Goliaths import Storms_Thunder
from AtlasActorLudi.SpeciesKit.Halflings import Brave
from AtlasActorLudi.SpeciesKit.Halflings import Halfling_Nimbleness
from AtlasActorLudi.SpeciesKit.Halflings import Luck
from AtlasActorLudi.SpeciesKit.Halflings import Naturally_Stealthy
from AtlasActorLudi.SpeciesKit.Orcs import Adrenaline_Rush
from AtlasActorLudi.SpeciesKit.Orcs import Darkvision as Orc_Darkvision
from AtlasActorLudi.SpeciesKit.Orcs import Relentless_Endurance
from AtlasActorLudi.SpeciesKit.Tieflings import Fiendish_Legacy
from AtlasActorLudi.SpeciesKit.Tieflings import Otherworldly_Presence
from AtlasActorLudi.SpeciesKit.traits import Darkvision as Common_Darkvision
from AtlasActorLudi.SpeciesKit.traits import Darkvision_Rules
from AtlasLusoris.FeaturesKit import Feature
from AtlasLusoris.FeaturesKit import ORIGIN_FEATS
from AtlasLusoris.FeaturesKit import Resourceful
from AtlasLusoris.FeaturesKit import Skillful
from AtlasLusoris.FeaturesKit import Trait
from AtlasLusoris.FeaturesKit import Versatile


def _completed_ledger(
		character,
		) -> None:
	character.AS = AbilityScores(
		STR=10,
		DEX=12,
		CON=14,
		INT=16,
		WIS=15,
		CHA=13,
		character=character,
		)
	character.proficiency_bonus = PB(
		character.level,
		)
	character.skills = Char_Skills(
		character,
		character.AS,
		character.proficiency_bonus,
		)
	character.base_health = 10
	character.known_spells = []


def _test_shared_darkvision_rules() -> None:
	for range_feet in (
		60,
		120,
		):
		rules = Darkvision_Rules(
			range_feet,
			)

		assert f"within {range_feet} feet" in rules

		# The 2024 glossary scopes every part of this, and an earlier wording
		# lost two of the three scopes.  Assert the scopes, not the phrasing.
		darkness = rules[ rules.index( "In Darkness" ): ]

		# 1. the range reaches the Darkness clause, or this promised unlimited
		#    darkvision in true Darkness
		assert "In Darkness within that range" in rules

		# 2. and 3. both caveats live inside the Darkness sentence: they do not
		#    apply to the Dim Light the Character is seeing as Bright Light
		assert "Disadvantage on Wisdom (Perception)" in darkness
		assert "shades of gray" in darkness

		# the unscoped claim that used to sit here said a Dwarf could not tell
		# red from blue at noon
		assert "cannot tell colors apart" not in rules


def _assert_already_gained_vocabulary(
		features,
		) -> None:
	"""
	A rule the Character already has must not be announced as a future one.

	What this catches is the retrospective or promissory voice: *will gain*,
	*when you reach*, *gained at level*.  A feature on the sheet is one the
	Character has, and saying when it arrived only helps somebody rereading
	their own past.

	It deliberately does **not** forbid *you have* or *you can*.  That is the
	rulebook's own voice, and the rules here are printed as the rulebook writes
	them: "You have Resistance to Poison damage", "You can see in Dim Light".
	Forbidding it would mean rewriting correct text into something stranger.

	Level 0 entries are skipped.  Those are the Species and Heritage
	descriptions, which are authored prose rather than rules, and they address
	the reader as *you* on purpose.
	"""
	for feature in features:
		if int(
				getattr(
						feature,
						"level",
						0,
						)
				or 0
				) == 0:
			continue

		description = feature.description.casefold()

		for forbidden in (
			"will gain",
			"when you reach",
			"gained at level",
			"you will gain",
			):
			assert forbidden not in description, (
				f"{feature.name!r} announces itself as a future feature: "
				f"{forbidden!r}"
				)


def _test_playable_species() -> None:
	for species in PLAYABLE_SPECIES:
		character = Character(
			seed=101,
			)

		selected = Apply_Species(
			character,
			species,
			)

		assert selected is species
		assert character in species
		assert character in Species
		assert character in Humanoid
		assert character.species == species.__name__
		assert character.creature_type == "Humanoid"
		assert f"{character:Species}" == species.__name__
		assert Find_Species(character) == species.__name__
		assert character.size in species.SIZE_OPTIONS

		if species in HERITAGES_BY_SPECIES:
			assert (
				Current_Heritage(character)
				in HERITAGES_BY_SPECIES[
					species
					]
				)
			assert Find_Heritage(character)
			assert Find_Subspecies(character) == Find_Heritage(character)
			assert f"{character:Subspecies}" == Find_Heritage(character)
		else:
			assert character.speed == species.SPEED

		# Every Species' projected entries obey the sheet's voice: a feature the
		# Character has is never announced as a future one, and an entry
		# without prose is allowed only when its chips are the whole feature.
		Resolve_Species_Features(character)
		_assert_already_gained_vocabulary(
			character.features,
			)
		for feature in character.features:
			if "Species" not in str(
				getattr(
					feature,
					"source",
					"",
					)
				):
				continue
			assert (
				feature.description.strip()
				or getattr(
					feature,
					"chips",
					None,
					)
				), f"{species.__name__} {feature.name!r} has neither prose nor chips"


def _test_species_declarations_own_the_catalog() -> None:
	assert tuple(
		Available[:]
		) == PLAYABLE_SPECIES
	assert tuple(
		NonPlayer_Only[:]
		) == NONPLAYER_SPECIES
	assert set(
		Declared_Species[:]
		) == set(
		(
			*PLAYABLE_SPECIES,
			*NONPLAYER_SPECIES,
			)
		)

	for species in PLAYABLE_SPECIES:
		assert species in Available
		assert species in Player_Handbook_2024
		assert species.WEIGHT > 0
		assert species.SIZE_OPTIONS
		assert species.SPEED > 0
		assert species.SOURCE_TITLE == "Player's Handbook (2024)"
		assert species.SOURCE_KIND == "official-reference"
		assert SPECIES_WEIGHTS[
			species.__name__
			] == species.WEIGHT
		assert species.HERITAGES == HERITAGES_BY_SPECIES.get(
			species,
			(),
			)
		assert species.TRAITS == tuple(
			base
			for base in species.__bases__
			if (
				isinstance(
					base,
					type,
					)
				and issubclass(
					base,
					Trait,
					)
				)
			)


def _test_random_species_is_level_stable() -> None:
	first = Character(
		seed=211,
		level=1,
		)
	progressed = Character(
		seed=211,
		level=20,
		)

	first_species = Apply_Species(first)
	progressed_species = Apply_Species(progressed)

	assert first_species is progressed_species
	assert first.size == progressed.size


def _test_human_grants_are_stable() -> None:
	first = Character(
		seed=23,
		)
	second = Character(
		seed=23,
		)

	Apply_Species(
		first,
		Human,
		)
	Apply_Species(
		second,
		Human,
		)
	_completed_ledger(first)
	_completed_ledger(second)
	Resolve_Species_Features(first)
	Resolve_Species_Features(second)

	assert first in Resourceful
	assert first in Trait
	assert first in Skillful
	assert first in Versatile
	assert any(
		first in origin
		for origin in ORIGIN_FEATS.values()
		)
	assert all(
		isinstance(
			feature,
			Feature,
			)
		for feature in first.features
		)

	first_features = [
		(
			feature.name,
			feature.description,
			)
		for feature in first.features
		]
	second_features = [
		(
			feature.name,
			feature.description,
			)
		for feature in second.features
		]

	assert first.size == second.size
	assert first_features == second_features


def _test_human_stateful_grants() -> None:
	skilled = Character(
		seed=19,
		level=5,
		)
	tough = Character(
		seed=1,
		level=5,
		)

	for character in (
		skilled,
		tough,
		):
		Apply_Species(
			character,
			Human,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)

	skillful_choice = skilled.skillful.grants[0].capability
	skilled_choices = tuple(
		grant.capability
		for grant in skilled.skilled.grants
		)
	assert skillful_choice not in skilled_choices
	assert getattr(
		skilled.skills,
		skillful_choice.legacy_attribute,
		).proficiency_level >= 1
	skillful_entry = next(
		feature
		for feature in skilled.features
		if feature.name == "Skillful"
		)
	assert (
		skillful_choice.name
		in skillful_entry.description
		)
	assert "you gain" not in skillful_entry.description.casefold()
	assert all(
		getattr(
			skilled.skills,
			capability.legacy_attribute,
			).proficiency_level >= 1
		for capability in skilled_choices
		)
	assert tough.base_health == 20


def _test_aasimar_revelation_geometry() -> None:
	assert Aasimar.REVELATIONS == AASIMAR_REVELATIONS
	assert all(
		revelation.__name__.replace(
			"_",
			" ",
			) not in HERITAGE_CHOICES
		for revelation in AASIMAR_REVELATIONS
		)

	for revelation in AASIMAR_REVELATIONS:
		character = Character(
			seed=347,
			level=3,
			)
		Apply_Species(
			character,
			Aasimar,
			)
		revelation(character)

		assert character in Aasimar
		assert character in Celestial_Revelation
		assert character in revelation
		assert Current_Revelation(character) is revelation


def _test_aasimar_rule_projection() -> None:
	novice = Character(
		seed=349,
		level=1,
		)
	Apply_Species(
		novice,
		Aasimar,
		)
	_completed_ledger(novice)
	Resolve_Species_Features(novice)

	assert novice in Celestial_Resistance
	assert novice in Healing_Hands
	assert novice in Light_Bearer
	assert novice.damage_resistances == (
		"Necrotic",
		"Radiant",
		)
	assert novice.species_spells == (
		"Light",
		)
	assert novice.species_spellcasting_ability == "CHA"
	assert novice.species_spell_free_casts == {}
	assert novice.healing_hands_dice_count == 2
	assert novice.healing_hands_die == 4
	assert novice.healing_hands_uses == 1
	assert novice.celestial_mark.ancestor_possessive in (
		"his",
		"her",
		"their",
		"its",
		)
	descent = next(
		feature
		for feature in novice.features
		if feature.name == "Celestial Descent"
		)
	assert " may " in descent.description
	assert "All of it comes down" not in descent.description
	assert "Your lineage traces back" not in descent.description
	assert Current_Revelation(novice) is None
	assert not any(
		feature.name.startswith(
			"Celestial Revelation",
			)
		for feature in novice.features
		)
	_assert_already_gained_vocabulary(
		novice.features,
		)

	for revelation in AASIMAR_REVELATIONS:
		character = Character(
			seed=353,
			level=5,
			)
		Apply_Species(
			character,
			Aasimar,
			)
		revelation(character)
		_completed_ledger(character)
		Resolve_Species_Features(character)
		feature = next(
			current
			for current in character.features
			if current.name.startswith(
				"Celestial Revelation",
				)
			)

		assert feature.level == 3
		# The level is carried by the Entry, not announced in the prose: a
		# feature on the sheet is one the Character already has.
		assert "Gained at Level" not in feature.description
		assert character.celestial_revelation_extra_damage == 3
		# No ``damage_type`` is published on purpose.  The rules say the option
		# is chosen each time the Aasimar transforms, so the sheet prints all
		# three with their own types and settles on none of them.
		assert not hasattr(
			character,
			"celestial_revelation_damage_type",
			)
		assert revelation.DAMAGE_TYPE in feature.description
		assert character.celestial_revelation_uses == 1
		assert character.celestial_revelation_duration_minutes == 1
		assert character.celestial_revelation_end_action == "No Action"
		_assert_already_gained_vocabulary(
			character.features,
			)

		if revelation is Talarian_Wings:
			assert character.celestial_revelation_fly_speed == 30

		if revelation is Inner_Radiance:
			assert character.celestial_revelation_aura_damage == 3
			assert character.celestial_revelation_aura_radius == 10

		if revelation is Necrotic_Shroud:
			assert character.celestial_revelation_save_dc == 12
			assert character.celestial_revelation_condition == "Frightened"

def _test_aasimar_seed_and_scaling() -> None:
	levels = (
		1,
		3,
		5,
		9,
		13,
		17,
		)
	revelations = []
	healing_dice = []
	extra_damage = []

	for level in levels:
		character = Character(
			seed=359,
			level=level,
			)
		Apply_Species(
			character,
			Aasimar,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)
		healing_dice.append(
			character.healing_hands_dice_count,
			)
		revelation = Current_Revelation(character)

		if level < 3:
			assert revelation is None
			continue

		revelations.append(revelation)
		extra_damage.append(
			character.celestial_revelation_extra_damage,
			)

	assert healing_dice == [
		PB(level)
		for level in levels
		]
	assert len(
		set(
			revelations,
			)
		) == 1
	assert extra_damage == [
		PB(level)
		for level in levels
		if level >= 3
		]


def _test_aasimar_revelation_conflict_is_atomic() -> None:
	character = Character(
		seed=367,
		level=3,
		)
	Apply_Species(
		character,
		Aasimar,
		)
	Talarian_Wings(character)

	try:
		Inner_Radiance(character)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError(
			"Applying a second Celestial Revelation must fail.",
			)

	assert character in Talarian_Wings
	assert character not in Inner_Radiance
	assert Current_Revelation(character) is Talarian_Wings


def _test_goliath_giant_heritage_geometry() -> None:
	assert Goliath.GIANT_HERITAGES == GOLIATH_GIANT_HERITAGES
	assert all(
		heritage.DISPLAY not in HERITAGE_CHOICES
		for heritage in GOLIATH_GIANT_HERITAGES
		)

	for heritage in GOLIATH_GIANT_HERITAGES:
		character = Character(
			seed=373,
			level=1,
			)
		Apply_Species(
			character,
			Goliath,
			)
		heritage(character)

		assert character in Goliath
		assert character in Giant_Heritage
		assert character in heritage
		assert character in Powerful_Build
		assert Current_Giant_Heritage(character) is heritage
		assert character.giant_heritage == heritage.DISPLAY
		assert character.giant_kind == heritage.GIANT_KIND


def _test_goliath_rule_projection() -> None:
	expected_records = {
		Clouds_Jaunt: (
			"giant_heritage_teleport_distance",
			30,
			),
		Fires_Burn: (
			"giant_heritage_damage_dice",
			"1d10",
			),
		Frosts_Chill: (
			"giant_heritage_speed_reduction",
			10,
			),
		Hills_Tumble: (
			"giant_heritage_condition",
			"Prone",
			),
		Stones_Endurance: (
			"giant_heritage_reduction_dice",
			"1d12",
			),
		Storms_Thunder: (
			"giant_heritage_range",
			60,
			),
		}

	for heritage, expected in expected_records.items():
		character = Character(
			seed=379,
			level=5,
			)
		Apply_Species(
			character,
			Goliath,
			)
		heritage(character)
		_completed_ledger(character)
		Resolve_Species_Features(character)

		assert character.giant_heritage_uses == 3
		assert character.giant_heritage_recovery == "Long Rest"
		assert getattr(
			character,
			expected[0],
			) == expected[1]
		assert character in Large_Form
		assert character.large_form_speed == 45
		assert character.large_form_uses == 1
		assert all(
			any(
				feature.name == name
				for feature in character.features
				)
			for name in (
				f"Giant Ancestry: {heritage.DISPLAY}",
				"Powerful Build",
				"Large Form",
				)
			)
		_assert_already_gained_vocabulary(
			character.features,
			)

		if heritage is Stones_Endurance:
			assert character.giant_heritage_ability_modifier == 2
			# Standard dice notation, not spelled out as a sentence: "1d12 + 2"
			# rather than "roll 1d12 and add 2" — and never "add -2" for a
			# negative modifier, which is why the sign is checked, not assumed.
			assert "1d12 + 2" in character.giant_heritage_effect


def _test_goliath_identity_and_scaling() -> None:
	levels = (
		1,
		5,
		9,
		13,
		17,
		)
	heritages = []
	uses = []

	for level in levels:
		character = Character(
			seed=383,
			level=level,
			)
		Apply_Species(
			character,
			Goliath,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)
		heritages.append(
			Current_Giant_Heritage(
				character,
				),
			)
		uses.append(
			character.giant_heritage_uses,
			)

		if level < Large_Form.LEVEL:
			assert character not in Large_Form
			assert not any(
				feature.name == "Large Form"
				for feature in character.features
				)
		else:
			assert character in Large_Form
			assert character.large_form_speed == 45

	assert len(
		set(
			heritages,
			)
		) == 1
	assert uses == [
		PB(level)
		for level in levels
		]


def _test_goliath_heritage_conflict_is_atomic() -> None:
	character = Character(
		seed=389,
		)
	Apply_Species(
		character,
		Goliath,
		)
	Clouds_Jaunt(character)

	try:
		Fires_Burn(character)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError(
			"Applying a second Giant Heritage must fail.",
			)

	assert character in Clouds_Jaunt
	assert character not in Fires_Burn
	assert Current_Giant_Heritage(character) is Clouds_Jaunt
	assert character.giant_heritage == Clouds_Jaunt.DISPLAY


def _test_halfling_trait_geometry_and_records() -> None:
	character = Character(
		seed=397,
		level=1,
		)
	Apply_Species(
		character,
		Halfling,
		)

	assert character in Halfling
	assert character in Brave
	assert character in Halfling_Nimbleness
	assert character in Luck
	assert character in Naturally_Stealthy
	assert character.size == "Small"
	assert character.speed == 30
	assert character.frightened_saving_throw_advantage is True
	assert character.brave_condition == "Frightened"
	assert character.brave_purposes == (
		"Avoid",
		"End",
		)
	assert character.creature_space_passage_size_difference == 1
	assert character.can_stop_in_passed_creature_space is False
	assert character.luck_test == "D20 Test"
	assert character.luck_trigger_roll == 1
	assert character.luck_must_use_new_roll is True
	assert character.naturally_stealthy_action == "Hide"
	assert character.hide_obscuring_creature_size_difference == 1


def _test_halfling_projection_is_stable() -> None:
	levels = (
		1,
		5,
		9,
		13,
		17,
		)

	expected_names = (
		"Halfling",
		"Brave",
		"Halfling Nimbleness",
		"Luck",
		"Naturally Stealthy",
		)
	snapshots = []

	for level in levels:
		character = Character(
			seed=401,
			level=level,
			)
		Apply_Species(
			character,
			Halfling,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)
		Resolve_Species_Features(character)
		species_features = tuple(
			feature
			for feature in character.features
			if feature.source == "Species Feature"
			)

		assert tuple(
			feature.name
			for feature in species_features
			) == expected_names
		assert species_features[0].level == 0
		assert all(
			feature.level == 1
			for feature in species_features[1:]
			)
		assert len(
			species_features,
			) == len(
			expected_names,
			)
		_assert_already_gained_vocabulary(
			species_features,
			)
		snapshots.append(
			tuple(
				(
					feature.name,
					feature.description,
					feature.chips,
					)
				for feature in species_features
				),
			)

	assert len(
		set(
			snapshots,
			)
		) == 1


def _test_orc_trait_geometry_and_records() -> None:
	character = Character(
		seed=409,
		level=1,
		)
	Apply_Species(
		character,
		Orc,
		)

	assert character in Orc
	assert character in Adrenaline_Rush
	assert character in Common_Darkvision
	assert character in Orc_Darkvision
	assert character in Relentless_Endurance
	assert character not in Powerful_Build
	assert character.size == "Medium"
	assert character.speed == 30
	assert character.darkvision == 120
	assert character.adrenaline_rush_action == "Bonus Action"
	assert character.adrenaline_rush_dash_action == "Dash"
	assert character.adrenaline_rush_temporary_hit_point_scaling == (
		"Proficiency Bonus"
		)
	assert character.adrenaline_rush_use_scaling == "Proficiency Bonus"
	assert character.adrenaline_rush_recovery == (
		"Short Rest",
		"Long Rest",
		)
	assert character.relentless_endurance_trigger_hit_points == 0
	assert character.relentless_endurance_result_hit_points == 1
	assert character.relentless_endurance_requires_survivable_damage is True
	assert character.relentless_endurance_uses == 1
	assert character.relentless_endurance_recovery == "Long Rest"


def _test_orc_projection_and_scaling() -> None:
	levels = (
		1,
		5,
		9,
		13,
		17,
		)

	expected_names = (
		"Orc",
		"Adrenaline Rush",
		"Darkvision",
		"Relentless Endurance",
		)
	uses = []
	temporary_hit_points = []

	for level in levels:
		character = Character(
			seed=419,
			level=level,
			)
		Apply_Species(
			character,
			Orc,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)
		Resolve_Species_Features(character)
		species_features = tuple(
			feature
			for feature in character.features
			if feature.source == "Species Feature"
			)

		assert tuple(
			feature.name
			for feature in species_features
			) == expected_names
		assert species_features[0].level == 0
		assert all(
			feature.level == 1
			for feature in species_features[1:]
			)
		assert character.darkvision == 120
		assert character not in Powerful_Build
		_assert_already_gained_vocabulary(
			species_features,
			)
		uses.append(
			character.adrenaline_rush_uses,
			)
		temporary_hit_points.append(
			character.adrenaline_rush_temporary_hit_points,
			)

	assert uses == [
		PB(level)
		for level in levels
		]
	assert temporary_hit_points == uses


def _test_tiefling_heritage_geometry() -> None:
	assert Tiefling.HERITAGES == TIEFLING_HERITAGES
	assert all(
		heritage.__name__ in HERITAGE_CHOICES
		for heritage in TIEFLING_HERITAGES
		)

	for heritage in TIEFLING_HERITAGES:
		character = Character(
			seed=431,
			level=5,
			)
		Apply_Species(
			character,
			Tiefling,
			heritage=heritage,
			)

		assert character in Tiefling
		assert character in heritage
		assert character in Heritage
		assert character in Fiendish_Legacy
		assert character in Otherworldly_Presence
		assert character in Common_Darkvision
		assert character in Humanoid
		assert character not in Fiend
		assert Current_Heritage(character) is heritage
		assert character.damage_resistances == (
			heritage.DAMAGE_RESISTANCE,
			)
		assert character.fiendish_legacy == heritage.__name__
		assert character.fiendish_legacy_damage_resistance == (
			heritage.DAMAGE_RESISTANCE
			)
		assert character.otherworldly_presence_spell == "Thaumaturgy"
		assert character.darkvision == 60
		assert character.speed == 30
		assert character.size in Tiefling.SIZE_OPTIONS
		assert f"{character:Species}" == "Tiefling"
		assert f"{character:Heritage}" == heritage.__name__


def _test_tiefling_rule_projection() -> None:
	expected_spells = {
		Abyssal: (
			"Poison Spray",
			"Ray of Sickness",
			"Hold Person",
			),
		Chthonic: (
			"Chill Touch",
			"False Life",
			"Ray of Enfeeblement",
			),
		Infernal: (
			"Fire Bolt",
			"Hellish Rebuke",
			"Darkness",
			),
		}
	unlock_counts = {
		1: 1,
		3: 2,
		5: 3,
		}

	for heritage, progression in expected_spells.items():
		for level, unlocked_count in unlock_counts.items():
			character = Character(
				seed=433,
				level=level,
				)
			Apply_Species(
				character,
				Tiefling,
				heritage=heritage,
				)
			_completed_ledger(character)
			Resolve_Species_Features(character)
			Resolve_Species_Features(character)
			unlocked_legacy = progression[
				:unlocked_count
				]
			expected_all = (
				"Thaumaturgy",
				*unlocked_legacy,
				)
			expected_free_casts = {
				spell_name: 1
				for spell_name in unlocked_legacy[
					1:
					]
				}
			legacy_feature = next(
				feature
				for feature in character.features
				if feature.name
				== f"Fiendish Legacy: {heritage.__name__}"
				)

			species_features = tuple(
				feature
				for feature in character.features
				if feature.source == "Species Feature"
				)

			assert character.species_spells == expected_all
			assert character.fiendish_legacy_spells == unlocked_legacy
			assert character.fiendish_legacy_free_casts == (
				expected_free_casts
				)
			assert character.species_spell_free_casts == (
				expected_free_casts
				)
			assert character.species_spellcasting_ability in (
				"INT",
				"WIS",
				"CHA",
				)
			assert character.species_spell_save_dc >= 10
			assert character.damage_resistances == (
				heritage.DAMAGE_RESISTANCE,
				)
			assert all(
				spell_name in legacy_feature.description
				for spell_name in unlocked_legacy
				)
			assert all(
				spell_name not in legacy_feature.description
				for spell_name in progression[
					unlocked_count:
					]
				)
			assert tuple(
				feature.name
				for feature in species_features
				) == (
				# The Species pair heads the list; the Legacy Entry closes
				# it, after the traits every Tiefling shares.
				"Tiefling",
				heritage.__name__,
				"Darkvision",
				"Otherworldly Presence",
				f"Fiendish Legacy: {heritage.__name__}",
				)
			_assert_already_gained_vocabulary(
				species_features,
				)


def _test_tiefling_identity_is_level_stable() -> None:
	levels = (
		1,
		3,
		5,
		9,
		13,
		17,
		)
	heritages = []
	sizes = []
	abilities = []
	spell_sets = []

	for level in levels:
		character = Character(
			seed=439,
			level=level,
			)
		Apply_Species(
			character,
			Tiefling,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)
		heritages.append(
			Current_Heritage(
				character,
				),
			)
		sizes.append(
			character.size,
			)
		abilities.append(
			character.species_spellcasting_ability,
			)
		spell_sets.append(
			set(
				character.species_spells,
				),
			)

	assert len(
		set(
			heritages,
			)
		) == 1
	assert len(
		set(
			sizes,
			)
		) == 1
	assert len(
		set(
			abilities,
			)
		) == 1
	assert all(
		earlier.issubset(
			later,
			)
		for earlier, later in zip(
			spell_sets,
			spell_sets[
				1:
				],
			)
		)


def _test_tiefling_heritage_conflict_is_atomic() -> None:
	character = Character(
		seed=443,
		)
	Apply_Species(
		character,
		Tiefling,
		heritage=Abyssal,
		)

	try:
		Infernal(character)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError(
			"Applying a second Tiefling Heritage must fail.",
			)

	assert character in Abyssal
	assert character not in Infernal
	assert Current_Heritage(character) is Abyssal
	assert character.damage_resistances == (
		"Poison",
		)


def _test_elf_heritage_geometry() -> None:
	assert Elf.HERITAGES == ELF_HERITAGES

	for heritage in ELF_HERITAGES:
		character = Character(
			seed=401,
			level=5,
			)

		selected = Apply_Species(
			character,
			Elf,
			heritage=heritage,
			)

		assert selected is Elf
		assert character in heritage
		assert character in Elf
		assert character in Heritage
		assert character in Species
		assert character in Humanoid
		assert Current_Heritage(character) is heritage
		assert f"{character:Species}" == "Elf"
		assert f"{character:Heritage}" == heritage.__name__.replace(
			"_",
			" ",
			)

		# The range is the Heritage's own record: the Dark Elf sees
		# further, and the shared Entry prints whatever the record says.
		assert character.darkvision == heritage.DARKVISION_RANGE

		if heritage is Wood_Elf:
			assert character.speed == 35
		else:
			assert character.speed == 30


def _test_elf_rule_projection() -> None:
	expected = {
		Dark_Elf: (
			"Dancing Lights",
			"Faerie Fire",
			"Darkness",
			),
		High_Elf: (
			"Prestidigitation",
			"Detect Magic",
			"Misty Step",
			),
		Wood_Elf: (
			"Druidcraft",
			"Longstrider",
			"Pass Without Trace",
			),
		}

	for heritage, spells in expected.items():
		character = Character(
			seed=409,
			level=5,
			)
		Apply_Species(
			character,
			Elf,
			heritage=heritage,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)

		assert getattr(
			character.skills,
			character.keen_senses_skill,
			).proficiency_level >= 1
		assert character.species_spells == spells
		assert character.species_spellcasting_ability in (
			"INT",
			"WIS",
			"CHA",
			)
		assert character.species_spell_save_dc >= 10
		assert character.long_rest_hours == 4
		assert character.magic_sleep_immune is True
		entries = {
			feature.name: feature
			for feature in character.features
			}
		assert entries[
			"Darkvision"
			].description == (
			"*Your elven eyes are sharp and your attention focused.*\n\n"
			+ Darkvision_Rules(
				heritage.DARKVISION_RANGE,
				)
			)
		assert entries[
			"Fey Ancestry"
			].description == (
			"*The echoes of the Fae still linger in you, letting you "
			"see through trickery and deception.*\n\n"
			"You have Advantage on saving throws you make to avoid "
			"or end the Charmed condition."
			)
		assert entries[
			"Keen Senses"
			].description == (
			"*Your focus and training can help you perceive your "
			"surroundings and understand your environment.*\n\nYou have proficiency in "
			f"{character.keen_senses_skill}."
			)
		assert entries[
			"Trance"
			].description == (
			"*Elves are said to be made of the same essence as dream and "
			"nightmare. Perhaps there is more than mere poetry to it.*\n\n"
			"You don't need to sleep, and magic can't put you to sleep. "
			"You can finish a Long Rest in 4 hours by meditating."
			)

		assert all(
			any(
				feature.name == name
				for feature in character.features
				)
			for name in (
				"Darkvision",
				"Fey Ancestry",
				"Keen Senses",
				"Trance",
				)
			)


def _test_all_elves_share_common_trait_voice() -> None:
	darkvision_flavour = (
		"*Your elven eyes are sharp and your attention focused.*\n\n"
		)
	fey_ancestry = (
		"*The echoes of the Fae still linger in you, letting you "
		"see through trickery and deception.*\n\n"
		"You have Advantage on saving throws you make to avoid "
		"or end the Charmed condition."
		)

	for heritage in ELF_HERITAGES:
		character = Character(
			seed=413,
			level=5,
			)
		Apply_Species(
			character,
			Elf,
			heritage=heritage,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)

		darkvision = next(
			feature
			for feature in character.features
			if feature.name == "Darkvision"
			)
		ancestry = next(
			feature
			for feature in character.features
			if feature.name == "Fey Ancestry"
			)
		lineage = next(
			feature
			for feature in character.features
			if feature.name.endswith(
				" Elf Lineage",
				)
			)

		assert darkvision.description.startswith(
			darkvision_flavour,
			)
		assert (
			f"within {heritage.DARKVISION_RANGE} feet"
			in darkvision.description
			)
		assert ancestry.description == fey_ancestry
		assert "leveled spells prepared" not in lineage.description
		assert "these spells prepared" in lineage.description


def _test_wood_elf_lineage_progression() -> None:
	expected_by_level = {
		1: (
			"Druidcraft",
			),
		3: (
			"Druidcraft",
			"Longstrider",
			),
		5: (
			"Druidcraft",
			"Longstrider",
			"Pass Without Trace",
			),
		}
	all_spells = expected_by_level[5]

	for level, expected in expected_by_level.items():
		character = Character(
			seed=417,
			level=level,
			)
		Apply_Species(
			character,
			Elf,
			heritage=Wood_Elf,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)
		lineage = next(
			feature
			for feature in character.features
			if feature.name == "Wood Elf Lineage"
			)

		assert "**Spellcasting Ability.**\n\nIntelligence." in (
			lineage.description
			)
		assert lineage.description.startswith(
			"*The woods have always cared for your people. Now their "
			"whispers guide you, their paths open before you, and their "
			"shadows protect you.*",
			)
		assert all(
			f"- {spell_name}" in lineage.description
			for spell_name in expected
			)
		assert all(
			f"- {spell_name}" not in lineage.description
			for spell_name in all_spells
			if spell_name not in expected
			)
		assert (
			"these spells prepared"
			in lineage.description
			) is (
			level >= 3
			)


def _test_elf_identity_is_level_stable() -> None:
	first = Character(
		seed=419,
		level=1,
		)
	progressed = Character(
		seed=419,
		level=5,
		)

	for character in (
		first,
		progressed,
		):
		Apply_Species(
			character,
			Elf,
			)
		_completed_ledger(character)
		Resolve_Species_Features(character)

	assert Current_Heritage(first) is Current_Heritage(progressed)
	assert first.keen_senses_skill == progressed.keen_senses_skill
	assert (
		first.species_spellcasting_ability
		== progressed.species_spellcasting_ability
		)
	assert set(
		first.species_spells,
		).issubset(
		progressed.species_spells,
		)


def _test_gnome_heritage_geometry() -> None:
	assert Gnome.HERITAGES == GNOME_HERITAGES

	for heritage in GNOME_HERITAGES:
		character = Character(
			seed=503,
			level=5,
			)

		selected = Apply_Species(
			character,
			Gnome,
			heritage=heritage,
			)

		assert selected is Gnome
		assert character in heritage
		assert character in Gnome
		assert character in Heritage
		assert character in Species
		assert character in Humanoid
		assert character in Gnomish_Cunning
		assert Current_Heritage(character) is heritage
		assert f"{character:Species}" == "Gnome"
		assert f"{character:Heritage}" == heritage.__name__.replace(
			"_",
			" ",
			)
		assert character.darkvision == 60
		assert character.speed == 30


def _test_gnome_rule_projection() -> None:
	forest = Character(
		seed=509,
		level=5,
		)
	Apply_Species(
		forest,
		Gnome,
		heritage=Forest_Gnome,
		)
	_completed_ledger(forest)
	Resolve_Species_Features(forest)

	assert forest.species_spells == (
		"Minor Illusion",
		"Speak with Animals",
		)
	assert forest.species_spell_free_casts == {
		"Speak with Animals": forest.proficiency_bonus,
		}
	assert forest.species_spellcasting_ability in (
		"INT",
		"WIS",
		"CHA",
		)
	assert forest.species_spell_save_dc >= 10
	assert all(
		any(
			feature.name == name
			for feature in forest.features
			)
		for name in (
			"Darkvision",
			"Gnomish Cunning",
			"Forest Gnome Lineage",
			)
		)

	rock = Character(
		seed=509,
		level=5,
		)
	Apply_Species(
		rock,
		Gnome,
		heritage=Rock_Gnome,
		)
	_completed_ledger(rock)
	Resolve_Species_Features(rock)

	assert rock.species_spells == (
		"Mending",
		"Prestidigitation",
		)
	assert rock.species_spell_free_casts == {}
	assert rock.rock_gnome_device_limit == 3
	assert rock.rock_gnome_device_armor_class == 5
	assert rock.rock_gnome_device_hit_points == 1
	assert rock.rock_gnome_device_duration_hours == 8
	assert rock.rock_gnome_device_casting_minutes == 10
	assert rock.rock_gnome_device_activation == "Bonus Action"
	assert rock.rock_gnome_device_dismantle_action == "Utilize"
	assert rock.rock_gnome_device_requires_touch is True


def _test_gnome_identity_and_scaling() -> None:
	levels = (
		1,
		5,
		9,
		13,
		17,
		)
	random_heritages = []
	abilities = []
	free_casts = []
	save_dcs = []
	spell_sets = []
	device_limits = []

	for level in levels:
		random_character = Character(
			seed=521,
			level=level,
			)
		Apply_Species(
			random_character,
			Gnome,
			)
		random_heritages.append(
			Current_Heritage(
				random_character,
				),
			)

		forest = Character(
			seed=523,
			level=level,
			)
		Apply_Species(
			forest,
			Gnome,
			heritage=Forest_Gnome,
			)
		_completed_ledger(forest)
		Resolve_Species_Features(forest)
		abilities.append(
			forest.species_spellcasting_ability,
			)
		free_casts.append(
			forest.species_spell_free_casts[
				"Speak with Animals"
				],
			)
		save_dcs.append(
			forest.species_spell_save_dc,
			)
		spell_sets.append(
			forest.species_spells,
			)

		rock = Character(
			seed=523,
			level=level,
			)
		Apply_Species(
			rock,
			Gnome,
			heritage=Rock_Gnome,
			)
		_completed_ledger(rock)
		Resolve_Species_Features(rock)
		device_limits.append(
			rock.rock_gnome_device_limit,
			)

	assert len(
		set(
			random_heritages,
			)
		) == 1
	assert len(
		set(
			abilities,
			)
		) == 1
	assert free_casts == [
		PB(level)
		for level in levels
		]
	assert save_dcs == sorted(
		save_dcs,
		)
	assert len(
		set(
			save_dcs,
			)
		) == len(
		levels,
		)
	assert len(
		set(
			spell_sets,
			)
		) == 1
	assert device_limits == [
		Rock_Gnome.DEVICE_LIMIT
		for _ in levels
		]


def _test_gnome_heritage_conflict_is_atomic() -> None:
	character = Character(
		seed=541,
		)
	Apply_Species(
		character,
		Gnome,
		heritage=Forest_Gnome,
		)

	try:
		Rock_Gnome(character)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError(
			"Applying a second Gnome Heritage must fail.",
			)

	assert character in Forest_Gnome
	assert character not in Rock_Gnome
	assert Current_Heritage(character) is Forest_Gnome


def _test_heritage_conflict_is_atomic() -> None:
	character = Character(
		seed=421,
		)
	Apply_Species(
		character,
		Elf,
		heritage=Dark_Elf,
		)

	try:
		Wood_Elf(character)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError(
			"Applying a second Heritage must fail.",
			)

	assert character in Dark_Elf
	assert character not in Wood_Elf
	assert Current_Heritage(character) is Dark_Elf


def _test_heritage_can_infer_elf() -> None:
	character = Character(
		seed=431,
		)

	selected = Apply_Species(
		character,
		heritage=Dark_Elf,
		)

	assert selected is Elf
	assert character in Dark_Elf
	assert character in Elf


def _test_heritage_can_infer_gnome() -> None:
	character = Character(
		seed=547,
		)

	selected = Apply_Species(
		character,
		heritage=Rock_Gnome,
		)

	assert selected is Gnome
	assert character in Rock_Gnome
	assert character in Gnome


def _test_species_conflict_is_atomic() -> None:
	character = Character(
		seed=307,
		)

	Apply_Species(
		character,
		Dwarf,
		)

	try:
		Elf(character)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError(
			"Applying a second Species must fail.",
			)

	assert character in Dwarf
	assert character not in Elf
	assert character.species == "Dwarf"


def _self_test() -> None:
	_test_shared_darkvision_rules()
	_test_playable_species()
	_test_species_declarations_own_the_catalog()
	_test_random_species_is_level_stable()
	_test_human_grants_are_stable()
	_test_human_stateful_grants()
	_test_aasimar_revelation_geometry()
	_test_aasimar_rule_projection()
	_test_aasimar_seed_and_scaling()
	_test_aasimar_revelation_conflict_is_atomic()
	_test_goliath_giant_heritage_geometry()
	_test_goliath_rule_projection()
	_test_goliath_identity_and_scaling()
	_test_goliath_heritage_conflict_is_atomic()
	_test_halfling_trait_geometry_and_records()
	_test_halfling_projection_is_stable()
	_test_orc_trait_geometry_and_records()
	_test_orc_projection_and_scaling()
	_test_tiefling_heritage_geometry()
	_test_tiefling_rule_projection()
	_test_tiefling_identity_is_level_stable()
	_test_tiefling_heritage_conflict_is_atomic()
	_test_elf_heritage_geometry()
	_test_elf_rule_projection()
	_test_all_elves_share_common_trait_voice()
	_test_wood_elf_lineage_progression()
	_test_elf_identity_is_level_stable()
	_test_gnome_heritage_geometry()
	_test_gnome_rule_projection()
	_test_gnome_identity_and_scaling()
	_test_gnome_heritage_conflict_is_atomic()
	_test_heritage_conflict_is_atomic()
	_test_heritage_can_infer_elf()
	_test_heritage_can_infer_gnome()
	_test_species_conflict_is_atomic()
	print("OK — SpeciesKit self-test")


if __name__ == "__main__":
	_self_test()
