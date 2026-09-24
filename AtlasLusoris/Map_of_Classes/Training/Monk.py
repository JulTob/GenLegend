from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import Feature
from AtlasLusoris.Grimoire_of_Features import ApplyRandomFeats, ApplyEpicBoon

class Monk(Progression):
	HIT_DIE = 8
	def __init__(Monk, character):
		Monk.character = character
		Monk.subclasses = {
			"Open Hand": OpenHand,
			"Shadow": Shadow,
			"Elements": Elements,
			"Mercy": Mercy
			}
	@property
	def MartialArtsDice(Monk):
		level = Monk.character.Level
		if level >= 17:	return '1d12'
		if level >= 11:	return '1d10'
		if level >= 5:	return '1d8'
		return '1d6'

	def features(Monk, character):
		level = Monk.character.Level
		subclass_name = Monk.character.Subclass or "Open Hand"

		# Monk Core Features
		feats = []

		# Level 1
		if level >= 1:
			feats.append(Feature("Unarmored Defense",(
				"While not wearing armor or wielding a shield, your AC equals 10 + your Dexterity modifier + your Wisdom modifier."
				)))

			feats.append(Feature("Martial Arts",   (
				f"""
				Your practice of martial arts gives you mastery of combat styles that use your Unarmed Strike and Monk weapons. You gain the following benefits while you are unarmed or wielding only Monk weapons and you aren't wearing armor or wielding a Shield.
				<br>
				<ul style="list-style-type: '🥋'; align:'left'">
						<li> <b> Bonus Unarmed Strike. </b> You can make an Unarmed Strike as a Bonus Action.
						<li> <b> Martial Arts Die.	</b>  You can roll {Monk.MartialArtsDice} in place of the normal damage of your Unarmed Strike or Monk weapons.
						<li> <b> Dexterous Attacks. </b> You can use your Dexterity modifier instead of your Strength modifier for the attack and damage rolls of your Unarmed Strikes and Monk weapons. In addition, when you use the Grapple or Shove option of your Unarmed Strike, you can use your Dexterity modifier instead of your Strength modifier to determine the save DC.
						</ul>
				"""
				)))
			character.skills.Simple_Weapons.set_proficiency()
			character.skills.Light_Weapons.set_proficiency()
		# Level 2
		if level >= 2:
			roll_health(Monk.character)
			character.speed += 10
			feats.append(Feature("Uncanny Metabolism",   (
				"""
				When you roll Initiative, you can regain all expended Focus Points.
				When you do so, roll your Martial Arts die, and regain a number
				of Hit Points equal to your Monk level plus the number rolled. <br>
				Once you use this feature, you can't use it again until you
				finish a <b>Long Rest</b>.
				"""
				)))
		# Level 3
		if level >= 3:
			subclass = Monk.subclasses[subclass_name](character)
			feats += subclass.features(level, Monk.character)
			feats.append(Feature("Deflect Attacks",  (
				"""
				When an attack roll hits you and its damage includes Bludgeoning, Piercing, or Slashing damage, you can take a Reaction to reduce the attack's total damage against you. The reduction equals 1d10 plus your Dexterity modifier and Monk level.

				If you reduce the damage to 0, you can expend 1 Focus Point to redirect some of the attack's force. If you do so, choose a creature you can see within 5 feet of yourself if the attack was a melee attack or a creature you can see within 60 feet of yourself that isn't behind Total Cover if the attack was a ranged attack. That creature must succeed on a Dexterity saving throw or take damage equal to two rolls of your Martial Arts die plus your Dexterity modifier. The damage is the same type dealt by the attack.
				"""
				)))
		# Level 4
		if level >= 4:
			character.set()
			feats += ApplyRandomFeats(character, n=1)
			feats.append(Feature("Slow Fall", (
				"You can take a Reaction when you fall to reduce any damage you take from the fall by an amount equal to five times your Monk level."
				)))
		# Level 5
		if level >= 5:
			feats.append(Feature("Extra Attack", (
				"You can attack twice, instead of once, whenever you take the Attack action on your turn."
				)))

			feats.append(Feature("Stunning Strike",  (
				"""
				Once per turn when you hit a creature with a Monk weapon or an Unarmed Strike, you can expend 1 Focus Point to attempt a stunning strike. The target must make a Constitution saving throw.
				On a failed save, the target has the Stunned condition until the start of your next turn.
				On a successful save, the target's Speed is halved until the start of your next turn,
				and the next attack roll made against the target before then has Advantage.
				"""
				)))
		# Level 6
		if level >= 6:
			character.speed += 5
			feats.append(Feature("Empowered Strikes", (
				"""
				Your Flurry of Blows, Patient Defense, and Step of the Wind gain the following benefits.
				<br>
				Flurry of Blows. You can expend 1 Focus Point to use Flurry of Blows and make three Unarmed Strikes with it instead of two.
				<br>
				Patient Defense. When you expend a Focus Point to use Patient Defense, you gain a number of Temporary Hit Points equal to two rolls of your Martial Arts die.
				<br>
				Step of the Wind. When you expend a Focus Point to use Step of the Wind, you can choose a willing creature within 5 feet of yourself that is Large or smaller. You move the creature with you until the end of your turn. The creature's movement doesn't provoke Opportunity Attacks.
				"""
				)))
		# Level 7
		if level >= 7:
			feats.append(Feature("Evasion", (
				"""
				When you're subjected to an effect that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed on the saving throw and only half damage if you fail.
				<br>
				You don't benefit from this feature if you have the Incapacitated condition.
				"""
			)))
		# Level 8
		if level >= 8:
			character.set()
			feats += ApplyRandomFeats(character, n=1)
		# Level 9
		if level >= 9:
			feats.append(Feature("Acrobatic Movement", (
				"While you aren't wearing armor or wielding a Shield, you gain the ability to move along vertical surfaces and across liquids on your turn without falling during the movement."
				)))
		if level >= 10:
			character.speed += 5
			feats.append(Feature("Heightened Focus", (
				"""
				Your Flurry of Blows, Patient Defense, and Step of the Wind gain the following upgrades.
				<br>
				<b>Flurry of Blows.</b> A creature you hit must succeed on a Constitution saving throw or be stunned until the start of your next turn.
				<br>
				<b>Patient Defense.</b> When you expend a Focus Point, you gain both the Dodge benefit and Temporary Hit Points.
				<br>
				<b>Step of the Wind.</b> When you expend a Focus Point, your Speed doubles until the end of the current turn.
				"""
				)))
			feats.append(Feature("Self-Restoration", (
				"""
				Through sheer force of will, you can remove one of the following conditions from yourself at the end of each of your turns: Charmed, Frightened, or Poisoned.
				<br>
				In addition, forgoing food and drink doesn't give you levels of Exhaustion.
				"""
				)))
		# Level 11
		#if level >= 11:
		# Level 12
		if level >= 12:
			character.set()
			feats += ApplyRandomFeats(character, n=1)
		# Level 13
		if level >= 13:
			feats.append(Feature("Tongue of Sun and Moon",  (
				"You understand all spoken languages and any creature that can understand a language can understand you."
				)))
			feats.append(Feature("Deflect Energy",  (
				"""
				You can now use your Deflect Attacks feature against attacks that deal any damage type, not just Bludgeoning, Piercing, or Slashing.
				"""
				)))
		if level >= 14:
			character.speed += 5
			feats.append(Feature("Disciplined Survivor",  (
				"""
				Your physical and mental discipline grant you proficiency in all saving throws.
				<br>
				Additionally, whenever you make a saving throw and fail, you can expend 1 Focus Point to reroll it, and you must use the new roll.
				"""
				)))
		# Level 15
		if level >= 15:
			feats.append(Feature("Perfect Focus",   (
				"""
				When you roll Initiative and don't use Uncanny Metabolism,
				you regain expended Focus Points until you have 4 if you have 3 or fewer.
				"""
			)))
		# Level 16
		if level >= 16:
			character.set()
			feats += ApplyRandomFeats(character, n=1)
		# Level 18
		if level >= 18:
			feats.append(Feature("Superior Defense", (
				"""
				At the start of your turn, you can expend 3 Focus Points to bolster yourself against harm for 1 minute or until you have the Incapacitated condition. During that time, you have Resistance to all damage except Force damage.
				"""
				)))
			character.speed += 5
		# Level 19
		if level >= 19:
			character.set()
			feats += ApplyEpicBoon(character, n=1)
		# Level 20
		if level >= 20:
			from AtlasLusoris.Grimoire_of_Features import BodyAndMindFeat
			body_and_mind = BodyAndMindFeat()
			feats.append(body_and_mind)
			body_and_mind(character)  # This should apply DEX+4 and WIS+4, up to 25


		return feats

