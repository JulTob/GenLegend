import time
from collections import defaultdict, Counter
from Minion import guardian, watcher, warden, spy, minion, changeling, report_bug, print_record, CHANGELING_MINION, CHANGELING_COLOR

try:
	import AtlasAlusoris.Map_of_NPC as NPC
	from AtlasLudus.Map_of_Dice import Dice
	from AtlasNomina.Map_of_Word_Entropy import entropify, reduce_entropy, increase_entropy, to_mean_entropy
	from AtlasNomina.Map_of_Markov import MarkovNameGenerator
	from AtlasLudus.Map_of_Useful_Functions import select1
except ImportError:
	raise

MAX_ATTEMPTS = 3
MAX_DEPTH = 1

# How many goes each naming method gets before NewWord moves to the next one.
# Its own constant on purpose: how many times to *repeat a method* is a
# different decision from how many attempts a method makes internally, and they
# should be tunable apart. Setting this to 1 restores the pre-ladder behaviour
# exactly, dice for dice, for anyone who needs old seeds to name old characters.
METHOD_ATTEMPTS = 3

LAST_RESORT_NAMES = (
	"Ada", "Bran", "Cora", "Dain", "Edda", "Fenn", "Gale", "Hale",
	"Ida", "Jarl", "Kesh", "Lorn", "Mira", "Nell", "Orin", "Pell",
	"Quill", "Rook", "Sela", "Tarn", "Vale", "Wren", "Yara", "Zeph",
	)

LAST_RESORT_SURNAMES = (
	"Ashdown", "Blackwater", "Coldiron", "Dunmore", "Eastmarch",
	"Fairholm", "Greystone", "Hallow", "Ironvale", "Keelson",
	"Longbarrow", "Marchwood", "Northgate", "Oakhand", "Pinefall",
	"Redhill", "Stormcrow", "Thornbury", "Underhill", "Westwind",
	)


# Restored 2026-08-30: Race_Ingredient and its ladder were called from
# NewName but defined nowhere, so every Character raised NameError and fell
# through to the last-resort roster. Recovered as real source from the
# parallel recovery branch, which had kept it rather than shimming it.
# Onset, nucleus and coda: enough to build a syllable out of nothing.
LAST_RESORT_PHONOTACTIC = (
	("b", "br", "d", "dr", "f", "g", "gr", "h", "k", "kr",
		"l", "m", "n", "p", "r", "s", "st", "t", "th", "v"),
	("a", "e", "i", "o", "u", "ae", "ea", "io", "ua", "ar",
		"or", "en", "in"),
	("n", "r", "l", "s", "th", "nd", "rn", "ll", "ss", "k", "m", "d"),
	)

# The four functions every race module is expected to offer, and what answers
# for each one when no module can. Adding a fifth ingredient means adding it
# here: that is the whole registration, and the ladder covers it from then on.
LAST_RESORT_INGREDIENT = {
	"Names":          LAST_RESORT_NAMES,
	"Surnames":       LAST_RESORT_SURNAMES,
	"Phonotactic":    LAST_RESORT_PHONOTACTIC,
	"Surphonotactic": LAST_RESORT_PHONOTACTIC,
	}

NAMING_INGREDIENTS = tuple(LAST_RESORT_INGREDIENT)


def _rung_name(
		source,
		):
	"""How a rung of the ladder is called in the log."""
	return getattr(
		source,
		"__name__",
		str(source),
		).split(".")[-1]


def _report_demotion(
		source,
		ingredient,
		reason,
		heir,
		):
	"""One line saying who could not answer, why, and who is being asked next."""
	print_record(
		f"{CHANGELING_MINION}: {time.strftime('%Y-%m-%d %H:%M:%S')} [naming] "
		f"{_rung_name(source)}.{ingredient} {reason}; "
		f"{heir} takes over.",
		CHANGELING_COLOR,
		)


def _plantilla():
	"""Rung two, imported late so a broken race module cannot take it down too."""
	try:
		from AtlasNomina.Races import plantilla
		return plantilla
	except Exception as exc:
		report_bug(
			exc
			)
		return None


