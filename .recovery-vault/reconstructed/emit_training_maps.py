"""Emit the six remaining AtlasOfTraining maps from vault Tags."""

from __future__ import annotations

import marshal
import re
import sys
import types
from pathlib import Path

ROOT = Path("/Users/tbs/Desktop/DnD")
VAULT = ROOT / ".recovery-vault" / "training"
OUT = ROOT / "AtlasLusoris" / "AtlasOfTraining"
T = "\t"

sys.path.insert(0, str(ROOT))
import AtlasLusoris.TrainingKit  # noqa: E402


DOCS = {
		"Artificer": '''\
"""
Artificer Training Tags — 2024 core Guild lessons + all Specialties.

Thought pattern
	1. Core lessons belong to the Artificer Guild (no Specialty).
	2. Specialty lessons set path=… and awaken only for that Specialty.
	3. Infusion counts live as Chips.
	4. Artificer has no legacy Progression — all lessons live here.
"""
''',
		"Bard": '''\
"""
Bard Training Tags — 2024 PHB core + all Colleges.

Thought pattern
	1. Core lessons belong to the Bard Guild (no College).
	2. College lessons set ``path=…`` and awaken only for that College.
	3. Bardic Inspiration die is a Chip + callable Entry — not separate.
	4. ASI / Epic Boon picks stay on legacy Progression.
"""
''',
		"Monk": '''\
"""
Monk Training Tags — 2024 PHB core + all Monk Traditions.

Thought pattern
	1. Core lessons belong to the Monk Guild (no path).
	2. Tradition lessons set ``path=…`` and awaken only for that Tradition.
	3. Numbers (Martial Arts die, Focus Points, Unarmored Movement speed)
	   live as Chips and in callable Entries.
	4. ASI / Epic Boon stay on legacy Progression.
	5. Speed bonuses stay in legacy (character mutation).
"""
''',
		"Sorcerer": '''\
"""
Sorcerer Training Tags — 2024 PHB core + all Origins.

Thought pattern
	1. Core lessons belong to the Sorcerer Guild (no Origin).
	2. Origin lessons set path=… and awaken only for that Origin.
	3. Sorcery Point counts live as Chips and callables.
	4. ASI / Epic Boon stay on legacy Progression.
"""
''',
		"Warlock": '''\
"""
Warlock Training Tags — 2024 PHB core + all Patrons.

Thought pattern
	1. Core lessons belong to the Warlock Guild (no Patron).
	2. Patron lessons set path=… and awaken only for that Patron.
	3. Invocation counts and Pact Magic slots live as Chips and callables.
	4. ASI / Epic Boon stay on legacy Progression.
"""
''',
		"Wizard": '''\
"""
Wizard Training Tags — 2024 PHB core + all Arcane Traditions.

Thought pattern
	1. Core lessons belong to the Wizard Guild (no Tradition).
	2. Tradition lessons set path=… and awaken only for that Tradition.
	3. Recovery levels and Portent dice live as Chips.
	4. ASI / Epic Boon stay on legacy Progression.
"""
''',
		}

IMPORTS = {
		"Artificer": (
			"from AtlasLusoris.TrainingKit import Make_Training\n"
			"from AtlasVenustas import Chip"
			),
		"Bard": (
			"from AtlasLusoris.TrainingKit import Make_Training\n"
			"from AtlasVenustas import Chip"
			),
		"Monk": (
			"from AtlasLusoris.TrainingKit import Make_Training\n"
			"from AtlasVenustas import Chip"
			),
		"Sorcerer": (
			"from AtlasLusoris.TrainingKit import Make_Training\n"
			"from AtlasVenustas import Chip"
			),
		"Warlock": (
			"from AtlasLusoris.FeaturesKit import Grant_Resistance\n"
			"from AtlasLusoris.TrainingKit import Make_Training\n"
			"from AtlasVenustas import Chip"
			),
		"Wizard": (
			"from AtlasLusoris.TrainingKit import Make_Training\n"
			"from AtlasVenustas import Chip"
			),
		}

CONSTANTS = {
		"Artificer": [
				('GUILD', 'Artificer'),
				('CORE_SOURCE', 'Training: Artificer'),
				('ALCHEMIST', 'Alchemist'),
				('ARMORER', 'Armorer'),
				('ARTILLERIST', 'Artillerist'),
				('BATTLE_SMITH', 'Battle Smith'),
				],
		"Bard": [
				('GUILD', 'Bard'),
				('CORE_SOURCE', 'Training: Bard'),
				('DANCE', 'Dance'),
				('GLAMOUR', 'Glamour'),
				('LORE', 'Lore'),
				('VALOR', 'Valor'),
				],
		"Monk": [
				('GUILD', 'Monk'),
				('CORE_SOURCE', 'Training: Monk'),
				('MERCY', 'Mercy'),
				('OPEN_HAND', 'Open Hand'),
				('SHADOW', 'Shadow'),
				('ELEMENTS', 'Elements'),
				],
		"Sorcerer": [
				('GUILD', 'Sorcerer'),
				('CORE_SOURCE', 'Training: Sorcerer'),
				('ABERRANT', 'Aberrant Sorcery'),
				('CLOCKWORK', 'Clockwork Sorcery'),
				('DRACONIC', 'Draconic Sorcery'),
				('WILD_MAGIC', 'Wild Magic Sorcery'),
				],
		"Warlock": [
				('GUILD', 'Warlock'),
				('CORE_SOURCE', 'Training: Warlock'),
				('ARCHFEY', 'Archfey'),
				('CELESTIAL', 'Celestial'),
				('FIEND', 'Fiend'),
				('GREAT_OLD_ONE', 'Great Old One'),
				],
		"Wizard": [
				('GUILD', 'Wizard'),
				('CORE_SOURCE', 'Training: Wizard'),
				('ABJURER', 'Abjurer'),
				('DIVINER', 'Diviner'),
				('EVOKER', 'Evoker'),
				('ILLUSIONIST', 'Illusionist'),
				('BLADESINGER', 'Bladesinger'),
				],
		}

PATH_HELPER = {
		"Artificer": {
				None: "_core",
				"Alchemist": "_alchemist",
				"Armorer": "_armorer",
				"Artillerist": "_artillerist",
				"Battle Smith": "_battle_smith",
				},
		"Bard": {
				None: "_core",
				"Dance": "_dance",
				"Glamour": "_glamour",
				"Lore": "_lore",
				"Valor": "_valor",
				},
		"Monk": {
				None: "_core",
				"Mercy": "_mercy",
				"Open Hand": "_open_hand",
				"Shadow": "_shadow",
				"Elements": "_elements",
				},
		"Sorcerer": {
				None: "_core",
				"Aberrant Sorcery": "_aberrant",
				"Clockwork Sorcery": "_clockwork",
				"Draconic Sorcery": "_draconic",
				"Wild Magic Sorcery": "_wild_magic",
				},
		"Warlock": {
				None: "_core",
				"Archfey": "_archfey",
				"Celestial": "_celestial",
				"Fiend": "_fiend",
				"Great Old One": "_goo",
				},
		"Wizard": {
				None: "_core",
				"Abjurer": "_abjurer",
				"Diviner": "_diviner",
				"Evoker": "_evoker",
				"Illusionist": "_illusionist",
				"Bladesinger": "_bladesinger",
				},
		}

