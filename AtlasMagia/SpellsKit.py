'''
SpellsKit — the TOP implementation of the Spell class and its Tags.

XKit per Canon/Conventions.md: this module OWNS the Spell class and every
Tag that may be applied to one. Lodge_of_Spells stays what its name says —
a curated registry of Spell instances — and imports Spell from here.
(QST-0031.1; TagKit is the pinned upstream, see Canon/TagKit-Doctrine.md.)

The three Tag families, each rooted on Spell_Tag (whose Precondition
restricts every spell Tag to Spell targets — TagPreconditionError and a
full rollback on anything else):

	School        — the eight canonical schools of magic. Exclusive: a spell
	                bears exactly one (enforced by School.Single_School).
	                Applied by __init__ from the school text; its Record
	                writes the canonical spell.school string.
	Tradition     — Arcane / Divine / Primal (the One D&D playtest grouping,
	                adopted deliberately as a project choice, not core rules).
	                NOT exclusive: Cure Wounds is Divine and Primal at once.
	Spell_List    — "this spell appears on X's list", one Tag per caster
	                class the codebase deals spells to. Not exclusive.
	                Subclass lists (Eldritch Knight, Arcane Trickster…) do
	                NOT live here: each subclass mints its own Tag in its own
	                file, inheriting the class list it draws from
	                (e.g. class Eldritch_Knight_List(Wizard_List)).
	Spell_Level   — Cantrip / Level 1–9. Exclusive (Single_Level); applied
	                by __init__; its Record writes spell.level.
	Concentration — the spell demands concentration. Applied by __init__
	                from the flag or a "Concentration…" duration.
	Ritual        — castable as a ritual. New explicit input (ritual=True);
	                also sniffed from legacy casting_time marks
	                ("1 Action R", "(R)", "or Ritual").
	Legacy        — a pre-2024 5e spell with no 2024 printing (legacy=True).
	                Kept playable; the Tag marks the vintage, and legacy
	                variable names carry an _L suffix in the Lodge.

Membership reads as TagKit intends:
	Evocation(fireball)              # tag it (atomic; no-op if already)
	fireball in Evocation            # IS-check
	fireball in School               # any school at all
	for spell in Wizard_List: ...    # the live registry, for free
	"evocation" in fireball          # string probe, case-insensitive
'''

import re

from TopKit import Tag, Pre, Record

try:
	from AtlasScriptum.Map_of_Formats import Entry
except ImportError:
	raise


