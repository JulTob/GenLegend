# 🧰 Repairs Ledger: every defect the reading found, in one table

> 📜 **Settled.** No chapter is still in flow. 📜 0 · 📚 0 · 📔 8

*Companion to the Mythos pages. Each row was observed in generated output or
read in source on 2026-09-08 in this worktree; line numbers are from that day.
This ledger reports; it does not fix. Rows are ordered by what a player or DM
meets first. "Page" names the Mythos page that explains why it matters.*

## 📔 A. The app cannot do it today (all three are in the path Decree 0004 parks behind `PLAYER_ONLY_PUBLISH`)

| # | What happens | Where | Page |
|---|---|---|---|
| A1 | `summon_nonplayer` fails after five attempts on every call: the vaulted `Grimoire_of_NPC.SetSize` passes two arguments to `Map_of_Size.Size(Type)`, which takes one. The NonPlayer sheet and the DM Companion cannot summon. The running bytecode is longer than the source on disk. | `AtlasActorLudi/AtlasAlusoris/Map_of_NonPlayer_Generation.py` (shim) → vault `Grimoire_of_NPC` line 357; `AtlasActorLudi/Map_of_Size.py:32` | NPCs-and-Villains §1 |
| A2 | `Map_of_Prose_Adventure` and `Charts_of_Choice_Collapse` fail to import: they import `Locus`, `Power`, `Plan` from `Grimoire_of_Adventure`, which defines none. "Generate scene" has nothing behind it. | `AtlasEpica/Map_of_Prose_Adventure.py:23-31` | NPCs-and-Villains §1, §5 |
| A3 | `generate_npcs` calls `NPC.NPC(...)` on the class. | `AtlasAlusoris/Map_of_NPC.py:51` | NPCs-and-Villains §1 |
| A4 | ~~**A Battle Master can fail to generate** (Player path, shipped). Student of War's untrained pick reads tool attributes off `char.skills` (`getattr(char.skills, "Woodworker_Tools")`), which holds no tools; when the seeded shuffle reaches a tool before an untrained skill, `AttributeError` becomes `TagImprintError: Imprint Make_Training.<locals>.Awaken failed`. Reproduced: Tiefling Fighter, seed 974460, levels 13 and 14. Same family as QST-0092 (Assassin).~~ Fixed by QST-0116.1: the sheet has Woodworker's Tools. | `AtlasLusoris/AtlasOfTraining/Map_of_Fighter_Training.py:523-575` | Fighter page; this sweep |

## 📔 B. Wrong on the player sheet

