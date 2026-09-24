"""
Official Origin Feat identities required by later 2024-format Backgrounds.

These Tags preserve semantic identity and source provenance.  Their detailed
mechanics remain deliberately catalogued, not guessed, until each receives a
dedicated Feature implementation.
"""

from TopKit import Imprint, Post, Record

from AtlasActorLudi.CharactersKit import Report_Of

from AtlasActorLudi.ProficiencyKit import (
	Commit_Training_Gain,
	Feature_Training_Record,
	Find_Training_Rank,
	New_Feature_Training_Record,
	Training_Batch,
	Training_Grant,
	Training_Rank,
	)
from AtlasActorLudi.SkillsKit import SKILLS, SKILLS_BY_KEY
from AtlasInventarium.ToolsKit import MUSICAL_INSTRUMENTS, TOOLS_BY_KEY
from AtlasLusoris.GuildKit import ability_preference
from AtlasLusoris.FeaturesKit import (
	New_Training_Batch,
	ORIGIN_FEATS,
	Origin_Feat,
	Plan_Feature_Training,
	Reserved_Background_Training,
	grant,
	)
from AtlasVenustas import Chip


def _class_name(
		name: str,
		) -> str:
	safe_name = "".join(
		character
		if character.isalnum()
		else "_"
		for character in name
		)

	return safe_name.strip(
		"_"
		)


def Make_Catalogued_Origin_Feat(
		*,
		name: str,
		source_title: str,
		source_url: str,
		) -> type[Origin_Feat]:
	"""Build one source-aware Origin Feat identity without invented rules."""
	description = (
		f"{name} is granted by an official Background from {source_title}. "
		"Its detailed mechanics await a dedicated Feature implementation."
		)

	@Imprint
	def Awaken(
			char,
			):
		grant(
			char,
			name=name,
			description=description,
			source=f"Origin Feat — {source_title}",
			)

	feature_tag = type(
		_class_name(
			name
			),
		(
			Origin_Feat,
			),
		{
			"NAME": name,
			"DESCRIPTION": Report_Of(
				description
				),
			"SOURCE_TITLE": Report_Of(
				source_title
				),
			"SOURCE_URL": Report_Of(
				source_url
				),
			"MECHANICS_STATUS": Report_Of(
				"catalogued"
				),
			"Awaken": Awaken,
			"__module__": __name__,
			},
		)

	return feature_tag


_SOURCE_URLS = {
	"Eberron: Forge of the Artificer": (
		"https://www.dndbeyond.com/sources/dnd/efota"
		),
	"Forgotten Realms: Heroes of Faerûn": (
		"https://www.dndbeyond.com/sources/dnd/frhof"
		),
	"Astarion's Book of Hungers": (
		"https://www.dndbeyond.com/sources/dnd/aboh"
		),
	"Lorwyn: First Light": (
		"https://www.dndbeyond.com/sources/dnd/lfl"
		),
	"Ravenloft: The Horrors Within": (
		"https://www.dndbeyond.com/sources/dnd/rthw"
		),
	}

_CATALOGUE = (
	(
		"Mutant Aberration",
		"Eberron: Forge of the Artificer",
		),
	(
		"Dragon Cult Initiate",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"Wildwarden",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"Agitator",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"Bastion",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"Banner Bearer",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"Field Lieutenant",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"Arcane Conduit",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"Strong Arm",
		"Forgotten Realms: Heroes of Faerûn",
		),
	(
		"On a Roll",
		"Astarion's Book of Hungers",
		),
	(
		"Cupbearer",
		"Astarion's Book of Hungers",
		),
	(
		"Hard to Hold",
		"Astarion's Book of Hungers",
		),
	(
		"Aurora",
		"Lorwyn: First Light",
		),
	(
		"Jinx",
		"Lorwyn: First Light",
		),
	(
		"Spared",
		"Ravenloft: The Horrors Within",
		),
	(
		"Sharp Eye",
		"Ravenloft: The Horrors Within",
		),
	(
		"Shadow Cast",
		"Ravenloft: The Horrors Within",
		),
	(
		"Gathered Whispers",
		"Ravenloft: The Horrors Within",
		),
	)

def _grant_language(
		char,
		language: str,
		) -> None:
	"""
	Carry a language onto the Character for the sheet's language line.

	Spoken to through whatever the Character is holding.  Once features are
	resolved that is a ``Linguistics``, which owns its own ``Add`` and de-
	duplicates for itself; before then it is a plain list, or nothing at all.
	Reaching past ``Add`` to append to internals is what broke every Origin Feat
	that grants a language, so this asks rather than assumes.
	"""
	languages = getattr(
		char,
		"languages",
		None,
		)

	if languages is None:
		languages = []
		char.languages = languages

	add = getattr(
		languages,
		"Add",
		None,
		)

	if callable(
			add
			):
		add(
			language
			)
		return

	if language not in languages:
		languages.append(
			language
			)


# ---------------------------------------------------------------------------
# RECOVERY NOTE 2026-08-30 -- there must be exactly ONE _grant_training here.
#
# The 2026-08-29 restore left two definitions of this name in this file.  The
# second was the pre-ledger version (took ``(char, options)``, returned a str,
# wrote straight to the mutable sheet via set_proficiency).  Being later in the
# file it shadowed this one, so every caller below -- all four pass
# ``background_tag=`` and read a Training_Batch back -- died with
# "TypeError: _grant_training() got an unexpected keyword argument
# 'background_tag'".  The stale copy was deleted.
#
# If a future restore reintroduces a second definition, THIS is the one to keep:
# it commits through the typed ledger (Plan_Feature_Training / Training_Batch)
# and honours Reserved_Background_Training.  Check with:
#     grep -c 'def _grant_training(' <this file>      # must print 1
# ---------------------------------------------------------------------------

def _grant_training(
		char,
		feature,
		options,
		*,
		source: str = "Origin Feat",
		rank: Training_Rank = Training_Rank.PROFICIENT,
		background_tag=None,
		) -> Training_Batch:
	"""Resolve and commit one typed Skill or Tool grant for a Feature."""
	candidates = []

	for option in options:
		if option == "Musical_Instrument":
			candidates.extend(
				MUSICAL_INSTRUMENTS
				)
			continue

		capability = (
			SKILLS_BY_KEY.get(
				option
				)
			or TOOLS_BY_KEY.get(
				option
				)
			)

		if capability is None:
			raise ValueError(
				f"Unknown training capability {option!r}."
				)

		candidates.append( capability )

	available = tuple(
		capability
		for capability in candidates
		if Find_Training_Rank(
			char,
			capability,
			) is None
		)
	pool = (
		available
		or tuple(
			candidates
			)
		)
	gain = Plan_Feature_Training(
		char,
		feature,
		pool,
		1,
		source=source,
		purpose=f"feat.{feature.__name__}.training",
		allow_trained=True,
		rank=rank,
		exclude=(
			Reserved_Background_Training(
				background_tag
				)
			if rank is Training_Rank.PROFICIENT
			else ()
			),
		)
	Commit_Training_Gain(
		char,
		gain,
		)

	return gain


def _proficiency_bonus(
		char,
		) -> int:
	"""Proficiency Bonus, derived from level when the sheet has not set one."""
	bonus = getattr(
		char,
		"proficiency_bonus",
		None,
		)

	if bonus is not None:
		return int(
			bonus
			)

	level = max(
		1,
		int(
			getattr(
				char,
				"level",
				1,
				) or 1
			),
		)

	return (level - 1) // 4 + 2


def _grant_language(
		char,
		language: str,
		) -> None:
	"""
	Carry a language onto the Character for the sheet's language line.

	Spoken to through whatever the Character is holding.  Once features are
	resolved that is a ``Linguistics``, which owns its own ``Add`` and de-
	duplicates for itself; before then it is a plain list, or nothing at all.
	Reaching past ``Add`` to append to internals is what broke every Origin Feat
	that grants a language, so this asks rather than assumes.
	"""
	languages = getattr(
		char,
		"languages",
		None,
		)

	if languages is None:
		languages = []
		char.languages = languages

	add = getattr(
		languages,
		"Add",
		None,
		)

	if callable(
			add
			):
		add(
			language
			)
		return

	if language not in languages:
		languages.append(
			language
			)