"""		Spell class    """
class Spell:
	# Roots for TagPaths()/Outline() trimming on tagged spells.
	TAG_ROOTS = ()  # filled after the Tag families are declared below

	def __init__(spell,
				 name="",
				 level=0,
				 school="",
				 casting_time="",
				 ranges = "",
				 duration = "",
				 components = "",
				 concentration = "",
				 definition = "",
				 ritual = False,
				 legacy = False):
		spell.name =  name
		spell.casting_time = casting_time
		spell.ranges = ranges
		spell.duration = duration
		spell.components = components
		spell.definition = definition
		#-- level, school, concentration and ritual are Tagged, not merely
		#-- stored: each helper applies the Tag whose Record writes the
		#-- attribute (falling back to a plain attribute when nothing maps)
		Assign_Level(spell, level)
		Assign_School(spell, school)
		Assign_Concentration(spell, concentration, duration)
		Assign_Ritual(spell, ritual, casting_time)
		Assign_Legacy(spell, legacy)

	def describe(spell):
		desc = spell.string
		return desc

	def __str__(spell):
		"""Plain Entry form. f"{spell:html}" / f"{spell:md}" pick richer shapes."""
		return spell.string

	def __format__(spell, spec):
		"""Dispatch f"{spell:html}" / f"{spell:md}" / f"{spell}" (plain)."""
		spec = (spec or "").strip().lower()
		if spec in ("html", "card"):    return spell.html()
		if spec in ("md", "markdown"):  return spell.md()
		if spec in ("", "s", "str", "plain"): return str(spell)
		raise ValueError(f"Unknown Spell format spec {spec!r} — use html, md, or plain")

	def html(spell):
		"""HTML spell card. Aliases: as_html; f"{spell:html}"."""
		desc = ""
		if spell.casting_time:   desc += f"<i>⟨{spell.casting_time}⟩</i><br>"
		if spell.ritual:         desc += "<i>(Ritual)</i><br>"
		if spell.concentration:  desc += f"<i>({spell.concentration}: </i>"
		if spell.duration:       desc += f"<i>({spell.duration})</i>"
		if spell.ranges:         desc += f"<br><i>>{spell.ranges}></i>"
		if spell.components:	 desc += f"<br><i>⦓{spell.components}⦔</i>"
		if spell.level == 0:
			level_text = "<b><p>Cantrip</b></p>"
		else:
			level_text = f"<b><p> Level {spell.level} Spell </b></p>"
		return f"""
		<h4 class="spell-title"> {spell.name}</h4>
		{level_text}
		<p class="spell-meta">{desc}</p>
		<p>
		{spell.definition }
		</p>
		"""

	def md(spell):
		"""Markdown spell sheet. Aliases: markdown, as_md; f"{spell:md}"."""
		level_text = "Cantrip" if spell.level == 0 else f"Level {spell.level}"
		meta = [level_text]
		if spell.school:         meta.append(str(spell.school))
		if spell.ritual:         meta.append("Ritual")
		if spell.concentration:  meta.append(str(spell.concentration))
		lines = [f"### {spell.name}", f"*{' · '.join(meta)}*", ""]
		if spell.casting_time:   lines.append(f"- **Casting Time:** {spell.casting_time}")
		if spell.ranges:         lines.append(f"- **Range:** {spell.ranges}")
		if spell.components:     lines.append(f"- **Components:** {spell.components}")
		if spell.duration:       lines.append(f"- **Duration:** {spell.duration}")
		lines.append("")
		lines.append(_html_to_md_lite(spell.definition))
		return "\n".join(lines)

	# Aliases are good and free — each name reads best in its own context.
	as_html = html
	as_md = md
	markdown = md

	@property
	def string(spell):

		name  = f"{spell.name}"
		desc  = f"{spell.school}"
		if spell.casting_time:   desc += f"({spell.casting_time})"
		if spell.concentration:  desc += f"⟨{spell.concentration}"
		if spell.duration:       desc += f"⟨{spell.duration}⟩"
		if spell.ranges:         desc += f"-{spell.ranges}"
		#-- The header line (school, time, range) only ever printed beside a
		#-- definition; a spell without one prints its name alone.
		if spell.definition:
			entry = Entry(title=name, rules=spell.definition, flavor=desc)
		else:
			entry = Entry(title=name)
		return f"{entry:html}"


def _html_to_md_lite(text):
	"""Definitions carry light HTML (<br>, <b>, <i>); fold it into markdown."""
	text = re.sub(r"<br\s*/?>", "\n", str(text))
	text = re.sub(r"</?b>", "**", text)
	text = re.sub(r"</?i>", "*", text)
	text = re.sub(r"</?(p|ul|li|div|h[1-6])[^>]*>", "\n", text)
	return re.sub(r"\n{3,}", "\n\n", text).strip()


def as_html(spell):
	"""Module-level alias of Spell.html, for callers that read better as functions."""
	return spell.html()


def as_md(spell):
	"""Module-level alias of Spell.md."""
	return spell.md()


"""		The root: every spell Tag is exclusive to Spell targets    """
class Spell_Tag(Tag):
	NAME = "Spell Tag"
	DESCRIPTION = "Root of every Tag a Spell may bear. Only Spell targets."

	@Pre
	def Spell_Only(agent):
		#-- the contract, not a hand-rolled assert: failure raises
		#-- TagPreconditionError and rolls the whole application back
		return isinstance(agent, Spell)


