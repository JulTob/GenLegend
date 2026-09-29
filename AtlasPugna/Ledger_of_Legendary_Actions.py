import random

try:
	from AtlasScriptum.Map_of_Formats import Entry_Text
	from AtlasLudus.Map_of_Dice import Dice
	from AtlasLudus.Map_of_Scores import PB
	import AtlasPugna.Grimoire_of_Attacks as attacks
except ImportError:
	raise


# General actions
Detect = 		Entry_Text(
		"Detect"
		f"{title} makes a Wisdom (Perception) check. {title} can use this check to find a hidden creature, spot, hear, or otherwise detect the presence of something."
		)
Attack = 		Entry_Text(
	f"Attack",
	f"{npc.title} can do one simple attack to any creature")
Move = 			Entry_Text(
	f"Move",
	f"{title} can move half their movement")
wing_Attack = 	Entry_Text(
	f"Wing Attack",
	random.choice([
		f"{title} beats its wings. Each creature within 10 feet of {title} must succeed on a DC{base_pb + STR} DEX saving throw or take {3*2 + STR} (2d6{STR:+}) bludgeoning damage and be knocked prone.",
		f"Each creature within 10 feet must succeed on a DC {8+pb+STR} DEX save or take {Dice(pb//2)}d6 + {STR} bludgeoning damage and be knocked prone."]),
	f"(Costs 2 Actions)")
command_ally = 	Entry_Text(
	f"Command Ally",
	f"{title} issues a command to one of its allies, allowing the ally to immediately take an extra action on {title}'s turn.")
radiant_blast = Entry_Text(
	f"Radiant Blast",
	f"{title} releases a burst of radiant energy, targeting one creature it can see within 60 feet. The target must succeed on a Wisdom saving throw DC {dc} or take {Dice(pb//2)}d6 radiant damage and be blinded until the end of {title}'s next turn.")
tail_sweep = 	Entry_Text(
	"Tail Sweep",
	f"{title} makes a tail attack against all creatures within 10 feet. Each must succeed on a DC {8+pb+STR} Dexterity saving throw or take {Dice(pb//2)}d6 bludgeoning damage and be knocked prone.")
frightful_presence = Entry_Text(
	"Frightful Presence",
	f"Each creature of {title}'s choice within {5*Dice(2)*Dice(2)} feet and aware of it must succeed on a Wisdom saving throw or become frightened for 1 minute."        )
mind_warp = 	Entry_Text(
	"Mind Warp",
	f"{title}  targets one creature it can see within 60 feet, assaulting its mind. The target must make a DC {dc} Intelligence saving throw or take {Dice(pb//2)}d6 psychic damage and be stunned until the end of {title}'s next turn."        )
warp_reality = 	Entry_Text(
	"Warp Reality",
	f"{title} alters reality in a small area, creating difficult terrain within {5*Dice()} feet."        )
deathly_touch = Entry_Text(
	"Deathly Touch",
	f"{title} touches one creature, forcing it to make a DC {dc} Constitution saving throw or take {Dice(pb//2)}d4 necrotic damage."        )
battle_cry = 	Entry_Text(
	f"Battle Cry",
	f"{title} rallies their allies, granting them courage. All allies that can hear, within {Dice()*10} feet, become immune to the Frightened condition for 1 minute."        )
deadly_gaze = 	Entry_Text(
	f"Deadly Gaze",
	f"The target becomes frightened on a failed DC{dc} Wisdom saving throw.")
death_touch = 	Entry_Text(
	f"Death Touch",
	f"{title} delivers a chilling touch, causing {Dice(pb//2)}d4 necrotic damage on a successful attack.",        )
terrifying_visage = Entry_Text(
	f"Terrifying Visage",
	f"{title} reveals its horrifying true form, causing all nearby enemies to make a DC{dc} Wisdom saving throw or become frightened."        )
tactical_maneuver = Entry_Text(
	f"Tactical Maneuver",
	f"{title} directs an ally, granting advantage to their next attack.")
