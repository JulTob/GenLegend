from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import (
	Feature,
	add_new_fighting_style,
	ApplyRandomFeats,
	ApplyEpicBoon
	)

class Fighter(Progression):
	def __init__(self, character):
		self.char = character

	def features(self, character=None):
		if character is None:
			character = self.char
		else:
			self.char = character
		features = []
		level = self.char.Level  # or .level
		subclass = self.char.Subclass or "Champion"
		secondWinds = 2
		WeaponMasteries = 3
		if level >= 4:
			secondWinds += 1
			WeaponMasteries += 1
		if level >= 10:
			secondWinds += 1
			WeaponMasteries += 1
		if level >= 16:
			WeaponMasteries += 1
		if level >= 2:
			roll_health(self.char)

		if level >= 1:
			features.append(Feature("Second Wind",
			f"""As a Bonus Action, you can regain Hit Points equal to 1d10 plus your Fighter level.
You can use this feature {secondWinds} times. You regain one expended use when you finish a Short Rest, and you regain all expended uses when you finish a Long Rest."""))
			features.append(Feature("Weapon Mastery",
			f"""Your training with weapons allows you to use the mastery properties of {WeaponMasteries} kinds of Simple or Martial weapons of your choice. Whenever you finish a Long Rest, you can practice weapon drills and change one of those weapon choices."""))
			style_feat = add_new_fighting_style(self.char, level=1)
			if style_feat:
				features.append(style_feat)
			else:
				from AtlasLusoris.Grimoire_of_Features import FightingStyleFeat
				features.append(FightingStyleFeat(self.char))
		if level >= 2:
			extra = " for a second time"
			if level >= 17: 	extra = "Once you use this feature twice. You can use it only once on a turn. "
			features.append(Feature("Action Surge",  f"""On your turn, you can take one additional action, except the Magic action. Once you use this feature{extra}, you can't do so again until you finish a Short or Long Rest."""))
			features.append(Feature("Tactical Mind", f"""You have a mind for tactics on and off the battlefield. When you fail an ability check, you can expend a use of your Second Wind to push yourself toward success. Rather than regaining Hit Points, you roll 1d10 and add the number rolled to the ability check, potentially turning it into a success. If the check still fails, this use of Second Wind isn't expended."""))
		if level >= 3:
			if subclass == "Champion":
				features.append(Feature("Champion",  "A Champion focuses on the development of martial prowess in a relentless pursuit of victory. Champions combine rigorous training with physical excellence to deal devastating blows, withstand peril, and garner glory. Whether in athletic contests or bloody battle, Champions strive for the crown of the victor."))
				features.append(Feature("Improved Critical",  """Your attack rolls with weapons and Unarmed Strikes can score a <b>Critical Hit on a roll of 19 or 20 on the d20</b>."""))
				features.append(Feature("Remarkable Athlete",  """Thanks to your athleticism, you have <b>Advantage on Initiative rolls and Strength (Athletics) checks</b>.
					In addition, immediately after you score a <b>Critical Hit, you can move up to half your Speed without provoking Opportunity Attacks.</b>"""))

			if subclass == "Eldritch Knight":
				features.append(Feature("Eldritch Knight",  "Eldritch Knights combine the martial mastery common to all Fighters with a careful study of magic. Their spells both complement and extend their combat skills, providing additional protection to shore up their armor and also allowing them to engage many foes at once with explosive magic."))
				features.append(Feature("War Bond",  """You learn a ritual that creates a magical bond between yourself and one weapon. You perform the ritual over the course of 1 hour, which can be done during a Short Rest. The weapon must be within your reach throughout the ritual, at the conclusion of which you touch the weapon and forge the bond. The bond fails if another Fighter is bonded to the weapon or if the weapon is a magic item to which someone else is attuned.
						Once you have bonded a weapon to yourself, you can't be disarmed of that weapon unless you have the Incapacitated condition. If it is on the same plane of existence, you can summon that weapon as a Bonus Action, causing it to teleport instantly to your hand.
						You can have up to two bonded weapons, but you can summon only one at a time with a Bonus Action. If you attempt to bond with a third weapon, you must break the bond with one of the other two."""))
		if level >= 4:
			feats = ApplyRandomFeats(self.char, n=1, level=4)
			features.extend(feats)
		if level >= 5:
			extra = "twice"
			if level >= 11: extra = "three times"
			if level >= 20: extra = "four times"
			features.append(Feature("Extra Attack",
				f"""You can attack {extra} instead of once
				whenever you take the Attack action
				on your turn."""))

			features.append(Feature("Tactical Shift",
				"""Whenever you activate your Second Wind
				with a Bonus Action, you can move up to
				half your Speed without provoking
				Opportunity Attacks."""))
		if level >= 6:
			feats = ApplyRandomFeats(self.char, n=1, level=6)
			features.extend(feats)
		if level >= 7:
			if subclass == "Champion":
				style_feat = add_new_fighting_style(self.char, level=7)
				if style_feat: features.append(style_feat)
				else: 
					features.append(FightingStyleFeat(self.char))

			if subclass == "Eldritch Knight":
				features.append(Feature("War Magic",
					"""When you take the Attack action on your
					turn, you can replace one of the attacks
					with a casting of one of your Wizard cantrips
					that has a casting time of an action."""))
		if level >= 8:
			feats = ApplyRandomFeats(self.char, n=1, level=8)
			features.extend(feats)
		if level >= 9:
			extra = """you can't use this feature
				again until you finish a Long Rest."""
			if level >= 13: extra = """You can use this feature twice
				before you finish a Long Rest."""
			if level >= 17: extra = """You can use this feature three times
				before you finish a Long Rest."""
			features.append(Feature("Indomitable",
				f"""If you fail a saving throw, you can reroll it
				with a bonus equal to your Fighter level. You must
				use the new roll. <br> {extra}	"""))
			features.append(Feature("Tactical Master",
				f"""When you attack with a weapon whose mastery
				property you can use, you can replace that property
				with the Push, Sap, or Slow property
				for that attack."""))
		if level >= 10:
			if subclass == "Champion":
				features.append(Feature("Heroic Warrior",
					"""The thrill of battle drives you toward
					victory. During combat, you can give yourself
					Heroic Inspiration whenever you start your
					turn without it."""))
			if subclass == "Eldritch Knight":
				features.append(Feature("Eldritch Strike",
					"""When you hit a creature with an attack using a weapon,
					that creature has Disadvantage on the next saving
					throw it makes against a spell you cast before the
					end of your next turn."""))
		if level >= 11:
			pass
		if level >= 12:
			feats = ApplyRandomFeats(self.char, n=1, level=12)
			features.extend(feats)
		if level >= 13:
			features.append(Feature("Studied Attacks",
				"""
				You study your opponents and learn from each attack you make.
				If you make an attack roll against a creature and miss, you
				have Advantage on your next attack roll against that creature
				before the end of your next turn.
				"""))
		if level >= 14:
			feats = ApplyRandomFeats(self.char, n=1, level=14)
			features.extend(feats)
		if level >= 15:
			if subclass == "Champion":
				features.append(Feature("Superior Critical",
				"""
				Your attack rolls with weapons and Unarmed Strikes
				can now score a Critical Hit on a roll of 18–20
				on the d20.
				"""))

			if subclass == "Eldritch Knight":
				features.append(Feature("Arcane Charge",
					"""When you use your Action Surge, you can teleport up to 30 feet to an unoccupied space you can see. You can teleport before or after the additional action."""))
		if level >= 16:
			feats = ApplyRandomFeats(self.char, n=1, level=16)
			features.extend(feats)
		if level >= 17:
			pass
		if level >= 18:
			if subclass == "Champion":
				features.append(Feature("Survivor",
					"""
					You attain the pinnacle of resilience in battle,
					giving you these benefits.<br>
					<b>Defy Death.</b> You have Advantage on
					Death Saving Throws. Moreover, when you roll 18–20
					on a Death Saving Throw, you gain the benefit of
					rolling a 20 on it. <br>
					<b>Heroic Rally.</b> At the start of each of your
					turns, you regain Hit Points equal to 5 plus your
					Constitution modifier if you are Bloodied and have
					at least 1 Hit Point.
					"""))
			if subclass == "Eldritch Knight":
				features.append(Feature("Improved War Magic",
					"""
					When you take the Attack action on your turn,
					you can replace two of the attacks with a
					casting of one of your level
					1 or level 2 Wizard spells
					that has a casting time of an action.
					"""))
		if level >= 19:
			feats = ApplyEpicBoon(self.char,)
			features.extend(feats)
		return features