def Race_Ingredient(
		race,
		ingredient,
		genus,
		):
	"""
	Ask a race module for one of its four naming ingredients, and keep asking
	downwards until something answers.

	A missing function and a bug inside a present one are the same event here:
	both mean this module cannot supply this ingredient for this genus, and both
	are reported before the demotion. The bottom rung is a constant, so this
	function has no failing path and its callers need no fallback of their own.
	"""
	ladder = [race, _plantilla()]
	for rung, source in enumerate(ladder):
		if source is None:
			continue
		heir = (
			_rung_name(ladder[rung + 1])
			if rung + 1 < len(ladder) and ladder[rung + 1] is not None
			else "the last-resort roster"
			)
		provider = getattr(
			source,
			ingredient,
			None,
			)
		if provider is None:
			_report_demotion(source, ingredient, "is not defined", heir)
			continue
		try:
			answer = provider(genus)
		except Exception as exc:
			report_bug(
				exc
				)
			_report_demotion(
				source,
				ingredient,
				f"raised {type(exc).__name__}",
				heir,
				)
			continue
		if answer:
			return answer
		_report_demotion(source, ingredient, "came back empty", heir)
	return LAST_RESORT_INGREDIENT[ingredient]


def _steady_pick(
		lusor,
		roster,
		offset=0,
		):
	"""Pick from a roster without needing the Character's full naming path."""
	try:
		return lusor.Pick(
			roster,
			dice=lusor.Dice_Bag(
				"Nomina.LastResort",
				version="1",
				),
			)
	except Exception as exc:
		report_bug(
			exc
			)
		from zlib import crc32

		identity = str(
			getattr(
				lusor,
				"seed",
				"",
				)
			or getattr(
				lusor,
				"race",
				"",
				)
			or id(
				lusor
				)
			).encode(
				"utf-8"
				)
		return roster[
			(crc32(
				identity
				) + offset) % len(
					roster
					)
			]


def LastResortGivenName(
		lusor,
		i=0,
		):
	"""Rung three for a given name: roster only."""
	return _steady_pick(
		lusor,
		LAST_RESORT_NAMES,
		)


def LastResortFamilyName(
		lusor,
		i=0,
		):
	"""Rung three for a family name."""
	return _steady_pick(
		lusor,
		LAST_RESORT_SURNAMES,
		offset=7,
		)


def LastResortName(
		lusor,
		):
	"""Rung three for a whole name. Nothing here can raise."""
	return (
		f"{LastResortGivenName(lusor)} {LastResortFamilyName(lusor)}"
		)


def LastResortWord(
		character,
		names=None,
		prefix=None,
		fix=None,
		suffix=None,
		depth=0,
		*,
		dice=None,
		):
	"""NewWord's stand-in, carrying NewWord's signature."""
	return _steady_pick(
		character,
		LAST_RESORT_NAMES,
		)


@changeling(LastResortWord)
def NewWord(
		names,
		prefix,
		fix,
		suffix,
		depth=0,
		*,
		dice,
		):
	'''
	Generates a new word based on the lists in a Lexicon object
	It uses different methods selected at random:
	- From the premade lists, concatenate a random selection of prefix-fix-suffix
	- Extraction of syllables from the Names list and generating by syllables
		- Weighted syllables
	- Markov Generator: Weighted Random Probability for the next letter
	- Remixing leters of a name to generate a new name.
	- Choosing a name directly from the lexicon.

	``dice`` is the Dice Bag of the name under construction, ``identity.name``,
	opened once in NewName: the order of the strategies and every draw inside
	them come from it, so no step reaches the shared generator (ruling 8).
	'''

	strategies = [
		#"EntropyUp",
		"Entropify",
		"EntropyDown",
		"Mutate",
		#"Extraction",
		#"Mix",
		"Markov",
		# "PhonotacticWeighted", ### Commented out: Errors
		"Syllabic",
		"Choose",
		# "EchoMorphology", ### Commented out: Feels weird
		]
	if depth > MAX_DEPTH:
		return dice.choice(names)

	choices = strategies[:]
	dice.shuffle(choices)
	HEAVY = {"Markov", "PhonotacticWeighted", "WeightExtraction"}
	for strategy in choices:
		try:
			if strategy == "EntropyUp":
				name = dice.choice(names)
				newName = mutate_entropy(name, increase_entropy, names, dice=dice)
				if is_valid_name(newName, strategy): return newName
				else: return name
			elif strategy == "EntropyDown":
				name = dice.choice(names) # NewWord(names, prefix, fix, suffix, depth)
				newName = mutate_entropy(name, reduce_entropy, names, dice=dice)
				if is_valid_name(newName, strategy): return newName
				else: return name
			elif strategy == "Entropify":
				name = dice.choice(names)# NewWord(names, prefix, fix, suffix, depth)
				newName = mutate_entropy(name, to_mean_entropy, names, dice=dice)
				if is_valid_name(newName, strategy): return newName
				else: return name
			elif strategy == "Mutate":
				name = dice.choice(names)
				newName1 = mutate_entropy(name, increase_entropy, names, dice=dice)
				newName2 = mutate_entropy(newName1, reduce_entropy, names, dice=dice)
				newName3 = mutate_entropy(newName2, to_mean_entropy, names, dice=dice)
				if is_valid_name(newName3, strategy): return newName3
				elif is_valid_name(newName2, strategy): return newName2
				elif is_valid_name(newName1, strategy): return newName1
				else: return name
			elif strategy == "Extraction":
				for _ in range(MAX_ATTEMPTS):
					name = SyllabicComposition(names, min_syllables=2, max_syllables=6, dice=dice)
					if name and is_valid_name(name, strategy):
						name_ent = entropify(name, names, dice=dice)
						if name_ent and is_valid_name(name, strategy):
							name = name_ent
						return name
			elif strategy == "Mix":
				name = Mixer(names, prefix, fix, suffix, depth + 1, dice=dice)
				name_b = name
				if name and is_valid_name(name, strategy):
					return name
			elif strategy == "EchoMorphology":
				name = dice.choice(names) # NewWord(names, prefix, fix, suffix, depth + 1)
				for i in range(MAX_ATTEMPTS):
					name = EchoMorphology(name, dice=dice)
					if name and is_valid_name(name, strategy):
						pass
					name = entropify(name, names, dice=dice)
					if name and is_valid_name(name, strategy):
						return name
				return dice.choice(names) # NewWord(names, prefix, fix, suffix, depth + 1)
			elif strategy == "Syllabic":
				name = Syllabic(prefix, fix, suffix, dice=dice)
				if name:
					return name
			elif strategy == "Choose":
				name = dice.choice(names)
				return name
			elif strategy == "Markov":
					markov = MarkovNameGenerator(names, dice=dice)
					for _ in range(MAX_ATTEMPTS):
						name = markov.generate_name()
						if name and is_valid_name(name, strategy):
							return name
			elif strategy == "PhonotacticWeighted":
					phonotactics = ExtractWeightedPhonotacticElements(names)
					for i in range(MAX_ATTEMPTS):
						name = GenerateFromWeightedPhonotactics(phonotactics, dice=dice)
						if name and is_valid_name(name, strategy):
							return name
			else:
				name = dice.choice(names)
				return name

		except Exception:
			return dice.choice(names)
	return dice.choice(names)