SECTION = {
		"Artificer": {
				None: "Core Guild lessons",
				"Alchemist": "Alchemist Specialty",
				"Armorer": "Armorer Specialty",
				"Artillerist": "Artillerist Specialty",
				"Battle Smith": "Battle Smith Specialty",
				},
		"Bard": {
				None: "Core Guild lessons",
				"Dance": "College of Dance",
				"Glamour": "College of Glamour",
				"Lore": "College of Lore",
				"Valor": "College of Valor",
				},
		"Monk": {
				None: "Core Guild lessons",
				"Mercy": "Warrior of Mercy",
				"Open Hand": "Warrior of the Open Hand",
				"Shadow": "Warrior of Shadow",
				"Elements": "Warrior of the Elements",
				},
		"Sorcerer": {
				None: "Core Guild lessons",
				"Aberrant Sorcery": "Aberrant Sorcery",
				"Clockwork Sorcery": "Clockwork Sorcery",
				"Draconic Sorcery": "Draconic Sorcery",
				"Wild Magic Sorcery": "Wild Magic Sorcery",
				},
		"Warlock": {
				None: "Core Guild lessons",
				"Archfey": "The Archfey",
				"Celestial": "The Celestial",
				"Fiend": "The Fiend",
				"Great Old One": "The Great Old One",
				},
		"Wizard": {
				None: "Core Guild lessons",
				"Abjurer": "Abjurer",
				"Diviner": "Diviner",
				"Evoker": "Evoker",
				"Illusionist": "Illusionist",
				"Bladesinger": "Bladesinger",
				},
		}


def load_vault(
		pyc_name: str,
		):
	pyc = VAULT / pyc_name
	body = types.ModuleType(
			f"_vault_{pyc_name}"
			)
	exec(
			marshal.loads(
					pyc.read_bytes()[
							16:
							]
					),
			body.__dict__,
			)
	code = marshal.loads(
			pyc.read_bytes()[
					16:
					]
			)
	return body, code


def closure_map(
		fn,
		):
	names = fn.__code__.co_freevars
	cells = fn.__closure__ or ()
	return {
			name: cell.cell_contents
			for name, cell in zip(
					names,
					cells,
					)
			}


def escape(
		text: str,
		) -> str:
	return (
		text.replace(
				"\\",
				"\\\\",
				).replace(
				'"',
				'\\"',
				)
		)


def wrap_fragments(
		text: str,
		width: int = 72,
		) -> list[str]:
	if not text:
		return [
				"",
				]
	pieces: list[tuple[str, str]] = []
	for unit in re.findall(
			r"<[^>]+>|[^<]+",
			text,
			):
		if unit.startswith(
				"<"
				):
			pieces.append(
					(
							"tag",
							unit,
							)
					)
			continue
		parts = unit.split(
				" "
				)
		for index, word in enumerate(
				parts
				):
			if index:
				pieces.append(
						(
								"space",
								" ",
								)
						)
			if word:
				pieces.append(
						(
								"word",
								word,
								)
						)
	chunks: list[str] = []
	buf = ""
	for kind, token in pieces:
		if kind == "space":
			if len(buf) >= width:
				chunks.append(
						buf.rstrip() + " "
						)
				buf = ""
			elif buf:
				buf += " "
			continue
		joined = buf + token
		if buf and kind == "word" and len(joined) > width:
			chunks.append(
					buf.rstrip() + " "
					)
			buf = token
		else:
			buf = joined
		if kind == "tag" and token in {
				"<ul>",
				"</ul>",
				"</li>",
				"<br>",
				}:
			chunks.append(
					buf
					)
			buf = ""
	if buf:
		chunks.append(
				buf
				)
	return [
			chunk for chunk in chunks if chunk != ""
			] or [
			"",
			]


def emit_string_arg(
		name: str,
		text: str,
		) -> str:
	frags = wrap_fragments(
			text
			)
	if "".join(
			frags
			) != text:
		frags = [
				text,
				]
	if len(frags) == 1 and len(frags[0]) < 68 and "<" not in frags[0]:
		return f'{T}{name}="{escape(frags[0])}",'
	lines = [
			f"{T}{name}=(",
			]
	for frag in frags:
		lines.append(
				f'{T}{T}"{escape(frag)}"'
				)
	lines.append(
			f"{T}{T}),"
			)
	return "\n".join(
			lines
			)


def emit_rank(
		) -> str:
	return f'''\
def _rank(
{T}{T}char,
{T}{T}) -> int:
{T}from AtlasLusoris.TrainingKit import level_in_guild
{T}return level_in_guild(
{T}{T}{T}char,
{T}{T}{T}GUILD,
{T}{T}{T})
'''


def emit_core(
		) -> str:
	return f'''\
def _core(
{T}{T}*,
{T}{T}name: str,
{T}{T}min_level: int,
{T}{T}description,
{T}{T}chips=(),
{T}{T}apply=None,
{T}{T}):
{T}return Make_Training(
{T}{T}{T}name=name,
{T}{T}{T}guild_name=GUILD,
{T}{T}{T}min_level=min_level,
{T}{T}{T}description=description,
{T}{T}{T}chips=chips,
{T}{T}{T}apply=apply,
{T}{T}{T}source=CORE_SOURCE,
{T}{T}{T})
'''


def emit_path_builder(
		fn_name: str,
		arg_name: str,
		source_expr: str,
		with_apply: bool = False,
		) -> str:
	apply_arg = f"\n{T}{T}apply=None," if with_apply else ""
	apply_kw = f"\n{T}{T}{T}apply=apply," if with_apply else ""
	return f'''\
def {fn_name}(
{T}{T}{arg_name}: str,
{T}{T}*,
{T}{T}name: str,
{T}{T}min_level: int,
{T}{T}description,
{T}{T}chips=(),{apply_arg}
{T}{T}):
{T}return Make_Training(
{T}{T}{T}name=name,
{T}{T}{T}guild_name=GUILD,
{T}{T}{T}min_level=min_level,
{T}{T}{T}description=description,
{T}{T}{T}chips=chips,{apply_kw}
{T}{T}{T}path={arg_name},
{T}{T}{T}source={source_expr},
{T}{T}{T})
'''


def emit_wrapper(
		fn_name: str,
		inner: str,
		const: str,
		with_apply: bool = False,
		) -> str:
	apply_arg = f"\n{T}{T}apply=None," if with_apply else ""
	apply_pass = f"\n{T}{T}{T}apply=apply," if with_apply else ""
	return f'''\
def {fn_name}(
{T}{T}*,
{T}{T}name: str,
{T}{T}min_level: int,
{T}{T}description,
{T}{T}chips=(),{apply_arg}
{T}{T}):
{T}return {inner}(
{T}{T}{T}{const},
{T}{T}{T}name=name,
{T}{T}{T}min_level=min_level,
{T}{T}{T}description=description,
{T}{T}{T}chips=chips,{apply_pass}
{T}{T}{T})
'''


