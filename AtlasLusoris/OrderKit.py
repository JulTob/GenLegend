"""
OrderKit — Secret Orders, collapsed one at a time.

An Order **precedes the Character**.  It is a thing already standing in the
world when someone knocks on its door, so it owns its own dice and picks its
own nature; a Character then *joins* one.  That is why the generator is
``Order(seed=...)`` and not a function of a Character.

	from AtlasLusoris.OrderKit import Order, Swear
	order = Order(seed=12)          # a house that exists whether or not anyone joins
	Swear(char, order)              # this Character is now sworn to it

Collapse order (each step narrows the next, none of them forbid anything):

	Tradition      Arcane | Divine | Primal → places, practices, safe spells
	Domains        two, unordered           → mechanics, philosophy, tension
	Facets         one face per Domain      → creed and goal
	Organization   Temple | Academy | …     → and the word then governs the prose
	Devotion       god | dragon | theorem | the dead | a river with opinions
	Name           <organization> of the <descriptor> <core>
	Perk · Sacrifice · Goal
	Feat           intuition_die · signature_magic · spells_of_the_order

Nothing here forbids a combination.  A Mercy order whose goal is a killing is
a surgeon's order that has decided what the tumour is, and it is *better* than
a safe one.  The generator states the pair and stops; the reader supplies the
reason, faster and better than any template could.
"""

from __future__ import annotations

from random import Random

from TopKit import Imprint, Pin, Pre, Record, Tag

from AtlasActorLudi.CharactersKit import Character
from AtlasLusoris.AtlasOfOrders.Map_of_Domains import DOMAINS
from AtlasEpica.Charts_of_The_Monomyth import render
from AtlasLusoris.AtlasOfOrders.Map_of_Myth import Myth as Make_Myth
from AtlasLusoris.AtlasOfOrders.Map_of_Traditions import (
	COMMON_ORGANIZATIONS,
	TRADITIONS,
	)
from AtlasLusoris.FeaturesKit import Origin_Feat, grant
from AtlasVenustas import Entry
from AtlasVenustas import Chip


# ---------------------------------------------------------------------------
# The Order — collapsed on construction
# ---------------------------------------------------------------------------


def _sentence_case(
		text: str,
		) -> str:
	"""
	Capitalise the opening of every sentence.

	A token may resolve at a sentence head — ``{perk}`` opening a Hook, a
	facet name opening a clause — and the pools store those lowercase
	because they are usually mid-sentence.  Fixing it here keeps every pool
	free to be written in its natural, mid-sentence form.
	"""
	letters = list(
		text
		)
	start = True

	for index, character in enumerate(
		letters
		):
		if start and character.isalpha():
			letters[index] = character.upper()
			start = False
		elif character in ".!?":
			start = True

	return "".join(
		letters
		)


class _Vocabulary(dict):
	"""
	Slot lookup that draws a word the first time one is asked for.

	Anything the Order supplies directly (``{house}``, ``{goal}``) is already
	present.  Anything else is a VOCABULARY key, drawn once through the
	Order's dice and then remembered, so a beat stays internally consistent.
	"""

	def __init__(
			words,
			order,
			base,
			):
		super().__init__(
			base
			)
		words.order = order

	def __missing__(
			words,
			key,
			):
		pool = VOCABULARY.get(
			key
			)

		if pool is None:
			raise KeyError(
				key
				)

		drawn = words.order.Pick(
			pool
			)
		words[key] = drawn

		return drawn