| # | What happens | Where | Page |
|---|---|---|---|
| B1 | Every character speaks Common and Halfling. Species and class branches compare the Character to a string (`char == "Elf"`), never true; the extra language is `set.pop()`, no dice; it is hash-ordered, so one process gave Halfling to every character and the next gave Common Sign Language. | `AtlasLudus/Map_of_Languages.py:1383-1399`, `:1325` | Sheet-Alignment-Languages §3 |
| B2 | The Celestial patron paragraph prints `Descent(kind='Star', names=(…)) of Justice`: the pick from `DESCENTS` is a record with a `names` tuple, formatted whole. | `AtlasLusoris/AtlasOfGuilds/WarlockKit.py:174-187` | Spells-and-Invocations §4 |
| B3 | A level-5 Bard knows Resurrection (level 7) and Find the Path (level 6): the baseline pool takes every level above 0, never capped by slot level. | `AtlasLusoris/Grimoire_of_Spellcasters.py:2502` | Spells-and-Invocations §2 |
| B4 | Sorcerer subclasses add no always-prepared spells (Draconic, Clockwork, Aberrant, Wild Magic); the Warlock branch has them, the Sorcerer branch has none. | `Grimoire_of_Spellcasters.py:1508-1665` | Spells-and-Invocations §2 |
| B5 | Cleric Domain spells are listed in a Feature ("3rd: …") and absent from the spell cards. | `AtlasLusoris/AtlasOfTraining/Map_of_Cleric_Training.py:511+` | Spells-and-Invocations §2 |
| B6 | Agonizing Blast, Eldritch Spear, Repelling Blast print "Choose one of your known Warlock cantrips"; the choice is recorded in `enhanced_cantrips` and never printed. Lessons of the First Ones prints "(see Origin Feats in FeaturesKit)". | `AtlasLusoris/AtlasOfInvocations/Map_of_Eldritch_Invocations.py` | Spells-and-Invocations §4; Feature-Text canon |
| B7 | Human male name lists have never fired: `MALE = "Je" in Type`. | `AtlasNomina/Races/Human.py:5` | Names §4 |
| B8 | Tieflings print a trailing space: `Fiend.Surnames` returns `[""]`. Decision pending on the family name; the space is a bug either way. | `AtlasNomina/Races/Fiend.py:961-963`; `Map_of_Names.py` default `f"{name} {surname}"` | Names §4 |
| B9 | Two Fiend names fused by missing commas (`"Honesty" "Zephyron"`, `"Honesty" "Honor"`); `Ravenwatcherg` in the Elf surname list. | `AtlasNomina/Races/Fiend.py:21`; `AtlasNomina/Races/Elf.py:391` | Names §4 |
| B10 | Story templates hard-code a pronoun ("Known for her fearless resolve … prides herself"; "channels her fighting spirit"). | `AtlasEpica/Map_of_Stories.py:845-846` | Stories-and-Titles §2 |
| B11 | Titles title-case the particles: "The Phoenix Of The Swan Shrine". | `AtlasEpica/Map_of_Titles.py:89-101` (`custom_cases`) | Stories-and-Titles §7 |
| B12 | `Noble {FullName}` for a They Noble reads as a rank. | `AtlasNomina/Map_of_Names.py` (Noble prefix branch) | Names §5 |
| B13 | Epic Boon texts abbreviated ("+1 to any ability (max 30)", "PB", "Re-charges"); "Once you use this benefit. (once per Long Rest)" is a broken sentence. | `AtlasLusoris/Grimoire_of_Features/__init__.py:303-540` | Feats §5 |
| B14 | "Intellicence" in the Ability Score Improvement feats. | `Grimoire_of_Features/__init__.py:329-339` | Feats §1 |
| B15 | Weapons print with no description (2 of 38 have one); shields are personalised, weapons are not. | `AtlasInventarium/Ledger_of_Weapons.py` | Equipment-and-Masteries §3 |
| B16 | 2014-layer leaks on class sheets: Paladin "Abjure Enemy" with literal "CHA"; Sorcerer "see PHB '24 pp145-150"; Rogue "Arcane Trickster: 3"; Druid double Primal Order; Ranger "You adopt the Hunter specialization" and duplicate Hunter's Lore; Wizard duplicate Spellbook; Monk blurbs; Bard PHB paragraphs verbatim; Fighter triple-pasted lines. | `AtlasLusoris/Map_of_Classes/Training/*.py` | each Guild page §8 |
| B17 | ~~The sixteen official backgrounds print the stubs the 2026-08-29 recovery left: a one-sentence description, no Hook, and in fifteen of them an old hook title where the background's name belongs (the Guard renders as "Watcher's Eye", the Soldier as "Military Rank"). The settled text is on the page.~~ Fixed by QST-0122.2. | `AtlasLusoris/BackgroundKit.py` (the sixteen `_Build_Player_Handbook_Background` records) | Backgrounds-Official §3, §4 |
| B18 | Em-dashes in rules text on the sheet: 98 sites across the Training maps and feat maps (35 in `Map_of_Official_Origin_Feats.py`, 9 in `Map_of_Paladin_Training.py`, 7 in `Map_of_Druid_Training.py`); 18 features carried one across 29 swept sheets. The Dialogs call this "against the formatting law." | `AtlasLusoris/AtlasOfTraining/*.py`, `AtlasOfFeatures/Map_of_Official_Origin_Feats.py` | Feature-Text canon; Dialogs 0016, 0018 |
| B19 | Open-choice phrases ("of your choice", "Choose one/two") at 79 source sites; 35 hits across 29 swept sheets (Expertise, Otherworldly Glamour, Metamagic Options…). Some are in-play choices and stay; most are elections the generator already made. | `Map_of_General_Feats.py` (8), `Map_of_Classes/Training/Warlock.py` (7), `Map_of_Bard_Training.py` (6), `Map_of_Barbarian_Training.py` (6)… | Feature-Text canon; QST-0067 |
| B20 | "a Aasimar" in a Story ("{name} is a young {species}"): the article does not agree with a vowel. | `AtlasEpica/Map_of_Stories.py` (Archetype: "a young {species}") | Stories-and-Titles |
| F. The feats, one Questa each (2026-09-10) |
| --- |
| Every feat defect below now has its own open Questa: QST-0095 two Dark Gifts crash · QST-0096 Blessed and Druidic Warrior grant nothing · QST-0097 Magic Initiate grants nothing · QST-0098 four General feats drop a benefit · QST-0099 Strong_Arm's degraded copy is live · QST-0100 Dragon Cult Initiate's language branch · QST-0101 the General catalogue is orphaned · QST-0102 the Epic Boon map declares nothing · QST-0103 legacy Lucky crashes · QST-0104 Arcane Infiltrator does not exist · QST-0105 Boon of Truesight · QST-0106 Blind Fighting states no rule · QST-0107 the Dark Gift lines · QST-0108 the rebrands do not name what they rename · QST-0109 Field Marshal, a design question for the Agora. Resilient was already QST-0067. |

