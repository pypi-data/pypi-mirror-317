# Copyright 2023 Louis Paternault
#
# This file is part of Jouets.
#
# Jouets is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Jouets is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with Jouets.  If not, see <http://www.gnu.org/licenses/>.

"""Simulation d'achats de paquets de cartes Panini"""

import itertools
import random


def simule(album, paquet):  # pylint: disable=inconsistent-return-statements
    """Simule l'achat de paquets de cartes jusqu'à obtention du paquet complet.

    :param int album: Nombre total de cartes dans l'album.
    :param int paquet: Nombre de cartes par paquet acheté.
    :return: Nombre de *paquets* achetés.
    """
    manquantes = album
    for essais in itertools.count(1):
        manquantes -= sum(
            1 for carte in random.sample(range(album), k=paquet) if carte < manquantes
        )
        if not manquantes:
            return essais
