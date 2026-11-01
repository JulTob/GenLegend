# QST-0151 — A Tiefling's aspect mixes two legacies

- **Type:** feature · lore (📗) · generator
- **Priority:** 🟡 medium *(Julio, 2026-10-30: "a tiefling creator equivalent to the aasimar: each legacy mixing two options aleatory and combine them to produce a unique character combining horns, colors, eyes, and in this case spells from both legacies")*
- **Status:** Working — the aspect lands here; the rules (spells, Resistance) are QST-0152
- **Owner:** unclaimed
- **Route to:** Lore (Bard) · Simplicity (Monk)
- **Related:** `Documenta/Canon/Mythos/Tiefling.md` §0 "The variable detail" · `AtlasActorLudi/SpeciesKit/Aasimar/Map_of_Ideals.py` (the model) · QST-0152 (the rules)

---

## 🔍 Diagnosis

The Tiefling canon (§0, "The variable detail") said it plainly: the body was
not drawn. Each legacy printed one fixed paragraph, so every Abyssal sheet ever
generated had the same fur, horns and eyes, and *"whether the Tiefling should
gain the same apparatus [as the Aasimar] is a real design question and nobody
has asked it yet."* Julio has now asked it.

## ✅ Julio's rulings

**2026-10-30.** A second legacy is drawn at random; the look combines both.

