"""
Great Grimoire of Characters.
Player rites for the Character skeleton (CharactersKit).
Rules from D&D 5e.

Public construction: New_Player (summons TBD in AtlasActorLudi).
Character here extends the skeleton with interim player rites — peel these
into Player Actions / nested Species·Guild·Background Tags over time.
"""
from Minion import guardian, watcher, warden, spy, minion, changeling
''' Cartography '''


# The two stand-ins below import late for the same reason every rite in this
# file does: AtlasNomina and AtlasEpica both reach back here, and a top-level
# import would close the circle. Wrapping them keeps @changeling's argument
# resolvable at class-definition time without paying that price.

def _last_resort_name(char):
	"""Rung three for a Character's name."""
	from AtlasNomina.Map_of_Names import LastResortName
	return LastResortName(char)


def _last_resort_title(character):
	"""Rung three for a Character's title."""
	from AtlasEpica.Map_of_Titles import LastResortTitle
	return LastResortTitle(character)


from AtlasActorLudi.Map_of_Size import Size
# Import statements grouped for clarity and error checking
try: # Cartography
	from AtlasLudus.Map_of_Languages import Character_Languages
	from AtlasActorLudi.Map_of_Scores import PB, Modifier
	from AtlasLusoris.AbilityScoresKit import AbilityScores
	from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScoresPlus
	from AtlasActorLudi.Grimoire_of_SavingThrows import SavingThrows
	from AtlasActorLudi.Grimoire_of_Skills import Char_Skills, get_other_proficiencies
	from AtlasLusoris.BackgroundKit import (
			Apply_Background,
			)
	from AtlasLusoris.Grimoire_of_Spellcasters import spellcaster
	from AtlasActorLudi.CharactersKit import (
			Character as Character_Skeleton,
			Player,
			)
	from AtlasActorLudi.GendersKit import Gender_Reveal

except ImportError:
	raise


def New_Player(
		char,
		name=None,
		species=None,
		char_class=None,
		subclass=None,
		specialization=None,
		background=None,
		level=1,
		gender=None,
		alignment=None,
		heritage=None,
		title=None,
		**_,
		):
	"""Build one Player from an already seeded Character shell."""
	Player(
		char
		)

	char.level = max(1, int(level))

	from AtlasActorLudi.AlignmentKit import New_Alignment
	New_Alignment(
		char,
		alignment,
		)

	from AtlasActorLudi.SpeciesKit import Apply_Species
	Apply_Species(
		char,
		species,
		heritage=heritage,
		)

	Gender_Reveal(
		char,
		gender,
		)

	from AtlasLusoris.GuildKit import (
			Apply_Guild,
			Apply_Specialization,
			)
	Apply_Guild(
			char,
			char_class,
			)
	Apply_Specialization(
			char,
			specialization
			if specialization is not None
			else subclass,
			)
	Apply_Background(
			char,
			background,
			)

	~char
	char.set_combat_attributes()
	char.set_stats()
	char.set_char_features()

	char.name = name or char.New_name()
	char.title = title or char.New_title()
	# The Species description addresses the Character by name, and the name is
	# only settled here.  Refresh that one Entry now it exists.
	from AtlasActorLudi.SpeciesKit.resolution import Project_Species_Description
	Project_Species_Description( char )
	# The Guild description composes across layers and may name the Character
	# too, so it is projected from here for the same reason.
	from AtlasLusoris.GuildKit import Project_Guild_Description
	Project_Guild_Description( char )
	# set_Objects was a SECOND equipment pass that re-rolled the budget and
	# clobbered the first one's spending. GearKit outfits exactly once inside
	# set_char_features, so this pass is gone.
	# Story can fail on sparse myth pools; must not roll back Player Imprint.
	try:
		char.setStory()
	except Exception:
		char.story = ""
	return char


# Stable alias used by AtlasActorLudi.Map_of_Character_Generation.
awaken_player = New_Player


def _creature_type_line(
	char,
	creature_type,
	) -> str:
	"""The rules type, with kinship in parentheses where there is one."""
	from AtlasActorLudi.SpeciesKit.kinship import Kinships_Of

	if creature_type is None:
		return ""

	kin = Kinships_Of( char )

	if not kin:
		return creature_type.__name__

	return f"{creature_type.__name__} ({', '.join(kin)})"


