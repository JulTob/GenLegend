"""General feats — 2024 PHB catalogue."""

# [Reconstructed 2026-08-31 from compiled bytecode after the working-tree
#  wipe. Declarations are verbatim; see Documenta/Questae for the incident.]

from __future__ import annotations

from AtlasActorLudi.ProficiencyKit import (
	Find_Training_Rank,
	Training_Grant,
	Training_Rank,
	)
from AtlasActorLudi.SkillsKit import (
	Arcana,
	History,
	Insight,
	Investigation,
	Nature,
	Perception,
	Religion,
	SKILLS,
	)
from AtlasInventarium.ToolsKit import (
	Cook_Utensils,
	Poisoners_Kit,
	)
from AtlasLusoris.FeatKit import Make_General_Feat
from AtlasLusoris.FeaturesKit import (
	New_Training_Batch,
	Plan_Feature_Training,
	)


def _Fixed_Training(
		capability,
		purpose: str,
		):
	def Plan(
			char,
			feature,
			):
		return Plan_Feature_Training(
				char,
				feature,
				(
						capability,
						),
				1,
				source='General Feat',
				purpose=purpose,
				allow_trained=True,
				)
	return Plan


def _Proficiency_Or_Expertise(
		char,
		capability,
		) -> Training_Rank:
	if Find_Training_Rank(
			char,
			capability,
			) is None:
		return Training_Rank.PROFICIENT
	return Training_Rank.EXPERTISE


def _Choice_Training(
		candidates,
		purpose: str,
		):
	def Plan(
			char,
			feature,
			):
		eligible = tuple(
				capability
				for capability in candidates
				if Find_Training_Rank(
						char,
						capability,
						) is not Training_Rank.EXPERTISE
				)
		return Plan_Feature_Training(
				char,
				feature,
				eligible if eligible else candidates,
				1,
				source='General Feat',
				purpose=purpose,
				allow_trained=True,
				rank_for=_Proficiency_Or_Expertise,
				)
	return Plan


def _Describe_Resolved_Choice(
		description: str,
		gain,
		) -> str:
	grant = gain.grants[0]
	word = (
			'Expertise'
			if grant.rank is Training_Rank.EXPERTISE
			else 'proficiency'
			)
	first = description.find(
			'Choose ',
			)
	last = description.find(
			'. You can take',
			first,
			)
	if first < 0 or last < 0:
		return description
	resolved = f"You have {word} in {grant.capability.name}"
	return description[:first] + resolved + description[last:]


def _Plan_Skill_Expert(
		char,
		feature,
		):
	untrained = tuple(
			skill
			for skill in SKILLS
			if Find_Training_Rank(
					char,
					skill,
					) is None
			)
	if not untrained:
		raise ValueError(
				'Skill Expert requires one Skill without proficiency.'
				)
	dice = char.Dice_Bag(
			'feat.Skill_Expert.training',
			version='2024',
			namespace='GenLegendTraining',
			)
	proficiency = char.Pick(
			untrained,
			dice=dice,
			)
	trained = tuple(
			skill
			for skill in SKILLS
			if Find_Training_Rank(
					char,
					skill,
					) is Training_Rank.PROFICIENT
			)
	expertise = char.Pick(
			trained if trained else (proficiency,),
			dice=dice,
			)
	grants = [
			Training_Grant(
					capability=proficiency,
					rank=Training_Rank.PROFICIENT,
					),
			]
	if expertise == proficiency:
		grants[0] = Training_Grant(
				capability=proficiency,
				rank=Training_Rank.EXPERTISE,
				)
	else:
		grants.append(
				Training_Grant(
						capability=expertise,
						rank=Training_Rank.EXPERTISE,
						)
				)
	return New_Training_Batch(
			char,
			feature,
			grants,
			source='General Feat',
			)


def _Describe_Skill_Expert(
		description: str,
		gain,
		) -> str:
	proficiency = next(
			(
					grant.capability.name
					for grant in gain.grants
					if grant.rank is Training_Rank.PROFICIENT
					),
			None,
			)
	expertise = next(
			grant.capability.name
			for grant in gain.grants
			if grant.rank is Training_Rank.EXPERTISE
			)
	start = description.find(
			'You gain proficiency',
			)
	if start < 0:
		return description
	resolved = (
			f"You have proficiency in {proficiency} and Expertise in {expertise}."
			if proficiency is not None
			else f"You have Expertise in {expertise}."
			)
	return description[:start] + resolved


