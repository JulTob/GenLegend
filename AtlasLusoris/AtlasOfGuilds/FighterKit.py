"""
FighterKit

The Fighter Guild owns its 2024 progression. Its four Specialization Shapes
publish their own feature, choice, resource, and magic Reports. TrainingKit
materializes those declarations on a Character after statistics and equipment
exist.
"""

# [restored 2026-08-29 from bytecode + session record, after the working-tree
#  wipe. Declarations are verbatim from the compiled module; helper bodies are
#  re-authored to the same behaviour. See Documenta/Questae for the incident.]

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType

from TopKit import Pre, Tag

from AtlasActorLudi.CharactersKit import Report_Of

from AtlasActorLudi.CharactersKit import Character
from AtlasInventarium.ToolsKit import (
	ARTISAN_TOOLS as _ARTISAN_TOOL_DEFINITIONS,
	)
from AtlasLusoris.Compass_of_Progression import (
	Choice_Progression,
	Feature_Grant,
	Resource_Progression,
	)
from AtlasLusoris.GuildKit import Build_Specialization, Fighter


# ---------------------------------------------------------------------------
# Declaration types
#
# Feature_Grant, Choice_Progression and Resource_Progression now live in
# Compass_of_Progression, shared with every Guild; the spellcasting shapes
# below are still the Fighter's alone.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Spellcasting_Rank:
	"""One row of a Specialization spellcasting table."""

	level: int
	cantrips: int
	prepared: int
	slots: tuple[int, int, int, int]

	def __post_init__(self) -> None:
		if not 1 <= self.level <= 20:
			raise ValueError(
				"Spellcasting_Rank level must be between 1 and 20."
				)
		if self.cantrips < 0 or self.prepared < 0 or any(
				slot < 0
				for slot in self.slots
				):
			raise ValueError(
				"Spellcasting_Rank counts cannot be negative."
				)


@dataclass(frozen=True, slots=True)
class Spellcasting_Progression:
	"""Spellcasting context published by a Specialization Shape."""

	ability: str
	spell_list: str
	focus: str
	ranks: tuple[Spellcasting_Rank, ...]

	def __post_init__(self) -> None:
		if self.ability not in (
				"STR",
				"DEX",
				"CON",
				"INT",
				"WIS",
				"CHA",
				):
			raise ValueError(
				"Spellcasting_Progression requires a valid ability."
				)
		if len(
				self.ranks
				) != 20 or not all(
				rank.level == index + 1
				for index, rank in enumerate(
					self.ranks
					)
				):
			raise ValueError(
				"Spellcasting_Progression requires one ordered rank for every level from 1 through 20."
				)

	def at(
			self,
			level: int,
			) -> Spellcasting_Rank:
		return self.ranks[
			min(
				max(
					level,
					1,
					),
				20,
				) - 1
			]


@dataclass(frozen=True, slots=True)
class Prepared_Magic:
	"""A feature-granted spell outside normal slot progression."""

	level: int
	spells: tuple[str, ...]
	ability: str
	uses_slot: bool = True
	uses_components: bool = True
	requires_concentration: bool = True

	def __post_init__(self) -> None:
		if self.level < 1 or not self.spells:
			raise ValueError(
				"Prepared_Magic requires a positive level and spells."
				)


# ---------------------------------------------------------------------------
# The core Fighter progression (PHB 2024)
# ---------------------------------------------------------------------------


FIGHTER_FEATURES = (
	Feature_Grant(1, "Fighting Style"),
	Feature_Grant(1, "Second Wind"),
	Feature_Grant(1, "Weapon Mastery"),
	Feature_Grant(2, "Action Surge"),
	Feature_Grant(2, "Tactical Mind"),
	Feature_Grant(5, "Extra Attack"),
	Feature_Grant(5, "Tactical Shift"),
	Feature_Grant(9, "Indomitable"),
	Feature_Grant(9, "Tactical Master"),
	Feature_Grant(13, "Studied Attacks"),
	)

