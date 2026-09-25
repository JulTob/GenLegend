# Dialog 0017: the Druid core fantasy

- **Topic:** The Druid's core fantasy, verified against the 2024 rules, and the provisional class and Circle descriptions for the beta character generator.
- **Commissioned by:** Julio (in chat, 2026-08-31), as part of the all-classes description commission: find the core fantasy through archetypal analysis, verify the rules establish it, write the prose in a register that fits the class.
- **Date:** 2026-08-31
- **Consuls called:** Lorekeeper (Elf Sage), Venustas (Bard), Contracts (Warlock), Simplicity (Monk). Vox reports.
- **Status:** 🟡 revised provisional. The 2024 rules read is retained, but the
  core fantasy is revised from elder belonging to study that changes the
  observer, pending Julio's word.

---

## 🧭 Framing

### Revision after the 2024 rules read

The first pass treated the Druid as someone admitted to an older society. The
stronger reading is that the Druid is an investigator who becomes part of the
world by studying it. Learning can mean receiving and retaining an answer;
studying is active contact with what is not yet understood. The Druid is a
porous vessel: not empty of personality, but willing to let observation,
experiment, experience, and empathy change the observer. Wild Shape is study
embodied, not a hidden animal self revealed.

This also explains why a Druid can be a healer, a Charlatan making profitable
potions, a Guard studying forensics, or an explorer with an unanswered thesis.
The class is not morally defined by conservation. Guardianship is a result of
understanding a system from within, and the Circle is the field of inquiry
that gives that investigation a peer language and method.

The 2024 rules support this reading directly: Spellcasting comes from
studying mystical forces; Magician adds Wisdom to Intelligence (Arcana or
Nature) checks; Druidic is learned and carries hidden messages; Wild Shape
requires forms the Druid has learned and can revise after a Long Rest; Wild
Companion summons a temporary Fey animal; Wild Resurgence exchanges spell
slots and Wild Shape; and Beast Spells preserves the Druid's personality,
memories, and speech while transformed. “Druidic is mathematics” is therefore
a GenLegend interpretation of its symbolic precision, not a claim about the
printed rules.

This commission arrived with no seed from Julio and no found text to inherit.
Both facts were verified before the council spoke:

- `AtlasLusoris/AtlasOfGuilds/DruidKit.py` is a 33-line stub: four bare
  `Build_Specialization` calls (Land, Moon, Sea, Stars), no `extends`, no
  `heading`. The texts proposed here get wired later, following the sibling
  kits' practice (`heading="Circle of the Land"` and so on, rendering the
  Circle paragraphs *under* the class's own).
- The recovery vault holds no Druid prose. Extracting the top-level names from
  `.recovery-vault/GuildKit.cpython-314.pyc` finds exactly four description
  constants: `BARBARIAN_DESCRIPTION`, `FIGHTER_DESCRIPTION`,
  `WARLOCK_DESCRIPTION`, `WIZARD_DESCRIPTION`. This Dialog is a fresh
  derivation, not a reconciliation.
- The rules are real source: `AtlasLusoris/AtlasOfTraining/Map_of_Druid_Training.py`
  (2024 PHB core plus all four Circles, 649 lines). The chassis
  (`GuildKit`): WIS primary, CON secondary, d8 Hit Die, INT and WIS saves,
  medium armor, the Adept vocation it shares with Cleric and Ranger.

One house fact the deliberation leans on: in this project the neighbouring
texts already claim territory. The Barbarian's Wild Heart says "you carry the
wild things in your heart" (the *inner* wild), and the Dragons canon
(`Documenta/Canon/Dragons-and-the-Overcoming.md`) owns self-authorship, the
becoming-what-you-are slot. Whatever the Druid is, it cannot be either of
those, or the roster blurs.

---

## 🗣️ Deliberation

**Lorekeeper (Elf Sage):** Three candidate fantasies, each with its
literature. All three are genuinely druidic; the question is which one is the
trunk and which are branches.