class Character(Character_Skeleton):
	"""Character skeleton + interim player rites (migrate → Player Tag Actions)."""

	@minion
	def set_combat_attributes(char):
		~char
		if getattr(
			char,
			"speed",
			None,
			) is None:
			char.speed = 30
		char.AS = AbilityScores(
			character=char
			)
		char.AC = 10 + Modifier(char.AS.DEX)
		char.base_health = 0
		char.set_Health()
		char.HitPointDie = char.CalculateHPD()
		return char

	@minion
	def set_stats(char):
		from AtlasLusoris.BackgroundKit import (
				Apply_Background_Abilities,
				Apply_Background_Training,
				)

		~char
		char.New_stats()
		Apply_Background_Abilities(
				char
				)
		# set_combat_attributes ran before the real roll, so its AC came from
		# placeholder 10s. Rebase the unarmored AC on the Dexterity we rolled.
		char.AC = 10 + Modifier(char.AS.DEX)
		char.set_Skills()
		Apply_Background_Training(
				char
				)
		return char

	@minion
	def set_char_features(char):
		from AtlasLusoris.Grimoire_of_Features import Feature
		from AtlasLusoris.OrderKit import Resolve_Order_Features

		~char
		char.known_spells = []
		Resolve_Order_Features(
				char
				)
		char.languages = Character_Languages(char)
		char.lineage = getattr(
				char,
				"lineage",
				None,
				)
		# Gear lives on `char.belongings` as Tagged Items; `char.equipment`
		# is a derived view of it (see GearKit.Loadout).
		char.belongings = []
		char.purse = 0

		char.features: list[Feature] = list(
				getattr(
					char,
					"features",
					[],
					) or []
				)
		from AtlasActorLudi.SpeciesKit import Resolve_Species_Features
		Resolve_Species_Features(
				char
				)
		char.apply_species_features()
		char.apply_background_features()

		# Gear BEFORE Guild training, so a lesson can look at what this
		# Character actually carries — Weapon Mastery names the weapons in
		# their hands instead of picking from the catalogue at random.
		from AtlasInventarium.GearKit import (
				Loadout,
				Outfit_Player,
				current_armour_class,
				)
		Outfit_Player(char)
		char.equipment = Loadout(char)

		char.apply_class_features()
		Resolve_Species_Features(
				char
				)
		seen = set()
		unique = []
		for feat in char.features:
			if not feat:
				continue
			key = (getattr(feat, "name", None), getattr(feat, "description", 	None))
			if key in seen:
				continue
			seen.add(key)
			unique.append(feat)
		char.features = unique

		char.skills.sync_with_abilities(char.AS)
		char.other_proficiencies = get_other_proficiencies(char.skills, char)
		# AC stays DERIVED from what is equipped, so an artifact's bonus is
		# summed rather than written over the natural formula.
		char.AC = current_armour_class(char)

		char.saving_throws = char.Saving_Throws()
		char.attack_rolls = AbilityScoresPlus(char.AS, char.proficiency_bonus)
		char.spellcaster = char.get_spellcaster()
		Resolve_Order_Features(
				char
				)
		return char


	@minion
	def setStory(char):
		from AtlasEpica.Map_of_Stories import Story
		char.story = Story(char)


	@minion
	def apply_background_features(char):
		"""Background contributions are applied during Character awakening."""
		return char


	@minion
	def apply_species_features(char):
		if getattr(
			char,
			"species",
			None,
			) in (
				"Aasimar",
				"Dragonborn",
				"Dwarf",
				"Goliath",
				"Halfling",
				"Human",
				"Elf",
				"Gnome",
				"Orc",
				"Tiefling",
				):
			return char

		from AtlasLusoris.Map_of_Species import species_features

		for feature in species_features(
			char.species,
			char,
			):
			feature(
				char
				)
			char.features.append(
				feature
				)

		return char

	@property
	@minion
	def health(char):
		result = char.base_health + Modifier(char.AS.CON) * char.level
		# Anything that grants Hit Points per level (Dwarven Toughness today,
		# the Tough feat tomorrow) adds itself to bonus_health_sources, and is
		# summed onto bonus_health_per_level.  Nothing here needs to know which.
		result += int(
			getattr(
				char,
				"bonus_health_per_level",
				0,
				) or 0
			) * char.level
		return result

	@minion
	def CalculateHPD(char):
		from AtlasLusoris.Map_of_Classes import health_dice
		dice = health_dice(char.char_class)
		return f"{char.level}D{dice}"

	@minion
	def set_Health(char):
		""" Calculate character health
			based on level and constitution modifier.
		"""
		from AtlasLusoris.Map_of_Classes import health_dice
		dice_value = health_dice(char.char_class)
		char.base_health = dice_value
		return char

	@minion
	def get_spellcaster(char):
		from AtlasLusoris.Grimoire_of_Spellcasters import spellcaster
		char.spellcaster = spellcaster(char)
		return char.spellcaster


	@property
	@minion
	def passive_perception(char):
		try:
			Mod = char.skills.Perception.calculate_modifier()
			return 10 + Mod
		except Exception:
			return 10  # Fallback

	@guardian
	def SetFeatures(char):
		from AtlasLusoris.Map_of_Classes import (
				GetFeatures,                 # main entry-point to get features list
				health_dice
				)
		GetFeatures(char)
		return char


	@minion
	def apply_class_features(character):
		from AtlasLusoris.Map_of_Classes import get_class_progression
		from AtlasLusoris.Map_of_Classes import (
				GetFeatures,                 # main entry-point to get features list
				health_dice
				)
		# TOP Training Tags first (Guild lessons); legacy Progression fills gaps.
		from AtlasLusoris.TrainingKit import (
				Apply_Guild_Trainings,
				filter_legacy_features,
				)
		Apply_Guild_Trainings(
				character
				)
		class_prog = get_class_progression(character)
		if class_prog:
			legacy = class_prog.features(
					character
					)
			character.features += filter_legacy_features(
					character,
					legacy,
					)
		return character


	@property
	def abilities(char):
		return char.AS

	@minion
	def Saving_Throws(char):
		"""Assign saving throw proficiencies from the Guild chassis."""
		from AtlasLusoris.GuildKit import guild_saves
		profs = list(
				guild_saves(
						char
						) or ()
				)
		return SavingThrows(
			char.AS,
			char.proficiency_bonus,
			profs,
			is_character=True,
			)


	@property
	@minion
	def character_class(char):
		return char.char_class

	@property
	@minion
	def race(char):
		from AtlasLusoris.Map_of_Species import species_to_race_and_subrace
		race, subrace = species_to_race_and_subrace(
			char.species,
			char,
			)
		return race

	@property
	@minion
	def subrace(char):
		from AtlasLusoris.Map_of_Species import species_to_race_and_subrace
		race, subrace = species_to_race_and_subrace(
			char.species,
			char,
			)
		return subrace

	@property
	@minion
	def guild(char):
		return char.char_class

	@property
	def Level(char):
		return char.level

	@property
	def Subclass(char):
		return char.subclass

	@property
	def Specialization(char):
		return char.specialization

	@minion
	def New_subclass(char):
		"""Compatibility route to the primary Guild's specific Shapes."""
		from AtlasLusoris.GuildKit import (
				Apply_Specialization,
				)
		tag = Apply_Specialization(
				char
				)

		return (
			tag.NAME
			if tag is not None
			else None
			)

	@changeling(_last_resort_name)
	def New_name(char):
		"""
		Generate or assign a name.

		Was @warden @guardian: two hundred attempts at the same thing. ``~char``
		reseeds from the *fixed* seed, so every one of those attempts replayed
		the identical dice into the identical failure. The Changeling steps
		sideways instead.
		"""
		from AtlasNomina.Map_of_Names import NewName
		~char
		# Use the existing name generation functions
		name = NewName(char)
		return name

	@changeling(_last_resort_title)
	def New_title(character):
		""" Generate or assign a title. """
		from AtlasEpica.Map_of_Titles import Title
		~character
		# Defensive: ensure the attribute exists
		if not hasattr(character, "title"):
			character.title = None
		return Title(character)

	@minion
	def to_dict(char):
		""" Convert character details to dictionary format. """
		from AtlasActorLudi.SpeciesKit import (
				Current_Creature_Type,
				Current_Heritage,
				)
		from AtlasLusoris.GuildKit import casting_title
		from AtlasLusoris.Map_of_Classes.Scroll_of_Constants import Archetype
		from AtlasInventarium.ToolsKit import Find_Practice_Entries
		creature_type = Current_Creature_Type( char )
		heritage = Current_Heritage( char )
		practices = tuple(
			practice.to_dict()
			for practice in Find_Practice_Entries(
				char
				)
			)
		return {
			'name': 		char.name,
			'title':		char.title,
			'Gender': 		char.gender,
			# "Humanoid (Celestial)": the rules answer, then what they resemble.
			# The kinship is parenthetical because it is never the rules answer;
			# a spell seeking Celestials still does not find an Aasimar.
			'CreatureType': _creature_type_line(
				char,
				creature_type,
				),
			'Species': 		f"{char:Species}",
			'Heritage': (
				heritage.__name__.replace(
					"_",
					" ",
					)
				if heritage is not None
				else ""
				),
			'Class': 		char.char_class,
			# What to print for the class.  Separate from 'Class' on purpose:
			# that one is the identity string, read back on regeneration and
			# looked up in GUILDS, so it must stay the plain Guild name.
			'Class_Title':	casting_title(
				char
				),
			# What to print for the class.  Separate from 'Class' on purpose:
			# that one is the identity string, read back on regeneration and
			# looked up in GUILDS, so it must stay the plain Guild name.
			'Class_Title':	casting_title(
				char
				),
			'Subclass': 	Archetype(char),
			'Specialization': char.specialization,
			'Background': 	char.background,
			'Level': 		char.level,
			'Seed': 		char.seed,
			'Stats': 		char.stats,
			'Alignment': 	char.alignment,
			'Skills': 		char.skills,
			'AC': 			char.AC,
			'Health': 		char.health,
			'PB':			char.proficiency_bonus,
			'size':			char.size,
			'passive_perception':		char.passive_perception,
			'other_proficiencies':		char.other_proficiencies,
			'Practices':	practices,
			'features':		char.features,
			'equipment': 	char.equipment,
			'SavingThrow':  char.saving_throws,
			'AttackRolls':	char.attack_rolls,
			'Spellcaster':	char.spellcaster,
			'Speed':		char.speed,
			'HPD':			char.HitPointDie,
			'Languages':	char.languages,
			'Story': 		char.story

			}

	@minion
	def NPCfy(char):
		from AtlasActorLudi.AtlasAlusoris import summon_nonplayer

		pc_to_npc = summon_nonplayer(
			race=char.race,
			guild=char.char_class,
			background=char.background,
			level=char.level,
			seed=char.seed,
			)
		return pc_to_npc

	@property
	def genus(char):
		"""
		Compute the Character (pc)'s genus as a string of tags.

		Mimics the NPC genus structure to maintain compatibility
		with functions like Title(), Descriptor(), etc.
		"""
		attributes = [
			str(char.race or ""),
			str(char.subrace or ""),
			str(char.char_class or ""),
			str(char.background or ""),
			str(char.specialization or ""),
			str(char.gender or ""),
			str(char.alignment or ""),
			]
		delimiter = " , "
		return delimiter.join(filter(None, attributes))

	@property
	def Type(char):
		# Build a string that includes species and other descriptors
		descriptors = [str(char.species)]
		descriptors.append(str(char.gender))
		descriptors.append(str(char.race))
		descriptors.append(str(char.subrace))
		#descriptors.append(str(char.background))
		# Combine descriptors into a single string
		return ' '.join(descriptors)

	@minion
	def roll_stat(char, dice=None):
		rolls = [
			char.Roll(
				6,
				dice=dice,
				)
			for _ in range(4)
			]
		return sum(sorted(rolls)[1:])

	@property
	def stats(self) -> dict[str,int]:
		return {
			"Strength":     self.abilities.STR,
			"Dexterity":    self.abilities.DEX,
			"Constitution": self.abilities.CON,
			"Intelligence": self.abilities.INT,
			"Wisdom":       self.abilities.WIS,
			"Charisma":     self.abilities.CHA,
			}

	@minion
	def New_stats(char):
		~char
		from AtlasLusoris.GuildKit import ability_weights, ABILITY_KEYS
		weights = ability_weights(char, amount=0)
		sorted_keys = sorted(
			ABILITY_KEYS,
			key=lambda name: (
				-weights.get(name, 0),
				ABILITY_KEYS.index(name)
			)
		)

		# Roll six ability scores
		~char
		# One Bag for the whole array, so the scores a Character rolls no
		# longer depend on how many other draws happened before this line.
		scores_bag = char.Dice_Bag(
				"identity.scores",
				version="1",
				namespace="GenLegendActor",
				)
		rolled_stats = [
			char.roll_stat(
				dice=scores_bag,
				)
			for _ in range(6)
			]
		rolled_stats.sort(reverse=True)
			# Sort from highest to lowest

		stats_by_key = {}
		for key, val in zip(sorted_keys, rolled_stats):
			stats_by_key[key] = val

		# Update the character's ability scores
		if char.AS:
			char.AS.STR = stats_by_key['STR']
			char.AS.DEX = stats_by_key['DEX']
			char.AS.CON = stats_by_key['CON']
			char.AS.INT = stats_by_key['INT']
			char.AS.WIS = stats_by_key['WIS']
			char.AS.CHA = stats_by_key['CHA']

		_key_to_fullname = {
			"STR": "Strength",
			"DEX": "Dexterity",
			"CON": "Constitution",
			"INT": "Intelligence",
			"WIS": "Wisdom",
			"CHA": "Charisma",
		}
		stats = {
			fullname: stats_by_key[key]
			for key, fullname in _key_to_fullname.items()
		}
		return stats

	@minion
	def set_Skills(char):
		""" Assign skill proficiencies
			based on character class.

			Background skills and tools are granted by
			``Apply_Background_Training`` after this builds the sheet.
		"""
		from AtlasLusoris.AtlasOfFeatures.Unarmored_Defense import (
				Unarmored_Defense,
				)

		char.skills = Char_Skills(
			AS=char.AS,
			ProficiencyBonus=char.proficiency_bonus,
			)
		~char

		# Step 2: Set default skills based on class
		if char.character_class:
			if char.character_class == "Fighter":
				char.skills.activate_proficiencies(2, [
					"Acrobatics",
					"Animal Handling",
					"Athletics",
					"History",
					"Insight",
					"Intimidation",
					"Perception",
					"Persuasion",
					"Survival",
					])
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Martial_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()
				char.skills.Medium.set_proficiency()
				char.skills.Heavy.set_proficiency()
				char.skills.Shields.set_proficiency()


			elif char.character_class == "Wizard":
				char.skills.activate_proficiencies(2, [
					"Arcana",
					"History",
					"Insight",
					"Investigation",
					"Medicine",
					"Religion",
					])
				char.skills.Simple_Weapons.set_proficiency()
			elif char.character_class == "Rogue":
				char.skills.Thieves_Tools.set_proficiency()
				char.skills.activate_proficiencies(4, [
					"Acrobatics",
					"Athletics",
					"Deception",
					"Insight",
					"Intimidation",
					"Investigation",
					"Perception",
					"Persuasion",
					"Sleight of Hand",
					"Stealth",
					])
				char.skills.activate_expertise(
					2,
					char.skills.get_proficient_skills()
					)
				if char.level >= 6:
					char.skills.activate_expertise(
						2,
						char.skills.get_proficient_skills()
						)
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Finesse.set_proficiency()
				char.skills.Light_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()
			elif char.character_class == "Cleric":
				char.skills.activate_proficiencies(2, [
					"History",
					"Insight",
					"Medicine",
					"Persuasion",
					"Religion",
					])
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()
				char.skills.Medium.set_proficiency()
				char.skills.Shields.set_proficiency()
			elif char.character_class == "Ranger":
				char.skills.activate_proficiencies(3, [
					"Animal Handling",
					"Athletics",
					"Insight",
					"Investigation",
					"Nature",
					"Perception",
					"Stealth",
					"Survival",
					])
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Martial_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()
				char.skills.Medium.set_proficiency()
				char.skills.Shields.set_proficiency()
			elif char.character_class == "Paladin":
				char.skills.activate_proficiencies(2, [
					"Athletics",
					"Insight",
					"Intimidation",
					"Medicine",
					"Persuasion",
					"Religion",
					])
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Martial_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()
				char.skills.Medium.set_proficiency()
				char.skills.Heavy.set_proficiency()
				char.skills.Shields.set_proficiency()
			elif char.character_class == "Bard":
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()

				char.skills.Musical_Instrument.set_proficiency()
				char.skills.activate_proficiencies(3, [
					"Athletics",
					'Acrobatics',
					'Sleight of Hand',
					'Stealth',
					'Arcana',
					'History',
					'Investigation',
					'Nature',
					'Religion',
					'Animal Handling',
					'Insight',
					'Medicine',
					'Perception',
					'Survival',
					'Deception',
					'Intimidation',
					'Performance',
					'Persuasion',
					])
				if char.level >= 2:
					# Expertise is granted by its own Training Tag, in
					# AtlasOfTraining/Map_of_Bard_Training.py, because the
					# Background has not taught its two skills yet and the
					# pool here is too small to double twice.
					char.skills.activate_jack_of_all_trades()
				if (
						getattr(
							char,
							"specialization",
							None,
							) == "Dance"
						and char.level >= 3
						):
					Unarmored_Defense(
							char,
							ability="CHA",
							shield_allowed=False,
							)
			elif char.character_class == "Monk":
				Unarmored_Defense(
						char,
						ability="WIS",
						shield_allowed=False,
						)
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Light_Weapons.set_proficiency()
				char.skills.activate_proficiencies(2, [
					"Acrobatics",
					"Athletics",
					"History",
					"Insight",
					"Religion",
					"Stealth",
					])

				# One Artisan's Tool or Musical Instrument, planned in the
				# training ledger (QST-0116): the sheet built a moment ago does
				# not yet show what the Background and its Feat taught, so a
				# pick read off it could spend the proficiency on a known tool.
				from AtlasActorLudi.ProficiencyKit import (
					Apply_Training_Record,
					Commit_Training_Gain,
					Ensure_Training_Record,
					)
				from AtlasInventarium.ToolsKit import (
					ARTISAN_TOOLS,
					MUSICAL_INSTRUMENTS,
					)
				from AtlasLusoris.FeaturesKit import Plan_Feature_Training
				from AtlasLusoris.GuildKit import Monk as Monk_Guild

				if any(
						batch.grant_id == "Guild.Monk.tool"
						for batch in Ensure_Training_Record(char).gains
						):
					Apply_Training_Record(char)
				else:
					monk_tool = Plan_Feature_Training(
						char,
						Monk_Guild,
						( *ARTISAN_TOOLS, *MUSICAL_INSTRUMENTS ),
						1,
						source="Class Proficiency",
						purpose="guild.Monk.tool",
						grant_id="Guild.Monk.tool",
						allow_short=True,
						)
					if monk_tool is not None:
						Commit_Training_Gain(char, monk_tool)
			elif char.character_class == "Druid":
				char.skills.Light.set_proficiency()
				char.skills.Shields.set_proficiency()
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Herbalism_Kit.set_proficiency()
				char.skills.activate_proficiencies(2, [
					"Arcana",
					"Animal Handling",
					"Insight",
					"Medicine",
					"Nature",
					"Perception",
					"Religion",
					"Survival",
					])
			elif char.character_class == "Warlock":
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()
				char.skills.activate_proficiencies(2, [
					"Arcana",
					"Deception",
					"History",
					"Intimidation",
					"Investigation",
					"Nature",
					"Religion",
					])
			elif char.character_class == "Sorcerer":
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.activate_proficiencies(2, [
					"Arcana",
					"Deception",
					"Insight",
					"Intimidation",
					"Persuasion",
					"Religion",
					])
			elif char.character_class == "Barbarian":
				# Always two.  The third that a level-3 Barbarian gets comes
				# from Primal Knowledge, which grants it itself so that the
				# feature entry can name the skill instead of saying "of your
				# choice" for a choice already made.  See
				# AtlasLusoris/AtlasOfTraining/Map_of_Barbarian_Training.py.
				char.skills.activate_proficiencies(2, [
					"Animal Handling",
					"Athletics",
					"Intimidation",
					"Nature",
					"Perception",
					"Survival",
					])
				if char.level >= 3:
					from AtlasLusoris.AtlasOfTraining.Map_of_Barbarian_Training import (
						Grant_Primal_Knowledge_Skill,
						)
					Grant_Primal_Knowledge_Skill(char)
				char.skills.Simple_Weapons.set_proficiency()
				char.skills.Martial_Weapons.set_proficiency()
				char.skills.Light.set_proficiency()
				char.skills.Medium.set_proficiency()
				char.skills.Shields.set_proficiency()
				Unarmored_Defense(
						char,
						ability="CON",
						shield_allowed=True,
						)
		return

	@property
	def proficiency_bonus(char):
		return PB(char.level)

	@property
	def PB(char):
		return char.proficiency_bonus

	@minion
	def set(char):
		~char
