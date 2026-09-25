# ⛏️ Dwarf

> 📖 **In flow.** 2 of 12 chapters are still proposals. 📚 4 · 📔 6 · 📖 2

> - 📕 **inherited from the 2024 rules.** Moving it costs rules compatibility.
> - 📙 **an aesthetic change.** The same rule wearing our name and look.
> - 📒 **a rule we changed.** A house rule, and it already cost compatibility.
> - 📘 **supportive lore.** It holds a rule or a core element up.
> - 📗 **deep lore.** Design that supports the fantasy rather than a rule.
> - A book marks a statement only if it can change exclusively through the
>   Questa / Agora / Decree system. Anything with no Questa and no Decree behind
>   it carries no book, however settled it feels.

*Wiki entry for the design team. Deep lore and settled direction, not page text.
Compiled 2026-09-08 from the Dwarf kit, the species entry, `Cultural-Inspirations.md`,
the old wiki's Dwarf paragraph, the class analyses, and QST-0094. Where the project owner
has decided, the decision is stated as such; where this page proposes, it says so.*

> **In one sentence.** **Gold, Faith, and Clan:** dwarves once ruled the world,
> until the Great Empire fell; now its scattered heirs carry their saints and
> metals from mountain holds and bank-cathedrals to the buccaneer sea.

---

## 📚 0. Rules

*The fixed points, and what we made of them. The books are defined at the head
of the page.*

### The rules as given

*Each entry is the rule itself, complete enough to resolve at a table. Not a
summary and not a cross-reference.*

> 📕 **Creature Type** Humanoid. **Size** Medium, with nothing to choose: the kit
> offers one option and never rolls for it. **Speed** 30 feet (Walking Speed).
> **Heritages** none. The Dwarf makes no ancestry, heritage or lineage choice, so
> a Dwarf never appears in the heritage tables. That is correct for 2024.
>
> 📕 **Darkvision.** You have Darkvision with a range of 120 feet. You can see in
> Dim Light within 120 feet as if it were Bright Light. In Darkness within that
> range you can see as if it were Dim Light: within that Darkness you have
> Disadvantage on Wisdom (Perception) checks that rely on sight, and you discern
> colors there only as shades of gray.
> > _Your eyes remember the mountain._ (recovered authored text, not wired;
> > awaiting ratification in §9)
>
> 📕 **Dwarven Resilience.** You have Resistance to Poison damage (you take half
> damage from it, rounded down, and the halving applies after all other modifiers
> to that damage). You also have Advantage on saving throws you make to avoid or
> end the Poisoned condition. The Advantage is on the condition, not on poison as
> a damage type: it covers both the save to avoid becoming Poisoned and any save
> to end it. No limit on uses, no recharge.
> > _What you consider spicy could kill an elf. A dwarven diet made your body
> > hard to poison._ (recovered authored text, not wired; awaiting ratification
> > in §9)
>
> 📕 **Dwarven Toughness.** Your Hit Point maximum increases by 1, and it
> increases by 1 again whenever you gain a level. At Level N your Hit Point
> maximum is therefore N higher than it would otherwise be (+1 at Level 1, +5 at
> Level 5, +20 at Level 20). This stacks with, and is calculated separately from,
> the Constitution modifier you add per level.
> > _Your Nana used to say: Dwarves eat beyond full, and work beyond exhaustion,
> > so have another bowl._ (recovered authored text, not wired; awaiting
> > ratification in §9)
>
> 📕 **Stonecunning.** As a Bonus Action, you gain Tremorsense with a range of 60
> feet for 10 minutes. You must be on a stone surface or touching a stone surface
> to use this Bonus Action; the stone can be natural or worked. You can use this
> Bonus Action a number of times equal to your Proficiency Bonus (2 at Levels
> 1-4, 3 at 5-8, 4 at 9-12, 5 at 13-16, 6 at 17-20), and you regain all expended
> uses when you finish a Long Rest.
> > _Your history is written in stone, so you read the stories stone tells._
> > (recovered authored text, not wired; awaiting ratification in §9)

No rule of the Dwarf has been changed, so this page carries no 📒. All four
traits also keep their published names, so there is no 📙 either: the Dwarf is
four inherited rules and nothing else.

Two absences, one addition and one wording, stated rather than left silent.

**The absences.** The kit grants the Dwarf no language, which is right for 2024,
where languages come from the origin and not from the species. And Stonecunning's
uses are printed but never spent: the sheet states the allowance and the
recharge, and no ledger in the app consumes a use. That is the project's
convention for every per-rest trait (the Orc's Adrenaline Rush and the Aasimar's
Healing Hands are recorded the same way), not a change to the rule. The sheet
records the allowance; the table spends it.

**The addition.** The 2024 Darkvision glossary entry does not print the
Disadvantage clause. It follows from Darkness seen as Dim Light being Lightly
Obscured, and the kit prints it because a player reading the sheet would
otherwise assume Darkvision cancels the penalty. Derived, not changed, so still
📕 and no 📒.