def helpers_artificer(
		) -> str:
	return "\n".join(
			[
					emit_rank(),
					f'''\
def _infusions_known(
{T}{T}char,
{T}{T}) -> int:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}if level >= 20:
{T}{T}return 12
{T}if level >= 18:
{T}{T}return 11
{T}if level >= 14:
{T}{T}return 10
{T}if level >= 12:
{T}{T}return 9
{T}if level >= 10:
{T}{T}return 8
{T}if level >= 8:
{T}{T}return 7
{T}if level >= 6:
{T}{T}return 6
{T}if level >= 4:
{T}{T}return 4
{T}return 2
''',
					emit_core(),
					emit_path_builder(
							"_specialty",
							"specialty_name",
							'f"Training: {specialty_name} Specialty"',
							),
					emit_wrapper(
							"_alchemist",
							"_specialty",
							"ALCHEMIST",
							),
					emit_wrapper(
							"_armorer",
							"_specialty",
							"ARMORER",
							),
					emit_wrapper(
							"_artillerist",
							"_specialty",
							"ARTILLERIST",
							),
					emit_wrapper(
							"_battle_smith",
							"_specialty",
							"BATTLE_SMITH",
							),
					]
			)


def helpers_bard(
		) -> str:
	return "\n".join(
			[
					emit_rank(),
					f'''\
def _bardic_die(
{T}{T}char,
{T}{T}) -> str:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}if level >= 15:
{T}{T}return "d12"
{T}if level >= 10:
{T}{T}return "d10"
{T}if level >= 5:
{T}{T}return "d8"
{T}return "d6"


def _bardic_uses(
{T}{T}char,
{T}{T}) -> int:
{T}from AtlasActorLudi.Map_of_Scores import Modifier
{T}cha = getattr(
{T}{T}{T}getattr(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}"abilities",
{T}{T}{T}{T}{T}None,
{T}{T}{T}{T}{T}),
{T}{T}{T}"CHA",
{T}{T}{T}10,
{T}{T}{T})
{T}return max(
{T}{T}{T}1,
{T}{T}{T}Modifier(
{T}{T}{T}{T}{T}cha,
{T}{T}{T}{T}{T}),
{T}{T}{T})
''',
					emit_core(),
					emit_path_builder(
							"_path",
							"path_name",
							'f"Training: College of {path_name}"',
							),
					emit_wrapper(
							"_dance",
							"_path",
							"DANCE",
							),
					emit_wrapper(
							"_glamour",
							"_path",
							"GLAMOUR",
							),
					emit_wrapper(
							"_lore",
							"_path",
							"LORE",
							),
					emit_wrapper(
							"_valor",
							"_path",
							"VALOR",
							),
					f'''\
def _bardic_entry(
{T}{T}char,
{T}{T}) -> str:
{T}die = _bardic_die(
{T}{T}{T}char,
{T}{T}{T})
{T}uses = _bardic_uses(
{T}{T}{T}char,
{T}{T}{T})
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}rest = "Short or Long" if level >= 5 else "Long"
{T}return (
{T}{T}{T}f"Your Bardic Inspiration die is a <b>{{die}}</b>. "
{T}{T}{T}"<br><b>Bonus Action:</b> inspire a creature within 60 feet "
{T}{T}{T}"that can see or hear you. That creature gains one Bardic "
{T}{T}{T}"Inspiration die. A creature can have only one Bardic Inspiration "
{T}{T}{T}"die at a time. "
{T}{T}{T}"<br>Once within the next hour, when the creature fails a D20 Test, "
{T}{T}{T}"it can roll the die and add the number to the d20, potentially "
{T}{T}{T}"turning failure into success. The die is expended when rolled. "
{T}{T}{T}f"<br>You can confer a total of <b>{{uses}} Bardic Inspiration dice</b>. "
{T}{T}{T}f"You regain all expended uses when you finish a <b>{{rest}} Rest</b>."
{T}{T}{T})
'''.replace(
							"{{die}}",
							"{die}",
							).replace(
							"{{uses}}",
							"{uses}",
							).replace(
							"{{rest}}",
							"{rest}",
							),
					]
			)


