'''
Genus: the genus line every vocabulary of Map_of_Titles tests against.

The one helper the vocabularies share. It lives apart from __init__ so that
a vocabulary imports this file and never the package itself, which is what
keeps the package free of circular imports. The story engine may import it
too.
'''

def Genus(lusor):
	'''
The genus line a vocabulary function tests against.

Every function in this file is handed the lusor, and every one of them wants
the same thing out of it: the genus, which is where the kind, the subrace,
the class, the background, the gender and the alignment are all written
down. Routing that through one accessor is what makes ``"Cleric" in
Genus(lusor)`` mean what it reads as.

Written the other way, as ``"Cleric" in lusor``, it silently asks TagKit
whether a Tag goes by that string, which is never true of a plain string. It
raised TypeError on a bare Character and answered False on a tagged one, so
all twenty of those tests were False forever and every line of conditional
vocabulary behind them had never once been reached. A Human was never
offered a Realm, a Cleric never a Sanctuary, a Vampire never anything of
its own.
'''
	return str(
		getattr(
			lusor,
			"genus",
			lusor,
			)
		or ""
		)