"""		Schools of magic — exactly one per spell    """
class School(Spell_Tag):
	NAME = "School"
	DESCRIPTION = "One of the eight schools of magic. A spell bears exactly one."
	ABSTRACT = True

	@Pre
	def Single_School(agent):
		#-- runs with the candidate school already active, so a second
		#-- school counts 2 and the application rolls back
		count = sum(1 for school in SCHOOLS.values() if agent in school)
		return count <= 1


class Abjuration(School):
	NAME = "Abjuration"
	DESCRIPTION = "Wards and protection: shields, banishments, dispels."

	@Record
	def school(spell):
		return "Abjuration"

class Conjuration(School):
	NAME = "Conjuration"
	DESCRIPTION = "Summoning and transportation: creatures, objects, teleports."

	@Record
	def school(spell):
		return "Conjuration"

class Divination(School):
	NAME = "Divination"
	DESCRIPTION = "Revelation: scrying, foresight, detection."

	@Record
	def school(spell):
		return "Divination"

class Enchantment(School):
	NAME = "Enchantment"
	DESCRIPTION = "Minds bent: charms, compulsions, sleep."

	@Record
	def school(spell):
		return "Enchantment"

class Evocation(School):
	NAME = "Evocation"
	DESCRIPTION = "Raw energy shaped: fire, lightning, radiant bolts."

	@Record
	def school(spell):
		return "Evocation"

class Illusion(School):
	NAME = "Illusion"
	DESCRIPTION = "Deceived senses: images, sounds, phantasms."

	@Record
	def school(spell):
		return "Illusion"

class Necromancy(School):
	NAME = "Necromancy"
	DESCRIPTION = "Life and death bartered: drains, undeath, false life."

	@Record
	def school(spell):
		return "Necromancy"

class Transmutation(School):
	NAME = "Transmutation"
	DESCRIPTION = "Matter reshaped: polymorphs, hastes, stone to mud."

	@Record
	def school(spell):
		return "Transmutation"


# Canonical name -> School Tag. The one lookup table for normalizing the
# Lodge's raw school strings (Assign_School strips whitespace and the
# Wildemount dunamancy suffixes D/DC/DG before consulting this).
SCHOOLS = {
	"Abjuration":    Abjuration,
	"Conjuration":   Conjuration,
	"Divination":    Divination,
	"Enchantment":   Enchantment,
	"Evocation":     Evocation,
	"Illusion":      Illusion,
	"Necromancy":    Necromancy,
	"Transmutation": Transmutation,
	}


"""		Spell levels — Cantrip and Levels 1 to 9, exactly one per spell    """
class Spell_Level(Spell_Tag):
	NAME = "Spell Level"
	DESCRIPTION = "The spell's level. A spell bears exactly one."
	ABSTRACT = True

	@Pre
	def Single_Level(agent):
		#-- same contract shape as Single_School: the candidate level is
		#-- already active when this runs, so a second level counts 2
		count = sum(1 for lvl in SPELL_LEVELS.values() if agent in lvl)
		return count <= 1


class Cantrip(Spell_Level):
	NAME = "Cantrip"
	DESCRIPTION = "Level 0 — at-will magic, no slot spent."

	@Record
	def level(spell):
		return 0

class Spell_Level_1(Spell_Level):
	NAME = "Level 1"

	@Record
	def level(spell):
		return 1

class Spell_Level_2(Spell_Level):
	NAME = "Level 2"

	@Record
	def level(spell):
		return 2

class Spell_Level_3(Spell_Level):
	NAME = "Level 3"

	@Record
	def level(spell):
		return 3

class Spell_Level_4(Spell_Level):
	NAME = "Level 4"

	@Record
	def level(spell):
		return 4