def helpers_monk(
		) -> str:
	table = f'''\
_MARTIAL_ARTS_DIE = (
{T}{T}"",
{T}{T}"1d6",
{T}{T}"1d6",
{T}{T}"1d6",
{T}{T}"1d6",
{T}{T}"1d8",
{T}{T}"1d8",
{T}{T}"1d8",
{T}{T}"1d8",
{T}{T}"1d8",
{T}{T}"1d8",
{T}{T}"1d10",
{T}{T}"1d10",
{T}{T}"1d10",
{T}{T}"1d10",
{T}{T}"1d10",
{T}{T}"1d10",
{T}{T}"1d12",
{T}{T}"1d12",
{T}{T}"1d12",
{T}{T}"1d12",
{T}{T})
'''
	return "\n".join(
			[
					table,
					f'''\
def _focus_points(
{T}{T}char,
{T}{T}) -> int:
{T}return max(
{T}{T}{T}1,
{T}{T}{T}_rank(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})
''',
					emit_rank(),
					f'''\
def _martial_die(
{T}{T}char,
{T}{T}) -> str:
{T}level = max(
{T}{T}{T}1,
{T}{T}{T}min(
{T}{T}{T}{T}{T}20,
{T}{T}{T}{T}{T}_rank(
{T}{T}{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}{T}{T}),
{T}{T}{T}{T}{T}),
{T}{T}{T})
{T}return _MARTIAL_ARTS_DIE[
{T}{T}{T}level
{T}{T}{T}]


def _unarmored_speed_bonus(
{T}{T}char,
{T}{T}) -> int:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}if level >= 18:
{T}{T}return 35
{T}if level >= 14:
{T}{T}return 30
{T}if level >= 10:
{T}{T}return 25
{T}if level >= 6:
{T}{T}return 20
{T}if level >= 2:
{T}{T}return 15
{T}return 10
''',
					emit_core(),
					emit_path_builder(
							"_path",
							"path_name",
							'f"Training: Monk ({path_name})"',
							),
					emit_wrapper(
							"_mercy",
							"_path",
							"MERCY",
							),
					emit_wrapper(
							"_open_hand",
							"_path",
							"OPEN_HAND",
							),
					emit_wrapper(
							"_shadow",
							"_path",
							"SHADOW",
							),
					emit_wrapper(
							"_elements",
							"_path",
							"ELEMENTS",
							),
					f'''\
def _martial_arts_entry(
{T}{T}char,
{T}{T}) -> str:
{T}die = _martial_die(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}"Your practice of martial arts gives you mastery of combat styles "
{T}{T}{T}"that use your Unarmed Strike and Monk weapons. You gain the following "
{T}{T}{T}"benefits while unarmed or wielding only Monk weapons and not wearing "
{T}{T}{T}"armor or wielding a Shield:"
{T}{T}{T}"<ul>"
{T}{T}{T}"<li><b>Bonus Unarmed Strike.</b> You can make an Unarmed Strike as a "
{T}{T}{T}"Bonus Action.</li>"
{T}{T}{T}f"<li><b>Martial Arts Die.</b> Roll <b>{{die}}</b> in place of the "
{T}{T}{T}"normal damage of your Unarmed Strike or Monk weapons.</li>"
{T}{T}{T}"<li><b>Dexterous Attacks.</b> You can use your Dexterity modifier "
{T}{T}{T}"instead of Strength for attack and damage rolls of Unarmed Strikes "
{T}{T}{T}"and Monk weapons. Also applies to Grapple or Shove save DCs.</li>"
{T}{T}{T}"</ul>"
{T}{T}{T})


def _monks_focus_entry(
{T}{T}char,
{T}{T}) -> str:
{T}fp = _focus_points(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}f"Your training has let you harness your psionic energy. You have "
{T}{T}{T}f"<b>{{fp}} Focus Points</b> that fuel your special actions. You regain "
{T}{T}{T}"all spent points when you finish a Long Rest. On a Short Rest you "
{T}{T}{T}"also regain Focus Points equal to half your Monk level (rounded up)."
{T}{T}{T}"<br>You can spend Focus Points on:"
{T}{T}{T}"<ul>"
{T}{T}{T}"<li><b>Flurry of Blows (1 point).</b> After the Attack action, make "
{T}{T}{T}"two Unarmed Strikes as a Bonus Action.</li>"
{T}{T}{T}"<li><b>Patient Defense (1 point).</b> Take the Dodge action as a "
{T}{T}{T}"Bonus Action.</li>"
{T}{T}{T}"<li><b>Step of the Wind (1 point).</b> Take the Disengage or Dash "
{T}{T}{T}"action as a Bonus Action; jump distance doubles for the turn.</li>"
{T}{T}{T}"</ul>"
{T}{T}{T})


def _unarmored_movement_entry(
{T}{T}char,
{T}{T}) -> str:
{T}bonus = _unarmored_speed_bonus(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}f"Your speed increases by <b>+{{bonus}} feet</b> while you aren't "
{T}{T}{T}"wearing armor or wielding a Shield."
{T}{T}{T})


def _apply_body_and_mind(
{T}{T}char,
{T}{T}) -> None:
{T}abilities = getattr(
{T}{T}{T}char,
{T}{T}{T}"abilities",
{T}{T}{T}None,
{T}{T}{T})
{T}if abilities is None:
{T}{T}return None
{T}from AtlasLusoris.Grimoire_of_Features import raise_stat
{T}raise_stat(
{T}{T}{T}char,
{T}{T}{T}"DEX",
{T}{T}{T}4,
{T}{T}{T}cap=25,
{T}{T}{T})
{T}raise_stat(
{T}{T}{T}char,
{T}{T}{T}"WIS",
{T}{T}{T}4,
{T}{T}{T}cap=25,
{T}{T}{T})


def _unarmored_armour_class(
{T}{T}char,
{T}{T}abilities,
{T}{T}) -> int:
{T}"""What this Character's AC would be with nothing on."""
{T}from AtlasActorLudi.Map_of_Scores import Modifier
{T}scores = getattr(
{T}{T}{T}char,
{T}{T}{T}"AS",
{T}{T}{T}None,
{T}{T}{T})
{T}if scores is None:
{T}{T}return 10
{T}return 10 + sum(
{T}{T}{T}Modifier(
{T}{T}{T}{T}{T}getattr(
{T}{T}{T}{T}{T}{T}{T}scores,
{T}{T}{T}{T}{T}{T}{T}ability,
{T}{T}{T}{T}{T}{T}{T}10,
{T}{T}{T}{T}{T}{T}{T}),
{T}{T}{T}{T}{T})
{T}{T}{T}for ability in abilities
{T}{T}{T})


def _unarmored_ac(
{T}{T}char,
{T}{T}) -> int:
{T}return _unarmored_armour_class(
{T}{T}{T}char,
{T}{T}{T}(
{T}{T}{T}{T}{T}"DEX",
{T}{T}{T}{T}{T}"WIS",
{T}{T}{T}{T}{T}),
{T}{T}{T})


def _unarmored_defense_entry(
{T}{T}char,
{T}{T}) -> str:
{T}armour_class = _unarmored_armour_class(
{T}{T}{T}char,
{T}{T}{T}(
{T}{T}{T}{T}{T}"DEX",
{T}{T}{T}{T}{T}"WIS",
{T}{T}{T}{T}{T}),
{T}{T}{T})
{T}return (
{T}{T}{T}f"While not wearing armor or wielding a Shield, your AC equals "
{T}{T}{T}f"<b>{{armour_class}}</b> (10 + Dexterity modifier + Wisdom modifier)."
{T}{T}{T})


def _hand_of_harm_entry(
{T}{T}char,
{T}{T}) -> str:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}poison_note = (
{T}{T}{T}"<br>You can also give that creature the Poisoned condition "
{T}{T}{T}"until the end of your next turn."
{T}{T}{T}if level >= 6
{T}{T}{T}else ""
{T}{T}{T})
{T}return (
{T}{T}{T}"Once per turn when you hit a creature with an Unarmed Strike and "
{T}{T}{T}"deal damage, you can expend 1 Focus Point to deal extra "
{T}{T}{T}"<b>Necrotic damage</b> equal to one roll of your Martial Arts die "
{T}{T}{T}f"plus your Wisdom modifier.{{poison_note}}"
{T}{T}{T})


def _hand_of_healing_entry(
{T}{T}char,
{T}{T}) -> str:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}cure_note = (
{T}{T}{T}"<br>When you use your Flurry of Blows, you can also end one of "
{T}{T}{T}"the following conditions on the creature you heal (Blinded, "
{T}{T}{T}"Deafened, Paralyzed, Poisoned, or Stunned)."
{T}{T}{T}if level >= 6
{T}{T}{T}else ""
{T}{T}{T})
{T}return (
{T}{T}{T}"As a <i>Magic action</i>, expend 1 Focus Point to touch a creature "
{T}{T}{T}"and restore Hit Points equal to one roll of your Martial Arts die "
{T}{T}{T}"plus your Wisdom modifier."
{T}{T}{T}"<br>When you use your Flurry of Blows, you can replace one Unarmed "
{T}{T}{T}"Strike with a use of this feature without expending a Focus Point "
{T}{T}{T}f"for the healing.{{cure_note}}"
{T}{T}{T})
'''.replace(
							"{{die}}",
							"{die}",
							).replace(
							"{{fp}}",
							"{fp}",
							).replace(
							"{{bonus}}",
							"{bonus}",
							).replace(
							"{{armour_class}}",
							"{armour_class}",
							).replace(
							"{{poison_note}}",
							"{poison_note}",
							).replace(
							"{{cure_note}}",
							"{cure_note}",
							),
					]
			)


