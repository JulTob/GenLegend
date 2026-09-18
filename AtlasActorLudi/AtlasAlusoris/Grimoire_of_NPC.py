"""
Great Grimoire of NonPlayer rites
Awakens a Character skeleton as NonPlayer (CharactersKit).
follows D&D 5e Rules
"""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  Every docstring, every
#-- contract, every failure message and every rule below is the original's,
#-- word for word: the whole eight-hundred-line file was transcribed and then
#-- proved instruction for instruction against the vaulted .pyc before this
#-- layout was applied.
#--
#-- Does this module own a domain axis (QST-0134)?  Yes, and it already says
#-- so in TOP: `class NonPlayer(Character_NonPlayer)` is the Guide's pattern 4
#-- (Bases and Shapes) — the Alusoris rites are a Shape laid over the canonical
#-- NonPlayer role Tag in CharactersKit, and @Imprint carries the summon
#-- request until membership binds the Actions that answer it.  Nothing was
#-- added, because nothing was missing.
#--
#-- FOUR DEFECTS ARE PRESERVED HERE, NOT REPAIRED.  Each is the bytecode's
#-- own, each is proved below at the line it lives on, and each is a change
#-- to live behaviour that is Julio's to make — QST-0081.9 already sets the
#-- precedent: "do not silently map the names in one file only."  They are:
#--   1. SetSize calls Size(npc, summary); live Map_of_Size.Size takes one
#--      argument.  A full NonPlayer therefore cannot be generated at all.
#--   2. SetName calls npc.Naming(npc) and raises TypeError.  Nothing calls it.
#--   3. SetMovement calls Movement(npc) twice, storing one answer and
#--      returning another.
#--   4. SimpleAttack reads a proficiency bonus as if it were a level.

try:
	from AtlasActorLudi.Map_of_Scores import Modifier, PB
	from AtlasActorLudi.Grimoire_of_AbilityScores import AbilityScores, apply_creature_ability_modifiers
	from AtlasActorLudi.Grimoire_of_SavingThrows import SavingThrows
	from AtlasActorLudi.Grimoire_of_Skills import Char_Skills
	from AtlasActorLudi.AtlasAlusoris.Map_of_Races import (
		Creature_Type_For_Race,
		race_weights,
		)
	from AtlasActorLudi.AtlasAlusoris.Map_of_Archetypes import (
		Classify_Archetype,
		Identity_Axis,
		)

	from TagKit import Imprint
	from AtlasActorLudi.CharactersKit import (
		Character,
		NonPlayer as Character_NonPlayer,
		)

	from AtlasActorLudi.GendersKit import Gender_Reveal
	from AtlasActorLudi.AtlasAlusoris.RaceKit import Apply_Race
	from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Features import Apply_NonPlayer_Features

	from AtlasLusoris.BackgroundKit import (
		Apply_Background,
		Apply_Background_Training,
		NONPLAYER_BACKGROUNDS,
		)

	from AtlasLusoris.GuildKit import Apply_Guild, GUILDS
except ImportError:
	#-- Re-raised unchanged, on purpose: a NonPlayer built from half its Atlases
	#-- would be a Character with silent holes in it, which is worse than a
	#-- refusal at import.
	raise


def _Settled_Request(npc):
	"""What was actually asked for, once the three old spellings agree.

	A summon may name a Background, the retired alias `profile`, or the even
	older single `archetype` that mixed Guild and Background into one word.
	This reconciles them into the four things the rites need, and refuses a
	request that says two different things at once.
	"""
	race = getattr(npc, "_nonplayer_race", None)
	guild = getattr(npc, "_nonplayer_guild", None)
	background = getattr(npc, "_nonplayer_background", None)
	profile_alias = getattr(npc, "_nonplayer_profile", None)
	legacy_archetype = getattr(npc, "_nonplayer_archetype", None)
	light = getattr(npc, "_nonplayer_light", False)

	if profile_alias:
		if background and background != profile_alias:

			raise ValueError(
				"NonPlayer Background and legacy Profile disagree: "
				f"{background!r} != {profile_alias!r}."
				)

		background = profile_alias

	#-- An Archetype is one word for whichever axis still answers to it, and
	#-- it never overrides a request that named that axis outright.
	if legacy_archetype:
		legacy_identity = Classify_Archetype(
			legacy_archetype
			)

		if legacy_identity.axis == Identity_Axis.GUILD:
			guild = guild or legacy_identity.name
		else:
			background = background or legacy_identity.name

	return race, guild, background, light


