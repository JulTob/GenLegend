# QST-0153 — The aspect carries how the world regards a Tiefling (experiment)

- **Type:** experiment · lore (📗) · generator
- **Priority:** 🟢 low until Julio reads the samples *(Julio, 2026-11-01: "Keep the current work, but branch to try this idea.")*
- **Status:** Working — an experimental branch stacked on QST-0151 (#122)
- **Owner:** unclaimed
- **Route to:** Lore (Bard)
- **Parent:** QST-0151 · **Related:** `Documenta/Canon/Mythos/Tiefling.md` §0 (passing), §4 (a diaspora with no homeland) · #124 (`{name}` and titles)

---

## 🔍 The idea, in Julio's words

> The talaria and halo are emotional anchors, they evoke an emotional
> response... But what would a tiefling feel when described? When everything
> said about them rings of insults, and fear? They would inspire frustration,
> fear, anger. Maybe starting the presentation with that... like "Your fur of
> {fur} carries multiple scars", or "{name}'s face is of great beauty, but
> most people only notice the horns: {horns}" or "People say you smell like a
> funeral, to incense and myrrh". [...] Transmitting not just the looks, but
> the meaning and vibe those looks carry onto you as a character. The "you
> are not passing" or "you must hide" vibe.

He also noted that a grammar works best when a start can be finished by
several endings, and that QST-0151 had taken too much of that away.

## 🧭 What the experiment does

- **Leads and endings.** A look is said, two times in three, through how
  someone else meets it: a lead ("Children point at the horns before their
  parents pull them away", "Innkeepers look anywhere but at your eyes",
  "People say you smell like a funeral") finished by the mark as a noun
  phrase (`PHRASE`), or by what people say a scent means (`OMEN`). Any lead
  finishes with any mark, so the mixing comes back.
- **A bearing.** A new slot in the collapse, lent by the legacies: how the
  look is carried. Chthonic lends passing ("Under a hood and in poor light you
  can pass for human, almost, and almost is a word you know well"), the Abyss
  lends no hiding at all, the Nine Hells lend the ones who stopped
  apologising. This is the emotional anchor, as the talaria and the halo are
  for the Aasimar.
- **Scars, stares, the hostile voice.** The fur carries scars "the kind a
  crowd leaves"; the place is said by "those who spit at your feet", "as if
  that settled anything". The hells are still only named, never described.
- **The name.** A lead may name the Character. The aspect is drawn before the
  Character has a name, so the grammar keeps `{full_name}` in place
  (`Derive(..., keep=...)`), and the Species projection fills it on its second
  pass, after naming. A Tiefling keeps its drawn paragraph as
  `heritage_description`, which `Project_Species_Description` prints ahead of
  a Heritage's fixed `HERITAGE_DESCRIPTION`.

## ❓ For Julio

1. Is this the voice? Samples in the PR body.
2. Should it replace QST-0151's presentations, or join them (the collapse can
   hold both kinds of structure, so some Tieflings are described plainly and
   some through regard)?
3. How bitter? The leads range from stares to thrown stones; a table may want
   that dialled.
