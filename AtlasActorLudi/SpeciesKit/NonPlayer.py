"""Humanoid Species Shapes used by the NonPlayer production line."""

from AtlasActorLudi.SpeciesKit.bases import Humanoid
from AtlasActorLudi.SpeciesKit.bases import Species
from AtlasActorLudi.SpeciesKit.declarations import Legacy_NonPlayer
from AtlasActorLudi.SpeciesKit.kinship import Dragon as Kin_Dragon
from AtlasActorLudi.SpeciesKit.kinship import Fey as Kin_Fey
from TopKit import Flag
from TopKit import Pre
from AtlasActorLudi.SpeciesKit.bases import No_Species_Yet


@Flag( "Aven", "Bird", "Raptor" )
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


@Flag( "Beastfolk", "Beast" )
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


@Flag( "Catfolk", "Cat", "Feline" )
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


@Flag( "Goblin", "Fae" )
class Goblin(
	Species,
	Humanoid,
	Kin_Fey,
	):
	"""A Goblin Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Goblin)


@Flag( "Kobold", "Dog" )
class Kobold(
	Species,
	Humanoid,
	Kin_Dragon,
	):
	"""A Kobold Humanoid lineage."""

	@Pre
	def Only_One_Species(
		target,
		):
		return No_Species_Yet( target )


Legacy_NonPlayer(Kobold)


@Flag( "Lizardfolk", "Lizard", "Reptile" )
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


@Flag( "Snakefolk", "Snake", "Reptile" )
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
