"""Humanoid Species Shapes used by the NonPlayer production line."""

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.declarations import Legacy_NonPlayer
from TopKit import Flag
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Aven" )
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


@Flag( "Beastfolk" )
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


@Flag( "Catfolk" )
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


@Flag( "Goblin" )
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


@Flag( "Kobold" )
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


@Flag( "Lizardfolk" )
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


@Flag( "Snakefolk" )
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