FIGHTER_CHOICES = (
	Choice_Progression(
			name="Fighting Style",
			gains=(
					(1, 1),
					),
			),
	Choice_Progression(
			name="Weapon Mastery",
			gains=(
					(1, 3),
					(4, 1),
					(10, 1),
					(16, 1),
					),
			),
	Choice_Progression(
			name="General Feat",
			gains=tuple(
					(level, 1)
					for level in (4, 6, 8, 12, 14, 16)
					),
			),
	Choice_Progression(
			name="Epic Boon",
			gains=(
					(19, 1),
					),
			),
	)

FIGHTER_RESOURCES = (
	Resource_Progression(
			name="Second Wind",
			values=(
					(1, "2"),
					(4, "3"),
					(10, "4"),
					),
			),
	Resource_Progression(
			name="Action Surge",
			values=(
					(2, "1"),
					(17, "2"),
					),
			),
	Resource_Progression(
			name="Indomitable",
			values=(
					(9, "1"),
					(13, "2"),
					(17, "3"),
					),
			),
	)

FEATURES = Report_Of(FIGHTER_FEATURES)
CHOICES = Report_Of(FIGHTER_CHOICES)
RESOURCES = Report_Of(FIGHTER_RESOURCES)
Fighter.FEATURES = FEATURES
Fighter.CHOICES = CHOICES
Fighter.RESOURCES = RESOURCES


# ---------------------------------------------------------------------------
# Battle Master maneuvers, as selectable Tags
# ---------------------------------------------------------------------------


class Maneuver(Tag):
	"""A Battle Master maneuver selected by a Character."""

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
				target,
				Character,
				)


_MANEUVER_TAGS: dict[str, type[Maneuver]] = {}


def _class_name(
		name: str,
		) -> str:
	return "".join(
		ch
		for ch in name.title()
		if ch.isalnum()
		)


def _Build_Maneuver(
		name: str,
		description: str,
		) -> type[Maneuver]:
	tag = type(
		_class_name(
			name
			),
		(
			Maneuver,
			),
		{
			"NAME": name,
			"DESCRIPTION": description,
			"__module__": __name__,
			},
		)
	_MANEUVER_TAGS[
		name
		] = tag
	return tag


Ambush = _Build_Maneuver(
		"Ambush",
		"Add a Superiority Die to a Stealth check or Initiative roll.",
		)
Bait_and_Switch = _Build_Maneuver(
		"Bait and Switch",
		"Trade places with a willing nearby creature and improve one ally's AC.",
		)
Commanders_Strike = _Build_Maneuver(
		"Commander's Strike",
		"Replace one attack so an ally can strike with their Reaction.",
		)
Commanding_Presence = _Build_Maneuver(
		"Commanding Presence",
		"Add a Superiority Die to Intimidation, Performance, or Persuasion.",
		)
Disarming_Attack = _Build_Maneuver(
		"Disarming Attack",
		"Add damage and force the target to save or drop a held object.",
		)
Distracting_Strike = _Build_Maneuver(
		"Distracting Strike",
		"Add damage and give the next other attacker Advantage.",
		)
Evasive_Footwork = _Build_Maneuver(
		"Evasive Footwork",
		"Disengage as a Bonus Action and add the die to AC for the turn.",
		)
Feinting_Attack = _Build_Maneuver(
		"Feinting Attack",
		"Gain Advantage against a nearby target and add damage on a hit.",
		)
Goading_Attack = _Build_Maneuver(
		"Goading Attack",
		"Add damage and hinder the target's attacks against anyone else.",
		)
Lunging_Attack = _Build_Maneuver(
		"Lunging Attack",
		"Dash as a Bonus Action and empower a melee hit after a straight advance.",
		)
Maneuvering_Attack = _Build_Maneuver(
		"Maneuvering Attack",
		"Add damage and let an ally reposition safely with their Reaction.",
		)
