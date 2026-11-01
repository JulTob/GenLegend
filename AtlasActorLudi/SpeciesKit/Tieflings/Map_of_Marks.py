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
		# Plain presentations (QST-0151): the look, said well.
		Make_Structure( "Scent_Led", "{SCENT}", "{HORNS}", "{EYES}", "{PLACE}" ),
		Make_Structure( "Horns_Led", "{HORNS}", "{FUR}", "{TAIL}", "{PLACE}" ),
		Make_Structure( "Gaze_Led", "{EYES}", "{HORNS}", "{SCENT}", "{PLACE}" ),
		Make_Structure( "Place_Led", "{PLACE_OPENING}", "{FUR}", "{EYES}" ),
		Make_Structure( "Coat_Led", "{FUR}", "{TAIL}", "{SCENT}", "{PLACE}" ),
		Make_Structure( "Portrait", "{HORNS}", "{EYES}", "{FUR}", "{SCENT}", "{PLACE}" ),
		# Punk presentations (QST-0153): the same look, closing on how it is
		# carried, or on a rough past with the road still open.
		Make_Structure( "Punk_Horns", "{HORNS}", "{FUR}", "{BEARING}", "{PLACE}" ),
		Make_Structure( "Punk_Gaze", "{EYES}", "{HORNS}", "{SCENT}", "{CLOSE}" ),
		Make_Structure( "Punk_Coat", "{FUR}", "{TAIL}", "{BEARING}" ),
		Make_Structure( "Punk_Scent", "{SCENT}", "{EYES}", "{PLACE}", "{CLOSE}" ),
		Make_Structure( "Story_Portrait", "{EYES}", "{HORNS}", "{FUR}", "{CLOSE}" ),
		Make_Structure( "Rumour_Led", "{PLACE_OPENING}", "{HORNS}", "{SCENT}", "{BEARING}" ),
		)


# ---------------------------------------------------------------------------
# Horns: every legacy has its own shapes and its own materials.  A shape
# brings its sentences, with the material set inside them.
# ---------------------------------------------------------------------------

