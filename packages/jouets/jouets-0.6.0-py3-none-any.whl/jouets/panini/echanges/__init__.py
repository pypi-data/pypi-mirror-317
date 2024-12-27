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

"""Simulation d'achats de paquets de cartes Panini, avec échanges"""

import collections
import itertools
import random


def simule(album, paquet, amis):  # pylint: disable=inconsistent-return-statements
    """Simule l'achat de cartes pour compléter plusieurs albums.

    :param int album: Nombre total de cartes dans l'album.
    :param int paquet: Nombre de cartes par paquet acheté.
    :param int amis: Nombre d'albums à compléter.
    :return: Nombre moyen de *paquets* achetés par album, c'est à dire :
        (nombre de paquets achetés) * (nombre de cartes par paquet) / (nombre d'amis)
    """
    manquantes = collections.Counter({carte: amis for carte in range(album)})

    for achats in itertools.count(0):
        if manquantes.total() == 0:
            return achats

        # Simule un tirage
        manquantes -= collections.Counter(random.sample(range(album), k=paquet))
        # Supprime les valeurs négatives
        # pylint: disable=pointless-statement
        +manquantes