class Order:
	"""One Secret Order, complete: name, doctrine, mechanics, and a price."""

	def __init__(
			order,
			seed: int = -1,
			):
		rng = Random()
		order.seed = int(
			seed
			if seed >= 0
			else rng.randint(
				0,
				2 ** 64,
				)
			)
		order.dices = Random(
			order.seed
			)

		order._collapse()

	# --- the one randomness surface ------------------------------------

	def Pick(
			order,
			ledger,
			weights=None,
			):
		"""Pick one item through this Order's own dice."""
		if not ledger:
			raise ValueError(
				"Pick: empty ledger"
				)

		if weights is None:
			return order.dices.choice(
				list(
					ledger
					)
				)

		return order.dices.choices(
			list(
				ledger
				),
			weights=list(
				weights
				),
			k=1,
			)[0]

	def Sample(
			order,
			ledger,
			count,
			):
		"""Pick several distinct items, in a stable order."""
		pool = list(
			ledger
			)

		if count >= len(
			pool
			):
			return tuple(
				pool
				)

		return tuple(
			order.dices.sample(
				pool,
				count,
				)
			)

	# --- collapse -------------------------------------------------------

	def _collapse(
			order,
			):
		order.tradition = order.Pick(
			TRADITIONS
			)
		order.domains = order.Sample(
			DOMAINS,
			2,
			)
		order.facets = tuple(
			order.Pick(
				domain.facets
				)
			for domain in order.domains
			)

		order.organization = order.Pick(
			tuple(
				order.tradition.organizations
				)
			+ COMMON_ORGANIZATIONS
			)
		order.devotion = order.Pick(
			order.tradition.devotions
			)
		order.place = order.Pick(
			order.tradition.places
			)
		order.practice = order.Pick(
			order.tradition.practices
			)

		# The name crosses the two spheres on purpose: a descriptor from one
		# and a core from the other gives "the Salt Anvil" rather than a
		# label that merely restates a single domain.
		first, second = order.domains

		if order.Pick(
			(
				True,
				False,
				)
			):
			first, second = second, first

		order.descriptor = order.Pick(
			first.descriptors
			)
		order.core = order.Pick(
			second.cores
			)
		order.title = f"the {order.descriptor} {order.core}"
		order.name = f"{order.organization} of {order.title}"

		relics = tuple(
			relic
			for domain in order.domains
			for relic in domain.relics
			)
		order.relic = order.Pick(
			relics
			)

		order.perk = order.Pick(
			tuple(
				perk
				for domain in order.domains
				for perk in domain.perks
				)
			)
		order.sacrifice = order.Pick(
			tuple(
				sacrifice
				for domain in order.domains
				for sacrifice in domain.sacrifices
				)
			)
		order.goal = order.Pick(
			tuple(
				facet.goal
				for facet in order.facets
				)
			)

		order._keys = frozenset(
			(
				order.tradition.name,
				order.organization,
				*(
					domain.name
					for domain in order.domains
					),
				*(
					domain.mark
					for domain in order.domains
					),
				*(
					facet.name
					for facet in order.facets
					),
				)
			)

		order._collapse_mechanics()
		order.description = order._write_description()
		order.hook = order._write_hook()

	def _collapse_mechanics(
			order,
			):
		"""Fill the three published slots from the two Domains."""
		checks = tuple(
			dict.fromkeys(
				check
				for domain in order.domains
				for check in domain.checks
				)
			)
		order.intuition_die = order.Sample(
			checks,
			2,
			)

		# The signature may cross spheres: the cantrip of one house and the
		# prepared spell of the other is a perfectly ordinary hybrid.
		order.cantrip = order.Pick(
			order.domains
			).cantrip
		order.prepared = order.Pick(
			order.domains
			).prepared

		merged: dict[int, tuple] = {}

		for level in (
			1,
			2,
			3,
			4,
			5,
			):
			spells = tuple(
				dict.fromkeys(
					spell
					for domain in order.domains
					for spell in domain.spells_of_the_order.get(
						level,
						(),
						)
					)
				)

			if not spells:
				# Safe coding: the Tradition guarantees the list is never bare.
				spells = tuple(
					order.tradition.fallback.get(
						level,
						(),
						)
					)

			if spells:
				# Two spheres merged can offer five at a level; the published
				# marks offer about two, so thin it rather than out-granting
				# the thing we patterned on.
				merged[level] = order.Sample(
					spells,
					2,
					)

		order.spells_of_the_order = merged

	# --- prose ----------------------------------------------------------

	def _slots(
			order,
			):
		return {
			"organization": order.organization,
			"house": order.organization.lower(),
			"order": f"the {order.name}",
			"devotion": order.devotion,
			"domain_a": order.domains[0].name,
			"domain_b": order.domains[1].name,
			"facet_a": order.facets[0].name,
			"facet_b": order.facets[1].name,
			"creed_a": order.facets[0].creed,
			"creed_b": order.facets[1].creed,
			"place": order.place,
			"practice": order.practice,
			"relic": order.relic,
			"perk": order.perk,
			"sacrifice": order.sacrifice,
			"goal": order.goal,
			}

	def _line(
			order,
			pool,
			):
		"""
		One beat: a shape drawn from ``pool``, then filled.

		Filling repeats, because a word drawn from VOCABULARY may itself
		carry slots — ``{belonging}`` can mention ``{house}`` — and a beat is
		not finished until nothing is left in braces.  Within one beat a
		vocabulary key resolves once and stays put, so a sentence that uses
		``{kin}`` twice does not contradict itself; across beats it is drawn
		fresh.
		"""
		line = order.Pick(
			pool
			)
		words = _Vocabulary(
			order,
			order._slots(),
			)

		for _ in range(
			6,
			):
			if "{" not in line:
				break

			line = line.format_map(
				words
				)

		# Slots can land at the head of a sentence (a facet name, an Order
		# name), so capitalise the opening of the line and of anything that
		# follows a full stop.
		letters = list(
			line
			)
		start = True

		for index, character in enumerate(
			letters
			):
			if start and character.isalpha():
				letters[index] = character.upper()
				start = False
			elif character in ".!?":
				start = True

		return "".join(
			letters
			)

	def _write_description(
			order,
			):
		"""
		Walk the arc through the project's Myth engine.

		``render`` resolves nested tokens over several passes, filters rows
		by ``If(order, conds)`` so domain-flavoured sentences reach only the
		Orders that keep that sphere, stores each resolution back so a token
		reads the same twice, and strips anything that failed to resolve
		rather than leaking a brace.
		"""
		myth = Make_Myth(
			order
			)
		order._myth = myth

		return _sentence_case(
			render(
				myth["Script"],
				myth,
				order,
				rng=order.dices,
				)
			)

	def _write_hook(
			order,
			):
		"""One hook: a pro, a con, and the purpose the con is paying for."""
		myth = getattr(
			order,
			"_myth",
			None,
			) or Make_Myth(
			order
			)

		return Entry(
			title=order.name,
			rules=_sentence_case(
				render(
					"{Hook}",
					myth,
					order,
					rng=order.dices,
					)
				),
			)

	# --- the feat -------------------------------------------------------

	def feat_name(
			order,
			):
		return f"Sign of {order.title}"

	def feat_description(
			order,
			):
		checks = " or ".join(
			order.intuition_die
			)
		levels = "; ".join(
			f"{level}: "
			+ ", ".join(
				getattr(
					spell,
					"name",
					str(
						spell
						),
					)
				for spell in spells
				)
			for level, spells in sorted(
				order.spells_of_the_order.items()
				)
			)

		return (
			f"<b>Intuition of {order.title}.</b> When you make an ability "
			f"check using {checks}, you can roll 1d4 and add the number "
			"rolled to the check. "
			"<b>Signature Magic.</b> You know the "
			f"<i>{getattr(order.cantrip, 'name', order.cantrip)}</i> cantrip. "
			"You always have "
			f"<i>{getattr(order.prepared, 'name', order.prepared)}</i> "
			"prepared, and can cast it once without a spell slot per Long "
			"Rest. Intelligence, Wisdom, or Charisma is your spellcasting "
			"ability for them (choose when you gain this feat). "
			"<b>Spells of the Order.</b> If you have the Spellcasting or Pact "
			"Magic feature, these are added to your spell list, by level "
			f"({levels})."
			)

	def __contains__(
			order,
			key,
			):
		"""
		Answer ``in`` so Myth rows can be gated on what this Order *is*.

		``If(host, conds)`` accepts any object with ``__contains__``, so a
		sentence tagged ``("the Veil", …)`` becomes eligible only for an
		Order that actually keeps that sphere — which is how the prose
		carries a theme without ever naming it.

		It also answers for **narrative facts already told**.  ``render``
		collapses a token to a literal the first time it resolves, so a
		token that has become a string is a thing the story has *said*.
		A row gated ``("sick_elder", …)`` therefore reaches only a telling
		in which an elder was actually invoked — which is how a later
		sentence may safely refer back to one, and how beats stop being
		independent draws.
		"""
		if key in order._keys:
			return True

		myth = getattr(
			order,
			"_myth",
			None,
			)

		return bool(
			myth
			) and isinstance(
			myth.get(
				key
				),
			str,
			)

	def __str__(
			order,
			):
		return order.name


