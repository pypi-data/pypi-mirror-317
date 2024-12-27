#!/usr/bin/env python3

# Copyright 2023 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Simulation du nombre de cartes à acheter pour compléter plusieurs albums, avec échanges."""

import argparse
import sys
import textwrap

from . import simule


def analyse():
    """Renvoit un analyseur de ligne de commande."""
    parser = argparse.ArgumentParser(
        prog="panini",
        description=textwrap.dedent(
            "Simule l'achat de cartes jusqu'à obtention de plusieurs albums complets."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Remarquez bien que le programme calcule et affiche le nombre moyen de *cartes* achetées par album (c'est-à-dire le nombre de paquet multiplié par le nombre de cartes par paquet, divisé par le nombre d'albums).
        """.strip(),
    )
    parser.add_argument(
        "album",
        metavar="ALBUM",
        type=int,
        help="Nombre de cartes par album.",
    )
    parser.add_argument(
        "paquet",
        metavar="PAQUET",
        type=int,
        help="Nombre de cartes par paquet.",
    )
    parser.add_argument(
        "amis",
        metavar="AMIS",
        type=int,
        help="Nombre d'albums à compléter",
    )
    parser.add_argument(
        "simulations",
        metavar="SIMULATIONS",
        type=int,
        nargs="?",
        default=1,
        help="Nombre de simulations à effectuer",
    )

    return parser


def main():
    """Fonction principale."""
    options = analyse().parse_args()
    if (
        options.album <= 0
        or options.paquet <= 0
        or options.simulations <= 0
        or options.amis <= 0
    ):
        print(
            """Les quatre options doivent être des nombres entiers strictement positifs."""
        )
        sys.exit(1)
    for _ in range(options.simulations):
        print(
            options.paquet
            * simule(options.album, options.paquet, options.amis)
            / options.amis
        )


if __name__ == "__main__":
    main()
