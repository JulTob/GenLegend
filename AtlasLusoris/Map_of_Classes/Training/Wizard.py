from ..Grimoire_of_Health  import roll_health, HIT_DIE_TABLE
from ..Codex_of_Progression import Progression

from AtlasLusoris.Grimoire_of_Features import (
		Feature,
		ApplyRandomFeats,
		ApplyEpicBoon
		)


class Wizard(Progression):
	def __init__(self, character):
		self.char = character
	HIT_DIE = 6
	def features(self, character):
		level = character.Level
		subclass = character.Subclass or "Abjurer"
		features = []
		feats = []
		if level >= 1:
			features.append(Feature("Ritual Adept", 
				"You can cast any spell as a Ritual if that spell has the Ritual tag and the spell is in your spellbook. You needn't have the spell prepared, but you must read from the book to cast a spell in this way."))
			features.append(Feature("Spellbook", """Your wizardly apprenticeship culminated in the creation of a unique book: your spellbook. It is a Tiny object that weighs 3 pounds, contains 100 pages, and can be read only by you or someone casting <b>Identify</b>.
			You determine the book's appearance and materials, such as a gilt-edged tome or a collection of vellum bound with twine.<br>
			The book contains the level 1+ spells you know.	 It starts with six level 1 Wizard spells of your choice. For each Wizard level after 1, add two Wizard spells of your choice to your spellbook. Each of these spells must be of a level for which you have spell slots. The spells are the culmination of arcane research you do regularly."""))
			features.append(Feature("Expanding and Replacing a Spellbook", """The spells you add to your spellbook as you gain levels reflect your ongoing magical research, but you might find other spells during your adventures that you can add to the book. You could discover a Wizard spell on a Spell Scroll, for example, and then copy it into your spellbook.<br>
				<b>Copying a Spell into the Book.</b> When you find a level 1+ Wizard spell, you can copy it into your spellbook if it's of a level you can prepare and if you have time to copy it. For each level of the spell, the transcription takes 2 hours and costs 50 GP. Afterward you can prepare the spell like the other spells in your spellbook. <br>
				<b>Copying the Book.</b> You can copy a spell from your spellbook into another book. This is like copying a new spell into your spellbook but faster, since you already know how to cast the spell. You need spend only 1 hour and 10 GP for each level of the copied spell.<br>
				If you lose your spellbook, you can use the same procedure to transcribe the Wizard spells that you have prepared into a new spellbook. Filling out the remainder of the new book requires you to find new spells to do so. For this reason, many wizards keep a backup spellbook."""))
			features.append(Feature("Arcane Recovery",  "You can regain some of your magical energy by studying your spellbook. When you finish a Short Rest, you can choose expended spell slots to recover. The spell slots can have a combined level equal to no more than half your Wizard level (round up), and none of the slots can be level 6 or higher. For example, if you're a level 4 Wizard, you can recover up to two levels' worth of spell slots, regaining either one level 2 spell slot or two level 1 spell slots. <br> Once you use this feature, you can't do so again until you finish a Long Rest."))
		if level >= 2:
			roll_health(self.char)
			features.append(Feature("Scholar",  "While studying magic, you also specialized in another field of study. Choose one of the following skills in which you have proficiency: Arcana, History, Investigation, Medicine, Nature, or Religion. You have Expertise in the chosen skill."))
			character.skills.activate_expertise(
				2,
				["Arcana", "History",	"Investigation",	"Medicine",
				"Nature",	"Religion"],
				dice=character.Dice_Bag( "Scholar.choice" ),
				)
		if level >= 3:
			if subclass == "Evoker":
				features.append(Feature("Evoker", 
					"Your studies focus on magic that creates powerful elemental effects such as bitter cold, searing flame, rolling thunder, crackling lightning, and burning acid. Some Evokers find employment in military forces, serving as artillery to blast armies from afar. Others use their power to protect others, while some seek their own gain."))
				features.append(Feature("Evocation Savant", 
					"Choose two Wizard spells from the Evocation school, each of which must be no higher than level 2, and add them to your spellbook for free.<br>In addition, whenever you gain access to a new level of spell slots in this class, you can add one Wizard spell from the Evocation school to your spellbook for free. The chosen spell must be of a level for which you have spell slots."))
				features.append(Feature("Potent Cantrip", 
					"""Your damaging cantrips affect even creatures that avoid the brunt of the effect.
					When you cast a cantrip at a creature and you miss with the attack roll or the target succeeds on a saving throw against the cantrip,
					the target takes half the cantrip's damage (if any) but suffers no additional effect from the cantrip."""))
		if level >= 4:
			feats += ApplyRandomFeats(character, n=1)
		if level >= 5:
			features.append(Feature("Memorize Spell", 
				"""Whenever you finish a Short Rest,
				you can study your spellbook and replace one of the level
				1+ Wizard spells you have prepared for your Spellcasting
				feature with another level 1+ spell from the book."""))

		if level >= 6 and subclass == "Evoker":
			features.append(Feature("Sculpt Spells", 
			"""You can create pockets of relative safety within the effects of
			your evocations. When you cast an Evocation spell that affects
			other creatures that you can see, you can choose a number of
			them equal to 1 plus the spell's level. The chosen creatures
			automatically succeed on their saving throws against the spell,
			and they take no damage if they would normally take half damage
			on a successful save."""))
		if level >= 8:
			feats += ApplyRandomFeats(character, n=1)
		if level >= 10 and subclass == "Evoker":
			features.append(Feature("Empowered Evocation", 
			"Whenever you cast a Wizard spell from the Evocation school, you can add your Intelligence modifier to one damage roll of that spell."))
		if level >= 12:
			feats += ApplyRandomFeats(character, n=1)
		if level >= 14 and subclass == "Evoker":
			features.append(Feature("Empowered Evocation", 
			"""You can increase the power of your spells.
			When you cast a Wizard spell with a spell slot of levels 1–5
			that deals damage, you can deal maximum damage with that spell
			on the turn you cast it. <br>
			The first time you do so, you suffer no adverse effect.
			If you use this feature again before you finish a Long Rest,
			you take <b>2d12 Necrotic damage</b> for each level of the
			spell slot immediately after you cast it. This damage ignores
			Resistance and Immunity. <br>
			Each time you use this feature again before finishing a
			Long Rest, the Necrotic damage per spell level increases by
			<b>1d12</b>."""))
		if level >= 16:
			feats += ApplyRandomFeats(character, n=1)
		if level >= 18:
			features.append(Feature("Spell Mastery", 
			"""You have achieved such mastery over certain spells that you
			can cast them at will. Choose a level 1 and a level 2 spell
			in your spellbook that have a casting time of an action.
			You always have those spells prepared, and you can cast them
			at their lowest level without expending a spell slot. To cast
			either spell at a higher level, you must expend a spell slot. <br>
			Whenever you finish a Long Rest, you can study your spellbook and
			replace one of those spells with an eligible spell of the same
			level from the book."""))
		if level >= 19:
			feats += ApplyEpicBoon(character, n=1)
		if level >= 20:
			features.append(Feature("Signature Spells", 
			"""Choose two level 3 spells in your spellbook as your signature
			spells. You always have these spells prepared, and you can cast
			each of them once at level 3 without expending a spell slot.
			When you do so, you can't cast them in this way again until you
			finish a Short or Long Rest. To cast either spell at a higher
			level, you must expend a spell slot."""))
		features.extend(feats)
		return features


