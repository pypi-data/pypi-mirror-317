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

"""Calcule et affiche les probabilités de victoire, semi-victorie, défaite."""

import argparse
import re

from .. import livres
from ..graphe import Histoire


def _type_histoire(text):
    """Convertit une "histoire" en liste de choix.

    >>> _type_histoire("PlH2M1B1")
    ["Pl", "H", "2", "M", "1", "B", "1"]

    Attention : Cette fonction ne fonctionne pas avec les caractères non ASCII.
    """
    return re.findall("[A-Z0-9][a-z]*", text)


def main(args):
    """Calcule et affiche les probabilités de victoire, semi-victorie, défaite."""
    parser = argparse.ArgumentParser(
        description="Calcule les probabilités de victoire des livres",
        parents=[livres.analyseur()],
    )
    parser.add_argument(
        "--préfixe",
        "-p",
        type=_type_histoire,
        default="",
        help="Ne considère que les histoires commençant par ce préfixe.",
    )
    options = parser.parse_args(args)
    début = Histoire(livres.LIVRES[options.livre])
    for fin in sorted(début.fins()):
        print(f"Probabilité de {fin} :", début.proba(fin, préfixe=options.préfixe))