# ---------------------------------------------------------------------------
# Tags — membership, and the minted per-Order sigil
# ---------------------------------------------------------------------------


class Sworn(Tag):
	"""Root of "this Character belongs to a Secret Order"."""

	NAME = "Sworn"

	@Pre
	def Character_Only(
			target,
			):
		return isinstance(
			target,
			Character,
			)


@Pin
class Declared_Order(Tag):
	"""
	Root Pin for the Sworn Tags minted per Order.

	This is a Pin rather than a dictionary: ``order_tag`` classifies the
	Tag it mints by applying this Pin *to that Tag*, and
	``Declared_Order[:]`` is then the catalogue of every Order anyone has
	sworn to, in minting order.  The Records below land on the minted Tag
	as Reports (``tag.TITLE``, ``tag.TRADITION``, ``tag.DOMAINS``),
	validated here instead of written blind into a class namespace.
	"""

	NAME = "Declared Order"

	@Pre
	def Sworn_Tag_Only(
			target,
			):
		return (
			isinstance(
				target,
				type,
				)
			and issubclass(
				target,
				Sworn,
				)
			and target is not Sworn
			)

	@Record
	def TITLE(
			target,
			*,
			title=None,
			) -> str:
		"""The Order's title: what follows "of" in its name."""
		if (
			not isinstance(
				title,
				str,
				)
			or not title.strip()
			):
			raise ValueError(
				"An Order's title must be non-empty text."
				)

		return title

	@Record
	def TRADITION(
			target,
			*,
			tradition=None,
			) -> str:
		"""The name of the Tradition the Order collapsed into."""
		if (
			not isinstance(
				tradition,
				str,
				)
			or not tradition.strip()
			):
			raise ValueError(
				"An Order's Tradition must be a non-empty name."
				)

		return tradition

	@Record
	def DOMAINS(
			target,
			*,
			domains=(),
			) -> tuple[str, ...]:
		"""The names of the Order's Domains, in the order it drew them."""
		resolved = tuple(
			domains or ()
			)

		if any(
			not isinstance(
				domain,
				str,
				)
			or not domain.strip()
			for domain in resolved
			):
			raise ValueError(
				"An Order's Domains must be non-empty names."
				)

		if len(
			set(
				resolved
				)
			) != len(
				resolved
				):
			raise ValueError(
				"An Order cannot hold one Domain twice."
				)

		return resolved