Menacing_Attack = _Build_Maneuver(
		"Menacing Attack",
		"Add damage and force the target to save against being Frightened.",
		)
Parry = _Build_Maneuver(
		"Parry",
		"Use a Reaction to reduce damage from a melee attack.",
		)
Precision_Attack = _Build_Maneuver(
		"Precision Attack",
		"Add a Superiority Die after an attack misses, possibly turning it into a hit.",
		)
Pushing_Attack = _Build_Maneuver(
		"Pushing Attack",
		"Add damage and push a Large or smaller target away on a failed save.",
		)
Rally = _Build_Maneuver(
		"Rally",
		"Grant a nearby ally Temporary Hit Points as a Bonus Action.",
		)
Riposte = _Build_Maneuver(
		"Riposte",
		"Use a Reaction to counterattack a creature that misses you in melee.",
		)
Sweeping_Attack = _Build_Maneuver(
		"Sweeping Attack",
		"Carry part of a melee hit into a second creature within reach.",
		)
Tactical_Assessment = _Build_Maneuver(
		"Tactical Assessment",
		"Add a Superiority Die to History, Investigation, or Insight.",
		)
Trip_Attack = _Build_Maneuver(
		"Trip Attack",
		"Add damage and knock a Large or smaller target Prone on a failed save.",
		)

MANEUVERS = MappingProxyType(
	_MANEUVER_TAGS
	)

FIGHTER_SKILLS = (
	"Acrobatics",
	"Animal Handling",
	"Athletics",
	"History",
	"Insight",
	"Intimidation",
	"Perception",
	"Persuasion",
	"Survival",
	)

# Display names of the Artisan's Tools, from ToolsKit's one list (QST-0116).
ARTISAN_TOOLS = tuple(
	tool.name
	for tool in _ARTISAN_TOOL_DEFINITIONS
	)


# ---------------------------------------------------------------------------
# Battle Master (3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------


BATTLE_MASTER_FEATURES = (
	Feature_Grant(3, "Combat Superiority"),
	Feature_Grant(3, "Student of War"),
	Feature_Grant(7, "Know Your Enemy"),
	Feature_Grant(10, "Improved Combat Superiority"),
	Feature_Grant(15, "Relentless"),
	Feature_Grant(18, "Ultimate Combat Superiority"),
	)

BATTLE_MASTER_CHOICES = (
	Choice_Progression(
			name="Maneuver",
			gains=(
					(3, 3),
					(7, 2),
					(10, 2),
					(15, 2),
					),
			options=tuple(
					MANEUVERS
					),
			),
	Choice_Progression(
			name="Artisan's Tools",
			gains=(
					(3, 1),
					),
			options=ARTISAN_TOOLS,
			),
	Choice_Progression(
			name="Fighter Skill",
			gains=(
					(3, 1),
					),
			options=FIGHTER_SKILLS,
			),
	)

BATTLE_MASTER_RESOURCES = (
	Resource_Progression(
			name="Superiority Dice",
			values=(
					(3, "4d8"),
					(7, "5d8"),
					(10, "5d10"),
					(15, "6d10"),
					(18, "6d12"),
					),
			),
	)


def _stable_choices(
		character,
		choice: Choice_Progression,
		bag_purpose: str,
		) -> tuple[str, ...]:
	options = list(
		choice.options
		)
	dice_bag = character.Dice_Bag(
		bag_purpose,
		version="1",
		namespace="GenLegendFighter",
		)
	dice_bag.shuffle(
		options
		)
	return tuple(
		options[
			:choice.total_at(
					character.level
					)
			]
		)