*Candidate A, the elder belonging.* The wild as the older order, and the
druid as someone still on speaking terms with it. The purest page is the
"Piper at the Gates of Dawn" chapter of The Wind in the Willows: Rat and Mole
row into the presence of something older than fear, are known by it, and are
gently made to forget, because mortals cannot carry that memory around. Sir
Gawain and the Green Knight runs on the same current: the Green Man rides
into the young court out of the old world, and the whole poem is the new
order being tested by the elder one. Tolkien's Bombadil ("Eldest, that's
what I am") is the figure the argument cannot touch because he predates the
argument. And Blackwood's "The Willows" is the same elder world with the
warmth removed: vast, indifferent, barely noticing us. In all four, the wild
is not scenery. It is society: an older one, still holding a chair for you.

*Candidate B, the honest shape.* Shapeshifting as truth-telling: the wild as
the true self, and the animal form as the self undisguised. The native well
is the Hanes Taliesin chase: Gwion becomes hare, salmon, wren, grain, and
Ceridwen answers greyhound, otter, hawk, hen, form matching form like
question and answer. Ovid's Metamorphoses makes change the engine of the
whole world. T.H. White's The Sword in the Stone has Merlyn school Wart as
perch, ant, goose and badger, each shape one lesson in being alive. Le Guin's
A Wizard of Earthsea files the caution: Ged stays a hawk too long and nearly
loses the man.

*Candidate C, the forgotten treaty.* The druid as keeper of a covenant
humans no longer remember signing. Princess Mononoke is the master text
(Ashitaka walking between iron town and forest, seeing with eyes unclouded),
Nausicaä its sibling (the poisoned wild is secretly doing the world a
kindness, and needs one interpreter). The Lorax speaks for the trees;
Treebeard is on nobody's side because nobody is altogether on his; Leopold's
A Sand County Almanac argues the community boundary outward until soil and
water and beast are members. And the oldest version is written law: the
sabbath of the land, the corner of the field left unharvested. People really
did once sign.

**Venustas (Bard):** Before we weigh them, two collisions to put on the
table, because they cut Candidate B off at the knees at class level.

First, the Wild Heart. Its found text already says "There is a wild instinct
that maybe everyone carries and few listen to. You listen." and ends
carrying the wild things in its heart. That Path owns the inner wild. A
Druid class text on the thesis "the wild is your true self" would make the
two guilds read as one fantasy at two volumes.

Second, the canon. "Become what you are" is the Dragons' doctrine, the
Ascending, and the house rule there is that nobody on the page gets to
explain it or claim it. A class description built on shapeshifting as
self-authorship walks straight into that reserved ground. If B survives
anywhere, it has to be reframed away from *self* and toward something else.

**Contracts (Warlock):** Then let the rules speak, because they settle it
more cleanly than I expected. I read every core lesson and all four Circles
in `Map_of_Druid_Training.py`.

The single most decisive wording sits inside Wild Shape itself: you
shape-shift into "a Beast form **you have learned**." Learned. Not
unleashed, not revealed, not remembered from some inner deep. The rules
treat every form as outward-facing knowledge, an acquaintance made, which is
the opposite of Candidate B's inner honesty. And the second most decisive
fact is an absence: nothing in the core class mechanics imposes a duty. No
feature rewards protecting anything, no rule punishes a felled tree.
Candidate C's treaty is folklore about the class until level 3, where
exactly one Circle makes it mechanical.

The rules read, each key feature and the one line of what it proves:

| Feature (level) | What it proves about the fantasy |
|---|---|
| Spellcasting (1) | "Drawing on the power of the natural world": the power is drawn, not owned. And the ability is Wisdom, so the craft is perception. Attention, rewarded. |
| Druidic (1) | A secret language, taught, with hidden messages others automatically fail to find. Membership in something older than any kingdom, with letters left for people not yet born. |
| Primal Order (1) | Magician or Warden: two ways of serving the same old order, and the generator settles which. The class prose may lean on neither weapons nor extra spellcraft. |
| Wild Shape (2) | "a Beast form you have learned": forms are acquaintances, not confessions. Duration in hours, not minutes: a way of moving through the world, not a combat trick. |
| Wild Companion (2) | The familiar arrives Fey: the older world sends you company from its own house. |
| Wild Resurgence (5) | Spell slots and Wild Shape convert into each other, both directions. Speaking with the wild and wearing the wild are one currency. |
| Elemental Fury (7) | The same elemental might backs the cantrip and the claw. Whichever hand you use, the same world is behind it. |
| Beast Spells (18) | You keep your speech inside the borrowed body. The two halves of the craft stop being halves. |
| Archdruid (20) | Unlimited shapes, and the body ages one year in every ten. The wild starts keeping you on its own calendar. |