**The wording.** The published Stonecunning puts the stone contact on *using the
Bonus Action*; the kit's projected entry reads "to use this Tremorsense", which a
table will read as a condition on keeping the sense rather than on starting it.
Ten minutes of Tremorsense is a long time to hold a wall. The entry above states
the published scope. This is a projection to correct in `Dwarves/resolution.py`,
not a house rule, and it carries no 📒 because nothing was decided.

### The supportive lore

> 📘 **The Dwarves are the setting's Iberian people, Iberian shaped by the
> Umayyads.** They hold two keys, `iberia` and `andalus`, and the two are never
> fused: a species holds a *list* of keys and does not get a blend. The overlap,
> and the reach into neighbours, is modelled by influence rather than by merging,
> so a Dwarf reaches a neighbour without that culture being folded into Iberia.
> Toledo is Dwarf vocabulary by the `iberia` key, beside its Andalusi and
> Maghrebi neighbours. Dwarves and Gnomes cohabit.
> Ratified by **QST-0046.2**, which lives in `Curia/Questae/Working/` rather than
> under `Documenta/Questae/`: the legacy half of the same system, pending the
> folder merge QST-0093.9. QST-0046.5 lists it as Related, so the identifier is
> live.
>
> 📘 **Every culture marker is a real culture named for itself.** There are no
> invented middle grounds, and a species that sits between traditions holds both
> markers instead of a merged one. Legend markers stand beside the real keys and
> feed the same reach map, `folklore_dwarf` among them, so a name is one roll
> across both families.
> Ratified by **QST-0046.5**.
>
> 📘 **Dwarves lean to metals, and the lean is extra weight, never a closed
> door.** Jewels and gems lean the same way to the Gnomes. Legend markers are
> where mithril and its like live, so mithril reaches the Dwarf through a legend
> register rather than through either of its real culture keys. Leanings, not
> laws.
> Ratified by **QST-0046.6**.
>
> 📘 **Saints belong to the Dwarves and stay out of the Celestials' system.** They
> were deliberately removed from the Celestial descents, because mixing the two
> reads as one system when they are two. The Aasimar's talaria take the metal and
> nod at the dwarven soul-metal without confirming anything, and that ambiguity is
> deliberate space for a DM.
> Ratified by **QST-0050**.
>
> 📘 **The species entry speaks in the first person plural, and its content is the
> Iberian and Hispanic roots, the clans, the gold and the soul-metals, and the
> Saints.** The rule voice of the four trait entries is settled with it: the 2024
> rulebook's present tense, with no level announcement. The four inspiration lines
> of §9 are proposals in that same round and are *not* settled text, so this
> page's "Awaiting ratification" label on them is correct.
> Ratified by **QST-0094**.
>
> 📘 **Martial and technique fantasy draws on Iberian and Eastern traditions
> rather than Germanic fechtbücher.** This is the standing ruling behind the
> Iberian half of the Dwarf's register, and it is the only part of that register
> with formal footing.
> Recorded as standing in the Agora Dialogs **0013** (Artificer), **0015**
> (Bard), **0016** (Cleric) and **0018** (Monk). It governs which wells a class
> text may draw on; it names no people, and it attributes nothing to the Dwarf.

That is the whole of the supportive lore this page can currently mark. Everything
else below rests on the shipping species entry, the canon documents, the old
wiki's Dwarf paragraph and this page's own decisions log. The canon documents are
explicitly outside the Questa / Agora / Decree system, so those claims carry no
book until a Questa says otherwise.

### What the rules force, and what we chose

Stonecunning is the demanding one. It forces a body that senses through stone, on
contact, in bursts of ten minutes, a number of bursts that grows with the
character. Dwarven Toughness forces a second thing across a whole career: a Hit
Point maximum that rises by one every level and never falls.

Our answer is **the metal, given and proven**. The four traits are read as proof
accumulated in a body, not as blood inherited. Toughness is the ledger, one line
a year and none struck out. Resilience is the mine air and the smelter's fumes,
survived. Stonecunning is attention paid to a mountain that still keeps the
accounts. Darkvision at 120 feet is the mine in the body.

**What that buys beyond the rule.** Stonecunning's stone contact stops being an
arbitrary restriction: the Dwarf and the land stand in a debt relationship, so a
hand on the wall is a creditor being asked. Toughness's one point per level
acquires a subject, because a number that only ever grows is a ledger line, and
that is the species' voice exactly. Resilience reads as something survived rather
than something in the blood, which is what keeps the species law's
taught-not-inherited reading intact where a heritable immunity would read as
inherited character. Sainthood gets its content, which is what makes the
separation of Saints from the Celestials worth defending instead of a naming
accident, and it is that content the talaria's metals nod at without confirming.
And the range ties the history to a number: at 120 feet a Dwarf sees as far into
the dark as anyone on the roster does, which is the right answer for the people
who lived down there longest. It is not a claim to be deepest, because the Orc
and three Elf lineages see just as far, and it must never be written as one.