def _proficiency_bonus(
		char,
		) -> int:
	"""Proficiency Bonus, derived from level when the sheet has not set one."""
	bonus = getattr(
		char,
		"proficiency_bonus",
		None,
		)

	if bonus is not None:
		return int(
			bonus
			)

	level = max(
		1,
		int(
			getattr(
				char,
				"level",
				1,
				) or 1
			),
		)

	return (level - 1) // 4 + 2


# Based on the Harper Agent feat
# source: Forgotten Realms: Heroes of Faerûn
class Agitator(Origin_Feat):
	"""Revolutionary rebrand of Harper Agent — official mechanics, new flavor."""

	NAME = "Agitator"
	DESCRIPTION = (
		"<b>Thieves' Cant.</b> You know Thieves' Cant. "
		"<br><b>Instrumental Training.</b> You gain proficiency with a Musical Instrument "
		"of your choice. "
		"<br><b>Cause a Scene.</b> When you take the Help action to aid an ally's attack "
		"roll, the enemy you distract can be within 30 feet of you rather than within "
		"5 feet, provided that enemy can see or hear you."
		)

	@Imprint
	def awaken(
			char,
			background_tag,
			):
		_grant_language(
			char,
			"Thieves' Cant",
			)
		gain = _grant_training(
			char,
			Agitator,
			(
				"Musical_Instrument",
				),
			background_tag=background_tag,
			)
		instrument = gain.grants[ 0 ].capability.name
		description = Agitator.DESCRIPTION.replace(
			"You gain proficiency with a Musical Instrument of your choice",
			f"You have proficiency with {instrument}",
			)
		grant(
			char,
			Agitator.NAME,
			description,
			source="Origin Feat",
			)

	@Record
	def agitator(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Agitator,
			)

	@Post
	def Has_Agitator_Training(
			char,
			):
		return bool( char.agitator.gains )


# Based on the Emerald Enclave Fledgling feat
# source: Forgotten Realms: Heroes of Faerûn
class Wildwarden(Origin_Feat):
	"""Nature-warden rebrand of Emerald Enclave Fledgling — official mechanics, new flavor."""

	NAME = "Wildwarden"
	DESCRIPTION = (
		"<b>Speak with Animals.</b> You always have the Speak with Animals spell "
		"prepared and can cast it with any spell slots you have. Choose Intelligence, "
		"Wisdom, or Charisma as your spellcasting ability for it when you gain this "
		"feat. Cast as a Ritual, its duration is 8 hours. "
		"<b>Warden's Shift.</b> When you take the Help action, you can switch places "
		"with a willing ally within 5 feet of you as part of that action. This "
		"movement doesn't provoke Opportunity Attacks, and you can't use it if the "
		"ally has the Incapacitated condition."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import SpeakwithAnimals

		ability = _pick_mental_casting_ability(char)
		_grant_known_cantrip(char, SpeakwithAnimals)
		description = (
			"<b>Speak with Animals.</b> You always have the <i>Speak with Animals</i> "
			"spell prepared and can cast it with any spell slots you have. "
			f"<b>{ability}</b> is your spellcasting ability for it. Cast as a Ritual, "
			"its duration is 8 hours.<br>"
			"<b>Warden's Shift.</b> When you take the Help action, you can switch places "
			"with a willing ally within 5 feet of you as part of that action. This "
			"movement doesn't provoke Opportunity Attacks, and you can't use it if the "
			"ally has the Incapacitated condition."
			f'<div class="spell">{SpeakwithAnimals}</div>'
			)
		grant(
			char,
			Wildwarden.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"🦊",
					"Speak with Animals",
					"Ritual 8h",
					),
				),
			)


# Based on the Cult of the Dragon Initiate feat
# source: Forgotten Realms: Heroes of Faerûn
class Dragon_Cult_Initiate(Origin_Feat):
	"""De-coupled rebrand of Cult of the Dragon Initiate — official mechanics, kept flavor."""

	NAME = "Dragon Cult Initiate"
	DESCRIPTION = (
		"<b>Dragon's Tongue.</b> You know Draconic. If you already know Draconic, "
		"you instead learn one language of your choice. "
		"<br><b>Dragon's Terror.</b> As a Magic action, you can instill terror in a "
		"creature you can see within 30 feet of you. It must succeed on a Wisdom "
		"saving throw (DC 8 plus your Wisdom modifier and Proficiency Bonus) or have "
		"the Frightened condition until the end of your next turn. On a success, or "
		"when the effect ends, the target is immune to this benefit for 24 hours. "
		"<br><b>Inspired by Fear.</b> When you cause a creature to be Frightened and you "
		"are the source of its fear, you can gain Heroic Inspiration if you lack it. "
		"You regain the use of this benefit when you finish a Short or Long Rest."
		)

	@Imprint
	def awaken(char):
		_grant_language(
			char,
			"Draconic",
			)
		scores = getattr(
			char,
			"AS",
			None,
			)
		wisdom = int(
			getattr(
				scores,
				"WIS",
				10,
				) or 10
			) if scores is not None else 10
		save_dc = 8 + (wisdom - 10) // 2 + _proficiency_bonus(
			char
			)
		grant(
			char,
			Dragon_Cult_Initiate.NAME,
			Dragon_Cult_Initiate.DESCRIPTION,
			source="Origin Feat",
			chips=(
				Chip(
					"🐉",
					"Dragon's Terror",
					f"DC {save_dc}",
					),
				Chip(
					"✨",
					"Inspired by Fear",
					"1/Rest",
					),
				),
			)


# Based on the Tyro of the Gauntlet feat
# source: Forgotten Realms: Heroes of Faerûn
class Bastion(Origin_Feat):
	"""Guardian's rebrand of Tyro of the Gauntlet — official mechanics, new names."""

	NAME = "Bastion"
	DESCRIPTION = (
		"<b>Vigilant.</b> When you take the Ready action, the next attack roll made "
		"against you has Disadvantage before the start of your next turn. "
		"<br><b>Stand as One.</b> When an ally within 5 feet of you is subjected to an "
		"effect that would push or pull it, you can take a Reaction to prevent that "
		"ally from being pushed or pulled. The ally can't have the Incapacitated condition."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Bastion.NAME,
			Bastion.DESCRIPTION,
			source="Origin Feat",
			)


def _pick_mental_casting_ability(char) -> str:
	"""Choose Intelligence, Wisdom, or Charisma — prefer the Character's strongest."""
	labels = (
		"Intelligence",
		"Wisdom",
		"Charisma",
		)
	scores = getattr(char, "AS", None) or getattr(char, "abilities", None)
	if scores is None:
		return char.Pick(list(labels))
	keys = (
		"INT",
		"WIS",
		"CHA",
		)
	values = [
		getattr(scores, key, 10)
		for key in keys
		]
	best = max(values)
	contenders = [
		(label, key)
		for label, key, value in zip(labels, keys, values)
		if value == best
		]
	if len(contenders) == 1:
		return contenders[0][0]
	# A tie on raw score is decided by what the Character actually leans on,
	# not by the dice: Class first, then Background and Species.
	preference = ability_preference(
		char
		)
	ranked = sorted(
		contenders,
		key=lambda pair: (
			preference.index(
				pair[1]
				)
			if pair[1] in preference
			else len(
				preference
				)
			),
		)
	leaders = [
		label
		for label, key in ranked
		if (
			preference.index(
				key
				)
			if key in preference
			else len(
				preference
				)
			) == (
			preference.index(
				ranked[0][1]
				)
			if ranked[0][1] in preference
			else len(
				preference
				)
			)
		]
	return char.Pick(leaders)


def _grant_known_cantrip(char, spell) -> None:
	"""Carry a cantrip onto the Character for later spellcaster merge."""
	if getattr(char, "known_spells", None) is None:
		char.known_spells = []
	names = {
		getattr(entry, "name", None)
		for entry in char.known_spells
		}
	if getattr(spell, "name", None) not in names:
		char.known_spells.append(spell)
	spellcaster = getattr(char, "spellcaster", None)
	if spellcaster is None:
		return
	for bag_name in (
		"cantrips_known",
		"spells_known",
		):
		bag = getattr(spellcaster, bag_name, None)
		if bag is None:
			continue
		bag_names = {
			getattr(entry, "name", None)
			for entry in bag
			}
		if getattr(spell, "name", None) not in bag_names:
			bag.append(spell)