def EchoMorphology(
		base_name,
		*,
		dice,
		):
	pattern = []
	for c in base_name.lower():
		if c in 'aei':
			pattern.append('A')
		if c in 'ou':
			pattern.append('O')
		if c in 'bdptfvwr':
			pattern.append('B')
		if c in 'ckqsxz':
			pattern.append('C')
		if c in 'ghjy':
			pattern.append('G')
		if c in 'lmn':
			pattern.append('M')
		else:
			pattern.append('X')
	name = ''
	for p in pattern:
		if p == 'A':
			name += dice.choice('aei')
		if p == 'O':
			name += dice.choice('ou')
		if p == 'B':
			name += dice.choice('bdptv')
		if p == 'C':
			name += dice.choice('csx')
		if p == 'G':
			name += dice.choice('gjy')
		if p == 'M':
			name += dice.choice('lmn')
	return name.capitalize()

def ExtractWeightedPhonotacticElements(name_list):
	from collections import Counter

	prefix_counts = Counter()
	fix_counts = Counter()
	suffix_counts = Counter()

	for name in name_list:
		name = name.lower()
		if len(name) < 3: continue

		prefix = name[:2]
		fix = name[1:3]
		suffix = name[-2:]

		prefix_counts[prefix] += 1
		fix_counts[fix] += 1
		suffix_counts[suffix] += 1

	return {
		'prefix': list(prefix_counts.keys()),
		'prefix_weights': list(prefix_counts.values()),
		'fix': list(fix_counts.keys()),
		'fix_weights': list(fix_counts.values()),
		'suffix': list(suffix_counts.keys()),
		'suffix_weights': list(suffix_counts.values()),
	}

def GenerateFromWeightedPhonotactics(
		phonotactics,
		syllable_count=2,
		*,
		dice,
		):
	name = ''
	for _ in range(syllable_count):
		o = dice.choices(phonotactics['prefix'], weights=phonotactics['prefix_weights'])[0]
		n = dice.choices(phonotactics['fix'], weights=phonotactics['fix_weights'])[0]
		c = dice.choices(phonotactics['suffix'], weights=phonotactics['suffix_weights'])[0]
		name += o + n[-1] + c[-1]  # basic syllable smoothing
	return name.capitalize()

