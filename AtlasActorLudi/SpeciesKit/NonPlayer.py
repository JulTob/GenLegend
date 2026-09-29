"""Humanoid Species Shapes used by the NonPlayer production line."""

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.declarations import Legacy_NonPlayer
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


class Aven(
	Species,
	Humanoid,
	):
	"""A birdlike Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Aven)


class Beastfolk(
	Species,
	Humanoid,
	):
	"""A Humanoid lineage with bestial traits."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Beastfolk)


class Catfolk(
	Species,
	Humanoid,
	):
	"""A feline Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Catfolk)


class Goblin(
	Species,
	Humanoid,
	):
	"""A Goblin Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Goblin)


class Kobold(
	Species,
	Humanoid,
	):
	"""A Kobold Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Kobold)


class Lizardfolk(
	Species,
	Humanoid,
	):
	"""A reptilian Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Lizardfolk)


class Snakefolk(
	Species,
	Humanoid,
	):
	"""A serpentine Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Snakefolk)