# Based on the Lords' Alliance Agent feat
# source: Forgotten Realms: Heroes of Faerûn
class Banner_Bearer(Origin_Feat):
	"""Herald's rebrand of Lords' Alliance Agent — official mechanics, new names."""

	NAME = "Banner Bearer"
	DESCRIPTION = (
		"<b>Inspiring Strike.</b> Once per turn when you score a Critical Hit against "
		"a creature, you can choose an ally within 30 feet of yourself who can see or "
		"hear you and who lacks Heroic Inspiration. That ally gains Heroic Inspiration. "
		"<br><b>Reassert Honor.</b> When an enemy you can see deals damage to an ally of "
		"yours that is within 5 feet of you, you have Advantage on your next attack "
		"roll against that enemy before the end of your next turn."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Banner_Bearer.NAME,
			Banner_Bearer.DESCRIPTION,
			source="Origin Feat",
			)


# Based on the Purple Dragon Rook feat
# source: Forgotten Realms: Heroes of Faerûn
class Field_Lieutenant(Origin_Feat):
	"""Squire's rebrand of Purple Dragon Rook — official mechanics, new names."""

	NAME = "Field Lieutenant"
	DESCRIPTION = (
		"You gain proficiency in one of the following skills of your choice: Insight, "
		"Performance, or Persuasion. "
		"<b>Rallying Cry.</b> When you roll Initiative and don't have the Incapacitated "
		"condition, you can choose a number of creatures equal to your Proficiency Bonus "
		"that you can see within 30 feet of yourself. Those creatures gain Heroic "
		"Inspiration. Once you use this benefit, you can't do so again until you finish "
		"a Long Rest."
		)

	@Imprint
	def awaken(
			char,
			background_tag,
			):
		gain = _grant_training(
			char,
			Field_Lieutenant,
			(
				"Insight",
				"Performance",
				"Persuasion",
				),
			background_tag=background_tag,
			)
		trained = gain.grants[ 0 ].capability.name
		description = Field_Lieutenant.DESCRIPTION.replace(
			"You gain proficiency in one of the following skills of your choice: "
			"Insight, Performance, or Persuasion",
			f"You have proficiency in <b>{trained}</b>",
			)
		grant(
			char,
			Field_Lieutenant.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"📯",
					"Rallying Cry",
					"1/LR",
					),
				),
			)

	@Record
	def field_lieutenant(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Field_Lieutenant,
			)

	@Post
	def Has_Field_Lieutenant_Training(
			char,
			):
		return bool( char.field_lieutenant.gains )


# Based on the Spellfire Spark feat
# source: Forgotten Realms: Heroes of Faerûn
class Arcane_Conduit(Origin_Feat):
	"""Arcane Mutant's rebrand of Spellfire Spark — official mechanics, new names."""

	NAME = "Arcane Conduit"
	DESCRIPTION = (
		"<b>Magic Absorption.</b> Once per turn, when you take damage from a spell or "
		"magical effect, you reduce the total damage taken by 1d4. You can't use this "
		"benefit if you have the Incapacitated condition. "
		"<b>Overflow.</b> You know the Sacred Flame cantrip. Intelligence, Wisdom, or "
		"Charisma is your spellcasting ability for it (choose when you gain this feat). "
		"You can also cast it as a Bonus Action a number of times equal to your "
		"Proficiency Bonus, and you regain all expended uses when you finish a Long Rest."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import SacredFlame

		ability = _pick_mental_casting_ability(char)
		_grant_known_cantrip(char, SacredFlame)
		uses = getattr(char, "proficiency_bonus", None)
		if uses is None:
			level = max(1, int(getattr(char, "level", 1) or 1))
			uses = (level - 1) // 4 + 2
		description = (
			"<b>Magic Absorption.</b> Once per turn, when you take damage from a "
			"spell or magical effect, you reduce the total damage taken by "
			"<b>1d4</b>. You can't use this benefit if you have the Incapacitated "
			"condition.<br>"
			"<b>Overflow.</b> You know the <i>Sacred Flame</i> cantrip. "
			f"<b>{ability}</b> is your spellcasting ability for it. "
			f"You can cast it as a Bonus Action <b>{uses}</b> times "
			"(equal to your Proficiency Bonus), and you regain all expended uses "
			"when you finish a Long Rest."
			f'<div class="spell">{SacredFlame}</div>'
			)
		grant(
			char,
			Arcane_Conduit.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"🔥",
					"Overflow",
					f"{uses}/LR",
					),
				),
			)


# Based on the Zhentarim Ruffian feat
# source: Forgotten Realms: Heroes of Faerûn
class Strong_Arm(Origin_Feat):
	"""Bailiff's rebrand of Zhentarim Ruffian — official mechanics, new names."""

	NAME = "Strong Arm"
	DESCRIPTION = (
		"<b>Exploit Opening.</b> When you roll damage for an Opportunity Attack, you "
		"can roll the damage dice twice and use either roll against the target. "
		"<br><b>On My Mark.</b> If you have Heroic Inspiration when you roll Initiative, "
		"you can expend it to give yourself and your allies Advantage on that "
		"Initiative roll."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Strong_Arm.NAME,
			Strong_Arm.DESCRIPTION,
			source="Origin Feat",
			)


# Based on the Aberrant Dragonmark feat
# source: Eberron: Forge of the Artificer
class Mutant_Aberration(Origin_Feat):
	"""Aberrant Mutant's rebrand of Aberrant Dragonmark — official mechanics, new names."""

	NAME = "Mutant Aberration"
	DESCRIPTION = (
		"<b>Mutant Fortitude.</b> When you fail a Constitution saving throw, you "
		"can take a Reaction to roll 1d4 and add the number rolled to the save, "
		"potentially turning the failure into a success. Once you've used this "
		"benefit, you can't use it again until you finish a Long Rest. "
		"<b>Mutant Magic.</b> You know one cantrip of your choice from the Sorcerer "
		"spell list. Also, choose a level 1 spell from that spell list. You always "
		"have that spell prepared. "
		"<b>Power Surge.</b> When you cast the level 1 spell from this feat, you can "
		"expend one of your Hit Point Dice and roll it. If you roll an even number, "
		"you gain a number of Temporary Hit Points equal to the number rolled. If "
		"you roll an odd number, one creature within 30 feet of you (not including "
		"you) takes Force damage equal to the number rolled. If no other creatures "
		"are in range, you take the damage."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import (
			AcidSplash,
			ChaosBolt,
			ChillTouch,
			MagicMissile,
			MindSliver,
			PoisonSpray,
			RayofSickness,
			ShockingGrasp,
			WitchBolt,
			)

		# The Sorcerer list is not yet queryable as a Tag (QST-0048.1), so the
		# choice is drawn from a shortlist that reads as an uncontrolled body
		# rather than a studied one.
		cantrip = char.Pick(
			[
				MindSliver,
				ChillTouch,
				ShockingGrasp,
				AcidSplash,
				PoisonSpray,
				],
			)
		spell = char.Pick(
			[
				ChaosBolt,
				MagicMissile,
				WitchBolt,
				RayofSickness,
				],
			)
		_grant_known_cantrip(char, cantrip)
		_grant_known_cantrip(char, spell)
		description = (
			"<b>Mutant Fortitude.</b> When you fail a Constitution saving throw, "
			"you can take a Reaction to roll <b>1d4</b> and add the number rolled "
			"to the save, potentially turning the failure into a success. Once "
			"you've used this benefit, you can't use it again until you finish a "
			"Long Rest.<br>"
			f"<b>Mutant Magic.</b> You know the <i>{cantrip.name}</i> cantrip, and "
			f"you always have <i>{spell.name}</i> prepared.<br>"
			f"<b>Power Surge.</b> When you cast <i>{spell.name}</i>, you can expend "
			"one of your Hit Point Dice and roll it. If you roll an <b>even</b> "
			"number, you gain a number of Temporary Hit Points equal to the number "
			"rolled. If you roll an <b>odd</b> number, one creature within 30 feet "
			"of you (not including you) takes Force damage equal to the number "
			"rolled. If no other creatures are in range, you take the damage."
			f'<div class="spell">{cantrip}</div>'
			f'<div class="spell">{spell}</div>'
			)
		grant(
			char,
			Mutant_Aberration.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U0001FA78",
					"Mutant Fortitude",
					"1/LR",
					),
				Chip(
					"\u26A1",
					"Power Surge",
					"Hit Die",
					),
				),
			)