inspiring_display = Entry_Text(
	f"Inspiring Display",
	f"{title} performs a stunning display, inspiring an ally within sight to take an extra action.")
swarm_tactics = Entry_Text(
		f"Swarm Tactics",
		f"{title} directs its allies in a coordinated attack, all allies within {Dice(2)*Dice(3)*10} feet of {title} can move up to half their speed.")
SwiftMovement = Entry_Text(
	"Swift Movement",
	f"{title} uses their knowledge of the terrain to move quickly or create an escape route. {title} moves up to their speed without provoquing opportunity attacks.")
LuckyBreak = 	Entry_Text(
	f"Lucky Break",
	f"{title} provoques disadvantage to the next attack targeted at them.",)
SneakyStrike = 	Entry_Text(
	f"Sneaky Strike",
	f"{title} makes a stealthy attack, gaining advantage if the target has an enemy within 5 feet of them.")
NimbleDodge = 	Entry_Text(
	f"Nimble Dodge",
	f"{title} moves quickly, gaining a +2 AC until the start of their turn.")
SerpentineGrace = Entry_Text(
	f"Serpentine Grace",
	f"{title} slithers quickly, avoiding attacks and repositioning itself. {title} moves half his speed without provoking opportunity attacks")
VenomousBite = 	Entry_Text(
   f"Venomous Bite",
   f"{title} delivers a poisonous bite to a creature it can reach within 5 feet. On a hit of a melee weapon attack the target receives {Dice(PB(pb//2))}d4 poison damage, and becomes poisoned")
QuickFix = 		Entry_Text(
	f"Quick Fix",
	f"{title} can use a cantrip that takes 1 Action.")
DeceptiveManeuver = Entry_Text(
	f"Deceptive Maneuver",
	f"{title} confuses an enemy, causing it to have disadvantage on its next attack.")
ProtectiveShift = 	Entry_Text(
	f"{race} Shift",
	f"{title} alters its form, gaining resistance to a damage type of its choice until its next turn.")
ElementalBlast = 	Entry_Text(
	f"Elemental Blast",
	random.choice([
		f"{title} sends out a burst of elemental energy in a line, requiring a DC{dc} Dexterity saving throw from affected creatures or take {Dice(pb//2)}d6 {attacks.Damage()} damage."
		f"{title} sends out a burst of elemental energy in a cone, requiring a DC{dc} Dexterity saving throw from affected creatures or take {Dice(pb-1)}d4 {attacks.Damage()} damage.",
		]))
BeguilingGaze = Entry_Text(
	f"Beguiling Gaze",
	random.choice([
		f"{title} targets one creature it can see, charming it, unless the target succeeds on a DC{dc} Wisdom saving throw.",
		f"{title} targets one creature it can see, putting it to sleep, unless the target succeeds on a DC{dc} Wisdom saving throw."
		]))
NaturesWrath = 	Entry_Text(
	f"Nature's Wrath",
	f"{title} summons vines or thorns in an area within {5*Dice(2)*Dice(2)*Dice(2)*Dice(2)*Dice(3)}, making it difficult terrain. Every creature that starts its turn within the area takes 1d4 damage."
	)
HellfireBlast = Entry_Text(
	f"Hellfire Blast",
	f"{title} releases a burst of hellfire, causing {intensity}d4 fire damage to all creatures within {5*Dice(2)*Dice(2)*Dice(3)} area."        )
MinionCommand = Entry_Text(
	f"Infernal Command",
	f"{title} commands his minions to attack a target creature, allowing them to attack immediately, using their reaction to do an attack to that target.")
MightyThrow = 	Entry_Text(
	f"Mighty Throw",
	f"{title} throws a large rock or similar object at a target, causing {intensity}d6 damage on impact.")
Stomp = 	Entry_Text(
	f"Stomp",
	f"{title} stomps the ground, creating a shockwave within {5*Dice(2)*Dice(3)} feet that knocks nearby creatures prone unless they succeed on a DC{base_pb+STR} Strength saving throw.")