def _class_name(
		name: str,
		) -> str:
	safe = "".join(
		character
		if character.isalnum()
		else "_"
		for character in name
		)

	return safe.strip(
		"_"
		) or "Order"


def order_tag(
		order: Order,
		) -> type[Sworn]:
	"""
	Mint (once) the Tag that means "sworn to this particular Order".

	The Field of ``Declared_Order`` is the memo: an Order already minted is
	found there by NAME, so a second call answers the same Tag.  The Tag
	is built with only its identity, and the Pin lands the rest.
	"""
	key = order.name

	for tag in Declared_Order[:]:
		if tag.NAME == key:
			return tag

	tag = type(
		_class_name(
			key
			),
		(
			Sworn,
			),
		{
			"NAME": key,
			"__doc__": f"Sworn to {key}.",
			"__module__": __name__,
			},
		)
	Declared_Order(
		tag,
		title=order.title,
		tradition=order.tradition.name,
		domains=tuple(
			domain.name
			for domain in order.domains
			),
		)

	return tag


def order_feat(
		order: Order,
		) -> type[Origin_Feat]:
	"""Mint the Origin Feat this Order's sigil confers."""
	name = order.feat_name()
	description = order.feat_description()

	@Imprint
	def awaken(
			char,
			):
		from AtlasLusoris.AtlasOfFeatures.Map_of_Official_Origin_Feats import (
			_grant_known_cantrip,
			)

		_grant_known_cantrip(
			char,
			order.cantrip,
			)
		_grant_known_cantrip(
			char,
			order.prepared,
			)
		grant(
			char,
			name,
			description,
			source="Origin Feat",
			chips=(
				Chip(
					"🕯",
					getattr(
						order.prepared,
						"name",
						"Signature",
						),
					"1/LR",
					),
				),
			)

	return type(
		_class_name(
			name
			),
		(
			Origin_Feat,
			),
		{
			"NAME": name,
			"DESCRIPTION": description,
			"awaken": awaken,
			"__module__": __name__,
			},
		)


