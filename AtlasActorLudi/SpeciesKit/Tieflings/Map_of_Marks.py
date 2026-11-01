"""
Map of Marks — every piece a Tiefling's aspect can be made of.

One row is one mark: its part (which slot it fills), the legacies that lend
it, its text, and its keys (the salient words it brings; no two marks in one
aspect may share a key).  The grammar each part's text must follow is written
on the part itself, in ``pins``.

What each legacy lends, in short (QST-0151, Julio's rulings of 2026-10-31):

- **Chthonic**: horns worn close like a crown, a tiara, a diadem (the least
  demonised of the three); pale, quiet materials; black eyes with one vivid
  colour; the coats of foxes, wolves and bulls, or the grey of a corpse;
  silver, pewter, iron; incense, myrrh, rain and turned earth.
- **Infernal**: horns that curl like a ram's or sweep back perfectly matched;
  jet, onyx, blued iron; black eyes with a gold or ember iris; black or a
  flame's colours; gold, brass, copper; sulfur, a doused campfire, the forge;
  the arrow-tipped tail.
- **Abyssal**: horns that twist, branch and spiral and never match; agate,
  nacre, beetle shell; eyes that will not keep one colour; the brightest
  coats, and markings that drift; bismuth, verdigris, electrum; wine just
  opened (the demons' smell), storms, brine and things gone too sweet.

The hells themselves are never described here or anywhere on the page: the
aspect only suggests where a bloodline starts (``Fiendish_Aspect``).

The marks that are said on their own (a horn shape, the eyes, a scent, a tail)
bring their own sentences, several each, and the grammar draws one: a word
with its own frames.  The aspect is a presentation, not an inventory: each
structure says only a few of these things, and says them well.

The old fixed paragraphs (one per legacy, before QST-0151) were the source of
these rows; they are reworked into parts, not kept.
"""

from __future__ import annotations

from AtlasActorLudi.SpeciesKit.Tieflings.pins import Abyssal_Marks
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Bearing
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Chthonic_Marks
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Coat
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Coat_Pattern
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Eyes
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Horn_Material
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Horn_Shape
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Infernal_Marks
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Make_Mark
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Make_Structure
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Scent
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Sheen
from AtlasActorLudi.SpeciesKit.Tieflings.pins import Tail


ABYSS = ( Abyssal_Marks, )
HADES = ( Chthonic_Marks, )
HELLS = ( Infernal_Marks, )
EVERY_LEGACY = (
		Abyssal_Marks,
		Chthonic_Marks,
		Infernal_Marks,
		)


# ---------------------------------------------------------------------------
# Structures: presentations.  Each says only a few things, in its own order;
# every sentence is a symbol of the aspect's grammar (``Grammar_of_Aspect``).
# A part a structure does not say stays empty (``Fiendish_Aspect``).
# ---------------------------------------------------------------------------

STRUCTURES = (
		Make_Structure(
				"Regard_Horns",
				"{HORNS}",
				"{FUR}",
				"{BEARING}",
				"{PLACE}",
				),
		Make_Structure(
				"Regard_Scent",
				"{SCENT}",
				"{EYES}",
				"{BEARING}",
				"{PLACE}",
				),
		Make_Structure(
				"Regard_Gaze",
				"{EYES}",
				"{HORNS}",
				"{SCENT}",
				"{BEARING}",
				),
		Make_Structure(
				"Regard_Hiding",
				"{BEARING}",
				"{FUR}",
				"{TAIL}",
				"{PLACE}",
				),
		Make_Structure(
				"Regard_Portrait",
				"{HORNS}",
				"{EYES}",
				"{SCENT}",
				"{BEARING}",
				"{PLACE}",
				),
		)


# ---------------------------------------------------------------------------
# Horns: every legacy has its own shapes and its own materials.  A shape
# brings its sentences, with the material set inside them.
# ---------------------------------------------------------------------------