| B21 | Goliath `Fire's Burn` and `Frost's Chill` print without the rule's "can", so an optional rider reads as mandatory: *"you deal an extra 1d10 Fire damage"* where the rule is *"you can deal"*. A use would be spent on every damaging hit. Their four sibling options all keep "you can". | `AtlasActorLudi/SpeciesKit/Goliaths/` (the options' `EFFECT` strings) | Goliath chapter 0 |
| B22 | Halfling Nimbleness renders "at least one size larger than you" where the 2024 rule is "a size larger than you", a single step. The constant is named `MINIMUM_RELATIVE_SIZE`, so this may be deliberate; undeclared either way. A Small Halfling may currently move through Large, Huge and Gargantuan creatures as well as Medium. | `AtlasActorLudi/SpeciesKit/Halflings/` | Halfling chapter 0 |
| B23 | **Resilient never grants the saving-throw proficiency**, which is the entire feat. It is described and not applied: no `training=` and no `apply=`. Already named by QST-0067. | `AtlasLusoris/AtlasOfFeats/Map_of_General_Feats.py` | Feats §4 · **QST-0067 (already open)** |
| B24 | **Blessed Warrior and Druidic Warrior grant nothing.** `Make_Fighting_Style` accepts an optional `apply=` and neither declaration passes one, so each awakens as a paragraph of text with no cantrips. The legacy copy of Druidic Warrior at least sampled two Druid cantrips. | `AtlasLusoris/AtlasOfFeats/Map_of_Fighting_Styles.py` | Feats §4 · **QST-0096** |
| B25 | **Magic Initiate (Cleric, Druid, Wizard) grants nothing**: no cantrips, no level-1 spell, no use tracking. The published "you can also cast it using spell slots" and the spellcasting-ability clause are absent from the text as well. | `AtlasLusoris/FeaturesKit.py` | Feats §4 · **QST-0097** |
| B26 | Benefits silently dropped from published General feats: Athlete's Climb Speed, Dual Wielder's Quick Draw, Medium Armor Master's Stealth benefit and armour prerequisite, Ritual Caster's ritual casting. | `Map_of_General_Feats.py` | Feats §4 · **QST-0098** |
| B27 | Dragon Cult Initiate's Dragon's Tongue is half implemented: `_grant_language` is called unconditionally and de-duplicates silently, so the published "if you already know Draconic, you instead learn one language of your choice" branch never fires. | `AtlasOfFeatures/Map_of_Official_Origin_Feats.py` | Feats §4 · **QST-0100** |
| B28 | **`Strong_Arm` is defined twice and the surviving copy is the degraded one.** The dead copy carries the `<br>` before "On My Mark"; the live copy does not, so the feat prints its two sub-benefits run together. Supersedes the earlier note that recorded only the duplication. | `Map_of_Official_Origin_Feats.py` lines 864 and 2021 | Feats §6 · **QST-0099** |
| B29 | **Two Dark Gifts crash on apply.** Echoing Soul and Symbiotic Being import `STANDARD_LANGUAGES` from `AtlasLudus.Map_of_Languages`, a name that exists nowhere in the repository. Measured: 4 per cent of seeded level-1 Humans fail to generate. | `Map_of_Official_Origin_Feats.py` | Feats §6 · **QST-0095** |
| B30 | **The General feat catalogue is orphaned.** Nothing outside `AtlasOfFeats/` imports `FeatKit`, so its gated, prerequisite-checking path runs only in its own self-test. The live level 4, 8, 12 and 16 draw is `ApplyRandomFeats` in `Grimoire_of_Features`, reading a different catalogue. | `AtlasLusoris/FeatKit.py`, `Grimoire_of_Features/__init__.py` | Feats §6 · **QST-0101** |
| B31 | Legacy `Lucky()` in `Grimoire_of_Features` raises `NameError` on `char` if called: the description interpolates a Character at build time rather than at apply time. Dead today, a landmine for anyone reaching for the legacy factory. | `Grimoire_of_Features/__init__.py` | Feats §2 · **QST-0103** |
| B32 | **Arcane Infiltrator does not exist.** It is named as the Agent of the Ninth Quill's Origin feat and is implemented nowhere. | `AtlasOfBackgrounds/Map_of_Arcana_Unleashed_Backgrounds.py` | Feats §5 · **QST-0104** |

