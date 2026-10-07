#!/usr/bin/env python3
"""Prove that every choice of a Character's build comes from its own Dice Bag.

This is a cross-module integration rite, here for the reason
``verify_fingerprint`` gives: one generated Character crosses every Atlas, so
no single module can hold the proof.

Ruling 8 of Dialog 0027 (QST-0144.6): every pick of a Character goes through
the Character's own random source, the Dice Bag, opened with a purpose named
by the Tag that offers the choice.  Three things break that law quietly and
this rite watches for all three while the grid is summoned:

- a purpose **derived** from the caller's stack frame (``module.function#n``)
  instead of written by the Tag;
- a draw from the **shared** streams, Python's ``random`` module or
  ``app.random``, which couple every later pick to every earlier one;
- a **private** ``random.Random( ... )`` opened outside ``Character.Dice_Bag``,
  a second Dice Bag design with its own key.

Run:

    .venv/bin/python scripts/verify_dice_purposes.py --report
    .venv/bin/python scripts/verify_dice_purposes.py --save scripts/dice_purposes.txt
    .venv/bin/python scripts/verify_dice_purposes.py --check scripts/dice_purposes.txt

``--report`` lists what the grid opened and never fails.  ``--save`` writes the
manifest of purposes, one per line, sorted; a line ending in ``.*`` declares
a family (``gear.title.*``: one bag per forged item, named by the item).  ``--check`` fails when the grid
opens a purpose the manifest does not declare (a new choice must be declared),
when any purpose is derived, and when any draw reaches a shared or a private
stream.  The grid is the fingerprint grid: every Guild at the levels and seeds
of ``FINGERPRINT_LEVELS`` and ``FINGERPRINT_SEEDS``.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from collections import Counter
from collections import defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(
        __file__
        ).resolve().parent.parent
if str(
        PROJECT_ROOT
        ) not in sys.path:
    sys.path.insert(
            0,
            str(
                    PROJECT_ROOT
                    ),
            )
if str(
        PROJECT_ROOT / "scripts"
        ) not in sys.path:
    sys.path.insert(
            0,
            str(
                    PROJECT_ROOT / "scripts"
                    ),
            )

from verify_fingerprint import Grid_Levels  # noqa: E402
from verify_fingerprint import Grid_Seeds  # noqa: E402
from verify_fingerprint import hush  # noqa: E402


# ---------------------------------------------------------------------------
# What the rite records
# ---------------------------------------------------------------------------


class Ledger:
    """Everything the grid drew, and who asked for it."""

    def __init__(
            ledger,
            ) -> None:
        ledger.purposes: Counter = Counter()
            #-- purpose -> how many Dice Bags were opened with it
        ledger.purpose_callers: dict[str, str] = {}
            #-- purpose -> the first site that opened it
        ledger.purpose_keys: dict[str, set[tuple[str, str]]] = defaultdict(
                set
                )
            #-- purpose -> the (version, namespace) pairs it was opened with
        ledger.shared: Counter = Counter()
            #-- "random.choice @ file:line" -> calls to a shared stream
        ledger.private: Counter = Counter()
            #-- "file:line" -> random.Random( ... ) opened outside Dice_Bag
        ledger.characters = 0


SHARED_FUNCTIONS = (
        "random",
        "choice",
        "choices",
        "sample",
        "shuffle",
        "randint",
        "randrange",
        "uniform",
        "gauss",
        "getrandbits",
        "triangular",
        )

OWN_FILES = (
        "CharactersKit.py",
        "verify_dice_purposes.py",
        )


def Caller_Site(
        skip_files: tuple[str, ...],
        ) -> str:
    """The first frame on the stack that is not one of the given files."""
    frame = sys._getframe(
            1
            )
    while frame is not None:
        name = frame.f_code.co_filename
        if not any(
                name.endswith(
                        skipped
                        )
                for skipped in skip_files
                ) and "random.py" not in name:
            try:
                shown = str(
                        Path(
                                name
                                ).resolve().relative_to(
                                PROJECT_ROOT
                                )
                        )
            except ValueError:
                shown = name
            return f"{shown}:{frame.f_lineno}"
        frame = frame.f_back
    return "?"


def Is_Derived(
        purpose: str,
        ) -> bool:
    """A purpose built from a stack frame, not written by a Tag."""
    return "#" in purpose or purpose.startswith(
            (
                    "Atlas",
                    "app.",
                    )
            )


# ---------------------------------------------------------------------------
# The watchers
# ---------------------------------------------------------------------------


def Watch_Dice_Bags(
        ledger: Ledger,
        ) -> None:
    """Record every Dice Bag a Character opens."""
    from AtlasActorLudi.CharactersKit import Character

    original = Character.Dice_Bag

    def Recording_Dice_Bag(
            char,
            purpose,
            *,
            version="1",
            namespace="GenLegend",
            ):
        shown = str(
                purpose
                ).strip()
        ledger.purposes[
                shown
                ] += 1
        ledger.purpose_keys[
                shown
                ].add(
                (
                        str(
                                version
                                ),
                        str(
                                namespace
                                ),
                        )
                )
        if shown not in ledger.purpose_callers:
            ledger.purpose_callers[
                    shown
                    ] = Caller_Site(
                    OWN_FILES
                    )
        return original(
                char,
                purpose,
                version=version,
                namespace=namespace,
                )

    Character.Dice_Bag = Recording_Dice_Bag


def Watch_Shared_Streams(
        ledger: Ledger,
        ) -> None:
    """Count every call to the shared streams, by the site that made it."""
    import app.random as app_random

    for module, label in (
            (
                    random,
                    "random",
                    ),
            (
                    app_random,
                    "app.random",
                    ),
            ):
        for name in SHARED_FUNCTIONS:
            function = getattr(
                    module,
                    name,
                    None,
                    )
            if function is None:
                continue

            def Counting(
                    *arguments,
                    _function=function,
                    _label=f"{label}.{name}",
                    **keywords,
                    ):
                ledger.shared[
                        f"{_label} @ {Caller_Site( OWN_FILES )}"
                        ] += 1
                return _function(
                        *arguments,
                        **keywords,
                        )

            setattr(
                    module,
                    name,
                    Counting,
                    )


def Watch_Private_Streams(
        ledger: Ledger,
        ) -> None:
    """Record every random.Random opened outside Character.Dice_Bag."""
    base = random.Random

    class Recording_Random(
            base
            ):
        def __init__(
                stream,
                seed=None,
                ):
            site = Caller_Site(
                    (
                            "verify_dice_purposes.py",
                            )
                    )
            if not site.endswith(
                    "CharactersKit.py"
                    ) and "CharactersKit.py:" not in site:
                ledger.private[
                        site
                        ] += 1
            super().__init__(
                    seed
                    )

    random.Random = Recording_Random


# ---------------------------------------------------------------------------
# The grid
# ---------------------------------------------------------------------------


def Summon_Grid(
        ledger: Ledger,
        ) -> None:
    """Summon every Guild at every level for every seed, watched."""
    from AtlasActorLudi.Map_of_Character_Generation import summon_player
    from AtlasLusoris.GuildKit import GUILDS

    for guild in sorted(
            GUILDS
            ):
        for level in Grid_Levels():
            for seed in Grid_Seeds():
                with hush():
                    summon_player(
                            seed=seed,
                            level=level,
                            guild=guild,
                            )
                ledger.characters += 1


# ---------------------------------------------------------------------------
# What the rite says
# ---------------------------------------------------------------------------


def Report(
        ledger: Ledger,
        ) -> None:
    derived = sorted(
            purpose
            for purpose in ledger.purposes
            if Is_Derived(
                    purpose
                    )
            )
    named = sorted(
            purpose
            for purpose in ledger.purposes
            if not Is_Derived(
                    purpose
                    )
            )
    print(
            f"{ledger.characters} Characters; "
            f"{sum( ledger.purposes.values() )} Dice Bags opened; "
            f"{len( named )} named purposes; {len( derived )} derived purposes; "
            f"{sum( ledger.shared.values() )} shared-stream calls from "
            f"{len( ledger.shared )} sites; "
            f"{sum( ledger.private.values() )} private streams from "
            f"{len( ledger.private )} sites."
            )
    print(
            "\n== named purposes (purpose | bags | version, namespace | first site)"
            )
    for purpose in named:
        keys = "; ".join(
                f"{version}, {namespace}"
                for version, namespace in sorted(
                        ledger.purpose_keys[
                                purpose
                                ]
                        )
                )
        print(
                f"  {purpose} | {ledger.purposes[ purpose ]} | {keys} | "
                f"{ledger.purpose_callers[ purpose ]}"
                )
    print(
            "\n== derived purposes (a frame, not a Tag)"
            )
    for purpose in derived:
        print(
                f"  {purpose} | {ledger.purposes[ purpose ]} | "
                f"{ledger.purpose_callers[ purpose ]}"
                )
    print(
            "\n== shared-stream calls (function @ site | calls)"
            )
    for site, calls in sorted(
            ledger.shared.items()
            ):
        print(
                f"  {site} | {calls}"
                )
    print(
            "\n== private streams (site | opened)"
            )
    for site, opened in sorted(
            ledger.private.items()
            ):
        print(
                f"  {site} | {opened}"
                )


def Manifest(
        ledger: Ledger,
        ) -> list[str]:
    """The purposes the grid opened, one per line, sorted."""
    return sorted(
            ledger.purposes
            )


def Save(
        ledger: Ledger,
        path: Path,
        ) -> int:
    lines = Manifest(
            ledger
            )
    path.write_text(
            "\n".join(
                    lines
                    ) + "\n",
            encoding="utf-8",
            )
    print(
            f"Saved {len( lines )} purposes to {path}"
            )
    return 0


def Check(
        ledger: Ledger,
        path: Path,
        ) -> int:
    """Fail on an undeclared purpose, a derived purpose, or a stray stream."""
    declared = set(
            line.strip()
            for line in path.read_text(
                    encoding="utf-8",
                    ).splitlines()
            if line.strip()
            )
    families = tuple(
            line[:-1]
            for line in declared
            if line.endswith(
                    ".*"
                    )
            )
        #-- A line ``gear.title.*`` declares a family: every purpose under
        #-- that prefix, for the choices keyed by a thing's name (an item).
    opened = set(
            Manifest(
                    ledger
                    )
            )
    failures: list[str] = []
    for purpose in sorted(
            opened - declared
            ):
        if purpose.startswith(
                families
                ):
            continue
        failures.append(
                f"undeclared purpose: {purpose} "
                f"(first at {ledger.purpose_callers[ purpose ]})"
                )
    unopened = []
    for purpose in sorted(
            declared - opened
            ):
        if purpose.endswith(
                ".*"
                ) and any(
                opened_purpose.startswith(
                        purpose[:-1]
                        )
                for opened_purpose in opened
                ):
            continue
        unopened.append(
                purpose
                )
            #-- a narrower grid opens fewer purposes than the wide one the
            #-- manifest was saved on: noted, not failed (QST-0144.6)
    for purpose in sorted(
            opened
            ):
        if Is_Derived(
                purpose
                ):
            failures.append(
                    f"derived purpose: {purpose} "
                    f"(at {ledger.purpose_callers[ purpose ]})"
                    )
        if len(
                ledger.purpose_keys[
                        purpose
                        ]
                ) > 1:
            failures.append(
                    f"one purpose, several keys: {purpose} "
                    f"{sorted( ledger.purpose_keys[ purpose ] )}"
                    )
    for site, calls in sorted(
            ledger.shared.items()
            ):
        failures.append(
                f"shared stream reached: {site} ({calls} calls)"
                )
    for site, opened_count in sorted(
            ledger.private.items()
            ):
        failures.append(
                f"private stream opened: {site} ({opened_count})"
                )
    if unopened:
        print(
                f"note: {len( unopened )} declared purposes never opened on this "
                f"grid (saved on the wide grid): {', '.join( unopened )}"
                )
    if failures:
        print(
                f"FAIL — {len( failures )} findings on {ledger.characters} Characters:"
                )
        for line in failures:
            print(
                    f"  ! {line}"
                    )
        return 1
    print(
            f"OK — {ledger.characters} Characters opened only the "
            f"{len( declared )} declared purposes, no derived purpose, "
            "no shared or private stream."
            )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
            description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            )
    group = parser.add_mutually_exclusive_group(
            required=True,
            )
    group.add_argument(
            "--report",
            action="store_true",
            help="list what the grid opened; never fails",
            )
    group.add_argument(
            "--save",
            type=Path,
            help="write the manifest of purposes",
            )
    group.add_argument(
            "--check",
            type=Path,
            help="compare against a manifest; fail on any stray draw",
            )
    arguments = parser.parse_args()

    ledger = Ledger()
    Watch_Dice_Bags(
            ledger
            )
    Watch_Shared_Streams(
            ledger
            )
    Watch_Private_Streams(
            ledger
            )
    Summon_Grid(
            ledger
            )

    if arguments.report:
        Report(
                ledger
                )
        return 0
    if arguments.save is not None:
        return Save(
                ledger,
                arguments.save,
                )
    return Check(
            ledger,
            arguments.check,
            )


if __name__ == "__main__":
    raise SystemExit(
            main()
            )