**2026-10-31** (review of the first draft, PR #122):

1. **"Aspect", never "face".** The look is a presentation, not only the face.
2. **The two hells are structure, and hidden,** as the Aasimar's two Ideals
   are. The page may suggest where the bloodline starts ("your looks suggest
   your bloodline starts in Hades"), but never describes a hell. Leave it open.
3. **Specific materials.** No "dark metal": say ivory, jet, agate.
4. **Subtle mystical smells**: incense, sulfur, a doused campfire.
5. **The metallic sheen, subtly, by metal**: copper, silver, brass.
6. **Built dynamically** from base structures that take shape as a wave
   function collapses; lists of Tags may be Pins.
7. **Every legacy has its own horn shapes.** Crowns are Chthonic's, the least
   demonised of the three.
8. **The old paragraphs are reworked into the new parts, not kept.** We move
   on.
9. (Rules, in QST-0152.) One Resistance, drawn; spells lent as the dice fall.
10. **More than one way to say each thing, chosen at random**, after
    Chomsky's generative principles: "they have the look of" is lame; "they
    resemble the finest" is one of several. Little variations accumulate into
    a new text.

**2026-11-01** (reading generated examples):

11. **A presentation, not an inventory.** "Most are too factual": collapse the
    options into an evocative presentation; do not say every detail, keep a
    strong presentation by focusing on a few.
12. **Images, not facts.** "The smell of rain lingers in you, like a
    persistent memory", not "a trace of cold stone after rain about you".
    "You smell of freshly opened wine, even in clean, fine clothes", not "a
    smell nobody can say where it comes from". Wine is a demonic smell (the
    Abyss).
13. **No ";" breaking the flow**: "Ram's horns of polished jet curl back over
    your ears", not "...like a ram's; they look like polished jet".
14. **The Abyssal eyes say what happens**: "Your eyes look an ordinary brown,
    until you stare too long at someone and they take on that person's
    colour."

## 🧭 What this questa does

A Tiefling keeps its one Heritage Tag (Abyssal, Chthonic or Infernal), and that
Tag keeps every rule it carries. The new part is the **blood**:

1. **Two legacies.** The first is the Heritage. The second is drawn from the
   whole list at uniform random and may be the same one again, which makes a
   *pure* blood, neither rarer nor commoner than any particular pair (the
   Aasimar's rule for its two Ideals). About two Tieflings in three are mixed.
2. **The aspect is collapsed, not assembled.** Ten slots: a structure (which
   few things are said, and in what order: six presentations, each saying
   three or four of horns, eyes, fur with its sheen, scent and tail, then the
   suggested place) and nine parts of the look (horn shape, horn material,
   eyes, coat, pattern, a second coat colour, sheen, scent, tail). Each part
   starts with every mark the blood's legacies lend, and `ABSENT`. The
   collapse fills the most constrained slot first, with the Character's own
   dice, and four rules narrow the rest after every draw:
   - **Say only what is presented.** The parts the structure does not say
     stay empty; the parts it says are filled; and a structure that would say
     a tail the blood does not have is ruled out.
   - **No word twice.** Marks sharing a key never meet: no gold iris under a
     gold sheen, no red fur marked with red.
   - **Pattern and second colour agree.** A two-colour pattern needs one; a
     one-colour pattern forbids one, and the other way round.
   - **A mixed blood shows both legacies**, in what is said. When only one
     slot could still show the legacy nothing has shown yet, that slot must
     show it.
   A slot left empty is a contradiction, and the wave starts again from the
   same dice stream (deterministic).
3. **The origin is suggested, never described.** The last (or first) line
   names the place of the legacy that lent the most of the look (the
   Heritage, on a tie): *the Abyss*, *Hades*, *the Nine Hells*. That the blood
   is two legacies is never said.
4. **The words are derived by a generative grammar.** Each sentence of the
   chosen structure is a symbol (`{HORNS}`, `{FUR}`, `{PLACE}`), rewritten by
   rules with several productions each, some nesting further symbols. The
   marks are the lexicon, and the marks said on their own (a horn shape, the
   eyes, a scent, a tail) bring whole sentences of their own, two each, with
   further words set inside them ("Ram's horns of {horn_material} curl back
   over your ears"). The derivation is drawn once, with the Character's dice,
   and the sentences are kept.
5. **The paragraph** prints where the Heritage paragraph printed until now,
   under the Heritage's name (the web sheet files the Heritage description by
   that name).

## 🏗️ How it is built (and why)

- **Marks are Tags; Pins catalogue them** (ruling 6; TOP Guide: say things
  about Tags with a Pin, never a side table). `Tieflings/pins.py` declares the
  `Aspect_Mark` Tag, the `Aspect_Part` Pin with one Shape per slot (its
  docstring is the grammar that slot's text must follow) and a `KEYS` Record,
  and the `Lent_By` Pin with one Shape per legacy. `crown in Horn_Shape` and
  `crown in Chthonic_Marks` are the only questions the collapse asks.
- **The roster is one table** (`Tieflings/Map_of_Marks.py`), one row per mark,
  made by `Make_Mark` / `Make_Structure` (QST-0093.11: factory-made Tags stay
  as rows of their table).
- **The collapse is generic** (`SpeciesKit/collapse.py`): slots, candidates,
  rules as plain functions `rule( drawn, domains ) -> domains`, lowest entropy
  first, `ABSENT` for a slot that stays empty. It knows nothing about Tieflings,
  so the Aasimar can use it later.
- **The grammar is generic too** (`SpeciesKit/grammar.py`): rewrite rules,
  upper-case symbols rewritten leftmost first, lower-case lexical items
  slotted from outside, each choice on the Character's dice. The Tiefling
  rules live in `Tieflings/Grammar_of_Aspect.py`; the grammar of every slot's
  words (what a horn shape must be to fit every production) is written on its
  part in `pins.py`.
- **The Tiefling layer** (`Tieflings/Fiendish_Aspect.py`) builds the slots
  from the blood's legacies, states the four rules, and composes the
  paragraph. Each legacy Tag carries only `PLACE` (a name) and `MARKS` (its
  Pin), beside its rules.
- **Drawn once, in the Heritage's Imprint** (`Imprint_Fiendish_Heritage`),
  from three named, level-free Dice Bags: `identity.species.Tiefling.fiendish_blood`
  (the second legacy), `…fiendish_blood.aspect` (the collapse) and
  `…fiendish_blood.voice` (the grammar). Decree 0002
  and 0009: every roll on the Character's own Dice, a choice made once in an
  Imprint, reading pure. A level-up never changes the aspect. Both bags are new
  and independent, so no other draw moves. Every candidate list is sorted by
  name, so no draw depends on registration or set order.
- **One policy for a missing blood: fail loudly.** Every reader takes
  `target.fiendish_blood` directly. The Imprint draws the blood whenever it
  sets a Heritage, so a Tiefling with a Heritage and no blood can only be a bug
  (review of #122).

## 📏 Measured

- SpeciesKit self-test green, with four tests for this questa: the grammar is
  complete (every symbol has a rule, every rule is used, every lexical item is
  one the aspect fills); the marks are
  a vocabulary (each mark fills exactly one part; each legacy has at least two
  horn shapes, lent by it alone); the aspect collapses for every pair of
  legacies on 40 seeds each, deterministically, obeying all four rules and
  naming exactly one place; and the Character path (60 seeds).
- Fingerprint identical to `main` (every Entry keeps its title). Sheet
  snapshot: only Tiefling sheets move, and only in their Heritage paragraph.

## ❓ Open, for Julio

1. **Voices.** Six presentations, ten rewrite rules, and two sentences for
   every mark said on its own; a new turn of phrase is one more production or
   one more sentence on a mark.
2. **Passing.** The canon says Chthonic passes as human most easily and
   Abyssal is hardest to hide. A structure could say so for the suggested
   legacy; not done yet.
3. **Tails.** Only the Nine Hells lend one. A blood with another legacy may
   have none (half the time, by the dice). Should Abyssal lend a tail of its
   own?
4. **Applying the marks.** Marks are words in a vocabulary, kept on the blood;
   they are never applied to the Character. Applying them would make
   `char in Horns_Crown` true, at the cost of many small Tags on every
   Tiefling. Worth it?
