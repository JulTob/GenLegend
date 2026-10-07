from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import (
	Feature,	ApplyRandomFeats,	ApplyEpicBoon,	PrimalChampionFeat)

import random

class Barbarian(Progression):
	# --- Per‑level number helpers -----------------------------------------
	def RageUses(self, lvl: int) -> int:
		table = {
			1: 2,  2: 2,  3: 3,  4: 3,  5: 3,
			6: 4,  7: 4,  8: 4,  9: 4, 10: 4,
			11: 4, 12: 5, 13: 5, 14: 5, 15: 5,
			16: 5, 17: 6, 18: 6, 19: 6, 20: 6,
			}
		lvl = max(1, min(lvl, 20))
		return table[lvl]

	def RageBonus(self, lvl: int) -> int:
		table = {
			1: 2,  2: 2,  3: 2,  4: 2,  5: 2,
			6: 2,  7: 2,  8: 2,  9: 3, 10: 3,
			11: 3, 12: 3, 13: 3, 14: 3, 15: 3,
			16: 4, 17: 4, 18: 4, 19: 4, 20: 4,
			}
		lvl = max(1, min(lvl, 20))
		return table[lvl]

	def WeaponMasteryNumber(self, lvl: int) -> int:
		table = {
			1: 2,  2: 2,  3: 2,  4: 3,  5: 3,
			6: 3,  7: 3,  8: 3,  9: 3, 10: 4,
			11: 4, 12: 4, 13: 4, 14: 4, 15: 4,
			16: 4, 17: 4, 18: 4, 19: 4, 20: 4,
			}
		lvl = max(1, min(lvl, 20))
		return table[lvl]

	def features(self, character=None):
		from AtlasActorLudi.Map_of_Scores import Modifier
		from AtlasLusoris.Grimoire_of_Features import UnarmoredDefense
		if character is None:
			character = self.char
		else:
			self.char = character
		features: list[Feature] = []
		feats:     list[Feature] = []
			# for random ASI feats, etc.

		level = self.char.Level  # or .level
		lvl = level
		subclass = self.char.Subclass or "Berserker"
		rage_uses = self.RageUses(level)
		rage_bonus = self.RageBonus(level)
		WeaponMasteries = self.WeaponMasteryNumber(level)


		if level >= 1:
			feats.append(Feature("Rage", (
				f"""You can imbue yourself with a primal power called <b>Rage</b>, a force that grants you extraordinary might and resilience.
					You can enter it as a <i>Bonus Action</i> if you aren't wearing Heavy armor.
					<br> You can enter your Rage {rage_uses} times.
					You regain one expended use when you finish a <i>Short Rest</i>,
					and you regain all expended uses when you finish a <i>Long Rest</i>.
					<br> While active, your Rage follows the Raging Rules."""
					)))
			feats.append(Feature("Raging: Damage Resistance", (
					f"While Raging, You have <i>Resistance to</i> <b>Bludgeoning, Piercing, and Slashing damage</b>."
					)))
			feats.append(Feature("Raging: Rage Damage", (
					f"""While Raging, When you make an attack using <b>Strength</b>
					—with either a weapon or an Unarmed Strike—
					and deal damage to the target,
					you gain a bonus to the damage: {rage_bonus}."""
					)))
			feats.append(Feature("Raging: Strength Advantage", (
					f"""While Raging, You have Advantage on Strength checks and Strength saving throws."""
					)))
			feats.append(Feature("Raging: No Concentration or Spells", (
					f"""While Raging, You can't maintain Concentration, and you can't cast spells."""
					)))
			feats.append(Feature("Raging: Duration", (
					f"""The Rage lasts until the end of your next turn, and it ends early if you don Heavy armor or have the Incapacitated condition.
					If your Rage is still active on your next turn, you can extend the Rage for another round by doing one of the following:
					<ul>
						<li>Make an attack roll against an enemy.</li>
						<li>Force an enemy to make a saving throw.</li>
      					<li>Take damage before the end of your next turn.</li>
						<li>Take a Bonus Action to extend your Rage.</li>
						</ul>
					Each time the Rage is extended, it lasts until the end of your next turn.
					You can maintain a Rage for up to 10 minutes."""
					)))

			feats.append(UnarmoredDefense("CON", "Barbarian"))

			feats.append(Feature("Weapon Mastery", (
					f"""Your training with weapons allows you to use
					the mastery properties of {WeaponMasteries} kinds
					of Simple or Martial Melee weapons of your choice,
					such as Greataxes and Handaxes.
					Whenever you finish a Long Rest, you can practice weapon
					drills and change one of those weapon choices."""
					)))
		# ---------------- Level 2 ----------------
		if lvl >= 2:
			roll_health(self.char)
			feats.extend([
				Feature("Danger Sense", "You gain an uncanny sense of when things aren't as they should be, giving you an edge when you dodge perils. You have Advantage on Dexterity saving throws unless you have the Incapacitated condition."),
				Feature("Reckless Attack", "You can throw aside all concern for defense to attack with increased ferocity. When you make your first attack roll on your turn, you can decide to attack recklessly. Doing so gives you Advantage on attack rolls using Strength until the start of your next turn, but attack rolls against you have Advantage during that time."),
				])
		# ---------------- Level 3 ----------------
		if lvl >= 3:
			# The extra ability is set in the character creation set_Skills()
			feats.extend([Feature("Primal Knowledge",
				"""While your Rage is active, you can channel primal
				power when you attempt certain tasks; whenever you
				make an ability check using one of the following skills,
				you can make it as a Strength check even if it normally
				uses a different ability:
				Acrobatics, Intimidation, Perception, Stealth, or Survival.
				When you use this ability, your Strength represents primal
				power coursing through you, honing your agility, bearing,
				and senses."""),
			])
			if subclass == "Storm Herald":
				auras = ["Desert", "Sea", "Tundra"]
				aura = random.choice(auras)
				feats.append( Feature("Path of the Storm Herald",
							"""Barbarians who follow the Path of the Storm Herald
							learn to transform rage into a mantle of primal magic,
							tapping into the forces of nature to create powerful
							magical effects."""))
				feats.append(Feature("Storm Aura",
							"""Starting at 3rd level, you emanate a stormy,
							magical aura while you rage. The aura extends <i>10</i> feet
							from you in every direction, but not through total cover.
							<br>Your aura has an effect that activates when
							you enter your rage, and you can activate the
							effect again on each of your turns as a bonus
							action.
							"""))
				if aura == "Desert":
					feats.append(Feature("Storm Aura: Desert",
							""" When this effect is activated, all other creatures
							in your aura take 2 fire damage each. The damage
							increases when you reach certain levels in this class,
							increasing to 3 at 5th level, 4 at 10th level,
							5 at 15th level, and 6 at 20th level.
							"""))
				elif aura == "Sea":
					feats.append(Feature("Storm Aura: Sea",
							""" When this effect is activated, you can choose one
							other creature you can see in your aura. The target
							must make a Dexterity saving throw. The target takes
							1d6 lightning damage on a failed save, or half as much
							damage on a successful one. The damage increases when
							you reach certain levels in this class, increasing to
							2d6 at 10th level, 3d6 at 15th level, and
							4d6 at 20th level.
							"""))
				elif aura == "Tundra":
					feats.append(Feature("Storm Aura: Tundra",
							""" When this effect is activated, each creature of
							your choice in your aura gains 2 temporary hit points,
							as icy spirits inure it to suffering. The temporary
							hit points increase when you reach certain levels in
							this class, increasing to 3 at 5th level,
							4 at 10th level, 5 at 15th level, and 6 at 20th level.
							"""))
		# ---------------- Level 4 ----------------
		if lvl >= 4:
			feats.extend(ApplyRandomFeats(self.char, n=1, level=4))
		# ---------------- Level 5 ----------------
		if lvl >= 5:
			feats.extend([
				Feature("Extra Attack",
					"You can attack twice instead of once whenever you take the Attack action on your turn."),
				Feature("Fast Movement",
					"Your speed increases by 10 feet while you aren't wearing Heavy armor."),
			])
		# ---------------- Level 6 ----------------
		if lvl >= 6:
			if subclass == "Storm Herald":
				if aura == "Desert":
					feats.append(Feature("Storm Soul: Desert",
							""" You gain resistance to fire damage, and you don't suffer the effects of extreme heat, as described in the Dungeon Master's Guide. Moreover, as an action, you can touch a flammable object that isn't being worn or carried by anyone else and set it on fire.
							"""))
				elif aura == "Sea":
					feats.append(Feature("Storm Soul: Sea",
							""" You gain resistance to lightning damage, and you can breathe underwater. You also gain a swimming speed of 30 feet..
							"""))
				elif aura == "Tundra":
					feats.append(Feature("Storm Soul: Tundra",
							""" You gain resistance to cold damage, and you don't suffer the effects of extreme cold, as described in the Dungeon Master's Guide. Moreover, as an action, you can touch water and turn a 5-foot cube of it into ice, which melts after 1 minute. This action fails if a creature is in the cube.
							"""))
		# ---------------- Level 7 ----------------
		if lvl >= 7:
			feats.extend([
				Feature("Feral Instinct",
					"Your instincts are so honed that you have Advantage on Initiative rolls."),
				Feature("Instinctive Pounce",
					"As part of the Bonus Action you take to enter your Rage, you can move up to half your Speed."),
			])
		# ---------------- Level 8 ----------------
		if lvl >= 8:
			feats.extend(ApplyRandomFeats(self.char, n=1, level=8))
		# ---------------- Level 9 ----------------
		if lvl >= 9:
			feats.append(Feature("Brutal Strike",
			"""If you use Reckless Attack, you can forgo any Advantage on one Strength-based attack roll of your choice on your turn. The chosen attack roll mustn't have Disadvantage.
			If the chosen attack roll hits, the target takes an extra 1d10 damage of the same type dealt by the weapon or Unarmed Strike, and you can cause one Brutal Strike effect of your choice.
			You have the following effect options:
			<br><b>Forceful Blow.</b> The target is pushed 15 feet straight away from you. You can then move up to half your Speed straight toward the target without provoking Opportunity Attacks.
			<br><b>Hamstring Blow.</b> The target's Speed is reduced by 15 feet until the start of your next turn. A target can be affected by only one Hamstring Blow at a time—the most recent one."""))
		# ---------------- Level 10 ----------------
		if lvl >= 10:
			if subclass == "Storm Herald":
				feats.append(Feature("Shielding Storm",
					"""At 10th level, you learn to use your mastery of the storm to protect others.
					Each creature of your choice has the damage resistance you gained from the
					Storm Soul feature while the creature is in your Storm Aura."""))
		# ---------------- Level 11 ----------------
		if lvl >= 11:
			feats.append(Feature("Relentless Rage",
				f"""Your Rage can keep you fighting despite grievous wounds.
				If you drop to 0 Hit Points while your Rage is active and
				don't die outright, you can make a DC 10 Constitution saving
				throw. If you succeed, your Hit Points instead change to a
				number equal to twice your Barbarian level({2*lvl}).
				Each time you use this feature after the first, the
				DC increases by 5. When you finish a Short or Long Rest,
				the DC resets to 10."""))
		# ---------------- Level 12 ----------------
		if lvl >= 12:
			feats.extend(ApplyRandomFeats(self.char, n=1, level=12))
		# ---------------- Level 13 ----------------
		if lvl >= 13:
			feats.append(Feature("Improved Brutal Strike",
				"""You have honed new ways to attack furiously.
				The following effects are now among your Brutal Strike options.
				<br><b>Staggering Blow.</b> The target has Disadvantage on the next saving throw it makes, and it can't make Opportunity Attacks until the start of your next turn.
				<br><b>Sundering Blow.</b> Before the start of your next turn, the next attack roll made by another creature against the target gains a +5 bonus to the roll. An attack roll can gain only one Sundering Blow bonus."""))
		# ---------------- Level 14 ----------------
		if lvl >= 14:
			if subclass == "Storm Herald":
				if aura == "Desert":
					feats.append(Feature("Raging Storm: Desert",
							f"""Immediately after a creature in your aura hits
							you with an attack, you can use your reaction to
							force that creature to make a Dexterity saving throw.
							On a failed save, the creature takes fire damage
							equal to half your barbarian level({int(lvl/2)}).
							"""))
				elif aura == "Sea":
					feats.append(Feature("Raging Storm: Sea",
							"""When you hit a creature in your aura with an
							attack, you can use your reaction to force that
							creature to make a Strength saving throw. On a
							failed save, the creature is knocked prone, as if
							struck by a wave
							"""))
				elif aura == "Tundra":
					feats.append(Feature("Raging Storm: Tundra",
							"""Whenever the effect of your Storm Aura is
							activated, you can choose one creature you can see
							in the aura. That creature must succeed on a
							Strength saving throw, or its speed is reduced to
							0 until the start of your next turn, as magical
							frost covers it.
							"""))
		# ---------------- Level 15 ----------------
		if lvl >= 15:
			feats.append(Feature("Persistent Rage",
			"""When you roll Initiative, you can regain all expended uses of Rage. After you regain uses of Rage in this way, you can't do so again until you finish a Long Rest.
			<br>In addition, your Rage is so fierce that it now lasts for 10 minutes without you needing to do anything to extend it from round to round. Your Rage ends early if you have the Unconscious condition (not just the Incapacitated condition) or don Heavy armor."""))
		# ---------------- Level 16 ----------------
		if lvl >= 16:
			feats.extend(ApplyRandomFeats(self.char, n=1, level=16))
		# ---------------- Level 17 ----------------
		if lvl >= 17:
			feats.append(Feature("Improved Brutal Strike",
			"""The extra damage of your Brutal Strike increases
			to 2d10. In addition, you can use two different Brutal
			Strike effects whenever you use your Brutal Strike
			feature."""))
		# ---------------- Level 18 ----------------
		if lvl >= 18:
			feats.append(Feature("Indomitable Might",
			"""If your total for a Strength check or Strength
			saving throw is less than your Strength score, you
			can use that score in place of the total."""))
		# ---------------- Level 19 ----------------
		if lvl >= 19:
			feats.extend(ApplyEpicBoon(self.char, n=1))
		# ---------------- Level 20 ----------------
		if lvl >= 20:
			champ = PrimalChampionFeat()
			features.append(champ)   # so it appears on the sheet
			champ(self.char)         # apply the mutation immediately





		if subclass == "Wildheart":
			WILDHEART_FLAVOR = {
					"Bear": "You carry the calm, immovable strength of the forest.",
					"Eagle": "Your eyes pierce the horizon, your rage lifts you to new heights.",
					"Elk": "Your movement is like thunder across the plains.",
					"Tiger": "Swift and deadly, your strikes are the precision of nature.",
					"Wolf": "You are pack-leader, calling the hunt together.",
					}
			if lvl >= 3:
				WILDHEART_ANIMAL_ASPECTS = {
					"Bear": Feature("Bear Aspect", "While raging, you have resistance to all damage except psychic."),
					"Eagle": Feature("Eagle Aspect",  "While raging, other creatures have disadvantage on opportunity attacks against you, and you can Dash as a bonus action."),
					"Elk": Feature("Elk Aspect", "While raging, your walking speed increases by 15 feet."),
					"Tiger": Feature("Tiger Aspect",  "While raging, you can add 10 feet to your jump distance when you move at least 20 feet."),
					"Wolf": Feature("Wolf Aspect",  "While raging, your allies have advantage on melee attacks against creatures within 5 feet of you."),
					}
				animal = random.choice(list(WILDHEART_ANIMAL_ASPECTS.keys()))
				aspect_feature = WILDHEART_ANIMAL_ASPECTS[animal]
				aspect_feature.description += f" <br><i>{WILDHEART_FLAVOR[animal]}</i>"
				feats.append(aspect_feature)

		return feats