AbilityScoreImprovement = Make_General_Feat(
	name='Ability Score Improvement',
	description="Increase one ability score of your choice by 2, or increase two ability scores by 1. You can't increase a score above 20 this way. Repeatable.",
	repeatable=True,
	)

Actor = Make_General_Feat(
	name='Actor',
	description='Increase your Charisma by 1, to a maximum of 20. You have Advantage on Charisma (Deception) and Charisma (Performance) checks to pass yourself off as a different person. You can mimic the speech of another person or the sounds made by other creatures. A creature that hears the mimicry can tell they are imitations with a successful Wisdom (Insight) check against a DC of 8 + your Charisma modifier + your Proficiency Bonus.',
	ability_any=('CHA',),
	asi=('CHA',),
	)

Athlete = Make_General_Feat(
	name='Athlete',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. When you are Prone, standing up uses only 5 feet of movement. You can make a running Long Jump or High Jump after moving only 5 feet.',
	ability_any=('STR', 'DEX'),
	asi=('STR', 'DEX'),
	)

Charger = Make_General_Feat(
	name='Charger',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. When you take the Dash action, your Speed increases by 10 feet for that action. If you move at least 10 feet in a straight line immediately before hitting with a melee attack, choose one: deal an extra 1d8 damage, or push the target up to 10 feet (if it is no more than one size larger).',
	ability_any=('STR', 'DEX'),
	asi=('STR', 'DEX'),
	)

Chef = Make_General_Feat(
	name='Chef',
	description="Increase your Constitution or Wisdom by 1, to a maximum of 20. You have proficiency with Cook's Utensils. As part of a Short Rest, you can cook special food that grants Temporary Hit Points; as part of a Long Rest, you can prepare treats that grant Heroic Inspiration.",
	asi=('CON', 'WIS'),
	training=_Fixed_Training(
			Cook_Utensils,
			'feat.Chef.training',
			),
	training_record='chef',
	)

CrossbowExpert = Make_General_Feat(
	name='Crossbow Expert',
	description="Increase your Dexterity by 1, to a maximum of 20. You ignore the Loading property of Crossbows. Being within 5 feet of an enemy doesn't impose Disadvantage on your attack rolls with Crossbows. When you make an extra attack with a Light Crossbow, you can add your ability modifier to the damage if you aren't already adding it.",
	ability_any=('DEX',),
	asi=('DEX',),
	)

Crusher = Make_General_Feat(
	name='Crusher',
	description='Increase your Strength or Constitution by 1, to a maximum of 20. Once per turn when you hit a creature with Bludgeoning damage, you can move it 5 feet to an unoccupied space if it is no more than one size larger. When you score a Critical Hit that deals Bludgeoning damage, attack rolls against that creature have Advantage until the start of your next turn.',
	asi=('STR', 'CON'),
	)

DefensiveDuelist = Make_General_Feat(
	name='Defensive Duelist',
	description='Increase your Dexterity by 1, to a maximum of 20. When an attack hits you while you are holding a Finesse weapon, you can take a Reaction to add your Proficiency Bonus to your Armor Class against that attack, potentially causing it to miss. This bonus lasts until the start of your next turn.',
	ability_any=('DEX',),
	asi=('DEX',),
	)

DualWielder = Make_General_Feat(
	name='Dual Wielder',
	description="Increase your Strength or Dexterity by 1, to a maximum of 20. When you take the Attack action on your turn and attack with a Light weapon, you can make one extra attack as a Bonus Action with a different one-handed weapon that lacks the Two-Handed property (you don't add your ability modifier to that extra attack's damage unless another feature says you do).",
	ability_any=('STR', 'DEX'),
	asi=('STR', 'DEX'),
	)

Durable = Make_General_Feat(
	name='Durable',
	description='Increase your Constitution by 1, to a maximum of 20. You have Advantage on Death Saving Throws. As a Bonus Action, you can expend and roll one of your Hit Point Dice and regain Hit Points equal to the roll plus your Constitution modifier (minimum of 1 Hit Point).',
	asi=('CON',),
	)

ElementalAdept = Make_General_Feat(
	name='Elemental Adept',
	description='Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. Choose one damage type: Acid, Cold, Fire, Lightning, or Thunder. Spells you cast ignore Resistance to that type, and any 1 on a damage die for that type becomes a 2. Repeatable (choose a different type each time).',
	requires_spellcasting=True,
	repeatable=True,
	asi=('INT', 'WIS', 'CHA'),
	)

