#!/usr/bin/env python3

# Copyright 2024 Louis Paternault
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

"""Calcul du nombre de chemins possibles aux jeux *Ma Première Aventure*."""

import textwrap

import argdispatch

from . import VERSION
from .commandes import fins, graphe, histoires, proba, victoires


def analyse():
    """Renvoit un analyseur de ligne de commande."""
    parser = argdispatch.ArgumentParser(
        prog="mpa",
        description=textwrap.dedent(
            "Calcule le nombre de chemins possibles aux jeux *Ma Première Aventure*."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    subparsers = parser.add_subparsers(dest="commande")
    subparsers.required = True

    subparsers.add_function(fins.main, command="fins")
    subparsers.add_function(graphe.main, command="graphe")
    subparsers.add_function(histoires.main, command="histoires")
    subparsers.add_function(proba.main, command="proba")
    subparsers.add_function(victoires.main, command="victoires")

    return parser


def main():
    """Fonction principale."""
    analyse().parse_args()


if __name__ == "__main__":
    main()