class Way:
	def __init__(self, character):
		self.character = character

class Mercy(Way):
	def features(way, level, character):
		feats = []
		extra_hand_harm = ""
		extra_hand_healing = ""
		# Level 6 extras
		if level >= 6:
			extra_hand_harm = "<br>You can also give that creature the Poisoned condition until the end of your next turn."
			extra_hand_healing = "<br> you can also end one of the following conditions on the creature you heal: <i>Blinded, Deafened, Paralyzed, Poisoned, or Stunned</i>."

		# Level 3 features
		if level >= 3:
			feats.append(Feature("Warrior of Mercy",
				"""
				Warriors of Mercy carry the same touch in either hand:
				the hand that closes a wound and the hand that ends a life.
				They are wandering physicians, but they do not flinch from
				the final choice when mercy must be decisive. They often wear
				masks to keep the face from showing the cost of the choice.
				"""))
			feats.append(Feature("Hand of Harm",
				f"""
				Once per turn when you hit a creature with an Unarmed Strike and deal damage, you can expend 1 Focus Point to deal extra Necrotic damage equal to one roll of your Martial Arts die plus your Wisdom modifier.
				{extra_hand_harm}
				"""))
			feats.append(Feature("Hand of Healing",
				f"""
				As a Magic action, you can expend 1 Focus Point to touch a creature and restore a number of Hit Points equal to a roll of your Martial Arts die plus your Wisdom modifier.
				When you use your Flurry of Blows, you can replace one of the Unarmed Strikes with a use of this feature without expending a Focus Point for the healing.
				{extra_hand_healing}
				"""))


			# Handling extra proficiencies explicitly
			character.skills.Insight.set_proficiency()
			character.skills.Medicine.set_proficiency()
			character.skills.Herbalism_Kit.set_proficiency()

		# Level 11 features
		if level >= 11:
			feats.append(Feature("Flurry of Healing and Harm",
			f"""
			When you use Flurry of Blows, you can replace each of the Unarmed Strikes with a use of Hand of Healing without expending Focus Points for the healing.
			<br>
			In addition, when you make an Unarmed Strike with Flurry of Blows and deal damage, you can use Hand of Harm with that strike without expending a Focus Point for Hand of Harm. You can still use Hand of Harm only once per turn.
			<br>
			You can use these benefits a total number of times equal to your Wisdom modifier (minimum of once). You regain all expended uses when you finish a Long Rest.
			"""))

		# Level 17 features
		if level >= 17:
			feats.append(Feature("Hand of Ultimate Mercy",
			"""
			Your mastery of life energy opens the door to the ultimate mercy.
			As a Magic action, you can touch the corpse of a creature that died
			within the past 24 hours and expend 5 Focus Points. The creature
			then returns to life with a number of Hit Points equal to 4d10
			plus your Wisdom modifier. If the creature died with any of the
			following conditions, the creature revives with the conditions
			removed: Blinded, Deafened, Paralyzed, Poisoned, and Stunned.
			<br>
			Once you use this feature, you can't use it again until you
			finish a Long Rest.
			"""))

		return feats