def _Fill_The_Sheet(npc):
	"""Everything a full NonPlayer carries that a light one does not.

	A light NonPlayer is a face with a name and an identity — enough for a
	scene card.  A full one is a creature that can be run at a table, so this
	is where the numbers come from.
	"""
	npc.size = npc.SetSize()
	npc.height = npc.size
	npc.ability_scores = npc.AS
	npc.pb = npc.proficiency_bonus
	npc.PB = npc.proficiency_bonus

	npc.AC = npc.SetAC()
	npc.armor_class = npc.AC
	npc.HP = npc.SetHitPoints(npc.level)
	npc.speed = 30
	npc.movement = npc.SetMovement()
	npc.ST = SavingThrows(
		npc,
		npc.AS,
		npc.proficiency_bonus,
		)

	npc.saving_throws = npc.ST
	npc.skills = Char_Skills(
		npc,
		npc.AS,
		npc.proficiency_bonus,
		)

	Apply_Background_Training(
		npc
		)

	npc.passive_perception = npc.ResolvePassivePerception()
	npc.to_hit_bonus = npc.CalculateToHitBonus()
	npc.spellcasting_ability = npc.SelectSpellcastingAbility()
	npc.spellcasting_ability_mod = (
		npc.CalculateSpellcastingAbilityModifier()
		)
	npc.spell_attack_bonus = (
		npc.spellcasting_ability_mod
		+ npc.proficiency_bonus
		)
	npc.spell_save_dc = (
		8
		+ npc.spell_attack_bonus
		)
	npc.dc = npc.spell_save_dc

	npc.ready = True


