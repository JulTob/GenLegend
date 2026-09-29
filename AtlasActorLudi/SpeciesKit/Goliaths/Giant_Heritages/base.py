"""The internal Goliath Giant Heritage Geometry."""

from TopKit import Pre

from AtlasLusoris.FeaturesKit import Trait


class Giant_Heritage(Trait):
	"""One persistent supernatural boon inherited from Giants."""

	LEVEL = 1
	USES = "PB"
	RECOVERY = "Long Rest"

	@Pre
	def Goliath_Only(
		target,
		):
		from AtlasActorLudi.SpeciesKit.Goliaths import Goliath

		return target in Goliath


def Current_Giant_Heritage(
	target,
	):
	"""Return the one Giant Heritage Shape currently carried."""
	from AtlasActorLudi.SpeciesKit.Goliaths.Giant_Heritages import GOLIATH_GIANT_HERITAGES

	# Tag membership is the only ledger of a carried Heritage: ask every
	# declared Heritage and keep the ones that hold this target.
	carried = tuple(
		heritage
		for heritage in GOLIATH_GIANT_HERITAGES
		if target in heritage
		)

	if len( carried ) > 1:
		raise ValueError(
			"A Goliath carries conflicting Giant Heritages: "
			+ ", ".join(
				heritage.__name__
				for heritage in carried
				)
			+ "."
			)

	return (
		carried[0]
		if carried
		else None
		)


def Imprint_Giant_Heritage(
	target,
	heritage,
	) -> None:
	"""Imprint one generated Giant Heritage while Tagging stays atomic."""
	current = Current_Giant_Heritage( target )

	if (
		current is not None
		and current is not heritage
		):
		raise ValueError(
			"A Goliath cannot carry two Giant Heritages: "
			f"{current.__name__!r} and {heritage.__name__!r}."
			)

	target.giant_heritage = heritage.DISPLAY
	target.giant_kind = heritage.GIANT_KIND
	target.giant_heritage_activation = heritage.ACTIVATION
	target.giant_heritage_use_scaling = "Proficiency Bonus"
	target.giant_heritage_recovery = heritage.RECOVERY


def No_Giant_Heritage_Yet(
	target,
	) -> bool:
	"""The gate every Giant Heritage declares: a Goliath has one."""
	return target not in Giant_Heritage