FeyTouched = Make_General_Feat(
	name='Fey-Touched',
	description='Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. You learn Misty Step and one level-1 Divination or Enchantment spell of your choice. You can cast each spell once per Long Rest without a spell slot, and you can also cast them with slots you have.',
	asi=('INT', 'WIS', 'CHA'),
	)

FieldMarshal = Make_General_Feat(
	name='Field Marshal',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. Prerequisite: the Field Lieutenant feat or Martial Weapon Proficiency. As a Bonus Action, you can bolster one ally you can see within 30 feet of yourself. That ally gains Temporary Hit Points equal to 2d6 plus the modifier of the ability score increased by this feat. You can take this Bonus Action a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest. You also have Advantage on attack rolls while you are Bloodied.',
	requires_feat_any=(
			'Field Lieutenant',
			'Martial Weapon Training',
			),
	requires_weapon_mastery=True,
	asi=('STR', 'DEX'),
	)

Grappler = Make_General_Feat(
	name='Grappler',
	description="Increase your Strength or Dexterity by 1, to a maximum of 20. You have Advantage on attack rolls against creatures Grappled by you. You can deal damage and Grapple as part of one Unarmed Strike once per turn. Your Speed isn't halved when you move a Grappled creature of your size or smaller.",
	ability_any=('STR', 'DEX'),
	asi=('STR', 'DEX'),
	)

GreatWeaponMaster = Make_General_Feat(
	name='Great Weapon Master',
	description='Increase your Strength by 1, to a maximum of 20. When you hit a creature with a Heavy melee weapon as part of the Attack action, you can deal extra damage equal to your Proficiency Bonus. When you score a Critical Hit or reduce a creature to 0 Hit Points with a melee weapon, you can make one attack with a weapon as a Bonus Action.',
	ability_any=('STR',),
	asi=('STR',),
	)

HeavilyArmored = Make_General_Feat(
	name='Heavily Armored',
	description='Increase your Strength or Constitution by 1, to a maximum of 20. You gain training with Heavy armor.',
	asi=('STR', 'CON'),
	)

HeavyArmorMaster = Make_General_Feat(
	name='Heavy Armor Master',
	description='Increase your Strength or Constitution by 1, to a maximum of 20. While wearing Heavy armor, Bludgeoning, Piercing, and Slashing damage you take from nonmagical attacks is reduced by your Proficiency Bonus.',
	asi=('STR', 'CON'),
	)

InspiringLeader = Make_General_Feat(
	name='Inspiring Leader',
	description='Increase your Wisdom or Charisma by 1, to a maximum of 20. When you finish a Short or Long Rest, you can give inspiring words to up to six allies (including yourself) who can hear you. Each gains Temporary Hit Points equal to your level plus the modifier of the ability you increased with this feat.',
	ability_any=('WIS', 'CHA'),
	asi=('WIS', 'CHA'),
	)

KeenMind = Make_General_Feat(
	name='Keen Mind',
	description='Increase your Intelligence by 1, to a maximum of 20. Choose Arcana, History, Investigation, Nature, or Religion. You gain proficiency in that skill, or Expertise if you already have proficiency. You can take the Study action as a Bonus Action.',
	ability_any=('INT',),
	asi=('INT',),
	training=_Choice_Training(
			(
					Arcana,
					History,
					Investigation,
					Nature,
					Religion,
					),
			'feat.Keen_Mind.training',
			),
	training_record='keen_mind',
	describe_training=_Describe_Resolved_Choice,
	)

def _already_wears_armour(
		target,
		) -> bool:
	"""True when the Character is already trained in armour of any weight."""
	from AtlasLusoris.GuildKit import LightlyArmored as Lightly_Armored_Training
	return target in Lightly_Armored_Training

LightlyArmored = Make_General_Feat(
	name='Lightly Armored',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. You gain training with Light armor and Shields.',
	asi=('STR', 'DEX'),
	redundant_if=_already_wears_armour,
	)

MageSlayer = Make_General_Feat(
	name='Mage Slayer',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. When you damage a creature that is concentrating on a spell, that creature has Disadvantage on the save it makes to maintain Concentration. Once per Short or Long Rest, if you fail an Intelligence, Wisdom, or Charisma saving throw, you can choose to succeed instead.',
	asi=('STR', 'DEX'),
	)

MartialWeaponTraining = Make_General_Feat(
	name='Martial Weapon Training',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. You gain proficiency with Martial weapons.',
	asi=('STR', 'DEX'),
	)

