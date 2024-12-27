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

"""Calcule et affiche l'ensemble des fins possibles."""

import argparse

from .. import livres
from ..graphe import Histoire


def main(args):
    """Calcule et affiche l'ensemble des fins possibles."""
    parser = argparse.ArgumentParser(
        description="Affiche toutes les fins possibles",
        parents=[livres.analyseur()],
    )
    print(
        "\n".join(sorted(Histoire(livres.LIVRES[parser.parse_args(args).livre]).fins()))
    )