def helpers_sorcerer(
		) -> str:
	return "\n".join(
			[
					emit_rank(),
					f'''\
def _sorcery_points(
{T}{T}char,
{T}{T}) -> int:
{T}return _rank(
{T}{T}{T}char,
{T}{T}{T})


def _metamagic_count(
{T}{T}char,
{T}{T}) -> int:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}count = 2
{T}if level >= 10:
{T}{T}count += 2
{T}if level >= 17:
{T}{T}count += 2
{T}return count
''',
					emit_core(),
					emit_path_builder(
							"_origin",
							"origin_name",
							'f"Training: {origin_name}"',
							),
					f'''\
def _font_of_magic_entry(
{T}{T}char,
{T}{T}) -> str:
{T}pts = _sorcery_points(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}f"You have <b>{{pts}} Sorcery Points</b> (regained on Long Rest)."
{T}{T}{T}"<br><b>Creating Spell Slots.</b> As a Bonus Action, spend points "
{T}{T}{T}"to create a slot: 1st 2 pts, 2nd 3 pts, 3rd 5 pts, 4th 6 pts, "
{T}{T}{T}"5th 7 pts (max 5th level)."
{T}{T}{T}"<br><b>Converting Spell Slots.</b> As a Bonus Action, expend a "
{T}{T}{T}"slot to gain Sorcery Points equal to its level."
{T}{T}{T})


def _metamagic_entry(
{T}{T}char,
{T}{T}) -> str:
{T}count = _metamagic_count(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}f"Choose <b>{{count}}</b> Metamagic options. Spend Sorcery Points "
{T}{T}{T}"to modify your spells — only one option per spell unless a feature "
{T}{T}{T}"says otherwise."
{T}{T}{T}"<br><i>Options (cost in Sorcery Points):</i> Careful Spell (1), "
{T}{T}{T}"Distant Spell (1), Empowered Spell (1), Extended Spell (1), "
{T}{T}{T}"Heightened Spell (2), Quickened Spell (2), Seeking Spell (1), "
{T}{T}{T}"Subtle Spell (1), Transmuted Spell (1), Twinned Spell (1)."
{T}{T}{T})
'''.replace(
							"{{pts}}",
							"{pts}",
							).replace(
							"{{count}}",
							"{count}",
							),
					emit_wrapper(
							"_aberrant",
							"_origin",
							"ABERRANT",
							),
					emit_wrapper(
							"_clockwork",
							"_origin",
							"CLOCKWORK",
							),
					emit_wrapper(
							"_draconic",
							"_origin",
							"DRACONIC",
							),
					f'''\
def _draconic_resilience_entry(
{T}{T}char,
{T}{T}) -> str:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}f"<b>Draconic Resilience.</b> Your hit point maximum increases by "
{T}{T}{T}f"<b>{{level}}</b> (1 per Sorcerer level). When you aren't wearing "
{T}{T}{T}"armor, your AC equals 13 + your Dexterity modifier."
{T}{T}{T})
'''.replace(
							"{{level}}",
							"{level}",
							),
					emit_wrapper(
							"_wild_magic",
							"_origin",
							"WILD_MAGIC",
							),
					]
			)


