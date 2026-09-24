# 🔌 Wiring Plan: how the drafted lines reach the sheet

> 📜 **Settled.** No chapter is still in flow. 📜 0 · 📚 2 · 📔 2

*Wiki entry for the design team. The Lines Annex holds every inspiration line
the Mythos pages drafted. The coverage sweep shows the sheet prints a line for
41% of class Training features and 0% of feats, while 62 of the 63 lineless
Training features on six level-20 sheets already have a line in the annex. This
page says how a line becomes sheet text, layer by layer, and proposes the
Questae. Nothing here is done; it is the map for doing it. 2026-09-08.*

---

## 📚 1. The shape, per layer

The house shape already exists and is used by four Guilds. A line is the first
thing in a Feature's description, italic, followed by a blank line, then the
rule. Nothing infers it at render time (Feature-Text canon: breaks are written,
never inferred).

| Layer | Where the text lives | The shape today | What wiring means |
|---|---|---|---|
| **Class Training** | `AtlasLusoris/AtlasOfTraining/Map_of_<Guild>_Training.py` | `"*You don't stay down. You fight.*\n\n"` + rule (Fighter, Barbarian) | Prepend the annex line in that form to each `description`. Templated Features (the Orders' Sign) take it once in the builder. |
| **Specializations** | `AtlasLusoris/AtlasOfGuilds/<Guild>Kit.py` (`Make_Specialization`) | Barbarian, Fighter, Warlock, Cleric carry prose; nine are bare | The Dialogs' provisional paragraphs (Bard, Cleric, Druid, Monk, Artificer) plus the Guild pages' drafts; wire after the project's word on each Dialog. |
| **Species traits** | `AtlasActorLudi/SpeciesKit/<People>/resolution.py` | The line is the plain first sentence of the entry ("Something in you remembers what a body is supposed to feel like…") | Prepend the annex line as the first sentence where the entry opens on a rule. QST-0094 is the lane ("inspiration lines… await the author"). |
| **Origin feats** | `AtlasLusoris/AtlasOfFeatures/Map_of_Official_Origin_Feats.py` (`DESCRIPTION`) and `FeaturesKit.py` | Skilled and Skillful carry a line; the rest do not; the Dark Gifts carry theirs as docstrings | Move each Dark Gift docstring into its `DESCRIPTION` in the house form; one line per setting feat from the Feats page. |
| **General feats, ASI** | `AtlasLusoris/AtlasOfFeats/Map_of_General_Feats.py`; `Grimoire_of_Features/__init__.py` (`Feat("Increased Strength", …)`) | Rules only | Prepend the Feats page §4 lines. |
| **Epic Boons** | `Grimoire_of_Features/__init__.py` lines 303 to 540 (`Map_of_Epic_Boons.py` is empty) | Abbreviated rules | Write the rules out, prepend the Feats page §5 lines; decide which file owns them. |
| **Invocations** | `AtlasLusoris/AtlasOfInvocations/Map_of_Eldritch_Invocations.py` (`Make_Invocation(description=…)`) | Rules only | Prepend the Spells page §4 clause lines. |
| **Weapon Mastery** | `AtlasLusoris/Map_of_Weapon_Masteries.py` (`weapon_mastery_entry`, `mastery_blurb`) | "*You feel comfortable with the weapons you trained with.*" | Replace the opening line; prepend a property line to each `mastery_blurb`. |
| **Spellcasting openings** | `Grimoire_of_Spellcasters.py` (each class's `__str__`) | "As a student of arcane magic, you have learned to cast spells." | Replace with the Spells page §5 openings. |
| **Alignment chip** | `AlignmentKit.py` / the sheet's chip | Value only | A chip carries no prose; the nine lines (Sheet page §2) need a small Entry beside the chip, or a tooltip. Design call. |
| **Story** | `AtlasEpica/Map_of_Stories.py` (`Myth` dict) | Gated `(gate, text)` rows | Add the twenty Origin rows gated on the written backgrounds and ten Outro rows gated on species; cut the contradicting Goals. |
| **Frame copy** | `app/publish_scope.py`, `app/pages/*.py` | Labels and one lede | Replace the five sentences (Brand page §2) once the author picks a variation. |

**Two rules to keep while wiring.**

- **Resolved numbers stay resolved.** A line never carries a number; the rule
  under it does, and the rule keeps its callables (Entry as projection).
- **One register per Guild.** The annex groups lines by page; a line moved
  across Guilds changes voice. Wire by page, not by feature name.

---

## 📔 2. Order of work, by coverage

The coverage sweep (README) gives the order: lowest share first, because that
is where a user meets the most silence.

| Questa (proposed) | Scope | Lines in the annex | Coverage today | Acceptance |
|---|---|---|---|---|
| Lines: Bard | 26 Training features | Bard-and-Sorcerer-Lines | 10% | ≥ 85% of Bard Training features open on a line |
| Lines: Sorcerer | 28 Training features | Bard-and-Sorcerer-Lines | 19% | ≥ 85% |
| Lines: Monk | Training | Monk page | 33% | ≥ 85% |
| Lines: Rogue | Training | Rogue page | 34% | ≥ 85% |
| Lines: Ranger | Training | Ranger page | 37% | ≥ 85% |
| Lines: Wizard, Artificer, Paladin | Training | their pages | 42–45% | ≥ 85% |
| Lines: feats and Boons | 45 General feats, 12 Boons, ASI, Origin feats, Dark Gifts | Feats page | 0% / 37% | every feat opens on a line |
| Lines: invocations and masteries | 28 invocations, 8 properties, the opening | Spells page §4, Equipment page §4 | 27% / one weak line | every clause opens on a line |
| Lines: species | traits opening on a rule, all ten peoples | people pages; QST-0094 | 58% | ≥ 85%, Darkvision convention decided |
| Story: gates | twenty Origins, ten Outros, the cut Goals | Stories page §8 | 0 gates for written backgrounds | every written background has ≥ 1 Origin |

Each Questa's test is the coverage sweep re-run on the same seeds: a number
before, a number after, in the Questa's rationale. The sweep script is in the
session scratchpad and belongs in `scripts/` once wanted it.

---

## 📔 3. What wiring must not do

- **Not explain.** A line names the feeling or the fact; it never says why the
  people or the Guild is the way it is (the canon's first rule, four times).
- **Not lock a choice.** The line may not reintroduce "of your choice" or a
  pronoun; it is written for the second person and any gender.
- **Not carry a number.** If a draft line has one (a few in the annex do), the
  number goes back into the rule.
- **Not cross registers.** The Fighter's yard is not the Monk's breath; the
  annex's page grouping is the guard.
- **Not print twice.** Where a Feature's text is built in `awaken` (the
  Crafter pattern), the line goes into the resolved text, not only the constant.

---

## 📚 4. Pointers

- **Lines-Annex**: the lines.
- **README, Voice coverage**: the numbers this plan moves.
- **Feature-Text canon**: breaks written, numbers resolved, no open choice.
- **Fighter page**: the wired shape, as it ships.
- **QST-0094**: the species lane; **QST-0062**: the voice sweep.