def Resolve_Battle_Master_Choices(
		character,
		) -> tuple[str, ...]:
	"""Resolve stable maneuver, tool, and skill Records."""
	maneuver_choice = BATTLE_MASTER_CHOICES[0]
	maneuver_names = _stable_choices(
		character,
		maneuver_choice,
		"fighter.battle_master.maneuvers",
		)
	character.maneuvers = maneuver_names

	tool = _stable_choices(
		character,
		BATTLE_MASTER_CHOICES[1],
		"fighter.battle_master.student.tool",
		)
	skill = _stable_choices(
		character,
		BATTLE_MASTER_CHOICES[2],
		"fighter.battle_master.student.skill",
		)
	character.battle_master_tool = (
		tool[0]
		if tool
		else None
		)
	character.battle_master_skill = (
		skill[0]
		if skill
		else None
		)
	return maneuver_names


def Apply_Battle_Master_Choices(
		character,
		) -> tuple[type[Maneuver], ...]:
	"""Apply the resolved Maneuver Tags after Battle Master commits."""
	maneuver_names = Resolve_Battle_Master_Choices(
		character
		)
	selected = tuple(
		MANEUVERS[
			name
			]
		for name in maneuver_names
		)
	for maneuver in selected:
		if character not in maneuver:
			maneuver(
				character
				)
	return selected


BATTLE_MASTER_DESCRIPTION = (
	"You trained in strategy.\n\n"
	"Every guard, every feint, every way a body can be made to move, to "
	"doubt, to fail. You train every technique you can find. Generations "
	"of people found them, argued about them, gave them names, and you "
	"learned the names. When the moment comes you are not improvising. "
	"You are planning.\n\n"
	"That is the difference. Others see a fight. You see a position, and "
	"you have the winning move."
	)
BattleMaster = Build_Specialization(
	guild=Fighter,
	name="Battle Master",
	module=__name__,
	reports={
			"FEATURES": BATTLE_MASTER_FEATURES,
			"CHOICES": BATTLE_MASTER_CHOICES,
			"RESOURCES": BATTLE_MASTER_RESOURCES,
			},
	awaken=Resolve_Battle_Master_Choices,
	after=Apply_Battle_Master_Choices,
	extends=BATTLE_MASTER_DESCRIPTION,
	heading="Battle Master",
	)


# ---------------------------------------------------------------------------
# Banneret (3 / 3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------
# Forgotten Realms: Heroes of Faerun, 2024.  Every feature spends a resource
# the Fighter already owns on somebody else: Group Recovery rides Second Wind,
# Rallying Surge rides Action Surge, Shared Resilience rides Indomitable.
# Nothing here is a new pool, which is why it declares FEATURES and no
# RESOURCES of its own.


BANNERET_FEATURES = (
	Feature_Grant(3, "Knightly Envoy"),
	Feature_Grant(3, "Group Recovery"),
	Feature_Grant(7, "Team Tactics"),
	Feature_Grant(10, "Rallying Surge"),
	Feature_Grant(15, "Shared Resilience"),
	Feature_Grant(18, "Inspiring Commander"),
	)

BANNERET_DESCRIPTION = (
	"You trained leadership. How to inspire. How to be a symbol. How to "
	"stand first and hold the line.\n\n"
	"People listen to you through thick and thin, because you go first. "
	"Because they trust you. You have to earn that every day. There is "
	"too much at stake. If the line falls, so does the army, so does the "
	"battle, so does the war. A banner is not a weapon. A banner is not "
	"always a flag. It is the symbol that stays up so the rest know where "
	"the line is. You are that symbol. You do not get to fall."
	)

Banneret = Build_Specialization(
	guild=Fighter,
	name="Banneret",
	module=__name__,
	reports={
			"FEATURES": BANNERET_FEATURES,
			# Every Banneret feature counts allies by the Charisma modifier,
			# so a Banneret rolled on the Guild's own STR/CON lifts exactly
			# one ally and the whole subclass does nothing.  It leans CHA
			# before the Guild speaks, the way the Eldritch Knight leans INT.
			"ABILITY_PREFERENCE": (
					"CHA",
					),
			},
	extends=BANNERET_DESCRIPTION,
	heading="Banneret",
	)