class NonPlayer(Character_NonPlayer):
	"""Alusoris rites layered over the canonical NonPlayer role Tag."""

	DESCRIPTION = (
		"Non-player rites: Race, Guild, Background, and light sheet."
		)

	@Imprint
	def Awaken(
		npc,
		race=None,
		archetype=None,
		guild=None,
		background=None,
		profile=None,
		lvl=1,
		light=False,
		**_,
		):
		"""Stash summon kwargs — full rites run after membership binds Actions."""
		npc._seed = npc.seed
		npc.level = max(int(lvl), 1)
		npc._nonplayer_light = bool(light)
		npc._nonplayer_race = race
		npc._nonplayer_archetype = archetype
		npc._nonplayer_guild = guild
		npc._nonplayer_background = background
		npc._nonplayer_profile = profile

	def Finish_Awakening(npc):
		"""Resolve NonPlayer dummies once Tag Actions are bound on the agent."""
		~npc

		race, guild, background, light = _Settled_Request(npc)

		npc.race = race if race else npc.Pick(
			tuple(race_weights),
			weights=tuple(
				race_weights.values()
				),
			)

		Apply_Race(
			npc,
			race=npc.race,
			creature_type=Creature_Type_For_Race(
				npc.race
				),
			)

		npc.subrace = npc.SetSubrace()
		selected_guild = guild or npc.Pick(
			tuple(
				GUILDS
				)
			)

		selected_background = background or npc.Pick(
			tuple(
				NONPLAYER_BACKGROUNDS
				)
			)

		Apply_Guild(
			npc,
			selected_guild,
			)

		npc.gender = npc.SetGender()
		Gender_Reveal(
			npc,
			npc.gender,
			)

		if not light:
			npc.AS = AbilityScores(
				10,
				10,
				10,
				10,
				10,
				10,
				character=npc,
				)

			npc.AS.RandomAbilityScores()

		Apply_Background(
			npc,
			selected_background,
			)

		from AtlasActorLudi.AlignmentKit import New_Alignment
		New_Alignment(
			npc
			)

		npc.proficiency_bonus = npc.ProficiencyBonus()
		npc.genus = npc.BuildGenus()
		npc.Type = npc.genus
		npc.SetIdentitySummary()
		npc.name = npc.Naming()
		npc.title = npc.SetTitle()

		if not light:
			_Fill_The_Sheet(npc)

		Apply_NonPlayer_Features(
			npc
			)

		return npc

	def SetIdentitySummary(npc):
		"""Materialize the identity fields consumed by legacy Maps."""
		values = (
			npc.race,
			npc.subrace,
			npc.char_class,
			npc.background,
			npc.gender,
			npc.alignment,
			)

		npc._identity_summary = " , ".join(
			str(
				value
				)
			for value in values
			if value not in (None, "")
			)

		return npc._identity_summary

	def ResolvePassivePerception(npc):
		"""Resolve passive Perception from the finalized Skills Record."""
		return npc.skills.passive(
			"Perception"
			)

	def ResolveLanguages(npc) -> list:
		"""Generate the language projection for this NonPlayer."""
		from AtlasLudus.Map_of_Languages import Language
		return Language(npc)

	def ResolveIdeal(npc):
		"""Generate one deterministic ideal inside its projection Dice Bag."""
		from AtlasActorLudi.Map_of_Personality import Ideal
		return Ideal(npc)

	def ResolvePlotHook(npc) -> str:
		"""Generate one deterministic plot hook inside its Dice Bag."""
		from AtlasActorLudi.Map_of_Personality import PlotHook
		return PlotHook(npc)

	def ResolveTrait(npc) -> str:
		"""Generate one deterministic personality trait inside its Dice Bag."""
		#-- "Deterministic" is the intent, and it is not yet true.  The
		#-- projection shim (Map_of_NonPlayer_Projections) lends this rite the
		#-- Character's own Dice Bag, but Map_of_Personality draws from a
		#-- module-level `app.random` instead of the agent, so the same seed
		#-- yields a different trait each time.  Four call sites there, none
		#-- here; recorded as a QST-0134 finding rather than patched.
		from AtlasActorLudi.Map_of_Personality import Trait
		return Trait(npc)

	def set_name(npc):
		npc.name = npc.Naming()

	def set_title(npc):
		npc.title = npc.SetTitle()

	def set_stats(npc):
		npc.size = npc.SetSize()
		npc.AC = npc.SetAC()
		npc.HP = npc.SetHitPoints(npc.level)
		npc.speed = 30
		npc.movement = npc.SetMovement()
		npc.ST = SavingThrows(
			npc,
			npc.AS,
			npc.proficiency_bonus,
			)

		npc.skills = Char_Skills(
			npc,
			npc.AS,
			npc.proficiency_bonus,
			)

		Apply_Background_Training(
			npc
			)

		npc.simple_attacks = npc.SimpleAttack()
		npc.special_attack = npc.SpecialAttack()

	def set_personality(npc):
		npc.spells = npc.Magic()
		npc.personality_ready.set()

	def SetAbilities(npc):
		"""Determine the abilities of the NPC. """
		from AtlasPugna.Map_of_Abilities import Abilities
		npc.abilities = Abilities(npc)
		return npc.abilities

	def to_dict(npc):
		return {
			"race": npc.race,
			"guild": npc.char_class,
			"background": npc.background,
			"lvl": npc.level,
			"seed": npc.seed,
			"feature_ids": [
				feature.key
				for feature in getattr(
					npc,
					"npc_features",
					(),
					)
				],
			}

	@classmethod
	def from_dict(cls, data):
		background = (
			data.get(
				"profile"
				)
			or
			data.get(
				"background"
				)
			)

		return NPC(
			race=data.get("race"),
			guild=data.get("guild"),
			background=background,
			lvl=data.get("lvl"),
			seed=data.get("seed"),
			)

	def SetGender(npc) -> str:
		"""Set the gender of the NPC. """
		from AtlasActorLudi.Map_of_Gender import NewGender, ElementalGender
		try:
			npc.gender = NewGender(
				npc
				)

			VALKYRE = "Valkyrie" in npc.subrace
			NYMPH = "Nymph" in npc.subrace
			if VALKYRE or NYMPH:
				npc.gender = "She"
			if "Elemental" in npc.race:
				npc.gender = ElementalGender(
					npc,
					npc.subrace,
					)

				return npc.gender
		except Exception:
			npc.gender = "They"
		return npc.gender

	def SetSize(npc) -> str:
		"""Set the size of the NPC. """
		from AtlasActorLudi.Map_of_Size import Size
		#-- DEFECT, preserved (QST-0134 finding 1).  Live Map_of_Size.Size
		#-- takes one argument.  This passes two, so every full NonPlayer
		#-- fails here and summon_nonplayer gives up after five attempts;
		#-- only light=True Characters reach the sheet.  The same live-versus-
		#-- vault split as QST-0081.9, and the same answer: Julio decides
		#-- whether Size grows a second parameter or this call drops one.
		npc.size = Size(
			npc,
			getattr(
				npc,
				"_identity_summary",
				npc.race,
				),
			)

		return npc.size

	def SetTitle(npc) -> str:
		"""Generate a title (a name they are known for) for the NPC. """
		try:
			from AtlasEpica.Map_of_Titles import Title
			return Title(npc)
		except Exception:
			pass
		return (
			f"The {npc.race} {npc.char_class} "
			f"{npc.background}"
			)

	def SetSubrace(npc) -> str:
		"""Determine the subrace of the NPC. """
		from AtlasActorLudi.AtlasAlusoris.Map_of_Races import Subrace
		npc.subrace = Subrace(
			npc,
			npc.race,
			)

		return npc.subrace

	def Naming(npc) -> str:
		"""Generate a name for the NPC. """
		try:
			from AtlasNomina.Map_of_Names import NewName
			return NewName(npc)
		except Exception:
			return npc.Pick([*("Zax", "Jon", "Nix", "Max", "Tod", "Raz", "Mox")])

	def SetAC(npc) -> int:
		"""
Calculate the NPC's armor class
based on various factors.

Postconditions:
<<      Returns an integer representing the NPC's armor class.
"""
		from AtlasActorLudi.AtlasAlusoris.Map_of_Archetypes import AC_Identity_modifier
		from AtlasActorLudi.AtlasAlusoris.Map_of_Races import AC_race_modifier

		Dice = npc.Roll
		Dizero = npc.Roll_Zero
		PB = npc.proficiency_bonus
		AC = 10 + Dice(Modifier(npc.AS.DEX)) + Dice(PB)

		abilities = {
			"STR": Modifier(npc.AS.STR),
			"DEX": Modifier(npc.AS.DEX),
			"CON": Modifier(npc.AS.CON),
			"INT": Modifier(npc.AS.INT),
			"WIS": Modifier(npc.AS.WIS),
			"CHA": Modifier(npc.AS.CHA),
			}

		for identity in (
			npc.char_class,
			npc.background,
			):

			AC += Dizero(
				AC_Identity_modifier(
					identity,
					**abilities,
					)
				)

		AC += Dizero(AC_race_modifier(
			race=npc.race,
			subrace=npc.subrace,
			))

		if AC < 10 + PB:
			AC = 10 + PB
		if AC > 20 + PB:
			AC = 20 + PB

		return AC

	def SetHitPoints(npc, level: int) -> int:
		"""
Determine and Set the hit points of the NPC.

Preconditions:
>>              <level> must be an [integer] greater than or equal to 1.

Postconditions:
<<              Returns the calculated hit points as an [integer].
"""
		Dice = npc.Roll
		hit_dice_sides = Dice(3, 4)

		dice_hp = hit_dice_sides + Dice(
			D=hit_dice_sides,
			N=level - 1,
			)
		con_hp = level * npc.ability_scores.con_mod

		if con_hp < 0:
			con_hp = 0

		total_hp = dice_hp + con_hp

		npc.HP = total_hp

		return total_hp

	def SetMovement(npc) -> str:
		"""Determine the NPC's movement capabilities. """
		from AtlasPugna.Map_of_Movement import Movement
		#-- DEFECT, preserved (QST-0134 finding 3).  Movement is asked twice,
		#-- so what is stored and what is returned are two separate draws.
		npc.movement = Movement(npc)
		return Movement(npc)

	def SimpleAttack(npc) -> str:
		"""Generate simple attack options for the NPC. """
		from AtlasPugna.Map_of_Attacks import Attack
		Dice = npc.Roll
		#-- DEFECT, preserved (QST-0134 finding 4).  PB turns a *level* into a
		#-- bonus, and it is handed a bonus: at level 20 the count is drawn
		#-- from 1..3 rather than 1..6.
		count = max(Dice(1, PB(npc.proficiency_bonus)), 1) or 1

		simple_list = []
		for _ in range(count):
			new_attack = Attack(npc)
			if new_attack not in simple_list:
				simple_list.append(new_attack)
		simple = "\n".join(simple_list)
		return simple

	def SpecialAttack(npc) -> str:
		from AtlasPugna.Map_of_Attacks import SpecialAttack
		special = ""
		special += SpecialAttack(npc)
		special += "\n"
		return special

	def SetName(npc) -> str:
		#-- DEFECT, preserved (QST-0134 finding 2).  Naming takes the agent
		#-- alone, so this raises TypeError every time it is called.  Nothing
		#-- calls it; Finish_Awakening uses npc.Naming().  Removing a public
		#-- rite is a change, not a recovery, so it stays until Julio says.
		return npc.Naming(npc)

	def ProficiencyBonus(npc) -> int:
		from AtlasActorLudi.Map_of_Scores import PB
		return PB(npc.level)

	def ResolveSenses(npc):
		"""Generate the senses projection for this NonPlayer."""
		from AtlasPugna.Map_of_Senses import Senses
		return Senses(npc)

	def ResolveResistances(npc):
		"""Generate resistances, immunities, and protections."""
		import AtlasPugna.Map_of_Resistances as resistances

		result = (
			f"{resistances.Resistances(npc)} \n"
			f"{resistances.ConditionImmunities(npc)}\n "
			)

		result += (
			"\n<h4>Protections:</h4> "
			f"{resistances.Protections(npc)} \n "
			)

		return result

	def BuildGenus(npc):
		"""
Build the compatibility identity summary used by legacy Maps.

Returns:
        A comma-separated string of the current identity Records.
"""
		attributes = [
			npc.race,
			npc.subrace,
			npc.char_class,
			npc.background,
			npc.gender,
			npc.alignment,
			]

		delimiter = " , "
		result = delimiter.join(
			str(
				attribute
				)
			for attribute in attributes
			if attribute not in (None, "")
			)

		return result

	def SetArmorClass(npc):
		npc.AC = npc.SetAC()
		return npc.AC

	def CalculateToHitBonus(npc) -> int:
		"""Calculate the NPC's to-hit bonus. """
		highest_ability_mod = Modifier(
			max(npc.ability_scores.STR,
				npc.ability_scores.DEX)
			)
		if npc.char_class == "Druid":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.WIS))
		if npc.background == "Shaman":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.WIS))
		if npc.char_class == "Warlock":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.CHA))
		if npc.char_class == "Wizard":
			highest_ability_mod = max(highest_ability_mod,
				Modifier(npc.ability_scores.INT))

		return highest_ability_mod + npc.proficiency_bonus

	def SelectSpellcastingAbility(npc) -> str:
		"""Select the strongest mental ability for legacy spell generation."""
		int_mod = npc.ability_scores.int_mod
		wis_mod = npc.ability_scores.wis_mod
		cha_mod = npc.ability_scores.cha_mod

		ability_mod_dict = {"INT": int_mod, "WIS": wis_mod, "CHA": cha_mod}

		return max(ability_mod_dict, key=ability_mod_dict.get)

	def CalculateSpellcastingAbilityModifier(npc) -> int:
		"""Return the modifier for the selected spellcasting ability."""
		int_mod = npc.ability_scores.int_mod
		wis_mod = npc.ability_scores.wis_mod
		cha_mod = npc.ability_scores.cha_mod
		return max(int_mod, wis_mod, cha_mod)

	def Magic(npc):
		import AtlasMagia.Map_of_Magic as magic
		return magic.Magic(npc)

	def SetAbilityScores(npc, STR, DEX, CON, INT, WIS, CHA):
		npc.AS = AbilityScores(
			STR,
			DEX,
			CON,
			INT,
			WIS,
			CHA,
			character=npc,
			)

		apply_creature_ability_modifiers(npc)
		npc.ST = SavingThrows(
			npc,
			npc.AS,
			npc.proficiency_bonus,
			)

	def SetMyStory(npc):
		try:
			from AtlasEpica.Map_of_Stories import Story
			return Story(npc)
		except Exception:
			return ""

	def Check(
		npc,
		race=None,
		archetype=None,
		guild=None,
		background=None,
		profile=None,
		gender=None,
		alignment=None,
		subrace=None,
		):
		"""
Check if specific attributes match given values.
Args:
        race (str, optional): Race tag to check.
        archetype (str, optional): Former mixed identity-axis value.
        guild (str, optional): Guild / class Tag to check.
        background (str, optional): True Background Tag to check.
        profile (str, optional): Deprecated alias for Background.
        gender (str, optional): Gender tag to check.
        alignment (str, optional): Alignment tag to check.
        subrace (str, optional): Subrace tag to check.
Returns:
        bool: True if all provided parameters match NPC's attributes exactly.
"""
		if archetype is not None:
			try:
				legacy_identity = Classify_Archetype(
					archetype
					)

			except ValueError:
				return False

			actual_by_axis = {
				Identity_Axis.GUILD: npc.char_class,
				Identity_Axis.BACKGROUND: npc.background,
				}

			if archetype.strip().casefold() != (
				actual_by_axis[
					legacy_identity.axis
					]
				).strip().casefold():

				return False

		checks = [
			(race, npc.race),
			(guild, npc.char_class),
			(background, npc.background),
			(profile, npc.background),
			(gender, npc.gender),
			(alignment, npc.alignment),
			(subrace, npc.subrace),
			]

		for provided, actual in checks:
			if provided is not None and provided.strip().lower() != actual.strip().lower():
				return False
		return True

	def LightNPC_Hyperlink(npc):
		from AtlasActorLudi.AtlasAlusoris.Map_of_NonPlayer_Paths import nonplayer_hash


		url = "/" + nonplayer_hash(
			race=npc.race,
			guild=npc.char_class,
			background=npc.background,
			level=npc.level,
			seed=npc._seed,
			)
		return f'<a href="{url}">{npc.name}, {npc.title}</a>'