HORN_SHAPES = (
		Make_Mark( "Horns_Crown", part=Horn_Shape, lent_by=HADES, keys=( "crown", "close" ), phrase=( "horns of {horn_material} worn close as a crown, so close they could be taken for a real one", "horns of {horn_material} that ring your head close as a crown, stately enough to make mourners bow", "close-set horns of {horn_material}, a crown you were born wearing and have never once taken off" ),
				text=(
						"A crown of {horn_material} rises from your brow, so close to your head that strangers take it for one",
						"Your horns sit close to your head like a crown of {horn_material}",
						"Your horns of {horn_material} rise close to your head, a crown nobody gave you and nobody can take",
						) ),
		Make_Mark( "Horns_Tiara", part=Horn_Shape, lent_by=HADES, keys=( "tiara", ), phrase=( "low horns of {horn_material} that follow your temples like a tiara", "low horns of {horn_material} that trace your temples like a tiara, fine enough to pass for jewellery", "slender horns of {horn_material} laid along your temples like a tiara left on after the last dance" ),
				text=(
						"Low horns of {horn_material} follow your temples like a tiara someone forgot to take off",
						"Your horns lie low along your temples, a tiara of {horn_material}",
						"A low tiara of {horn_material} grows along your temples, as if you were meant for some quieter throne",
						) ),
		Make_Mark( "Horns_Diadem", part=Horn_Shape, lent_by=HADES, keys=( "diadem", ), phrase=( "short points of {horn_material} ringing your brow like a diadem", "short, even points of {horn_material} that circle your brow like a diadem, almost too fine to be horns", "short points of {horn_material} set around your brow like the diadem of some pale, nameless saint" ),
				text=(
						"Short points of {horn_material} ring your brow like a diadem",
						"A diadem of {horn_material} rings your brow, too even to be an accident",
						"Your brow is ringed with short points of {horn_material}, like a diadem worn too long",
						) ),
		Make_Mark( "Horns_Tines", part=Horn_Shape, lent_by=HADES, keys=( "tines", "antler" ), phrase=( "small tines of {horn_material} above your temples, like antlers just beginning", "small forked tines of {horn_material} above your temples, like a fawn's first antlers", "little tines of {horn_material} that branch above your temples, still as soft-looking as antlers in velvet" ),
				text=(
						"Small tines of {horn_material} branch above your temples, like antlers just beginning",
						"Your horns are only tines of {horn_material}, branching above your temples like a young stag's",
						"Little tines of {horn_material} sprout above your temples, as if your horns are still deciding what to be",
						) ),
		Make_Mark( "Horns_Laurel", part=Horn_Shape, lent_by=HADES, keys=( "laurel", ), phrase=( "horns of {horn_material} that lie flat in your hair like a laurel wreath", "flat horns of {horn_material} that follow your hair like a laurel wreath, the kind given to the honoured dead", "horns of {horn_material} pressed flat into your hair like laurel leaves, so quiet that a hood hides them completely" ),
				text=(
						"Your horns of {horn_material} lie flat against your hair, like a laurel wreath that grew there",
						"A wreath of {horn_material} lies flat along your skull, so close it could be braided",
						"Your horns are a laurel of {horn_material}, worn so long they have become part of you",
						) ),
		Make_Mark( "Horns_Ram", part=Horn_Shape, lent_by=HELLS, keys=( "ram", "back" ), phrase=( "ram's horns of {horn_material}, curling back over your ears", "heavy ram's horns of {horn_material} that curl back over your ears in two matching coils", "ram's horns of {horn_material}, curling back over your ears and built for butting through doors that stay shut" ),
				text=(
						"Ram's horns of {horn_material} curl back over your ears",
						"Your horns curl back over your ears like a ram's, {horn_material} catching the light",
						"Your horns of {horn_material} curl back over your ears like a ram's, heavy and patient",
						) ),
		Make_Mark( "Horns_Swept", part=Horn_Shape, lent_by=HELLS, keys=( "swept", "back" ), phrase=( "two horns of {horn_material}, swept back and matched to the last curve", "two horns of {horn_material} swept back from your brow like a pair of banners in the same wind", "horns of {horn_material} swept back from your brow, every curve answering its twin" ),
				text=(
						"Two horns of {horn_material} sweep back from your brow, matched to the last curve",
						"Your horns sweep back from your brow in a perfect pair, smooth as {horn_material}",
						"Your horns of {horn_material} sweep back from your brow, so perfectly matched they look carved",
						) ),
		Make_Mark( "Horns_Spires", part=Horn_Shape, lent_by=HELLS, keys=( "spire", ), phrase=( "two ridged spires of {horn_material}", "two ridged spires of {horn_material} that rise from your brow, straight as the pillars of a judge's hall", "ridged spires of {horn_material} that rise straight from your brow and add a hand's breadth to your height in every argument" ),
				text=(
						"Two ridged spires of {horn_material} rise from your brow",
						"Your horns rise straight from your brow, ridged spires of {horn_material}",
						"Two spires of {horn_material} rise from your brow, ridged like old bark",
						) ),
		Make_Mark( "Horns_Bull", part=Horn_Shape, lent_by=HELLS, keys=( "bull", ), phrase=( "thick horns of {horn_material}, sweeping out and up like a bull's", "thick horns of {horn_material}, sweeping out and up like a bull's and wide enough to clear a crowded room", "broad horns of {horn_material} that reach out and up like a prize bull's, and are carried with twice the pride" ),
				text=(
						"Thick horns of {horn_material} sweep out and up like a bull's",
						"Your horns of {horn_material} sweep out and up, broad as a bull's",
						"Your horns of {horn_material} reach out and up like a bull's, so wide that you take doorways sideways",
						) ),
		Make_Mark( "Horns_Capped", part=Horn_Shape, lent_by=HELLS, keys=( "brass", "capped" ), phrase=( "horns of {horn_material}, their tips capped in old brass", "horns of {horn_material}, each point capped in brass and polished until it gleams like a church bell", "horns of {horn_material} with old brass caps on their points, the only inheritance you ever received" ),
				text=(
						"The tips of your horns of {horn_material} are capped in old brass, a gift from someone you lost",
						"Your horns of {horn_material} end in caps of worn brass, polished every morning out of habit",
						"Old brass caps the points of your horns of {horn_material}, so you never catch a curtain again",
						) ),
		Make_Mark( "Horns_Twisted", part=Horn_Shape, lent_by=ABYSS, keys=( "twisted", ), phrase=( "twisted spikes of {horn_material}, no two alike", "twisted spikes of {horn_material} that jut from your brow at angles nobody could draw twice", "twisted spikes of {horn_material}, each growing whichever way it pleases, like the branches of a tree struck twice by lightning" ),
				text=(
						"Twisted spikes of {horn_material} break from your brow, no two alike",
						"Your horns grow in twisted spikes of {horn_material}, and no two of them agree",
						"Twisted spikes of {horn_material} crowd your brow, each growing its own way",
						) ),
		Make_Mark( "Horns_Barbed", part=Horn_Shape, lent_by=ABYSS, keys=( "barb", ), phrase=( "barbed horns of {horn_material}, never the same on both sides", "barbed horns of {horn_material} that branch like bramble, heavier on one side than the other", "branching barbs of {horn_material}, as uneven as briars and every bit as hard to hold" ),
				text=(
						"Barbed horns of {horn_material} branch from your head, never the same on both sides",
						"Your horns branch into barbs of {horn_material}, each side going its own way",
						"Barbs of {horn_material} branch from your head, more like thorns than horns",
						) ),
		Make_Mark( "Horns_Spiral", part=Horn_Shape, lent_by=ABYSS, keys=( "spiral", ), phrase=( "two spirals of {horn_material}, each turning the wrong way", "two spirals of {horn_material} that turn against each other, like dancers who never learned the same steps", "corkscrew horns of {horn_material}, one winding sunwise and the other against it" ),
				text=(
						"Your horns of {horn_material} spiral in opposite directions, as if neither asked the other",
						"Two spirals of {horn_material} turn from your brow, each the wrong way round",
						"Your horns of {horn_material} corkscrew in opposite directions, never quite agreeing",
						) ),
		Make_Mark( "Horns_Regrown", part=Horn_Shape, lent_by=ABYSS, keys=( "broken", ), phrase=( "horns of {horn_material}, one broken long ago and grown back jagged", "mismatched horns of {horn_material}, one smooth and the other grown back jagged where it broke", "horns of {horn_material} that no longer match, since one snapped in a fight you won anyway and came back jagged" ),
				text=(
						"One of your horns of {horn_material} broke long ago and grew back jagged",
						"Your horns of {horn_material} do not match, since one broke and grew back wild",
						"You broke a horn of {horn_material} once, and it grew back wilder than before",
						) ),
		Make_Mark( "Horns_Ringed", part=Horn_Shape, lent_by=ABYSS, keys=( "rings", "iron" ), phrase=( "horns of {horn_material}, pierced with a row of small iron rings", "horns of {horn_material} studded with little iron rings, every one put there by your own hand", "horns of {horn_material} pierced with a row of iron rings, one for every friend who stayed" ),
				text=(
						"Your horns of {horn_material} are pierced with small iron rings, one for every year you survived",
						"A row of little iron rings runs up each of your horns of {horn_material}, and they chime when you laugh",
						"You have hung your horns of {horn_material} with iron rings, because if people will stare, let them stare at something",
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
		Make_Mark( "Eyes_Violet_Iris", part=Eyes, lent_by=HADES, keys=( "violet", "vivid", "grave", "black" ), phrase=( "black eyes, each holding a single violet iris", "black eyes with a violet iris in each, as delicate as a pressed flower", "black eyes, each with a violet iris like a flower on a grave nobody visits" ),
				text=(
						"Your eyes are black, each holding a single violet iris, like a flower left on a grave",
						"At the bottom of your black eyes lies a vivid violet, like a flower in a well",
						"Each of your black eyes holds one violet iris, small and vivid as a bruise",
						) ),
		Make_Mark( "Eyes_Green_Iris", part=Eyes, lent_by=HADES, keys=( "green", "moss", "black" ), phrase=( "black eyes with irises the green of tomb moss", "black eyes with irises as green as moss after the thaw", "black eyes with irises green as moss, the kind that grows on anything left alone long enough" ),
				text=(
						"Your eyes are black, and their irises are the green of moss on a tombstone",
						"In the black of your eyes sits a green iris, bright as new moss",
						"Your eyes are black, with a green iris in each like a leaf at the bottom of a pond",
						) ),
		Make_Mark( "Eyes_Ice_Iris", part=Eyes, lent_by=HADES, keys=( "ice", "well", "black" ), phrase=( "black eyes with irises of pale ice", "black eyes with irises as pale as the first ice on a pond", "black eyes with irises of ice, waiting for a thaw that has not come yet" ),
				text=(
						"Your eyes are black as a well at night, with irises of pale ice",
						"Irises pale as ice float in eyes as black as a well",
						"Your black eyes hold irises so pale they look like frost on a window",
						) ),
		Make_Mark( "Eyes_Silver_Ring", part=Eyes, lent_by=HADES, keys=( "silver", "coin", "black" ), phrase=( "black eyes, each ringed with a thin line of silver", "black eyes edged with a fine thread of silver, bright as a new coin", "black eyes with a thin silver circle round each iris, like the coin the dead carry for the ferryman" ),
				text=(
						"Your eyes are black, each ringed with a thin line of silver, like a coin at the bottom of a well",
						"A thin ring of silver circles the black of each of your eyes",
						"A silver ring circles each of your black irises, like the rim of an old coin",
						) ),
		Make_Mark( "Eyes_Starless", part=Eyes, lent_by=HADES, keys=( "starless", "black" ), phrase=( "eyes black all the way through, without iris or white", "eyes of depthless black, starless and somehow kind", "eyes black from lid to lid, the starless dark of a long, deep sleep" ),
				text=(
						"Your eyes are black all the way through, without iris or white, and somehow they are kind",
						"There is no white in your eyes and no iris either, only a quiet, starless black",
						"Your eyes are black from edge to edge, like a night sky with every star put out",
						) ),
		Make_Mark( "Eyes_Coal_Iris", part=Eyes, lent_by=HELLS, keys=( "gold", "coal", "black" ), phrase=( "black eyes with a golden iris burning in each, like a coal", "black eyes with a gold iris glowing in each, like a coal that refuses to go out", "black eyes where gold burns low and steady, like coals kept for whoever comes home late" ),
				text=(
						"Your eyes are black, and in each burns a golden iris, like a coal that will not go out",
						"A coal of gold burns in the black of each of your eyes",
						"Your irises burn gold in the black of your eyes, steady as coals in a banked fire",
						) ),
		Make_Mark( "Eyes_Ember_Iris", part=Eyes, lent_by=HELLS, keys=( "red", "ember", "black" ), phrase=( "black eyes with irises like embers in a grate", "black eyes with irises of ember red, set as evenly as a pair of lamps", "black eyes with ember-red irises that nobody has managed to put out" ),
				text=(
						"Embers sit where your irises should be, red in the black of your eyes",
						"Your irises glow the red of embers in a grate, set in eyes of perfect black",
						"Your irises are the deep red of embers, and they brighten when you are angry",
						) ),
		Make_Mark( "Eyes_Candle_Iris", part=Eyes, lent_by=HELLS, keys=( "gold", "candle", "flame", "black" ), phrase=( "black eyes where the gold flickers like a candle", "black eyes where gold flickers like a candle that has outlasted every draught", "black eyes with a gold flame in each, like candles left in a window for someone on the road home" ),
				text=(
						"In the black of your eyes, the gold of each iris flickers like a candle flame",
						"Your eyes are black, and the gold in them flickers like candlelight in a draught",
						"Gold flickers in the black of your eyes, like a candle someone forgot to blow out",
						) ),
		Make_Mark( "Eyes_Furnace", part=Eyes, lent_by=HELLS, keys=( "furnace", "black" ), phrase=( "black eyes that glow like a furnace door when you are angry", "black eyes with the glow of a banked furnace somewhere deep in them", "black eyes that flare like a furnace flung open when someone pushes you too far" ),
				text=(
						"Your eyes are black, until you are angry and they glow like a furnace door left open",
						"In the black of your eyes there is a glow, banked low, like a furnace at night",
						"When you are angry, your black eyes glow from somewhere deep, like a furnace with its door ajar",
						) ),
		Make_Mark( "Eyes_Spark", part=Eyes, lent_by=HELLS, keys=( "spark", "black", "laugh" ), phrase=( "black eyes where a red spark jumps whenever you laugh", "black eyes that throw sparks whenever you laugh, like a struck flint", "black eyes where a spark wakes at the first good joke" ),
				text=(
						"Your eyes are black, and a spark of red jumps in them whenever you laugh",
						"A red spark lives in the black of your eyes, and it dances when you are pleased",
						"Your black eyes catch fire for a moment when you laugh, a single red spark in each",
						) ),
		Make_Mark( "Eyes_Borrowed", part=Eyes, lent_by=ABYSS, keys=( "brown", "stare" ), phrase=( "plain brown eyes that take the colour of whoever stares too long", "brown eyes that answer every long stare with the starer's own colour", "plain brown eyes that slowly borrow the colour of whoever stares at you longest" ),
				text=(
						"Your eyes look an ordinary brown, until you stare too long at someone and they take on that person's colour",
						"Your eyes are a plain brown, until you hold someone's gaze too long and they borrow its colour",
						"Your eyes are an ordinary brown, until someone stares too long and finds their own colour looking back",
						) ),
		Make_Mark( "Eyes_Mornings", part=Eyes, lent_by=ABYSS, keys=( "morning", "mirror" ), phrase=( "eyes that are never the same colour two days running", "eyes that greet every morning in a colour the mirror has never seen", "eyes that surprise you in the mirror every morning, and never unkindly" ),
				text=(
						"No mirror has ever seen your eyes the same colour twice",
						"Your eyes wake each morning in a colour of their own choosing",
						"Your eyes change colour overnight, and you have long since stopped checking which",
						) ),
		Make_Mark( "Eyes_Moods", part=Eyes, lent_by=ABYSS, keys=( "mood", ), phrase=( "eyes that change colour with every mood you try to hide", "eyes that tell the truth about your every mood, one colour at a time", "eyes that flush with a new colour at every mood you would rather swallow" ),
				text=(
						"Your eyes change colour before your face can, and give away every mood you would rather hide",
						"Every mood you have shows first in your eyes, which shift colour to match it",
						"Your eyes give away every mood, shifting colour faster than you can hide what you feel",
						) ),
		Make_Mark( "Eyes_Mismatched", part=Eyes, lent_by=ABYSS, keys=( "mismatch", ), phrase=( "mismatched eyes that trade their colours while you sleep", "mismatched eyes that swap colours whenever nobody is looking", "mismatched eyes, one bright as a jay's wing and the other some colour without a name" ),
				text=(
						"Your eyes do not match, and they trade their colours while you sleep",
						"One of your eyes is never the colour of the other, and they take turns",
						"Your eyes never match, and each seems to have its own opinion of the room",
						) ),
		Make_Mark( "Eyes_Sea_Liar", part=Eyes, lent_by=ABYSS, keys=( "sea", "lie" ), phrase=( "eyes that turn the colour of the sea whenever you lie", "eyes that flood sea-green at even the smallest lie", "eyes that turn the colour of a rough sea at every lie, even the kind ones" ),
				text=(
						"Your eyes go the colour of the sea whenever you lie, so you have learned not to",
						"Every lie you tell turns your eyes sea-green, which has made you famously honest",
						"Your eyes are a dull grey, until you lie and they flood with the colour of the sea",
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
		Make_Mark( "Scent_Incense", part=Scent, lent_by=HADES, keys=( "incense", "temple" ), phrase=( "incense", "frankincense in an empty shrine", "incense on cool marble" ), omen=( "a funeral", "a prayer said too late", "a priest come to the wrong house" ),
				text=(
						"A breath of incense follows you, as if you had just left a temple nobody remembers",
						"You smell faintly of incense, the kind burned for the dead",
						"Incense clings to your clothes, though you have not set foot in a temple in years",
						) ),
		Make_Mark( "Scent_Myrrh", part=Scent, lent_by=HADES, keys=( "myrrh", ), phrase=( "myrrh", "myrrh and dry linen", "myrrh in a sealed reliquary" ), omen=( "a tomb", "an embalmer's workshop", "a saint nobody prays to any more" ),
				text=(
						"Myrrh clings to you, sweet and ancient, like the inside of a reliquary",
						"There is myrrh in your hair, though you have never bought any",
						"You smell faintly of myrrh, like a reliquary opened for the first time in a century",
						) ),
		Make_Mark( "Scent_Rain", part=Scent, lent_by=HADES, keys=( "rain", ), phrase=( "rain on stone", "rain on a slate roof", "the first rain after a drought" ), omen=( "an open grave", "a churchyard in autumn", "a mourner caught without a cloak" ),
				text=(
						"The smell of rain lingers in you, like a persistent memory",
						"You smell of rain on stone, even under a cloudless sky",
						"Rain follows you, or at least its smell does, even in the driest town",
						) ),
		Make_Mark( "Scent_Turned_Earth", part=Scent, lent_by=HADES, keys=( "earth", "grave" ), phrase=( "turned earth", "turned earth and cut roots", "damp soil under a spade" ), omen=( "a fresh grave", "a sexton at the end of a long day", "a garden planted for the dead" ),
				text=(
						"You smell of freshly turned earth, the way a garden does, or a grave",
						"Wherever you sleep, the room smells of turned earth by morning",
						"You smell of turned earth, like a field the morning after the plough",
						) ),
		Make_Mark( "Scent_Cold_Wax", part=Scent, lent_by=HADES, keys=( "wax", "chapel" ), phrase=( "cold wax", "cold wax and dusty pews", "wax gone cold on a stone floor" ), omen=( "a vigil", "an empty chapel at dusk", "a prayer that went unanswered" ),
				text=(
						"You smell of cold candle wax and old chapels",
						"A scent of cold wax clings to you, like a chapel after the last prayer",
						"Cold wax and old prayers are what you smell like, and nobody knows why",
						) ),
		Make_Mark( "Scent_Lilies", part=Scent, lent_by=HADES, keys=( "lilies", ), phrase=( "lilies", "lilies in a cool room", "lilies and wet stems" ), omen=( "a deathbed", "a wreath on the wrong door", "a bride who never came home" ),
				text=(
						"You smell of lilies, the kind people bring when it is already too late",
						"A scent of white lilies follows you, heavy and sweet and a little sad",
						"Lilies, always lilies, as if someone had just left flowers for you",
						) ),
		Make_Mark( "Scent_Sulfur", part=Scent, lent_by=HELLS, keys=( "sulfur", "match" ), phrase=( "sulfur", "sulfur and struck flint", "a match just struck" ), omen=( "a curse being spoken", "a bargain sealed in a hurry", "a contract you should not have signed" ),
				text=(
						"A trace of sulfur follows you, like a struck match that never quite goes out",
						"Every room you enter smells, briefly, of sulfur",
						"A whiff of sulfur follows you around corners, never quite gone",
						) ),
		Make_Mark( "Scent_Campfire", part=Scent, lent_by=HELLS, keys=( "campfire", "smoke" ), phrase=( "old smoke", "woodsmoke and wet cinders", "a campfire drowned at dawn" ), omen=( "a burned house", "a camp abandoned in a hurry", "a village after the soldiers left" ),
				text=(
						"You smell like a campfire just put out, warm and a little dangerous",
						"Smoke from a fire long since doused still clings to you",
						"You smell of a campfire on a cold night, smoke and warmth together",
						) ),
		Make_Mark( "Scent_Forge", part=Scent, lent_by=HELLS, keys=( "iron", "forge" ), phrase=( "hot iron", "hot iron and quenching water", "iron fresh from the anvil" ), omen=( "a branding", "a sword with your name on it", "a smith working through the night" ),
				text=(
						"You carry the smell of hot iron, like a forge at the end of the day",
						"Close to you, the air smells of iron fresh from the forge",
						"You smell of the forge, iron and coal and long days",
						) ),
		Make_Mark( "Scent_Snuffed_Candle", part=Scent, lent_by=HELLS, keys=( "candle", "smoke" ), phrase=( "snuffed candles", "a candle pinched out", "wick smoke in a quiet room" ), omen=( "a wake", "a party that ended early", "a room someone has just died in" ),
				text=(
						"You smell of a snuffed candle, that thin smoke that means someone has just left",
						"The smell of a candle just blown out follows you from room to room",
						"Wherever you have been, the air smells as if someone had just blown out the last candle",
						) ),
		Make_Mark( "Scent_Cinnamon_Ash", part=Scent, lent_by=HELLS, keys=( "cinnamon", "ash" ), phrase=( "cinnamon and ash", "cinnamon and cooling ash", "clove, cinnamon and ash" ), omen=( "a market after a fire", "a bakery that burned with the bread inside", "a spice caravan that never arrived" ),
				text=(
						"You smell of cinnamon and ash, like a spice market after a fire",
						"There is cinnamon on you, and under it, always, a little ash",
						"Cinnamon and ash cling to you, sweet and scorched at once",
						) ),
		Make_Mark( "Scent_Burnt_Sugar", part=Scent, lent_by=HELLS, keys=( "sugar", ), phrase=( "burnt sugar", "caramel left too long in the pan", "toffee in a scorched pan" ), omen=( "a fire in a sweetshop", "a confectioner's last mistake", "a birthday that ended in tears" ),
				text=(
						"You smell of burnt sugar, sweet and scorched, like a fairground after closing",
						"There is a smell of caramel left too long on the fire about you",
						"Burnt sugar clings to you, the smell of a treat that went a little wrong",
						) ),
		Make_Mark( "Scent_Wine", part=Scent, lent_by=ABYSS, keys=( "wine", ), phrase=( "freshly opened wine", "wine just uncorked", "a cask newly broached" ), omen=( "a feast gone wrong", "a wedding nobody survived", "a toast to the wrong king" ),
				text=(
						"You smell of freshly opened wine, even in clean, fine clothes",
						"A scent of wine just uncorked follows you, rich and a little too sweet",
						"You smell of red wine, poured too generously",
						) ),
		Make_Mark( "Scent_Storm", part=Scent, lent_by=ABYSS, keys=( "storm", "lightning" ), phrase=( "lightning", "air split by lightning", "the wind before a storm" ), omen=( "a storm about to break", "a tower about to be struck", "a quarrel about to start" ),
				text=(
						"The air around you smells the way it does before a storm",
						"You smell of the air before lightning, sharp and restless",
						"You smell of rain about to fall, sharp with lightning",
						) ),
		Make_Mark( "Scent_Brine", part=Scent, lent_by=ABYSS, keys=( "brine", "sea" ), phrase=( "brine", "brine and wet rope", "salt spray and kelp" ), omen=( "a drowned sailor", "a shipwreck nobody reported", "a widow waiting on the pier" ),
				text=(
						"You smell of brine, as if you had just walked out of the sea",
						"Salt and brine cling to you, however far you are from any coast",
						"You smell of the sea, salt and kelp and somewhere far away",
						) ),
		Make_Mark( "Scent_Overripe", part=Scent, lent_by=ABYSS, keys=( "sweet", "fruit" ), phrase=( "overripe fruit", "fruit gone soft in the sun", "sweet figs split open" ), omen=( "rot dressed up as sweetness", "a banquet left out too long", "an orchard nobody harvested" ),
				text=(
						"A sweetness of overripe fruit hangs about you, pleasant for a moment too long",
						"You smell of flowers left too long in the vase, sweet on the edge of turning",
						"You smell of fruit a day past ripe, sweet enough to be dangerous",
						) ),
		Make_Mark( "Scent_Absinthe", part=Scent, lent_by=ABYSS, keys=( "absinthe", "mint" ), phrase=( "absinthe and wild mint", "absinthe and crushed mint", "wormwood and anise" ), omen=( "a night nobody remembers", "a fever dream", "a poet's last good idea" ),
				text=(
						"You smell of absinthe and wild mint, green and dizzying",
						"A green, dizzying scent of absinthe follows you from one bad decision to the next",
						"There is absinthe on your breath and your clothes, though you swear you only had one",
						) ),
		Make_Mark( "Scent_Patchouli_Smoke", part=Scent, lent_by=ABYSS, keys=( "patchouli", "smoke" ), phrase=( "patchouli and cheap smoke", "patchouli and pipe smoke", "patchouli and smoke in a cellar" ), omen=( "a den of thieves", "a card game that ended in knives", "a gambling den after a raid" ),
				text=(
						"You smell of patchouli and cheap smoke, like the back room of a tavern nobody admits to",
						"Patchouli and pipe smoke follow you, the smell of every party worth leaving early",
						"You carry a haze of patchouli and smoke, and the guards always sniff twice",
						) ),
		)


# ---------------------------------------------------------------------------
# Tails: only the Nine Hells lend one.  A structure that says the tail is
# never drawn for a blood that has none (``Fiendish_Aspect``).
# ---------------------------------------------------------------------------

TAILS = (
		Make_Mark( "Tail_Arrow", part=Tail, lent_by=HELLS, keys=( "arrow", "tips" ),
				text=(
						"A long tail sways behind you, ending in an arrow-shaped tip",
						"Behind you, a long tail ends in a tip shaped like an arrowhead",
						"You keep your tail wound under your coat, but it lashes when you are angry, and then everyone knows",
						"Your tail ends in a neat arrowhead, and you have tied a ribbon just above it",
						) ),
		Make_Mark( "Tail_Lash", part=Tail, lent_by=HELLS, keys=( "arrow", "barb", "tips" ),
				text=(
						"A thin tail lashes behind you when you are angry, its tip barbed like an arrow",
						"You have learned to sit with your back to the wall, so nobody steps on the tail, or stares at it",
						"Your thin tail is barbed at the tip, and it knocks things off tables when you are nervous",
						) ),
		Make_Mark( "Tail_Curl", part=Tail, lent_by=HELLS, keys=( "curl", ),
				text=(
						"Your tail curls around your ankle when you stand still, like a cat's",
						"You have a long, restless tail that gives away every feeling you would rather keep",
						"Your tail flicks when you are amused, and it has ruined more than one straight face",
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
						"You could pass, on a dark day, but lately you have stopped wanting to",
						"You learned how to pass for human, and then you learned you did not have to",
						"You have passed for human in a hundred doorways, and not once has it felt like coming home",
						"You have quit passing for human, and the people who stayed are the ones worth keeping",
						) ),
		Make_Mark( "Bearing_Hood", part=Bearing, lent_by=HADES, keys=( "hood", ),
				text=(
						"You still own a deep hood, and you wear it only when it rains",
						"Your hood stays down these days, and the world has had to get used to it",
						"You have come to keep the hood for the weather and give the rest of you to the sun",
						"Your hood has become a pillow, a satchel and a blanket, everything but a refuge",
						) ),
		Make_Mark( "Bearing_Stillness", part=Bearing, lent_by=HADES, keys=( "still", ),
				text=(
						"You have a stillness people mistake for menace, until you smile",
						"Graveyards never frightened you, and these days neither do crowds",
						"Your stillness has unnerved more bullies than any blade ever could",
						"You have learned to wait out trouble the way a tomb waits out the seasons",
						) ),
		Make_Mark( "Bearing_Deep_Hoods", part=Bearing, lent_by=HADES, keys=( "hoods", ),
				text=(
						"You own more hoods than shirts, and every one of them is deep",
						"You keep your hood up in every town, and still the dogs bark",
						"You have worn your hoods so long that your own face has come to surprise you in puddles",
						"You have taken to sewing your own hoods, deep and dark and lined with something soft",
						) ),
		Make_Mark( "Bearing_Gentle", part=Bearing, lent_by=HADES, keys=( "gentle", ),
				text=(
						"Animals trust you before people do, and you have come to prefer it that way",
						"You are kinder than you look, and you have stopped waiting for anyone to notice",
						"You have found a way with the dying, and not one of them has been afraid of you",
						"You have taken in every stray that follows you home, and a few people besides",
						) ),
		Make_Mark( "Bearing_Funerals", part=Bearing, lent_by=HADES, keys=( "funeral", ),
				text=(
						"You wear your horns to every funeral, wedding and brawl, and this year you have been to all three",
						"You have stood at more funerals than weddings, and the mourners have come to find you a comfort",
						"You have danced at a funeral or two, and nobody who loved the dead has complained",
						"You have become the one people send for when someone dies, because grief has never frightened you",
						) ),
		Make_Mark( "Bearing_No_Hiding", part=Bearing, lent_by=ABYSS, keys=( "hide", ),
				text=(
						"No hood was ever deep enough to hide you, so you threw the last one in a river",
						"There was never any hiding what you are, so you stopped trying and started enjoying it",
						"You have tried every way to hide there is, and none of them suited you half as well as being seen",
						"You have hidden in cellars, haylofts and other people's stories, and you are done with all of them",
						) ),
		Make_Mark( "Bearing_Watched", part=Bearing, lent_by=ABYSS, keys=( "watch", ),
				text=(
						"Shopkeepers still count their wares twice when you walk in, and you have learned to wink at them",
						"Someone is always watching you, so you give them something worth watching",
						"You have been watched in every market from here to the coast, and you have learned to give a little bow",
						"You have learned to feel someone watching you the way other people feel the cold coming",
						) ),
		Make_Mark( "Bearing_Loud", part=Bearing, lent_by=ABYSS, keys=( "loud", ),
				text=(
						"You dress louder than anyone else in the room, and somehow it suits you",
						"You have never once blended in, and you have stopped pretending you want to",
						"You have taken to wearing every colour at once, as if you were not bright enough already",
						"You have been asked to leave every quiet room you ever walked into, and you have left each one louder than you found it",
						) ),
		Make_Mark( "Bearing_Marked", part=Bearing, lent_by=ABYSS, keys=( "gates", ),
				text=(
						"Someone is always watching your hands, wherever you go",
						"There is no hiding what you are, and every town lets you know it before the gates",
						"You have been searched at every gate between here and the mountains, and you have learned to whistle through it",
						"You have had your name written in more town ledgers than you can remember, always under the same heading",
						) ),
		Make_Mark( "Bearing_Laugh", part=Bearing, lent_by=ABYSS, keys=( "laugh", ),
				text=(
						"You laugh easily for all the stares, and it is the laugh people remember",
						"You have learned to laugh first, before anyone else can, and to make them laugh with you",
						"Your laugh has become the one thing about you that nobody thinks to fear",
						"You have laughed your way through hunger, heartbreak and three jails, and you are not finished laughing",
						) ),
		Make_Mark( "Bearing_Painted", part=Bearing, lent_by=ABYSS, keys=( "paint", ),
				text=(
						"You paint your horns on feast days, because if they are going to stare, they might as well enjoy it",
						"You have painted your horns a new colour for every town, so no two places remember you the same",
						"You have let the children at every inn paint your horns, and you wear their stars and flowers for weeks",
						"You have painted your horns the colour of your skin, hoping they would vanish, and they never quite have",
						) ),
		Make_Mark( "Bearing_Unapologetic", part=Bearing, lent_by=HELLS, keys=( "apology", ),
				text=(
						"You stopped apologising for your horns years ago, and the world has had to adjust",
						"You learned early that apologising changes nothing, so you learned to sing instead",
						"You have heard every apology the world expects from you, and you have offered none of them",
						"You have made no apology for your face or your name, and you do not intend to start",
						) ),
		Make_Mark( "Bearing_Temper", part=Bearing, lent_by=HELLS, keys=( "temper", ),
				text=(
						"You have a temper, and you have learned to point it at the right people",
						"You carry yourself like someone who has already survived the worst of it",
						"You have learned to bank your temper like a hearth fire, low and patient and ready",
						"Your temper has cost you friends, homes and one very good job, and you are learning, slowly",
						) ),
		Make_Mark( "Bearing_Careful", part=Bearing, lent_by=HELLS, keys=( "careful", ),
				text=(
						"You keep your hands where people can see them, and that has saved your life more than once",
						"You speak softly and move slowly, because the alternative has cost you before",
						"You have learned to move through a room like someone counting the exits, and you always know how many there are",
						"You have taken to keeping your boots polished and your debts paid, so that nobody can ever find a reason",
						) ),
		Make_Mark( "Bearing_Warm", part=Bearing, lent_by=HELLS, keys=( "warm", ),
				text=(
						"You run warm, and on cold nights your friends find excuses to sit beside you",
						"You have warmed more cold hands than you can count, and never asked why they reached for you",
						"You have learned that your warmth frightens people in summer and draws them near in winter",
						"You have become the warmest thing in every winter camp, and the children have noticed",
						) ),
		Make_Mark( "Bearing_Singer", part=Bearing, lent_by=HELLS, keys=( "sing", ),
				text=(
						"You learned to sing in taverns that would not serve you, and now they ask you back",
						"You have sung your way out of more trouble than you ever fought your way out of",
						"You have learned the hymns that call your kind wicked, and you sing them better than the choir",
						"You have sung yourself through every lonely winter, and the songs have kept you company",
						) ),
		Make_Mark( "Bearing_Soft_Spoken", part=Bearing, lent_by=HELLS, keys=( "voice", ),
				text=(
						"You speak softly, and somehow every room goes quiet to listen",
						"You keep your voice low and your chin high, and both have served you well",
						"You have learned that a low voice carries further than a shout, and you have never needed to raise yours",
						"Your voice has become the one people ask for when a child cannot sleep",
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
