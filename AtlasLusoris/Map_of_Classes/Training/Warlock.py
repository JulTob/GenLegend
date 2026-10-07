from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import (
	Feature,
	BuildAvailableInvocations,
	ApplyRandomFeats,
	ApplyEpicBoon
	)


class Warlock(Progression):
	HIT_DIE = 8

	def __init__(self, character):
		self.character = character

	HIT_DIE = 8

	@staticmethod
	def warlock_invocations_known(level):
		# These tables match 2024 PHB progression
		if level <= 1: return 1
		if level < 5: return 3
		if level < 7: return 5
		if level < 9: return 6
		if level <= 11: return 7
		if level <= 14: return 8
		if level < 17: return 9
		return 10

	def prepare_invocations(self):
		n = Warlock.warlock_invocations_known(self.character.level)
		available = list(BuildAvailableInvocations(self.character))
		dice = self.character.Dice_Bag(
				"Eldritch_Invocations.choice",
				)
		chosen = dice.sample(available, min(n, len(available)))

		self.character.invocations = []

		# Here is the magic:
		for inv in chosen:
			inv(self.character)  # applies effect if needed
			self.character.invocations.append(inv)

	def features(self, character):
		features = []
		# Assign subclass if not already set
		if not character.Subclass:
			subclass = choice(subclasses["Warlock"])
			character.Subclass = subclass
		else:
			subclass = character.Subclass

		level = character.level
		n_inv = Warlock.warlock_invocations_known(level)


		# Level 1:
		if level >= 1:
			features.append(Feature("Eldritch Invocations",
				f"You have unearthed Eldritch Invocations, pieces of forbidden knowledge that imbue you with an abiding magical ability or other lessons.",
				f"Class: Warlock – {subclass}"))

			features.append(Feature("Pact Magic",
				"""Through occult ceremony, you have formed a pact with a mysterious entity to gain magical powers. The entity is a voice in the shadows-its identity unclear—but its boon to you is concrete: the ability to cast spells.""",
				"Class: Warlock"))

		# Level 2:
		if level >= 2:
			roll_health(character)
			features.append(Feature("Magical Cunning",
				f"You can perform an esoteric rite for 1 minute. At the end of it, you regain expended Pact Magic spell slots but no more than a number equal to half your maximum (round up). Once you use this feature, you can't do so again until you finish a Long Rest.",
				"Class: Warlock"))

		# Level 3:
		if level >= 3:

			if subclass == "Celestial":
				patron_dice = character.Dice_Bag(
						"Celestial.patron.name",
						)
				patron = patron_dice.choice([
					"Solinar, the Sunforged Champion",         # an Empyrean who led the Bright Legion
					"Seraphiel, the Radiant Guard",            # a six-winged seraph of Mount Celestia
					"Mariel, the Trumpet Voice",               # trumpet-bearing Archon of the Fourth Spire
					"Cavoriel, the Golden Sentinel",           # Planetar captain of the Celestial Host
					"Aurius, the Dawnbringer",                 # Deva herald of the first light

					# Celestial Beasts & Uncommon Fiends of Light
					"Lumiel, the Lightweaver Unicorn",         # a star-born unicorn of the Seven Heavens
					"Astreon, the Starmantle Couatl",           # cosmic serpent-guardian
					"Helion, the Daystar Ki-rin",               # dragon-steed of the Sun Throne
					"Caelius, the Cloudstrider Pegasus",       # winged steed of the Serene Aerie
					"Sylvaran, the Forest’s Radiance",     # elk-noble of the Verdant Sphere

					# Archon & Fatebinders
					"Zephyria, the Auroral Dancer",            # Skypiercer Archon of Wind’s Grace
					"Avitor, the Guiding Star",                 # celestial archer who steers lost souls
					"Juniel, the Dawnwatcher",                 # watchful Archon at the Gate of Days
					"Radiatus, the Beaconheart",               # living lighthouse of the Celestial Sea
					"Seluna, the Silver Light",                # Moon-archon of the Constant Vigil

					# Empyreal & Astral Mystics
					"Celestria, the Starweaver",               # astral spirit who threads reality’s web
					"Astrion, the Empyrean Host",               # crown-bearer of the Astral Realm
					"Elunara, the Starlit Path",               # guide through the Midnight Vale
					"Veloria, the Luminous Fount",             # wellspring of celestial grace
					"Serenus, the Calm Radiance",              # mediator between light and shadow

					# Dawn & Twilight Wardens
					"Nymera, the Twilight Wing",               # dusk-bound protector of veiled portals
					"Lunara, the Moon’s Embrace",              # guardian spirit of lunar tides
					"Galara, the Empyreal Shield",             # fortress-spirit of the Celestial Keep
					"Serulen, the Lightwarden",                # archon who polices the planar borders
					"Auradora, the Battle Muse",            # inspirer of hope in mortal hearts

					"Orcax, the Black Sun",
					"Cihuacouatl, The Soul Recollector",
					"Crassistriga, The First Sphinx",
					"Orion, the Constellation",
					"The Forgotten God",
					"Thorondor, Monarch of the Giant Eagles",
					"Demigod",
					"Burning Seraph",
					"Calliope, Muse of Adventures",
					"Clio, Muse of Historians",
					"Erato, Muse of Poets",
					"Euterpe, Muse of Music",
					"Melpomene, Muse of Tragedy",
					"Polyhymnia, Muse of Hymns",
					"Terpsichore, Muse of Dance",
					"Thalia: Muse of comedy",
					"Urania, Muse of astronomy",
					"Ophanim, The Last Angelic Throne",
					"Ophiuchus, Archon of the Zodiac",
					#"Eclipsar",
					# "Planetar", "Dark Sun",
					 #"Seraph", "Phoenix",
					#"Oracle", "Avatar", "Guardian",
					#"Avatar", "Gate Guardian", "Ki-rin"
					])
				features.append(Feature("Celestial Patron",
					f"""Your pact draws on the Upper Planes, the realms of
					everlasting bliss. You entered, willingly or not,
					in a pact with a Celestial: {patron}.
					Your pact allows you to experience
					a hint of the holy light that illuminates
					the multiverse.""",
					"Class: Warlock"))
				features.append(Feature("Healing Light",
					f"""You gain the ability to channel celestial energy to heal wounds. You have a pool of d6s to fuel this healing. The number of dice in the pool equals 1 plus your Warlock level.
					<br>
					As a Bonus Action, you can heal yourself or one creature you can see within 60 feet of yourself, expending dice from the pool. The maximum number of dice you can expend at once equals your Charisma modifier (minimum of one die). Roll the dice you expend, and restore a number of Hit Points equal to the roll's total. Your pool regains all expended dice when you finish a Long Rest.
					""",
					"Class: Warlock"))
			if subclass == "Fiend":
				patron_dice = character.Dice_Bag(
						"Fiend.patron",
						)
				patron = patron_dice.choice([
					"The Infernal Librarian",	"The Hell Duke",	"The Throne of Chains",
					"The Whisperer Beneath the Ashes", "The Lord of Flies", "The Soul Collector",
					"The King of Rot",	"The Vermilion Herald", "The Sovereign",
					"The Baron of Infinite Flesh", "The Flesh Architect",
					"The Prince of Blood", "The Lord of the Ashes", "The God Butcher",
					"The Hellgate Warden", "The Pestilent", "The Black Sulfur",
					"The Corruptor", "Asmodeus, Lord of the Nine Hells",
					"Demogorgon, Prince of Demons", "Orcus, Prince of Undeath",
					"Yeenoghu, Lord of Gnolls",
					])

				features.append(Feature("Fiend Patron",
					f"""Your pact draws on the Lower Planes, the realms of
					perdition. You forged a bargain with {patron}.
					{patron}'s aims are certainly evil, but ultimately unknown
					to you.
					""",
					"Class: Warlock"))
				features.append(Feature("Dark One's Blessing",
					f"""
					When you reduce an enemy to 0 Hit Points, you gain
					<i>Temporary Hit Points equal to your Charisma modifier plus your Warlock level</i>
					(minimum of 1 Temporary Hit Point).
					You also gain this benefit if someone else reduces an enemy within 10 feet of you to 0 Hit Points.
					""",
					"Class: Warlock"))
			if subclass == "Great Old One":
				patron_dice = character.Dice_Bag(
						"GreatOldOne.patron",
						)
				patron = patron_dice.choice([
					"Tharizdun, the Chained God", "Zargon, the Returner",
					"Hadar, the Dark Hunger", 'Cthulhu, The Great One',
					"Yugiax, the Sleeper", "Karunash, The Fractured One",
					"Ouroboric, The Fractal of Madness",
					"Krigon, The Dream Eater",
					"Oneric, The Unfinished",
					"Ol, the Darkness", "Falaxus, The Vortex",
					"Dharana, The Permanent Storm",
					"Mokshada, The Eye Who Watches"
					"Koshal, The Unbirther", "Vajrak, The Legion of One",
					"Raktash, The White Blood","Jvaran, The Will Eater",
					"Yamraka, The Fate Unwaver", "Kushara, the Death Blossom",
					"Tharaka, the Star Eater", "Utpala, The Forgotten",
					"Dendar, the Night Serpent", "Tharizdûn, the Chained God",
					"Atropus, the World Born", "The Infinite Library"
					])

				features.append(Feature("Great Old One Patron",
					f"""You found your bind is to an unspeakable being
					from the Far Realm: {patron}. <br>
					Your Patron's aims are beyond comprehension. But you always
					feel the gaze of {patron} watching you.
					""",
					"Class: Warlock"))
				features.append(Feature("Awakened Mind",
					f"""
					You can form a telepathic connection between your mind and the mind of another. As a Bonus Action, choose one creature you can see within 30 feet of yourself. You and the chosen creature can communicate telepathically with each other while the two of you are within a number of miles of each other equal to your Charisma modifier (minimum of 1 mile). To understand each other, you each must mentally use a language the other knows.
					<br>
					The telepathic connection lasts for a number of minutes equal to your Warlock level. It ends early if you use this feature to connect with a different creature.
					""",
					"Class: Warlock"))
				features.append(Feature("Psychic Spells",
					f"""
					When you cast a Warlock spell that deals damage, you can change its damage type to Psychic. In addition, when you cast a Warlock spell that is an Enchantment or Illusion, you can do so without Verbal or Somatic components.
					""",
					"Class: Warlock"))
			if subclass == "Archfey":
				patron_dice = character.Dice_Bag(
						"Archfey.patron",
						)
				patron = patron_dice.choice([
	"Aranella, the Spring Warden",
	"Sylvenor, the Summer Flame",
	"Cormora, the Autumn Harbinger",
	"Hyfira, the Winter Queen",
	"Veravor, the Leafcaller",
	"Thesmora, the Seedbinder",
	"Zarariel, the Harvest Lord",
	"Odryss, the Falling Leaf",
	"Melanth, the Frost Whisper",
	"Lethora, the Blossom Muse",

	# Twilight & Celestial
	"Duskryn, the Twilight Dancer",
	"Selvaris, the Gloaming Bard",
	"Nyxora, the Night Bloom",
	"Noctifer, the Midnight Refrain",
	"Elyndra, the Moonlit Veil",
	"Solara, the Dawn Chorus",
	"Vespera, the Evening Star",
	"Aurinel, the Morning Dew",
	"Cyranth, the Starweaver",
	"Lunora, the Silver Mirror",

	# Dreamweavers
	"Somnora, the Dreamspinner",
	"Oneira, the Sleep Maiden",
	"Morphelis, the Slumber King",
	"Hypnara, the Restless Echo",
	"Reveria, the Vision Giver",
	"Fantelis, the Reverie Keeper",
	"Euphoron, the Joyous Lapse",
	"Nemoris, the Dreaming Woods",
	"Lythara, the Wandering Sleep",
	"Viscel, the Nightshade Poet",

	# Floral Courts
	"Thalinor, the Vine Lord",
	"Mimora, the Petal Rain",
	"Brythos, the Bloom King",
	"Sylphine, the Whispering Grass",
	"Oakrath, the Ancient Bough",
	"Ivoria, the Hanging Moss",
	"Faylira, the Thorn Queen",
	"Roselorn, the Blush Blossom",
	"Bramoth, the Brambleheart",
	"Fernara, the Spore Dancer",

	# Bestial Lieges
	"Bramorin, the Deer Prince",
	"Lupell, the Wolf Stalker",
	"Fayhune, the Fox Trickster",
	"Ravelen, the Crow Mystic",
	"Serpentis, the Snake Charmer",
	"Hawkris, the Sky Hunter",
	"Wollara, the Bear Guardian",
	"Staglyn, the Antlered Sage",
	"Tigrisi, the Owl Seer",
	"Falinox, the Night Panther",

	# Watersprites
	"Aqualis, the River Singer",
	"Marinth, the Ocean Embrace",
	"Coralyn, the Reef Enchantress",
	"Tideon, the Sea Wanderer",
	"Pearlion, the Depth Whisperer",
	"Ebbryl, the Flowing Veil",
	"Brinora, the Salt Dream",
	"Surian, the Shore Guardian",
	"Druelon, the Wavecaller",
	"Nimora, the Tide Weaver",

	# Windsingers
	"Breezea, the Cloud Dancer",
	"Zephyros, the Gale Singer",
	"Stormora, the Tempest Herald",
	"Mistran, the Wind Whisperer",
	"Gustael, the North Wind",
	"Sirenae, the Whispering Draft",
	"Cyclonis, the Spinning Puff",
	"Vaylora, the Updraft Weaver",
	"Ciros, the Zephyr Scout",
	"Aeralis, the Sighing Sky",

	# Light & Shadow
	"Luminar, the Dawnbringer",
	"Shadeha, the Night Veil",
	"Eclipser, the Shadow Kiss",
	"Radiant, the Sunblade",
	"Umbrae, the Shade Siren",
	"Glisara, the Gleam Maiden",
	"Veloris, the Velvet Dark",
	"Photalis, the Light Warden",
	"Shadera, the Twilight Shard",
	"Aurorix, the Radiant Crown",

	# Fire & Frost
	"Scorchor, the Flameborne",
	"Frosthen, the Iceheart",
	"Embera, the Wildfire",
	"Glacior, the Frost Herald",
	"Ashrono, the Cinder Muse",
	"Chillara, the Winter Song",
	"Blazara, the Blazeheart",
	"Snowtal, the Crystal Frost",
	"Pyronis, the Ember Lash",
	"Icelyn, the Snow Veil",

	# Cosmic & Arcane
	"Starforgia, the Celestial Smith",
	"Cometra, the Sky Dart",
	"Orbiona, the Sphere Maiden",
	"Nebulina, the Mistborn",
	"Galactra, the Dreamsilver",
	"Solandra, the Sun Thread",
	"Meteora, the Falling Star",
	"Auroriel, the Polar Flame",
	"Cosmora, the Vast Song",
	"Astronyx, the Starshard",

	"Titania, Queen of the Summer Court",
	"Oberon, King of the Gloaming",
	"The Queen of Air and Darkness",
	"Hyrsam, Prince of Fools",
	"The Green Lord",

						])
				features.append(Feature("Archfey Patron",
					f"""Your pact draws on the power of the Feywild.
					 You forged a bargain with {patron}.
					{patron} is often inscrutable and whimsical.
					""",
					"Class: Warlock"))
				features.append(Feature("Steps of the Fey",
					f"""
{patron} grants you the ability to move between the boundaries of the planes.
You can cast <i>Misty Step</i> without expending a spell slot a number of times equal to your Charisma modifier (minimum of once), and you regain all expended uses when you finish a Long Rest.
					""",
					"Class: Warlock"))
				features.append(Feature("Steps of the Fey Option",
					f"""
					Whenever you cast <i>Misty Step</i> you can choose one additional effect:
1>
<li><b> Refreshing Step.</b> Immediately after you teleport, you or one creature you can see within 10 feet of yourself gains 1d10 Temporary Hit Points.
</ul>					""",
					"Class: Warlock"))
				features.append(Feature("Steps of the Fey Option",
					f"""
					Whenever you cast <i>Misty Step</i> you can choose one additional effect.
<ul>
<li><b> Taunting Step.</b> Creatures within 5 feet of the space you left must succeed on a Wisdom saving throw against your spell save DC or have Disadvantage on attack rolls against creatures other than you until the start of your next turn.
</ul>					""",
					"Class: Warlock"))


		if level >= 6:
			if subclass == "Archfey":
				features.append(Feature("Misty Escape",
					f"""
You can cast <i>Misty Step</i> as a <b>Reaction</b> in response to taking damage.
					""",
					"Class: Warlock"))
				features.append(Feature("Steps of the Fey Option",
					f"""
					Whenever you cast <i>Misty Step</i> you can choose one of the following additional effects.
<ul>
<li><b>Disappearing Step.</b> You have the <i>Invisible</i> condition until the start of your next turn or until immediately after you make an attack roll, deal damage, or cast a spell.
</ul>					""",
					"Class: Warlock"))
				features.append(Feature("Steps of the Fey Option",
					f"""
					Whenever you cast <i>Misty Step</i> you can choose one additional effects.
<ul style="list-style-type: '🪬'">
<li><b>Dreadful Step.</b> Creatures within 5 feet of the space you left or the space you appear in (your choice) must succeed on a Wisdom saving throw against your spell save DC or take 2d10 Psychic damage.
</ul>					""",
					"Class: Warlock"))
			if subclass == "Fiend":
				features.append(Feature("Dark One's Own Luck",
					f"""
You can call on your fiendish patron to alter fate in your favor.
When you make an ability check or a saving throw, you can use this
feature to <b>add 1d10 to your roll</b>. You can do so after seeing the
 roll but before any of the roll's effects occur.
<br>
You can use this feature a number of times equal to your
Charisma modifier (minimum of once), but you can use it
no more than once per roll. You regain all expended uses
when you finish a Long Rest.					""",
					"Class: Warlock"))
			if subclass == "Great Old One":
				features.append(Feature("Clairvoyant Combatant",
					f"""
When you form a telepathic bond with a creature using your
Awakened Mind, you can force that creature to make a Wisdom
saving throw against your spell save DC. On a failed save,
the creature has Disadvantage on attack rolls against you,
and you have Advantage on attack rolls against that creature
for the duration of the bond.
<br>
Once you use this feature, you can't use it again until you
finish a Short or Long Rest unless you expend a Pact Magic
spell slot (no action required) to restore your use of it.					""",
					"Class: Warlock"))
			if subclass == "Celestial":
				features.append(Feature("Radiant Soul",
					f"""
					Your link to your patron allows you to serve as a conduit for radiant energy. You have Resistance to Radiant damage. Once per turn, when a spell you cast deals Radiant or Fire damage, you can add your Charisma modifier to that spell's damage against one of the spell's targets.

					""",
					"Class: Warlock"))

		if level >= 9:
			from AtlasMagia.Lodge_of_Spells import ContactOtherPlane
			features.append(Feature("Contact Patron",
				f"""
In the past, you usually contacted your patron through intermediaries. Now you can communicate directly; you always have the Contact Other Plane spell prepared. With this feature, you can cast the spell without expending a spell slot to contact your patron, and you automatically succeed on the spell's saving throw.
<br>
Once you cast the spell with this feature, you can't do so in this way again until you finish a Long Rest.
<div class="spell">{ContactOtherPlane}</div>
				""",
				"Class: Warlock"))
		if level >= 10:
			if subclass == "Archfey":
				features.append(Feature("Beguiling Defenses",
					f"""
Your patron teaches you how to guard your mind and body. You are immune to the Charmed condition.

In addition, immediately after a creature you can see hits you with an attack roll, you can take a Reaction to reduce the damage you take by half (round down), and you can force the attacker to make a Wisdom saving throw against your spell save DC. On a failed save, the attacker takes Psychic damage equal to the damage you take. Once you use this Reaction, you can't use it again until you finish a Long Rest unless you expend a Pact Magic spell slot (no action required) to restore your use of it.
					""",
					"Class: Warlock"))
			if subclass == "Celestial":
				features.append(Feature("Celestial Resilience",
f"""
You gain Temporary Hit Points whenever you use your Magical Cunning feature or finish a Short or Long Rest.
These Temporary Hit Points equal your Warlock level plus your Charisma modifier.
Additionally, choose up to five creatures you can see when you gain the points.
Those creatures each gain Temporary Hit Points equal to half your Warlock level
plus your Charisma modifier.
""",
					"Class: Warlock"))
			if subclass == "Great Old One":
				from AtlasMagia.Lodge_of_Spells import Hex
				features.append(Feature("Eldritch Hex",
					f"""
Your alien patron {patron} grants you a powerful curse.
You always have the Hex spell prepared. When you cast Hex
and choose an ability, the target also has Disadvantage on
saving throws of the chosen ability for the duration of the spell.
<div class="spell">{Hex}</div>

""",
					"Class: Warlock"))
				features.append(Feature("Thought Shield",
					f"""
Your thoughts can't be read by telepathy or other means unless you allow it.
You also have Resistance to Psychic damage, and whenever a creature deals
Psychic damage to you, that creature takes the same amount of damage that you take.
					""",
					"Class: Warlock"))
			if subclass == "Fiend":
				features.append(Feature("Fiendish Resilience",
					f"""
					Choose one damage type, other than Force, whenever you finish a Short or Long Rest. You have Resistance to that damage type until you choose a different one with this feature.
					"""
					"Class: Warlock"))


		if level >= 14:
			if subclass == "Archfey":
				features.append(Feature("Bewitching Magic",
					f"""
Your patron grants you the ability to weave your magic with teleportation. Immediately after you cast an Enchantment or Illusion spell using an action and a spell slot, you can cast Misty Step as part of the same action and without expending a spell slot.
""",
					"Class: Warlock"))
			if subclass == "Celestial":
				features.append(Feature("Searing Vengeance",
f"""
When you or an ally within 60 feet of you is about to make a Death Saving Throw, you can unleash radiant energy to save the creature.
The creature regains Hit Points equal to half its Hit Point maximum and can end the Prone condition on itself.
Each creature of your choice that is within 30 feet of the creature takes Radiant damage equal to 2d8 plus your Charisma modifier,
and each has the Blinded condition until the end of the current turn. <br>
Once you use this feature, you can't use it again until you finish a Long Rest.
""",
					"Class: Warlock"))
			if subclass == "Great Old One":
				features.append(Feature("Create Thrall",
					f"""
When you cast Summon Aberration, you can modify it so that it doesn't require Concentration. If you do so, the spell's duration becomes 1 minute for that casting, and when summoned, the Aberration has a number of Temporary Hit Points equal to your Warlock level plus your Charisma modifier.
<br>
In addition, the first time each turn the Aberration hits a creature under the effect of your Hex, the Aberration deals extra Psychic damage to the target equal to the bonus damage of that spell.""",
					"Class: Warlock"))
			if subclass == "Fiend":
				features.append(Feature("Hurl Through Hell",
					f"""
Once per turn when you hit a creature with an attack roll, you can
try to instantly transport the target through the Lower Planes.
The target must succeed on a Charisma saving throw against your
spell save DC, or the target disappears and hurtles through a
nightmare landscape. The target takes <b>8d10 Psychic damage</b> if it
isn't a Fiend, and it has the Incapacitated condition until the
end of your next turn, when it returns to the space it previously
occupied or the nearest unoccupied space.
<br>
Once you use this feature, you can't use it again until you finish a Long Rest unless you expend a Pact Magic spell slot (no action required) to restore your use of it.
					"""
					"Class: Warlock"))

		if level >= 19:
			feats = ApplyEpicBoon(character)
			features.extend(feats)

		if level >= 20:
			features.append(Feature("Eldritch Master", 
				"""When you use your Magical Cunning feature, you regain all your expended Pact Magic spell slots.""",
				"Class: Warlock"))

		self.prepare_invocations()
		features.extend(getattr(character, "invocations", []))

		for asi_level in [4,8,12,16,19]:
			if level >= asi_level:
				features.extend(ApplyRandomFeats(character, n=1, level=asi_level))

		return features