def first_valid(
		strategy_fns,
		validator,
		fallback_names,
		retries=2,
		timeout=2.0,
		*,
		dice,
		):
	"""
	Run strategy_fns (list of callables) in parallel with timeout.
	Return the first valid result or fallback to a name from fallback_names.
	"""
	for attempt in range(retries):
		stop = Event()

		def task(fn):
			try:
				if stop.is_set():
					return None
				result = fn()
				if result and validator(result):
					stop.set()
					return result
			except Exception as exc:
				# Was ``raise e``, which crossed the thread boundary and came
				# back out of fut.result(), so one broken strategy failed the
				# whole heat instead of losing it.
				report_bug(exc)
			return None

		with ThreadPoolExecutor() as ex:
			futures = [ex.submit(task, fn) for fn in strategy_fns]
			try:
				done, _ = wait(futures, timeout=timeout, return_when=FIRST_COMPLETED)
			except TimeoutError:
				continue

			for fut in done:
				result = fut.result()
				if result:
					return result


	# All attempts failed or timed out; fallback to predefined list
	fallback_name = dice.choice(fallback_names)
	return fallback_name

def LoadRace(trait):
	"""
	Dynamically imports the appropriate race module based on the genus.
	The imported module for the race, or a fallback module if not found.
	"""
	race_module_map = {
		"Aberration": 	"AtlasNomina.Races.Aberration",
		"Aven" : 		"AtlasNomina.Races.Aven",
		"Beast": 		"AtlasNomina.Races.Beast",
		"Beastfolk": 	"AtlasNomina.Races.Beastfolk",
		"Catfolk": 		"AtlasNomina.Races.Catfolk",
		"Celestial" : 	"AtlasNomina.Races.Celestial",
		"Construct" : 	"AtlasNomina.Races.Construct",
		"Dragon"    : 	"AtlasNomina.Races.Dragon",
		"Dwarf"		: 	"AtlasNomina.Races.Dwarf",
		"Elemental" : 	"AtlasNomina.Races.Elemental",
		"Elf"    : 		"AtlasNomina.Races.Elf",
		"Fey"    : 		"AtlasNomina.Races.Fey",
		"Fiend"    : 	"AtlasNomina.Races.Fiend",
		"Giant"    : 	"AtlasNomina.Races.Giant",
		"Gnome"    : 	"AtlasNomina.Races.Gnome",
		"Goblin" : 		"AtlasNomina.Races.Goblin",
		"Halfling"    : "AtlasNomina.Races.Halfling",
		"Human"    : 	"AtlasNomina.Races.Human",
		"Kobold"    : 	"AtlasNomina.Races.Kobold",
		"Lizardfolk" : 	"AtlasNomina.Races.Lizardfolk",
		"Monstrosity" : "AtlasNomina.Races.Monstrosity",
		"Ooze" : 		"AtlasNomina.Races.Ooze",
		"Orc" : 		"AtlasNomina.Races.Orc",
		"Plant" : 		"AtlasNomina.Races.Plant",
		"Snakefolk" : 	"AtlasNomina.Races.Snakefolk",
		"Undead": 		"AtlasNomina.Races.Undead",
		"Vampire": 		"AtlasNomina.Races.Vampire",
		}
	import importlib
	module_path = race_module_map.get(trait)
	if module_path is None:
		# Not an error: plenty of genera have no module of their own and the
		# template is the right answer for them. Nothing to report.
		return _plantilla()
	try:
		return importlib.import_module(module_path)
	except Exception as exc:
		# A race module that will not even import is a real defect, and used to
		# be indistinguishable from the line above: the sheet quietly filled
		# with template names and nobody was told which module was down.
		report_bug(exc)
		_report_demotion(
			module_path,
			"the module",
			f"would not import ({type(exc).__name__})",
			"plantilla",
			)
		return _plantilla()

NAME_PURPOSE = "identity.name"
	#-- The one Dice Bag a name is drawn from, as Epica.Title is for the title:
	#-- the name is one choice of the Character with several steps.


def Naming_Dice(
		lusor,
		):
	"""
	The Dice Bag every draw of this lusor's name comes from.

	A Character opens its own bag on ``identity.name`` (ruling 8, QST-0144.6)
	and NewName hands it down the whole ladder as ``dice``: the order of the
	strategies, the base names, the Markov walk, the entropy swaps, the
	syllables and the full-name format all draw from it in turn.

	A lusor that is not a Character is the legacy NonPlayer of Decree 0004,
	not ported yet. It brings no Dice Bag and seeds ``app.random`` on its own
	seed before asking for a name, so it keeps drawing from that stream,
	deterministic per seed as before, until its own port.
	"""
	from AtlasActorLudi.CharactersKit import Character

	if isinstance(
			lusor,
			Character,
			):
		return lusor.Dice_Bag(
			NAME_PURPOSE,
			)

	import app.random as legacy_shared_stream
		#-- Imported here, not at the top: the integrator deletes app/random.py
		#-- once no summon reaches it, and this branch leaves with the NonPlayer port.

	return legacy_shared_stream


