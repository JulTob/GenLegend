'''
Great Grimoire of the NPC class
Carrying this grimoire allows for Summoning Non Player Characters
follows D&D 5e Rules
'''

''' Cartography '''
from threading import Thread, Event
import app.random as random

try:
	from AtlasLudus.Map_of_Dice import Dice, Dizero
	from AtlasActorLudi.Map_of_Scores import Modifier, PB
	from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores, apply_creature_ability_modifiers
	from AtlasActorLudi.Grimoire_of_SavingThrows import SavingThrows
	from AtlasActorLudi.Grimoire_of_Skills import Skills
	from AtlasAlusoris.Map_of_Races import race_weights, Race
	from AtlasAlusoris.Map_of_Archetypes import Archetypes, Archetype
except ImportError:
	raise

"""		NPC class    """
class NPC:
	def __init__(npc, race = None, archetype = None, lvl=1, seed=random.randint(0, 2**8), light= False):
		"""
		INVOCATION OF A NEW Non Player Character.

		Preconditions:
		-     <race> and <archetype> must be valid [strings].
		-     <lvl> must be an [integer] >= 1.

		Postconditions:
		- Generates an [NPC] with attributes based on the provided <race>, <archetype>, and <level>.
		"""
		# npc.ready = False

		# Set core values
		npc.seed = int(seed) if seed else random.randint(0, 64**6 - 1)
		npc._seed = npc.seed
		random.seed(npc.seed)

		npc.race =       	race if race else Race()
		npc.subrace =   	npc.SetSubrace()
		npc.archetype = 	archetype if archetype else Archetype()
		npc.level = 		max(lvl, 1)
		npc.gender = 		npc.SetGender()
		npc.name = npc.Naming()
		npc.title = npc.SetTitle()
		if not light:
			npc.size = npc.SetSize()

			npc.AS = AbilityScores(10, 10, 10, 10, 10, 10) # Default
			npc.AS.RandomAbilityScores()

			npc.AC = npc.SetAC()
			npc.HP = npc.SetHitPoints(npc.level)
			npc.speed = 30
			npc.movement = npc.SetMovement()
			npc.ST = SavingThrows(npc.AS, npc.proficiency_bonus)
			npc.skills = Skills(npc.AS, npc.proficiency_bonus)

			npc.ready = True

	@property
	def alignment(npc):
		random.seed(npc._seed)
		alignment = "Neutral"
		try:
			from AtlasActorLudi.Map_of_Alignments     import Alignment
			npc.alignment = Alignment()
		except:
			return "True Neutral"
		return alignment


	@property
	def passive_perception(npc):
		random.seed(npc._seed)
		return npc.skills.Passive(npc.skills.Perception)

	@property
	def languages(npc) -> list:
		from AtlasLudus.Map_of_Languages import Language
		random.seed(npc._seed)
		return Language(npc)

	@property
	def simple_attacks(npc):
		random.seed(npc._seed)
		return npc.SimpleAttack()

	@property
	def special_attack(npc):
		random.seed(npc._seed)
		return npc.SpecialAttack()

	@property
	def ideal(npc):
		from AtlasActorLudi.Map_of_Personality import Ideal
		random.seed(npc._seed)
		return  Ideal(npc)

	@property
	def plothook(npc)	-> str:
		from AtlasActorLudi.Map_of_Personality import PlotHook
		random.seed(npc._seed)
		return PlotHook(npc)

	@property
	def trait(npc)	-> str:
		""" Personality trait. """
		from AtlasActorLudi.Map_of_Personality import Trait
		random.seed(npc._seed)
		return Trait(npc)

	@property
	def spells(npc):
		random.seed(npc._seed)
		return npc.Magic()

	@property
	def story(npc):
		random.seed(npc._seed)
		return npc.SetMyStory()

	@property
	def abilities(npc):
		random.seed(npc._seed)
		return npc.SetAbilities()

	def set_name(npc):
		random.seed(npc._seed)
		npc.name =  npc.Naming()

	def set_title(npc):
		random.seed(npc._seed)
		npc.title = 	npc.SetTitle()

	def set_stats(npc):
		random.seed(npc._seed)
		npc.size = 	npc.SetSize()
		npc.AC = 	npc.SetAC()
		npc.HP = npc.SetHitPoints(npc.level)
		npc.speed = 30
		npc.movement = npc.SetMovement()
		npc.ST = SavingThrows(npc.AS, npc.proficiency_bonus)
		npc.skills = Skills(npc.AS,npc.proficiency_bonus)
		npc.passive_perception = npc.skills.Passive(npc.skills.Perception)
		npc.simple_attacks = npc.SimpleAttack()
		npc.special_attack = npc.SpecialAttack()
		#npc.stats_ready.set()

	@property
	def Skills(npc):
		random.seed(npc._seed)
		return npc.skills

	@property
	def ability_scores(npc):
		random.seed(npc._seed)
		return npc.AS

	def set_personality(npc):
		random.seed(npc._seed)
		npc.spells = npc.Magic()
		npc.personality_ready.set()

	def SetAbilities(npc):
		""" Determine the abilities of the NPC. """
		from AtlasPugna.Map_of_Abilities import Abilities
		random.seed(npc._seed)
		npc.abilities = Abilities(npc)
		return npc.abilities

	@property
	def ability_scores(npc):
		random.seed(npc.seed)
		return npc.AS

	def to_dict(npc):
		random.seed(npc.seed)
		return {
				"race": npc.race,
				"archetype": npc.archetype,
				"lvl": npc.level,
				"seed": npc.seed,
				}


	@classmethod
	def from_dict(cls, data):
		random.seed(npc.seed)
		return cls(
			race = data.get('race'),
			archetype = data.get('archetype'),
			lvl = data.get('lvl'),
			seed = data.get('seed'),
			)

	def SetGender(npc)	-> str:
		""" Set the gender of the NPC. """
		from AtlasActorLudi.Map_of_Gender	import NewGender, ElementalGender
		random.seed(npc.seed)
		try:
			npc.gender = NewGender()
			VALKYRE = "Valkyrie" in npc.subrace
			NYMPH = "Nymph" in npc.subrace
			if VALKYRE or NYMPH: npc.gender = "She"
			if "Elemental" in npc.race:
				npc.gender = ElementalGender(npc.subrace)
				return npc.gender
		except Exception:
			npc.gender = "They"
		return npc.gender

	def SetSize(npc)	-> str:
		""" Set the size of the NPC. """
		from AtlasActorLudi.Map_of_Size import Size
		random.seed(npc.seed)
		npc.size = Size(npc.Type)
		return npc.size



	def SetTitle(npc)	 -> str:
		""" Generate a title (a name they are known for) for the NPC. """
		random.seed(npc.seed)
		try:
			from AtlasEpica.Map_of_Titles import Title
			return Title(npc)
		except Exception:
			pass
		return f"The {npc.race} {npc.archetype}"

	def SetSubrace(npc)	-> str:
		""" Determine the subrace of the NPC. """
		from AtlasAlusoris.Map_of_Races    import Subrace
		random.seed(npc.seed)
		npc.subrace = Subrace(npc.race)
		return npc.subrace

	def Naming(npc)	-> str:
		""" Generate a name for the NPC. """
		random.seed(npc.seed)
		try:
			from AtlasNomina.Map_of_Names import NewName
			return NewName(npc)
		except Exception:
			return random.choice([
					"Zax",	"Jon",	"Nix",	"Max", "Tod",	"Raz",	"Mox"
					])

	def SetAC(npc)	-> int:
		"""
		Calculate the NPC's armor class
		based on various factors.

		Postconditions:
		<<	Returns an integer representing the NPC's armor class.
		"""
		''' Cartography '''
		from AtlasAlusoris.Map_of_Archetypes import AC_Archetype_modifier
		from AtlasAlusoris.Map_of_Races import AC_race_modifier

		random.seed(npc.seed)

		PB = npc.proficiency_bonus
		AC = 10 + Dice(Modifier(npc.AS.DEX)) + Dice(PB)

		# Apply additional AC based on archetype
		AC += Dizero(AC_Archetype_modifier(
			archetype= npc.archetype,
			STR = Modifier(npc.AS.STR),
			DEX = Modifier(npc.AS.DEX),
			CON = Modifier(npc.AS.CON),
			INT = Modifier(npc.AS.INT),
			WIS = Modifier(npc.AS.WIS),
			CHA = Modifier(npc.AS.CHA),
			))

		# Apply additional AC based natural resistances
		AC += Dizero(AC_race_modifier(
			race = npc.race,
			subrace = npc.subrace
			))

		if AC < 10 + PB: AC = 10 + PB
		if AC > 20 + PB: AC = 20 + PB

		return AC

	def SetHitPoints(npc, level: int) -> int:
		"""
		Determine and Set the hit points of the NPC.

		Preconditions:
		>> 		<level> must be an [integer] greater than or equal to 1.

		Postconditions:
		<<		Returns the calculated hit points as an [integer].
		"""
		random.seed(npc.seed)
		hit_dice_sides = Dice(3,4)
			# Each Dice(3) call rolls a 3-sided die
			# range: 4-12 , expected value: 8
		dice_hp = hit_dice_sides + Dice(
			D = hit_dice_sides,
			N = level-1)
		con_hp =  level * npc.ability_scores.con_mod

		if con_hp<0:
			con_hp = 0

		total_hp = dice_hp  +  con_hp

		npc.HP  = total_hp

		return  total_hp

	def SetMovement(npc)	-> str:
		""" Determine the NPC's movement capabilities. """
		from AtlasPugna.Map_of_Movement import Movement
		random.seed(npc.seed)
		npc.movement = Movement(npc)
		return Movement(npc)

	def SimpleAttack(npc)  -> str:
		""" Generate simple attack options for the NPC. """
		from AtlasPugna.Map_of_Attacks import Attack
		random.seed(npc.seed)

		count = max(Dice(1, PB(npc.proficiency_bonus)), 1) or 1

		simple_list = []
		for _ in range(count):
			new_attack = Attack(npc)
			if new_attack not in simple_list:
				simple_list.append(new_attack)
		simple = '\n'.join(simple_list)
		return simple

	def SpecialAttack(npc)	-> str:
		from AtlasPugna.Map_of_Attacks import SpecialAttack
		random.seed(npc.seed)
		special = ""
		special += SpecialAttack(npc)
		special += "\n"
		return special

	def SetName(npc)	-> str:
		random.seed(npc.seed)
		return npc.Naming(npc)

	def ProficiencyBonus(npc)	-> int:
		from AtlasActorLudi.Map_of_Scores import PB
		random.seed(npc.seed)
		return PB(npc.level)

	@property
	def senses(npc):
		from AtlasPugna.Map_of_Senses import Senses
		random.seed(npc.seed)
		return Senses(npc)

	@property
	def resistances(npc):
		import AtlasPugna.Map_of_Resistances as resistances
		random.seed(npc.seed)
		result =  f"{resistances.Resistances(npc)} \n{resistances.ConditionImmunities(npc)}\n "
		result += f"\n<h4>Protections:</h4> {resistances.Protections(npc)} \n "
		return result

	@property
	def martial(npc):
		from AtlasPugna.Map_of_Martial_Abilities  import Skills
		random.seed(npc.seed)
		return Skills(npc)

	@property
	def background(npc):
		return npc.archetype

	@property
	def Type(npc):
		return npc.genus

	@property
	def genus(npc):
		"""
		Compute the NPC (alusor)'s genus as a set of tags

		Returns:
			string: A string of unique tags representing the genus.
			>> <"(gen)">.
		"""

		# Safely add attributes to the set if they are defined
		attributes = [
			npc.race,
			npc.subrace,
			npc.archetype,
			npc.gender,
			npc.alignment,
			]
		delimiter = " , " # Define a delimiter
		result = delimiter.join(attributes)
		#Inform(f"NPC Genus Tags: {result}")
		return result

	@property
	def proficiency_bonus(npc) -> int:
		""" Property mask to call proficiency bonus. """
		random.seed(npc.seed)
		return npc.ProficiencyBonus()

	def SetArmorClass(npc):
		random.seed(npc.seed)
		npc.AC = npc.SetAC()
		return npc.AC

	@property
	def to_hit_bonus(npc) -> int:
		""" Calculate the NPC's to-hit bonus. """
		# Assuming to hit is based on the higher of STR or DEX modifier
		random.seed(npc.seed)
		highest_ability_mod = Modifier(
			max(npc.ability_scores.STR,
				npc.ability_scores.DEX))
		if npc.archetype == "Druid":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.WIS))
		if npc.archetype == "Shaman":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.WIS))
		if npc.archetype == "Warlock":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.CHA))
		if npc.archetype == "Wizard":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.INT))

		return highest_ability_mod + npc.proficiency_bonus

	@property
	def attack_bonus(npc) -> int:
		""" Provide the NPC's attack bonus. """
		""" Masks <To Hit Bonus> """
		return npc.to_hit_bonus

	@property
	def magic_affinity(npc):
		return npc.magical

	@property
	def height(npc):
		return npc.size

	@property
	def spellcasting_ability(npc):
		random.seed(npc.seed)

		# Find the highest modifier among INT, WIS, and CHA
		int_mod = npc.ability_scores.int_mod
		wis_mod = npc.ability_scores.wis_mod
		cha_mod = npc.ability_scores.cha_mod

		# Create a dictionary to associate the ability score with its modifier
		ability_mod_dict = {'INT': int_mod, 'WIS': wis_mod, 'CHA': cha_mod}

		# Find the ability with the highest modifier
		return max(ability_mod_dict, key=ability_mod_dict.get)

	@property
	def spellcasting_ability_mod(npc):
		random.seed(npc.seed)
		# Find the highest modifier among INT, WIS, and CHA
		int_mod = npc.ability_scores.int_mod
		wis_mod = npc.ability_scores.wis_mod
		cha_mod = npc.ability_scores.cha_mod
		return max(int_mod,wis_mod,cha_mod)

	@property
	def spell_attack_bonus(npc):
		return npc.spellcasting_ability_mod + npc.proficiency_bonus

	@property
	def Set_spell_save_dc(npc):
		return 8 + npc.spell_attack_bonus

	@property
	def dc(npc):
		return npc.Set_spell_save_dc

	@property
	def ability_mod(npc):
		return getattr(npc.ability_scores, f"{npc.spellcasting_ability.lower()}_mod")

	@property
	def spell_save_dc(npc):
		return 8 + npc.ability_mod + npc.proficiency_bonus

	@property
	def armor_class(npc):
		return npc.AC

	@property
	def saving_throws(npc):
		return npc.ST

	@property
	def pb(npc):
		return npc.ProficiencyBonus()

	@property
	def PB(npc):
		return npc.ProficiencyBonus()

	def Magic(npc):
		import AtlasMagia.Map_of_Magic as magic
		random.seed(npc.seed)
		return magic.Magic(npc)

	def SetAbilityScores(npc, STR, DEX, CON, INT, WIS, CHA):
		random.seed(npc.seed)
		npc.AS = AbilityScores(STR, DEX, CON, INT, WIS, CHA)
		apply_creature_ability_modifiers(npc)
		npc.ST = SavingThrows(npc.AS, npc.proficiency_bonus)

	def SetMyStory(npc):
		random.seed(npc.seed)
		try:
			from AtlasEpica.Map_of_Stories import Story
			return Story(npc)
		except Exception:
			return ""

	def Check(npc, race=None, archetype=None, gender=None, alignment=None, subrace=None):
		"""
		Check if specific attributes match given values.
		Args:
			race (str, optional): Race tag to check.
			archetype (str, optional): Archetype (class) tag to check.
			gender (str, optional): Gender tag to check.
			alignment (str, optional): Alignment tag to check.
			subrace (str, optional): Subrace tag to check.
		Returns:
			bool: True if all provided parameters match NPC's attributes exactly.
		"""
		random.seed(npc.seed)
		checks = [
			(race, npc.race),
			(archetype, npc.archetype),
			(gender, npc.gender),
			(alignment, npc.alignment),
			(subrace, npc.subrace),
			]

		# Check each provided parameter
		for provided, actual in checks:
			if provided is not None and provided.strip().lower() != actual.strip().lower():
				return False
		return True

	def LightNPC_Hyperlink(npc):
		# Set the seed to ensure deterministic output
		random.seed(npc._seed)

		# Optional: Build genus or category if needed
		genus = f"{npc.race} {npc.archetype}"

		# Build the link
		url = f"/npc/{npc.race}/{npc.archetype}/{npc.level}/{npc._seed}"
		return f'<a href="{url}">{npc.name}, {npc.title}</a>'

	def __contains__(npc, text):
		if text in npc.genus: return True
		return False