IngeniousTrap = Entry_Text(
	f"Ingenious Trap",
	random.choice([
		f"{title} quickly assembles and sets a trap, which can ensnare a creature within 5 feet of it, making it prone, unless the target succeeds on a DC{dc} Dexterity saving throw.",
		f"{title} quickly assembles and sets a trap, which can damage a creature within 5 feet of it, making 1d6 of {attacks.Damage()} damage, unless the target succeeds on a DC{dc} Dexterity saving throw.",
		]))
SmallEscape = 	Entry_Text(
	f"{race}'s Escape",
	random.choice([
		f"{title} teleports up to {Dice(2)*Dice(3)*5} feet.",
		f"{title} becomes temporarily invisible until the start of their turn."
		]))
SneakyStab = 	Entry_Text(
	f"Sneaky Stab",
	f"{title} makes a sudden simple melee attack with advantage on its attack roll."),
Disappear = 	Entry_Text(
	f"Disappear",
	f"{title} blends into its surroundings, becoming hidden to its enemies. Any wisdomm check to discern his location and Ranged attack rolls have disadvantage.")
QuickTinkerer = Entry_Text(
	f"Quick Tinkerer",
	f"{title} quickly activates a tinkered device that, on a failed Dexterity saving throw DC{dc}, blinds an enemy within 5ft of {npc.title} until the end ot the next creature's turn.")
ScaledDefense = Entry_Text(
	f"Scaled Defense",
	f"{title} hardens its scales, gaining +2 AC until the start of their turn.")
SwiftReptile = 	Entry_Text(
	f"Swift Reptile"
	f"{title} scapes swiftly, moving up to their speed without provoking opportunity attacks.")
TerrifyingRoar = 	Entry_Text(
	f"Terrifying Roar",
	f"{title} emits a fearsome roar, causing an enemy within 5 feet to become frightened on a failed DC{base_pb+CHA} Wisdom saving throw.")
RendNTear = 	Entry_Text(
	f"Rend and Tear",
	f"{title} makes a special or normal attack against a single target.")
Engulf = 	Entry_Text(
	f"Engulf",
	f"{title} attempts to engulf a nearby smaller creature, trapping it inside its body, unless the creature succeeds a DC {base_pb+STR} Dexterity Saving Throw, being restrained on a fail.")
CorrosiveTouch = 	Entry_Text(
	f"Corrosive Touch",
	f"{title} makes a simple melee attack, dealing an extra {intensity}d6 acid damage on a hit.")
WarCry = 	Entry_Text(
	f"War Cry",
	f"{title} lets out a powerful cry, bolstering the morale of allies and intimidating enemies. Within {Dice(2)*Dice(2)*Dice(3)*10} feet, all allies of {title} become immune to the Frightened condition, and enemies within the range make a DC {dc} Wisdom saving throw or become Frightened")
BrutalStrike = 	Entry_Text(
	f"Brutal Strike",
	f"{title} makes a simple attack. On a hit, the target becomes Prone.")
EntanglingRoots = 	Entry_Text(
	f"Entangling Roots",
	f"{title} causes roots to burst from the ground, attempting to entangle nearby creatures. The terrain within {Dice(2)*Dice(2)*Dice(3)*5} feet becomes difficult terrain. {title} is immune to this effect.")
heal_self = 	Entry_Text(
	f"Heal Self",
	f"{title} magically regains {2*4+CON} (2d8 + {CON}) hit points.",
	"(Costs 3 Actions)")
HealingFlux = 	Entry_Text(
	f"Healing Flux",
	f"{title} exudes restorative energy, healing itself or an ally within 5 feet. The target heals 1d4{WIS:+}")
TacticalAmbush = 	Entry_Text(
	f"Tactical Ambush",
	f"{title} uses his cunning and gains a tactical advantage, gaining advantage on its first attack roll against a target.")
shimmering_shield = Entry_Text(
	f"Shimmering Shield",
	f"{title} creates a shimmering, magical field around itself or another creature it can see within 60 feet of it. The target gains a +2 bonus to AC until the end of {title}'s next turn.",
	"(Costs 2 Actions)")