# Sharp Eye is not setting-bound, so it keeps its published name.
# source: Ravenloft: The Horrors Within
class Sharp_Eye(Origin_Feat):
	"""Investigator's origin feat — official mechanics, unchanged name."""

	NAME = "Sharp Eye"
	DESCRIPTION = (
		"When you take the Search or Study action, you can give yourself Advantage "
		"on any ability check you make as part of that action. You can use this "
		"benefit a number of times equal to your Proficiency Bonus, and you regain "
		"all expended uses when you finish a Long Rest. If the check fails, this "
		"use isn't expended."
		)

	@Imprint
	def awaken(char):
		uses = _proficiency_bonus(
			char
			)
		description = (
			"When you take the <b>Search</b> or <b>Study</b> action, you can give "
			"yourself <b>Advantage</b> on any ability check you make as part of "
			"that action. You can use this benefit "
			f"<b>{uses}</b> times (your Proficiency Bonus), and you regain all "
			"expended uses when you finish a Long Rest. <b>If the check fails, "
			"the use isn't expended</b>, so a failure costs you only time."
			)
		grant(
			char,
			Sharp_Eye.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U0001F50D",
					"Sharp Eye",
					f"{uses}/LR",
					),
				),
			)


# TODO (questa pending): the nine Dark Gift feats from the same book
# (Aberrant Anatomy, Echoing Soul, Gathered Whispers, Living Shadow, Mist
# Walker, Second Skin, Symbiotic Being, Touch of Death, Watchers).  They fill
# the Origin Feat slot as an alternative, at the DM's discretion, and share one
# shape: a real benefit plus a curse that fires on a natural 1.  Only Mist
# Walker names Ravenloft geography; the rest port as written.  Investigator,
# Spirit Medium and Mist Wanderer all want them.


# Based on the Survivor feat
# source: Ravenloft: The Horrors Within
class Spared(Origin_Feat):
	"""Survivor's rebrand of Survivor the feat, so the Background may take the name."""

	NAME = "Spared"
	DESCRIPTION = (
		"<b>Hypervigilance.</b> When you roll Initiative, if the result of the D20 "
		"Test is 9 or lower, you can reroll the d20 and must use the new roll. "
		"<b>Steel Yourself.</b> When you fail a saving throw to avoid or end the "
		"Charmed or Frightened condition, you can take a Reaction to add your "
		"Proficiency Bonus to that save, potentially turning the failure into a "
		"success. Once you use this benefit, you can't use it again until you "
		"finish a Long Rest."
		)

	@Imprint
	def awaken(char):
		bonus = _proficiency_bonus(
			char
			)
		description = (
			"<b>Hypervigilance.</b> When you roll Initiative, if the result of the "
			"D20 Test is <b>9 or lower</b>, you can reroll the d20 and must use "
			"the new roll.<br>"
			"<b>Steel Yourself.</b> When you <b>fail</b> a saving throw to avoid or "
			"end the <b>Charmed</b> or <b>Frightened</b> condition, you can take a "
			f"Reaction to add <b>+{bonus}</b> (your Proficiency Bonus) to that "
			"save, potentially turning the failure into a success. Once per Long "
			"Rest."
			)
		grant(
			char,
			Spared.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U0001F6E1",
					"Steel Yourself",
					"1/LR",
					),
				),
			)


# ---------------------------------------------------------------------------
# Dark Gifts — power that was done to you, with a curse attached
#
# A classification, not a feat.  Dark Gifts fill the Origin Feat slot as an
# alternative, at the DM's discretion, and every one of them pairs a real
# benefit with a price that fires on a natural 1.  Subclassing means
# ``char in Dark_Gift`` answers itself, and the eight not yet written slot in
# under the same parent without anything else changing.
#
# The published prerequisite ("a Ravenloft campaign") is dropped: the shape is
# not setting-bound, and only Mist Walker names that geography.
# ---------------------------------------------------------------------------


class Dark_Gift(Origin_Feat):
	"""A boon that arrived uninvited and kept a share of you."""

	CATEGORY = Report_Of(
		"Dark Gift"
		)