def helpers_warlock(
		) -> str:
	return "\n".join(
			[
					emit_rank(),
					f'''\
def _invocations_known(
{T}{T}char,
{T}{T}) -> int:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}table = (
{T}{T}{T}1, 3, 3, 3, 5, 5, 6, 6, 7, 7,
{T}{T}{T}7, 8, 8, 8, 9, 9, 9, 10, 10, 10,
{T}{T}{T})
{T}return table[
{T}{T}{T}min(
{T}{T}{T}{T}{T}level,
{T}{T}{T}{T}{T}20,
{T}{T}{T}{T}{T}) - 1
{T}{T}{T}]


def _pact_row(
{T}{T}char,
{T}{T}):
{T}"""
{T}This Warlock's row of the Pact Magic table.

{T}Read, never recomputed.  The table in ``Grimoire_of_Spellcasters`` is
{T}what the sheet actually casts from, and a second copy of the
{T}progression here was quietly disagreeing with it: it granted one slot
{T}below level 11 and two above, where the rules give one, then two,
{T}then three, then four.
{T}"""
{T}from AtlasLusoris.Grimoire_of_Spellcasters import (
{T}{T}{T}WARLOCK_SPELLCASTING_TABLE,
{T}{T}{T})
{T}return WARLOCK_SPELLCASTING_TABLE.get(
{T}{T}{T}min(
{T}{T}{T}{T}{T}max(
{T}{T}{T}{T}{T}{T}{T}_rank(
{T}{T}{T}{T}{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}{T}{T}{T}{T}),
{T}{T}{T}{T}{T}{T}{T}1,
{T}{T}{T}{T}{T}{T}{T}),
{T}{T}{T}{T}{T}20,
{T}{T}{T}{T}{T}),
{T}{T}{T}WARLOCK_SPELLCASTING_TABLE[
{T}{T}{T}{T}{T}20
{T}{T}{T}{T}{T}],
{T}{T}{T})


def _pact_slot_level(
{T}{T}char,
{T}{T}):
{T}return _pact_row(
{T}{T}{T}char,
{T}{T}{T})[
{T}{T}{T}"slot_level"
{T}{T}{T}]


def _pact_slots(
{T}{T}char,
{T}{T}):
{T}return _pact_row(
{T}{T}{T}char,
{T}{T}{T})[
{T}{T}{T}"slots"
{T}{T}{T}][
{T}{T}{T}0
{T}{T}{T}]


def _pact_magic_entry(
{T}{T}char,
{T}{T}) -> str:
{T}row = _pact_row(
{T}{T}{T}char,
{T}{T}{T})
{T}slots = row[
{T}{T}{T}"slots"
{T}{T}{T}][
{T}{T}{T}0
{T}{T}{T}]
{T}plural = "" if slots == 1 else "s"
{T}return (
{T}{T}{T}"Through occult ceremony you have formed a pact with a mysterious "
{T}{T}{T}f"entity. You have <b>{{slots}} Pact Magic slot{{plural}}</b> of spell "
{T}{T}{T}f"level <b>{{row['slot_level']}}</b>. All of your slots are of that "
{T}{T}{T}"level, and you regain all expended Pact Magic slots when you "
{T}{T}{T}"finish a Short or Long Rest."
{T}{T}{T})


def _mystic_arcanum_entry(
{T}{T}char,
{T}{T}) -> str:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}arcana = []
{T}if level >= 11:
{T}{T}arcana.append(
{T}{T}{T}{T}"6th"
{T}{T}{T}{T})
{T}if level >= 13:
{T}{T}arcana.append(
{T}{T}{T}{T}"7th"
{T}{T}{T}{T})
{T}if level >= 15:
{T}{T}arcana.append(
{T}{T}{T}{T}"8th"
{T}{T}{T}{T})
{T}if level >= 17:
{T}{T}arcana.append(
{T}{T}{T}{T}"9th"
{T}{T}{T}{T})
{T}if not arcana:
{T}{T}return "Mystic Arcanum not yet unlocked at this level."
{T}known = ", ".join(
{T}{T}{T}arcana
{T}{T}{T})
{T}return (
{T}{T}{T}"Your patron grants you a magical secret called an arcanum. You "
{T}{T}{T}"choose one Warlock spell at each of these levels as an arcanum: "
{T}{T}{T}f"<b>{{known}}</b>. You can cast each of them once without a spell "
{T}{T}{T}"slot, and you regain all uses when you finish a Long Rest."
{T}{T}{T})


def _magical_cunning_entry(
{T}{T}char,
{T}{T}) -> str:
{T}"""
{T}Recovery moved from a rite to the moment of danger.

{T}The published feature is a one-minute rite, once per Long Rest, for
{T}half your slots.  A minute of quiet is a Short Rest with extra steps,
{T}and the Warlock refills on a Short Rest anyway, so the feature only
{T}mattered in a window that barely exists.

{T}Hung on Initiative it costs almost nothing in power -- a party that
{T}rests after every fight already had this -- and it buys the class its
{T}fantasy. Attrition still bites, because **Hit Points do not come
{T}back**.  You get what you signed for, which is power and not rescue:
{T}more dangerous every round, and no closer to surviving.
{T}"""
{T}slots = _pact_slots(
{T}{T}{T}char,
{T}{T}{T})
{T}plural = "" if slots == 1 else "s"
{T}return (
{T}{T}{T}"You keep a line open, and it answers when you are about to need "
{T}{T}{T}"it. <b>When you roll Initiative, you regain all expended Pact "
{T}{T}{T}f"Magic spell slots</b>: {{slots}} slot{{plural}} at spell level "
{T}{T}{T}f"{{_pact_slot_level(char)}}, with no limit on how often. What comes "
{T}{T}{T}"back is power, not rescue. Your wounds stay exactly where they are."
{T}{T}{T})
'''.replace(
							"{{slots}}",
							"{slots}",
							).replace(
							"{{plural}}",
							"{plural}",
							).replace(
							"{{row['slot_level']}}",
							"{row['slot_level']}",
							).replace(
							"{{known}}",
							"{known}",
							).replace(
							"{{_pact_slot_level(char)}}",
							"{_pact_slot_level(char)}",
							),
					emit_core(),
					emit_path_builder(
							"_patron",
							"patron_name",
							'f"Training: The {patron_name} Patron"',
							with_apply=True,
							),
					emit_wrapper(
							"_archfey",
							"_patron",
							"ARCHFEY",
							with_apply=True,
							),
					emit_wrapper(
							"_celestial",
							"_patron",
							"CELESTIAL",
							with_apply=True,
							),
					f'''\
def _healing_light_dice(
{T}{T}char,
{T}{T}) -> int:
{T}"""One plus your Warlock level.  Was level + 5, which is the 2014 pool."""
{T}return _rank(
{T}{T}{T}char,
{T}{T}{T}) + 1


def _charisma_modifier(
{T}{T}char,
{T}{T}) -> int:
{T}scores = getattr(
{T}{T}{T}char,
{T}{T}{T}"AS",
{T}{T}{T}None,
{T}{T}{T})
{T}if scores is None:
{T}{T}return 1
{T}return max(
{T}{T}{T}1,
{T}{T}{T}(
{T}{T}{T}{T}{T}int(
{T}{T}{T}{T}{T}{T}{T}getattr(
{T}{T}{T}{T}{T}{T}{T}{T}{T}scores,
{T}{T}{T}{T}{T}{T}{T}{T}{T}"CHA",
{T}{T}{T}{T}{T}{T}{T}{T}{T}10,
{T}{T}{T}{T}{T}{T}{T}{T}{T}),
{T}{T}{T}{T}{T}{T}{T}) - 10
{T}{T}{T}{T}{T}) // 2,
{T}{T}{T})


def _healing_light_entry(
{T}{T}char,
{T}{T}) -> str:
{T}pool = _healing_light_dice(
{T}{T}{T}char,
{T}{T}{T})
{T}spend = _charisma_modifier(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}"You channel celestial energy to heal wounds, drawing on a pool of "
{T}{T}{T}f"<b>{{pool}}d6</b>. As a Bonus Action you can heal yourself or one "
{T}{T}{T}"creature you can see within 60 feet, expending dice from the pool "
{T}{T}{T}"and restoring Hit Points equal to the total rolled. You can spend "
{T}{T}{T}f"at most <b>{{spend}}</b> dice at once. Your pool regains all expended "
{T}{T}{T}"dice when you finish a Long Rest."
{T}{T}{T})


def _grant_radiant_resistance(
{T}{T}char,
{T}{T}) -> None:
{T}Grant_Resistance(
{T}{T}{T}char,
{T}{T}{T}"Radiant",
{T}{T}{T})
'''.replace(
							"{{pool}}",
							"{pool}",
							).replace(
							"{{spend}}",
							"{spend}",
							),
					emit_wrapper(
							"_fiend",
							"_patron",
							"FIEND",
							with_apply=True,
							),
					f'''\
def _dark_ones_blessing_entry(
{T}{T}char,
{T}{T}) -> str:
{T}level = _rank(
{T}{T}{T}char,
{T}{T}{T})
{T}gained = max(
{T}{T}{T}1,
{T}{T}{T}level + _charisma_modifier(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})
{T}return (
{T}{T}{T}f"When you reduce an enemy to 0 Hit Points, you gain <b>{{gained}} "
{T}{T}{T}"Temporary Hit Points</b>. You also gain this benefit if someone "
{T}{T}{T}"else reduces an enemy within 10 feet of you to 0 Hit Points."
{T}{T}{T})


def _dark_ones_own_luck_entry(
{T}{T}char,
{T}{T}) -> str:
{T}uses = max(
{T}{T}{T}1,
{T}{T}{T}_charisma_modifier(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})
{T}plural = "" if uses == 1 else "s"
{T}return (
{T}{T}{T}"You can call on your fiendish patron to alter fate in your favour. "
{T}{T}{T}"When you make an ability check or a saving throw, you can use this "
{T}{T}{T}"feature to add 1d10 to your roll. You can do so after seeing the "
{T}{T}{T}"roll but before any of its effects occur. You have "
{T}{T}{T}f"<b>{{uses}}</b> use{{plural}}, no more than one per roll, and you "
{T}{T}{T}"regain all expended uses when you finish a Long Rest."
{T}{T}{T})
'''.replace(
							"{{gained}}",
							"{gained}",
							).replace(
							"{{uses}}",
							"{uses}",
							).replace(
							"{{plural}}",
							"{plural}",
							),
					emit_wrapper(
							"_goo",
							"_patron",
							"GREAT_OLD_ONE",
							with_apply=True,
							),
					f'''\
def _awakened_mind_entry(
{T}{T}char,
{T}{T}) -> str:
{T}miles = max(
{T}{T}{T}1,
{T}{T}{T}_charisma_modifier(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})
{T}minutes = max(
{T}{T}{T}1,
{T}{T}{T}_rank(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})
{T}plural = "" if miles == 1 else "s"
{T}return (
{T}{T}{T}"Your patron left a door open in your mind. As a Bonus Action you "
{T}{T}{T}"can choose one creature you can see within 30 feet, and the two of "
{T}{T}{T}"you can speak telepathically while you are within "
{T}{T}{T}f"<b>{{miles}} mile{{plural}}</b> of each other. To understand each "
{T}{T}{T}"other you must each mentally use a language the other knows. The "
{T}{T}{T}f"connection lasts <b>{{minutes}} minutes</b>, and ends early if you "
{T}{T}{T}"use this feature on someone else."
{T}{T}{T})


def _grant_psychic_resistance(
{T}{T}char,
{T}{T}) -> None:
{T}Grant_Resistance(
{T}{T}{T}char,
{T}{T}{T}"Psychic",
{T}{T}{T})


def _create_thrall_entry(
{T}{T}char,
{T}{T}) -> str:
{T}temporary = max(
{T}{T}{T}1,
{T}{T}{T}_rank(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}) + _charisma_modifier(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})
{T}return (
{T}{T}{T}"When you cast <i>Summon Aberration</i>, you can modify it so that "
{T}{T}{T}"it does not require Concentration. If you do, the spell's duration "
{T}{T}{T}"becomes 1 minute for that casting, and the Aberration arrives with "
{T}{T}{T}f"<b>{{temporary}} Temporary Hit Points</b>. In addition, the first "
{T}{T}{T}"time each turn the Aberration hits a creature under the effect of "
{T}{T}{T}"your <i>Hex</i>, it deals extra Psychic damage to that target "
{T}{T}{T}"equal to the bonus damage of that spell."
{T}{T}{T})
'''.replace(
							"{{miles}}",
							"{miles}",
							).replace(
							"{{plural}}",
							"{plural}",
							).replace(
							"{{minutes}}",
							"{minutes}",
							).replace(
							"{{temporary}}",
							"{temporary}",
							),
					]
			)