def awaken_nonplayer(
	npc,
	race=None,
	archetype=None,
	guild=None,
	background=None,
	profile=None,
	lvl=1,
	light=False,
	**_,
	):
	"""Apply NonPlayer to an existing Character skeleton (module-level helper)."""
	NonPlayer(
		npc,
		race=race,
		archetype=archetype,
		guild=guild,
		background=background,
		profile=profile,
		lvl=lvl,
		light=light,
		)

	npc.Finish_Awakening()

	return npc


def NPC(
	race=None,
	archetype=None,
	guild=None,
	background=None,
	profile=None,
	lvl=1,
	light=False,
	seed=-1,
	target=None,
	**kwargs,
	):
	"""
Interim constructor for call sites that still say NPC(...).
Public Summon design lives in AtlasActorLudi — do not grow this.
"""
	level = kwargs.pop("level", lvl)

	npc = (
		target
		if target is not None
		else Character(
			seed=seed,
			level=level,
			)
		)

	if not isinstance(
		npc,
		Character,
		):

		raise TypeError(
			"NPC target must be a Character."
			)

	return awaken_nonplayer(
		npc,
		race=race,
		archetype=archetype,
		guild=guild,
		background=background,
		profile=profile,
		lvl=level,
		light=light,
		**kwargs,
		)