⚠️ **What breaks if a later hand removes the metal as flavour.** Stonecunning
becomes a radar with a pointless restriction attached. Toughness becomes a bare
number with nothing to say for itself, and the ledger goes with it. Resilience
falls back on blood, the one reading the species law refuses. The clan's
absolution loses its subject, because gold proves the metal, and without the
metal it is only money. Sainthood empties, and the deliberate Dwarf and Celestial
ambiguity empties with it: ratified space (QST-0050) resting on unratified lore.
That imbalance is an argument for writing the Questa, not for treating the metal
as free.

### The variable detail

Drawn per character: the name, long and compound, Iberian and Italianate, with a
surname that reads like a ledger line; which of the two keys the gear and the
vocabulary come from, and how far the reach map carries (from `iberia` to
`andalus`, Carthage, the Celts and Rome; from `andalus` to the Maghreb, `iberia`,
the Levant and Persia); whether a legend marker fires and which one, so mithril
mail and the tapping hammer are in reach without a real culture claiming them;
the material lean toward metals; and the Cleric prayer. Nothing lineage-shaped is
drawn at all, because the Dwarf has no heritage choice to make, and the one size
option is taken rather than rolled.

None of it was filled in at random, and part of it is ratified rather than
merely reasoned: each key is a real culture named for itself and never a blend
(QST-0046.5), the reach map is what lets a Dwarf touch a neighbour without
merging it (QST-0046.2), and the metal lean is extra weight rather than a closed
door (QST-0046.6). The name module is the exception. Its four inspirations carry
no book, and one of them, Renaissance Italy, belongs to the Gnome on the culture
map, so that draw is in tension with the keys until a Questa aligns them.

---

## 📚 1. Where the Dwarf lives in the code

| What | Where | State |
|---|---|---|
| Species entry | `AtlasActorLudi/SpeciesKit/Dwarves/__init__.py` | Shipping. First person plural ("we remember"). Closes on what to do with the gold. |
| Traits and rules | `Dwarves/traits.py`, `resolution.py` | Rule voice landed (QST-0094). **No inspiration lines yet**; four were proposed in QST-0094 and await ratification (§9). Darkvision 120, Resilience, Toughness, Stonecunning. |
| Names | `AtlasNomina/Races/Dwarf.py` | Inspirations: the Golden Age of Spain (conquistadores), Renaissance Italy, Portuguese, the Carthaginian empire (Hannibal). |
| Culture keys | `iberia`, `andalus`; legends `folklore_dwarf`, `tolkien_dwarves` | Toledo steel in the Materials map; mithril through the Tolkien register. Dwarves lean to metals through extra weight, never a closed door. |
| Prayer | `Map_of_Cleric_Prayers.py` | *Metal shapes in the forge. People in the challenge.* *A saint is a sinner trying to be better.* *Forgetting is hard, but harder is forgiving.* Plus Life, Knowledge (Cervantes), War (*No hay atajo sin trabajo*), Grave (Teresa of Ávila, Quevedo). |
| Old wiki | `app/Wiki/Lore.html` | The conquistador paragraph: Bank Templars, Basque-inspired Mountain Dwarves, goldsaints and silversaints, the Missing Crown and the Holy Gold. Unedited and repetitive; the source of the lore, not its final form. |
| Metaphysic | `Dragons-and-the-Overcoming.md`, the peoples table | *Platonic soul-metal; Sainthood as transcendence into one's own pure substance.* |

---

## 📔 2. Origin: soul-metal

Each people has one organising idea. The Dwarf's: **a soul is a metal, given,
and it must be proven.** The Celestial's Ideal is fixed and cannot bend; the
Elf drifts by collective consent; the Dragon authors itself alone; the Dwarf's
metal is handed down and then tested, in the forge and in the challenge, until
it is pure or it is not. *"Metal shapes in the forge. People in the
challenge."*

**Sainthood** is the transcendence into one's own pure substance: a Dwarf who
proved the metal all the way down. The goldsaints and silversaints of the old
halls are Dwarves who did. Saints belong to the Dwarves and stay out of the
Celestials' system (QST-0050): two things that look alike from a distance, on
purpose, and are not the same. *"A saint is a sinner trying to be better."*

**The metal shows.** The Aasimar's talaria shine like metals (black iron, gold,
red iron, silver, verdigris, bronze) and confirm nothing; the ambiguity is
deliberate DM space. A Dwarf who notices would say the Celestials borrowed
the idea. A Celestial would say nothing.

**Physical traits.** Darkvision to 120 feet (as deep as anyone on the roster),
resistance to poison, one Hit Point per level, and Stonecunning (tremorsense
on stone). The species law permits biology; these are the mines in the body.

---

## 📚 3. History: the Great Mountain fell