HORN_SHAPES = (
		Make_Mark( "Horns_Crown", part=Horn_Shape, lent_by=HADES, keys=( "crown", "close" ), phrase="a crown of {horn_material}, worn so close that it could be taken for a real one",
				text=(
						"A crown of {horn_material} rises from your brow, so close to your head that strangers take it for one.",
						"Your horns sit close to your head like a crown of {horn_material}.",
						) ),
		Make_Mark( "Horns_Tiara", part=Horn_Shape, lent_by=HADES, keys=( "tiara", ), phrase="low horns of {horn_material} that follow your temples like a tiara",
				text=(
						"Low horns of {horn_material} follow your temples like a tiara someone forgot to take off.",
						"Your horns lie low along your temples, a tiara of {horn_material}.",
						) ),
		Make_Mark( "Horns_Diadem", part=Horn_Shape, lent_by=HADES, keys=( "diadem", ), phrase="short points of {horn_material} ringing your brow like a diadem",
				text=(
						"Short points of {horn_material} ring your brow like a diadem.",
						"A diadem of {horn_material} rings your brow, too even to be an accident.",
						) ),
		Make_Mark( "Horns_Ram", part=Horn_Shape, lent_by=HELLS, keys=( "ram", "back" ), phrase="ram's horns of {horn_material}, curling back over your ears",
				text=(
						"Ram's horns of {horn_material} curl back over your ears.",
						"Your horns curl back over your ears like a ram's, {horn_material} catching the light.",
						) ),
		Make_Mark( "Horns_Swept", part=Horn_Shape, lent_by=HELLS, keys=( "swept", "back" ), phrase="two horns of {horn_material}, swept back and matched to the last curve",
				text=(
						"Two horns of {horn_material} sweep back from your brow, matched to the last curve.",
						"Your horns sweep back from your brow in a perfect pair, smooth as {horn_material}.",
						) ),
		Make_Mark( "Horns_Spires", part=Horn_Shape, lent_by=HELLS, keys=( "spire", ), phrase="two ridged spires of {horn_material}",
				text=(
						"Two ridged spires of {horn_material} rise from your brow.",
						"Your horns rise straight from your brow, ridged spires of {horn_material}.",
						) ),
		Make_Mark( "Horns_Twisted", part=Horn_Shape, lent_by=ABYSS, keys=( "twisted", ), phrase="twisted spikes of {horn_material}, no two alike",
				text=(
						"Twisted spikes of {horn_material} break from your brow, no two alike.",
						"Your horns grow in twisted spikes of {horn_material}, and no two of them agree.",
						) ),
		Make_Mark( "Horns_Barbed", part=Horn_Shape, lent_by=ABYSS, keys=( "barb", ), phrase="barbed horns of {horn_material}, never the same on both sides",
				text=(
						"Barbed horns of {horn_material} branch from your head, never the same on both sides.",
						"Your horns branch into barbs of {horn_material}, each side going its own way.",
						) ),
		Make_Mark( "Horns_Spiral", part=Horn_Shape, lent_by=ABYSS, keys=( "spiral", ), phrase="two spirals of {horn_material}, each turning the wrong way",
				text=(
						"Your horns of {horn_material} spiral in opposite directions, as if neither asked the other.",
						"Two spirals of {horn_material} turn from your brow, each the wrong way round.",
						) ),
		)

HORN_MATERIALS = (
		Make_Mark( "Horn_Ivory", part=Horn_Material, lent_by=HADES, keys=( "ivory", ),
				text="old ivory" ),
		Make_Mark( "Horn_Bone", part=Horn_Material, lent_by=HADES, keys=( "bone", ),
				text="sun-bleached bone" ),
		Make_Mark( "Horn_Antler", part=Horn_Material, lent_by=HADES, keys=( "antler", ),
				text="pale antler" ),
		Make_Mark( "Horn_Jet", part=Horn_Material, lent_by=HELLS, keys=( "jet", ),
				text="polished jet" ),
		Make_Mark( "Horn_Onyx", part=Horn_Material, lent_by=HELLS, keys=( "onyx", ),
				text="onyx" ),
		Make_Mark( "Horn_Blued_Iron", part=Horn_Material, lent_by=HELLS, keys=( "iron", ),
				text="blued iron" ),
		Make_Mark( "Horn_Agate", part=Horn_Material, lent_by=ABYSS, keys=( "agate", ),
				text="banded agate" ),
		Make_Mark( "Horn_Nacre", part=Horn_Material, lent_by=ABYSS, keys=( "pearl", ),
				text="mother-of-pearl" ),
		Make_Mark( "Horn_Beetle", part=Horn_Material, lent_by=ABYSS, keys=( "beetle", ),
				text="beetle shell" ),
		)