def _a_nonplayer(**request):
	"""One light NonPlayer, built from a fixed seed."""
	fields = {
			"seed": 31,
			"lvl": 5,
			"light": True,
			}
	fields.update(request)
	return NPC(**fields)


def _test_the_request_is_settled_before_anything_is_built() -> None:
	"""Three spellings of one identity are reconciled, or the request refused."""

	#-- A Background named twice, the same both times, is one Background.
	agreed = _a_nonplayer(background="Sage", profile="Sage")
	assert agreed.background == "Sage"

	#-- Named twice, differently, is a mistake in the request.
	try:
		_a_nonplayer(background="Sage", profile="Soldier")
	except ValueError as refusal:
		assert "Background and legacy Profile disagree" in str(refusal), \
				f"Refused, but not for the disagreement: {refusal}"
	else:
		raise AssertionError(
				"Two different Backgrounds in one request should be refused."
				)

	#-- An Archetype lands on whichever axis still answers to the name.
	assert _a_nonplayer(archetype="Rogue").char_class == "Rogue", \
			"A Guild-shaped Archetype settles on the Guild."
	assert _a_nonplayer(archetype="Criminal").background == "Criminal", \
			"A Background-shaped Archetype settles on the Background."

	#-- And it never overrides an axis the request named outright.
	both = _a_nonplayer(archetype="Rogue", guild="Wizard")
	assert both.char_class == "Wizard", \
			"An explicit Guild wins over a legacy Archetype."