class Shadow(Way):
	def features(way, level, character):
		feats = []

		# Level 3 features
		if level >= 3:
			from AtlasMagia.Lodge_of_Spells import Darkness, MinorIllusion
			feats.append(Feature("Warrior of Shadow",
				"""
				Warriors of Shadow practice stealth and subterfuge, harnessing the power of the Shadowfell. They are at home in darkness, able to draw gloom around themselves to hide, leap from shadow to shadow, and take on a wraithlike form.
				"""))

			feats.append(Feature("Shadow Arts: Darkness. ",
				f"""
				You can expend 1 Focus Point to cast the Darkness spell
				without spell components. You can see within the spell's
				area when you cast it with this feature. While the spell
				persists, you can move its area of Darkness to a space
				within 60 feet of yourself at the start of each of your
				turns.
				<div class="spell">{Darkness}</div>
				"""))
			feats.append(Feature("Shadow Arts: Darkvision. ",
				"""
				You gain Darkvision with a range of 60 feet. If you
				already have Darkvision, its range increases by 60 feet.
				"""))
			feats.append(Feature("Shadow Arts: Shadowy Figments. ",
				f"""
				You know the Minor Illusion spell.
				Wisdom is your spellcasting ability for it.
				<div class="spell">{MinorIllusion}</div>
				"""))

		# Level 6 features
		if level >= 6:
			feats.append(Feature("Shadow Step",
				"""
				While entirely within Dim Light or Darkness, you can use a
				Bonus Action to teleport up to 60 feet to an unoccupied space
				you can see that is also in Dim Light or Darkness. You then
				have Advantage on the next melee attack you make before the
				end of the current turn.
				"""))

		# Level 11 features
		if level >= 11:
			feats.append(Feature("Improved Shadow Step",
			"""
			When you use your Shadow Step, you can expend 1 Focus Point
			to remove the requirement that you must start and end in
			Dim Light or Darkness for that use of the feature. As part of
			this Bonus Action, you can make an Unarmed Strike immediately
			after you teleport.
			"""))

		# Level 17 features
		if level >= 17:
			feats.append(Feature("Cloak of Shadows",
				"""
				As a Magic action while entirely within Dim Light or Darkness, you can expend 3 Focus Points to shroud yourself with shadows for 1 minute, until you have the Incapacitated condition, or until you end your turn in Bright Light. While shrouded by these shadows, you gain the following benefits.
				<ul style="list-style-type: '🥷🏼'; align:'left'">
					<li><b>Invisibility: </b> You have the Invisible condition. </li>
					<li><b>Partially Incorporeal</b> You can move through occupied spaces as if they were Difficult Terrain. If you end your turn in such a space, you are shunted to the last unoccupied space you were in. </li>
					<li><b>Shadow Flurry.</b>You can use your Flurry of Blows without expending any Focus Points.</li>
					</ul>
				"""))

		return feats