# ---------------------------------------------------------------------------
# Joining
# ---------------------------------------------------------------------------


class Sign_of_the_Order(Origin_Feat):
	"""
	The doorway feat: an initiate's mark, whose powers are not known until
	the Order is known.

	A Background Tag inherits its Origin Feat, so the class must exist when
	the Background is declared — but an Order mints its own feat per
	Character.  This one therefore carries no mechanics of its own.  It
	collapses the Order and lets *that* grant the real sign, so the sheet
	shows one feat (``Sign of the Quiet Forge``) rather than a placeholder
	beside it.
	"""

	NAME = "Sign of the Order"
	DESCRIPTION = (
		"An initiate's mark, conferred at swearing. What it grants depends "
		"on which Order conferred it."
		)

	@Imprint
	def awaken(
			char,
			):
		Forge_Order(
			char
			)


def Forge_Order(
		char,
		order: Order | None = None,
		) -> Order:
	"""
	Collapse one Character's Order and write it onto the sheet.

	Grants only — **no Tag application** — so this is safe to call from
	inside an Imprint, where TagKit forbids re-entrant tagging.  With no
	Order given, one is collapsed from the Character's own seed, so the same
	Character always finds the same door.  Orders are deliberately never
	shared: two people each sworn to a *different* secret order is comedy
	and drama, while co-membership makes one of them an authority and
	flattens both.
	"""
	if order is None:
		order = Order(
			seed=getattr(
				char,
				"seed",
				0,
				)
			)

	char.order = order
	grant(
		char,
		name=order.name,
		description=order.description,
		source="Secret Order",
		)
	grant(
		char,
		name=order.hook.title,
		description=order.hook.rules,
		source="Order Hook",
		)
	grant(
		char,
		name=order.feat_name(),
		description=order.feat_description(),
		source="Origin Feat",
		)

	return order


def Resolve_Order_Features(
		char,
		):
	"""
	Apply Order sigil mechanics once sheet lists exist.

	``Forge_Order`` writes the prose entries during Background imprint;
	cantrips need ``known_spells`` first. Idempotent across the two
	calls in ``set_char_features``.
	"""
	order = getattr(
		char,
		"order",
		None,
		)
	if order is None:
		return char

	from AtlasLusoris.AtlasOfFeatures.Map_of_Official_Origin_Feats import (
		_grant_known_cantrip,
		)

	_grant_known_cantrip(
		char,
		order.cantrip,
		)
	_grant_known_cantrip(
		char,
		order.prepared,
		)

	return char