## 📔 C. Breaks the replay or the Dice doctrine

| # | What happens | Where | Page |
|---|---|---|---|
| C1 | `NewName` and `Namer` seed the **global** `random` with the Character's seed. | `AtlasNomina/Map_of_Names.py:360, 368, 569, 593` | Names §1 |
| C2 | `ApplyEpicBoon` draws with `random.sample` and prints "Epic Boom!" (also line 380 for damage types). | `Grimoire_of_Features/__init__.py:555, 644-645, 380` | Feats §5 |
| C3 | Language draw by `set.pop()` (see B1): hash-ordered, not the Character's. | `Map_of_Languages.py:1325` | Sheet-Alignment-Languages §3 |
| C4 | Legacy `NPC.alignment` assigns the drawn alignment and returns a local "Neutral". | `AtlasAlusoris/Grimoire_of_NPC.py:65-77` | NPCs-and-Villains §1 |
| C5 | Legacy NPC story always empty: `SetMyStory` swallows the `TypeError` from `~npc`. | `Grimoire_of_NPC.py:529-535`; `AtlasActorLudi/Map_of_Stories.py` | NPCs-and-Villains §1 |

## 📔 D. Duplicates and dead files

| # | What | Where |
|---|---|---|
| D1 | `Strong_Arm` defined twice; the second wins. | `AtlasLusoris/AtlasOfFeatures/Map_of_Official_Origin_Feats.py:864, 2021` |
| D2 | Two copies of the Titles vocabulary (9,470 and 10,049 lines). | `AtlasNomina/Map_of_Titles.py`, `AtlasEpica/Map_of_Titles.py` |
| D3 | Two copies of the Story engine (2,940 and 2,889 lines). | `AtlasActorLudi/Map_of_Stories.py`, `AtlasEpica/Map_of_Stories.py` |
| D4 | Two spell registries: 319 `Spell` instances and a 136-entry compressed dict in the same file. | `AtlasMagia/Lodge_of_Spells.py` |
| D5 | Fighting Styles defined twice. | `AtlasOfFeats/Map_of_Fighting_Styles.py`; `Grimoire_of_Features` |
| D6 | `Map_of_Epic_Boons.py` binds all twelve names to `None`, so `_EPIC_BOON_DECLARATIONS` stays empty and the entire TagKit boon path, including its real level-19 precondition, is dead. The texts that reach a sheet live in `Grimoire_of_Features`. | `AtlasLusoris/AtlasOfFeats/Map_of_Epic_Boons.py` |
| D7 | `HumanLegacy.py` (7,105 lines) imported by nothing; `Kit_of_Elvish.py` imported by nothing. | `AtlasNomina/Races/HumanLegacy.py`; `AtlasNomina/AtlasScriptum/Kit_of_Elvish.py` |
| D8 | Monk Focus techniques live in the Lodge of Spells. | `Lodge_of_Spells.py:7083+` |
| D9 | Orphaned `("greece", …)` prayer keys; two dead keys, six silent markers, three broken lines. | `Map_of_Cleric_Prayers.py` (Cleric page) |
| D10 | `Documenta/Sources/Jedi` cited by the Psi Warrior commentary is gone. | Fighter page |
| D11 | Rogue legacy Training adds two `AddAnyLanguage` calls (2024 grants one). | `AtlasLusoris/Map_of_Classes/Training/Rogue.py:49-51` |
| D12 | The design documents live in two trees: `Curia/` (188 files; Decrees 0001-0004, 0007, 0008; Agentia, Consuls, Vademecum) and `Documenta/` (133 files; Decrees 0005-0006; Sources; this Mythos). Decree 0002, cited by code and Questae as the Dice doctrine, resolves only in `Curia`. | `Curia/Agora/Decrees/0002-character-root-and-dice.md` |

## 📔 E. Design gaps that read as defects (decisions, not bugs)