# ---------------------------------------------------------------------------
# Eyes: each mark brings its own sentences.
# ---------------------------------------------------------------------------

EYES = (
		Make_Mark( "Eyes_Violet_Iris", part=Eyes, lent_by=HADES, keys=( "violet", "vivid", "grave", "black" ), phrase="black eyes, each holding a single violet iris",
				text=(
						"Your eyes are black, each holding a single violet iris, like a flower left on a grave.",
						"At the bottom of your black eyes lies a vivid violet, like a flower in a well.",
						) ),
		Make_Mark( "Eyes_Green_Iris", part=Eyes, lent_by=HADES, keys=( "green", "moss", "black" ), phrase="black eyes with irises the green of tomb moss",
				text=(
						"Your eyes are black, and their irises are the green of moss on a tombstone.",
						"In the black of your eyes sits a green iris, bright as new moss.",
						) ),
		Make_Mark( "Eyes_Ice_Iris", part=Eyes, lent_by=HADES, keys=( "ice", "well", "black" ), phrase="black eyes with irises of pale ice",
				text=(
						"Your eyes are black as a well at night, with irises of pale ice.",
						"Irises pale as ice float in eyes as black as a well.",
						) ),
		Make_Mark( "Eyes_Coal_Iris", part=Eyes, lent_by=HELLS, keys=( "gold", "coal", "black" ), phrase="black eyes with a golden iris burning in each, like a coal",
				text=(
						"Your eyes are black, and in each burns a golden iris, like a coal that will not go out.",
						"A coal of gold burns in the black of each of your eyes.",
						) ),
		Make_Mark( "Eyes_Ember_Iris", part=Eyes, lent_by=HELLS, keys=( "red", "ember", "black" ), phrase="black eyes with irises like embers in a grate",
				text=(
						"Embers sit where your irises should be, red in the black of your eyes.",
						"Your irises glow the red of embers in a grate, set in eyes of perfect black.",
						) ),
		Make_Mark( "Eyes_Candle_Iris", part=Eyes, lent_by=HELLS, keys=( "gold", "candle", "flame", "black" ), phrase="black eyes where the gold flickers like a candle",
				text=(
						"In the black of your eyes, the gold of each iris flickers like a candle flame.",
						"Your eyes are black, and the gold in them flickers like candlelight in a draught.",
						) ),
		Make_Mark( "Eyes_Borrowed", part=Eyes, lent_by=ABYSS, keys=( "brown", "stare" ), phrase="plain brown eyes that take the colour of whoever stares too long",
				text=(
						"Your eyes look an ordinary brown, until you stare too long at someone and they take on that person's colour.",
						"Your eyes are a plain brown, until you hold someone's gaze too long and they borrow its colour.",
						) ),
		Make_Mark( "Eyes_Mornings", part=Eyes, lent_by=ABYSS, keys=( "morning", "mirror" ), phrase="eyes that are never the same colour two days running",
				text=(
						"No mirror has ever seen your eyes the same colour twice.",
						"Your eyes wake each morning in a colour of their own choosing.",
						) ),
		Make_Mark( "Eyes_Moods", part=Eyes, lent_by=ABYSS, keys=( "mood", ), phrase="eyes that change colour with every mood you try to hide",
				text=(
						"Your eyes change colour before your face can, and give away every mood you would rather hide.",
						"Every mood you have shows first in your eyes, which shift colour to match it.",
						) ),
		)


# ---------------------------------------------------------------------------
# Fur: a coat colour, a pattern, and sometimes a second colour (the accent,
# drawn from the same coats).  The grammar says them with the sheen.
# ---------------------------------------------------------------------------