*"Our people ruled the world once. Then the Great Mountain fell, the Gilded Era
ended with it, and the dwarves spread out across the world instead, carrying
their ledgers and their grudges."*

The old wiki fills the shape and the entry keeps the shape only, which is
right: the Gilded Era was an empire of holy rites, engineering, pageantry and
gold, devoted to divine monarchs and its own destiny; hubris and spiritual
fervour shattered it; the people scattered into rival kingdoms and enclaves.
Two survive as names:

- **The Bank Templars**: merchant-keepers of vaults, the bank-cathedrals, the
  fleets and the long terrible expeditions. Commerce and faith in one house.
- **The Mountain Dwarves**: isolationist redoubts, Basque-inspired, keeping the
  old ways and a hard-won solitude.

Two prayers survive as politics: some pray for the **Missing Crown** (the
restoration), some for the **Holy Gold** (the faith without the throne). The
species entry gives the player the third: *"what will you do with the gold you
carry home? Raise a shrine to a Saint? Open a Bank Temple? Or spend it on
spices and mead?"*

**The clan absolves.** *"Come back home with enough gold, and your clan will
hail you as a hero, no matter your past transgressions."* This is the most
consequential sentence in the entry: it forgives the thief, the mercenary and
the exile in advance, and it makes the Dwarf the one people whose adventurer
has a guaranteed homecoming with one condition attached. Every Dwarf
adventurer's story has an accountant at the end of it.

**Others call it greed.** *"They do not understand. Gold never corrupts. A gilded
prayer to our Saints and Ancestors will never weaken."* The Dwarf does not
argue the point; the sentence is doctrine, and the Life prayers argue the other
side from inside (*"Gold held is not living. Gold earned is gold spent."*
*"The real gold is in your soul."*). The species holds both.

---

## 📔 4. Culture: Iberia and Andalus, two keys, one people

**The law:** one key, one culture; Iberia and al-Andalus are two keys, not a
blend, and the overlap is modelled by influence, not by merging. The wiki names
the well: the Spanish-speaking world as an analogy to the old Spanish empire,
itself shaped by Carthage, Rome, the Umayyads, Sefarad, and the Reconquista.
"History is messy."