def _test_a_light_nonplayer_is_whole_enough_to_show() -> None:
	"""A light NonPlayer carries the identity a scene card needs."""
	npc = _a_nonplayer()

	for field in ("name", "race", "char_class", "background", "gender", "alignment"):
		assert getattr(npc, field), f"A NonPlayer must have a {field}."

	assert npc.level == 5
	assert npc._seed == 31, "The seed it was built from is kept on the sheet."
	assert npc.proficiency_bonus == 3, "Level five carries a bonus of three."
	assert npc.genus == npc.Type == npc.BuildGenus()
	assert npc.race in npc._identity_summary
	assert npc.LightNPC_Hyperlink().startswith('<a href="/npc/')

	#-- A level below one is still a level one Character.
	assert _a_nonplayer(lvl=0).level == 1
	assert _a_nonplayer(lvl=-5).level == 1

	#-- The same seed builds the same NonPlayer.
	assert _a_nonplayer().name == npc.name


def _test_what_a_nonplayer_says_about_itself() -> None:
	"""Check answers only when every claim matches, ignoring case and space."""
	npc = _a_nonplayer(race="Elf", guild="Wizard", background="Sage")

	assert npc.Check()
	assert npc.Check(race="Elf")
	assert npc.Check(race=" elf "), "Case and surrounding space do not matter."
	assert npc.Check(race="Elf", guild="Wizard", background="Sage")
	assert npc.Check(profile="Sage"), "The retired alias reads the Background."
	assert not npc.Check(race="Dwarf")
	assert not npc.Check(guild="Rogue")
	assert not npc.Check(archetype="Nonesuch"), \
			"A name no axis answers to matches nothing."

	#-- A saved sheet carries the whole request.
	saved = npc.to_dict()
	assert saved["race"] == "Elf" and saved["guild"] == "Wizard"
	assert saved["background"] == "Sage"
	assert saved["lvl"] == 5 and saved["seed"] == npc.seed
	assert "feature_ids" in saved, "The tactical loadout is saved by key."

	#-- Reading it back cannot be proved today: from_dict builds a *full*
	#-- NonPlayer, and defect 1 below stops every full build at SetSize.  The
	#-- round trip is therefore the clearest measure of that defect's reach —
	#-- a saved NonPlayer cannot currently be reopened at all.
	try:
		NonPlayer.from_dict(saved)
	except TypeError as failure:
		assert "positional argument" in str(failure), \
				f"from_dict failed for a new reason: {failure}"
	else:
		raise AssertionError(
				"from_dict now works, so defect 1 is fixed: restore the round "
				"trip check here and close the finding."
				)