COATS = (
		Make_Mark( "Coat_Electric_Blue", part=Coat, lent_by=ABYSS, keys=( "blue", ),
				text="electric blue" ),
		Make_Mark( "Coat_Acid_Green", part=Coat, lent_by=ABYSS, keys=( "green", ),
				text="acid green" ),
		Make_Mark( "Coat_Bright_Violet", part=Coat, lent_by=ABYSS, keys=( "violet", ),
				text="bright violet" ),
		Make_Mark( "Coat_Vivid_Magenta", part=Coat, lent_by=ABYSS, keys=( "magenta", "vivid" ),
				text="vivid magenta" ),
		Make_Mark( "Coat_Fox_Red", part=Coat, lent_by=HADES, keys=( "red", "fox" ),
				text="fox red" ),
		Make_Mark( "Coat_Wolf_Grey", part=Coat, lent_by=HADES, keys=( "grey", "wolf" ),
				text="wolf grey" ),
		Make_Mark( "Coat_Bull_Brown", part=Coat, lent_by=HADES, keys=( "brown", "bull" ),
				text="bull brown" ),
		Make_Mark( "Coat_Corpse_White", part=Coat, lent_by=HADES, keys=( "white", "corpse" ),
				text="corpse-white" ),
		Make_Mark( "Coat_Onyx_Black", part=Coat, lent_by=HELLS, keys=( "black", "onyx" ),
				text="onyx black" ),
		Make_Mark( "Coat_Flame_Red", part=Coat, lent_by=HELLS, keys=( "red", "flame" ),
				text="flame red" ),
		Make_Mark( "Coat_Ember_Orange", part=Coat, lent_by=HELLS, keys=( "orange", "ember" ),
				text="ember orange" ),
		Make_Mark( "Coat_Brimstone_Yellow", part=Coat, lent_by=HELLS, keys=( "yellow", "brimstone" ),
				text="brimstone yellow" ),
		)

COAT_PATTERNS = (
		# One colour.
		Make_Mark( "Pattern_Plain", part=Coat_Pattern, lent_by=EVERY_LEGACY,
				text="{a}" ),
		Make_Mark( "Pattern_Darker_Back", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "back", ),
				text="{a}, darker along your back" ),
		Make_Mark( "Pattern_Paler_Beneath", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "beneath", ),
				text="{a}, paler beneath" ),
		Make_Mark( "Pattern_Hound_Sleek", part=Coat_Pattern, lent_by=HADES, keys=( "hound", "close" ),
				text="{a}, sleek and close like a hound's" ),
		Make_Mark( "Pattern_Charred_Tips", part=Coat_Pattern, lent_by=HELLS, keys=( "tips", ),
				text="{a}, darkening at the tips like charred wood" ),
		# Two colours.
		Make_Mark( "Pattern_Spotted", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "spots", ),
				text="{a}, spotted with {b}" ),
		Make_Mark( "Pattern_Striped", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "stripes", ),
				text="{a}, striped with {b}" ),
		Make_Mark( "Pattern_Faded_Tips", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "tips", ),
				text="{a}, fading to {b} at the tips" ),
		Make_Mark( "Pattern_Back_And_Beneath", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "back", "beneath" ),
				text="{a} along your back and {b} beneath" ),
		Make_Mark( "Pattern_Mask", part=Coat_Pattern, lent_by=EVERY_LEGACY, keys=( "mask", ),
				text="{a}, with a mask of {b} around your eyes" ),
		Make_Mark( "Pattern_Blaze", part=Coat_Pattern, lent_by=HADES, keys=( "blaze", ),
				text="{a}, with a blaze of {b} on your chest" ),
		Make_Mark( "Pattern_Licking_Flame", part=Coat_Pattern, lent_by=HELLS, keys=( "flame", "tips" ),
				text="{a}, with {b} licking up from the tips like flame" ),
		Make_Mark( "Pattern_Drifting_Spots", part=Coat_Pattern, lent_by=ABYSS, keys=( "spots", ),
				text="{a}, with spots of {b} that drift a little every night" ),
		Make_Mark( "Pattern_Wandering_Stripes", part=Coat_Pattern, lent_by=ABYSS, keys=( "stripes", ),
				text="{a}, with stripes of {b} that never sit in the same place twice" ),
		)


# ---------------------------------------------------------------------------
# The sheen: every Tiefling's fur catches the light like metal, subtly.
# ---------------------------------------------------------------------------

