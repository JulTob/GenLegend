"""Paladin progression (PHB 2024)."""

from typing import List  
	# I'm using List from typing for type hinting, so I can annotate feats: List[Feature] = []. The [] is the actual list instance; List is just the type hint.
from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import (
	Feature,
	add_new_fighting_style,
	ApplyRandomFeats,
	ApplyEpicBoon
	)

from AtlasActorLudi.Map_of_Scores import Modifier 


class Paladin(Progression):


	HIT_DIE = 10

	def __init__(self, character):
		self.char = character

	def features(self, character=None):
		if character is None:
			character = self.char
		else:
			self.char = character
		feats: List[Feature] = []
		level = character.Level
		subclass = character.Subclass or "Devotion"
		cha_mod = Modifier(character.abilities.CHA)

		# Level 1
		if level >= 1:
			feats.append(Feature("Lay on Hands",
								f"""<strong>Bonus Action</strong> - Heal pool = {5 * level} HP
								You have a pool of healing power that replenishes when you finish a Long Rest. With that pool, you can restore a total number of Hit Points equal to five times your Paladin level ({5 * level} times).

								As a Bonus Action, you can touch a creature (which could be yourself) and draw power from the pool of healing to restore a number of Hit Points to that creature, up to the maximum amount remaining in the pool.

								You can also expend 5 Hit Points from the pool of healing power to remove the Poisoned condition from the creature; those points don't also restore Hit Points to the creature.""")
								)
			feats.append(Feature("Weapon Mastery",
								"""<strong>Master weapon properties</strong>
								Your training with weapons allows you to use the mastery properties of two kinds of weapons of your choice with which you have proficiency, such as Longswords and Javelins.

								Whenever you finish a Long Rest, you can change the kinds of weapons you chose. For example, you could switch to using the mastery properties of Halberds and Flails."""))

		# Level 2
		if level >= 2:
			roll_health(self.char)
			style_feat = add_new_fighting_style(self.char, level=2)
			if style_feat:
				feats.append(style_feat)
			else:
				feats.append(Feature("Fighting Style", "No new fighting styles available."))
			feats.append(Feature(
					"Paladin's Smite",
					"""<strong>Spell</strong> – Always prepared; you can cast <em>Divine Smite</em> once per Long
					Rest without expending a slot.<br>
					<strong>Bonus Action</strong> – Cast <em>Divine Smite</em> on yourself (Concentration, up to 1
					minute). While it lasts, the next time you hit with a melee weapon or Unarmed Strike you deal 2d8
					radiant damage, plus 1d8 for each slot level above 1st (max 6d8), plus 1d8 more if the target is a
					Fiend or Undead. The spell then ends.<br>
					You can cast it additional times by expending spell slots."""
					))

		# Level 3
		if level >= 3:
			
			uses = 3 if level >= 11 else 2
			feats.append(Feature(
				"Channel Divinity",
				f"""<strong>Uses:</strong> {uses} per Long Rest; you regain one expended use when you finish a
				Short Rest.<br>
				You can channel divine energy to fuel magical effects. Each time you use this class’s Channel
				Divinity, choose one of the effects you know (such as Divine Sense or an option from your
				subclass).<br>
				If an effect requires a saving throw, the DC equals your Paladin spell save DC."""
				))
			if subclass == "Devotion":
				feats.append(Feature("Sacred Weapon",
									 """<strong>Channel Divinity</strong> - As an action
You can imbue a weapon with divine energy. For 1 minute, the weapon glows with bright light in a 20-foot radius and dim light for an additional 20 feet. While the weapon is glowing, you can add your Charisma modifier to attack rolls made with it."""))
				feats.append(Feature("Turn the Unholy",
									 """<strong>Channel Divinity</strong> - As an action
You present your holy symbol and speak a prayer censuring fiends and undead. Each fiend or undead that can see or hear you within 30 feet of you must make a Wisdom saving throw. If the creature fails its saving throw, it is turned for 1 minute or until it takes damage.

A turned creature must spend its turns trying to move as far away from you as it can, and it can't willingly move to a space within 30 feet of you. It also can't take reactions. For its action, it can use only the Dash action or try to escape from an effect that prevents it from moving. If there's nowhere to move, the creature can use the Dodge action."""))
			elif subclass == "Vengeance":
				feats.append(Feature("Abjure Enemy",
									 f"""<strong>Channel Divinity</strong> - As an action
Choose up to {character.Charisma if hasattr(character, 'Charisma') else 'CHA'} creatures within 30 feet of you. Each target must make a Wisdom saving throw. On a failed save, a target is frightened for 1 minute or until it takes any damage. While frightened, the target's speed is 0, and it can't benefit from any bonus to its speed.

On a successful save, the target is immune to this effect for 24 hours."""))
				feats.append(Feature("Vow of Enmity",
									 """<strong>Channel Divinity</strong> - As a bonus action
You can utter a vow of enmity against a creature you can see within 10 feet of you. The target must make a Wisdom saving throw. On a failed save, it is frightened of you for 1 minute or until it takes damage. While frightened, it has disadvantage on attack rolls against you.

On a successful save, the target is immune to this effect for 24 hours."""))
			else:
				feats.append(Feature(f"{subclass} Oath Feature",
									 f"Oath of {subclass} feature."))

		# Level 4
		if level >= 4:
			feats += ApplyRandomFeats(character, n=1, level=4)

		# Level 5
		if level >= 5:
			feats.append(Feature("Extra Attack",
								 """<strong>Multiple Attacks</strong>
								 You can attack twice, instead of once, whenever you take the Attack action on your turn."""))
			feats.append(Feature("Faithful Steed",
					"""<strong>Spell</strong> – Always prepared; you can cast <em>Faithful Steed</em> once per
					Long Rest without expending a slot.<br>
					<strong>Otherworldly Steed</strong> – The spell summons the new Otherworldly Steed stat block.
					When you cast it, choose Balmoral, Charger, or Courser traits; you can change the choice each time
					you cast.<br>
					<strong>Shared Bond</strong> – The steed is celestial, fey, or fiendish (your choice), uses your
					proficiency bonus, understands one language you speak, and vanishes at 0 HP. While it is within 1
					mile you can communicate telepathically, and any spell you cast that targets only you also targets
					the steed.<br>
					<strong>Dismiss / Resummon</strong> – You can dismiss it as an action. Casting the spell again
					resummons the same steed at full HP."""
					))


		# Level 6
		if level >= 6:
			aura_range = 10 if level < 18 else 30
			feats.append(Feature(
      			"Aura of Protection",
					f"""<strong>Saving Throw Aura</strong> – {aura_range}‑ft emanation (inactive while you are
					Incapacitated).<br>
					You and friendly creatures within the aura gain a bonus to all saving throws equal to your
					Charisma modifier (minimum +1).<br>
					If multiple Paladin auras overlap, a creature chooses which Aura of Protection to benefit from."""
					))

		# Level 7
		if level >= 7 and subclass:
			aura_range = 10 if level < 18 else 30
			if subclass == "Devotion":
				feats.append(Feature("Aura of Devotion",
									 f"Immune to charm within {aura_range} ft."))
			elif subclass == "Vengeance":
				feats.append(Feature("Relentless Avenger",
									 "Opportunity attacks when enemy moves away."))
			else:
				feats.append(Feature(f"{subclass} Oath Feature",
									 f"Oath of {subclass} feature."))

		# Level 8
		if level >= 8:
			feats += ApplyRandomFeats(character, n=1, level=8)

		# Level 9
		if level >= 9:
			targets = max(1, cha_mod)
			feats.append(Feature(
				"Abjure Foes",
				f"""<strong>Channel Divinity</strong> – Magic action.<br>
					Choose up to {targets} creatures you can see within 60 ft. Each target must succeed on a Wisdom
					save against your Paladin spell save DC or become <em>Frightened</em> for 1 minute (or until it
					takes damage).<br>
					While frightened this way, a creature can do only one of the following on its turn: move, take an
					action, or take a bonus action."""
					))

		# Level 10
		if level >= 10:
			aura_range = 10 if level < 18 else 30
			feats.append(Feature("Aura of Courage",
								 f"""<strong>Courage Aura</strong> - {aura_range} ft radius
You and friendly creatures within {aura_range} feet of you can't be frightened while you are conscious.

At 18th level, the range of this aura increases to 30 feet."""))

		# Level 11
		if level >= 11:
			feats.append(Feature(
				"Radiant Strikes",
				"""Whenever you hit a creature with a melee weapon attack or an Unarmed Strike, the target takes an
				extra 1d8 radiant damage."""
					))

		# Level 12
		if level >= 12:
			feats += ApplyRandomFeats(character, n=1, level=12)

		# Level 13
		if level >= 13:
			pass  # No features at this level

		# Level 14
		if level >= 14:
			feats.append(Feature(
				"Restoring Touch",
				"""When you use Lay on Hands on a creature, you can expend 5 hit points from the pool (without
					restoring HP) to end one of these conditions on it: Blinded, Charmed, Deafened, Frightened,
					Paralyzed, or Stunned. Spend 5 hit points for each condition you remove."""
				))

		# Level 15
		if level >= 15 and subclass:
			if subclass == "Devotion":
				feats.append(Feature("Purity of Spirit",
									 "Always detect evil and good."))
			elif subclass == "Vengeance":
				feats.append(Feature("Soul of Vengeance",
									 "Opportunity attacks when enemy casts spell."))
			else:
				feats.append(Feature(f"{subclass} Oath Feature",
									 f"Oath of {subclass} feature."))

		# Level 16
		if level >= 16:
			feats += ApplyRandomFeats(character, n=1, level=16)

		# Level 17
		if level >= 17:
			pass  # No features at this level

		# Level 18
		if level >= 18:
			feats.append(Feature("Aura Expansion",
								 "Auras increase to 30 ft."))

		# Level 19
		if level >= 19:
			feats += ApplyEpicBoon(character)

		# Level 20
		if level >= 20 and subclass:
			if subclass == "Devotion":
				feats.append(Feature("Holy Nimbus",
									 "Capstone: radiant aura damages enemies."))
			elif subclass == "Vengeance":
				feats.append(Feature("Avenging Angel",
									 "Capstone: fly and extra damage."))
			else:
				feats.append(Feature(f"{subclass} Oath Feature",
									 f"Capstone of Oath of {subclass}."))

		return feats