def Swear(
		char,
		order: Order | None = None,
		) -> Order:
	"""
	Forge the Order and stamp its Tags as well.

	Use from ordinary code, never from inside another Tag's Imprint: it
	applies ``Sworn`` membership and the minted per-Order sigil, so
	``char in Sworn`` and ``char in order_tag(order)`` both answer.
	"""
	order = Forge_Order(
		char,
		order,
		)
	order_tag(
		order
		)(
		char
		)

	return order


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def _test_reproducible():
	first = Order(
		seed=99
		)
	second = Order(
		seed=99
		)
	assert first.name == second.name
	assert first.description == second.description
	assert first.feat_description() == second.feat_description()


def _test_shape():
	order = Order(
		seed=7
		)
	assert len(
		order.domains
		) == 2
	assert order.domains[0] is not order.domains[1]
	assert len(
		order.facets
		) == 2
	assert len(
		order.intuition_die
		) == 2
	assert order.spells_of_the_order, "spell list must never be empty"
	assert order.organization in order.name
	assert "{" not in order.description, "an unfilled slot escaped"
	assert "{" not in order.hook.rules


def _test_variety():
	names = {
		Order(
			seed=index
			).name
		for index in range(
			40
			)
		}
	assert len(
		names
		) > 30, f"only {len(names)} distinct names in 40 rolls"


def _test_swearing():
	import gc

	from AtlasActorLudi.CharactersKit import Player

	char = Character(
		seed=5
		)
	Player(
		char
		)
	order = Swear(
		char
		)
	assert char in Sworn
	assert char.order is order
	#-- The memo is the Pin's Field, held weakly: the Character carrying
	#-- the sigil keeps it findable, so this holds after a sweep too.
	gc.collect()
	assert char in order_tag(
		order
		)
	names = [
		getattr(
			feature,
			"name",
			"",
			)
		for feature in char.features
		]
	assert order.name in names
	assert order.feat_name() in names


def _test_declared_orders():
	"""The Pin's Field is the catalogue the memo dictionary used to be."""
	from TopKit import TagCompositionError

	orders = tuple(
		Order(
			seed=seed
			)
		for seed in (
			11,
			12,
			13,
			)
		)
	before = tuple(
		Declared_Order[:]
		)
	minted = tuple(
		order_tag(
			order
			)
		for order in orders
		)

	#-- The Field holds what the old dictionary held: every minted Tag, in
	#-- minting order, keyed by NAME, nothing twice.
	assert tuple(
		Declared_Order[:]
		) == before + minted
	assert tuple(
		tag.NAME
		for tag in minted
		) == tuple(
			order.name
			for order in orders
			)
	assert len(
		{
			tag.NAME
			for tag in Declared_Order[:]
			}
		) == len(
			Declared_Order[:]
			)

	for order, tag in zip(
		orders,
		minted,
		):
		#-- The memo: a second call answers the same Tag, not a sibling.
		assert order_tag(
			order
			) is tag
		assert tag in Declared_Order
		assert issubclass(
			tag,
			Sworn,
			)
		#-- The Reports the namespace used to carry, now landed by the Pin.
		assert tag.TITLE == order.title
		assert tag.TRADITION == order.tradition.name
		assert tag.DOMAINS == tuple(
			domain.name
			for domain in order.domains
			)

	#-- A declaration the Pin refuses never joins the Field.
	stray = type(
		"Stray_Order",
		(
			Sworn,
			),
		{
			"NAME": "Stray Order",
			"__module__": __name__,
			},
		)
	try:
		Declared_Order(
			stray,
			title="",
			tradition="Arcane",
			domains=(),
			)
	except TagCompositionError:
		pass
	else:
		raise AssertionError(
			"Declared_Order accepted a blank title"
			)
	assert stray not in Declared_Order


def _self_test():
	_test_reproducible()
	_test_shape()
	_test_variety()
	_test_swearing()
	_test_declared_orders()
	print(
		"OK — OrderKit self-test"
		)


if __name__ == "__main__":
	_self_test()


__all__ = (
	"Order",
	"Sworn",
	"Declared_Order",
	"Swear",
	"Forge_Order",
	"Resolve_Order_Features",
	"order_feat",
	"order_tag",
	"Sign_of_the_Order",
	)
