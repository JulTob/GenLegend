"""
Grammar of Aspect — the rewrite rules a Tiefling's aspect is written with.

The beauty of the generator is mixing ups and downs (Julio, 2026-11-01).  So
this grammar holds every register at once, side by side as options, and lets
the collapse find each Tiefling's story: plain, tender ("strangely
beautiful"), punk ("born this way", a rough past and the road still open), and
sad (the stares, the stones, the hood kept up).  One Tiefling with a really
sad story is fine; all of them sad is not, and neither is all of them punk.
No register is forced: the chips fall as they may.

Variety comes from structure inside structure, and from more lines:

- **Clause and afterthought.**  A feature is a mark's own clause, and
  sometimes an afterthought sentence of its own ("{horns}.{HORN_AFTER}").
  Most afterthoughts are empty, listed several times on purpose; an
  afterthought never joins the clause with a comma, so it never piles onto a
  clause that has one.
- **Frame first, or verdict last.**  The same idea in two positions: "Nobody
  forgets your horns: ram's horns of polished jet, curling back over your
  ears." and "Ram's horns of polished jet, curling back over your ears:
  nobody forgets them."
- **Nested small variations.**  Who reacts ({PEOPLE}), how a scent is
  reported ({SAY_SCENT}), how the fur takes the light ({SHEEN_LINE}).
- **A closing drawn in halves.**  "{PAST}, {FUTURE}.": every past with every
  future, sad, punk or tender, so a closing may lift a sad paragraph or sour
  a bright one.

The marks are the lexicon (each mark sentence is a clause, no full stop):

- ``{horns}`` / ``{eyes}`` / ``{scent}`` / ``{tail}`` / ``{bearing}``: a
  mark's own clauses
- ``{horn_phrase}`` / ``{eyes_phrase}`` / ``{scent_phrase}``: the marks as
  noun phrases, and ``{horn_phrase_cap}`` / ``{eyes_phrase_cap}`` the same
  with a capital, to open a sentence; ``{omen}``: what people say a scent
  means
- ``{horn_material}``, ``{fur}``, ``{sheen}``, ``{place}``
- ``{full_name}``: kept, and filled when the sheet is printed (#124)

Every production must read as English for every item its slots can hold; no
semicolons.  Words a production adds are not keyed, so a production should
not reuse a word a mark may bring.
"""

from __future__ import annotations