BardicInspiration = Entry_Text(
	f"Bardic Inspiration",
	f"{title} inspires an ally within earshot, granting them a bonus to their next ability check, attack roll, or saving throw of 1d{2*(1+Dice(5))}.")
Rage = 	Entry_Text(
	f"Rage",
	f"{title} enters a state of rage, gaining bonus of {1+ pb//2} to melee damage, and gains resistance to bludgeoning, piercing, and slashing damage.")
FrenziedAttack = 	Entry_Text(
	f"Frenzied Attack",
	f"{title} makes an attack with advantage against a single target. The next attack against {title} gains advantage.")
DivineInspiration = Entry_Text(
	f"Divine Inspiration",
	f"{title} calls upon their deity for inspiration, healing an ally {pb//2}d4.")
UnexpectedCourage = Entry_Text(
	f"Unexpected Courage",
	f"{title} rallies their inner strength, attacking with extraordinary bravery. It makes a simple attack. The attack is a Critical hit on a 19 or 20 on the atttack roll.",
	"Costs 2 actions")
DarkRitual = 	Entry_Text(
	f"Dark Ritual",
	f"{title} quickly performs a sinister ritual, targeting one creature it can see within 30 feet. The target must succeed on a DC {dc} Wisdom saving throw or become cursed. While cursed, the target takes an additional 2 (1d4) necrotic damage whenever it takes damage from any source. The curse lasts for 1 minute or until {title} is incapacitated or dies.",
	"Costs 2 Actions")
NaturesAid = 	Entry_Text(
	f"Nature's Aid",
	random.choice([
		f"{title} calls upon nature to assist, by healing an ally {pb//2}d4.",
		f"{title} calls upon nature to assist, entangling an enemy. On a failed DC{dc} Dexterity saving throw the enemy is restrained."
		]))
Pathfinder = 	Entry_Text(
	f"Pathfinder",
	f"{title} can move their full speed without provoking opportunity attacks.")
ProtectiveStance = 	Entry_Text(
	f"Protective Stance",
	f"{title} takes a defensive position, granting increased {1+pb//4:+} AC to themselves and one other creature within 5 feet.")
SwiftAid = 	Entry_Text(
	f"Swift Aid",
	f"{title} quickly tends to an ally's wounds, restoring {pb-1}d6 hit points.")
HeroicSacrifice = 	Entry_Text(
	f"Heroic Sacrifice",
	f"{title} finds the strength to keep fighting, gaining {pb//2}d6 temporary hit points.",
	"Costs 2 Actions")
PreciseShot = 	Entry_Text(
	f"Precise Shot",
	f"{title} makes a special attack.")
ChivalrousCharge = 	Entry_Text(
	f"Chivalrous Charge",
	f"{title} charges an enemy, moving half their speed and doing a simple attack.")
ArcaneBurst= 	Entry_Text(
	f"Arcane Burst",
	f"{title} releases a burst of magical energy. All creatures within {Dice(3)*Dice(2)*5} feet receive {pb//2}d6 {attacks.Damage()} damage")
KiStrike = 	Entry_Text(
	f"Ki Strike",
	f"{title} channels their ki energy to make rapid strikes, making two simple attacks.")
CommandingPresence = 	Entry_Text(
	f"Commanding Presence",
	f"{title} commands an ally, allowing them to move half their speed.")
Blessing = 	Entry_Text(
	 f"Blessing",
	 f"{title} blesses an ally, granting them a bonus 1d{2*(1+Dice(5))} to their next attack or saving throw.")
BoardingAction = 	Entry_Text(
	f"Boarding Action",
	f"{title} swiftly moves across the battlefield, engaging an enemy in close combat, moving their full speed and doing a simple attack.")
HuntersMark = 	Entry_Text(
	f"Hunter's Mark",
	f"{title} marks a target, granting a bonus {pb//2}d6 to damage on their next attack against that target.")
CunningAction = Entry_Text(
	f"Cunning Action",
	f"{title} uses their quick wits to gain advantage on their next action.")