@changeling(LastResortName)
def NewName(lusor):
	"""
	Generate a full name for the given lusor (character).

	Was @guardian. The dice here come from a Bag opened on the seed, so every
	retry drew the same numbers and met the same wall: a hundred attempts at a
	failure that never had a second outcome. A Changeling steps aside to
	LastResortName instead, and the sheet gets a name either way.

	One Dice Bag, ``identity.name``, is opened here and handed down as ``dice``
	to every word and every strategy. It replaces a reseed of the global
	generator on the lusor's seed, which made every draw of the name depend
	on its place in the order of the draws (QST-0144.6).
	"""
	import AtlasNomina.Races.plantilla as fallback

	genus = lusor.genus
	dice = Naming_Dice(
		lusor,
		)

	race = LoadRace(lusor.race)

	# Four ingredients, one ladder each. These used to catch AttributeError
	# only, which covered a race module that never defined the function and let
	# every bug *inside* a defined one straight through: that is how a stray
	# ``Names +=`` in Elf.Phonotactic became a hundred retries and a ceiling
	# message instead of one reported UnboundLocalError and a generic elf.
	names = Race_Ingredient(race, "Names", genus)
	surnames = Race_Ingredient(race, "Surnames", genus)
	o, n, c = Race_Ingredient(race, "Phonotactic", genus)
	os, ns, cs = Race_Ingredient(race, "Surphonotactic", genus)


	# Define genus-based flags
	MONSTER =         "Monstrosity"    in genus
	CELESTIAL =     "Celestial"        in genus
	BEAST =         ("Beast" in genus) and not("folk" in genus)
	if  "Giant"        in genus:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		surname = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		FullName =  f"{name} {surname}son"
	elif "Elemental"    in genus:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		surname = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		FullName = f"{name} {surname}"
	elif BEAST or MONSTER:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		FullName = name
	elif "Construct"     in genus:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		surname = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		FullName = select1(
			[
				f"{name}-{surname}",
				f"{name} {surname}",
				f"{name}:{surname}",
				f"{name}_{surname}",
				],
			dice=dice,
			)
	elif "Dwarf"         in genus:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		name2 = NewWord(names, o, n, c, dice=dice).capitalize()
		surname = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		surname2 = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		FullName = select1(
			[
				f"{name} {name2} {surname} {surname2}",
				],
			dice=dice,
			)
	elif "Gnome"         in genus:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		name2 = NewWord(names, o, n, c, dice=dice).capitalize()
		name3 = NewWord(names, o, n, c, dice=dice).capitalize()
		surname = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		FullName =  f"{name} {name2} {name3} {surname}"
	elif "Vampire"         in genus:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		surname = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		FullName = f"{name} {surname}"
	else:
		name = NewWord(names, o, n, c, dice=dice).capitalize()
		surname = NewWord(surnames, os, ns, cs, dice=dice).capitalize()
		FullName = f"{name} {surname}"

	if "Noble"         in genus:
		if lusor.gender.title() == "He":
			FullName = f"Lord {FullName}"
		if lusor.gender.title() == "She":
			FullName = f"Lady {FullName}"
		if lusor.gender.title() == "They":
			FullName = f"Noble {FullName}"

	lusor._name = name
	return FullName.title()

# The four ingredient readers below are @guardian no longer. Every one of them
# reads a seeded generator, so a retry replays the same dice into the same wall;
# and every one of them now goes through Race_Ingredient, which has no failing
# path of its own. The safeguard moved from repeating the work to replacing it.

def Phonotactic(lusor, sur = False):
	"""
	Retrieve phonotactic elements (prefix, fix, suffix) for a lusor's genus.

	Args:
		lusor (object): The lusor object containing genus and other attributes.
		sur (bool): Whether to retrieve surname phonotactics.

	Returns:
		tuple: prefix, fix, and suffix as lists.
	"""
	if sur:
		return Surphonotactic(lusor)
	return Race_Ingredient(
		LoadRace(lusor.race),
		"Phonotactic",
		lusor.genus,
		)

def Surphonotactic(lusor):
	"""Retrieve the surname's phonotactic elements for a lusor's genus."""
	return Race_Ingredient(
		LoadRace(lusor.race),
		"Surphonotactic",
		lusor.genus,
		)