if __name__ == "__main__":
	from random import Random
	from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores
	from AtlasActorLudi.Grimoire_of_Skills import Char_Skills

	class Probe:
		"""A level 2 Wizard stand-in with the fields Wizard.features reads."""
		def __init__(probe):
			probe.Level = 2
			probe.Subclass = None
			probe.char_class = "Wizard"
			probe.base_health = 6
			probe.opened = []
			probe.skills = Char_Skills(
				AS=AbilityScores(10, 10, 10, 10, 10, 10),
				ProficiencyBonus=2,
				)

		def Dice_Bag(probe, purpose):
			probe.opened.append(purpose)
			return Random(purpose)

	scholar_skills = {"Arcana", "History", "Investigation", "Medicine", "Nature", "Religion"}

	#-- level 2: the hit die rolls from Wizard.hit_points, then the Scholar
	#-- lesson doubles two of its six skills from Scholar.choice
	probe = Probe()
	features = Wizard(probe).features(probe)
	assert probe.opened == ["Wizard.hit_points", "Scholar.choice"], probe.opened
	doubled = {skill.name for skill in probe.skills.get_all_skills() if skill.proficiency_level == 2}
	assert len(doubled) == 2 and doubled <= scholar_skills, doubled
	assert "Scholar" in [feature.name for feature in features]
	assert 7 <= probe.base_health <= 12, probe.base_health

	#-- the same Wizard doubles the same two skills again
	again = Probe()
	Wizard(again).features(again)
	assert {skill.name for skill in again.skills.get_all_skills() if skill.proficiency_level == 2} == doubled

	print("OK - Training/Wizard: the Scholar's Expertise draws from Scholar.choice.")
