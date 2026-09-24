# AtlasPugna.Map_of_Legendary_Actions

''' Cartography '''
import random
try:
	from AtlasLudus.Map_of_Dice import Dice
	from AtlasActorLudi.Map_of_Scores import PB
	from AtlasAlusoris.Grimoire_of_NPC import NPC
	import AtlasPugna.Map_of_Attacks as attacks
	from AtlasScriptum.Map_of_Formats import Entry_Text
except ModuleNotFoundError:
	raise



def Num_Legendary_Actions(npc: NPC) -> int:
	"""
	Calculate the number of legendary actions an NPC can perform.
	Returns:
	<< 	[int]: Number of legendary actions.
		Dice returns a random integer 1-n, or n-1 if n<1

	Args:
	>>	npc [NPC]: The NPC character.
	"""
	pb = npc.pb
	n = min(pb // 3,4)
	n = max(0,n)
	result = Dice(n)
	return result

def NumLegendaryAction(npc):
	return Num_Legendary_Actions(npc)

def Resistances(npc: NPC) -> str:
	"""
	Determine if the NPC has legendary resistances and return a formatted string.

	Returns:
	<<	[str]: Formatted string describing the NPC's legendary resistances, or an empty string if none.

	Args:
	>>	<npc> [NPC]: The NPC character.

	"""
	# Define the minimum level required for legendary resistances
	LEVEL_THRESHOLD = 10 + Dice(20)

	res = 0
	if Dice(npc.level) >= LEVEL_THRESHOLD:
		res = Dice(3)
		result = (f"<h3>Legendary Resistance ({res}/Rest)</h3>"
			f"If {npc.title} fails a saving throw, {npc.gender} can choose to succeed instead. \n"
			)
	else:
		result = ""
	return result

def Legendary(npc: NPC) -> str:
	"""
	Generate a description of the NPC's legendary actions.

	Args:
		npc (NPC): The NPC character.

	Returns:
		str: A formatted string describing the NPC's legendary actions.
	"""
	num = Num_Legendary_Actions(npc)
	if num <= 0:
		# Exit
		return ""
	result = ""
	result += Resistances(npc)
	result += LegendaryHeader(npc, num)
	result += LegendaryActions(npc, num)
	return result

def LegendaryHeader(npc, num) -> str:
	# Determine pluralization
	s = "s" if num > 1 else ""
	result = f"<h3>Legendary Actions</h3>"
	result += f"{npc.title} gains {num} legendary action{s} charge{s} at the end of their turn. "
	result += f"Charges can be spent when using a Legendary Action, choosing from the options below. "
	result += f"\n\t Only one legendary action can be used at a time, and only at the end of another creature's turn."
	return result

def LegendaryActions(npc, num) -> str:
	''' Returns:
		<<	A string with the Actions put together.
		'''
	actions = set()
	result = ""
	for i in range(num):
		actions.add(LegendaryAction(npc))
	for action in actions:
		result += f"{action}\n"
	return result

def LegendaryAction(npc = None) -> str:
	from AtlasScriptum.Map_of_Formats import Entry_Text
	from AtlasAlusoris.Map_of_Archetypes import Archetype
	from AtlasAlusoris.Map_of_Races import Race, Subrace

	if not npc:
		pass  # no NPC for legendary actions

	race = npc.race if npc else Race()
	subrace = npc.subrace if npc else Subrace()
	background = npc.archetype if npc else Archetype()
	lvl = npc.level if npc else Dice(20)
	actions = []
	num = NumLegendaryAction(npc) if npc else 1
	pb = PB(lvl)
	power_dc = 8+pb
	magic_dc = npc.spell_save_dc if npc else 10
	dc = max(power_dc,magic_dc)
	STR = npc.AS.str_mod if npc else 0
	DEX = npc.AS.dex_mod if npc else 0
	CON = npc.AS.con_mod if npc else 0
	CHA = npc.AS.cha_mod if npc else 0
	WIS = npc.AS.wis_mod if npc else 0
	title = npc.title  if npc else "The character"
	alignment = npc.alignment

	intensity = Dice(PB(pb-1))
	dice_size = 2*(1+Dice(5))
	roll = f"{intensity}D{dice_size}"

	# General actions
	Detect = Entry_Text(
			"Detect",
			f"{title} makes a Wisdom (Perception) check. {title} can use this check to find a hidden creature, spot, hear, or otherwise detect the presence of something."
			)
	Attack = Entry_Text(
		f"Attack",
		f"{title} can do one simple attack to any creature")
	Move = Entry_Text(
		f"Move",
		f"{title} can move half their movement")
	WingAttack = Entry_Text(
		f"Wing Attack",
		random.choice([
			f"{title} beats its wings. Each creature within 10 feet of {title} must succeed on a DC{power_dc + STR} DEX saving throw or take {3*2 + STR} (2d6{STR:+}) bludgeoning damage and be knocked prone.",
			f"Each creature within 10 feet must succeed on a DC {power_dc+STR} DEX save or take {Dice(intensity)}d6 + {STR} bludgeoning damage and be knocked prone."]),
		f"(Costs 2 Actions)")
	CommandAlly = Entry_Text(
		f"Command Ally",
		f"{title} issues a command to one of its allies, allowing the ally to immediately take an extra action on {title}'s turn.")
	RadiantBlast = Entry_Text(
		f"Radiant Blast",
		f"{title} releases a burst of radiant energy, targeting one creature it can see within 60 feet. The target must succeed on a Wisdom saving throw DC {dc} or take {Dice(intensity)}d6 radiant damage and be blinded until the end of {title}'s next turn.")
	TailSweep = Entry_Text(
		"Tail Sweep",
		f"{title} makes a tail attack against all creatures within 10 feet. Each must succeed on a DC {power_dc+STR} Dexterity saving throw or take {Dice(intensity)}d6 bludgeoning damage and be knocked prone.")
	FrightfulPresence = Entry_Text(
		"Frightful Presence",
		f"Each creature of {title}'s choice within {5*Dice(2)*Dice(3)} feet and aware of it must succeed on a Wisdom saving throw or become frightened for 1 minute."        )
	MindWarp = Entry_Text(
		"Mind Warp",
		f"{title}  targets one creature it can see within 60 feet, assaulting its mind. The target must make a DC {dc} Intelligence saving throw or take {Dice(intensity)}d6 psychic damage and be stunned until the end of {title}'s next turn."        )
	WarpReality = Entry_Text(
		"Warp Reality",
		f"{title} alters reality in a small area, creating difficult terrain within {5*Dice(2)*Dice(3)} feet."        )
	DeathlyTouch = Entry_Text(
		"Deathly Touch",
		f"{title} touches one creature, forcing it to make a DC {dc} Constitution saving throw or take {Dice(intensity)}d4 necrotic damage."        )
	BattleCry = Entry_Text(
		f"Battle Cry",
		f"{title} rallies their allies, granting them courage. All allies that can hear, within {Dice(2)*Dice(2)*Dice(3)*5} feet, become immune to the Frightened condition for 1 minute."        )
	DeadlyGaze = Entry_Text(
		f"Deadly Gaze",
		f"The target becomes frightened on a failed DC{dc} Wisdom saving throw.")
	DeathTouch = Entry_Text(
		f"Death Touch",
		f"{title} delivers a chilling touch, causing {Dice(intensity)}d4 necrotic damage on a successful attack.",        )
	TerrifyingVisage = Entry_Text(
		f"Terrifying Visage",
		f"{title} reveals its horrifying true form, causing all nearby enemies to make a DC{dc} Wisdom saving throw or become frightened."        )
	TacticalManeuver = Entry_Text(
		f"Tactical Maneuver",
		f"{title} directs an ally, granting advantage to their next attack.")
	InspiringDisplay = Entry_Text(
		f"Inspiring Display",
		f"{title} coordinates a stunning display, inspiring an ally within sight to take an extra action.")
	SwarmTactics = Entry_Text(
			f"Swarm Tactics",
			f"{title} directs its allies in a coordinated attack, all allies within {Dice(2)*Dice(3)*10} feet of {title} can move up to half their speed.")
	SwiftMovement = Entry_Text(
		"Swift Movement",
		f"{title} uses their knowledge of the terrain to move quickly or create an escape route. {title} moves up to their speed without provoquing opportunity attacks.")
	LuckyBreak = Entry_Text(
		f"Lucky Break",
		f"{title} provoques disadvantage to the next attack targeted at them.",)
	SneakyStrike = Entry_Text(
		f"Sneaky Strike",
		f"{title} makes a stealthy attack, gaining advantage if the target has an enemy within 5 feet of them.")
	NimbleDodge = Entry_Text(
		f"Nimble Dodge",
		f"{title} moves quickly, gaining a +2 AC until the start of their turn.")
	SerpentineGrace = Entry_Text(
		f"Serpentine Grace",
		f"{title} slithers quickly, avoiding attacks and repositioning itself. {title} moves half his speed without provoking opportunity attacks")
	VenomousBite = Entry_Text(
	   f"Venomous Bite",
	   f"{title} delivers a poisonous bite to a creature it can reach within 5 feet. On a hit of a melee weapon attack the target receives {Dice(PB(intensity))}d4 poison damage, and becomes poisoned")
	QuickFix = Entry_Text(
		f"Quick Fix",
		f"{title} can use a cantrip that takes 1 Action.")
	DeceptiveManeuver = Entry_Text(
		f"Deceptive Maneuver",
		f"{title} confuses an enemy, causing it to have disadvantage on its next attack.")
	ProtectiveShift = Entry_Text(
		f"{race} Shift",
		f"{title} alters their body, gaining resistance to a damage type of its choice until its next turn.")
	ElementalBlast = Entry_Text(
		f"Elemental Blast",
		random.choice([
			f"{title} sends out a burst of elemental energy in a line, requiring a DC{dc} Dexterity saving throw from affected creatures or take {Dice(intensity)}d6 {attacks.Damage()} damage."
			f"{title} sends out a burst of elemental energy in a cone, requiring a DC{dc} Dexterity saving throw from affected creatures or take {Dice(intensity)}d4 {attacks.Damage()} damage.",
			]))
	BeguilingGaze = Entry_Text(
		f"Beguiling Gaze",
		random.choice([
			f"{title} targets one creature it can see, charming it, unless the target succeeds on a DC{dc} Wisdom saving throw.",
			f"{title} targets one creature it can see, putting it to sleep, unless the target succeeds on a DC{dc} Wisdom saving throw."
			]))
	NaturesWrath = Entry_Text(
		f"Nature's Wrath",
		f"{title} summons vines or thorns in an area within {5*Dice(2)*Dice(2)*Dice(2)*Dice(3)}, making it difficult terrain. Every creature that starts its turn within the area takes 1d4 damage."
		)
	HellfireBlast = Entry_Text(
		f"Hellfire Blast",
		f"{title} releases a burst of hellfire, causing {Dice(intensity)}d4 fire damage to all creatures within {5*Dice(2)*Dice(2)*Dice(3)} area."        )
	MinionCommand = Entry_Text(
		f"Infernal Command",
		f"{title} commands his minions to attack a target creature, allowing them to attack immediately, using their reaction to do an attack to that target.")
	MightyThrow = Entry_Text(
		f"Mighty Throw",
		f"{title} throws a large rock or similar object at a target, causing {Dice(intensity)}d6 damage on impact.")
	Stomp = Entry_Text(
		f"Stomp",
		f"{title} stomps the ground, creating a shockwave within {5*Dice(2)*Dice(3)} feet that knocks nearby creatures prone unless they succeed on a DC{power_dc+STR} Strength saving throw.")
	IngeniousTrap = Entry_Text(
		f"Ingenious Trap",
		random.choice([
			f"{title} quickly assembles and sets a trap, which can ensnare a creature within 5 feet of it, making it prone, unless the target succeeds on a DC{dc} Dexterity saving throw.",
			f"{title} quickly assembles and sets a trap, which can damage a creature within 5 feet of it, making 1d6 of {attacks.Damage()} damage, unless the target succeeds on a DC{dc} Dexterity saving throw.",
			]))
	SmallEscape = Entry_Text(
		f"{race}'s Escape",
		random.choice([
			f"{title} teleports up to {Dice(2)*Dice(3)*5} feet.",
			f"{title} becomes temporarily invisible until the start of their turn."
			]))
	SneakyStab = Entry_Text(
		f"Sneaky Stab",
		f"{title} makes a sudden simple melee attack with advantage on its attack roll."),
	Disappear = Entry_Text(
		f"Disappear",
		f"{title} blends into its surroundings, becoming hidden to its enemies. Any wisdomm check to discern his location and Ranged attack rolls have disadvantage.")
	QuickTinkerer = Entry_Text(
		f"Quick Tinkerer",
		f"{title} quickly activates a tinkered device that, on a failed Dexterity saving throw DC{dc}, blinds an enemy within 5ft of {title} until the end ot the next creature's turn.")
	ScaledDefense = Entry_Text(
		f"Scaled Defense",
		f"{title} hardens its scales, gaining +2 AC until the start of their turn.")
	SwiftReptile = Entry_Text(
		f"Swift Reptile",
		f"{title} scapes swiftly, moving up to their speed without provoking opportunity attacks.")
	TerrifyingRoar = Entry_Text(
		f"Terrifying Roar",
		f"{title} emits a fearsome roar, causing an enemy within 5 feet to become frightened on a failed DC{power_dc+CHA} Wisdom saving throw.")
	RendNTear = Entry_Text(
		f"Rend and Tear",
		f"{title} makes a special or normal attack against a single target.")
	Engulf = Entry_Text(
		f"Engulf",
		f"{title} attempts to engulf a nearby smaller creature, trapping it inside its body, unless the creature succeeds a DC {power_dc+STR} Dexterity Saving Throw, being restrained on a fail.")
	CorrosiveTouch = Entry_Text(
		f"Corrosive Touch",
		f"{title} makes a simple melee attack, dealing an extra {Dice(intensity)}d6 acid damage on a hit.")
	WarCry = Entry_Text(
		f"War Cry",
		f"{title} lets out a powerful cry, bolstering the morale of allies and intimidating enemies. Within {Dice(2)*Dice(2)*Dice(3)*5} feet, all allies of {title} become immune to the Frightened condition, and enemies within the range make a DC {dc} Wisdom saving throw or become Frightened")
	BrutalStrike = Entry_Text(
		f"Brutal Strike",
		f"{title} makes a simple attack. On a hit, the target becomes Prone.")
	EntanglingRoots = Entry_Text(
		f"Entangling Roots",
		f"{title} causes roots to burst from the ground, attempting to entangle nearby creatures. The terrain within {Dice(2)*Dice(3)*5} feet becomes difficult terrain. {title} is immune to this effect.")
	HealSelf = Entry_Text(
		f"Heal Self",
		f"{title} magically regains {2*4+CON} (2d8 + {CON}) hit points.",
		"(Costs 3 Actions)")
	HealingFlux = Entry_Text(
		f"Healing Flux",
		f"{title} exudes restorative energy, healing itself or an ally within 5 feet. The target heals 1d4{WIS:+}")
	TacticalAmbush = Entry_Text(
		f"Tactical Ambush",
		f"{title} uses his cunning and gains a tactical advantage, gaining advantage on its first attack roll against a target.")
	Shimmering_shield = Entry_Text(
		f"Shimmering Shield",
		f"{title} creates a shimmering, magical field around itself or another creature it can see within 60 feet of it. The target gains a +2 bonus to AC until the end of {title}'s next turn.",
		"(Costs 2 Actions)")
	ShimmeringShield =	Shimmering_shield
	BardicInspiration = Entry_Text(
		f"Bardic Inspiration",
		f"{title} inspires an ally within earshot, granting them a bonus to their next ability check, attack roll, or saving throw of 1d{dice_size}.")
	Rage = Entry_Text(
		f"Rage",
		f"{title} enters a state of rage, gaining bonus of {Dice(intensity):+} to melee damage, and gains resistance to bludgeoning, piercing, and slashing damage.")
	FrenziedAttack = Entry_Text(
		f"Frenzied Attack",
		f"{title} makes an attack with advantage against a single target. The next attack against {title} gains advantage.")
	DivineInspiration = Entry_Text(
		f"Divine Inspiration",
		f"{title} calls upon their deity for inspiration, healing an ally {Dice(intensity)}d4.")
	UnexpectedCourage = Entry_Text(
		f"Unexpected Courage",
		f"{title} rallies their inner strength, attacking with extraordinary bravery. It makes a simple attack. The attack is a Critical hit on a 19 or 20 on the atttack roll.",
		"Costs 2 actions")
	DarkRitual = Entry_Text(
		f"Dark Ritual",
		f"{title} quickly mutters a sinister chant, targeting one creature it can see within 30 feet. The target must succeed on a DC {dc} Wisdom saving throw or become cursed. While cursed, the target takes an additional 2 (1d4) necrotic damage whenever it takes damage from any source. The curse lasts for 1 minute or until {title} is incapacitated or dies.",
		"Costs 2 Actions")
	NaturesAid = Entry_Text(
		f"Nature's Aid",
		random.choice([
			f"{title} calls upon nature to assist, by healing an ally {Dice(intensity)}d4.",
			f"{title} calls upon nature to assist, entangling an enemy. On a failed DC{dc} Dexterity saving throw the enemy is restrained."
			]))
	Pathfinder = Entry_Text(
		f"Pathfinder",
		f"{title} can move their full speed without provoking opportunity attacks.")
	ProtectiveStance = Entry_Text(
		f"Protective Stance",
		f"{title} takes a defensive position, granting increased {Dice(intensity):+} AC to themselves and one other creature within 5 feet.")
	SwiftAid = Entry_Text(
		f"Swift Aid",
		f"{title} quickly tends to an ally's wounds, restoring {intensity}d6 hit points.")
	HeroicSacrifice = Entry_Text(
		f"Heroic Sacrifice",
		f"{title} finds the strength to keep fighting, gaining {roll} temporary hit points.",
		"Costs 2 Actions")
	PreciseShot = Entry_Text(
		f"Precise Shot",
		f"{title} makes a special attack.")
	ChivalrousCharge = Entry_Text(
		f"Chivalrous Charge",
		f"{title} charges an enemy, moving half their speed and doing a simple attack.")
	ArcaneBurst= Entry_Text(
		f"Arcane Burst",
		f"{title} releases a burst of magical energy. All creatures within {Dice(3)*Dice(2)*5} feet receive {roll} {attacks.Damage()} damage")
	KiStrike = Entry_Text(
		f"Ki Strike",
		f"{title} channels their ki energy to make rapid strikes, making two simple attacks.")
	CommandingPresence = Entry_Text(
		f"Commanding Presence",
		f"{title} commands an ally, allowing them to move half their speed.")
	Blessing = Entry_Text(
		 f"Blessing",
		 f"{title} blesses an ally, granting them a bonus {roll} to their next attack or saving throw.")
	BoardingAction = Entry_Text(
		f"Boarding Action",
		f"{title} swiftly moves across the battlefield, engaging an enemy in close combat, moving their full speed and doing a simple attack.")
	HuntersMark = Entry_Text(
		f"Hunter's Mark",
		f"{title} marks a target, granting a bonus {roll} to damage on their next attack against that target.")
	CunningAction = Entry_Text(
		f"Cunning Action",
		f"{title} uses their quick wits to gain advantage on their next action.")
	MomentofClarity = Entry_Text(
		f"Moment of Clarity",
		f"{title} provides critical information or advice, granting advantage to an ally's next check.")
	TacticalManeuver = Entry_Text(
		f"Tactical Maneuver",
		f"{title} directs their allies, granting advantage to their next attack.")
	InsightfulDiscovery = Entry_Text(
		f"Insightful Discovery",
		f"{title} uses their knowledge to reveal an immunity, resistance, or vulnerability, or provide crucial information about an enemy's defenses.")
	SpiritCall  = Entry_Text(
		f"Spirit Call",
		random.choice([
			f"{title} calls upon the spirits to aid in battle, healing all allies within {5*Dice(2)*Dice(3)} feet {Dice(intensity)}d4 hit points.",
			f"{title} calls upon the spirits to aid in battle, harming all enemies that start their turn within {5*Dice(2)*Dice(3)} feet {Dice(intensity)}d4 hit points.",
			]))
	CovertOperation = Entry_Text(
		f"Covert Operation",
		f"{title} sabotages an enemy, causing their next attack to be at disadvantage.")
	StreetSmarts = Entry_Text(
		f"Street Smarts",
		f"{title} uses their survival skills to disengage, hide, or dash.")
	BattleFrenzy = Entry_Text(
		f"Battle Frenzy",
		f"{title} enters a state of frenzy, increasing their attack capability for a short time. He makes a simple attack at disadvantage. On a hit, the target recives an extra {roll} damage.")
	Hex = Entry_Text(
		f"Hex",
		f"{title} places a curse on an enemy, causing their saving throws to have disadvantage for 1 minute.")
	HealingTouch = Entry_Text(
		f"Healing Touch",
		f"{title} touches another creature, healing it for {roll} of hit points.")
	BattleCommand = Entry_Text(
		"Battle Command.",
		f"As a bonus action, {title} targets one ally he can see within 30 feet of them. If the target can see or hear {title}, the target can use its reaction to make one melee attack or to take the Dodge or Hide action.")
	PsychicDrain = Entry_Text(
		f"Psychic Drain",
		f"One creature {title} can see takes {int(intensity*3.5)} ({intensity}d6) psychic damage, and {title} regains hit points equal to the damage the creature takes.",
		"(Costs 2 Actions)")
	Teleport = Entry_Text(
		"Teleport",
		f"{title} magically teleports, along with any equipment it is wearing or carrying, up to {Dice(2)*Dice(2)*Dice(3)*10} feet to an unoccupied space it can see."
		"(Costs 2 Actions)")
	CastASpell = Entry_Text(
		"Cast A Spell",
		f"{title} casts a spell from its list of prepared spells, using a spell slot (or a daily use) as normal. "
		)
	ParalyzingTouch = Entry_Text("Paralyzing Touch",
		f"{title} touches one creature within 5 feet of it. The target must succeed on a DC {dc} Constitution saving throw or be paralyzed for 1 minute. The target can repeat the saving throw at the start of each of its turns, ending the effect on itself on a success.",
		"(Costs 2 Actions)")
	PsionicBlast =  Entry_Text("Psionic Blast",
		f"{title} emits a wave of psionic energy. Each creature in a 30-foot cone must succeed on a DC {magic_dc} Intelligence saving throw or take {intensity*4} ({intensity}D8) psychic damage and be stunned for 1 minute. A stunned target can repeat the saving throw at the start of each of its turns, ending the effect on itself on a success.",
		"(Costs 3 Actions)")
	DragonBreath =  Entry_Text("Dragon Breath",
		f"{title} exhales a torrent of destructive energy. Each creature in a 60-foot cone must make a DC {dc} Dexterity saving throw, taking {intensity*4} ({intensity}D8) {attacks.Damage()} damage on a failed save, or half as much damage on a successful one.",
		"(Costs 3 Actions)")

	racial_actions = {
		"Aberration":[  ParalyzingTouch,	PsychicDrain,		Detect,				FrenziedAttack,     CorrosiveTouch,     Engulf,             RendNTear,          TerrifyingRoar,     ScaledDefense,      Disappear,          Stomp,              ProtectiveShift,    VenomousBite,       TerrifyingVisage,  DeadlyGaze,        DeathlyTouch,      WarpReality,       MindWarp,          FrightfulPresence, ],
		"Aven":[        Detect,				HuntersMark,        BoardingAction,     SwiftAid,           Pathfinder,          NaturesAid,         TacticalAmbush,     RendNTear,          SneakyStab,         SmallEscape,        DeceptiveManeuver,  QuickFix,           NimbleDodge,        SneakyStrike,       LuckyBreak,         SwiftMovement,      TacticalManeuver,  BattleCry,         WingAttack,        ],
		"Beast":[       Hex,                SwiftAid,           NaturesAid,         HealingFlux,        EntanglingRoots,    Engulf,             RendNTear,          TerrifyingRoar,     Disappear,          SmallEscape,        NaturesWrath,       BeguilingGaze,      VenomousBite,       NimbleDodge,        SneakyStrike,       SwiftMovement,      SwarmTactics,      InspiringDisplay,  DeathTouch,        DeadlyGaze,        DeathlyTouch,      TailSweep,         HealingTouch,      HealSelf,
						Detect,				RendNTear,      	TerrifyingRoar,     ],
		"Beastfolk":[   BattleFrenzy,       Blessing,           ChivalrousCharge,   HeroicSacrifice,     SwiftAid,           Pathfinder,          NaturesAid,         FrenziedAttack,     Rage,               TacticalAmbush,     BrutalStrike,       WarCry,             RendNTear,          TerrifyingRoar,     Disappear,          SmallEscape,        Stomp,              NaturesWrath,       BeguilingGaze,      QuickFix,           NimbleDodge,        SneakyStrike,       LuckyBreak,
						Detect,				SwiftMovement,  	SwarmTactics,      TacticalManeuver,  TerrifyingVisage,  DeathTouch,        DeadlyGaze,        BattleCry,         FrightfulPresence, TailSweep,         HealingTouch,      CommandAlly,       HealSelf,          RendNTear,          TerrifyingRoar      ],
		"Catfolk":	[	Teleport,			TerrifyingRoar,		CunningAction,		DeceptiveManeuver,	StreetSmarts,		],
		"Celestial":[   MomentofClarity,    Blessing,           CommandingPresence, ChivalrousCharge,   HeroicSacrifice,     SwiftAid,           ProtectiveStance,   DivineInspiration,  ShimmeringShield,  HealingFlux,        BrutalStrike,       WarCry,             TerrifyingRoar,     MinionCommand,      BeguilingGaze,      QuickFix,           TerrifyingVisage,  DeadlyGaze,        BattleCry,         DeathlyTouch,      WarpReality,                           ShimmeringShield,
						Detect,				HealSelf,      		HealSelf,			RadiantBlast,      HealingTouch,      ],
		"Construct":[   ParalyzingTouch,	Detect,				MomentofClarity,    ProtectiveStance,   Pathfinder,          ShimmeringShield,  HealingFlux,        CorrosiveTouch,     QuickTinkerer,      SneakyStab,         SmallEscape,        IngeniousTrap,      Stomp,              MightyThrow,        MinionCommand,      ElementalBlast,     ProtectiveShift,    QuickFix,                               ],
		"Dragon":[      DragonBreath,		VenomousBite,		CommandingPresence, ArcaneBurst,        Engulf,             RendNTear,          TerrifyingRoar,     SwiftReptile,       ScaledDefense,      MinionCommand,      ElementalBlast,     SerpentineGrace,    TerrifyingVisage,  BattleCry,         WingAttack,        TailSweep,         FrightfulPresence, ],
		"Dwarf":[       ChivalrousCharge,   ProtectiveStance,   FrenziedAttack,     BrutalStrike,       WarCry,             TerrifyingRoar,     IngeniousTrap,      Stomp,              MightyThrow,        NimbleDodge,        BattleCry,         FrightfulPresence, ShimmeringShield,  ],
		"Elemental":[   ArcaneBurst,        CorrosiveTouch,     Engulf,             Disappear,          SmallEscape,        MightyThrow,        ElementalBlast,     ProtectiveShift,    ],
		"Elf":[         ParalyzingTouch,	Detect,				InsightfulDiscovery,                    CommandingPresence, PreciseShot,        SwiftAid,           Pathfinder,          NaturesAid,         TacticalAmbush,     EntanglingRoots,    ],
		"Fey":[         ParalyzingTouch,	Teleport,			Detect,				Blessing,           ArcaneBurst,        HeroicSacrifice,     SwiftAid,           NaturesAid,         UnexpectedCourage,  TacticalAmbush,     HealingFlux,        EntanglingRoots,    Disappear,          SneakyStab,         SmallEscape,        BeguilingGaze,      DeceptiveManeuver,  NimbleDodge,        TerrifyingVisage,  BattleCry,         WarpReality,       NaturesWrath            ],
		"Fiend":[       Hex,                CommandingPresence, DarkRitual,         ShimmeringShield,  TacticalAmbush,     BrutalStrike,       WarCry,             CorrosiveTouch,     Engulf,             RendNTear,          TerrifyingRoar,     ScaledDefense,      SmallEscape,        Stomp,              MinionCommand,      HellfireBlast,       DeceptiveManeuver,  VenomousBite,       SerpentineGrace,    SwarmTactics,     TerrifyingVisage,   DeathTouch,       DeadlyGaze,	BattleCry,
						Detect,				WarpReality,		FrightfulPresence, ],
		"Giant":[       CommandingPresence, ChivalrousCharge,   ProtectiveStance,   NaturesAid,         FrenziedAttack,     Rage,               BrutalStrike,       WarCry,             Engulf,             RendNTear,          TerrifyingRoar,     Stomp,              MightyThrow,        ElementalBlast,     BattleCry,                             ],
		"Gnome":[       ParalyzingTouch,	Teleport,			Detect,				ArcaneBurst,        SwiftAid,           Pathfinder,          NaturesAid,         UnexpectedCourage,  TacticalAmbush,     HealingFlux,        EntanglingRoots,    QuickTinkerer,      Disappear,          SneakyStab,         SmallEscape,        IngeniousTrap,      NaturesWrath,       DeceptiveManeuver,  QuickFix,           NimbleDodge,        SwarmTactics,],
		"Goblin":[      ParalyzingTouch,	Detect,				CunningAction,      SwiftAid,           UnexpectedCourage,  FrenziedAttack,     Rage,               TacticalAmbush,     RendNTear,          Disappear,          SneakyStab,         SmallEscape,        IngeniousTrap,      MinionCommand,      NaturesWrath,       DeceptiveManeuver,  QuickFix,           NimbleDodge,        SwarmTactics,      SneakyStrike,       ],
		"Halfling":[    Detect,				ChivalrousCharge,   HeroicSacrifice,    SwiftAid,           Pathfinder,          NaturesAid,         UnexpectedCourage,  TacticalAmbush,     SneakyStab,         DeceptiveManeuver,  NimbleDodge,        LuckyBreak ,],
		"Human":[       Detect,				TacticalManeuver,   ChivalrousCharge,   HeroicSacrifice,     SwiftAid,           ProtectiveStance,   Pathfinder,          UnexpectedCourage,  TacticalAmbush,     IngeniousTrap,      MinionCommand,      QuickFix,           LuckyBreak,         TacticalManeuver,  BattleCry,         DeathlyTouch,      HealingTouch,      CommandAlly,       HealSelf,          ],
		"Kobold":[      DragonBreath,		Detect,				UnexpectedCourage,  FrenziedAttack,     TacticalAmbush,     WarCry,             RendNTear,          SwiftReptile,       ScaledDefense,      QuickTinkerer,      Disappear,          SneakyStab,         SmallEscape,        IngeniousTrap,      ElementalBlast,     QuickFix,           SerpentineGrace,    NimbleDodge,        SwarmTactics,   ],
		"Lizardfolk":[  DragonBreath,		ParalyzingTouch,	Detect,				ProtectiveStance,   Pathfinder,         NaturesAid,         FrenziedAttack,     Rage,               BrutalStrike,       WarCry,             RendNTear,          TerrifyingRoar,     SwiftReptile,       ScaledDefense,      Disappear,          SneakyStab,         Stomp,              MightyThrow,        NaturesWrath,       DeceptiveManeuver,                      VenomousBite,       SerpentineGrace,             ],
		"Monstrosity":[ Detect,				FrenziedAttack,     BrutalStrike,       CorrosiveTouch,     Engulf,             RendNTear,          TerrifyingRoar,     SwiftReptile,       ScaledDefense,      Stomp,              ProtectiveShift,    VenomousBite,       SerpentineGrace,                ],
		"Ooze": [       ArcaneBurst,        SwiftAid,           CorrosiveTouch,     Engulf,             Disappear,          SmallEscape,        ElementalBlast,     ProtectiveShift,   SerpentineGrace,     DeathlyTouch,            ],
		"Orc": [        Detect,				BattleFrenzy,       CommandingPresence, HeroicSacrifice,     ProtectiveStance,   Rage,               FrenziedAttack,     BrutalStrike,       WarCry,             RendNTear,          TerrifyingRoar,     Stomp,              MightyThrow,        BattleCry,            ],
		"Plant": [      ParalyzingTouch,	ArcaneBurst,        SwiftAid,           Pathfinder,          NaturesAid,         HealingFlux,        EntanglingRoots,    CorrosiveTouch,     Engulf,             Disappear,          SmallEscape,        NaturesWrath,             ],
		"Snakefolk": [  DragonBreath,		ParalyzingTouch,	Detect,				Hex,                CunningAction,      BoardingAction,     Pathfinder,          NaturesAid,         Engulf,             RendNTear,          TerrifyingRoar,     SwiftReptile,       ScaledDefense,      Disappear,          SneakyStab,         HellfireBlast,     BeguilingGaze,    DeceptiveManeuver,    VenomousBite, SerpentineGrace,            ],
		"Undead":[      CunningAction,      ProtectiveStance,   DarkRitual,         Rage,               WarCry,             CorrosiveTouch,     RendNTear,          SneakyStab,         MinionCommand,      HellfireBlast,       VenomousBite,       SwarmTactics,      TerrifyingVisage,  DeathTouch,    DeadlyGaze,    DeathlyTouch,  FrightfulPresence, ],

		# Subraces
		"Sphynx": [		DragonBreath,		CastASpell,			Teleport,	],
		}

	background_actions = {
		"Artist": [     Detect,				MomentofClarity,    ArcaneBurst,        SwiftAid,           UnexpectedCourage,  BardicInspiration,  QuickTinkerer,      Disappear,          SneakyStab,         SmallEscape,        IngeniousTrap,      BeguilingGaze,      ElementalBlast,     QuickFix,           InspiringDisplay,  ],
		"Bandit": [     CovertOperation,    CunningAction,      TacticalAmbush,     RendNTear,          Disappear,          SneakyStab,         SmallEscape,        MightyThrow,        MinionCommand,      DeceptiveManeuver,  SwarmTactics,      TacticalManeuver,  BattleCry,         ],
		"Bard": [       CastASpell,			StreetSmarts,       ArcaneBurst,        SwiftAid,           DarkRitual,         UnexpectedCourage,  BardicInspiration,  ShimmeringShield,  HealingFlux,        Disappear,          SneakyStab,         SmallEscape,        BeguilingGaze,      DeceptiveManeuver,  QuickFix,           BattleCry,         ],
		"Barbarian": [  Detect,				BoardingAction,     ProtectiveStance,   FrenziedAttack,     Rage,               EntanglingRoots,    BrutalStrike,       WarCry,             RendNTear,          TerrifyingRoar,     Stomp,              MightyThrow,        BattleCry,         ],
		"Berserker": [  BattleFrenzy,       BoardingAction,     SwiftAid,           NaturesAid,         FrenziedAttack,     BrutalStrike,       WarCry,             RendNTear,          TerrifyingRoar,     MightyThrow,        NaturesWrath,       ElementalBlast,     DeadlyGaze,        BattleCry,         ],
		"Charlatan": [  PsychicDrain,		Detect,				BattleCommand,		Hex,                StreetSmarts,       TacticalManeuver,   CommandingPresence, HeroicSacrifice,     SwiftAid,           DarkRitual,         UnexpectedCourage,  ShimmeringShield,  TacticalAmbush,     WarCry,             QuickTinkerer,      Disappear,          SneakyStab,         SmallEscape,        IngeniousTrap,      MinionCommand,      BeguilingGaze,      QuickFix, NimbleDodge,
						TacticalManeuver,	DeceptiveManeuver            ],
		"Cleric": [     Blessing,           SwiftAid,           DarkRitual,         DivineInspiration,  ShimmeringShield,  HealingFlux,        HellfireBlast,       DeathlyTouch,      ],
		"Crafter":  [   Detect,				InsightfulDiscovery,                    SwiftAid,           ShimmeringShield,  HealingFlux,        CorrosiveTouch,     QuickTinkerer,      Disappear,          SneakyStab,         SmallEscape,        IngeniousTrap,      ElementalBlast,     QuickFix,           ],
		"Criminal": [   Detect,				StreetSmarts,       CovertOperation,    TacticalManeuver,   CunningAction,      BoardingAction,     Pathfinder,          TacticalAmbush,     Disappear,          SneakyStab,         SmallEscape,        DeceptiveManeuver,  NimbleDodge,        SwarmTactics,      TacticalManeuver,  LuckyBreak,         SneakyStrike        ],
		"Commoner": [   BoardingAction,     PreciseShot,        HeroicSacrifice,     SwiftAid,           ProtectiveStance,   Pathfinder,          BrutalStrike,       QuickTinkerer,      Disappear,          SmallEscape,        IngeniousTrap,      Stomp,              MightyThrow,        QuickFix,           NimbleDodge,        ],
		"Cultist":  [   DragonBreath,		CastASpell,			PsychicDrain,		Hex,                Blessing,           SwiftAid,           DarkRitual,         DivineInspiration,  FrenziedAttack,     ShimmeringShield,  WarCry,             CorrosiveTouch,     Disappear,          SneakyStab,         MinionCommand,      HellfireBlast,       NaturesWrath,       BeguilingGaze,      ElementalBlast, DeathTouch,WarpReality,DeathlyTouch,    ],
		"Druid":    [   CastASpell,			Detect,				SwiftAid,           NaturesAid,         HealingFlux,        EntanglingRoots,    Disappear,          NaturesWrath,       ElementalBlast,     ProtectiveShift,    DeathlyTouch,      ],
		"Expert": [     Detect,				BattleCommand,		TacticalManeuver,   MomentofClarity,    CunningAction,      Pathfinder,          ShimmeringShield,  TacticalAmbush,     QuickTinkerer,      Disappear,          SneakyStab,         MinionCommand,      QuickFix,           ],
		"Explorer": [   Detect,				InsightfulDiscovery,                    HuntersMark,        BoardingAction,     PreciseShot,        HeroicSacrifice,     Pathfinder,          UnexpectedCourage,  TacticalAmbush,     EntanglingRoots,    Disappear,          SneakyStab,         SmallEscape,        IngeniousTrap,      NaturesWrath,       NimbleDodge,        SerpentineGrace,    ],
		"Fighter": [	TacticalManeuver,   CommandingPresence,	BattleCommand,		],
		"Guard": [      Detect,				BattleCommand,		TacticalManeuver,   CommandingPresence, PreciseShot,        ProtectiveStance,   UnexpectedCourage,  ShimmeringShield,  BrutalStrike,       WarCry,             RendNTear,          SwarmTactics,      TacticalManeuver,  BattleCry,         ],
		"Healer": [     Blessing,           SwiftAid,           NaturesAid,         DivineInspiration,  ShimmeringShield,  HealingFlux,        HealSelf,          ],
		"Hero":   [     BattleCommand,		HeroicSacrifice,     SwiftAid,           ProtectiveStance,   Pathfinder,          UnexpectedCourage,  DivineInspiration,  FrenziedAttack,     ShimmeringShield,  HealSelf,          BrutalStrike,       WarCry,     RendNTear,  Stomp, MightyThrow,   MinionCommand, BattleCry,            ],
		"Hunter": [     Detect,				HuntersMark,        PreciseShot,        Pathfinder,          NaturesAid,         TacticalAmbush,     EntanglingRoots,    Disappear,          SneakyStab,         IngeniousTrap,      NaturesWrath,       NimbleDodge, SerpentineGrace,    ],
		"Knight": [     BattleCommand,		BattleFrenzy,       CommandingPresence, ChivalrousCharge,   HeroicSacrifice,     ProtectiveStance,   UnexpectedCourage,  FrenziedAttack,     ShimmeringShield,  HealingFlux,        HealSelf,          BrutalStrike,   WarCry,     RendNTear,  MinionCommand,   TacticalManeuver,BattleCry,            ],
		"Mage": [       CastASpell,			ArcaneBurst,        Disappear,          ElementalBlast,     ProtectiveShift,            ],
		"Merchant":[    StreetSmarts,       BoardingAction,     Pathfinder,          UnexpectedCourage,  QuickTinkerer,      Disappear,          SmallEscape,        MinionCommand,      DeceptiveManeuver,   ],
		"Monk": [       DragonBreath,		ParalyzingTouch,	Detect,				MomentofClarity,    KiStrike,           SwiftAid,           ProtectiveStance,   ShimmeringShield,  HealSelf,          BrutalStrike,       Disappear,          SneakyStab,          NimbleDodge,               ],
		"Ninja":[       ParalyzingTouch,	Detect,				CovertOperation,    CunningAction,      KiStrike,           PreciseShot,        ProtectiveStance,   Pathfinder,          TacticalAmbush,     RendNTear,          Disappear,             SneakyStab,          SmallEscape,  DeceptiveManeuver,    NimbleDodge, SerpentineGrace],
		"Noble":[       CommandingPresence, ChivalrousCharge,   ProtectiveStance,   UnexpectedCourage,  WarCry,             TacticalManeuver,  CommandAlly,       BattleCry,                        ],
		"Priest": [     HealingTouch,      	ShimmeringShield,  	HealingFlux,        HealSelf,          MinionCommand,      ],
		"Pirate":[      BattleCommand,		CunningAction,      BoardingAction,     Blessing,           ChivalrousCharge,   PreciseShot,        UnexpectedCourage,  FrenziedAttack,     TacticalAmbush,     RendNTear,           Disappear,             SneakyStab,  SmallEscape, DeceptiveManeuver,   QuickFix,    SerpentineGrace, NimbleDodge, SneakyStrike,    SwarmTactics,   DeadlyGaze,            ],
		"Paladin":	[	BattleCommand,		],
		"Ranger":[      Detect,				HuntersMark,        PreciseShot,        Pathfinder,          NaturesAid,         TacticalAmbush,     EntanglingRoots,    RendNTear,          Disappear,          SneakyStab,          SmallEscape,          NaturesWrath,                ],
		"Rogue":[       ParalyzingTouch,	Detect,				CunningAction,      PreciseShot,        Pathfinder,          UnexpectedCourage,  TacticalAmbush,     RendNTear,          QuickTinkerer,      Disappear,          SneakyStab,    DeceptiveManeuver,           SerpentineGrace,    NimbleDodge,  SneakyStrike, DeathTouch,            ],
		"Scholar": [    CastASpell,			PsychicDrain,		Detect,				InsightfulDiscovery,                    MomentofClarity,    ArcaneBurst,        UnexpectedCourage,  QuickTinkerer,      Disappear,          SmallEscape,        MinionCommand,  QuickFix,        TacticalManeuver,            ],
		"Soldier": [    BattleCommand,		TacticalManeuver,   ChivalrousCharge,   ProtectiveStance,   UnexpectedCourage,  TacticalAmbush,     HealSelf,          BrutalStrike,       WarCry, RendNTear,  MinionCommand,  SwarmTactics,   TacticalManeuver,      BattleCry,            ],
		"Sorcerer": [   QuickFix,           WarpReality,       	ArcaneBurst,        ],
		"Shaman": [     DragonBreath,		CastASpell,			Hex,                SwiftAid,           NaturesAid,         DivineInspiration,  HealingFlux,        HealSelf,          EntanglingRoots,    MinionCommand,      NaturesWrath,    BeguilingGaze,   ProtectiveShift, WarpReality,       DeathlyTouch,            ],
		"Spy":[         ParalyzingTouch,	Detect,				CovertOperation,    MomentofClarity,    CunningAction,      HuntersMark,        BoardingAction,     PreciseShot,        HeroicSacrifice,     Pathfinder,          UnexpectedCourage,  TacticalAmbush,     QuickTinkerer,  Disappear,  SneakyStab, SmallEscape,    IngeniousTrap,  DeceptiveManeuver,  SerpentineGrace,    SneakyStrike,   DeathlyTouch,            ],
		"Traveler":[    Detect,				HuntersMark,        BoardingAction,     PreciseShot,        Pathfinder,          NaturesAid,         UnexpectedCourage,  HealSelf,          QuickTinkerer,      Disappear,     SmallEscape,                 NaturesWrath,  SwiftMovement,],
		"Prankster":[   Detect,				StreetSmarts,       CovertOperation,    CunningAction,      BoardingAction,     PreciseShot,        HeroicSacrifice,     SwiftAid,           Pathfinder,          UnexpectedCourage,  TacticalAmbush,     BrutalStrike,   RendNTear,      QuickTinkerer, Disappear,     SneakyStab,    SmallEscape,   IngeniousTrap, MightyThrow,   QuickFix,    SneakyStrike,    SwarmTactics,               ],
		"Warrior": [    BattleCommand,		BattleFrenzy,       HeroicSacrifice,  	ProtectiveStance,   BrutalStrike,       WarCry, RendNTear,                      TacticalManeuver,  BattleCry          ],
		"Warlock": [    ParalyzingTouch,	CastASpell,			PsychicDrain,		Hex,                ArcaneBurst,        DarkRitual,         DivineInspiration,  HealingFlux,        CorrosiveTouch,     ScaledDefense,      MinionCommand,      HellfireBlast,  BeguilingGaze,  ProtectiveShift,     QuickFix,           WarpReality,DeathlyTouch,            ],
		"Witch": [      ParalyzingTouch,	CastASpell,			PsychicDrain,		Hex,                ArcaneBurst,        SwiftAid,           NaturesAid,         DarkRitual,         HealingFlux,        HealSelf,          EntanglingRoots,    CorrosiveTouch,   Disappear,    NaturesWrath,   BeguilingGaze,      ProtectiveShift,  TerrifyingVisage,DeadlyGaze,WarpReality,DeathlyTouch,            ],
		"Wizard": [     CastASpell,			ArcaneBurst,        DarkRitual,         CorrosiveTouch,     QuickTinkerer,   SmallEscape, ElementalBlast,               ProtectiveShift,    QuickFix,           ],
		}


	# Adding race-specific actions
	if  race    	in racial_actions:
		actions += racial_actions[race]
	if  subrace    	in racial_actions:
		actions += racial_actions[subrace]
	if  background  in background_actions:
		actions     += background_actions[background]

	# Add general actions
	if not actions:
		actions += [Attack, Move]

	actions = list(set(actions))

	action = f"\n{random.choice(actions)}"
	#print(action)
	return  action

def Lair(npc):

	race = npc.race if npc else Race()
	background = npc.archetype if npc else Background()
	title = npc.title  if npc else "The character"
	name = title
	lvl = npc.level if npc else Dice(20)

	pb = PB(lvl)

	power_dc = 8+pb
	magic_dc = npc.spell_save_dc if npc else 10
	dc = max(power_dc,magic_dc)

	STR = npc.AS.str_mod if npc else 0
	DEX = npc.AS.dex_mod if npc else 0
	CON = npc.AS.con_mod if npc else 0
	CHA = npc.AS.cha_mod if npc else 0
	WIS = npc.AS.wis_mod if npc else 0

	intensity = Dice(PB(pb-1))
	dice_size = 2*(1+Dice(5))
	roll = f"{intensity}D{dice_size}"

	actions =[]

	result = ""
	result += f"Unless otherwise noted, any lair action that demands a saving throw uses the spellsave DC {dc}."
	result += "\n On initiative count 20 (losing initiative ties), the creature can take a lair action to cause one of the following effects, but can't use the same effect two rounds in a row:\n"

	ElementalShift = Entry_Text(
		"Elemental Shift",
		f"{title} can choose a section up to 20x20 feet or less of a wall within its lair to become ethereal for one round. Other creatures passing through the affected area must succeed on a Dexterity saving throw or become restrained until the end of their next turn as they struggle against the elements.")
	GraspingPlants = Entry_Text(
		"Grasping Plants",
		f"The lair causes roots and vines to temporarily grow. until initiative count 20 on the next round, the ground within 20 feet of {title} is difficult terrain. {title} is immune to this effect.")
	InkSplash = Entry_Text("Ink Splash",
		f"{title} splashes magical ink that spreads across the floor in a 20-foot radius centered on a point within the lair. The area becomes difficult terrain, and any creature that starts its turn in the area or enters it for the first time on a turn must succeed on a DC{dc} Dexterity saving throw or be restrained by the sticky ink until the end of its next turn. ")
	AnimatingArt = Entry_Text("Animating Art",
		f"{title} can animate one of its artworks as an action, bringing to life a shadowy creature (use the stats for a shadow or another appropriate creature, but with an artistic flair in its appearance). This creature acts on its own initiative and follows the commands of {title}. Only one animated artwork can be active at a time.")
	ChaoticAura = Entry_Text("Chaotic Aura",
		f"{title} creates misdirecting currents of air and magic around itself. Until initiative count 20 on the next round, whenever a ranged attack roll misses {title}, reroll the attack against a random creature within 30 feet of {title} that doesn't have total cover against the attack.")
	Earthquake = Entry_Text("Earthquake",
		f"{title} causes an earthquake in its lair. All other creature on the ground must succeed on a DC {dc} Dexterity saving throw or be knocked prone.")

	VolcanicEruption = Entry_Text("Volcanic Eruption",
		f"{title} causes magma to burst from the ground at three different points it can see within the lair. Each creature in a 10-foot radius must succeed on a DC {npc.spell_save_dc} Dexterity saving throw or take {3*pb} ({pb}D6) fire damage.")

	PsionicPulse = Entry_Text(
		"Psionic Pulse",
		f"{title} emits a pulse of psychic energy. Each creature of its choice within 120 feet must succeed on a DC {npc.spell_save_dc} Intelligence saving throw or take {pb*3} ({pb}D6) psychic damage and have disadvantage on attack rolls until the end of their next turn.")

	MentalManipulation= Entry_Text("Mental Manipulation",
	 f"{title} attempts to dominate one creature it can see within its lair. The target must succeed on a DC {npc.spell_save_dc - 2} Wisdom saving throw or be charmed by the {npc.title} until initiative count 20 on the next round.")

	NecroticFog = Entry_Text("Necrotic Fog",
	  f"{title} creates a cloud of necrotic fog in a 20-foot radius. Each creature in the area must succeed on a DC {npc.spell_save_dc} Constitution saving throw or take {pb*3} ({pb}D6) necrotic damage and be blinded until the end of its next turn.")

	GhostlyApparitions = Entry_Text("Ghostly Apparitions",
	f"{title} summons ghostly apparitions that attack creatures in the lair. Each creature must succeed on a DC {npc.spell_save_dc} Wisdom saving throw or be frightened until the end of its next turn.")

	EntanglingVines = Entry_Text("Entangling Vines",
	 f"{title} causes vines to sprout from the ground and entangle creatures in the area. Each creature must succeed on a DC {npc.spell_save_dc} Strength saving throw or be restrained until the end of its next turn.")

	CallLightning = Entry_Text("Call Lightning",
	 f"{title} calls down a bolt of lightning at a point it can see within 60 feet. Each creature within 5 feet must succeed on a DC {npc.spell_save_dc} Dexterity saving throw or take {4*pb} ({pb}D8) lightning damage.")

	SummonBats = Entry_Text("Summon Bats",
	f"{title} summons a swarm of bats to harass enemies. Each creature within 30 feet must succeed on a DC {npc.spell_save_dc} Dexterity saving throw or take {pb*3}({pb}D6) piercing damage and have disadvantage on attack rolls until the end of its next turn.")

	BloodMist = Entry_Text("Blood Mist",
	 f"{title} creates a mist of blood that obscures vision in a 20-foot radius. Creatures in the area are blinded until the end of their next turn.")
	DarknessSurge = Entry_Text("Darkness Surge",
		f"{title} can cause a surge of shadowy energy to fill the lair, dimming light sources. For one round, areas of bright light become dim, and areas of dim light become darkness.")



	extra_actions_background = {
		"Artist": [		DarknessSurge,		AnimatingArt,		MentalManipulation,	PsionicPulse,		AnimatingArt,   	InkSplash,],
		"Bandit": [		EntanglingVines,	NecroticFog,		InkSplash,			],
		"Bard": [		AnimatingArt,		InkSplash,			MentalManipulation,	InkSplash,			],
		"Berserker": [	GhostlyApparitions,	Earthquake,			GraspingPlants,	],
		"Barbarian": [	Earthquake,			CallLightning,		EntanglingVines,	Earthquake,			],
		"Cleric": [		DarknessSurge,		CallLightning,		GhostlyApparitions,	],
		"Commoner": [	EntanglingVines,	],
		"Charlatan": [	NecroticFog,		MentalManipulation,	PsionicPulse,		InkSplash,			],
		"Crafter": [	AnimatingArt,		CallLightning,		NecroticFog,		AnimatingArt,  	InkSplash,			],
		"Cultist": [	Earthquake,			DarknessSurge,		GhostlyApparitions,	NecroticFog,		MentalManipulation,	PsionicPulse,		VolcanicEruption,	],
		"Druid": [		Earthquake,			CallLightning,		EntanglingVines,	GhostlyApparitions,	VolcanicEruption,	Earthquake,			ChaoticAura,	GraspingPlants,],
		"Expert": [		AnimatingArt,		CallLightning,		NecroticFog,		InkSplash,			],
		"Explorer": [	EntanglingVines,	VolcanicEruption,	InkSplash,			],
		"Guard": [		CallLightning,		],
		"Hero":	[		CallLightning,		GhostlyApparitions,	],
		"Hunter": [		EntanglingVines,	GraspingPlants,	],
		"Knight": [		CallLightning,		],
		"Mage": [   	DarknessSurge,		AnimatingArt,		CallLightning,		MentalManipulation,	ChaoticAura,		ElementalShift,    InkSplash,],
		"Merchant": [	AnimatingArt,		InkSplash,			],
		"Monk": [		EntanglingVines,	GhostlyApparitions,	MentalManipulation,	],
		"Ninja": [		DarknessSurge,		InkSplash,			GhostlyApparitions,	NecroticFog,		MentalManipulation,	],
		"Paladin": [	CallLightning,		GhostlyApparitions,	],
		"Prankster": [	InkSplash,			PsionicPulse,		],
		"Priest": [		CallLightning,		GhostlyApparitions,	MentalManipulation,	],
		"Pirate": [		NecroticFog,		],
		"Ranger": [		EntanglingVines,	GraspingPlants,	],
		"Rogue": [		DarknessSurge,		NecroticFog,		],
		"Scholar": [	CallLightning,		PsionicPulse,		InkSplash,			],
		"Shaman": [ 	Earthquake,			DarknessSurge,		CallLightning,		EntanglingVines,	GhostlyApparitions,	VolcanicEruption,	Earthquake,			ChaoticAura,	ElementalShift,  GraspingPlants,],
		"Spy": [		DarknessSurge,		NecroticFog,		MentalManipulation,	PsionicPulse,		DarknessSurge, 	InkSplash,],
		"Sorcerer":[	Earthquake,			CallLightning,		PsionicPulse,		Earthquake,			ChaoticAura,],
		"Traveler": [	InkSplash,			CallLightning,		],
		"Warlock":[		Earthquake,			DarknessSurge,		AnimatingArt,		CallLightning,		GhostlyApparitions,	NecroticFog,		MentalManipulation,	PsionicPulse,		VolcanicEruption,	Earthquake,			ChaoticAura,	],
		"Witch": [		DarknessSurge,		CallLightning,		EntanglingVines,	GhostlyApparitions,	MentalManipulation,	ChaoticAura,		GraspingPlants,],
		"Wizard":[  	Earthquake,			InkSplash,			CallLightning,		ChaoticAura,		ElementalShift, ],

		}

	extra_actions_race = {
		"Aberration":[		Earthquake,			MentalManipulation,	PsionicPulse,		ChaoticAura,		],
		"Aven":[    		CallLightning,		GhostlyApparitions,	MentalManipulation,	ChaoticAura,		ElementalShift, ],
		"Beast": [			Earthquake,			CallLightning,		EntanglingVines,	GhostlyApparitions,	MentalManipulation,	Earthquake,			GraspingPlants,],
		"Beastfolk": [		Earthquake,			CallLightning,		EntanglingVines,	GhostlyApparitions,	MentalManipulation,	Earthquake,			GraspingPlants,],
		"Catfolk": [		CallLightning,		GhostlyApparitions,	MentalManipulation,	],
		"Celestial":[   	CallLightning,		GhostlyApparitions,	MentalManipulation,	Earthquake,			ChaoticAura,	ElementalShift, ],
		"Construct": [ 		CallLightning,		Earthquake,			],
		"Dragon": [			VolcanicEruption,	Earthquake,			GraspingPlants,],
		"Dwarf": [			Earthquake,			CallLightning,		],
		"Elemental":[   	CallLightning,		VolcanicEruption,	ChaoticAura,		ElementalShift, ],
		"Elf": [			EntanglingVines,	MentalManipulation,	GraspingPlants,	],
		"Fey": [			EntanglingVines,	MentalManipulation,	PsionicPulse,		ChaoticAura,		GraspingPlants,],
		"Fiend": [			Earthquake,			DarknessSurge,		GhostlyApparitions,	NecroticFog,		MentalManipulation,	VolcanicEruption,	Earthquake,		],
		"Giant": [			Earthquake,			CallLightning,		VolcanicEruption,	Earthquake,			],
		"Gnome": [			InkSplash,			EntanglingVines,	MentalManipulation,	GraspingPlants,	],
		"Goblin": [			GhostlyApparitions,	MentalManipulation,	PsionicPulse,		GraspingPlants,	],
		"Halfling": [		GhostlyApparitions,	GraspingPlants,	],
		"Human": [			CallLightning,		],
		"Kobold": [			DarknessSurge,		],
		"Lizardfolk": [		EntanglingVines,	GraspingPlants,	],
		"Monstrosity": [	Earthquake,			EntanglingVines,	VolcanicEruption,	Earthquake,	ChaoticAura,	],
		"Ooze":	[			InkSplash,			CallLightning,		NecroticFog,		VolcanicEruption,	],
		"Orc": [			GhostlyApparitions,	Earthquake,			GraspingPlants,],
		"Plant": [			Earthquake,			EntanglingVines,	EntanglingVines,	NecroticFog,		MentalManipulation,	Earthquake,			GraspingPlants,],
		"Snakefolk": [		EntanglingVines,	GhostlyApparitions,	NecroticFog,		MentalManipulation,	PsionicPulse,		VolcanicEruption,	GraspingPlants,	],
		"Undead":	[		DarknessSurge,		GhostlyApparitions,	GhostlyApparitions,	NecroticFog,		NecroticFog,		MentalManipulation,	Earthquake,			],
		}

	extra_actions_subrace = {
		"Old One": [GraspingPlants,],
		"Chaos Warper": [GraspingPlants,],
		"Lesser God": [GraspingPlants,],
		"Tutelar God": [GraspingPlants,],
		"Unicorn": [GraspingPlants,],
		"Sphynx": [	CallLightning,		],
		# Celestials
		"Planetar": [	Earthquake,			],
		"Archangel": [	Earthquake,			],
		# Constructs
		"Golem":	[	Earthquake,			],
		# Elementals
		"Gaian":	[Earthquake,			],

		}

	# Fetch the extra skills for the selected race and background
	extra_actions = list(set(extra_actions_race.get(npc.race, []) +
							extra_actions_subrace.get(npc.subrace, []) +
							extra_actions_background.get(npc.archetype, [])))

	# Eliminate redundancies
	number_of_actions = min(len(extra_actions),
						   Dice(npc.proficiency_bonus), 4)


	# Select and format skills
	actions = random.sample(extra_actions, number_of_actions)

	return result + '\n'.join(actions) if actions else "<u>None</u>"



	if Type == "Fey" and Dice() == 1:        r += "\n- Grasping Plants \n\t The fey causes roots and vines to temporarily grow around it; until initiative count 20 on the next round, the ground within 20 feet of the fey is difficult terrain."
	if Type == "Fey" and Dice() == 1:        r += "\n- Fey Walk \n\t Until initiative count 20 on the next round, the fey can pass through solid walls, doors, ceilings, and floors as if the surfaces weren't there."
	if Type == "Fey" and Dice() == 1:        r += "\n- The fey targets any number of doors and windows that they can see, causing each one to either open or close as they wish. Closed doors can be magically locked (requiring a successful DC 20 Strength check to force open) until they choose to make them unlocked, or until they use this lair action again to open them."
	if Type == "Fey" and Dice() == 1:        r += "\n- The fey fills up to four 10-foot cubes of water with ink. The inky areas are heavily obscured for 1 minute, although a steady, strong underwater current disperses the ink on initiative count 10. The fey ignores the obscuring effect of the ink."
	if Type == "Fey" and Dice() == 1:        r += "\n- The fey chooses one humanoid within the lair and instantly creates a simulacrum of that creature (as if created with the simulacrum spell). This hideous simulacrum is formed out of seaweed, slime, half-eaten fish, and other garbage, but still generally resembles the creature it is imitating. This simulacrum obeys the fey's commands and is destroyed on initiative count 20 on the next round."
	if Type == "Fey" and Dice() == 1:        r += "\n- The fey creates an illusory duplicate of themselves, which appears in its own space. As long as they can see their duplicate, the fey can move it a distance equal to their walking speed as well as make the illusion speak on their turn (no action required). The illusion has the same statistics as the fey but can't take actions or reactions. It can interact with its environment and even pick up and hold real objects. The illusion seems real in every way but disappears if it takes any amount of damage. Otherwise, it lasts until the fey dismisses it (no action required) or can no longer see it. If the fey uses this lair action to create a new duplicate, the previous one vanishes, dropping any real objects in its possession."

	if Type == "Fiend" and Dice() == 1:     r += "\n- One creature the fiend can see within 120 feet of them must succeed on a Charisma saving throw or be banished to a prison demiplane. To escape, the creature must use its action to make a Charisma check contested by the fiend's. If the creature wins, it escapes the demiplane. Otherwise, the effect ends on initiative count 20 on the next round. When the effect ends, the creature reappears in the space it left or in the nearest unoccupied space if that one is occupied."
	if Type == "Fiend" and Dice() == 1:     r += "\n- The fiend targets up to three creatures that they can see within 60 feet of them. Each target must succeed on a Constitution saving throw or be flung up to 30 feet through the air. A creature that strikes a solid object or is released in midair takes 1d6 bludgeoning damage for every 10 feet moved or fallen."


	return r

def Region(npc):

	title = getattr(npc, "title", "Unknown Entity")
	race = getattr(npc, "race", "Unknown Race")
	archetype = getattr(npc, "archetype", "Unknown Archetype")
	dc = getattr(npc, "spell_save_dc", 10)
	subrace = getattr(npc, "subrace", "Unknown")
	actions = []
	creature_type = race + ' ' + subrace + ' ' + archetype

	pre = ""
	pre += f"{npc.title} has an effect on its domains that may include any of the following magical effects:\n"
	dissipation_note = f"\nIf {npc.title} dies, these effects dissipate during the next {Dice(6,2)} days."

	wildlife = Entry_Text(
		"Wildlife Frenzy",
		"The wildlife in the area displays unnatural aggression and grotesque mutations, their behavior becoming erratic and dangerous to travelers."
		)
	volcan = Entry_Text(
		"Volcanic Unrest"
		f"The ground trembles as volcanic activity intensifies within a mile of the lair, spewing ash, heat, and occasional jets of molten rock."
		)
	risen_dead = Entry_Text(
		"Risen Dead",
		f"{npc.title}'s domain stir with unholy energy, waking the dead. The dead rise in nearby graveyards"
		)
	moving_shadows = Entry_Text(
		"Restless Shadows",
		f"Shadows twist and glide unnaturally, as if animated by an unseen will, stalking the edges of perception."
		)
	wither = Entry_Text(
		"Blight",
		f"Local plants wither and die, as if drained of life."
		)
	beast_guardians = Entry_Text(
		"Beast Guardians",
		f"The beasts of {npc.title}'s domain instinctively rally to its defense, drawn by an unshakable nexus with the {npc.race}. Beasts (appropiate to {title}) with an Intelligence score of 2 or lower will aggressively defend the territory from intruders, acting as loyal protectors."
		)
	no_flames = Entry_Text(
		"Extinguished flames",
		f"Open flames of a non magical nature are extinguished within {npc.title}'s domain. Torches and campfires refuse to burn. Enclosed lanterns remain eerily unaffected."
		)
	hider = Entry_Text("Hidding in the Shadows",	f"The natural environment of the {npc.race}'s domain seems to conspire with its inhabitants, offering abundant cover and shadows. Creatures native to this area instinctively blend into their surroundings, making it almost impossible to spot them without careful scrutiny. All such creatures have advantage on Dexterity (Stealth) checks while within the domain.")
	healing_aura = Entry_Text(
		"Aura of Vitality",
		f"Within {npc.title}'s domain, healing magic surges. When a creature casts a spell or uses a magical effect that causes another creature to regain hit points, the target regains the maximum number of hit points possible for the spell or effect."
		)
	anticursed = Entry_Text(
		"Sanctuary",
		f"A tranquil aura pervades {npc.title}'s domain, dispelling all lingering malice. All curses affecting good-aligned creatures are suppressed while within this domain."
		)
	compulsory_offering = Entry_Text(
		f"Compulsory Offering",
		(	"An intangible presence weighs on the heart, compelling travelers to leave tribute for unseen forces."
			f"The first time a creature enters the lair's domain (1 mile radius), it must succeed on a DC {dc} Wisdom saving throw or feel a strong compulsion to leave an offering worth at least 5 gp in a hidden location. The {npc.race} instantly senses the offering's position. Each creature can be affected by this compulsion only once."
		))
	malleable_time = Entry_Text(
		"Malleable Time",
		f"Time is fluid within 1 mile of {npc.title}'s lair, flowing somewhere between half and twice its normal speed.")
	pests = Entry_Text("Pests",
		f"Birds, rodents, snakes, spiders, or toads (or some other creatures appropriate to the {npc.race}) are found in great profusion.")
	eternal_twilight = Entry_Text("Eternal Twilight",
		f"The sun seems to struggle in this region, never fully rising nor setting, casting an eternal twilight that blankets the area. Shadows cast within this zone are deeper and more pronounced, and natural light sources appear dimmer than usual. This effect unsettles locals and affects the behavior of wildlife, making nocturnal creatures more active during what should be daylight hours.")
	shadow_whispers = Entry_Text("Shadow Whispers",
		f"Shadows within a few miles of the lair seem to whisper when no one is looking directly at them. These whispers are unintelligible but carry with them a sense of foreboding and unease. This can unsettle travelers and make locals superstitious about venturing out without light, even during the day.")
	artistic_hallucination = Entry_Text("Artistic Hallucinations",
		f"Individuals who spend more than a few hours in the region may start to see vivid, albeit brief, hallucinations. These visions are often artistic in nature, such as paintings coming to life or sculptures moving in the corner of one's eye.")
	drained_creativity = Entry_Text("Drained Creativity",
		f"Artists, crafters, and anyone trying to create within the region find their work frustratingly difficult. Colors seem less vibrant, inspiration harder to come by, and finished works often seem lacking, as {title} is siphoning creativity for itself. This effect could lead to tales of a curse that plagues artists, driving them either away from the region or mad with the inability to fulfill their creative desires.")
	EternalBreeze = Entry_Text(
		"Eternal Breeze",
		f"A constant, unnaturally strong wind blows across the region. Creatures can't fly, and fire, fog, smoke, and similar effects are extinguished at the end of any creature's turn. The Eternal Breeze doesn't affect {npc.title}")
	inhospitable = Entry_Text(
		"Inhospitable",
		f"The nearby land becomes scorched and inhospitable.")
	BeastCharm = Entry_Text(
		"Bestiality",
		f"Beasts that have an Intelligence score of 2 or lower are charmed by the {race} and directed to be annoying toward intruders in the area.")
	Figurines = Entry_Text("Dolls","Strange carved figurines, twig fetishes, or rag dolls magically appear in trees.")
	Slime = Entry_Text("Slime", "Most surfaces are covered by a thin film of slime, which is slick and sticks to anything that touches it.")
	VisionsOfBeyond= Entry_Text("Visions of Beyond","Intelligent creatures see hallucinations of dead friends, family members, and even themselves, as figures from the realms of the dead. Any attempt to interact with a hallucinatory image causes it to disappear.")
	Nightmares = Entry_Text("Nighmares", "When sleeping, creatures are transported to a harmless but eerie demiplane filled with shadowy forms, waxy corpses, and cackling. ")
	EldritchMists = Entry_Text(
		"Eldritch Mists",
		"A dense, greenish mist clings to the ground, reducing visibility to 30 feet. Voices, screams and whispers can be heard comming from the mist."
		)
	FungalBloom = Entry_Text(
		"Fungal Bloom",
		f"Massive fungal growths as tall as trees sprout. If eaten, the creature must make a DC {dc-1} Constitution saving throw or become poisoned for 1 hour."
		)
	AncestralGuidance = Entry_Text(
		"Ancestral Guidance",
		"The spirits of the ancestors can guide their champions on this sacred land. {alignment} creatures within the 1 mile feel an uplifting presence from ancestral entities. {alignment} creatures are under the Guidance spell while they stay in the area."
		)
	GravityDistortion = Entry_Text(
		"Gravity Distortion",
		"Gravity warps within a mile of the lair. Creatures have their jump distances halved and the range of attacks with a range get halved."
		)
	GravityDistortion2 = Entry_Text(
		"Gravity Distortion",
		"Gravity warps within a mile of the lair. Creatures have their jump distances doubled and the range of attacks with a range get doubled."
		)
	ArtistEffect = Entry_Text(
		"Eternal Masterpiece",
		f"Within a mile of {npc.title}'s domain, every place seems to contain an hipnotic, absorving artwork (Melodies in the wind, colors in the shadows, or essences blooming in petals. Creatures pausing to admire the beauty find themselves enthralled (DC {dc} Wisdom saving throw), losing focus on their tasks for 1 minute. Creatures affected are drwan toward the source."
		)
	BanditEffect = Entry_Text(
		"Ambush Grounds",
		f"{title} is a master of ambushes. The roads within a mile of {title}'s domain are fraught with hidden dangers. Travelers have disadvantage on Wisdom (Perception) checks to spot ambushes or traps."
		)
	BarbarianEffect = Entry_Text(
		"Howl of the Wild",
		f"The land within a mile of {npc.title}'s domain trembles with overwhelming primal energy. Creatures have advantage on their Wisdom Saving Throws and disadvantage on Intelligence Saving Throws as instincts overpower reason."
		)
	BardEffect = Entry_Text(
		"Enchanted Melodies",
		f"Distant music echoes faintly within a mile of {npc.title}'s lair. On a failed Charisma Saving Throw, the will of the creature gets affected by the melody, becoming Charmed by {title}."
		)
	CharlatanEffect = Entry_Text(
		"Illusory Deals",
		f"Shimmering mirages appear within a mile of {npc.title}'s domain. Creatures have disadvantage on detecting illusions."
		)
	ClericEffect = Entry_Text(
		"Sanctuary",
		f"This place holds the presence of divinity, marked with scent of incense lingering faintly. No mortal may fight within the sanctuary grounds (300 feet around the shrines) without angering the gods. Undeads gain a level of exhaustion while in the area."
		)
	CommonerEffect = Entry_Text(
		"Humble Prosperity",
		f"At the edge of civilization stands a settlement under {npc.title}'s watch. Orchards are heavy with fruit, fields wave golden, and wildlife ventures close to the village's edge, yet an air of stillness suggests not all is as tranquil as it seems."
		)
	CrafterEffect = Entry_Text(
		"Blooming Industry",
		f"{title}'s domain is expanding, taking over the surrounding nature. Forges puff plumes of smoke, rivers darken with runoff, and the distant clang of hammers echoes day and night. Within 1 mile, Nature is damaged or mutated."
		)
	MentorEffect = Entry_Text(
		"Walking Library",
		f"Legends about the knowledge and wisdom of {title} have reached wide and far, attracting pupils to {title}'s location. You may encounter students of this teachings within 1 mile."
		)
	MerchantEffect = Entry_Text(
		"Market Magnet",
		f"The fame of {title}'s products has turned the region into a bustling hub. Vendors and caravans converge here, creating impromptu markets filled with rare goods and enticing bargains. You may find objects of remarkable rarity within shops in 1 mile."
		)
	MonkEffect = Entry_Text(
		"The Enlightened Path",
		f"The region near {title}'s domain hums with disciplined energy. Disciples, seekers of truth, and wanderers converge here to sharpen their skills and find balance. Training rings and serene meditation groves dot the area, exuding a calm yet powerful aura."
		)
	NinjaEffect = Entry_Text(
		"Shroud of Silence",
		f"The presence of {title} cloaks the area in an eerie stillness. Villages nearby are distrustful and secretive, with people speaking in hushed tones. The forest around their lair seems to conspire, offering no clear paths to outsiders."
		)
	NobleEffect = Entry_Text(
		"Courtly Domain",
		f"The influence of {title} radiates throughout the land. Peasants bow lower, roads are cleaner, and the architecture exudes sophistication and grandeur. {title}'s will is law. Anyone entering this territory must ask for permision or carry a signed pass."
		)
	PaladinEffect = Entry_Text(
		"Sanctuary of Light",
		f"The ground near {title}'s domain glows faintly, as if touched by divine favor. Travelers speak of feeling safer, their spirits lifted, and even their wounds mending faster under the radiant skies."
		)
	PirateEffect = Entry_Text(
		"Rogue's Refuge",
		f"The villages near {title}'s domain teems with tales of danger and adventure. Rumors of hidden treasures fill taverns, while locals trade in whispered rumors and half-forgotten maps."
		)
	RangerEffect = Entry_Text(
		"Warden's Haven",
		f"Nature thrives in perfect harmony around {title}'s domain. Rare beasts roam unafraid, and ancient trees form a cathedral of untouched wilderness. Travelers, tread lightly. Be aware of the protective eyes upon you."
		)
	SoldierEffect = Entry_Text(
		"Legacy of Valor",
		f"Marching routes and fortified outposts define the lands near {title}'s domain. Veterans and recruits alike gather to train or reminisce, their camaraderie echoing in the cadence of disciplined drills."
		)
	RogueEffect = Entry_Text(
		"Veil of Subterfuge",
		f"Within {title}'s domain, nothing is as it seems. Markets teem with coded exchanges, and back alleys hide silent watchers. Those who enter may find themselves pawns in a game they never agreed to play."
		)
	SpyEffect = Entry_Text(
		"Web of Secrets",
		f"Around {title}'s domain, no word goes unnoticed. Every village hides an informant, and even the wind seems to whisper intrigue. Travelers feel watched, as though every step feeds into an unseen agenda."
		)
	TricksterEffect = Entry_Text(
		"Realm of Mirth",
		f"The land surrounding {title}'s domain are confusing and mindbending. Roads twist unexpectedly, objects vanish only to reappear in improbable places, and distances and time seems random."
		)
	PaladinEffect = Entry_Text(
		"Inspiration",
		f"The lands around {title}'s domain feel a strong inspiration and influence. Strongholds of idealistic and ardent followers rise like beacons. These followers rally under banners inspired by {title}'s unwavering ideals. Travelers speak of a calm yet unyielding authority that compels even the wayward to tread carefully."
		)
	PriestEffect = Entry_Text(
		"Sacred Ascent",
		f"Pilgrims flock to {title}'s domain, drawn by the whispered promises of divine blessings and miracles. The people hum with hymns of devotion, and the sick and weary often find unexplainable solace. Even nature seems to bow in reverence, as the land itself is blessed."
		)
	ScholarEffect = Entry_Text(
		"Field of Knowledge",
		f"The region surrounding {title}'s domain is a haven for wisdom-seekers. Ancient runes, hidden libraries, and wandering sages dot the landscape, each a fragment of the grand tapestry of knowledge curated by {title}. The curious find themselves stumbling upon revelations as if they are obvious."
		)
	ShamanEffect = Entry_Text(
		"Spirit's Respite",
		f"In {title}'s domain, the veil between worlds feels thin. The whispers of ancestors guide the living, and even the winds carry the faint echo of wisdom. Visitors often find themselves inexplicably rejuvenated, their burdens eased as the spirits of the land offer silent aid."
		)
	SorcererEffect = Entry_Text(
		"Tides of Chaos",
		f"Within the domains of {title}, within 1 mile, reality seems pliable, as if bent by the weight of untamed magic. Flickers of light and strange distortions hint at currents of wild magic. Travelers often leave with tales of phenomena too bizarre to recount without skepticism. When any creature casts a spell, they should roll in the Wild Magic Table (Player Handbook)."
		)
	TravelerEffect = Entry_Text(
		"Gathering of Paths",
		f"Campsites and bustling outposts spring up wherever {title}'s sets camp, drawing wanderers from every corner. Here, the air is alive with shared stories, and the mingling of cultures creates a tapestry of adventure that inspires all who pass through."
		)
	Circus = Entry_Text(
		"Wandering Carnival",
		f"The region surrounding {title}'s domain is alive with vibrant tents and traveling performers. Music, laughter, and the scent of exotic foods create an air of festivity, attracting wanderers and adventurers alike. However, hidden beneath the revelry are whispers of secrets traded and schemes unfolding."
		)
	WarlockEffect = Entry_Text(
		"Shadowed Covenant",
		f"An unnatural stillness pervades {title}'s domain, broken only by the faint whispers of distant entities. Symbols of eldritch origin mark the terrain, and an oppressive presence weighs heavily on the hearts of those who stray too close."
		)
	WarriorEffect = Entry_Text(
		"Field of Strife",
		f"The land near {title}'s domain is marked by the echoes of a battle. Broken weapons and scattered armor litter the soil, while swords rust with no memory of their wielder."
		)
	WitchEffect = Entry_Text(
		"Bewitched Swamp",
		f"In the shadow of {title}'s domain, the forest pulses with a life of its own. Strange lights flicker among ancient trees, and the very air seems to hum with the power of forgotten spells. The brave and the foolish alike are drawn to its haunting allure."
		)
	WizardEffect = Entry_Text(
		"Arcane Bastion",
		f"Towering spires and intricate glyphs dominate {title}'s domain, a testament to unmatched magical mastery. The land feels alive with arcane energy, and bizarre phenomena offer a glimpse into experiments that push the boundaries of reality itself."
		)


	effects = []

	effects_background = {
		"Artist": [     Circus,					TravelerEffect,			SorcererEffect,			ScholarEffect,			PaladinEffect,			NobleEffect,			MerchantEffect,			CrafterEffect,			CommonerEffect,			CharlatanEffect,		BardEffect,				ArtistEffect,			Figurines,				artistic_hallucination, eternal_twilight,       ],
		"Bandit": [		RogueEffect,			PirateEffect,			NinjaEffect,			BanditEffect,			],
		"Barbarian": [	WarriorEffect,			SorcererEffect,			RangerEffect,			BarbarianEffect,		AncestralGuidance,		beast_guardians,		],
		"Bard":[		Circus,					TravelerEffect,			SorcererEffect,			ScholarEffect,			PaladinEffect,			PirateEffect,			CharlatanEffect,		ArtistEffect,			AncestralGuidance,		],
		"Berserker":[   WarriorEffect,			inhospitable,           ],
		"Criminal": [	SpyEffect,				RogueEffect,			PirateEffect,			NobleEffect,			NinjaEffect,			],
		"Cultist":[     WarlockEffect,			ShamanEffect,			ScholarEffect,			PaladinEffect,			NobleEffect,			NinjaEffect,			MonkEffect,				EldritchMists,			VisionsOfBeyond,		inhospitable,           shadow_whispers,        pests,  ],
		"Charlatan":[	Circus,					TravelerEffect,			PaladinEffect,			TricksterEffect,		SpyEffect,				RogueEffect,			PirateEffect,			CharlatanEffect,		BardEffect,				ArtistEffect,			Figurines				],
		"Crafter":[		WizardEffect,			ScholarEffect,			CrafterEffect,			CharlatanEffect,		ArtistEffect,			Figurines				],
		"Cleric": [		ShamanEffect,			PriestEffect,			PaladinEffect,			MonkEffect,				ClericEffect,			AncestralGuidance,		VisionsOfBeyond			],
		"Commoner":[	TravelerEffect,			PaladinEffect,			PirateEffect,			CommonerEffect,			AncestralGuidance,		beast_guardians			],
		"Crafter": [	WizardEffect,			MerchantEffect,			],
		"Druid": [    	WitchEffect,			PriestEffect,			RangerEffect,			NobleEffect,			AncestralGuidance,		FungalBloom,			beast_guardians,		BeastCharm,		 		EternalBreeze,          pests,                  ],
		"Expert": [		WizardEffect,			PaladinEffect,			NobleEffect,			MonkEffect,				MentorEffect,			CrafterEffect,			],
		"Explorer": [	TravelerEffect,			RangerEffect,			PirateEffect,			MonkEffect,				],
		"Fighter": [	WarriorEffect,			SoldierEffect,			NobleEffect,			MonkEffect,				],
		"Guard": [		TravelerEffect,			SoldierEffect,			RangerEffect,			NobleEffect,			CommonerEffect,	],
		"Healer":[		PriestEffect,			PaladinEffect,			RangerEffect,			MonkEffect,				ClericEffect,			beast_guardians,		],
		"Hunter": [		TravelerEffect,			RangerEffect,			BarbarianEffect,		beast_guardians,		BeastCharm,			    pests,                  hider,                  wildlife,beast_guardians],
		"Hero":[		WarriorEffect,			TravelerEffect,			PaladinEffect,			SoldierEffect,			PirateEffect,			NobleEffect,			MonkEffect,				CommonerEffect,			AncestralGuidance		],
		"Knight": [		WarriorEffect,			SoldierEffect,			NobleEffect,			],
		"Mage":[        WizardEffect,			SorcererEffect,			ScholarEffect,			CharlatanEffect,		EldritchMists,			EternalBreeze,          ],
		"Monk": [		ShamanEffect,			ScholarEffect,			PriestEffect,			RangerEffect,			MonkEffect,				CommonerEffect,			ClericEffect,			AncestralGuidance,		beast_guardians,		],
		"Mentor": [		ShamanEffect,			MonkEffect,				MentorEffect,			CommonerEffect,			],
		"Merchant": [	TravelerEffect,			SpyEffect,				PirateEffect,			MerchantEffect,			],
		"Noble": [		SoldierEffect,			NobleEffect,			AncestralGuidance,		],
		"Ninja": [		WarlockEffect,			RogueEffect,			PirateEffect,			NinjaEffect,			EldritchMists,			],
		"Priest":[		ScholarEffect,			PaladinEffect,			NobleEffect,			MonkEffect,				CommonerEffect,			ClericEffect,			VisionsOfBeyond			],
		"Paladin": [	WarriorEffect,			PaladinEffect,			PaladinEffect,			PaladinEffect,			SoldierEffect,			RangerEffect,			MentorEffect,			AncestralGuidance		],
		"Pirate": [		PriestEffect,			PirateEffect,			MerchantEffect,			],
		"Ranger":[		TravelerEffect,			RangerEffect,			CommonerEffect,			beast_guardians,		],
		"Rogue": [		SpyEffect,				RogueEffect,			PirateEffect,			NinjaEffect,			MerchantEffect,			],
		"Scholar": [	WizardEffect,			SorcererEffect,			ShamanEffect,			ScholarEffect,			PaladinEffect,			PirateEffect,			MonkEffect,				MentorEffect,			],
		"Shaman":[     	WitchEffect,			WarlockEffect,			SorcererEffect,			ShamanEffect,			ShamanEffect,			ShamanEffect,			PriestEffect,			RangerEffect,			MonkEffect,				beast_guardians, 		VisionsOfBeyond,		BeastCharm,				EternalBreeze,          pests,                  ],
		"Sorcerer":[    WizardEffect,			WarlockEffect,			SorcererEffect,			SorcererEffect,			SorcererEffect,			RangerEffect,			CharlatanEffect,		EldritchMists,			inhospitable,           EternalBreeze,          ],
		"Spy": [		SpyEffect,				RogueEffect,			PirateEffect,			NinjaEffect,			CommonerEffect,			],
		"Soldier": [	TravelerEffect,			SoldierEffect,			PirateEffect,			NobleEffect,			MonkEffect,				],
		"Traveler": [	Circus,					Circus,					TravelerEffect,			TravelerEffect,			TravelerEffect,			PirateEffect,			MonkEffect,				MerchantEffect,			MentorEffect,			],
		"Trickster": [	Circus,					Circus,					SorcererEffect,			SpyEffect,				RogueEffect,			PirateEffect,			BardEffect,				ArtistEffect,			EldritchMists,			Figurines,				],
		"Warrior": 	[	WarriorEffect,			WarriorEffect,			WarriorEffect,			SoldierEffect,			PirateEffect,			CommonerEffect,			],
		"Warlock":[     WizardEffect,			WitchEffect,			WarlockEffect,			SorcererEffect,			ShamanEffect,			ScholarEffect,			PaladinEffect,			SpyEffect,				NinjaEffect,			MentorEffect,			EldritchMists,			Slime,					BeastCharm,				inhospitable,           EternalBreeze,          ],
		"Witch":[       WitchEffect,			WarlockEffect,			SorcererEffect,			ShamanEffect,			PriestEffect,			CharlatanEffect,		ArtistEffect,			EldritchMists,			beast_guardians,		Figurines,				BeastCharm,				inhospitable,           EternalBreeze,          shadow_whispers,        eternal_twilight,   pests],
		"Wizard":[      WizardEffect,			WarlockEffect,			Circus,					SorcererEffect,			ScholarEffect,			NobleEffect,			NinjaEffect,			MonkEffect,				MerchantEffect,			CrafterEffect,			CharlatanEffect,		EternalBreeze,          ],
		}
	effects_race = {
		"Aberration": [ WitchEffect,			WarlockEffect,			NinjaEffect,			GravityDistortion,				GravityDistortion2,				EldritchMists,					Slime,			EternalBreeze,  inhospitable,   wildlife],
		"Aven":[        RangerEffect,			beast_guardians,				EternalBreeze,  ],
		"Beast":[      	WitchEffect,			SorcererEffect,			RangerEffect,			ClericEffect,					BardEffect,						BarbarianEffect,				beast_guardians,				BeastCharm,	 	pests,          ],
		"Beastfolk": [  WarlockEffect,			RangerEffect,			BarbarianEffect,				beast_guardians,				BeastCharm,		pests,          hider,          beast_guardians],
		"Catfolk":[		WarlockEffect,			RangerEffect,			BarbarianEffect,				beast_guardians,				],
		"Celestial" : [ ShamanEffect,			PriestEffect,			PaladinEffect,			MonkEffect,				MentorEffect,			ClericEffect,			GravityDistortion,				GravityDistortion2,				VisionsOfBeyond,				healing_aura,   hider,          no_flames,anticursed,compulsory_offering],
		"Construct": [	SorcererEffect,			CrafterEffect,			Figurines		],
		"Dragon": [     SorcererEffect,			NobleEffect,			inhospitable,   wildlife,       volcan,compulsory_offering],
		"Dwarf": [		CrafterEffect,			],
		"Elemental":[   WizardEffect,			SorcererEffect,			inhospitable,   EternalBreeze,  ],
		"Elf":[			RangerEffect,			NobleEffect,			BanditEffect,					ArtistEffect,					beast_guardians,				],
		"Fey":[         SorcererEffect,			RangerEffect,			ArtistEffect,					EldritchMists,					BeastCharm,		pests,          compulsory_offering],
		"Fiend":[      	WarriorEffect,			WarlockEffect,			ShamanEffect,			SpyEffect,				NinjaEffect,			EldritchMists,	 				VisionsOfBeyond,				inhospitable,   EternalBreeze,  ],
		"Giant":[       NobleEffect,			CrafterEffect,			BarbarianEffect,				EternalBreeze,  ],
		"Gnome":[		TravelerEffect,			SorcererEffect,			RangerEffect,			ArtistEffect,					FungalBloom,	],
		"Goblin":[      SorcererEffect,			FungalBloom,	beast_guardians,				pests,          ],
		"Halfling": [	beast_guardians,				],
		"Human": [		ShamanEffect,			beast_guardians,				],
		"Kobold":[      pests,          ],
		"Lizardfolk":[  ShamanEffect,			beast_guardians,				BeastCharm,		pests,          ],
		"Monstrosity":[	WarriorEffect,			NinjaEffect,			BarbarianEffect,				FungalBloom,	],
		"Ooze":[        FungalBloom,			Slime,			inhospitable,   ],
		"Orc": [		WarriorEffect,			ShamanEffect,			BarbarianEffect,				beast_guardians,				],
		"Plant":[       SorcererEffect,			RangerEffect,			beast_guardians,				Slime,			BeastCharm,		pests,          ],
		"Snakefolk":[   WitchEffect,			WarlockEffect,			SpyEffect,				BanditEffect,					beast_guardians,				pests,          ],
		"Undead": [     WitchEffect,			WarriorEffect,			WarlockEffect,			ShamanEffect,			NinjaEffect,			EldritchMists,					VisionsOfBeyond,			inhospitable,   shadow_whispers,    eternal_twilight,    pests,risen_dead,moving_shadows,wither,no_flames],
		}

	effects_subrace = {
		"Archfey": [SorcererEffect,			RangerEffect,			NobleEffect,			],
		"Demon":[		pests],
		"Eldritch Horror":[		pests],
		"Fungical Intelectual": [	FungalBloom],
		"Forester":[	pests],
		"Gaians":[		pests],
		"Genie": [		NobleEffect,			MonkEffect,				],
		"Harpy": [		BardEffect,	],
		"Hag": [		NinjaEffect,			],
		"Lycan": [		NinjaEffect,			],
		"Myceliumanoid": 	[	FungalBloom],
		"Myconid Sovereign": [	FungalBloom],
		"Merfolk": [		BardEffect,	],
		"Moira": [		NinjaEffect,	],
		"Ogre":[		pests],
		"Oni": [		NinjaEffect,],
		"Parasyte":[	pests],
		"Parca": [		NinjaEffect,],
		"Sands Elf":[	pests],
		"Shadow Kobold":[	shadow_whispers,   eternal_twilight,  pests],
		"Swamp": [		FungalBloom],
		"Scarecrow":[	NinjaEffect,			VisionsOfBeyond,		pests],
		"Sylvan Elf":[	pests],
		"Spider Queen": [NinjaEffect,				],
		"Singing Lotus": [		BardEffect,	],
		"Unicorn": [	RangerEffect,			],
		"Vampire": [	EldritchMists,		inhospitable,	beast_guardians],
		"Wood Elf":[	RangerEffect,			pests],
		"Wild Elf":[	RangerEffect,			pests],
		"Werewolf": [	RangerEffect,			NinjaEffect,			],
		}

	# Fetch the extra effects for the selected race and background
	effects += list(effects_race.get(race, []) +
					effects_subrace.get(subrace, []) +
					effects_background.get(archetype, []))

	if "Dragon Turtle" in subrace and pests not in effects:
		effects.append(pests)

	# Eliminate redundancies
	number_of_effects = min(len(effects),
							Dice(2))

	# Select and format effects
	effects = random.sample(effects, number_of_effects) if effects else []
	effects = list(set(effects))
	result_list = '\n\n'.join(effects) if effects else None
	if result_list:
		result = (
			pre + '<i>' + result_list  + '</i>' + dissipation_note
			)
		return result
	else:
		return None