**Iberia**: Toledo steel, the Cid, Roncevaux on the Dwarf border (the Song of
Roland is set in the Pyrenees against Zaragoza: the Paladin's founding poem
happens at a Dwarf pass), Santiago and Calatrava (the Iberian military orders
are the crusader register on the Iberian key), La Verdadera Destreza (the sword
as geometry: the Open Hand Monk, the Battle Master's *tretas*), the tercio's
*alférez* (the Banneret), Don Quixote (the Glory Paladin: *Living Legend* is
"the legends, whether true or exaggerated"), the picaresque (Lazarillo: the
Rogue's register), the cantigas de escarnio and the romancero (the Bard), the
*Libro de la montería* and the montero (the Ranger), Juanelo Turriano's
*artificio* (the Artificer), the Cueva de Salamanca (the Occultist Warlock;
the Shadow background's lost shadow), Teresa of Ávila, Quevedo and Machado in
the prayers, the Basajaun and Mari of Anboto on the Basque side (the Druid's
teaching wild man and the lady who is the weather).

**Andalus**: Abbas ibn Firnas, who flew over Córdoba (the Artificer), Andalusi
falconry (the Beast Master's falcon), the *baratero*'s navaja (the Shadow
Monk), *"This world is a bridge. We all must cross"* in the Grave prayers, and
the whole register of a civilisation that was the other half of the same
peninsula. The Song of Roland's enemy is this key; the Dwarves carry both sides
of Roncevaux.

**Legends**: `tolkien_dwarves` (rune-axes, delving, mithril mail) and
`folklore_dwarf` (knockers, nisse, the tapping hammer), the latter shared with
the Gnomes.

**Names**: the Golden Age of Spain, Renaissance Italy, Portuguese, Carthage.
The generator's Dwarves are called Elidio Gabibir Elora Martinez, Vivian
Valleja Pedraferra Minacorazón, Etebar Santanitán Ardorerojo Abecero: long,
compound, Iberian and Italianate, a surname like a ledger line.

**Materials**: metals through extra weight (Toledo steel, and mithril through
the Tolkien register); gems lean to the Gnomes. "Leanings, not laws."

---

## 📔 5. Metaphysics: given, proven, spent

**Against the Celestials.** Fixed against given-and-proven: an Aasimar cannot
change the spark; a Dwarf must change the metal. The two peoples are the
setting's two Platonisms and they disagree about whether the Form is finished.
A Dwarf Cleric of Life ("the real gold is in your soul") is the argument said
aloud.

**Against the Dragons.** *"A dwarf who spends ninety years on one gem may
Ascend through the obsession itself, because the obsession was the only thing
in that life that was truly theirs. Seen from outside this looks like a curse,
and the family will describe it that way."* The canon wrote the Dwarf Draconic
Sorcerer before the class did. The Dwarf who proves the metal all the way is a
Saint; the Dwarf who proves *one thing* all the way, alone, is a dragon, and
the clan cannot tell the difference from outside, which is the tragedy.

**Against the Elves.** Given against dreamt. A Dwarf is what the forge made; an
Elf is what the people imagined. "Dwarves and Gnomes trade and share
settlements", and the Gnome is the middle point of the Renaissance pair: the
Dwarf's metals and the Gnome's jewels are one trade route.

**The mountain is owed.** *"Everything we dwarves ever built, we built while
chasing it: the mines."* The Dwarf and the land are in a debt relationship, and
the Great Mountain fell. A Dwarf Druid is the mountain's creditor among a
people of debtors; Stonecunning is attention paid to stone, and the Basajaun
taught the farmers to forge. Deep lore, never on the page: the fall of the
Great Mountain as the covenant's breach.

---

## 📔 6. The classes: what the metal does in each

| Class | The Dwarf in it |
|---|---|
| **Fighter** | *"Metal shapes in the forge. People in the challenge."* The class thesis in the species' mouth. The Banneret is the tercio's alférez, sworn not to let the banner fall: Iberian before anyone's. |
| **Paladin** | The Cid, exiled by his king and still fighting in the king's name ("what a good vassal, if he only had a good lord"); Santiago and Calatrava; Roncevaux on the border. The Glory Paladin is Don Quixote, and *Living Legend* is his feature. |
| **Rogue** | The pícaro: the Thief the clan absolves in advance. A Dwarf who robs a bank-cathedral and brings the gold home is the species' own kind of hero. |
| **Bard** | The cantigas de escarnio in a bank-cathedral; the romancero as the people's memory; the vihuela; Lorca's duende was always the Dwarf's. |
| **Monk** | Destreza without the sword (Open Hand): the circle on the floor is Iberian. The baratero's knife (Shadow). A Monk needs no food; the clan's "come back with enough gold" has no purchase, which is the character. |
| **Wizard** | The ledger. The Spellbook map already draws "a sheaf of steel leaves on a ring, each leaf a page struck rather than written" for Smith's Tools. A Bank Templar who keeps this book. |
| **Artificer** | Juanelo's *artificio*; Abbas ibn Firnas's wings; the Armorer who builds the given metal into armour and steps inside ("what you make with your own hands is yours in a way no gift will ever be" against "metal is holy": the Dwarf who made what the Saints say was given). |
| **Cleric** | The demanding parent is the Dwarf's default: the metal was given so it could be proven. The Dwarf War Cleric needs no reconciliation; the Dwarf Life Cleric argues *"Gold, like life, must be shared and passed on"* against a people who count everything. |
| **Barbarian** | The Zealot taken by a **Saint**, not a god (the Zealot's god should be species-drawn, Barbarian page). Rage as the crucible. |
| **Sorcerer** | The ninety-year gem (§5). Draconic Sorcery as the family's curse. |
| **Druid** | The mountain's creditor; the Basajaun's pupil; Mari's weather. |
| **Ranger** | The montero; the falconer of al-Andalus. |
| **Warlock** | The Cueva de Salamanca: the Devil's school where the last student out pays, and one escaped by leaving his shadow. The Occultist (Intelligence) variant has an Iberian home; a Dwarf with the Shadow background is the Salamanca student. A Dwarf Warlock's gold has a lien on it. |

---

## 📔 7. Backgrounds

- **Squire.** "You served someone the songs are about." Sancho. A Dwarf Squire
  Paladin who *became* the one the songs are about is a Quixote who won.
- **Servant.** The Bank Templar's sideboard; "you knew where the silver was
  hidden." The Servant Dwarf knows exactly what the silver weighs.
- **Gambler.** "You have been rich. Twice in one night you have been nothing."
  A Dwarf who has been nothing has an accountant waiting at home.
- **Sellsword.** "A fair price and the good name that brings the next
  contract." The tercio for hire; the good name is the clan's.
- **Hermeticist.** The alchemist-jeweller: "gold to the sun, silver to the
  moon." A Dwarf Hermeticist treats correspondence as metallurgy.
- **Stranger.** A people who remember, among a people who forgot: the Dwarf
  Stranger's old ones keep the Missing Crown.
- **Inquisitor.** "You still believe. That is the part nobody outside ever
  understands." The Dwarf Inquisitor of a faith that is also a bank.
- **Bailiff.** The law that serves the vault. Forgery Kit against a ledger.
- **Archaeologist.** The record of the Gilded Era; "an accurate account… buys
  you the rest of your life": a Dwarf Archaeologist is paid twice, once by the
  college and once by the clan.
- **Tomb Raider.** The Great Mountain's tombs. A Dwarf who robs their own
  ancestors and is hailed for the gold.
- **Guardian, Soldier.** The tercio's rank and file.
- **Artisan, Merchant (official).** The officials most natural to a Dwarf: the
  maker who measures the world by whether it was built to last, and the trader
  of the long routes. Their Hooks are *The Guild* and *I Know Where to Get It*
  (Backgrounds-Official §3).

---

## 📖 8. Decisions and ratification queue

### Unratified, and what each one needs

*Stated as design, not as law. Each line names the Questa that would ratify it.
This is the work list, and it is long.*

- **A soul is a metal, given, and it must be proven**, set against the
  Celestial's fixed Ideal, the Elf's collective consent and the Dragon's
  self-authorship. The organising idea rests on the peoples table in
  `Dragons-and-the-Overcoming.md` and on the species docstring. QST-0094 uses the
  word "soul-metals" for what the entry contains and QST-0050 speaks of "the
  dwarven soul-metal", but neither states the given-and-proven doctrine or the
  four-way contrast; QST-0053 points at that table as the register of organising
  principles per people without ratifying a single row. Needs a Questa ratifying
  that table row by row, with the Dwarf's formula as its own decided line.
- **Sainthood as transcendence into one's own pure substance**, and the
  goldsaints and silversaints of the old halls as Dwarves who proved the metal
  all the way down. QST-0050 puts Saints with the Dwarves and says nothing about
  what Sainthood is or that saints carry metal ranks. Needs a Questa downstream
  of QST-0050.
- **The history: the Great Mountain, the Guilded Era, the scattering.** Present
  in the shipping entry (which spells it "Guilded Era", not "Gilded") and in the
  old wiki's paragraph, and nowhere else: "Great Mountain", "Guilded Era",
  "Gilded Era" and "grudge" all return nothing across the formal system. Needs a
  history Questa, so the shape is canon rather than an unedited draft.
- **The two surviving factions**: the Bank Templars with their vaults, and the
  isolationist, Basque-inspired Mountain Dwarves. Old wiki only. The shipping
  entry supplies the bank-cathedrals, the fleets and the long terrible
  expeditions but names no faction, so the two names have one unratified source
  between them. The same Questa must decide whether `basque` becomes its own
  atomic key beside `iberia` (no such key exists in the map today), since
  QST-0046.5 forbids blends.
- **The Missing Crown and the Holy Gold** as the surviving religious politics.
  Old wiki only, where the second is spelled "Holly Gold". Needs a Questa
  deciding the split as canon, its spelling, and whether it is player-visible or
  design-team lore.
- **The entry's own doctrine**: that the clan absolves whoever comes home with
  enough gold, so every Dwarf adventurer has a guaranteed homecoming and an
  accountant at the end of the story; and that gold never corrupts, with the Life
  prayers arguing the other side from inside the species. QST-0094 ratifies the
  entry's voice and tense, never its content. Needs the content half: a Questa
  that reads the species entry line by line.
- **The prayers.** "Metal shapes in the forge. People in the challenge.", "A
  saint is a sinner trying to be better." and "Forgetting is hard, but harder is
  forgiving." in the species pool; "The real gold is in your soul." and "Gold
  held is not living. Gold earned is gold spent." on Life; "There is no shortcut
  without work." on War (the file carries *no hay atajo sin trabajo* beside it as
  a source comment, and the Spanish is not what prints); "Traveller, there is no
  road; you make the road by walking." on the `iberia` key; "This world is a
  bridge. We all must cross." on the `andalus` key. Every one returns nothing in
  the formal system; the prayer map is only ever named as a file there. Needs a
  Questa ratifying the species-keyed and culture-keyed prayer pools as authored
  canon, naming the Dwarf, `iberia` and `andalus` rows.
- **Darkvision at 120 feet, and poison resistance as identity.** No Questa
  attributes the range to the Dwarf or ranks it against the other species, and
  the ranking the page has been making is wrong: 120 feet is the longest range on
  the roster but not the Dwarf's alone, since the Orc has 120 and so do the Drow,
  Dark Elf and Shadow Elf lineages. Whatever is written must say "as deep as
  anyone's", never "the deepest". Needs a Questa tabling Darkvision ranges and
  damage resistances per species, which QST-0094's open convention question would
  naturally carry.
- **That Darkvision prints as an entry rather than as a bare chip.** The
  earlier reading was wrong here: QST-0094 records
  the Aasimar as chip-only by design and lists the convention as still open (Elf,
  Orc, Gnome, Dwarf and Tiefling print the rule; Aasimar and Dragonborn print the
  chip), and QST-0051 is where "Darkvision is a record, not a paragraph" is
  written. The Dwarf resolver prints both the rule and a range chip today, so the
  Dwarf already sits on the printing side of a question nobody has answered.
  QST-0094 settles it when the convention question is answered.
- **That the four entries read in the rules' second person at all.** QST-0062 is
  open and names the Dwarf as one of five kits written in a clipped, agentless
  register, citing Stonecunning and Dwarven Toughness as its two examples of the
  register to be replaced, with the Aasimar and the Dragonborn as the target.
  QST-0094's rewrite landed that voice on the Dwarf, but QST-0062 was never
  closed against it and still describes the old text. Needs QST-0062 re-read
  against the shipping entries and resolved or narrowed.
- **The obsession path to Ascension**: a Dwarf who spends ninety years on one gem
  may Ascend through the obsession itself, Draconic Sorcery as the family's
  curse, and a clan that cannot tell a Saint from a dragon from outside. Canon
  only (`Dragons-and-the-Overcoming.md`). The Agora touches the Ascending once,
  in the Druid Dialog 0017, and only to reserve it: nobody on the page explains
  it or claims it. Nothing there is about the Dwarf. Needs the Dwarf row of that
  table ratified.
- **The mountain is owed**: the Dwarf and the land in a debt relationship, the
  fall of the Great Mountain as the covenant's breach, and a Dwarf Druid as the
  mountain's creditor among a people of debtors. This page and the Druid page
  alone. Needs its own Questa, or the history Questa extended to cover the debt
  frame.
- **The Iberian and Andalus reference registers**, both sides of Roncevaux: the
  Cid, the Song of Roland at a Dwarf pass, Santiago and Calatrava, the tercio's
  *alférez* as the Banneret, Don Quixote as the Glory Paladin, Lazarillo and the
  picaresque, the cantigas de escarnio and the romancero, the *Libro de la
  montería*, Juanelo Turriano's *artificio*, the Cueva de Salamanca, Teresa of
  Ávila, Quevedo, Machado, the Basajaun and Mari of Anboto; and on the other key
  Abbas ibn Firnas, Andalusi falconry, and the *baratero*'s navaja. The standing
  Iberian-and-Eastern ruling above is the only formal footing, and it settles the
  well rather than the list: it says which traditions a martial or technique text
  may draw on, not that these particular figures are the Dwarf's. Needs a Questa
  ratifying the Dwarf's register and stating which class texts may draw on it.
- **The class table of §6 and the background readings of §7.** No background line
  quoted there appears anywhere in the formal system. Needs a Questa per
  cross-axis (species × class, species × background), or one Questa declaring such
  cross-readings wiki-only and never ratified.
- **The legend markers and their vocabularies**: `tolkien_dwarves` for rune-axes,
  delving and mithril mail, `folklore_dwarf` for knockers, nisse and the tapping
  hammer, the second shared with the Gnomes. Both markers, both vocabularies and
  the sharing are recorded, in the gear and materials maps and in the legend
  table of `Cultural-Inspirations.md`; neither the code nor the canon is the
  Questa system, and no Questa names `tolkien_dwarves` at all. Needs a Questa
  enumerating each species' legend markers and their nouns, the half of the
  double mapping QST-0046.5 describes but never lists.
- **The name module's inspirations**: the Golden Age of Spain, Renaissance Italy,
  Portuguese, and Carthage. Three of the four sit inside what the culture map
  already gives the Dwarf (Portuguese and the Golden Age under `iberia`, Carthage
  as a weighted neighbour of `iberia` in the reach map). Renaissance Italy is the
  odd one: the culture map gives Italy and the Renaissance to the Gnome, so the
  name draw claims a register the keys do not. Needs a Questa aligning the name
  inspirations with the keys, and deciding whether names may hold inspirations the
  culture map does not.
- **The Zealot's god for a Dwarf is a Saint, and the draw should be
  species-keyed.** This page's own proposal, correctly labelled. The Barbarian
  Dialog 0014 treats the Zealot as vesselhood, a god riding a body, and never
  mentions Saints. Needs a Questa routed through the Barbarian's texts.
- **The biology carve-out**: "the species law permits biology; these are the mines
  in the body." The taught-not-inherited law is used as a binding test inside the
  Agora, but the *carve-out* for plainly physical traits is stated only on the
  Mythos pages and in the folder's standing rules, which are not the Questa
  system. Needs a Questa or a Decree restating the law with the carve-out written
  in, so darkvision and size are not read as moral inheritance.

### Ratified decisions

**Decided**

- Iberia and al-Andalus are two keys, never fused (the law).
- Saints are Dwarven and stay out of the Celestials' table.
- The species entry speaks as "we" (`a1221a1`).
- Rule voice for the four traits (QST-0094).

**Unresolved after QST-0094**

- The four inspiration lines proposed there (§9) still need ratification.
- The cross-species Darkvision convention is open. The Dwarf currently prints
  both its rule and its range chip; the locked Aasimar deliberately prints only
  the chip. Neither implementation silently settles the other.

**Open (this page proposes)**

- The Zealot's god for a Dwarf is a Saint; the draw should be species-keyed.
- The old wiki's Dwarf paragraph is the lore's source and is repetitive; this
  page should replace it as the reference, and the wiki's public text should
  be cut to the entry plus one paragraph.
- Materials: Toledo steel by the `iberia` key is in place; the Dwarf Wizard's
  steel-leaf spellbook should draw it.

---

## 📖 9. Lines

*The author's four recovered lines, found together in
`.recovery-vault/AUTHORED-TEXT-ARCHIVE.md` and introduced to Git by `cd1a8b3`.
They replace the later review's generic proposals. They are still not wired and
await ratification through QST-0094; provenance establishes whose words they
are, not their rules status.*

| Entry | Recovered authored line |
|---|---|
| **Darkvision** | *Your eyes remember the mountain.* |
| **Dwarven Resilience** | *What you consider spicy could kill an elf. A dwarven diet made your body hard to poison.* |
| **Dwarven Toughness** | *Your Nana used to say: Dwarves eat beyond full, and work beyond exhaustion, so have another bowl.* |
| **Stonecunning** | *Your history is written in stone, so you read the stories stone tells.* |

These lines locate the traits in memory, food, family and history: the mountain
is remembered rather than merely mined, resilience is cultural and domestic
rather than industrial, Toughness arrives in Nana's voice, and stone holds
stories rather than accounts.

---

## 📚 10. Pointers

- **Paladin page**: Roncevaux, the Cid, Quixote.
- **Fighter page**: the alférez and the tercio.
- **Sorcerer page**: the ninety-year gem.
- **Druid page**: the Basajaun, Mari, the mountain's creditor.
- **Artificer page**: Juanelo and Abbas ibn Firnas.
- **Gnome page**: the Renaissance pair, one trade route.
- **Celestials page**: Saints and Celestials, two systems that look like one.


---

## 📔 11. Design assessment: the strong spine and the load-bearing risks

### What works

The Dwarf has the strongest single verb among the unfinished peoples: **prove**.
It turns the published rules into one argument rather than four decorations.
Darkvision is the mine remembered by the body; Resilience is exposure survived;
Toughness is proof accumulated; Stonecunning is an account the mountain can still
be asked to read. The same verb also makes room for a Fighter, Cleric, Rogue or
Artificer without declaring one of them the proper Dwarf. A Guild becomes an
anvil, not a stereotype.

The second strength is the contradiction inside the culture. The entry says gold
never corrupts and promises absolution to whoever brings enough home; the Life
prayers answer that hoarded gold is not living. Neither side needs to be made
secretly correct. That argument is more useful to a player than generic greed,
and it gives every Dwarf adventurer a homecoming with a price.

The Iberian and Andalusi keys are also productive rather than cosmetic. They meet
in Toledo steel, bank-cathedrals, expeditions, the *alférez*, the picaresque,
Córdoba's artificers and both sides of Roncevaux. The code's long, compound names
and forge surnames make the register audible before the lore is explained. This
is exactly what a consulting wiki should preserve: a repeatable set of choices,
not a paragraph of atmosphere.

### What needs restraint

**Soul-metal is not yet law.** It is the best organising idea on the page, but
the ratification audit in §8 shows that most of its consequences are readings,
not decisions. Until that queue closes, other pages may use it to test cohesion
but should not silently turn Saints, metals or the Great Mountain into fixed
setting facts. The chapter markers now reflect that distinction.

**Iberia must remain a register, not an essence.** The two culture keys can shape
objects, institutions, techniques, prayers and names. They must not imply that a
Dwarf inherits a nationality, temperament or moral character. The existing
weighted reach map is the correct mechanism: neighbouring vocabularies can enter
a character without fusing real cultures into a fantasy composite.

**Gold needs an economic consequence.** At present it is simultaneously sacrament,
proof, family debt and adventuring reward. That density is a virtue, but only if
future writing asks who owns the mines, who records a homecoming, whose labour
makes absolution possible and what happens to the Dwarf who returns empty-handed.
Without those answers, the Bank Temple risks becoming scenery and the clan's
welcome risks becoming a joke.

**The Great Mountain needs one decided failure.** Hubris, spiritual fervour and a
broken covenant are three compatible readings, but they are not interchangeable.
The history Questa should decide what the Dwarves believe happened, what the
setting establishes happened, and whether those answers differ. That single
difference can power the Missing Crown, the Holy Gold and the mountain's debt
without requiring an encyclopedia of the fallen empire.

### Recommended order of work

1. Ratify the one-sentence doctrine: a soul is a metal, given and proven.
2. Decide the Great Mountain's public history and the disputed religious reading.
3. Define Sainthood just far enough to distinguish a Saint from a Celestial and
   from a Dwarf who Ascends through obsession.
4. Resolve the four trait lines and the cross-species Darkvision presentation
   convention together, so the Dwarf follows the locked Aasimar's method without
   copying its answer blindly.
5. Audit the generated names by source pool. Keep the four-part ledger shape;
   decide whether Renaissance Italian names are intentional cultural reach or a
   leak from the Gnome register.
6. Only then write Bank Templars, Mountain Dwarves, the Missing Crown and the
   Holy Gold as player-facing material. Institutions should realize the doctrine,
   not substitute for deciding it.