MediumArmorMaster = Make_General_Feat(
	name='Medium Armor Master',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. While wearing Medium armor, you can add up to 3, rather than 2, to your AC if you have a Dexterity of 16 or higher.',
	asi=('STR', 'DEX'),
	)

ModeratelyArmored = Make_General_Feat(
	name='Moderately Armored',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. You gain training with Medium armor and Shields.',
	asi=('STR', 'DEX'),
	)

MountedCombatant = Make_General_Feat(
	name='Mounted Combatant',
	description='Increase your Strength, Dexterity, or Wisdom by 1, to a maximum of 20. While mounted and not Incapacitated, you have Advantage on attack rolls against unmounted creatures smaller than your mount within 5 feet of the mount; you can force an attack targeting the mount to target you instead; and if the mount is subjected to an effect that allows a Dexterity save for half damage, it takes no damage on a success.',
	asi=('STR', 'DEX', 'WIS'),
	)

Observant = Make_General_Feat(
	name='Observant',
	description='Increase your Intelligence or Wisdom by 1, to a maximum of 20. Choose Insight, Investigation, or Perception. You gain proficiency in that skill, or Expertise if already proficient. You can take the Search action as a Bonus Action.',
	ability_any=('INT', 'WIS'),
	asi=('INT', 'WIS'),
	training=_Choice_Training(
			(
					Insight,
					Investigation,
					Perception,
					),
			'feat.Observant.training',
			),
	training_record='observant',
	describe_training=_Describe_Resolved_Choice,
	)

Piercer = Make_General_Feat(
	name='Piercer',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. Once per turn when you hit with Piercing damage, you can reroll one of the damage dice and must use the new roll. When you score a Critical Hit that deals Piercing damage, you can roll one additional damage die.',
	asi=('STR', 'DEX'),
	)

Poisoner = Make_General_Feat(
	name='Poisoner',
	description="Increase your Dexterity or Intelligence by 1, to a maximum of 20. You have proficiency with a Poisoner's Kit. You can apply poison to a weapon or ammunition as a Bonus Action. Poisons you create have a save DC of 8 + the modifier of the ability you increased + your Proficiency Bonus, and you ignore Resistance to Poison damage.",
	asi=('DEX', 'INT'),
	training=_Fixed_Training(
			Poisoners_Kit,
			'feat.Poisoner.training',
			),
	training_record='poisoner',
	)

PolearmMaster = Make_General_Feat(
	name='Polearm Master',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. When you take the Attack action and attack with a Quarterstaff, Spear, Pike, Glaive, Halberd, or Lance, you can use a Bonus Action to make a melee attack with the opposite end (1d4 Bludgeoning). While wielding such a weapon, creatures provoke Opportunity Attacks from you when they enter your reach.',
	ability_any=('STR', 'DEX'),
	asi=('STR', 'DEX'),
	)

Resilient = Make_General_Feat(
	name='Resilient',
	description="Choose one ability score in which you lack saving throw proficiency. Increase that score by 1, to a maximum of 20, and you gain proficiency in that ability's saving throws.",
	asi=(
			'STR',
			'DEX',
			'CON',
			'INT',
			'WIS',
			'CHA',
			),
	)

RitualCaster = Make_General_Feat(
	name='Ritual Caster',
	description='Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. You learn a number of level-1 Ritual spells equal to your Proficiency Bonus from any class lists. They are always prepared for you. You can cast one of them with its normal casting time once per Long Rest without a slot.',
	ability_any=('INT', 'WIS', 'CHA'),
	asi=('INT', 'WIS', 'CHA'),
	)

Sentinel = Make_General_Feat(
	name='Sentinel',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. When you hit a creature with an Opportunity Attack, its Speed becomes 0 for the rest of the turn. Creatures provoke Opportunity Attacks from you even if they take the Disengage action. When a creature within 5 feet of you makes an attack against a target other than you, you can take a Reaction to make a melee attack against the attacking creature.',
	ability_any=('STR', 'DEX'),
	asi=('STR', 'DEX'),
	)

ShadowTouched = Make_General_Feat(
	name='Shadow-Touched',
	description='Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. You learn Invisibility and one level-1 Illusion or Necromancy spell of your choice. You can cast each once per Long Rest without a spell slot, and you can also cast them with slots you have.',
	asi=('INT', 'WIS', 'CHA'),
	)