if __name__ == "__main__":
	#-- Self-test (QST-0144.6, ruling 8).  The invocations a Warlock knows and
	#-- the patron's name are drawn from the Character's Dice Bag, opened with
	#-- the purpose of the Tag that offers each choice, with the default key,
	#-- from the pools and with the sample size the builder had before the
	#-- port; the shared random stream is never reached from this file.
	import contextlib
	import io
	import os
	import random as stdlib_random
	import sys
	from AtlasActorLudi.CharactersKit import Character
	from AtlasActorLudi.Map_of_Character_Generation import summon_player

	THIS_FILE = os.path.realpath(
			__file__
			)
	opened = []
		#-- (purpose, version, namespace) of every bag opened from this file
	drawn = {}
		#-- purpose -> [(pool, result)] or [(pool, k, result)] of every draw
	shared = []
		#-- (function, line) of every shared-stream call made from this file

	def from_this_file(
			frame,
			) -> bool:
		return os.path.realpath(
				frame.f_code.co_filename
				) == THIS_FILE

	class Probe_Dice(
			stdlib_random.Random
			):
		"""A Dice Bag that remembers every pool it was asked to draw from."""

		purpose = "?"

		def choice(
				dice,
				population,
				):
			result = super().choice(
					population
					)
			drawn.setdefault(
					dice.purpose,
					[],
					).append(
					(
							list(
									population
									),
							result,
							)
					)
			return result

		def sample(
				dice,
				population,
				k,
				**keywords,
				):
			result = super().sample(
					population,
					k,
					**keywords,
					)
			drawn.setdefault(
					dice.purpose,
					[],
					).append(
					(
							list(
									population
									),
							k,
							result,
							)
					)
			return result

	original_dice_bag = Character.Dice_Bag

	def recording_dice_bag(
			char,
			purpose,
			*,
			version="1",
			namespace="GenLegend",
			):
		bag = original_dice_bag(
				char,
				purpose,
				version=version,
				namespace=namespace,
				)
		if not from_this_file(
				sys._getframe(
						1
						)
				):
			return bag
		opened.append(
				(
						purpose,
						version,
						namespace,
						)
				)
		probe = Probe_Dice()
		probe.setstate(
				bag.getstate()
				)
		probe.purpose = purpose
		return probe

	def counting(
			name,
			):
		original_function = getattr(
				stdlib_random,
				name,
				)

		def counted(
				*arguments,
				**keywords,
				):
			caller = sys._getframe(
					1
					)
			if from_this_file(
					caller
					):
				shared.append(
						(
								name,
								caller.f_lineno,
								)
						)
			return original_function(
					*arguments,
					**keywords,
					)

		return counted

	WATCHED = (
			"choice",
			"sample",
			"shuffle",
			"random",
			"randint",
			"seed",
			)
	saved = {
			name: getattr(
					stdlib_random,
					name,
					)
			for name in WATCHED
			}

	def summon(
			**request,
			):
		with contextlib.redirect_stdout(
				io.StringIO()
				), contextlib.redirect_stderr(
				io.StringIO()
				):
			return summon_player(
					**request
					)

	#-- (Specialization, purpose, pool size, first name, last name), measured
	#-- on the random-module pools before the port.
	PATRON_POOLS = (
			(
					"Archfey",
					"Archfey.patron",
					105,
					"Aranella, the Spring Warden",
					"The Green Lord",
					),
			(
					"Celestial",
					"Celestial.patron.name",
					44,
					"Solinar, the Sunforged Champion",
					"Ophiuchus, Archon of the Zodiac",
					),
			(
					"Fiend",
					"Fiend.patron",
					22,
					"The Infernal Librarian",
					"Yeenoghu, Lord of Gnolls",
					),
			(
					"Great Old One",
					"GreatOldOne.patron",
					24,
					"Tharizdun, the Chained God",
					"The Infinite Library",
					),
			)
	LEVEL = 3

	Character.Dice_Bag = recording_dice_bag
	for name in WATCHED:
		setattr(
				stdlib_random,
				name,
				counting(
						name
						),
				)
	try:
		for specialization, purpose, size, first, last in PATRON_POOLS:
			opened.clear()
			drawn.clear()
			warlock = summon(
					guild="Warlock",
					specialization=specialization,
					level=LEVEL,
					seed=7,
					)
			assert sorted(
					opened_purpose
					for opened_purpose, _, _ in opened
					) == sorted(
					[ "Eldritch_Invocations.choice", purpose ]
					), opened
			assert all(
					(version, namespace) == ("1", "GenLegend")
					for _, version, namespace in opened
					), opened
			[ ( names, patron ) ] = drawn[ purpose ]
			assert ( len( names ), names[ 0 ], names[ -1 ] ) == ( size, first, last ), (
					len( names ),
					names[ 0 ],
					names[ -1 ],
					)
			assert patron in names, patron
			[ ( available, k, chosen ) ] = drawn[ "Eldritch_Invocations.choice" ]
			assert k == min(
					Warlock.warlock_invocations_known( LEVEL ),
					len( available ),
					), ( k, len( available ) )
			assert warlock.invocations == chosen, ( warlock.invocations, chosen )
		assert shared == [], shared
	finally:
		Character.Dice_Bag = original_dice_bag
		for name, function in saved.items():
			setattr(
					stdlib_random,
					name,
					function,
					)

	print(
			"OK: the Warlock's invocations and patron names come from the "
			"Character's Dice Bag under Eldritch_Invocations.choice and the "
			"Specializations' names, with their old pools and sample size."
			)
