

'''...༼Cartography of the Map of Attacks༽...'''
import app.random as random
try:
	from AtlasActorLudi.Map_of_Scores import PB as ProficiencyBonus
	from AtlasActorLudi.Map_of_Conditions import Condition, SavingThrow, Recovery
	from AtlasAlusoris.Grimoire_of_NPC import NPC
	from AtlasLudus.Map_of_Dice import Dice
	from AtlasLudus.Compass_of_Damages import DamageType, MagicDamageType
	from AtlasLudus.Map_of_Useful_Functions import select1
	from AtlasInventarium.Grimoire_of_Weapons import Weapon
	from AtlasInventarium.Lodge_of_Basic_Weapons import Lodge as lg
	from AtlasScriptum.Map_of_Formats import Entry_Text
except ImportError:
	raise

from Minion import guardian, watcher, warden, spy, minion

@guardian
def Attack(npc):
	weapon = NewWeapon(npc)
	return str(weapon)


def PossibleWeapons(npc):
		possible_weapons = []
		MartialMeleeWeapons = []
		MartialRangedWeapons = []
		SimpleMeleeWeapons = []
		SimpleRangedWeapons = []
		PrimalWeapons = []
		Type= npc.Type
		PB = ProficiencyBonus(npc.proficiency_bonus)
		STR = npc.ability_scores.str_mod
		DEX = npc.ability_scores.dex_mod
		CON = npc.ability_scores.con_mod
		MAG = max(
			npc.ability_scores.cha_mod,
			npc.ability_scores.wis_mod,
			npc.ability_scores.int_mod)
		title = npc.title
		Lodge = lg(npc)
		# Races
		if "Aberration" in Type:
			Lodge.Bite.damage_dice = select1(['d4','d4','d4','d4','d6','d6','d8'])
			Lodge.Tentacle.damage_dice = select1(['d4','d4','d4','d4','d6','d6','d8'])
			Lodge.Bite.properties += select1([
				'',
				f'''<br><b>Infectious:</b> The bite makes an aditional 1{
				 	select1(
						['d4','d6','d8'],
						[4,2,1]
						)
					} of Acid Damage.''',
				],[8,1])
			possible_weapons += [
				Lodge.Tail,
				Lodge.Bite,
				Lodge.Tentacle,
				Lodge.Tentacle,
				]
		if "Aven" 		in Type:
			possible_weapons += [
				Lodge.Claws,
				Lodge.Bite,
				Lodge.Net,
				Lodge.Trident,
				Lodge.Sling,
				Lodge.Dart,
				Lodge.Spear,
				Lodge.Javelin,
				Lodge.Dagger,
				]
		if "Beast" 		in Type:
			Lodge.Bite.damage_dice = random.choice(['d6','d6','d8'])
			Lodge.Tail.damage_dice = random.choice(['d6','d6','d8'])

			possible_weapons += [
				Lodge.Tail,
				Lodge.Bite,
				Lodge.Claws,
				Lodge.Slam,
				]
		if "Beastfolk" 	in Type:
			possible_weapons += [
				Lodge.Fists,
				Lodge.Knuckles,
				Lodge.Club,
				Lodge.GreatClub,
				Lodge.Javelin,
				Lodge.Mace,
				Lodge.Quarterstaff,
				Lodge.Slam,
				Lodge.Spear,
				Lodge.Dart,
				Lodge.Sling,
				Lodge.Rock,
				Lodge.Whip,
				Lodge.Trident,
				]
		if "Catfolk" 	in Type:
			possible_weapons += [
				Lodge.Dagger,
				Lodge.Claws,
				Lodge.Handaxe,
				Lodge.Dart,
				Lodge.Scimitar,
				Lodge.Whip,
				Lodge.Bite,

				]
		if "Celestial"	in Type:
			possible_weapons += [
				Lodge.Club,
				Lodge.GreatClub,
				Lodge.Javelin,
				Lodge.LightHammer,
				Lodge.Mace,
				Lodge.Quarterstaff,
				Lodge.Spear,
				Lodge.Shortbow,
				]
		if "Construct"	in Type:
			possible_weapons = [
				Lodge.Firebolt,
				Lodge.Knuckles,
				Lodge.Club,
				Lodge.Javelin,
				Lodge.LightHammer,
				Lodge.Mace,
				Lodge.Slam,
				Lodge.LightCrossbow,
				Lodge.Dart,
				Lodge.Maul,
				]
		if "Dragon" 	in Type:
			Lodge.Bite.damage_dice = random.choice(['d6','d6','d8'])
			Lodge.Claws.damage_dice = random.choice(['d6','d6','d8'])
			Lodge.Tail.damage_dice = random.choice(['d6','d6','d8'])
			possible_weapons += [
				Lodge.Tail,
				Lodge.Tail,
				Lodge.Bite,
				Lodge.Claws,
				Lodge.Firebolt,
				Lodge.Breath,
				Lodge.Breath,
				Lodge.Breath,
				Lodge.Breath,
				Lodge.Breath,
				Lodge.Slam,
				]

			MartialRangedWeapons = [
				Lodge.Firebolt,
				]
		if "Dwarf"		in Type:
			possible_weapons += SimpleMeleeWeapons
			possible_weapons += [
				Lodge.Rock,
				Lodge.ThrowingAxe,
				Lodge.FlintlockPistol,
				Lodge.Musket,
				Lodge.Blunderbuss,
				Lodge.Warhammer,
				Lodge.WarPick,
				]
			possible_weapons += MartialMeleeWeapons
		if "Elemental" 	in Type:
			possible_weapons += SimpleRangedWeapons
			possible_weapons += SimpleMeleeWeapons
			possible_weapons += [
				Lodge.Trident,
				Lodge.Scimitar,
				Lodge.Whip,
				]
		if "Elf"		in Type:
			possible_weapons += [
				Lodge.Dagger,
				Lodge.Quarterstaff,
				Lodge.Spear,
				Lodge.Scimitar,
				Lodge.Longbow,
				]
			possible_weapons += SimpleRangedWeapons
		if "Fey"		in Type:
			possible_weapons += [
				Lodge.Firebolt,
				Lodge.Bite,
				Lodge.Blowgun,
				Lodge.Lance,
				Lodge.Whip,
				]
			possible_weapons += SimpleRangedWeapons + SimpleMeleeWeapons
		if "Fiend"		in Type:
			Lodge.Tail.damage_dice = select1([ 'd6','d6','d8'])
			Lodge.Bite.damage_dice = select1([ 'd6','d6','d8'])
			Lodge.Morningstar.properties += select1([
				'',
				f'''<br><b>Hellfire:</b> The weapon makes an aditional 1d{
					select1(
						['d4', 'd6', 'd8'],
						[4,2,1])} of Fire Damage''',
				],[8,1])
			Lodge.Maul.properties += select1([
				'',
				f'''<br><b>Hellfire:</b> The weapon makes an aditional 1d{
					select1(
						['d4', 'd6', 'd8'],
						[4,2,1])} of Fire Damage''',
				],[8,1])
			Lodge.Flail.properties += select1([
				'',
				f'''<br><b>Hellfire:</b> The weapon makes an aditional 1d{
					select1(
						['d4', 'd6', 'd8'],
						[4,2,1])} of Fire Damage''',
				],[8,1])
			Lodge.Trident.properties += select1([
				'',
				f'''<br><b>Hellfire:</b> The weapon makes an aditional 1d{
					select1(
						['d4', 'd6', 'd8'],
						[4,2,1])} of Fire Damage''',
				],[8,1])
			Lodge.Whip.properties += select1([
				'',
				f'''<br><b>Hellfire:</b> The weapon makes an aditional 1d{
					select1(
						['d4', 'd6', 'd8'],
						[4,2,1])} of Fire Damage''',
				],[8,1])

			possible_weapons += [
				Lodge.Knuckles,
				Lodge.Handaxe,
				Lodge.Mace,
				Lodge.Sickle,
				Lodge.Spear,
				Lodge.Nunchaku,
				Lodge.Shortbow,
				Lodge.Sling,
				Lodge.Flail,
				Lodge.Maul,
				Lodge.Morningstar,
				Lodge.Pike,
				Lodge.Rapier,
				Lodge.Trident,
				Lodge.Whip,
				Lodge.Net,
				Lodge.Tail,
				Lodge.Bite,
				Lodge.Claws,
				Lodge.Firebolt,
				]
		if "Giant"		in Type:
			Lodge.Fists.damage_dice = 'd6'
			Lodge.Club.damage_dice = 'd6'
			Lodge.LightHammer.damage_dice = 'd6'
			Lodge.Mace.damage_dice = 'd8'
			Lodge.Rock.damage_dice = 'd6'
			possible_weapons += [
				Lodge.Fists,
				Lodge.Club,
				Lodge.GreatClub,
				Lodge.Handaxe,
				Lodge.LightHammer,
				Lodge.Knuckles,
				Lodge.Mace,
				Lodge.Slam,
				Lodge.Rock,
				Lodge.LightHammer,
				Lodge.Mace,
				Lodge.Sling,
				Lodge.Greataxe,
				Lodge.Greatsword,
				Lodge.Maul,
				Lodge.Morningstar,
				Lodge.Warhammer,
				Lodge.ThrowingAxe,
				]
		if "Gnome"		in Type:
			possible_weapons += [
				Lodge.Firebolt,
				Lodge.FlintlockPistol,
				Lodge.HandCrossbow,
				Lodge.Sling,
				Lodge.Dart,
				Lodge.Dagger,
				Lodge.Club,
				]
		if "Goblin"		in Type:
			possible_weapons += [
				Lodge.Knuckles,
				Lodge.Club,
				Lodge.Dagger,
				Lodge.Spear,
				Lodge.LightCrossbow,
				Lodge.Dart,
				Lodge.HandCrossbow,
				Lodge.HeavyCrossbow,
				Lodge.FlintlockPistol,
				]
		if "Halfling"	in Type:
			possible_weapons += [
				Lodge.Knuckles,
				Lodge.Club,
				Lodge.Mace,
				Lodge.Sickle,
				Lodge.Shortbow,
				Lodge.LightCrossbow,
				Lodge.Sling,
				Lodge.Rock,
				Lodge.Halberd,
				Lodge.Musket,
				]
		if "Human"		in Type:
			possible_weapons += SimpleMeleeWeapons
			possible_weapons += [
				Lodge.LightCrossbow,
				Lodge.Shortbow,
				Lodge.Greatsword,
				]
		if "Kobold"		in Type:
			possible_weapons += PrimalWeapons
			possible_weapons += [
				Lodge.Firebolt,
				Lodge.Breath,
				Lodge.Net,
				Lodge.Blowgun,
				Lodge.Pike,
				Lodge.Dart,
				Lodge.LightCrossbow,
				Lodge.GreatClub,
				Lodge.Javelin,
				Lodge.Spear,
				Lodge.Sling,
				Lodge.Tail,
				Lodge.Bite,
				Lodge.Claws,
				Lodge.Firebolt,
				]
		if "Lizardfolk"	in Type:
			Lodge.Bite.damage_dice = random.choice(['d4','d4', 'd6','d6','d8'])
			Lodge.Claws.damage_dice = random.choice(['d4','d4', 'd6','d6','d8'])

			possible_weapons += [
				Lodge.Club,
				Lodge.GreatClub,
				Lodge.Javelin,
				Lodge.Quarterstaff,
				Lodge.Spear,
				Lodge.Nunchaku,
				Lodge.Dart,
				Lodge.Shortbow,
				Lodge.Sling,
				Lodge.Rock,
				Lodge.LightCrossbow,
				Lodge.Dart,
				Lodge.Shortbow,
				Lodge.Scimitar,
				Lodge.Pike,
				Lodge.Trident,
				Lodge.WarPick,
				]
		if "Monstrosity" in Type:
			Lodge.Tail.damage_dice = select1([ 'd4','d6','d8'], [4,2,1])
			Lodge.Bite.damage_dice = select1([ 'd4','d6','d8'], [4,2,1])
			Lodge.Claws.damage_dice = select1([ 'd4','d6','d8'], [4,2,1])
			possible_weapons += [
				Lodge.Tail,
				Lodge.Bite,
				Lodge.Claws,
				Lodge.Firebolt,
				]
		if "Ooze"		in Type:
			possible_weapons += [
				Lodge.Slam,
				Lodge.Dart,
				Lodge.Sling,
				Lodge.Tentacle,
				]
		if "Orc"		in Type:
			possible_weapons += SimpleMeleeWeapons
			possible_weapons += [
				Lodge.Fists,
				Lodge.Knuckles,
				Lodge.ThrowingAxe,
				Lodge.Blunderbuss,
				Lodge.Sling,
				Lodge.Battleaxe,
				]
		if "Plant"		in Type:
			possible_weapons += [
				Lodge.Claws,
				Lodge.Net,
				Lodge.Whip,
				Lodge.Rock,
				Lodge.Sling,
				Lodge.Shortbow,
				Lodge.Dart,
				Lodge.Quarterstaff,
				Lodge.Mace,
				Lodge.Club,
				Lodge.GreatClub,
				]
		if "Snakefolk"	in Type:
			Lodge.Bite.properties += select1([
					'',
					f'''<b>Venomous:</b> The bite makes an aditional {
						select1(['d4', 'd6','d8'],[4,2,1])
						} of Poison Damage.'''
					],[8,1])
			Lodge.Bite.damage_dice = select1(['d4','d6','d8'],[4,2,1])
			Lodge.Tail.damage_dice = select1(['d4','d6','d8'],[4,2,1])
			possible_weapons += PrimalWeapons
			possible_weapons += [
				Lodge.Longbow,
				Lodge.Whip,
				Lodge.Trident,
				Lodge.Scimitar,
				Lodge.Rapier,
				Lodge.Flail,
				Lodge.Shortbow,
				Lodge.Dart,
				Lodge.Spear,
				Lodge.Sickle,
				Lodge.Javelin,
				Lodge.Dagger,
				Lodge.Tail,
				Lodge.Bite,
				]
		if "Undead"		in Type:
			Lodge.Bite.properties += select1([
					'',
					f'''<b>Corruption:</b> The bite makes an aditional {
						select1(['d4','d6','d8'],[4,2,1])
						} of Necrotic Damage.''',
					],[8,1])
			possible_weapons += [
				Lodge.Fists,
				Lodge.Dagger,
				Lodge.Club,
				Lodge.Slam,
				Lodge.Spear,
				Lodge.Rock,
				Lodge.Flail,
				Lodge.Pike,
				Lodge.Sickle,
				]
			Lodge.Bite.damage_dice = select1(['d4','d6','d8'],[4,2,1])
			Lodge.Bite.attack_modifier= CON
			Lodge.Bite.damage_type = select1(['Piercing','Necrotic'])
			if Dice()==1:
				Lodge.Bite.properties += f"The target's hit point maximum is reduced by an amount equal to the damage taken, and the undead regains hit points equal to that amount. The reduction lasts until the target finishes a long rest. The target dies if this effect reduces its hit point maximum to 0."
				if Dice()==1:
					Lodge.Bite.properties += f"A humanoid slain by this attack rises 24 hours later as a zombie under {title}'s control, unless the humanoid is restored to life or its body is destroyed. {title} can have no more than {npc.proficiency_bonus+CON}  zombies under its control at one time."

			if Dice()==1:
				Lodge.Bite.properties += f"The target must succeed on a DC {8+npc.proficiency_bonus+CON} Constitution saving throw or its hit point maximum is reduced by an amount equal to the damage taken. This reduction lasts until the target finishes a long rest. The target dies if this effect reduces its hit point maximum to 0."
				if Dice()==1:
					Lodge.Bite.properties += f"A humanoid slain by this attack rises 24 hours later as a zombie under {title}'s control, unless the humanoid is restored to life or its body is destroyed. {title} can have no more than {npc.proficiency_bonus+CON}  zombies under its control at one time."
			possible_weapons += [
				Lodge.LifeDrain,
				Lodge.Bite]
		if "Vampire"		in Type:
			Lodge.Bite.properties += select1([
					'',
					f'''<b>Corruption:</b> The bite makes an aditional {
						select1(['d6','d8','d10'],[4,2,1])
						} of Necrotic Damage.''',
					],[8,1])
			possible_weapons += [
				Lodge.Fists,
				Lodge.Dagger,
				Lodge.Club,
				Lodge.Slam,
				Lodge.Spear,
				Lodge.Rock,
				Lodge.Flail,
				Lodge.Pike,
				Lodge.Sickle,
				]
			Lodge.Bite.damage_dice = select1(['d4','d6','d8'],[4,2,1])
			Lodge.Bite.attack_modifier= CON
			Lodge.Bite.damage_type = select1(['Piercing','Necrotic'])
			if Dice()==1:
				Lodge.Bite.properties += f"The target's hit point maximum is reduced by an amount equal to the damage taken, and the undead regains hit points equal to that amount. The reduction lasts until the target finishes a long rest. The target dies if this effect reduces its hit point maximum to 0."
				if Dice()==1:
					Lodge.Bite.properties += f"A humanoid slain by this attack rises 24 hours later as a zombie under {title}'s control, unless the humanoid is restored to life or its body is destroyed. {title} can have no more than {npc.proficiency_bonus+CON}  zombies under its control at one time."

			if Dice()==1:
				Lodge.Bite.properties += f"The target must succeed on a DC {8+npc.proficiency_bonus+CON} Constitution saving throw or its hit point maximum is reduced by an amount equal to the damage taken. This reduction lasts until the target finishes a long rest. The target dies if this effect reduces its hit point maximum to 0."
				if Dice()==1:
					Lodge.Bite.properties += f"A humanoid slain by this attack rises 24 hours later as a zombie under {title}'s control, unless the humanoid is restored to life or its body is destroyed. {title} can have no more than {npc.proficiency_bonus+CON}  zombies under its control at one time."
			possible_weapons += [
				Lodge.LifeDrain,
				Lodge.Bite]

		# subrace
		if "Gith" 		in Type:
			possible_weapons += SimpleMeleeWeapons + SimpleRangedWeapons

		# Backgrounds
		if "Bandit" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Barbarian" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Berserker" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Cleric" in Type:
			possible_weapons += MartialMeleeWeapons
		if "Criminal" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Guard" in Type:
			ShieldBash = Weapon("Shield Bash",Dice(PB),'d4',STR,'Bludgeoning','reach',f"If the target is a {npc.size} or smaller creature, it must succeed on a DC { 8 + npc.pb + STR} Strength saving throw or be knocked prone.")
			MartialMeleeWeapons += [ShieldBash]
			possible_weapons += MartialMeleeWeapons
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Hero" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Hunter" in Type:
			possible_weapons += MartialRangedWeapons
		if "Knight" in Type:
			possible_weapons += MartialMeleeWeapons
		if "Monk" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Noble" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Pirate" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Ranger" in Type:
			possible_weapons += MartialRangedWeapons
		if "Soldier" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Rogue" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Spy" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons
		if "Warrior" in Type:
			possible_weapons += MartialMeleeWeapons + MartialRangedWeapons

		#possible_weapons += SimpleMeleeWeapons + SimpleRangedWeapons

		return possible_weapons

