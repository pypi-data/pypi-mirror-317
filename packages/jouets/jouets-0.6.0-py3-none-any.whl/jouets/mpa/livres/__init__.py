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

"""Définit les différents livres pouvant être étudiés."""

import argparse
import sys

from ...utils import plugins
from . import dragon


def charge_livres():
    """Renvoit le dictionnaire des livres définis dans les sous-modules."""
    livres = {}
    for module in plugins.iter_modules(sys.modules[__package__]):
        try:
            for nom, livre in getattr(module, "LIVRES").items():
                if nom in livres:
                    # pylint: disable=line-too-long
                    print(
                        f"""Avertissement: Livre "{ nom }" (module { module.__name__}) ignoré, car un livre du même nom existe déjà.""",
                        file=sys.stderr,
                    )
                    continue
                livres[nom] = livre
        except AttributeError:
            pass
    return livres


LIVRES = charge_livres()


def analyseur():
    """Renvoit un analyseur syntaxique permettant de choisir un des livres."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("livre", choices=LIVRES.keys())
    return parser