class Elements(Way):
	def features(way, level, character):
		feats = []
		# Level Attunement extras
		elemental_attunement_extra = ""
		if level >= 11:
			elemental_attunement_extra += """<li><b>Stride of the Elements.</b>
				You have a Fly Speed and a Swim Speed equal to your Speed.</li>"""
		if level >= 17:
			elemental_attunement_extra += """<li><b>Damage Resistance.</b>
				You gain Resistance to one of the following damage types
				of your choice: Acid, Cold, Fire, Lightning, or Thunder.
				At the start of each of your turns,
				you can change this choice.</li>"""
			elemental_attunement_extra += """<li><b>Destructive Stride.</b>
				When you use your Step of the Wind, your Speed increases by
				20 feet until the end of the turn. For that duration, any
				creature of your choice takes damage equal to one roll of
				your Martial Arts die when you enter a space within 5 feet
				of it. The damage type is your choice of Acid, Cold, Fire,
				Lightning, or Thunder. A creature can take this damage only
				once per turn.</li>"""
			elemental_attunement_extra += """<li><b>Empowered Strikes.</b>
				Once on each of your turns, you can deal extra damage
				to a target equal to one roll of your Martial Arts die
				when you hit it with an Unarmed Strike. The extra damage
				is the same type dealt by that strike.
				</li>"""


		# Level 3 features
		if level >= 3:
			from AtlasMagia.Lodge_of_Spells import Elementalism
			feats.append(Feature("Warrior of the Elements",
				"""
				Warriors of the Elements tap into the power of the
				Elemental Planes. Harnessing their supernatural focus,
				these Monks momentarily tame the energy of the
				Elemental Chaos to empower themselves in and out of battle.
				"""))
			bullet = character.Pick(
				("🌪️", "🔥", "❄️", "🪨"),
				dice=character.Dice_Bag(
					"training.monk.elements.bullet",
					version="2024",
					namespace="GenLegendMonk",
					),
				)
			feats.append(Feature("Elemental Attunement",
				f"""
				At the start of your turn, you can expend 1 Focus Point to imbue yourself with elemental energy. The energy lasts for 10 minutes or until you have the Incapacitated condition. You gain the following benefits while this feature is active.
				<ul style="list-style-type: '{bullet}'; align:'left'">
					<li><b>Reach </b> When you make an Unarmed Strike, your reach is 10 feet greater than normal, as elemental energy extends from you. </li>
					<li><b> Elemental Strikes.</b> Whenever you hit with your Unarmed Strike, you can cause it to deal your choice of Acid, Cold, Fire, Lightning, or Thunder damage rather than its normal damage type. When you deal one of these types with it, you can also force the target to make a Strength saving throw. On a failed save, you can move the target up to 10 feet toward or away from you, as elemental energy swirls around it. </li>
					{elemental_attunement_extra}
					</ul>
				"""))
			feats.append(Feature("Manipulate Elements",
				f"""
				You know the Elementalism spell. Wisdom is your spellcasting ability for it.
				<div class="spell">{Elementalism}</div>
				"""))
		# Level 6 features
		if level >= 6:
			feats.append(Feature("Elemental Burst",
				"""
				As a Magic action, you can expend 2 Focus Points to cause
				elemental energy to burst in a 20-foot-radius Sphere centered on
				a point within 120 feet of yourself. Choose a damage type:
				Acid, Cold, Fire, Lightning, or Thunder.
				<br>
				Each creature in the Sphere must make a Dexterity saving throw.
				On a failed save, a creature takes damage of the chosen type
				equal to three rolls of your Martial Arts die. On a successful
				save, a creature takes half as much damage.
				"""))


		return feats