# Based on the Gathered Whispers dark gift
# source: Ravenloft: The Horrors Within
class Gathered_Whispers(Dark_Gift):
	"""Spirit Medium's origin feat — official mechanics, unchanged name."""

	NAME = "Gathered Whispers"
	DESCRIPTION = (
		"You are haunted by a cacophony of whispering spirits only you can hear. "
		"<b>Grave Words.</b> You learn the Message spell and can cast it without "
		"Material components. Additionally, you always have the Augury spell "
		"prepared. You can cast it without a spell slot or spell components, and "
		"you must finish a Long Rest before you can cast it in this way again. You "
		"can also cast the spell using any spell slots you have. Intelligence, "
		"Wisdom, or Charisma is your spellcasting ability for this benefit (choose "
		"when you select this feat). "
		"<b>Protective Shroud.</b> When you are hit by an attack roll, you can take "
		"a Reaction to channel your haunting spirits into a protective, otherworldly "
		"scream. You can add your Proficiency Bonus to your AC against that attack, "
		"potentially causing it to miss. You can use this benefit a number of times "
		"equal to your Proficiency Bonus, and you regain all expended uses when you "
		"finish a Long Rest. "
		"<b>Voices from Beyond.</b> Immediately after you make a D20 Test and roll a "
		"1 on the d20, the haunting whispers rise to a ghastly volume. Make a Wisdom "
		"saving throw (DC 13 plus your Proficiency Bonus). On a failed save, you "
		"have the Deafened condition until the end of your next turn. While "
		"Deafened, you have Disadvantage on ability checks and attack rolls."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import Augury, Message

		ability = _pick_mental_casting_ability(
			char
			)
		uses = _proficiency_bonus(
			char
			)
		_grant_known_cantrip(char, Message)
		_grant_known_cantrip(char, Augury)
		description = (
			"You are haunted by a cacophony of whispering spirits only you can "
			"hear.<br>"
			"<b>Grave Words.</b> You know <i>Message</i> and can cast it without "
			"Material components. You always have <i>Augury</i> prepared; you can "
			"cast it without a spell slot or spell components once per Long Rest, "
			"and you can also cast it using any spell slots you have. "
			f"<b>{ability}</b> is your spellcasting ability for this benefit.<br>"
			"<b>Protective Shroud.</b> When you are <b>hit</b> by an attack roll, "
			"you can take a Reaction to channel your haunting spirits into a "
			"protective, otherworldly scream, adding "
			f"<b>+{uses}</b> (your Proficiency Bonus) to your AC against that "
			"attack, potentially causing it to miss. "
			f"<b>{uses}</b> times per Long Rest.<br>"
			"<b>Voices from Beyond.</b> Immediately after you make a D20 Test and "
			"roll a <b>1</b>, the whispers rise to a ghastly volume. Make a Wisdom "
			f"saving throw (<b>DC {13 + uses}</b>). On a failure you have the "
			"<b>Deafened</b> condition until the end of your next turn, and while "
			"Deafened you have Disadvantage on ability checks and attack rolls."
			f'<div class="spell">{Message}</div>'
			f'<div class="spell">{Augury}</div>'
			)
		grant(
			char,
			Gathered_Whispers.NAME,
			description,
			source="Origin Feat \u2014 Dark Gift",
			chips=(
				Chip(
					"\U0001F52E",
					"Augury",
					"1/LR",
					),
				Chip(
					"\U0001F4A2",
					"Protective Shroud",
					f"{uses}/LR",
					),
				),
			)


# Based on the Mist Walker dark gift
# source: Ravenloft: The Horrors Within
class Shadow_Cast(Dark_Gift):
	"""Shadow's rebrand of Mist Walker — official mechanics, new names.

	Domain Traveler is deliberately absent.  It was the one Dark Gift benefit
	whose text named Ravenloft's geography, and a planar crossing is a table
	permission rather than a feat: it lives in the Background's hook, where the
	DM has already agreed to it.
	"""

	NAME = "Shadow Cast"
	DESCRIPTION = (
		"<b>Flinch.</b> When you take damage, or fail a saving throw to avoid or "
		"end the Grappled or Restrained condition, you can take a Reaction and "
		"teleport up to 15 feet to an unoccupied space you can see. You can use "
		"this a number of times equal to your Proficiency Bonus, and you regain all "
		"expended uses when you finish a Long Rest. "
		"<b>It Follows.</b> Every time you finish a Long Rest, you must travel more "
		"than 10 miles away before taking a Short Rest. Otherwise you must succeed "
		"on a Constitution saving throw (DC 13 plus your Proficiency Bonus) or gain "
		"no benefit from that Short Rest."
		)

	@Imprint
	def awaken(char):
		bonus = _proficiency_bonus(
			char
			)
		description = (
			"<b>Flinch.</b> When you take damage, or fail a saving throw to avoid "
			"or end the <b>Grappled</b> or <b>Restrained</b> condition, you can "
			"take a Reaction and teleport up to <b>15 feet</b> to an unoccupied "
			f"space you can see. <b>{bonus}</b> times per Long Rest.<br>"
			"<b>It Follows.</b> Every time you finish a Long Rest, you must travel "
			"more than <b>10 miles</b> away before taking a Short Rest. Otherwise "
			"you must succeed on a Constitution saving throw "
			f"(<b>DC {13 + bonus}</b>) or gain no benefit from that Short Rest."
			)
		grant(
			char,
			Shadow_Cast.NAME,
			description,
			source="Origin Feat \u2014 Dark Gift",
			chips=(
				Chip(
					"\U0001F4A8",
					"Flinch",
					f"{bonus}/LR",
					),
				Chip(
					"\U0001F311",
					"It Follows",
					"10 miles",
					),
				),
			)


# Based on the Vampire's Plaything feat
# source: Astarion's Book of Hungers
class Cupbearer(Origin_Feat):
	"""Servant's rebrand of Vampire's Plaything — official mechanics, new names.

	The historical office explains both halves of Decanting: a cupbearer served
	the drink *and* tasted it first for poison.  "Vampire's Plaything" is gone
	because it settled the one question the Background refuses to settle, namely
	whether you were a victim or an accomplice.
	"""

	NAME = "Cupbearer"
	DESCRIPTION = (
		"<b>Decanting.</b> When you finish a Long Rest, you can create one Potion "
		"of Healing or an Antitoxin, as long as you have an empty vial or flask. "
		"These liquids evaporate when you finish another Long Rest. "
		"<b>Timely Retreat.</b> You can take a Bonus Action to take the Dash action "
		"or the Disengage action. You can use this benefit a number of times equal "
		"to your Proficiency Bonus, and you recover all expended uses when you "
		"finish a Long Rest. "
		"<b>On Call.</b> The DM determines your former masters (a vampire dynasty is "
		"recommended), their goals, and their fate. Talk with your DM about weaving "
		"them into the story. While you and your former masters are on the same "
		"plane of existence, they can communicate with you telepathically, and you "
		"can choose to allow them to perceive through your senses."
		)

	@Imprint
	def awaken(char):
		uses = _proficiency_bonus(
			char
			)
		description = (
			"<b>Decanting.</b> When you finish a Long Rest, you can create one "
			"<i>Potion of Healing</i> or an <i>Antitoxin</i>, as long as you have "
			"an empty vial or flask. These liquids <b>evaporate</b> when you finish "
			"another Long Rest.<br>"
			"<b>Timely Retreat.</b> You can take a <b>Bonus Action</b> to take the "
			f"Dash or Disengage action, <b>{uses}</b> times (your Proficiency "
			"Bonus), recovered on a Long Rest.<br>"
			"<b>On Call.</b> The DM determines your former masters (a vampire dynasty "
			"is recommended), their goals, and their fate. Talk with your DM about "
			"weaving them into the story. While you and your former masters are on "
			"the same plane of existence, they can communicate with you "
			"telepathically, and you can choose to allow them to perceive through "
			"your senses."
			)
		grant(
			char,
			Cupbearer.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U0001F9EA",
					"Decanting",
					"1/LR",
					),
				Chip(
					"\U0001F6AA",
					"Timely Retreat",
					f"{uses}/LR",
					),
				),
			)


# Based on the Tireless Reveler feat
# source: Astarion's Book of Hungers
class On_a_Roll(Origin_Feat):
	"""Gambler's rebrand of Tireless Reveler — official mechanics, new name.

	The published name reads as a party.  The rule is a streak: somebody else
	spends their luck and yours comes back, which is the hot hand, not a feast.
	"""

	NAME = "On a Roll"
	DESCRIPTION = (
		"When an ally you can see within 60 feet of yourself expends Heroic "
		"Inspiration, you can gain Heroic Inspiration if you lack it. You can use "
		"this benefit a number of times equal to your Proficiency Bonus, and you "
		"regain all expended uses when you finish a Short or Long Rest."
		)

	@Imprint
	def awaken(char):
		uses = _proficiency_bonus(
			char
			)
		description = (
			"When an ally you can see within <b>60 feet</b> of yourself expends "
			"<b>Heroic Inspiration</b>, you can gain Heroic Inspiration if you "
			f"lack it. <b>{uses}</b> times (your Proficiency Bonus), and you "
			"regain all expended uses when you finish a <b>Short or Long Rest</b>."
			)
		grant(
			char,
			On_a_Roll.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U0001F3B2",
					"On a Roll",
					f"{uses}/SR",
					),
				),
			)


# Based on the Vampire Hunter feat
# source: Astarion's Book of Hungers
class Hard_to_Hold(Origin_Feat):
	"""Exorcist's rebrand of Vampire Hunter — official mechanics, new name.

	Nothing in the published rules is about vampires, or about stakes: both
	benefits are about *not being taken*.  You get out of what holds you and you
	shrug off what drains you, which is the whole Background — everything out
	there wants you to stop being a separate person, and you are professionally
	difficult to absorb.
	"""

	NAME = "Hard to Hold"
	DESCRIPTION = (
		"<b>Adroit Escape.</b> You have Advantage on checks to escape from "
		"nonmagical restraints or the Grappled condition. "
		"<b>Vitality Ward.</b> When you take Necrotic damage, you can take a "
		"Reaction to mitigate the damage. Roll a number of d6s equal to your "
		"Proficiency Bonus, and add them together. Reduce the Necrotic damage you "
		"take by this total. Once you use this benefit, you can't use it again "
		"until you finish a Short or Long Rest."
		)

	@Imprint
	def awaken(char):
		dice = _proficiency_bonus(
			char
			)
		description = (
			"<b>Adroit Escape.</b> You have <b>Advantage</b> on checks to escape "
			"from nonmagical restraints or the <b>Grappled</b> condition.<br>"
			"<b>Vitality Ward.</b> When you take <b>Necrotic</b> damage, you can "
			f"take a Reaction to roll <b>{dice}d6</b> (your Proficiency Bonus) and "
			"reduce that damage by the total. Once per Short or Long Rest."
			)
		grant(
			char,
			Hard_to_Hold.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U0001F6E1",
					"Vitality Ward",
					f"{dice}d6, 1/SR",
					),
				),
			)