def helpers_wizard(
		) -> str:
	return "\n".join(
			[
					emit_rank(),
					f'''\
def _intelligence_modifier(
{T}{T}char,
{T}{T}) -> int:
{T}scores = getattr(
{T}{T}{T}char,
{T}{T}{T}"AS",
{T}{T}{T}None,
{T}{T}{T})
{T}return int(
{T}{T}{T}getattr(
{T}{T}{T}{T}{T}scores,
{T}{T}{T}{T}{T}"int_mod",
{T}{T}{T}{T}{T}0,
{T}{T}{T}{T}{T}) or 0
{T}{T}{T})


def _bladesong_uses(
{T}{T}char,
{T}{T}) -> int:
{T}"""Intelligence modifier, minimum once."""
{T}return max(
{T}{T}{T}1,
{T}{T}{T}_intelligence_modifier(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})


def _bladesong_ac(
{T}{T}char,
{T}{T}) -> int:
{T}"""The Agility bonus: Intelligence modifier, minimum +1."""
{T}return max(
{T}{T}{T}1,
{T}{T}{T}_intelligence_modifier(
{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}),
{T}{T}{T})


def _recovery_slots(
{T}{T}char,
{T}{T}) -> int:
{T}return max(
{T}{T}{T}1,
{T}{T}{T}(
{T}{T}{T}{T}{T}_rank(
{T}{T}{T}{T}{T}{T}{T}char,
{T}{T}{T}{T}{T}{T}{T}) + 1
{T}{T}{T}{T}{T}) // 2,
{T}{T}{T})
''',
					emit_core(),
					emit_path_builder(
							"_tradition",
							"tradition_name",
							'f"Training: {tradition_name} Tradition"',
							),
					f'''\
def _arcane_recovery_entry(
{T}{T}char,
{T}{T}) -> str:
{T}recovery = _recovery_slots(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}"When you finish a Short Rest, you can choose expended spell slots "
{T}{T}{T}"to recover. The slots can have a combined level equal to no more "
{T}{T}{T}f"than <b>{{recovery}}</b> (half your Wizard level, rounded up), and "
{T}{T}{T}"none can be level 6 or higher."
{T}{T}{T}"<br>Once you use this feature, you can't do so again until you "
{T}{T}{T}"finish a Long Rest."
{T}{T}{T})


def _spell_levels_on_the_sheet(
{T}{T}char,
{T}{T}) -> int:
{T}"""
{T}The summed level of every levelled spell this Character is carrying.

{T}Rebuilding a lost book costs an hour and 10 GP per spell level, so
{T}this is the number both figures are struck from. Cantrips cost nothing
{T}to set down again and are not counted.
{T}"""
{T}try:
{T}{T}known = char.get_spellcaster().spells_known
{T}except Exception:
{T}{T}return 0
{T}total = 0
{T}for spell in known:
{T}{T}if "Cantrip" in type(
{T}{T}{T}{T}spell
{T}{T}{T}{T}).__name__:
{T}{T}{T}continue
{T}{T}total += int(
{T}{T}{T}{T}getattr(
{T}{T}{T}{T}{T}{T}spell,
{T}{T}{T}{T}{T}{T}"level",
{T}{T}{T}{T}{T}{T}0,
{T}{T}{T}{T}{T}{T}) or 0
{T}{T}{T}{T})
{T}return total


def _apply_spellbook(
{T}{T}char,
{T}{T}) -> None:
{T}"""Settle what this Wizard's book physically is, once and for life."""
{T}from AtlasLusoris.AtlasOfTraining.Map_of_Spellbooks import (
{T}{T}{T}Draw_Spellbook,
{T}{T}{T})
{T}Draw_Spellbook(
{T}{T}{T}char,
{T}{T}{T})


def _spellbook_entry(
{T}{T}char,
{T}{T}) -> str:
{T}"""
{T}The rules, opening on whatever this Character's book turned out to be.

{T}Matter-of-fact on purpose: the form is one clause, the rules follow
{T}unchanged, and nothing announces that a choice was made.
{T}"""
{T}form = getattr(
{T}{T}{T}char,
{T}{T}{T}"spellbook_form",
{T}{T}{T}None,
{T}{T}{T}) or "a Tiny object"
{T}levels = _spell_levels_on_the_sheet(
{T}{T}{T}char,
{T}{T}{T})
{T}return (
{T}{T}{T}f"Your Spellbook is {{form}}. It holds the spells you know. It is a "
{T}{T}{T}"Tiny object weighing 3 pounds, it has room for 100 pages, and it "
{T}{T}{T}"can be read only by you or by someone casting <i>Identify</i>."
{T}{T}{T}"<br><b>Copying a Spell.</b> A Wizard spell you find, on a Spell "
{T}{T}{T}"Scroll or in another book, can be copied into yours if it is of a "
{T}{T}{T}"level you can prepare. It takes 2 hours and 50 GP per spell level."
{T}{T}{T}"<br><b>Copying the Book.</b> Copying a spell you already know into "
{T}{T}{T}"a second book is faster: 1 hour and 10 GP per spell level. Many "
{T}{T}{T}"Wizards keep a spare for exactly that reason."
{T}{T}{T}"<br><b>Replacing the Book.</b> If you lose it you must spend "
{T}{T}{T}f"<b>{{levels * 10}} GP</b> and <b>{{levels}} hours</b> to rebuild it "
{T}{T}{T}"with the spells on this sheet. Any other spell you had learnt is "
{T}{T}{T}"lost with the original."
{T}{T}{T})
'''.replace(
							"{{recovery}}",
							"{recovery}",
							).replace(
							"{{form}}",
							"{form}",
							).replace(
							"{{levels * 10}}",
							"{levels * 10}",
							).replace(
							"{{levels}}",
							"{levels}",
							),
					emit_wrapper(
							"_abjurer",
							"_tradition",
							"ABJURER",
							),
					emit_wrapper(
							"_diviner",
							"_tradition",
							"DIVINER",
							),
					f'''\
def _portent_dice(
{T}{T}char,
{T}{T}) -> int:
{T}return 3 if _rank(
{T}{T}{T}char,
{T}{T}{T}) >= 14 else 2
''',
					emit_wrapper(
							"_evoker",
							"_tradition",
							"EVOKER",
							),
					emit_wrapper(
							"_illusionist",
							"_tradition",
							"ILLUSIONIST",
							),
					emit_wrapper(
							"_bladesinger",
							"_tradition",
							"BLADESINGER",
							),
					f'''\
def _bladesong_entry(
{T}{T}char,
{T}{T}) -> str:
{T}return (
{T}{T}{T}"As a <i>Bonus Action</i> you invoke the Bladesong, provided you "
{T}{T}{T}"are not wearing armor or using a Shield. It lasts 1 minute, and "
{T}{T}{T}"ends early if you have the Incapacitated condition, if you don "
{T}{T}{T}"armor or a Shield, or if you use two hands to attack with a weapon. "
{T}{T}{T}"You can dismiss it at any time (no action required)."
{T}{T}{T}f"<br>You can invoke it <b>{{_bladesong_uses(char)}}</b> times, "
{T}{T}{T}"regaining all uses on a Long Rest and one use whenever you use "
{T}{T}{T}"Arcane Recovery."
{T}{T}{T}f"<br><b>Agility.</b> You gain <b>+{{_bladesong_ac(char)}}</b> to AC, "
{T}{T}{T}"your Speed increases by <b>10 feet</b>, and you have Advantage on "
{T}{T}{T}"Dexterity (Acrobatics) checks."
{T}{T}{T}"<br><b>Bladework.</b> When you attack with a weapon you are "
{T}{T}{T}"proficient with, you can use <b>Intelligence</b> for the attack "
{T}{T}{T}"and damage rolls instead of Strength or Dexterity."
{T}{T}{T}"<br><b>Focus.</b> When you make a Constitution saving throw to "
{T}{T}{T}"maintain Concentration, you can add "
{T}{T}{T}f"<b>+{{_intelligence_modifier(char)}}</b> to the total."
{T}{T}{T})
'''.replace(
							"{{_bladesong_uses(char)}}",
							"{_bladesong_uses(char)}",
							).replace(
							"{{_bladesong_ac(char)}}",
							"{_bladesong_ac(char)}",
							).replace(
							"{{_intelligence_modifier(char)}}",
							"{_intelligence_modifier(char)}",
							),
					]
			)