def NamesList(lusor):
	"""The lexicon of given names this lusor's kind draws on."""
	# Was: a plain `if not Names` guard falling through to
	# ``Races.plantilla.Names(genus)`` — a module never imported under that name
	# and a variable never defined in this scope. It could only ever raise
	# NameError, so an empty lexicon was the one case it did not handle.
	# Race_Ingredient treats empty as a refusal and demotes on it.
	return Race_Ingredient(
		LoadRace(lusor.race),
		"Names",
		lusor.genus,
		)

def SurnamesList(lusor):
	"""The lexicon of family names this lusor's kind draws on."""
	return Race_Ingredient(
		LoadRace(lusor.race),
		"Surnames",
		lusor.genus,
		)

# No @guardian. NewWord's ladder already gives every method METHOD_ATTEMPTS
# goes with fresh dice, and nesting a second retry inside the first turns three
# tries into thirty, each one reported. One mechanism, owned by the caller.
def Syllabic(
		prefix,
		fix,
		suffix,
		*,
		dice,
		):
	'''
	-- Syllabic Union. --
	Creates a syllabic union from the prefix, fix, and suffix lists.
	'''
	pre = dice.choice(prefix)
	fix = dice.choice(fix)
	suf = dice.choice(suffix)

	result = f"{pre}{fix}{suf}"
	return result

# No @spy. It was a development probe, and it had outlived that: this is a pure
# predicate called several times per strategy per name, and the Spy prints a
# full call tree on every one of those calls, success or failure. Nothing was
# learnt from the thousandth identical tree that the first had not already said.
def is_valid_name(name, strategy=""):
	"""
	Checks if a name is valid based on various specific criteria.

	Parameters:
		name (str): The name to check.

	Returns:
		bool: True if the name is valid, False otherwise.
	"""
	#Record(f"Checking name: {name}")
	#Record(type(name))

	if not name.isalpha(): return False

	# Check if name has the right range of length in letters
	if len(name) < 4:
		#Record("Name Too Short")
		return False
	if len(name) > 10:
		#Record("Name Too Long")
		return False

	vowels = "aeiou"

	# Check if at least one of the first two letters is a vowel or an exception
	exceptions = ["br",    "tr", "pr", "gr", "fr","vl", "dr", "bl", "ch","kr", "sh", "th", 'kl', 'st']
	if not any(char in vowels for char in name[:2].lower()):
		if not name[:2].lower() in exceptions:
			return False

	# Check each substring of 3 letters for at least one vowel
	for i in range(len(name) - 2):
		chunk = name[i:i+3].lower()
		if not any(vowel in chunk for vowel in vowels):
			return False

	# Check for no more than two consecutive vowels
	consecutive_vowels = 0
	for char in name.lower():
		if char in vowels:
			consecutive_vowels += 1
			if consecutive_vowels > 2:
				return False
		else:
			consecutive_vowels = 0

	Valid = 'aeiou'
	if not any(char in Valid for char in name[-2:].lower()):
		# Last two letters should not be consonants
		return False

	# QUE or QUI use of Q
	for i in range(len(name) - 1):
		if name[i].lower() == 'q' and not (name[i+1:i+3].lower() in ["ue", "ui"]):
			return False

	if "aa" in name.lower(): return False
	if "ee" in name.lower(): return False
	if "ii" in name.lower(): return False
	if "uu" in name.lower(): return False
	if "pp" in name.lower(): return False
	if "jr" in name.lower(): return False

	return True

DEPTH = 3

def Mixer(
		names,
		prefix,
		fix,
		suffix,
		depth=15,
		*,
		dice,
		):
	"""
	Mixes names by transforming the sound-alike letters in a name.
	"""

	import AtlasNomina.Linguistics as Linguistics

	sound_mappings = Linguistics.sound_mapping()

	# Generate a base name using NewWord and pass the seed for consistency
	Name =  NewWord(names,prefix,fix,suffix, depth-1, dice=dice)

	name_list = list(Name)
		# Transforms the name string into a list of letters

	# Iterate over each letter in the name
	for i in range(len(name_list)):
		original_letter = name_list[i].lower()
		# Decide whether to switch the letter (Weights=[switch,stay])
		if dice.choices([True, False], weights=[7, 15])[0]:
			# Get the sound-alike options for the selected letter
			sound_alike_options = sound_mappings.get(original_letter, [])
			# If there are options, replace the letter
			if sound_alike_options:
				name_list[i] = dice.choice(sound_alike_options)
	# Join the list back into a string
	result = ''.join(name_list).capitalize()
	result = entropify(result, names, dice=dice)
	return result