# Based on the Child of the Sun feat
# source: Lorwyn: First Light
class Aurora(Origin_Feat):
	"""Destined's rebrand of Child of the Sun — official mechanics, new names.

	"Eyes of Eirdu" named a place that no longer exists in this project, so it
	becomes Unclouded Eyes.  Note it is an *aura*: allies within 10 feet share
	it, which is why the Background is about the people who follow you.
	"""

	NAME = "Aurora"
	DESCRIPTION = (
		"<b>Unclouded Eyes.</b> You and allies within 10 feet of you have Advantage "
		"on saving throws made to avoid or end the Blinded condition. "
		"<b>Faerie Fire.</b> You learn the Faerie Fire spell. Intelligence, Wisdom, "
		"or Charisma is your spellcasting ability for this spell (choose when you "
		"select this feat). You can cast it once without a spell slot, and you "
		"regain the ability to cast it in that way when you finish a Long Rest. You "
		"can also cast the spell using any spell slots you have. When you cast it "
		"without a spell slot using this benefit, taking damage can't break your "
		"Concentration on the spell."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import FaerieFire

		ability = _pick_mental_casting_ability(
			char
			)
		_grant_known_cantrip(char, FaerieFire)
		description = (
			"<b>Unclouded Eyes.</b> You <i>and allies within 10 feet of you</i> "
			"have <b>Advantage</b> on saving throws made to avoid or end the "
			"<b>Blinded</b> condition.<br>"
			"<b>Faerie Fire.</b> You know <i>Faerie Fire</i> and can cast it once "
			"without a spell slot per Long Rest, or with any spell slots you have. "
			f"<b>{ability}</b> is your spellcasting ability for it. Cast without a "
			"slot, <b>taking damage cannot break your Concentration</b> on it."
			f'<div class="spell">{FaerieFire}</div>'
			)
		grant(
			char,
			Aurora.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U00002728",
					"Faerie Fire",
					"1/LR",
					),
				),
			)


# Based on the Shadowmoor Hexer feat
# source: Lorwyn: First Light
class Jinx(Origin_Feat):
	"""Fated's rebrand of Shadowmoor Hexer — official mechanics, new names."""

	NAME = "Jinx"
	DESCRIPTION = (
		"<b>Hex.</b> You always have the Hex spell prepared. Intelligence, Wisdom, "
		"or Charisma is your spellcasting ability for this spell (choose when you "
		"select this feat). You can cast it once without a spell slot, and you "
		"regain the ability to cast it in that way when you finish a Long Rest. You "
		"can also cast the spell using any spell slots you have. "
		"<b>Backfire.</b> When a creature that you've cursed with Hex hits you with "
		"an attack roll, the creature takes Psychic damage equal to your Proficiency "
		"Bonus. A creature takes this damage only once per turn."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import Hex

		ability = _pick_mental_casting_ability(
			char
			)
		bonus = _proficiency_bonus(
			char
			)
		_grant_known_cantrip(char, Hex)
		description = (
			"<b>Hex.</b> You always have <i>Hex</i> prepared, and can cast it once "
			"without a spell slot per Long Rest, or with any spell slots you have. "
			f"<b>{ability}</b> is your spellcasting ability for it.<br>"
			"<b>Backfire.</b> When a creature you have cursed with <i>Hex</i> hits "
			f"you with an attack roll, it takes <b>{bonus}</b> Psychic damage (your "
			"Proficiency Bonus). Only once per turn per creature."
			f'<div class="spell">{Hex}</div>'
			)
		grant(
			char,
			Jinx.NAME,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"\U0001F311",
					"Hex",
					"1/LR",
					),
				Chip(
					"\U0001F4A5",
					"Backfire",
					f"{bonus} psychic",
					),
				),
			)


# The remaining seven Dark Gifts.  Published mechanics, unchanged names: only
# Mist Walker's text named Ravenloft geography, and that one already became
# Shadow Cast.  The "Ravenloft Campaign" prerequisite is dropped throughout.
# Every one pairs a real benefit with a price that fires on a natural 1.


class Aberrant_Anatomy(Dark_Gift):
	"""Exposure to something from outside has rearranged you."""

	NAME = "Aberrant Anatomy"
	DESCRIPTION = (
		"<b>Breathless.</b> You can hold your breath for 1 hour. "
		"<b>Extrasensory Perception.</b> You have proficiency in the Perception "
		"skill, if you lack it. You also gain Expertise in that skill. In "
		"addition, you have Blindsight with a range of 15 feet. "
		"<b>Warping Flesh.</b> Immediately after you make a D20 Test and roll a 1 "
		"on the d20, make a Constitution saving throw (DC 13 plus your Proficiency "
		"Bonus). On a failed save, you have the Stunned condition until the end of "
		"your next turn."
		)

	@Imprint
	def awaken(
			char,
			background_tag,
			):
		bonus = _proficiency_bonus(char)
		_grant_training(
			char,
			Aberrant_Anatomy,
			(
				"Perception",
				),
			source="Origin Feat — Dark Gift",
			rank=Training_Rank.EXPERTISE,
			background_tag=background_tag,
			)
		grant(
			char,
			Aberrant_Anatomy.NAME,
			"<b>Breathless.</b> You can hold your breath for <b>1 hour</b>.<br>"
			"<b>Extrasensory Perception.</b> You have proficiency and "
			"<b>Expertise</b> in <b>Perception</b>, and <b>Blindsight</b> out to "
			"<b>15 feet</b>.<br>"
			"<b>Warping Flesh.</b> Immediately after a D20 Test rolling a <b>1</b>, "
			f"make a Constitution save (<b>DC {13 + bonus}</b>) or have the "
			"<b>Stunned</b> condition until the end of your next turn.",
			source="Origin Feat — Dark Gift",
			chips=(Chip(
				"\U0001F441",
				"Blindsight",
				"15 ft",
				),),
			)

	@Record
	def aberrant_anatomy(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Aberrant_Anatomy,
			)

	@Post
	def Has_Aberrant_Anatomy_Training(
			char,
			):
		return bool( char.aberrant_anatomy.gains )


class Echoing_Soul(Dark_Gift):
	"""You remember a life that was not this one."""

	NAME = "Echoing Soul"
	DESCRIPTION = (
		"<b>Channelled Prowess.</b> You have proficiency in two skills of your "
		"choice. In addition, choose one skill you have proficiency in; you gain "
		"Expertise in that skill. Whenever you finish a Long Rest you can change "
		"your choice. "
		"<b>Inherent Tongues.</b> You know one additional language of your choice. "
		"<b>Intrusive Echoes.</b> Immediately after you make a D20 Test and roll a "
		"1 on the d20, make a Constitution saving throw (DC 13 plus your "
		"Proficiency Bonus). On a failed save, you have the Incapacitated condition "
		"until the end of your next turn, and your Speed is halved while so."
		)

	@Imprint
	def awaken(
			char,
			background_tag,
			):
		bonus = _proficiency_bonus(char)
		from AtlasLudus.Map_of_Languages import STANDARD_LANGUAGES

		untrained = tuple(
			skill
			for skill in SKILLS
			if Find_Training_Rank(
				char,
				skill,
				) is None
			)
		reserved = set(
			Reserved_Background_Training(
				background_tag
				)
			)
		pool = (
			untrained
			if len( untrained ) >= 2
			else SKILLS
			)
		pool = tuple(
			skill
			for skill in pool
			if skill not in reserved
			)

		if len( pool ) < 2:
			pool = tuple(
				skill
				for skill in SKILLS
				if skill not in reserved
				)
		dice = char.Dice_Bag(
			"feat.Echoing_Soul.training",
			version="2024",
			namespace="GenLegendTraining",
			)
		selected = tuple(
			dice.sample(
				list(
					pool
					),
				k=2,
				)
			)
		expertise_pool = tuple(
			skill
		for skill in SKILLS
		if (
			Find_Training_Rank(
				char,
				skill,
				) is Training_Rank.PROFICIENT
			or skill in selected
				)
			)
		expertise = char.Pick(
			expertise_pool,
			dice=dice,
			)
		gains = [
			Training_Grant(
				capability=skill,
				rank=(
					Training_Rank.EXPERTISE
					if skill == expertise
					else Training_Rank.PROFICIENT
					),
				)
			for skill in selected
			]

		if expertise not in selected:
			gains.append(
				Training_Grant(
					capability=expertise,
					rank=Training_Rank.EXPERTISE,
					)
				)

		gain = New_Training_Batch(
			char,
			Echoing_Soul,
			gains,
			source="Origin Feat — Dark Gift",
			)
		Commit_Training_Gain(
			char,
			gain,
			)
		first, second = (
			skill.name
			for skill in selected
			)
		tongue = char.Pick(list(STANDARD_LANGUAGES))
		_grant_language(char, tongue)
		grant(
			char,
			Echoing_Soul.NAME,
			"<b>Channelled Prowess.</b> You have proficiency in "
			f"<b>{first}</b> and "
			f"<b>{second}</b>, and <b>Expertise</b> in "
			f"<b>{expertise.name}</b>, changeable on a Long Rest.<br>"
			f"<b>Inherent Tongues.</b> You know <b>{tongue}</b>.<br>"
			"<b>Intrusive Echoes.</b> Immediately after a D20 Test rolling a "
			f"<b>1</b>, make a Constitution save (<b>DC {13 + bonus}</b>) or have "
			"the <b>Incapacitated</b> condition until the end of your next turn, "
			"with your Speed halved.",
			source="Origin Feat — Dark Gift",
			chips=(Chip(
				"\U0001F504",
				"Expertise",
				"swap on LR",
				),),
			)

	@Record
	def echoing_soul(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Echoing_Soul,
			)

	@Post
	def Has_Echoing_Soul_Training(
			char,
			):
		return bool( char.echoing_soul.gains )