def NewWeapon(npc):

	weapon = random.choice(PossibleWeapons(npc))

	if not weapon:
		weapon = lg(npc).Bite
			# Default weapon

	weapon.damage_intensity = Dice(npc.pb-1)

	return weapon

def Damage():
	return random.choice(list(DamageType))

def MagicDamage():
	return random.choice(list(MagicDamageType))

def SpecialAttack(npc=None):
	if not npc:
		from AtlasAlusoris.Grimoire_of_NPC import NPC
		npc1 = NPC()
	else:
		npc1 = npc
	return SpecialWeapon(npc1)

def SpecialWeapon( npc = None):
	from AtlasInventarium.Compass_of_Recharging import RechargeTime
	if not npc:
		from AtlasAlusoris.Grimoire_of_NPC import NPC
		npc = NPC()
	Lvl = npc.level
	Mod = Dice(npc.pb) + random.choice([
			npc.ability_scores.str_mod,
			npc.ability_scores.dex_mod,
			npc.ability_scores.con_mod,
			npc.ability_scores.int_mod,
			npc.ability_scores.wis_mod,
			npc.ability_scores.cha_mod])

	STR=npc.ability_scores.str_mod
	DEX=npc.ability_scores.dex_mod

	recharges_at = random.choice(list(RechargeTime))
	charges = Dice(npc.pb)
	s = '' if charges<2 else 's'

	description = f"<h4>Special Attack:</h4> {charges} charge{s} per day. Recharges {recharges_at}. \n\t"

	# Basic attack description
	w = NewWeapon(npc)
	dmg = MagicDamage()
	w.name = f"{dmg} {w.name}"
	w.damage_intensity += 1
	w.damage_type = str(dmg)


	# Potential condition application
	if Dice(10)+Dice(10) <= Dice(Lvl):
		condition = Condition(dmg.value)
		saving_throw = SavingThrow(condition)
		w.properties +=	 f" On a hit the target is affected by the {condition.value} condition."
		w.properties += f" The Condition may be countered with a succesful DC {(10 + Mod )}{saving_throw} Saving Throw at the beggining of the target's turn."
	description += str(w)
	return description