What this table describes is Candidate A, sharpened: not vague belonging but
**membership maintained through attention**. Wisdom is the engine, Druidic
is the passport, the shapes are the vocabulary, and Archdruid is the elder
world adopting your clock at the end. The treaty never appears; the true
self never appears; the long acquaintance appears at levels 1, 2, 5, 18 and
20.

**Lorekeeper (Elf Sage):** Conceded at class level, on both B and C, with
the migrations flagged so nothing is lost. B does not die, it *reframes* and
moves to the Moon, where the subclass is literally named for the one body
that changes every night and is never anything but itself. Shapeshifting as
honesty survives there in the only form the rules permit: not "the beast is
the real you" but "you change the way the moon changes, and every phase is
true." Le Guin's caution is answered by the same figure: the moon has never
once failed to come back. And C moves to the Land, the one Circle whose
level-14 feature is the treaty made visible: Nature's Sanctuary, where beast
and plant must save against their own wish to strike you. The class refuses
the duty; a Circle may keep the covenant. That contrast is roster texture,
exactly as the Barbarian keeps possession out of the class and gives it to
the Zealot.

**Venustas (Bard):** The register is documentary natural history, not generic
nature writing. The narrator observes before interpreting: habitat, tracks,
weather, migration, pressure, light. Land may carry the patient ecological
clarity of Attenborough's documentaries; Moon may carry the intimate field
attention associated with Félix Rodríguez de la Fuente's wolf films; Stars
may widen into Sagan-like cosmological wonder. These are tonal coordinates,
not imitation or quotation. The prose should remain GenLegend's own: direct
second person, concrete evidence first, wonder earned by the observation.