class Spell_Level_5(Spell_Level):
	NAME = "Level 5"

	@Record
	def level(spell):
		return 5

class Spell_Level_6(Spell_Level):
	NAME = "Level 6"

	@Record
	def level(spell):
		return 6

class Spell_Level_7(Spell_Level):
	NAME = "Level 7"

	@Record
	def level(spell):
		return 7

class Spell_Level_8(Spell_Level):
	NAME = "Level 8"

	@Record
	def level(spell):
		return 8

class Spell_Level_9(Spell_Level):
	NAME = "Level 9"

	@Record
	def level(spell):
		return 9


SPELL_LEVELS = {
	0: Cantrip,
	1: Spell_Level_1,
	2: Spell_Level_2,
	3: Spell_Level_3,
	4: Spell_Level_4,
	5: Spell_Level_5,
	6: Spell_Level_6,
	7: Spell_Level_7,
	8: Spell_Level_8,
	9: Spell_Level_9,
	}


"""		Casting demands — concentration and rituals    """
class Concentration(Spell_Tag):
	NAME = "Concentration"
	DESCRIPTION = "The spell demands concentration to sustain."

	@Record
	def concentration(spell):
		return "Concentration"

class Ritual(Spell_Tag):
	NAME = "Ritual"
	DESCRIPTION = "Castable as a ritual: +10 minutes, no slot spent."

	@Record
	def ritual(spell):
		return True

class Legacy(Spell_Tag):
	NAME = "Legacy"
	DESCRIPTION = (
		"A 5e spell from before the 2024 revision, with no 2024 printing. "
		"Kept playable; the Tag marks the vintage."
		)

	@Record
	def legacy(spell):
		return True


"""		Casting traditions — Arcane / Divine / Primal (One D&D playtest)    """
class Tradition(Spell_Tag):
	NAME = "Tradition"
	DESCRIPTION = (
		"Arcane, Divine, or Primal — the One D&D playtest's grouping, "
		"adopted as a project choice (UA, not core). A spell may bear "
		"more than one: Cure Wounds is Divine and Primal."
		)
	ABSTRACT = True


class Arcane(Tradition):
	NAME = "Arcane"
	DESCRIPTION = "The studied and innate lists: Bard, Sorcerer, Warlock, Wizard."

class Divine(Tradition):
	NAME = "Divine"
	DESCRIPTION = "The granted lists: Cleric, Paladin."

class Primal(Tradition):
	NAME = "Primal"
	DESCRIPTION = "The natural lists: Druid, Ranger."


TRADITIONS = {
	"Arcane": Arcane,
	"Divine": Divine,
	"Primal": Primal,
	}


"""		Class spell lists — who may learn it    """
class Spell_List(Spell_Tag):
	NAME = "Spell List"
	DESCRIPTION = "The spell appears on this class's (or subclass's) list."
	ABSTRACT = True


class Bard_List(Spell_List):
	NAME = "Bard"
	DESCRIPTION = "On the Bard spell list."

class Cleric_List(Spell_List):
	NAME = "Cleric"
	DESCRIPTION = "On the Cleric spell list."

class Druid_List(Spell_List):
	NAME = "Druid"
	DESCRIPTION = "On the Druid spell list."

class Paladin_List(Spell_List):
	NAME = "Paladin"
	DESCRIPTION = "On the Paladin spell list."

class Ranger_List(Spell_List):
	NAME = "Ranger"
	DESCRIPTION = "On the Ranger spell list."

class Sorcerer_List(Spell_List):
	NAME = "Sorcerer"
	DESCRIPTION = "On the Sorcerer spell list."

class Warlock_List(Spell_List):
	NAME = "Warlock"
	DESCRIPTION = "On the Warlock spell list."

class Wizard_List(Spell_List):
	NAME = "Wizard"
	DESCRIPTION = "On the Wizard spell list."