Sharpshooter = Make_General_Feat(
	name='Sharpshooter',
	description="Increase your Dexterity by 1, to a maximum of 20. Attacking at Long Range doesn't impose Disadvantage on your ranged weapon attack rolls. Your ranged weapon attacks ignore Half Cover and Three-Quarters Cover. Being within 5 feet of an enemy doesn't impose Disadvantage on your ranged weapon attack rolls.",
	ability_any=('DEX',),
	asi=('DEX',),
	)

ShieldMaster = Make_General_Feat(
	name='Shield Master',
	description='Increase your Strength by 1, to a maximum of 20. If you take the Attack action on your turn and hit with a melee weapon while holding a Shield, you can force the target to make a Strength save (DC 8 + your Strength modifier + your Proficiency Bonus) or be pushed 5 feet or knocked Prone. If you are subjected to an effect that allows a Dexterity save for half damage while holding a Shield, you can take a Reaction to take no damage on a success.',
	asi=('STR',),
	)

SkillExpert = Make_General_Feat(
	name='Skill Expert',
	description='Increase one ability score of your choice by 1, to a maximum of 20. You gain proficiency in one skill of your choice, and you gain Expertise in one skill of your choice in which you have proficiency.',
	asi=(
			'STR',
			'DEX',
			'CON',
			'INT',
			'WIS',
			'CHA',
			),
	training=_Plan_Skill_Expert,
	training_record='skill_expert',
	describe_training=_Describe_Skill_Expert,
	)

Skulker = Make_General_Feat(
	name='Skulker',
	description="Increase your Dexterity by 1, to a maximum of 20. You have Blindsight with a range of 10 feet. You have Advantage on Dexterity (Stealth) checks to Hide during combat. If you are Hidden and miss with an attack roll, making the attack doesn't reveal your location.",
	ability_any=('DEX',),
	asi=('DEX',),
	)

Slasher = Make_General_Feat(
	name='Slasher',
	description="Increase your Strength or Dexterity by 1, to a maximum of 20. Once per turn when you hit with Slashing damage, you can reduce the target's Speed by 10 feet until the start of your next turn. When you score a Critical Hit that deals Slashing damage, the target has Disadvantage on attack rolls until the start of your next turn.",
	asi=('STR', 'DEX'),
	)

Speedy = Make_General_Feat(
	name='Speedy',
	description="Increase your Dexterity or Constitution by 1, to a maximum of 20. Your Speed increases by 10 feet. When you take the Dash action on your turn, Difficult Terrain doesn't cost you extra movement. Opportunity Attacks made against you have Disadvantage.",
	ability_any=('DEX', 'CON'),
	asi=('DEX', 'CON'),
	)

SpellSniper = Make_General_Feat(
	name='Spell Sniper',
	description="Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. Your spell attack rolls ignore Half Cover and Three-Quarters Cover. Being within 5 feet of an enemy doesn't impose Disadvantage on your spell attack rolls. When you cast a spell that requires an attack roll and has a range of at least 10 feet, that spell's range increases by 60 feet.",
	requires_spellcasting=True,
	asi=('INT', 'WIS', 'CHA'),
	)

Telekinetic = Make_General_Feat(
	name='Telekinetic',
	description='Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. You learn Mage Hand or improve it (invisible, range +30 feet, Bonus Action control). As a Bonus Action, you can try to telekinetically shove one creature you can see within 30 feet.',
	asi=('INT', 'WIS', 'CHA'),
	)

Telepathic = Make_General_Feat(
	name='Telepathic',
	description='Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. You can speak telepathically to any creature you can see within 60 feet. You also learn Detect Thoughts and can cast it without a spell slot once per Long Rest.',
	asi=('INT', 'WIS', 'CHA'),
	)

WarCaster = Make_General_Feat(
	name='War Caster',
	description='Increase your Intelligence, Wisdom, or Charisma by 1, to a maximum of 20. You have Advantage on Constitution saving throws to maintain Concentration. You can perform the Somatic components of spells even when you have weapons or a Shield in one or both hands. When a creature provokes an Opportunity Attack from you, you can cast a spell that normally has a casting time of one action and targets only that creature instead of making an Opportunity Attack.',
	requires_spellcasting=True,
	asi=('INT', 'WIS', 'CHA'),
	)

WeaponMaster = Make_General_Feat(
	name='Weapon Master',
	description='Increase your Strength or Dexterity by 1, to a maximum of 20. You can use the Weapon Mastery property of one Simple or Martial weapon of your choice with which you have proficiency. You can change the chosen weapon when you finish a Long Rest.',
	asi=('STR', 'DEX'),
	)