class Living_Shadow(Dark_Gift):
	"""Your shadow moves on its own, and occasionally on its own behalf."""

	NAME = "Living Shadow"
	DESCRIPTION = (
		"<b>Grasping Shadow.</b> You learn the Mage Hand spell and can cast it "
		"without spell components. Intelligence, Wisdom, or Charisma is your "
		"spellcasting ability for it (choose when you select this feat). "
		"<b>Lengthened Strike.</b> When you make a melee attack roll as part of the "
		"Attack or Magic action on your turn, you can increase your reach for that "
		"attack by 10 feet. You can use this a number of times equal to your "
		"Proficiency Bonus, and you regain all expended uses when you finish a Long "
		"Rest. "
		"<b>Ominous Will.</b> Immediately after you make a D20 Test and roll a 1 on "
		"the d20, make a Wisdom saving throw (DC 13 plus your Proficiency Bonus). "
		"On a failed save, you have the Incapacitated condition until the start of "
		"your next turn, at which point you roll on the Shadow's Will table to "
		"determine what you do during that turn."
		)

	SHADOWS_WILL = (
		"<b>1</b> — You take no action and no Bonus Action, and you use all your "
		"movement to move in a random direction (1d4: 1 north, 2 east, 3 south, "
		"4 west).",
		"<b>2-6</b> — You do not move and take no Bonus Action, and you take the "
		"Attack action to make one melee attack against a random creature within "
		"reach. If none are within reach, you take no action.",
		"<b>7-8</b> — You have the Prone condition, and your turn ends.",
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import MageHand

		ability = _pick_mental_casting_ability(char)
		bonus = _proficiency_bonus(char)
		_grant_known_cantrip(char, MageHand)
		grant(
			char,
			Living_Shadow.NAME,
			f"<b>Grasping Shadow.</b> You know <i>Mage Hand</i> and cast it without "
			f"spell components. <b>{ability}</b> is your spellcasting ability for "
			"it.<br>"
			"<b>Lengthened Strike.</b> When you make a melee attack roll as part of "
			"the Attack or Magic action, you can increase your reach for that "
			f"attack by <b>10 feet</b>. <b>{bonus}</b> times per Long Rest.<br>"
			"<b>Ominous Will.</b> Immediately after a D20 Test rolling a <b>1</b>, "
			f"make a Wisdom save (<b>DC {13 + bonus}</b>) or have the "
			"<b>Incapacitated</b> condition until the start of your next turn, then "
			"roll <b>1d8</b> on the Shadow's Will table for what you do with that "
			"turn.<br>"
			+ "<br>".join(
				Living_Shadow.SHADOWS_WILL
				)
			+ f'<div class="spell">{MageHand}</div>',
			source="Origin Feat — Dark Gift",
			chips=(Chip(
				"\U0001F5A4",
				"Lengthened Strike",
				f"{bonus}/LR",
				),),
			)


class Touch_of_Death(Dark_Gift):
	"""Something in you is already partway across."""

	NAME = "Touch of Death"
	DESCRIPTION = (
		"<b>Death Touch.</b> You learn the Chill Touch spell and can cast it "
		"without spell components. Necrotic damage you deal with this spell ignores "
		"Resistance. Intelligence, Wisdom, or Charisma is your spellcasting ability "
		"for it (choose when you select this feat). "
		"<b>Pull of the Grave.</b> You have Disadvantage on Death Saving Throws."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import ChillTouch

		ability = _pick_mental_casting_ability(char)
		_grant_known_cantrip(char, ChillTouch)
		grant(
			char,
			Touch_of_Death.NAME,
			f"<b>Death Touch.</b> You know <i>Chill Touch</i> and cast it without "
			"spell components. Its Necrotic damage <b>ignores Resistance</b>. "
			f"<b>{ability}</b> is your spellcasting ability for it.<br>"
			"<b>Pull of the Grave.</b> You have <b>Disadvantage</b> on Death Saving "
			"Throws."
			f'<div class="spell">{ChillTouch}</div>',
			source="Origin Feat — Dark Gift",
			chips=(Chip(
				"\U0001F480",
				"Death Saves",
				"Disadvantage",
				),),
			)


class Watchers(Dark_Gift):
	"""Something is always looking, and it is not on your side."""

	NAME = "Watchers"
	DESCRIPTION = (
		"<b>Borrowed Eyes.</b> You always have the Beast Sense and Speak with "
		"Animals spells prepared. You can cast each without a spell slot once, and "
		"you must finish a Long Rest before casting it that way again. You can also "
		"cast them using spell slots you have. "
		"<b>Heightened Suspicion.</b> Whenever you take the Search action, you can "
		"roll 1d4 and add the number rolled to any ability check made as part of "
		"that action. "
		"<b>Incessant Watchers.</b> You have Disadvantage on saving throws made "
		"against the Scrying spell. In addition, immediately after you make a D20 "
		"Test and roll a 1 on the d20, make a Wisdom saving throw (DC 13 plus your "
		"Proficiency Bonus). On a failed save, you have Disadvantage on D20 Tests "
		"for 1 minute; you can repeat the save at the end of each of your turns, "
		"ending the effect early on a success."
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import BeastSense, SpeakwithAnimals

		bonus = _proficiency_bonus(char)
		_grant_known_cantrip(char, BeastSense)
		_grant_known_cantrip(char, SpeakwithAnimals)
		grant(
			char,
			Watchers.NAME,
			"<b>Borrowed Eyes.</b> You always have <i>Beast Sense</i> and <i>Speak "
			"with Animals</i> prepared, and can cast each once per Long Rest "
			"without a spell slot, or with slots you have.<br>"
			"<b>Heightened Suspicion.</b> When you take the <b>Search</b> action, "
			"roll <b>1d4</b> and add it to any ability check made as part of that "
			"action.<br>"
			"<b>Incessant Watchers.</b> <b>Disadvantage</b> on saves against "
			"<i>Scrying</i>. And immediately after a D20 Test rolling a <b>1</b>, "
			f"make a Wisdom save (<b>DC {13 + bonus}</b>) or have Disadvantage on "
			"D20 Tests for <b>1 minute</b>, repeating the save at the end of each "
			"of your turns."
			f'<div class="spell">{BeastSense}</div>'
			f'<div class="spell">{SpeakwithAnimals}</div>',
			source="Origin Feat — Dark Gift",
			chips=(Chip(
				"\U0001F50E",
				"Search",
				"+1d4",
				),),
			)


class Second_Skin(Dark_Gift):
	"""There is another shape in you, and it does not always wait to be asked."""

	NAME = "Second Skin"
	DESCRIPTION = (
		"<b>Alternate Form.</b> You always have the Alter Self spell prepared. You "
		"can cast it without a spell slot or spell components, and you must finish "
		"a Long Rest before you can cast it in this way again. You can also cast it "
		"using spell slots of the appropriate level. Intelligence, Wisdom, or "
		"Charisma is your spellcasting ability for it (choose when you select this "
		"feat). When you cast it without a spell slot using this feature, it "
		"doesn't require Concentration. "
		"<b>Involuntary Change.</b> Certain circumstances trigger your "
		"transformation involuntarily. After you experience your catalyst, at the "
		"start of your next turn make a Charisma saving throw (DC 13 plus your "
		"Proficiency Bonus). On a failed save, you immediately use Alternate Form "
		"to cast Alter Self without a spell slot. If you have already expended that "
		"use, you instead have the Stunned condition until the start of your next "
		"turn."
		)

	CATALYSTS = (
		"seeing a particular phase of the moon",
		"smelling the scent of a certain flower",
		"hearing temple bells ringing",
		"hearing a particular melody",
		"touching pure silver with your bare skin",
		"seeing someone who resembles a specific individual",
		)

	@Imprint
	def awaken(char):
		from AtlasMagia.Lodge_of_Spells import AlterSelf

		ability = _pick_mental_casting_ability(char)
		bonus = _proficiency_bonus(char)
		catalyst = char.Pick(list(Second_Skin.CATALYSTS))
		_grant_known_cantrip(char, AlterSelf)
		grant(
			char,
			Second_Skin.NAME,
			"<b>Alternate Form.</b> You always have <i>Alter Self</i> prepared, and "
			"can cast it once per Long Rest without a spell slot or components, or "
			f"with slots of the appropriate level. <b>{ability}</b> is your "
			"spellcasting ability for it. Cast without a slot, it does "
			"<b>not require Concentration</b>.<br>"
			f"<b>Involuntary Change.</b> Your catalyst is <b>{catalyst}</b>. After "
			"you experience it, at the start of your next turn make a Charisma save "
			f"(<b>DC {13 + bonus}</b>) or immediately cast <i>Alter Self</i> "
			"without a slot. If that use is already spent, you have the "
			"<b>Stunned</b> condition until the start of your next turn."
			f'<div class="spell">{AlterSelf}</div>',
			source="Origin Feat — Dark Gift",
			chips=(
				Chip(
					"\U0001F43A",
					"Alter Self",
					"1/LR",
					),
				Chip(
					"\U0001F567",
					"Catalyst",
					catalyst.split()[0].title(),
					),
				),
			)


class Symbiotic_Being(Dark_Gift):
	"""Something else lives in you, helps you, and is not on your errand."""

	NAME = "Symbiotic Being"
	SKILLS = (
		"Arcana",
		"Deception",
		"History",
		"Intimidation",
		"Insight",
		"Investigation",
		"Nature",
		"Religion",
		"Perception",
		"Persuasion",
		)
	DESCRIPTION = (
		"<b>Entwined Existence.</b> The symbiote can't be targeted. If you die, so "
		"does your symbiote; if you are returned to life, it also revives. "
		"<b>Second Mind.</b> You gain proficiency in one of the following skills: "
		"Arcana, Deception, History, Intimidation, Insight, Investigation, Nature, "
		"Religion, Perception, or Persuasion. You also know one additional language "
		"of your choice. "
		"<b>Sustained Symbiosis.</b> When you fail a saving throw, you can take a "
		"Reaction and expend one of your Hit Dice, adding the number rolled to the "
		"save and potentially turning the failure into a success. You can use this "
		"a number of times equal to your Proficiency Bonus, and you regain all "
		"expended uses when you finish a Long Rest. "
		"<b>Symbiotic Agenda.</b> Immediately after you make a D20 Test and roll a "
		"1 on the d20, make a Charisma saving throw (DC 13 plus your Proficiency "
		"Bonus). On a failed save, you have the Charmed condition for 1d12 hours, "
		"during which you must try to follow the symbiote's commands and further "
		"its goals as determined by the DM. Whenever you take damage you can repeat "
		"the save, ending the effect on a success."
		)

	@Imprint
	def awaken(
			char,
			background_tag,
			):
		from AtlasLudus.Map_of_Languages import STANDARD_LANGUAGES

		bonus = _proficiency_bonus(char)
		gain = _grant_training(
			char,
			Symbiotic_Being,
			Symbiotic_Being.SKILLS,
			source="Origin Feat — Dark Gift",
			background_tag=background_tag,
			)
		trained = gain.grants[ 0 ].capability.name
		tongue = char.Pick(list(STANDARD_LANGUAGES))
		_grant_language(char, tongue)
		grant(
			char,
			Symbiotic_Being.NAME,
			"<b>Entwined Existence.</b> The symbiote cannot be targeted. If you "
			"die, so does it; if you are returned to life, so is it.<br>"
			f"<b>Second Mind.</b> You have proficiency in "
			f"<b>{trained}</b> and know <b>{tongue}</b>.<br>"
			"<b>Sustained Symbiosis.</b> When you <b>fail</b> a saving throw, you "
			"can take a Reaction and expend one <b>Hit Die</b>, adding the roll to "
			f"the save. <b>{bonus}</b> times per Long Rest.<br>"
			"<b>Symbiotic Agenda.</b> Immediately after a D20 Test rolling a "
			f"<b>1</b>, make a Charisma save (<b>DC {13 + bonus}</b>) or have the "
			"<b>Charmed</b> condition for <b>1d12 hours</b>, following the "
			"symbiote's agenda. Repeat the save whenever you take damage.",
			source="Origin Feat — Dark Gift",
			chips=(Chip(
				"\U0001FAB1",
				"Sustained Symbiosis",
				f"{bonus}/LR",
				),),
			)

	@Record
	def symbiotic_being(
			char,
			) -> Feature_Training_Record:
		return New_Feature_Training_Record(
			char,
			Symbiotic_Being,
			)

	@Post
	def Has_Symbiotic_Being_Training(
			char,
			):
		return bool( char.symbiotic_being.gains )


# Based on the Zhentarim Ruffian feat
# source: Forgotten Realms: Heroes of Faerûn
class Strong_Arm(Origin_Feat):
	"""Bailiff's rebrand of Zhentarim Ruffian — official mechanics, new names."""

	NAME = "Strong Arm"
	DESCRIPTION = (
		"<b>Exploit Opening.</b> When you roll damage for an Opportunity Attack, you "
		"can roll the damage dice twice and use either roll against the target. "
		"<b>On My Mark.</b> If you have Heroic Inspiration when you roll Initiative, "
		"you can expend it to give yourself and your allies Advantage on that "
		"Initiative roll."
		)

	@Imprint
	def awaken(char):
		grant(
			char,
			Strong_Arm.NAME,
			Strong_Arm.DESCRIPTION,
			source="Origin Feat",
			)


# Real, implemented setting feats override their catalogued placeholders.
REAL_SETTING_FEATS = {
	"Agitator": Agitator,
	"Arcane Conduit": Arcane_Conduit,
	"Banner Bearer": Banner_Bearer,
	"Bastion": Bastion,
	"Field Lieutenant": Field_Lieutenant,
	"Strong Arm": Strong_Arm,
	"Dragon Cult Initiate": Dragon_Cult_Initiate,
	"Wildwarden": Wildwarden,
	"Mutant Aberration": Mutant_Aberration,
	"Sharp Eye": Sharp_Eye,
	"Spared": Spared,
	"Cupbearer": Cupbearer,
	"On a Roll": On_a_Roll,
	"Hard to Hold": Hard_to_Hold,
	"Aurora": Aurora,
	"Jinx": Jinx,
	"Aberrant Anatomy": Aberrant_Anatomy,
	"Echoing Soul": Echoing_Soul,
	"Living Shadow": Living_Shadow,
	"Second Skin": Second_Skin,
	"Symbiotic Being": Symbiotic_Being,
	"Touch of Death": Touch_of_Death,
	"Watchers": Watchers,
	"Gathered Whispers": Gathered_Whispers,
	"Shadow Cast": Shadow_Cast,
	}

OFFICIAL_ORIGIN_FEATS = {
	**{
		name: Make_Catalogued_Origin_Feat(
			name=name,
			source_title=source_title,
			source_url=_SOURCE_URLS[
				source_title
				],
			)
		for name, source_title in _CATALOGUE
		},
	**REAL_SETTING_FEATS,
	}

# Julio's call: a Human's Versatile draws from base feats *and* every setting
# Origin feat, Dark Gifts included.  ORIGIN_FEATS is mutated rather than
# shadowed so SpeciesKit sees the same pool without importing this module.
ORIGIN_FEATS.update(
	OFFICIAL_ORIGIN_FEATS
	)

BACKGROUND_ORIGIN_FEATS = {
	**ORIGIN_FEATS,
	**OFFICIAL_ORIGIN_FEATS,
	}


__all__ = (
	"BACKGROUND_ORIGIN_FEATS",
	"Make_Catalogued_Origin_Feat",
	"OFFICIAL_ORIGIN_FEATS",
	)