Against the siblings, so the shelf reads as a set: the Barbarian chants, the
Fighter talks between drills, the Warlock confesses, the Wizard writes
aphorisms. The Druid *notices*. And one deliberate register shift at the
close: the last three sentences of the class text go geological ("Mountains
count in winters. Forests count in centuries. So, in time, will you."),
which is Archdruid's slowed ageing performed as rhythm, the sentences
lengthening their own units of time. The Fighter's "When Death comes for
you, it will not collect" is the precedent for letting the closing line
reach for the level-20 truth.

**Simplicity (Monk):** My lens is the knife, and for a fresh derivation the
knife guards against three temptations rather than against edits.

*The eco-sermon.* The moment the class text scolds anybody, it moral-locks a
class the way we refuse to moral-lock backgrounds. The wild being older than
walls is a fact of the setting; walls being wrong would be a doctrine. The
drafts must stay non-adversarial: the druid is not against the city, the
druid simply never dropped the older acquaintance. I will read every line
for a wagging finger.

*The lore-dump.* No order named, no first tree, no history of druidry.
Letters in leaf and stone, an old understanding, people you will never
meet: things a player can inhabit, with the meaning left to them.

*The open choice.* The generator has already settled the Primal Order
(Magician or Warden, drawn in `apply` from a named Dice Bag, per the map),
so the class prose may assume neither armor nor extra cantrip. Likewise the
Land's terrain, re-chosen each Long Rest in 2024, is a genuine at-table
decision and so *may* stay open in its feature entry; the description prose
still should not enumerate options.

Calibration: class at three short paragraphs, each Circle at two. That
matches the Fighter and Fiend density.

**Contracts (Warlock):** The Circle verification, and three findings the
texts must answer rather than write around.

*Land.* Circle Spells keyed to terrain, re-chosen per Long Rest (each
country teaches you its own way of answering); Land's Aid heals allies and
poisons a foe in one gesture (the ground feeds its own and turns on the
rest); Natural Recovery returns spell slots on a Short Rest (rest on the
land and it restores you); Nature's Ward grants Immunity to Poisoned,
Frightened and disease, and natural plants stop impeding you (the place no
longer treats you as a stranger); Nature's Sanctuary at 14 makes Beasts and
Plants save or turn aside (the covenant, visible). The treaty fantasy is
fully funded here and only here.

*Moon.* Circle Forms scale the Beast CR and open the Elementals at 10 (not
even flesh is the limit of the vocabulary); Moon Spells are the night side:
Faerie Fire, Moonbeam, Vampiric Touch, Greater Invisibility. **Finding one:
Vampiric Touch is Necrotic and predatory. The Moon list is genuinely
nocturnal, teeth included, so the text must not paint pure silver.** And a
detail I want on record because it is beautiful: in the 2024 rules Moonbeam
is the spell shapechangers dread (Disadvantage on the save, forced back to
true form). The Moon druid's own light polices false shapes while its Wild
Shape grants true ones. Honesty of shape is not our metaphor imposed on the
kit; it is the kit. Moonlight Step moves you the way light moves; Lunar Form
resists everything but Psychic and Radiant while regenerating: phases do not
destroy the moon.

*Sea.* Wrath of the Sea is an aura: you do not aim the sea, you stand in it
and it happens around you. Aquatic Affinity opens the border (Swim Speed,
water-breathing). Stormborn makes Cold, Lightning and Thunder weather rather
than harm, and pushes with every storm-flavoured spell. **Finding two:
Oceanic Gift computes one number and pays it out both ways, damage to
enemies and the same Hit Points to friends. "It feeds a coast and drowns it
with the same water" is not a metaphor we chose; it is the arithmetic of the
level-14 feature.** No treaty anywhere in this Circle: the sea signs
nothing. The roster texture writes itself: Land signs, Sea never did.

*Stars.* Star Map is attention written down until the record itself becomes
a Focus, with Guidance and Guiding Bolt always ready (the sky repays being
read, in guidance). Cosmic Omen is Hesiod as a Reaction: read the sky at
rest, then tell luck which way to lean, Weal or Woe. **Finding three, and
the structural one: Starry Form spends a use of Wild Shape.** The night sky
is reached through the class's own signature currency. The rules are saying
the stars are one more wilderness, and the constellation figures (Archer,
Chalice, Dragon) are its beasts, lent the same way. Twinkling Constellations
brightens them; Full of Stars turns the watcher partly into the watched,
incorporeal. The arc is attention, then reading, then becoming.

**Venustas (Bard):** Accepting all three findings into the drafts: the
Moon's closing line answers the teeth, the Sea's closing image is the
two-handed wave, and the Stars text ends on becoming what you watched. One
more literary note for the Sea, since the well should be the house's
preferred ones where it can: Hemingway's The Old Man and the Sea gives us
la mar, the sea loved in the feminine and never once trusted, which is the
exact register of a Sea druid's devotion, and Hokusai's Great Wave holds the
whole subclass in one image: beauty, scale and threat in a single curl of
water, the boats small, the mountain smaller. For the Stars, Hesiod's Works
and Days (sow when the Pleiades rise, sail when they set) and the Polynesian
wayfinders, who read stars and swell together and crossed an ocean by
attention alone: the oldest literacy, older than letters.

**Simplicity (Monk):** The drafts below pass my three guards: no sermon, no
proper noun, no open choice. Two flags for Julio rather than for us. The
class close ("So, in time, will you") spends its last breath on the
level-20 truth, like the Fighter's Death line; I judge the precedent
sufficient. And the Land text uses covenant language ("what may be taken and
what must be left") while staying hospitality rather than job; if it reads
as duty to Julio, the fix is one sentence, not a rewrite. No unanswered
objection from me.

**Contracts (Warlock):** No unanswered objection. The rules read stands.

**Lorekeeper (Elf Sage):** No unanswered objection. The migrations are
recorded.

**Venustas (Bard):** No unanswered objection.

---

## 🌿 Circle analyses

Each Circle is a different grammar of the same conversation the class text
opens: the place that answers, the change that stays, the wild that owes
nothing, the wild that outlasts everything.

### Land

**Fantasy in one line:** The old covenant kept: you remember what each place
is owed, and the place remembers you back.

Candidate C, housed where the rules fund it. The evidence is Leopold's land
ethic (the community enlarged until the soil is a member), Treebeard's
weariness, the Lorax's advocacy softened from placard to practice, and the
old written forms of the pact: the field's corner left standing, the
seventh-year rest. The text frames the covenant as hospitality, guest
becoming kin, never as employment. Rules echo: Circle Spells re-learned per
terrain (each country teaches its own way of answering); Land's Aid feeding
allies and poisoning a foe in one gesture; Natural Recovery (rest on the
land and it restores your reach); Nature's Ward (poison forgets your name,
fear finds no hold, green things part); Nature's Sanctuary (beast and briar
turn aside: the treaty made visible at 14).