def mutate_entropy(
		base,
		fn,
		names,
		*,
		dice,
		):
	for _ in range(MAX_ATTEMPTS**2):
		new = fn(base, names, dice=dice)
		if new and is_valid_name(new, fn.__name__):
			return new
	return base
		# give up, keep original


def SyllabicExtraction(names):
	'''
	This function produces a set of syllables present in the words
	that make up the list of 'names'. It includes substrings of all lengths
	by sliding through each word.

	For 'Joan', it would produce:
	{'j', 'o', 'a', 'n', 'jo', 'oa', 'an', 'joa', 'oan', 'joan'}.

	Then it adds this set to the overall set, avoiding duplicates.
	'''
	import re
	syllables = set()
	pattern = re.compile(r'[bcdfghjklmnpqrstvwxyz]?[aeiou]{1,2}[bcdfghjklmnpqrstvwxyz]?')
	for name in names:
		chunks = pattern.findall(name.lower())
		for chunk in chunks:
			if 2 <= len(chunk) <= 4:
				syllables.add(chunk)

	return list(syllables)

def SyllabicComposition(
		names,
		min_syllables=2,
		max_syllables=6,
		*,
		dice,
		):
	syllables = SyllabicExtraction(names)
	if not syllables:
		return dice.choice(names)
	selected = dice.choices(syllables, k=dice.randint(min_syllables, max_syllables))
	return ''.join(selected).capitalize()


def SyllabicWeightedExtraction(names):
	syllable_weights = defaultdict(int)
	for name in names:
		length = len(name)
		for i in range(length):
			for j in range(i+1, length+1):
				syllable = name[i:j].lower()
				syllable_weights[syllable] += 1
	return syllable_weights

def SyllabicWeightedName(
		names,
		min_syllables=2,
		max_syllables=6,
		*,
		dice,
		):
	# Extracting syllables and their weights
	syllables_with_weights = SyllabicWeightedExtraction(names)

	if not syllables_with_weights:
		return dice.choice(names)

	syllables = list(syllables_with_weights.keys())
	weights   = list(syllables_with_weights.values())

	attempts = 0
	while attempts < 10:
		# pick between min_syllables and max_syllables chunks
		k = dice.randint(min_syllables, max_syllables)
		selected_syllables = dice.choices(population = syllables, weights=weights, k=k)
		name = ''.join(selected_syllables).capitalize()
		if is_valid_name(name, "SyllabicWeighted"):
			return name
		attempts += 1

	# if none passed validity in 10 tries, return whatever we last built
	return ''.join(selected_syllables).capitalize()


def SyllabicExtraction__Legacy(names):
	syllables = set()
	for name in names:
		length = len(name)
		for i in range(1, length):
			syllables.add(name[:i].lower())
			syllables.add(name[i:].lower())
	return list(syllables)

def SyllabicName__Legacy(
		syllables,
		min_syllables=2,
		max_syllables=8,
		*,
		dice,
		):
	name = ''.join(dice.choice(syllables) for _ in range(dice.randint(min_syllables, max_syllables)))
	return name.capitalize()


# ---------------------------------------------------------------------------
# Self-test: the naming ladder under ruling 8 (QST-0144.6)
# ---------------------------------------------------------------------------


class _Recording_Dice:
	"""A Dice Bag that remembers every pool it was asked to draw from."""

	def __init__(
			self,
			bag,
			):
		self.bag = bag
		self.calls = []

	def choice(
			self,
			pool,
			):
		self.calls.append(
			(
				"choice",
				list(pool),
				),
			)
		return self.bag.choice(
			pool,
			)

	def choices(
			self,
			pool,
			weights=None,
			k=1,
			):
		self.calls.append(
			(
				"choices",
				list(pool),
				k,
				),
			)
		return self.bag.choices(
			pool,
			weights=weights,
			k=k,
			)

	def shuffle(
			self,
			pool,
			):
		self.calls.append(
			(
				"shuffle",
				list(pool),
				),
			)
		self.bag.shuffle(
			pool,
			)

	def randint(
			self,
			low,
			high,
			):
		self.calls.append(
			(
				"randint",
				low,
				high,
				),
			)
		return self.bag.randint(
			low,
			high,
			)


def _probe_lusor(
		seed,
		level=1,
		):
	"""A bare Character carrying the three attributes NewName reads."""
	from AtlasActorLudi.CharactersKit import Character

	class Lusor(Character):
		def __init__(
				self,
				seed,
				level,
				):
			super().__init__(
				seed=seed,
				level=level,
				)
			self.genus = "Elf , Rogue , They"
			self.race = "Elf"
			self.gender = "They"

	return Lusor(
		seed,
		level,
		)