HELPERS = {
		"Artificer": helpers_artificer,
		"Bard": helpers_bard,
		"Monk": helpers_monk,
		"Sorcerer": helpers_sorcerer,
		"Warlock": helpers_warlock,
		"Wizard": helpers_wizard,
		}


def chip_value_name(
		value,
		) -> str:
	if callable(
			value
			):
		name = getattr(
				value,
				"__name__",
				"",
				)
		if name == "<lambda>":
			return "_unarmored_ac"
		return name
	return repr(
			value
			)


def emit_chips(
		chips,
		) -> str | None:
	if not chips:
		return None
	lines = [
			f"{T}chips=(",
			]
	for chip in chips:
		label = chip[
				0
				]
		value = chip[
				1
				]
		symbol = chip[
				2
				] if len(
				chip
				) > 2 else ""
		lines.append(
				f"{T}{T}Chip("
				)
		lines.append(
				f'{T}{T}{T}"{escape(str(symbol))}",'
				)
		lines.append(
				f'{T}{T}{T}"{escape(label)}",'
				)
		lines.append(
				f"{T}{T}{T}{chip_value_name(value)},"
				)
		lines.append(
				f"{T}{T}{T}),"
				)
	lines.append(
			f"{T}{T}),"
			)
	return "\n".join(
			lines
			)


def emit_description(
		description,
		) -> str:
	if callable(
			description
			):
		return f"{T}description={description.__name__},"
	return emit_string_arg(
			"description",
			description or "",
			)


def emit_training(
		binding: str,
		helper: str,
		tag,
		cells: dict,
		) -> str:
	apply = cells.get(
			"apply"
			)
	chips = cells.get(
			"resolved_chips"
			) or ()
	description = cells.get(
			"description"
			)
	parts = [
			f"{binding} = {helper}(",
			f'{T}name="{escape(tag.NAME)}",',
			f"{T}min_level={int(tag.MIN_LEVEL)},",
			emit_description(
					description
					),
			]
	chip_src = emit_chips(
			chips
			)
	if chip_src:
		parts.append(
				chip_src
				)
	if apply is not None:
		parts.append(
				f"{T}apply={apply.__name__},"
				)
	parts.append(
			f"{T})"
			)
	return "\n".join(
			parts
			)


def path_of(
		tag,
		):
	path = tag.PATH
	if path is None or path == "":
		return None
	return str(
			path
			)


def emit_guild(
		guild: str,
		) -> str:
	pyc_name = f"Map_of_{guild}_Training.cpython-314.pyc"
	body, code = load_vault(
			pyc_name
			)
	chunks = [
			DOCS[
					guild
					].rstrip(),
			"",
			"from __future__ import annotations",
			"",
			IMPORTS[
					guild
					],
			"",
			"",
			]
	for name, value in CONSTANTS[
			guild
			]:
		chunks.append(
				f'{name} = "{value}"'
				)
	chunks.append(
			""
			)
	chunks.append(
			HELPERS[
					guild
					]()
			)
	last_path = object()
	for binding in code.co_names:
		tag = body.__dict__.get(
				binding
				)
		if not isinstance(
				tag,
				type,
				):
			continue
		if not hasattr(
				tag,
				"MIN_LEVEL",
				):
			continue
		if not hasattr(
				tag,
				"Awaken",
				):
			continue
		path = path_of(
				tag
				)
		helper = PATH_HELPER[
				guild
				][
				path
				]
		if path != last_path:
			title = SECTION[
					guild
					][
					path
					]
			chunks.append(
					""
					)
			chunks.append(
					"# " + ("-" * 75)
					)
			chunks.append(
					f"# {title}"
					)
			chunks.append(
					"# " + ("-" * 75)
					)
			chunks.append(
					""
					)
			last_path = path
		cells = closure_map(
				tag.Awaken
				)
		chunks.append(
				emit_training(
						binding,
						helper,
						tag,
						cells,
						)
				)
		chunks.append(
				""
				)
	text = "\n".join(
			chunks
			).rstrip() + "\n"
	# Fix accidental double-braces left in source expressions
	return text


def main(
		) -> None:
	for guild in (
			"Artificer",
			"Bard",
			"Monk",
			"Sorcerer",
			"Warlock",
			"Wizard",
			):
		text = emit_guild(
				guild
				)
		target = OUT / f"Map_of_{guild}_Training.py"
		target.write_text(
				text
				)
		print(
				f"wrote {target} ({text.count(chr(10))} lines)"
				)


if __name__ == "__main__":
	main()