# ---------------------------------------------------------------------------
# Champion (3 / 3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------


CHAMPION_FEATURES = (
	Feature_Grant(3, "Improved Critical"),
	Feature_Grant(3, "Remarkable Athlete"),
	Feature_Grant(7, "Additional Fighting Style"),
	Feature_Grant(10, "Heroic Warrior"),
	Feature_Grant(15, "Superior Critical"),
	Feature_Grant(18, "Survivor"),
	)

CHAMPION_CHOICES = (
	Choice_Progression(
			name="Additional Fighting Style",
			gains=(
					(7, 1),
					),
			),
	)

CHAMPION_DESCRIPTION = (
	"You train your body beyond your own limits.\n\n"
	"You want to become a Champion. To be victorious. To take the laurel. "
	"You have the will to fight, to compete, to stand across from someone "
	"you look up to and find out what you are made of. You want to be the "
	"last one standing, with the whole arena chanting your name.\n\n"
	"The others call it luck. You have noticed it comes most often on the "
	"days you did the work."
	)

Champion = Build_Specialization(
	guild=Fighter,
	name="Champion",
	module=__name__,
	reports={
			"FEATURES": CHAMPION_FEATURES,
			"CHOICES": CHAMPION_CHOICES,
			},
	extends=CHAMPION_DESCRIPTION,
	heading="Champion",
	)


# ---------------------------------------------------------------------------
# Eldritch Knight (3 / 3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------


ELDRITCH_KNIGHT_FEATURES = (
	Feature_Grant(3, "Spellcasting"),
	Feature_Grant(3, "War Bond"),
	Feature_Grant(7, "War Magic"),
	Feature_Grant(10, "Eldritch Strike"),
	Feature_Grant(15, "Arcane Charge"),
	Feature_Grant(18, "Improved War Magic"),
	)

ELDRITCH_KNIGHT_MAGIC = Spellcasting_Progression(
	ability="INT",
	spell_list="Wizard",
	focus="Arcane Focus",
	ranks=(
			Spellcasting_Rank(1, 0, 0, (0, 0, 0, 0)),
			Spellcasting_Rank(2, 0, 0, (0, 0, 0, 0)),
			Spellcasting_Rank(3, 2, 3, (2, 0, 0, 0)),
			Spellcasting_Rank(4, 2, 4, (3, 0, 0, 0)),
			Spellcasting_Rank(5, 2, 4, (3, 0, 0, 0)),
			Spellcasting_Rank(6, 2, 4, (3, 0, 0, 0)),
			Spellcasting_Rank(7, 2, 5, (4, 2, 0, 0)),
			Spellcasting_Rank(8, 2, 6, (4, 2, 0, 0)),
			Spellcasting_Rank(9, 2, 6, (4, 2, 0, 0)),
			Spellcasting_Rank(10, 3, 7, (4, 3, 0, 0)),
			Spellcasting_Rank(11, 3, 8, (4, 3, 0, 0)),
			Spellcasting_Rank(12, 3, 8, (4, 3, 0, 0)),
			Spellcasting_Rank(13, 3, 9, (4, 3, 2, 0)),
			Spellcasting_Rank(14, 3, 10, (4, 3, 2, 0)),
			Spellcasting_Rank(15, 3, 10, (4, 3, 2, 0)),
			Spellcasting_Rank(16, 3, 11, (4, 3, 3, 0)),
			Spellcasting_Rank(17, 3, 11, (4, 3, 3, 0)),
			Spellcasting_Rank(18, 3, 11, (4, 3, 3, 0)),
			Spellcasting_Rank(19, 3, 12, (4, 3, 3, 1)),
			Spellcasting_Rank(20, 3, 13, (4, 3, 3, 1)),
			),
	)