### Moon

**Fantasy in one line:** Change that stays itself: you change as the moon
changes, and every phase of you is true.

Candidate B, reframed and housed. The Taliesin chase and Ovid stand behind
it; the werewolf myth is inverted (the moon forces a shape on the cursed,
and offers shapes to you); Le Guin's caution about losing the man in the
hawk is answered by the figure itself, because the moon always comes back.
The deliberation's Moonbeam finding anchors the honesty reading in the kit:
this Circle's own light forces false shapes to confess, while its forms are
all true. Rules echo: Circle Forms scaling to Elementals (not even flesh
limits the vocabulary); the nocturnal spell list, teeth included (Vampiric
Touch is in the text's "answer for both"); Improved Circle Forms putting
Radiant moonlight in the claw; Moonlight Step (you move the way light
moves); Lunar Form regenerating under Resistance (phases do not destroy the
moon).

### Sea

**Fantasy in one line:** You keep company with the one wild that never
signed anything, and you carry its weather home.

The contrast Circle: where the Land keeps covenant, the sea owes nothing,
and the Sea druid loves it precisely for never pretending otherwise. The
Odyssey's unappeasable water, Hemingway's la mar (loved in the feminine,
never trusted), Hokusai's one curled wave over the small boats. The fantasy
is devotion without terms: not mastery of the sea but membership in its
weather. Rules echo: Wrath of the Sea as an aura (you stand in the sea and
it happens around you); Aquatic Affinity opening the border (breath, speed);
Stormborn making Cold, Lightning and Thunder into family weather, every
storm-spell shoving like surf; Oceanic Gift computing one number and paying
it as harm to enemies and healing to friends: the same water feeding and
drowning, with no hatred in it anywhere.

### Stars

**Fantasy in one line:** The night sky is the oldest wilderness, and you
learned to read it.

The Circle for the druid whose wild is up. Hesiod's almanac sky (sow at this
rising, sail at that setting), the shepherds and wayfinders who read stars
before anyone read letters, the universal habit of drawing figures on the
dark. The structural finding carries the analysis: Starry Form spends Wild
Shape, so the constellations are this class's beasts, lent from a higher
pasture by the same old friendship. Rules echo: Star Map (watching until the
watching becomes a map, a record that casts); Cosmic Omen (read the sky at
rest, then tip luck Weal or Woe a breath before it lands); Starry Form's
Archer, Chalice and Dragon drawn on you in light; Twinkling Constellations
brightening them; Full of Stars (partly incorporeal: watch anything long
enough, with enough love, and you take on its nature).

---

## ✅ Convergence check

- [x] Every called Consul has spoken.
- [x] Every objection has been answered or conceded.
- [x] The rules read covers every core lesson and all four Circles.
- [x] Proposed texts are on the table; findings flagged for Julio, not
      written around.

---

## 📜 Current working descriptions

These are the current player-facing descriptions, developed from the
study-centered draft. They are wired in
`Grimoire_of_Guilds.py` and `AtlasOfGuilds/DruidKit.py`.