| # | What | Page |
|---|---|---|
| E1 | The written backgrounds have zero gates in the Story engine; the story never reads the hook. | Stories-and-Titles §3 |
| E2 | Species Goals and Origins in the Story engine contradict the canon (bloodline curse, celestial mission, silver dragon, scattered clans, old hatreds). | Stories-and-Titles §4 |
| E3 | The Celestial NPC table is the 2014 canon; "Tiefling" is a Fiend kind. | NPCs-and-Villains §2 |
| E4 | Spell draws uniform; invocations ignore the patron. Decree 0005 §1 says affinity weights what a character receives; this is the largest selection it does not yet weight. | Spells-and-Invocations §2-4 |
| E5 | No wonder is ever bought (purse ~30 gp at every level). | Equipment-and-Masteries §2 |
| E6 | A third of player characters Evil by uniform draw. | Sheet-Alignment-Languages §2 |
| E7 | Dark Gift docstrings are the lines and never reach the sheet. | Feats §3 |
| E8 | Draconic Sorcerer draws no ancestry; Wild Magic Surge table absent. | Sorcerer page |
| E9 | Goliath `son` patronymic; Elf surnames off-culture; Halfling food names. | Names §4 |

## 📔 G. The random sweep (30 seeds, 2026-09-08)

Thirty random species × Guild × level × seed summons: 29 generated, 1 crashed
(A4). Across the 29 sheets: 35 open-choice hits (B19), 18 em-dash features
(B18), 11 titles with capitalised particles (B11), 9 empty Darkvision entries
(the chip-only convention, README open item), 3 bare stat abbreviations (B16),
2 pronoun mismatches on They characters (B10), 2 Tiefling names ending in a
space (B8), 1 book reference (B16), 1 "a Aasimar" (B20). The sweep script lives
in the session scratchpad, not the repository. A second sweep of sixty seeds at
levels 3 to 20 generated 60 of 60, so the Battle Master failure (A4) is
seed-dependent: about one in ninety across the two sweeps.

## 📔 How this ledger was made

Every A and B row was reproduced from generated output in this worktree
(`summon_player`, `summon_nonplayer`, `spellcaster`, the Story and Title
composers), then traced to source. C and D rows were read in source. E rows are
design findings whose pages carry the argument. Verification commands used are
recorded in the session; the dump scripts live in the session scratchpad and
are not part of the repository.

## 📔 F. Where a Questa already exists

| Ledger row | Questa | Note |
|---|---|---|
| A1, A3 | QST-0075 Restore the NonPlayer public surface; QST-0084, QST-0085, QST-0086 Unhide NPC Generator / List, Wire DM tools; QST-0093.7 the Player path off legacy Alusoris; QST-0079 vault survey | The `Size` call is the concrete blocker none of them names yet. |
| A2 | QST-0086 Wire DM/Magistratum Tools | The missing `Locus`/`Power`/`Plan` are the concrete blocker. |
| B2 | QST-0054 Warlock patron features are a 2014/2024 mixture | The `Descent` repr is new; so is the 2014 Genie patron (Dao, Djinni, Efreeti, Marid) still drawn in `Grimoire_of_Spellcasters.py:2270-2310`, which QST-0054 does not yet name. |
| B3 | QST-0071 Wizard spell counts ignore the Wizard table; QST-0059 verify spell texts | The Bard's cap is the sibling defect. |
| B5, B6 | QST-0057 Granted spells belong in the Magic section; QST-0069 feat-granted spells; QST-0067 Chef and Resilient must resolve, record and print their choices | The enhanced cantrip is the same rule as QST-0067. |
| B8 | **QST-0052 Generated names can carry a trailing space** | Open already; the Fiend empty surname is the cause. |
| B16 | QST-0051, QST-0055, QST-0062, QST-0094 (voice); QST-0054 (Warlock) | The 2014 leaks per Guild page. |
| Species inspiration lines (every people page) | QST-0094 Species entries speak the rulebook's present voice ("inspiration lines and two conventions await the author") | The lines drafted on the people pages belong in that Questa's lane. |
| B15 | QST-0060 Sheet presentation; QST-0046.12 re-evaluate the item system | |
| C1, C2, C3 | QST-0089 Monk and Ranger training Maps call `random`; QST-0016.6.1 seeded replay | Three more global-`random` sites. |
| C5 | QST-0077 `Map_of_Stories.Name()` silently failed on every character | The NPC branch of the same silence. |
| D12 | QST-0093.9 Station 9: one Documenta | Decree 0002 is in `Curia`. |
| E1 | QST-0064.1 Practices as Adventure Hooks | Adjacent: hooks as engine inputs. |
| E3 | QST-0050 A CelestialKit shared by Player Species and the NPC generator | The Ideal × Descent proposal is that Kit's content. |
| E5 | QST-0046.9 Starting wealth tracks the money-per-level curve; QST-0046.10 worn wealth | |
| Orders voice | QST-0061 The Order background: too many entries, and the voice is off | |
| B1, B7, B9, B10, B11, B12, D1-D8 | none found | New. |
