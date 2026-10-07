from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import (
	Feature,
	ApplyRandomFeats,
	ApplyEpicBoon
	)

class Rogue(Progression):
	HIT_DIE = 8

	# Helper: Sneak Attack dice by level (2024)
	@staticmethod
	def sneak_attack_dice(level: int) -> str:
		# 1d6 at 1, +1d6 every two levels
		n = 1 + ((level - 1) // 2)
		return f"{n}d6"

	def features(self, character):
		feats = []
		level = character.Level
		subclass = character.Subclass or choice(subclasses.get("Rogue", ["Thief"]))
		# === LEVEL 1 ===
		if level >= 1:
			# Sneak Attack
			feats.append(Feature(
				"Sneak Attack", 1,
				f"""Once per turn, you can deal an extra
				<b>{self.sneak_attack_dice(level)}</b>
				damage to one creature you hit with an attack
				if you have Advantage on the attack roll, or
				if any ally of yours is within 5 feet
				of the enemy.
				<br>
				You must be using Finesse or a Ranged weapon to
				activate a Sneak Attack. The extra damage's type
				is the same as the weapon's type.
				<br>
				An enemy with the <b>Incapacitated</b> condition
				automatically activates a Sneak Attack.
				<br>
				Disadvantage on the attack roll deactivates a
				Sneack Attack, independently of how many factors
				would activate it.
				"""
			))
			# Thieves’ Cant
			character.languages.Add({"Thieves' Cant"})
			character.languages.AddAnyLanguage()
			character.languages.AddAnyLanguage()
			feats.append(Feature(
				"Weapon Mastery", 1,
				"""
				Your training with weapons allows you to use the mastery properties of two kinds of weapons of your choice with which you have proficiency.
				"""
				))
		# === LEVEL 2 ===
		if level >= 2:
			roll_health(self.char)
			feats.append(Feature(
				"Cunning Action", 2,
				"""
				Your quick thinking and agility allow you to move and act quickly. On your turn, you can take one of the following actions as a <i>Bonus Action</i>:
				<ul style="list-style-type: '🗡️'; align:'left'">
					<li><b>Dash</b>: You gain extra movement for the current turn. The increase equals your Speed after applying any modifiers.
					<li><b>Disengage</b>: Your movement doesn't provoke <i>Opportunity Attacks</i> for the rest of the current turn.
					<li><b>Hide</b>. You try to conceal yourself. To do so, you must succeed on a DC 15 Dexterity (Stealth) check while you're Heavily Obscured or behind Three-Quarters Cover or Total Cover, and you must be out of any enemy's line of sight; if you can see a creature, you can discern whether it can see you. On a successful check, you have the Invisible condition. Make note of your check's total, which is the DC for a creature to find you with a Wisdom (Perception) check. You stop being hidden immediately after any of the following occurs: you make a sound louder than a whisper, an enemy finds you, you make an attack roll, or you cast a spell with a Verbal component.
					</ul>
				"""
				))
		# === LEVEL 3 ===
		if level >= 3:
			feats += [
				Feature("Steady Aim", 3,
					"""
					As a Bonus Action, you give yourself Advantage on your next attack roll on the current turn. You can use this feature only if you haven't moved during this turn, and after you use it, your Speed is 0 until the end of the current turn.					""")
					]
			if character.subclass == "Arcane Trickster":
				from AtlasMagia.Lodge_of_Spells import MageHand
				feats.append(Feature(
					"Arcane Trickster", 3,
					f"""
					Some Rogues enhance their fine-honed skills of stealth and
					agility with spells, learning magical tricks to aid them
					in their trade. Some Arcane Tricksters use their talents
					as pickpockets and burglars, while others are pranksters.
					"""
					))
				feats.append(Feature(
					"Mage Hand Legerdemain", 3,
					f"""
					You know the <i>Mage Hand</i> cantrip. <br>
					When you cast Mage Hand, you can cast it as a
					<i>Bonus Action</i>,
					 and you can make the spectral hand Invisible.
					 You can control the hand as a Bonus Action,
					 and through it, you can make
					 <i>Dexterity (Sleight of Hand)</i> checks.
					 <div class="spell">{MageHand}</div>
					"""
					))

			if character.subclass == "Assassin":
				feats.append(Feature(	"Assassin", 3,
					f"""
					An Assassin's training focuses on using stealth,
					poison, and disguise to eliminate foes with deadly
					efficiency. While some Rogues who follow this path
					are hired killers, spies, or bounty hunters, the
					capabilities of this subclass are equally useful
					for adventurers facing a variety of monstrous
					enemies.
					"""
					))
				feats.append(Feature("Assassinate", 3,
					f"""
					You're adept at ambushing a target, granting you the
					following benefits. <br>
					<b>Initiative.</b> You have Advantage on Initiative rolls.
					<b>Surprising Strikes.</b> During the first round of each
					combat, you have Advantage on attack rolls against any
					creature that hasn't taken a turn. If your Sneak Attack
					hits any target during that round, the target takes extra
					damage of the weapon's type equal to your Rogue level.
					"""
					))
				# Assassin's Tools (proficiency and the two kits) is granted by the
				# Training Tag in AtlasOfTraining/Map_of_Rogue_Training.py.

			if character.subclass == "Thief":
				feats.append(Feature(	"Thief", 3,
					f"""
					A mix of burglar, treasure hunter, and explorer, you are
					the epitome of an adventurer. In addition to improving
					your agility and stealth, you gain abilities useful for
					delving into ruins and getting maximum benefit from
					the magic items you find there.
					"""))
				feats.append(Feature(	"Fast Hands", 3,
					f"""
					As a Bonus Action, you can do one of the following.
					<ul style="list-style-type: '🫳'; align:'left'">
						<li> <b>Sleight of Hand.</b> Make a Dexterity (Sleight of Hand) check to pick a lock or disarm a trap with Thieves' Tools or to pick a pocket.
						<li> <b>Use an Object.</b> Take the Utilize action, or take the Magic action to use a magic item that requires that action.
						</ul>
					"""))
				feats.append(Feature(	"Second-Story Work", 3,
					f"""
					You've trained to get into especially hard-to-reach places, granting you these benefits.
					<ul style="list-style-type: '🫳'; align:'left'">
						<li> <b>Climber.</b> You gain a Climb Speed equal to your Speed.
						<li> <b>Jumper.</b> You can determine your jump distance using your Dexterity rather than your Strength.
						</ul>
					"""))
		# === LEVEL 4 ===
		if level >= 4:
			feats += ApplyRandomFeats(character, n=1, level=4)
		# === LEVEL 5 ===
		if level >= 5:
			feats.append(Feature("Cunning Strike", 5,
				"""
You've developed cunning ways to use your Sneak Attack. When you deal Sneak Attack damage, you can add one of the following Cunning Strike effects. Each effect has a die cost, which is the number of Sneak Attack damage dice you must forgo to add the effect. You remove the die before rolling, and the effect occurs immediately after the attack's damage is dealt. For example, if you add the Poison effect, remove 1d6 from the Sneak Attack's damage before rolling.
<br>
If a Cunning Strike effect requires a saving throw, the DC equals 8 plus your Dexterity modifier and Proficiency Bonus.
<br>
Poison (Cost: 1d6). You add a toxin to your strike, forcing the target to make a Constitution saving throw. On a failed save, the target has the Poisoned condition for 1 minute. At the end of each of its turns, the Poisoned target repeats the save, ending the effect on itself on a success.
<br>
To use this effect, you must have a Poisoner's Kit on your person.
<br>
Trip (Cost: 1d6). If the target is Large or smaller, it must succeed on a Dexterity saving throw or have the Prone condition.
<br>
Withdraw (Cost: 1d6). Immediately after the attack, you move up to half your Speed without provoking Opportunity Attacks.
				"""
				))
			feats.append(Feature("Uncanny Dodge", 5,
				"""
When an attacker that you can see hits you with an attack roll, you can take a Reaction to halve the attack's damage against you (round down).
				"""
				))
		# === LEVEL 6 ===
		if level >= 6:
			pass
		# === LEVEL 7 ===
		if level >= 7:
			feats.append(Feature( "Reliable Talent", 7,
				"""
Whenever you make an ability check that uses one of
your skill or tool proficiencies, you can treat a
d20 roll of 9 or lower as a 10.
				"""
			))
			feats.append(Feature("Evasion", 7,
				"""
You can nimbly dodge out of the way of certain
dangers. When you're subjected to an effect that
allows you to make a Dexterity saving throw to
take only half damage, you instead take no damage
if you succeed on the saving throw and only half
damage if you fail. You can't use this feature
if you have the Incapacitated condition.
				"""
				))
		# === LEVEL 8 ===
		if level >= 8:
			feats += ApplyRandomFeats(character, n=1, level=8)
		# === LEVEL 9 ===
		if level >= 9:

			if character.subclass == "Arcane Trickster":
				from AtlasMagia.Lodge_of_Spells import MageHand
				feats.append(Feature(
					"Magical Ambush", 3,
					f"""
If you have the Invisible condition when you cast a spell on a creature, it has Disadvantage on any saving throw it makes against the spell on the same turn.
					"""
					))

			if character.subclass == "Assassin":
				feats.append(Feature(	"Infiltration Expertise", 3,
					f"""
You are expert at the following techniques that aid your infiltrations.
<br>
<b>Masterful Mimicry.</b> You can unerringly mimic another person's speech,
handwriting, or both if you have spent at least 1 hour studying them.
<br>
<b>Roving Aim.</b> Your Speed isn't reduced to 0 by using Steady Aim.
					"""
					))

			if character.subclass == "Thief":
				feats.append(Feature(	"Supreme Sneak", 3,
					f"""
You gain the following Cunning Strike option. <br>
<b>Stealth Attack (Cost: 1d6).</b> If you have the Hide action's Invisible condition, this attack doesn't end that condition on you if you end the turn behind Three-Quarters Cover or Total Cover.
					"""))
		# === LEVEL 10 ===
		if level >= 10:
			feats += ApplyRandomFeats(character, n=1, level=10)
		# === LEVEL 11 ===
		if level >= 11:
			feats.append(Feature(
				"Improved Cunning Strike", 10,
				"""
You can use up to two Cunning Strike effects when you deal Sneak Attack damage, paying the die cost for each effect.
				"""
			))

			feats.append(Feature(
				"Reliable Sneak", 11,
				"Once per turn, you can reroll the damage dice for Sneak Attack and use either total."
			))
		# === LEVEL 12 ===
		if level >= 12:
			feats += ApplyRandomFeats(character, n=1, level=12)
		# === LEVEL 13 ===
		if level >= 13:

			if character.subclass == "Arcane Trickster":

				feats.append(Feature("Versatile Trickster", 3,
					f"""
					You gain the ability to distract targets with your Mage Hand.
					When you use the Trip option of your Cunning Strike on a
					creature, you can also use that option on another creature
					within 5 feet of the spectral hand.
					"""
					))

			if character.subclass == "Assassin":
				feats.append(Feature(	"Envenom Weapons", 3,
					f"""
					When you use the Poison option of your Cunning Strike,
					the target also takes 2d6 Poison damage whenever it fails
					the saving throw. This damage ignores Resistance to Poison
					damage.
					"""
					))

			if character.subclass == "Thief":
				feats.append(Feature( "Use Magic Device", 3,
					f"""
You've learned how to maximize use of magic items, granting you the following benefits.
<ul style="list-style-type: '🎩'; align:'left'">
	<li><b>Attunement.</b> You can attune to up to four magic items at once.
	<li><b>Charges.</b> Whenever you use a magic item property that expends charges, roll 1d6. On a roll of 6, you use the property without expending the charges.
	<li><b>Scrolls.</b>  You can use any Spell Scroll, using Intelligence as your spellcasting ability for the spell. If the spell is a cantrip or a level 1 spell, you can cast it reliably. If the scroll contains a higher-level spell, you must first succeed on an Intelligence (Arcana) check (DC 10 plus the spell's level). On a successful check, you cast the spell from the scroll. On a failed check, the scroll disintegrates.
	</ul>
					"""))
		# === LEVEL 14 ===
		if level >= 14:
			feats.append(Feature("Devious Strikes", 14,
				"""
				You've practiced new ways to use your Sneak Attack deviously. The following effects are now among your Cunning Strike options.
				<ul style="list-style-type: '🗡️'; align:'left'">

					<li><b>Daze</b> (Cost: 2d6). The target must succeed on a Constitution saving throw, or on its next turn, it can do only one of the following: move or take an action or a Bonus Action.

					<li><b>Knock Out</b> (Cost: 6d6). The target must succeed on a Constitution saving throw, or it has the Unconscious condition for 1 minute or until it takes any damage. The Unconscious target repeats the save at the end of each of its turns, ending the effect on itself on a success.

					<li><b>Obscure</b> (Cost: 3d6). The target must succeed on a Dexterity saving throw, or it has the Blinded condition until the end of its next turn.
					</ul>
				"""
				))
		# === LEVEL 15 ===
		if level >= 15:
			feats.append(Feature(
				"Slippery Mind", 15,
				"""
Your cunning mind is exceptionally difficult to control. You gain proficiency in Wisdom and Charisma saving throws.
				"""
			))
		# === LEVEL 16 ===
		if level >= 16:
			feats += ApplyRandomFeats(character, n=1, level=16)
		# === LEVEL 17 ===
		if level >= 17:
			if character.subclass == "Arcane Trickster":

				feats.append(Feature("Spell Thief", 3,
					f"""
You gain the ability to magically steal the knowledge of how to cast a spell from another spellcaster.
<br>
Immediately after a creature casts a spell that targets you or includes you in its area of effect, you can take a Reaction to force the creature to make an Intelligence saving throw.
The DC equals your spell save DC.
On a failed save, you negate the spell's effect against you, and you steal the knowledge of the spell if it is at least level 1 and of a level you can cast (it doesn't need to be a Wizard spell).
For the next 8 hours, you have the spell prepared. The creature can't cast it until the 8 hours have passed.
<br>
Once you steal a spell with this feature, you can't use this feature again until you finish a Long Rest.

					"""
					))

			if character.subclass == "Assassin":
				feats.append(Feature(	"Death Strike", 3,
					f"""
When you hit with your Sneak Attack on the first round of a combat, the target must succeed on a Constitution saving throw (DC 8 plus your Dexterity modifier and Proficiency Bonus), or the attack's damage is doubled against the target.
					"""
					))

			if character.subclass == "Thief":
				feats.append(Feature( "Thief's Reflexes", 3,
					f"""
You are adept at laying ambushes and quickly escaping danger. You can take two turns during the first round of any combat. You take your first turn at your normal Initiative and your second turn at your Initiative minus 10.
					"""))
		# === LEVEL 18 ===
		if level >= 18:
			feats.append(Feature( "Elusive", 18,
				"""
You're so evasive that attackers rarely gain the upper hand against you.
No attack roll can have Advantage against you unless you have the Incapacitated condition.
				"""
			))
		# === LEVEL 19 ===
		if level >= 19:
			feats += ApplyEpicBoon(character, n=1)
		# === LEVEL 20 ===
		if level >= 20:
			feats.append(Feature(
				"Stroke of Luck", 20,
				"""
You have a marvelous knack for succeeding when you need to. If you fail a D20 Test, you can turn the roll into a 20.

Once you use this feature, you can't use it again until you finish a Short or Long Rest.
				"""
			))
		# Always update Sneak Attack dice at current level
		for i, feat in enumerate(feats):
			if feat.name == "Sneak Attack":
				feat.description = f"Once per turn, you can deal an extra <b>{self.sneak_attack_dice(level)}</b> damage to one creature you hit with an attack if you have Advantage on the attack roll, or if another enemy of the target is within 5 feet of it."
		return feats