MomentofClarity = 	Entry_Text(
	f"Moment of Clarity",
	f"{title} provides critical information or advice, granting advantage to an ally's next check.")
TacticalManeuver = 	Entry_Text(
	f"Tactical Maneuver",
	f"{title} directs their allies, granting advantage to their next attack.")
InsightfulDiscovery = 	Entry_Text(
	f"Insightful Discovery",
	f"{title} uses their knowledge to reveal an immunity, resistance, or vulnerability, or provide crucial information about an enemy's defenses.")
SpiritCall  = 	Entry_Text(
	f"Spirit Call",
	random.choice([
		f"{title} calls upon the spirits to aid in battle, healing all allies within {5*Dice(2)*Dice(3)} feet {pb//2}d4 hit points.",
		f"{title} calls upon the spirits to aid in battle, harming all enemies that start their turn within {5*Dice(2)*Dice(3)} feet {pb//2}d4 hit points.",
		]))
CovertOperation = 	Entry_Text(
	f"Covert Operation",
	f"{title} sabotages an enemy, causing their next attack to be at disadvantage.")
StreetSmarts = 	Entry_Text(
	f"Street Smarts",
	f"{title} uses their survival skills to disengage, hide, or dash.")
BattleFrenzy = 	Entry_Text(
	f"Battle Frenzy",
	f"{title} enters a state of frenzy, increasing their attack capability for a short time. He makes a simple attack at disadvantage. On a hit, the target recives an extra {pb//2}d6 damage.")
Hex = 	Entry_Text(
	f"Hex",
	f"{title} places a curse on an enemy, causing their saving throws to have disadvantage for 1 minute.")
healing_touch = 	Entry_Text(
	f"Healing Touch",
	f"{title} touches another creature, healing it for {Dice(pb//2)}d4 of hit points.")
BattleCommand = 	Entry_Text(
	"Battle Command.",
	f"As a bonus action, {npc.title} targets one ally he can see within 30 feet of them. If the target can see or hear {npc.title}, the target can use its reaction to make one melee attack or to take the Dodge or Hide action.")
PsychicDrain = 	Entry_Text(
	f"Psychic Drain",
	f"One creature charmed by {title} One creature charmed by the aboleth takes {pb*3.5//2} ({pb//2}d6) psychic damage, and {title} regains hit points equal to the damage the creature takes.",
	"(Costs 2 Actions)")
Teleport = 	Entry_Text(
	"Teleport",
	f"{title} magically teleports, along with any equipment it is wearing or carrying, up to 120 feet to an unoccupied space it can see."
	"(Costs 2 Actions)")
CastASpell = 	Entry_Text(
	"Cast A Spell",
	"{title} casts a spell from its list of prepared spells, using a spell slot (or a daily use) as normal."
	)
ParalyzingTouch = 	Entry_Text("Paralyzing Touch",
	f"{npc.title} touches one creature within 5 feet of it. The target must succeed on a DC {npc.spell_save_dc} Constitution saving throw or be paralyzed for 1 minute. The target can repeat the saving throw at the start of each of its turns, ending the effect on itself on a success.",
	"(Costs 2 Actions)")
PsionicBlast =  	Entry_Text("Psionic Blast",
	f"{npc.title} emits a wave of psionic energy. Each creature in a 30-foot cone must succeed on a DC {npc.spell_save_dc} Intelligence saving throw or take {pb*4} ({pb}D8) psychic damage and be stunned for 1 minute. A stunned target can repeat the saving throw at the start of each of its turns, ending the effect on itself on a success.",
	"(Costs 3 Actions)")
DragonBreath =  	Entry_Text("Dragon Breath",
	f"{npc.title} exhales a torrent of destructive energy. Each creature in a 60-foot cone must make a DC {npc.spell_save_dc} Dexterity saving throw, taking {pb*4} ({pb}D8) {attacks.Damage()} damage on a failed save, or half as much damage on a successful one.",
	"(Costs 3 Actions)")