SHEENS = (
		Make_Mark( "Sheen_Silver", part=Sheen, lent_by=HADES, keys=( "silver", ),
				text="silver" ),
		Make_Mark( "Sheen_Pewter", part=Sheen, lent_by=HADES, keys=( "pewter", ),
				text="pewter" ),
		Make_Mark( "Sheen_Iron", part=Sheen, lent_by=HADES, keys=( "iron", ),
				text="iron" ),
		Make_Mark( "Sheen_Gold", part=Sheen, lent_by=HELLS, keys=( "gold", ),
				text="gold" ),
		Make_Mark( "Sheen_Brass", part=Sheen, lent_by=HELLS, keys=( "brass", ),
				text="brass" ),
		Make_Mark( "Sheen_Copper", part=Sheen, lent_by=HELLS, keys=( "copper", ),
				text="copper" ),
		Make_Mark( "Sheen_Bismuth", part=Sheen, lent_by=ABYSS, keys=( "bismuth", ),
				text="bismuth" ),
		Make_Mark( "Sheen_Verdigris", part=Sheen, lent_by=ABYSS, keys=( "verdigris", ),
				text="verdigris" ),
		Make_Mark( "Sheen_Electrum", part=Sheen, lent_by=ABYSS, keys=( "electrum", ),
				text="electrum" ),
		)


# ---------------------------------------------------------------------------
# Scents: each mark brings its own sentences.  Subtle, and never explained.
# Wine is the demons' smell, so the Abyss lends it.
# ---------------------------------------------------------------------------

SCENTS = (
		Make_Mark( "Scent_Incense", part=Scent, lent_by=HADES, keys=( "incense", "temple" ), phrase="incense", omen="a funeral",
				text=(
						"A breath of incense follows you, as if you had just left a temple nobody remembers.",
						"You smell faintly of incense, the kind burned for the dead.",
						) ),
		Make_Mark( "Scent_Myrrh", part=Scent, lent_by=HADES, keys=( "myrrh", ), phrase="myrrh", omen="a tomb",
				text=(
						"Myrrh clings to you, sweet and ancient, like the inside of a reliquary.",
						"There is myrrh in your hair, though you have never bought any.",
						) ),
		Make_Mark( "Scent_Rain", part=Scent, lent_by=HADES, keys=( "rain", ), phrase="rain on stone", omen="an open grave",
				text=(
						"The smell of rain lingers in you, like a persistent memory.",
						"You smell of rain on stone, even under a cloudless sky.",
						) ),
		Make_Mark( "Scent_Turned_Earth", part=Scent, lent_by=HADES, keys=( "earth", "grave" ), phrase="turned earth", omen="a fresh grave",
				text=(
						"You smell of freshly turned earth, the way a garden does, or a grave.",
						"Wherever you sleep, the room smells of turned earth by morning.",
						) ),
		Make_Mark( "Scent_Sulfur", part=Scent, lent_by=HELLS, keys=( "sulfur", "match" ), phrase="sulfur", omen="a curse being spoken",
				text=(
						"A trace of sulfur follows you, like a struck match that never quite goes out.",
						"Every room you enter smells, briefly, of sulfur.",
						) ),
		Make_Mark( "Scent_Campfire", part=Scent, lent_by=HELLS, keys=( "campfire", "smoke" ), phrase="old smoke", omen="a burned house",
				text=(
						"You smell like a campfire just put out, warm and a little dangerous.",
						"Smoke from a fire long since doused still clings to you.",
						) ),
		Make_Mark( "Scent_Forge", part=Scent, lent_by=HELLS, keys=( "iron", "forge" ), phrase="hot iron", omen="a branding",
				text=(
						"You carry the smell of hot iron, like a forge at the end of the day.",
						"Close to you, the air smells of iron fresh from the forge.",
						) ),
		Make_Mark( "Scent_Snuffed_Candle", part=Scent, lent_by=HELLS, keys=( "candle", "smoke" ), phrase="snuffed candles", omen="a wake",
				text=(
						"You smell of a snuffed candle, that thin smoke that means someone has just left.",
						) ),
		Make_Mark( "Scent_Wine", part=Scent, lent_by=ABYSS, keys=( "wine", ), phrase="freshly opened wine", omen="a feast gone wrong",
				text=(
						"You smell of freshly opened wine, even in clean, fine clothes.",
						"A scent of wine just uncorked follows you, rich and a little too sweet.",
						) ),
		Make_Mark( "Scent_Storm", part=Scent, lent_by=ABYSS, keys=( "storm", "lightning" ), phrase="lightning", omen="a storm about to break",
				text=(
						"The air around you smells the way it does before a storm.",
						"You smell of the air before lightning, sharp and restless.",
						) ),
		Make_Mark( "Scent_Brine", part=Scent, lent_by=ABYSS, keys=( "brine", "sea" ), phrase="brine", omen="a drowned sailor",
				text=(
						"You smell of brine, as if you had just walked out of the sea.",
						"Salt and brine cling to you, however far you are from any coast.",
						) ),
		Make_Mark( "Scent_Overripe", part=Scent, lent_by=ABYSS, keys=( "sweet", "fruit" ), phrase="overripe fruit", omen="rot dressed up as sweetness",
				text=(
						"A sweetness of overripe fruit hangs about you, pleasant for a moment too long.",
						"You smell of flowers left too long in the vase, sweet on the edge of turning.",
						) ),
		)


