'''
Self-test of Map_of_Titles: one title for each genus line of a small roster.

Run it as ``python -m AtlasEpica.Map_of_Titles``. The roster and test() are
the single file's own; check_package() first makes sure every name that file
defined still answers from the package.
'''
from AtlasEpica.Map_of_Titles import Title

def test():
	from AtlasActorLudi.CharactersKit import Character

	class Lusor(Character):
		def __init__(
				self,
				genus: str,
				seed: int = 1,
				):
			super().__init__(
				seed=seed,
				)

			self.genus = genus

		def __contains__(self, key: str) -> bool:
			return key in self.genus

	lusors = [
		Lusor("Kitsune Cleric Sage"),
		Lusor("Vampire Undead Paladin"),
		Lusor("Dwarf Barbarian Fighter"),
		Lusor("Elf Rogue Wizard"),
		Lusor("Halfling Cleric Paladin"),
		Lusor("Gnome Rogue Fighter"),
		Lusor("Half-Elf-Human Rogue Paladin"),
		Lusor("Half-Orc+Celestial Barbarian Fighter"),
		Lusor("Fairy Rogue Wizard"),
		Lusor("Demon Fiend Berserker Barbarian"),
		Lusor("Orc Barbarian Wizard"),
		]

	for lusor in lusors:
		print(f"{lusor.genus}: \n\t{Title(lusor)}")

def check_package():
	'''Every name the single-file Map_of_Titles defined answers from the package.'''
	import AtlasEpica.Map_of_Titles as titles

	names = (
		"Title", "LastResortTitle", "LAST_RESORT_TITLES", "Genus", "_part",
		"custom_cases", "Descriptor", "Rank", "Place", "Element",
		"Artifact", "Master", "Animal", "Origin",
		)
	missing = [name for name in names if not hasattr(titles, name)]
	assert not missing, f"Map_of_Titles no longer answers to {missing}"
	print(f"Map_of_Titles: {len(names)} names reachable from the package.")


if __name__ == "__main__":
	check_package()
	test()