def _prepared_gains() -> tuple[tuple[int, int], ...]:
	"""The prepared-spell column as level gains, straight off the table."""
	gains = []
	previous = 0
	for rank in ELDRITCH_KNIGHT_MAGIC.ranks:
		if rank.prepared > previous:
			gains.append(
				(
					rank.level,
					rank.prepared - previous,
					)
				)
			previous = rank.prepared
	return tuple(
		gains
		)


ELDRITCH_KNIGHT_CHOICES = (
	Choice_Progression(
			name="Wizard Cantrip",
			gains=(
					(3, 2),
					(10, 1),
					),
			),
	Choice_Progression(
			name="Prepared Wizard Spell",
			gains=_prepared_gains(),
			),
	)

ELDRITCH_KNIGHT_DESCRIPTION = (
	"You trained tricks. That's how you learnt magic.\n\n"
	"Nobody ever told you why any of it works. What you have is a "
	"sequence: this movement, this word, in this order, and then the "
	"thing happens. You learnt it the way you learnt a disarm, by doing "
	"it wrong four hundred times in a row. Then you did it right four "
	"hundred more.\n\n"
	"A wizard once called that a bag of tricks. They were right. You have a "
	"knack for them."
	)

EldritchKnight = Build_Specialization(
	guild=Fighter,
	name="Eldritch Knight",
	module=__name__,
	reports={
			"FEATURES": ELDRITCH_KNIGHT_FEATURES,
			"CHOICES": ELDRITCH_KNIGHT_CHOICES,
			"MAGIC": ELDRITCH_KNIGHT_MAGIC,
			# Casts from INT, so it leans there before the Guild's own CON.
			"ABILITY_PREFERENCE": (
					"INT",
					),
			},
	extends=ELDRITCH_KNIGHT_DESCRIPTION,
	heading="Eldritch Knight",
	)


# ---------------------------------------------------------------------------
# Psi Warrior (3 / 7 / 10 / 15 / 18)
# ---------------------------------------------------------------------------
# One training, three methods. The branch reads the Order axis and never
# Morality, because the split it models is methodological rather than moral:
# the Order subordinates the self to keep a shared thing standing, the
# individual exalts the self and answers to nobody, and the third refuses both
# readings. The two source manuals in Documenta/Sources/Jedi are the argument
# for it in their very form. One is a single Code in a single voice. The other
# is six authors bound into one volume who agree on nothing, and its compiler
# says so in the preface.
#
# Neutral is the unmarked absence of an Order Tag, so it is the default branch
# rather than a third case. Across 120 generated Characters the split runs
# roughly 38 / 24 / 38, so all three are load-bearing.


PSI_WARRIOR_FEATURES = (
	Feature_Grant(3, "Psionic Power"),
	Feature_Grant(7, "Telekinetic Adept"),
	Feature_Grant(10, "Guarded Mind"),
	Feature_Grant(15, "Bulwark of Force"),
	Feature_Grant(18, "Telekinetic Master"),
	)

PSI_WARRIOR_RESOURCES = (
	Resource_Progression(
			name="Psionic Energy Dice",
			values=(
					(3, "4d6"),
					(5, "6d8"),
					(9, "8d8"),
					(11, "8d10"),
					(13, "10d10"),
					(17, "12d12"),
					),
			),
	)

PSI_WARRIOR_MAGIC = Prepared_Magic(
	level=18,
	spells=(
			"Telekinesis",
			),
	ability="INT",
	uses_slot=False,
	uses_components=False,
	requires_concentration=True,
	)

PSI_WARRIOR_METHODS = {
	"Lawful": (
		"Fear is the first death. You must not fear. Fear stirs the mind. "
		"So does love. So does grief. So does anger. You look at them, "
		"and let the course flow over you. They pass. You do not. "
		"Discipline. Master yourself."
		),
	"Chaotic": (
		"Fear is the first spark. Fear means you are brave, and not "
		"stupid. You listen to your emotions, as they show the path of "
		"least resistance. You are a fire burning bright, and they are "
		"the winds that fuel you. You are your own master."
		),
	"Neutral": (
		"Fear is just one form. You flow with your emotions. You face "
		"your fears, as they hold what you need. You let their currents "
		"take you, slowly and surely. You become the river. You break "
		"the stone. You calm the fire. You master the moment."
		),
	}