def _test_new_name_opens_one_bag():
	"""NewName opens exactly one Dice Bag, identity.name, and the shared streams never move."""
	import random
	import app.random as app_random
	from AtlasActorLudi.CharactersKit import Character

	opened = []
	original = Character.Dice_Bag

	def Recording_Dice_Bag(
			char,
			purpose,
			*,
			version="1",
			namespace="GenLegend",
			):
		opened.append(
			(
				purpose,
				version,
				namespace,
				),
			)
		return original(
			char,
			purpose,
			version=version,
			namespace=namespace,
			)

	Character.Dice_Bag = Recording_Dice_Bag
	stdlib_state = random.getstate()
	app_state = app_random.getstate()
	try:
		name = NewName(
			_probe_lusor(
				seed=7,
				),
			)
	finally:
		Character.Dice_Bag = original

	assert opened == [
		(
			"identity.name",
			"1",
			"GenLegend",
			),
		], opened
	assert random.getstate() == stdlib_state, "the stdlib stream moved"
	assert app_random.getstate() == app_state, "app.random moved"
	assert isinstance(
		name,
		str,
		) and name.strip(), name


def _test_name_is_keyed_by_the_bag():
	"""Same seed, same name, whatever the level or the state of the main bag."""
	first = _probe_lusor(
		seed=11,
		)
	again = _probe_lusor(
		seed=11,
		level=20,
		)
	again.dices.random()
		#-- the main bag has moved; the name must not care
	assert NewName(first) == NewName(again)
	assert NewName(
		_probe_lusor(
			seed=12,
			),
		) != NewName(first)


def _test_new_word_pools_are_what_they_were():
	"""The strategy shuffle and every base draw come from the pools they always did."""
	from AtlasActorLudi.CharactersKit import Character

	names = list(LAST_RESORT_NAMES)
	prefix, fix, suffix = LAST_RESORT_PHONOTACTIC
	known_pools = (
		names,
		list(prefix),
		list(fix),
		list(suffix),
		)
	for seed in range(1, 13):
		dice = _Recording_Dice(
			Character(
				seed=seed,
				).Dice_Bag(
					NAME_PURPOSE,
					),
			)
		word = NewWord(
			names,
			prefix,
			fix,
			suffix,
			dice=dice,
			)
		assert word, seed
		assert dice.calls[0] == (
			"shuffle",
			[
				"Entropify",
				"EntropyDown",
				"Mutate",
				"Markov",
				"Syllabic",
				"Choose",
				],
			), dice.calls[0]
		for call in dice.calls[1:]:
			if call[0] == "choice":
				is_markov_start = all(
					set(state) == {"^"}
					for state in call[1]
					)
				assert call[1] in known_pools or is_markov_start, call
			elif call[0] == "choices":
				assert call[2] == 1, call
					#-- the Markov walk: one next character at a time


def _test_syllabic_draws_prefix_fix_suffix():
	"""Syllabic draws one prefix, one fix and one suffix, in that order, from the dice."""
	from AtlasActorLudi.CharactersKit import Character

	prefix, fix, suffix = LAST_RESORT_PHONOTACTIC
	dice = _Recording_Dice(
		Character(
			seed=2,
			).Dice_Bag(
				NAME_PURPOSE,
				),
		)
	word = Syllabic(
		prefix,
		fix,
		suffix,
		dice=dice,
		)
	assert word
	assert dice.calls == [
		("choice", list(prefix)),
		("choice", list(fix)),
		("choice", list(suffix)),
		], dice.calls


def _test_a_lusor_without_a_bag_keeps_the_shared_stream():
	"""The legacy NonPlayer (no Dice Bag) still names itself from app.random, deterministic per seed."""
	import app.random as app_random

	class Legacy_Lusor:
		genus = "Elf , Rogue , They"
		race = "Elf"
		gender = "They"
		seed = 5

	assert Naming_Dice(
		Legacy_Lusor(),
		) is app_random
	app_random.seed(5)
	first_lusor = Legacy_Lusor()
	first = NewName(first_lusor)
	assert hasattr(first_lusor, "_name"), "NewName did not answer itself"
	app_random.seed(5)
	assert NewName(Legacy_Lusor()) == first


if __name__ == "__main__":
	_test_new_name_opens_one_bag()
	_test_name_is_keyed_by_the_bag()
	_test_new_word_pools_are_what_they_were()
	_test_syllabic_draws_prefix_fix_suffix()
	_test_a_lusor_without_a_bag_keeps_the_shared_stream()
	print("Map_of_Names: self-test passed")