Plain prose, paragraphs separated by blank lines, ready to lift into the kit
as string constants when the wiring lands (headings per sibling practice:
"Circle of the Land", "Circle of the Moon", "Circle of the Sea", "Circle of
Stars").

**DRUID_DESCRIPTION**:

```
To be a Druid is to see yourself as part of a greater thing. A Druid studies a cosmos made of order and chaos, experiences it, embodies it, and searches for what is not yet understood. You follow the air directing the storm. You put your hands in the soil and smell its nutrients. You feed the cub until it becomes a wolf. Life is not learned from a book. It is lived, entered, and learned through being there.

You are not a watchful observer. You are an enthusiastic participant. Experiment and experience become one. Observer and observed become the same thing. The search changes you. You have glimpsed the connection among living things, and you have let the world fill you. You were the wolf feeding the cub, the eagle riding the storm, the warg smelling the ground, because you understood exactly what they are, and that made you aware of what you are. The world is not a catalogue. It is an experiment in progress, and you are part of the apparatus.
```

**LAND_DESCRIPTION**:

```
You learn about this land, and the lands beyond the horizon. You learn where water runs after rain, which grasses return first, why foxes hunt rabbits, and how a field dies when one small insect disappears.

The Circle of the Land studies habitat as a living system. Every answer creates another question. Every connection opens another investigation. Your Circle studies and shares this knowledge to preserve the natural order. You do not guard nature because it is innocent. You guard the experiment because you understand how much disappears when it is broken.
```

**MOON_DESCRIPTION**:

```
Your study begins with tracks. Not just the shape of the paw, but the distance between them, the weight in the mud, the moment the animal stopped and looked back. The Circle of the Moon studies the animal from inside. You learn hunger, caution, territory, and the need to run. There is no honest way to observe a living thing without being changed by it.

Your Circle studies change, difference, and the connections among all living things. You learn that every form belongs to one tree of life. The observation then takes you: fur, muscle, talon, scale. You try not to ask why it is so easy for you to understand the beast, or whether, after changing, you will still want to return.
```

**SEA_DESCRIPTION**:

```
Life began in the sea. Life remains in motion. What becomes static drowns. You study currents, flux, cycles, migration, and the first invisible difference that becomes a storm. The sea is ever changing. It is the oldest experiment. You learned to flow with it.

The Circle of the Sea studies change at its largest scale. You learn that calm is not kindness and violence is not anger. Water follows forces. You let those forces shape you, until adapting becomes instinct. You breathe where others cannot, move as the current moves, and bring the sea ashore. You become one with the sea, and you guide it.
```

**STARS_DESCRIPTION**:

```
At dusk, the first stars appear before the eye that looks up. One becomes two, two become a pattern, and the universe slowly opens for you. And you open yourself to the universe. You are one of the wanderers: a living thing that looks up from a small world and discovers that it, too, is moving through the dark. The light you watch began before your ancestors had names.

Some stars are more than fires. They are principles made visible, ordered by influence and omen. You study the heavens to learn the patterns by which to guide your own life. You become infinite by discovering how much world can fit inside one observing life. You are the cosmos looking at itself.
```

---

## 🕊️ Vox report

**The working choice.** The Druid's core fantasy is **study that changes the
participant**: an investigator enters an experiment, understands the world
through attention and empathy, and eventually embodies what they have studied.
Learning receives an answer; study tests what is not yet known. The
2024 rules establish it through studying mystical forces, Wisdom-powered
comprehension, Magician's investigation bonus, Druidic's learned symbols,
Wild Shape's learned and revisable forms, Wild Resurgence's exchange between
spell knowledge and embodiment, and Beast Spells' retention of personality and
memory. The register is **documentary natural history with mythic scale**:
exploratory, concrete, patient, and capable of wonder without becoming a
sermon. Circles are fields of inquiry and peer practices. Land investigates
habitat and succession, Moon animal behaviour and transformation, Sea force
and flux, and Stars pattern, wanderers, and celestial Ideals.

**The strongest rival.** Candidate C, the forgotten treaty (Mononoke,
Nausicaä, the Lorax, Leopold): rejected at class level because no core
mechanic imposes or rewards guardianship, so a duty-built class text would
promise what the sheet never delivers; preserved at Circle level, where the
Land's features pay the fantasy in full. Candidate B (the wild as the true
self) was cut harder: Wild Shape's own wording makes forms learned rather
than revealed, the Barbarian's Wild Heart already owns the inner wild, and
self-authorship is the Dragons' reserved ground. It survives at the Moon as
transformation through understanding, not as a hidden animal identity.

**Open questions for Julio.**

1. **The documentary register.** Land, Moon, Sea, and Stars now have distinct
   observational voices. The references to Attenborough, Félix Rodríguez de
   la Fuente, and Sagan are tonal coordinates only; the prose should remain
   original and second-person.
2. **The Moon's teeth.** The council keeps the night's predatory side
   ("there are teeth in it, and you answer for both") because Vampiric Touch
   sits on the Moon list. If the Moon should read purely silver, that
   sentence is the one to change, and the rules finding should be recorded
   as overruled rather than unnoticed.
3. **The Land's covenant tone.** Hospitality was chosen over duty
   ("welcomed in", not "sworn to"). If it still reads as a job to Julio,
   the fix is the first paragraph's middle sentence, not the fantasy.
4. **Wiring.** DruidKit.py currently passes no `extends`/`heading`; when the
   texts land, headings should follow sibling practice ("Circle of the
   Land", and so on) so Circle prose renders under the class's own.

→ Awaiting Julio's word. The five texts ship as provisional until then.