PSI_WARRIOR_OPENING = (
	"You train your emotions. Your feelings. Fear, grief, fury, love... "
	"You are in control."
	)

# The closing is shared on purpose: it is the one thing all three methods
# agree on, which is what makes them three answers to one question rather
# than three subclasses.
PSI_WARRIOR_CLOSING = (
	"You do understand one thing: the true battle is internal and "
	"precedes the blade."
	)


def Psi_Warrior_Method(
		character,
		) -> str:
	"""Which of the three disciplines this Character took, by the Order axis."""
	from AtlasActorLudi.AlignmentKit import Chaotic, Lawful

	if character in Lawful:
		return "Lawful"
	if character in Chaotic:
		return "Chaotic"
	return "Neutral"


def Psi_Warrior_Description(
		character,
		) -> str:
	"""Project the Psi Warrior's discipline for this Character."""
	return "\n\n".join(
		(
			PSI_WARRIOR_OPENING,
			PSI_WARRIOR_METHODS[
				Psi_Warrior_Method(
					character
					)
				],
			PSI_WARRIOR_CLOSING,
			)
		)


PsiWarrior = Build_Specialization(
	guild=Fighter,
	name="Psi Warrior",
	module=__name__,
	reports={
			"FEATURES": PSI_WARRIOR_FEATURES,
			"RESOURCES": PSI_WARRIOR_RESOURCES,
			"MAGIC": PSI_WARRIOR_MAGIC,
			},
	extends=Psi_Warrior_Description,
	heading="Psi Warrior",
	)

SPECIALIZATIONS = Fighter.SPECIALIZATIONS


# ---------------------------------------------------------------------------
# Focused self-test
# ---------------------------------------------------------------------------


def _feature_names(
		owner,
		) -> tuple[str, ...]:
	return tuple(
		grant.name
		for grant in owner
		)


def _self_test() -> None:
	assert "Fighting Style" in _feature_names(
		FIGHTER_FEATURES
		)
	assert FIGHTER_CHOICES[0].name == "Fighting Style"
	assert FIGHTER_CHOICES[2].total_at(20) == 6

	assert len(
		MANEUVERS
		) == 20
	assert BATTLE_MASTER_CHOICES[0].total_at(3) == 3
	assert BATTLE_MASTER_CHOICES[0].total_at(20) == 9
	assert BATTLE_MASTER_RESOURCES[0].at(18) == "6d12"

	assert PSI_WARRIOR_RESOURCES[0].values == (
		(3, "4d6"),
		(5, "6d8"),
		(9, "8d8"),
		(11, "8d10"),
		(13, "10d10"),
		(17, "12d12"),
		)
	assert PsiWarrior.MAGIC.spells == (
		"Telekinesis",
		)
	assert sorted(
		PSI_WARRIOR_METHODS
		) == [
		"Chaotic",
		"Lawful",
		"Neutral",
		]

	assert ELDRITCH_KNIGHT_MAGIC.at(20).prepared == 13
	assert ELDRITCH_KNIGHT_CHOICES[1].total_at(20) == 13
	assert ELDRITCH_KNIGHT_MAGIC.at(13).slots == (4, 3, 2, 0)

	names = {
		spec.NAME
		for spec in SPECIALIZATIONS
		}
	assert names >= {
		"Battle Master",
		"Banneret",
		"Champion",
		"Eldritch Knight",
		"Psi Warrior",
		}
	print(
		"OK — FighterKit self-test"
		)


if __name__ == "__main__":
	_self_test()