GRAMMAR: dict[str, tuple[str, ...]] = {

	# --- Sentences -------------------------------------------------------

	# The mark's own clause is listed three times: the framed and verdict
	# forms are spice, not the meal.
	"HORNS": (
		"{horns}.{HORN_AFTER}",
		"{horns}.{HORN_AFTER}",
		"{horns}.{HORN_AFTER}",
		"{HORN_FRAME}: {horn_phrase}.",
		"{horn_phrase_cap}: {HORN_VERDICT}.",
		),

	"EYES": (
		"{eyes}.{EYE_AFTER}",
		"{eyes}.{EYE_AFTER}",
		"{eyes}.{EYE_AFTER}",
		"{EYE_FRAME}: {eyes_phrase}.",
		"{eyes_phrase_cap}: {EYE_VERDICT}.",
		),

	# {fur} may carry commas of its own, so a clause ends on it; the sheen
	# comes before it, or after it as a sentence of its own.
	"FUR": (
		"{FUR_BODY}{FUR_AFTER}",
		"{FUR_BODY}{FUR_AFTER}",
		"Your fur is {fur}. {SHEEN_LINE}{FUR_AFTER}",
		"Your coat is {fur}. {SHEEN_LINE}{FUR_AFTER}",
		),

	"FUR_BODY": (
		"Lamplight finds {sheen} in your fur, which is {fur}.",
		"A glint of {sheen} runs through your fur, which is {fur}.",
		"Your fur carries a sheen of {sheen}: {fur}.",
		"When you turn, a sheen of {sheen} moves through your coat of {fur}.",
		),

	"SHEEN_LINE": (
		"Where the light catches it, it gleams like {sheen}.",
		"In lamplight it takes on a sheen of {sheen}.",
		"It holds a sheen of {sheen}, the way old coins do.",
		"When you move, it shows a subtle sheen of {sheen}.",
		),

	"SCENT": (
		"{scent}.{SCENT_AFTER}",
		"{scent}.{SCENT_AFTER}",
		"{SAY_SCENT} you smell like {omen}, of {scent_phrase}.{SCENT_AFTER}",
		"You smell of {scent_phrase}, and {PEOPLE_LOWER} call it the smell of {omen}.",
		"{SAY_SCENT} you smell like {omen}.",
		),

	"TAIL": (
		"{tail}.",
		),

	"BEARING": (
		"{bearing}.",
		),

	"CLOSE": (
		"{PAST}, {FUTURE}.",
		),

	"PLACE": (
		"Your looks suggest your {LINE} {BEGINS} {place}.",
		"{WHO} would say your {LINE} {BEGINS} {place}.",
		"{WHO} would trace your {LINE} to {place}.",
		"Some whisper that your {LINE} comes straight from {place}.",
		"{HOSTILE} say your {LINE} {BEGINS} {place}, as if that settled anything.",
		"{HOSTILE} say your {LINE} {BEGINS} {place}, and they say it loudly.",
		),

	"PLACE_OPENING": (
		"Your looks suggest your {LINE} {BEGINS} {place}, though nobody can say how many generations ago.",
		"{WHO} would trace your {LINE} to {place}, though not how far.",
		"Some whisper that your {LINE} comes straight from {place}, and nobody asks twice.",
		"{HOSTILE} say your {LINE} {BEGINS} {place}, and you have stopped arguing.",
		),

	# --- Afterthoughts: plain, tender, punk and sad, side by side --------

	# A horn clause need not say "horns" ("A wreath of bone lies flat along
	# your skull"), so every afterthought names them.
	"HORN_AFTER": (
		"",
		"",
		"",
		"",
		"",
		" You have never once filed your horns down.",
		" One horn was chipped in an old fight, and it is no less beautiful for it.",
		" Strangers stare at your horns until they forget to be afraid.",
		" You wear your horns as if you chose them.",
		" Children point at your horns, and these days you point back.",
		" In the right light your horns are almost lovely, and you have learned where the right light is.",
		" As a child you filed your horns down every spring, and every summer they grew back.",
		" No hat has ever sat right on you, and no innkeeper has ever missed why.",
		),

	"EYE_AFTER": (
		"",
		"",
		"",
		"",
		"",
		" You have stopped looking away first.",
		" People call them unsettling, right up until they call them beautiful.",
		" They have seen worse than whoever is staring back.",
		" Someone once told you they were beautiful, and you still remember who.",
		" Children are never afraid of them, only adults.",
		" You learned young to keep them lowered.",
		),

	"SCENT_AFTER": (
		"",
		"",
		"",
		"",
		" You have made your peace with it.",
		" Some find it strange, and a few find it irresistible.",
		" You wear it like a perfume you chose.",
		" Nobody has ever washed it off you, and you stopped letting them try.",
		" Dogs adore it, which is more than can be said for their owners.",
		" You have scrubbed until your skin was raw, and it never washes off.",
		),

	"FUR_AFTER": (
		"",
		"",
		"",
		"",
		"",
		" An old scar runs through it, and you never bothered to hide it.",
		" You keep it short, wild, and entirely your own.",
		" Here and there it grows back paler, over scars you no longer explain.",
		" It carries old scars, the kind a crowd leaves.",
		" There is a scar in it for every town that wanted you gone.",
		" It still shows the marks of more than one thrown stone.",
		" It is softer than anyone expects, and only a few have found out.",
		),

	# --- Frames and verdicts: the same idea at either end ----------------

	"HORN_FRAME": (
		"You were born with them",
		"Nobody forgets your horns",
		"{PEOPLE} see the horns first, and you a little after",
		"{PEOPLE} see the horns first, and you a long time after",
		"{full_name}'s face is strangely beautiful, but most people remember the horns",
		"{full_name}'s face is of great beauty, but most people only notice the horns",
		"Children point at the horns before their parents pull them away",
		),

	"HORN_VERDICT": (
		"nobody forgets them",
		"you were born with them",
		"{PEOPLE_LOWER} see them first, and you a little after",
		"children point at them before their parents pull them away",
		"you would not trade them for anything",
		),

	"EYE_FRAME": (
		"People remember your eyes long after your name",
		"Few people hold your gaze for long",
		"Your eyes are the strangest thing about you, and the loveliest",
		"Innkeepers look anywhere but at your eyes",
		"Priests make a quiet sign when they meet your eyes",
		"Mothers tell their children not to look at your eyes",
		),

	"EYE_VERDICT": (
		"few people hold them for long",
		"people remember them long after your name",
		"the strangest thing about you, and the loveliest",
		"priests make a quiet sign when they meet them",
		),

	"PEOPLE": (
		"Strangers",
		"Most people",
		"Guards",
		"Travellers",
		),

	"PEOPLE_LOWER": (
		"strangers",
		"most people",
		"guards",
		"travellers",
		),

	"SAY_SCENT": (
		"People say",
		"Behind your back, they say",
		"You have been told, more than once, that",
		"Old women in the market say",
		),

	# --- The closing: a past and a future, any with any ------------------

	"PAST": (
		"Your past is rough at the edges",
		"You have been run out of more towns than you can name",
		"You were born this way",
		"You have walked a hard road to get here",
		"You were left on a temple step, or so the story goes",
		"You have buried more friends than you meant to",
		"You grew up being told what you were",
		),

	"FUTURE": (
		"but the road ahead is wide open",
		"and still you walk as if the world owes you a song",
		"but you have decided the best part has not happened yet",
		"and you have decided that is the interesting part",
		"and you are still deciding what to make of it",
		"and some nights you are not sure it was worth it",
		"but the people who matter have stopped noticing the horns",
		),

	# --- The place: named, never described --------------------------------

	"WHO": (
		"Anyone who knows the signs",
		"Those who read such things",
		"A scholar of such matters",
		),

	"HOSTILE": (
		"Those who spit at your feet",
		"The priests who turned you away",
		"The ones who throw stones",
		),

	"LINE": (
		"bloodline",
		"line",
		"blood",
		),

	"BEGINS": (
		"starts in",
		"begins in",
		"rises from",
		"was first kindled in",
		),
	}