class OpenHand(Way):
	def features(way, level, character):
		feats = []

		# Level 3 features
		if level >= 3:
			bullet = character.Pick(
				("🫸", "🫷", "🤚", "✋", "🫱", "🫲", "👋", ""),
				dice=character.Dice_Bag(
					"training.monk.open_hand.bullet",
					version="2024",
					namespace="GenLegendMonk",
					),
				)
			feats.append(Feature("Open Hand Technique",
			f"""
			Whenever you hit a creature with an attack granted by your
			Flurry of Blows, you can impose one of the following effects
			on that target.
			<ul style="list-style-type: '{bullet}'; align:'left'">
				<li><b>Addle.</b> The target can't make Opportunity Attacks
				until the start of its next turn. </li>
				<li><b>Push.</b> The target must succeed on a Strength
				saving throw or be pushed up to 15 feet away from you. </li>
				<li><b>Topple.</b> The target must succeed on a Dexterity
				saving throw or have the Prone condition. </li>
				</ul>
			"""))

		# Level 6 features
		if level >= 6:
			feats.append(Feature("Wholeness of Body",
			"""
			You gain the ability to heal yourself. As a Bonus Action,
			you can roll your Martial Arts die. You regain a number of
			Hit Points equal to the number rolled plus your Wisdom
			modifier (minimum of 1 Hit Point regained).
			<br>
			You can use this feature a number of times equal to your
			Wisdom modifier (minimum of once), and you regain all
			expended uses when you finish a Long Rest.
			"""))

		# Level 11 features
		if level >= 11:
			feats.append(Feature("Fleet Step",
			"""When you take a Bonus Action other than Step of the Wind,
			you can also use Step of the Wind immediately after that
			Bonus Action."""))

		# Level 17 features
		if level >= 17:
			feats.append(Feature("Quivering Palm",
			"""You gain the ability to set up lethal vibrations in someone's
			body. When you hit a creature with an Unarmed Strike, you can
			expend 4 Focus Points to start these imperceptible vibrations,
			which last for a number of days equal to your Monk level.
			The vibrations are harmless unless you take an action to end them.
			Alternatively, when you take the Attack action on your turn, you
			can forgo one of the attacks to end the vibrations. To end them,
			you and the target must be on the same plane of existence.
			When you end them, the target must make a Constitution saving
			throw, taking 10d12 Force damage on a failed save or half as
			much damage on a successful one.
			<br>
			You can have only one creature under the effect of
			this feature at a time. You can end the vibrations harmlessly
			(no action required)."""))

		return feats