# Subclass lists (Eldritch Knight, Arcane Trickster, …) are NOT declared
# here: each subclass mints its own Tag in its own file, inheriting the
# class list it draws from — e.g. `class Eldritch_Knight_List(Wizard_List)`,
# so tagging a spell for the subclass also enrolls it on the parent list
# (TagKit auto-applies Bases). SpellsKit only owns the class-level lists.


# Class-list name -> Tag, keyed exactly as Grimoire_of_Spellcasters'
# SPELL_LISTS speaks today, so QST-0031.3's migration is a dict walk.
# Subclass keys ("Eldritch Knight", "Arcane Trickster") are registered by
# their own files when those Tags are minted.
SPELL_LISTS_TAGS = {
	"Bard":             Bard_List,
	"Cleric":           Cleric_List,
	"Druid":            Druid_List,
	"Paladin":          Paladin_List,
	"Ranger":           Ranger_List,
	"Sorcerer":         Sorcerer_List,
	"Warlock":          Warlock_List,
	"Wizard":           Wizard_List,
	}

# Which lists each tradition covers (the UA mapping, for QST-0031.3 to
# derive a spell's Tradition from its class lists). Subclass lists inherit
# their parent list's tradition through the Tag hierarchy — no row needed.
TRADITION_OF_LIST = {
	"Bard":             Arcane,
	"Sorcerer":         Arcane,
	"Warlock":          Arcane,
	"Wizard":           Arcane,
	"Cleric":           Divine,
	"Paladin":          Divine,
	"Druid":            Primal,
	"Ranger":           Primal,
	}


"""		The Assign helpers — __init__'s door from raw data to Tags    """
_DUNAMANCY_SUFFIX = re.compile(r"\s+(D|DC|DG)$")
_RITUAL_MARK = re.compile(r"\(R\)|\bor Ritual\b|\bR\s*$", re.IGNORECASE)


def Assign_Level(spell, level):
	"""Tag the spell's level; the Tag's Record writes spell.level."""
	try:
		tag = SPELL_LEVELS.get(int(level))
	except (TypeError, ValueError):
		tag = None
	if tag is not None:
		tag(spell)
	else:
		spell.level = level  #-- unknown levels keep the raw value, untagged


def Assign_School(spell, school):
	"""Tag the spell's school; the Tag's Record writes the canonical name.

	Raw Lodge strings arrive with trailing whitespace and Wildemount
	dunamancy suffixes ("Evocation DG", "Necromancy DC"). The base school
	is tagged; when a suffix was stripped the original survives on
	spell.school_raw so QST-0031.3 can still decide dunamancy's fate.
	"""
	text = str(school).strip() if school else ""
	base = _DUNAMANCY_SUFFIX.sub("", text)
	tag = SCHOOLS.get(base)
	if tag is not None:
		if base != text:
			spell.school_raw = text
		tag(spell)
	else:
		spell.school = school  #-- unknown schools keep the raw value, untagged


def Assign_Concentration(spell, concentration, duration=""):
	"""Tag concentration from the explicit flag or a 'Concentration…' duration."""
	demands = bool(str(concentration).strip()) or (
			"concentration" in str(duration).lower()
			)
	if demands:
		Concentration(spell)
	else:
		spell.concentration = concentration


def Assign_Ritual(spell, ritual, casting_time=""):
	"""Tag rituals from the explicit flag or legacy casting_time marks.

	The Lodge's older entries encode rituals inside casting_time —
	"1 Action R", "1 Minute (R)", "1 Action or Ritual" — so those marks
	are honored until the data itself is normalized ("1 Reaction" does
	not match: the R must stand alone at the end).
	"""
	if ritual is True or _RITUAL_MARK.search(str(casting_time or "")):
		Ritual(spell)
	else:
		spell.ritual = False


def Assign_Legacy(spell, legacy):
	"""Tag pre-2024 spells; the Tag's Record writes spell.legacy."""
	if legacy is True:
		Legacy(spell)
	else:
		spell.legacy = False