# ---------------------------------------------------------------------------
# Tails: only the Nine Hells lend one.  A structure that says the tail is
# never drawn for a blood that has none (``Fiendish_Aspect``).
# ---------------------------------------------------------------------------

TAILS = (
		Make_Mark( "Tail_Arrow", part=Tail, lent_by=HELLS, keys=( "arrow", "tips" ),
				text=(
						"A long tail sways behind you, ending in an arrow-shaped tip.",
						"Behind you, a long tail ends in a tip shaped like an arrowhead.",
						"You keep your tail wound under your coat, but it lashes when you are angry, and then everyone knows.",
						) ),
		Make_Mark( "Tail_Lash", part=Tail, lent_by=HELLS, keys=( "arrow", "barb", "tips" ),
				text=(
						"A thin tail lashes behind you when you are angry, its tip barbed like an arrow.",
						"You have learned to sit with your back to the wall, so nobody steps on the tail, or stares at it.",
						) ),
		)


# ---------------------------------------------------------------------------
# Bearing: how the look is carried, which is what the look means.  The canon
# says Chthonic passes for human most easily and Abyssal is the hardest to
# hide; the Nine Hells lend the ones who stopped trying.
# ---------------------------------------------------------------------------

BEARINGS = (
		Make_Mark( "Bearing_Almost_Passing", part=Bearing, lent_by=HADES, keys=( "pass", ),
				text=(
						"Under a hood and in poor light you can pass for human, almost, and almost is a word you know well.",
						"You can pass, on a dark day, and you have learned exactly how dark it needs to be.",
						) ),
		Make_Mark( "Bearing_Hood", part=Bearing, lent_by=HADES, keys=( "hood", ),
				text=(
						"You own more hoods than shirts, and every one of them is deep.",
						"You keep your hood up in every town, and still the dogs bark.",
						) ),
		Make_Mark( "Bearing_No_Hiding", part=Bearing, lent_by=ABYSS, keys=( "hide", ),
				text=(
						"No hood was ever deep enough to hide you, so you stopped trying.",
						"There is no hiding what you are, and every town lets you know it before the gates.",
						) ),
		Make_Mark( "Bearing_Watched", part=Bearing, lent_by=ABYSS, keys=( "watch", ),
				text=(
						"Wherever you go, someone is watching your hands.",
						"Shopkeepers count their wares twice when you walk in, and you have stopped pretending not to see it.",
						) ),
		Make_Mark( "Bearing_Defiant", part=Bearing, lent_by=HELLS, keys=( "eyes_down", ),
				text=(
						"You stopped lowering your eyes a long time ago, and people notice that more than the horns.",
						"You learned early that apologising changes nothing, so you stopped.",
						) ),
		Make_Mark( "Bearing_Hands_Seen", part=Bearing, lent_by=HELLS, keys=( "hands", ),
				text=(
						"You keep your hands where people can see them, and that has saved your life more than once.",
						"You speak softly and move slowly, because the alternative has cost you before.",
						) ),
		)


ROSTER = (
		*STRUCTURES,
		*HORN_SHAPES,
		*HORN_MATERIALS,
		*EYES,
		*COATS,
		*COAT_PATTERNS,
		*SHEENS,
		*SCENTS,
		*TAILS,
		*BEARINGS,
		)