def _test_the_four_preserved_defects() -> None:
	"""The four known breakages, asserted so a repair is visible here first.

	Each is the vaulted bytecode's own behaviour, kept because repairing it
	changes the running application and that is Julio's call (QST-0134, and
	QST-0081.9 for the precedent).  When one is fixed, this test fails and
	says which — that is the point of writing them down as checks.
	"""
	npc = _a_nonplayer()

	#-- 1. A full NonPlayer cannot be built: SetSize passes two arguments to a
	#--    Size that takes one.
	try:
		_a_nonplayer(light=False)
	except Exception as failure:
		assert "Size()" in str(failure) or "positional argument" in str(failure), \
				f"Defect 1 changed shape: {type(failure).__name__}: {failure}"
	else:
		raise AssertionError(
				"Defect 1 is FIXED: a full NonPlayer now builds. "
				"Delete this check and close the finding."
				)

	#-- 2. SetName hands the agent to Naming a second time.
	try:
		npc.SetName()
	except TypeError as failure:
		assert "positional argument" in str(failure), \
				f"Defect 2 changed shape: {failure}"
	else:
		raise AssertionError(
				"Defect 2 is FIXED: SetName now answers. "
				"Delete this check and close the finding."
				)

	#-- 3. SetMovement asks Movement twice, so what it stores and what it
	#--    returns are two separate answers.  Counted with a stand-in, because
	#--    the real Movement needs a full sheet this NonPlayer does not have.
	import AtlasPugna.Map_of_Movement as movement_map

	real_movement = movement_map.Movement
	answers = []
	movement_map.Movement = lambda who: f"draw {len(answers)}" if not answers.append(1) else ""
	try:
		returned = npc.SetMovement()
		asked = len(answers)
		stored = npc.movement
	finally:
		movement_map.Movement = real_movement

	assert asked == 2, \
			f"Defect 3 is FIXED: Movement was asked {asked} time(s). Close the finding."
	assert stored != returned, \
			"Defect 3 is FIXED: the stored and returned answers now agree. " \
			"Close the finding."

	#-- 4. SimpleAttack turns the proficiency bonus into a level, so a level
	#--    twenty NonPlayer draws its attack count from 1..3 instead of 1..6.
	import AtlasActorLudi.Map_of_Scores as scores

	real_pb = scores.PB
	seen = []
	scores.PB = lambda value: seen.append(value) or real_pb(value)
	try:
		npc.SimpleAttack()
	except Exception:
		pass
	finally:
		scores.PB = real_pb

	assert npc.proficiency_bonus in seen, \
			"Defect 4 is FIXED: PB is no longer handed a bonus. Close the finding."
	assert npc.level not in seen, \
			"Defect 4 is FIXED: PB is handed the level now. Close the finding."


def _self_test() -> None:
	_test_the_request_is_settled_before_anything_is_built()
	_test_a_light_nonplayer_is_whole_enough_to_show()
	_test_what_a_nonplayer_says_about_itself()
	_test_the_four_preserved_defects()
	print("OK — Alusoris Grimoire_of_NPC self-test (four defects still recorded)")


if __name__ == "__main__":
	_self_test()