Spell.TAG_ROOTS = (Spell_Tag,)


if __name__ == "__main__":
	# Self-test / usage demo. Run:  python AtlasMagia/SpellsKit.py
	from TopKit import TagPreconditionError

	bolt = Spell(name="Test Bolt", level=1, school="Evocation", definition="zap")

	# 1) Tagging and membership, root included
	Evocation(bolt)
	assert bolt in Evocation, "tagged spell must be in its school"
	assert bolt in School, "school membership must climb to the family root"
	assert bolt in Spell_Tag, "…and to the kit root"
	assert isinstance(bolt, Spell), "the host class survives tagging"

	# 2) More axes compose on the same target
	Arcane(bolt)
	Wizard_List(bolt)
	Sorcerer_List(bolt)
	assert bolt in Arcane and bolt in Wizard_List and bolt in Sorcerer_List

	# 3) The registry, for free
	assert any(s is bolt for s in Evocation), "Field iteration finds the spell"
	assert any(s is bolt for s in Spell_List), "…on every family it bears"

	# 4) String probe (Tagged mixin)
	assert "evocation" in bolt and "wizard" in bolt

	# 5) Contract: only Spell targets
	class NotASpell:
		pass

	try:
		Evocation(NotASpell())
	except TagPreconditionError:
		pass
	else:
		raise AssertionError("a non-Spell must be rejected by Spell_Only")

	# 6) Contract: one school per spell (atomic rollback)
	try:
		Necromancy(bolt)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError("a second school must be rejected")
	assert bolt in Evocation and bolt not in Necromancy, "rollback must hold"

	# 7) Labels speak D&D, not Python
	assert Wizard_List.Label() == "Wizard"

	# 8) Records materialize as DATA on the instance, not methods:
	#    the @Record builder runs once at tagging; its return value is
	#    written into the instance __dict__ (TagKit _apply_record_values).
	assert bolt.level == 1 and type(bolt.level) is int
	assert object.__getattribute__(bolt, "__dict__")["level"] == 1
	assert bolt.school == "Evocation" and type(bolt.school) is str

	# 9) __init__ auto-tags every intrinsic axis
	brew = Spell(
		name="Test Brew", level=3, school="Transmutation DG ",
		casting_time="1 Minute R", duration="Concentration, up to 1 hour",
		definition="bubbles",
		)
	assert brew in Spell_Level_3 and brew.level == 3
	assert brew in Transmutation, "dunamancy suffix strips to the base school"
	assert brew.school_raw == "Transmutation DG", "…but the raw string survives"
	assert brew in Concentration, "sniffed from the duration text"
	assert brew in Ritual and brew.ritual is True, "sniffed from the legacy R mark"
	reaction = Spell(name="Test Retort", level=1, school="Evocation",
					 casting_time="1 Reaction", definition="riposte")
	assert reaction not in Ritual, "'1 Reaction' must not read as a ritual"

	# 10) One level per spell, same contract shape as schools
	try:
		Spell_Level_5(brew)
	except TagPreconditionError:
		pass
	else:
		raise AssertionError("a second level must be rejected")

	# 11) Subclass lists live in their subclass's file, inheriting the class
	#     list they draw from — Bases auto-apply, so the parent list follows.
	class Test_Knight_List(Wizard_List):
		NAME = "Test Knight"
	Test_Knight_List(brew)
	assert brew in Wizard_List, "subclass list enrolls the parent list too"

	# 12) The format spec picks the shape; plain stays plain
	assert format(bolt, "html") == bolt.html() == bolt.as_html()
	assert format(bolt, "md") == bolt.md() == bolt.markdown()
	assert f"{bolt}" == str(bolt)
	assert "### Test Brew" in brew.md() and "Ritual" in brew.md()
	assert "(Ritual)" in brew.html()

	print("SpellsKit self-test passed.")
