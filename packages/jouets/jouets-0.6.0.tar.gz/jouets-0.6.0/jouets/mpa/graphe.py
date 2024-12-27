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

"""Outils permettant de définir le graphe correspondant à toutes les histoires possibles."""

from __future__ import annotations

import dataclasses
import operator
import statistics
import types
import typing
from collections.abc import Collection
from numbers import Number

################################################################################


class _Effet:
    def __call__(self, histoire: Histoire):
        raise NotImplementedError

    @property
    def txt(self):
        """Renvoit une version « pour humain » de l'effet."""
        raise NotImplementedError


@dataclasses.dataclass(init=False)
class EffetAffecte(_Effet):
    """Affecte des choses aux roues.

    Par exemple, `EffetAffecte(bleu="marteau")` ajoute un marteau à la roue bleue.
    """

    roues: dict

    def __init__(self, **kwargs):
        self.roues = kwargs

    def __call__(self, histoire: Histoire):
        histoire.roues.update(self.roues)
        return histoire

    @property
    def txt(self):
        return "\n".join(
            f"{couleur}={valeur}" for couleur, valeur in self.roues.items()
        )


@dataclasses.dataclass(init=False)
class EffetAffecteSiVide(_Effet):
    """Affecte des choses aux roues, si elles sont vides.

    Par exemple, `EffetAffecteSiVide(bleu="marteau")` ajoute un marteau à la roue bleue,
    si la roue ne contenait rien (clef absente du dictionnaire, ou valeur égale à None).
    """

    roues: dict

    def __init__(self, **kwargs):
        self.roues = kwargs

    def __call__(self, histoire: Histoire):
        for clef, valeur in self.roues.items():
            if histoire.roues.get(clef, None) is None:
                histoire.roues[clef] = valeur
        return histoire

    @property
    def txt(self):
        return "\n".join(
            f"{couleur}={valeur} (si vide)" for couleur, valeur in self.roues.items()
        )


class EffetRien(_Effet):
    """Ne fait rien."""

    def __call__(self, histoire: Histoire):
        return histoire

    @property
    def txt(self):
        return ""


@dataclasses.dataclass(init=False)
class EffetAjoute(_Effet):
    """Ajoute une valeur à une des roues."""

    ajouts: dict

    def __init__(self, **kwargs):
        self.ajouts = kwargs

    def __call__(self, histoire: Histoire):
        for couleur, valeur in self.ajouts.items():
            histoire.roues[couleur] += valeur
        return histoire

    @property
    def txt(self):
        return "\n".join(
            f"{couleur} + {valeur}" if valeur > 0 else f"{couleur} - {abs(valeur)}"
            for couleur, valeur in self.ajouts.items()
        )


@dataclasses.dataclass(init=False)
class EffetEt(_Effet):
    """Applique plusieurs effets."""

    effets: Collection[_Effet]

    def __init__(self, *args):
        self.effets = args

    def __call__(self, histoire: Histoire):
        for effet in self.effets:
            histoire = effet(histoire)
        return histoire

    @property
    def txt(self):
        return "\n".join(effet.txt for effet in self.effets)


#: Effets pouvant être appliqués.
#:
#: .. autoclass:: EffetAffecte
#: .. autoclass:: EffetAffecteSiVide
#: .. autoclass:: EffetAjoute
#: .. autoclass:: EffetRien
#: .. autoclass:: EffetEt
Effet = types.SimpleNamespace(
    rien=EffetRien,
    ajoute=EffetAjoute,
    affecte=EffetAffecte,
    affecteSiVide=EffetAffecteSiVide,
    et=EffetEt,
)

################################################################################


class _Condition:
    def __call__(self, histoire):
        raise NotImplementedError

    @property
    def txt(self):
        """Renvoit une version « pour humain » de la condition."""
        raise NotImplementedError


class ConditionVrai(_Condition):
    """Cette condition est toujours vérifiée."""

    def __call__(self, histoire):
        return True

    @property
    def txt(self):
        return "Vrai"


@dataclasses.dataclass
class ConditionCompte(_Condition):
    """Le nombre de roues ayant une certaine valeur est comprise dans l'intervalle.

    Par exemple, ``Condition.compte("bobo", inf=2)`` signifie
    qu'au moins deux roues ont la valeur ``"bobo"``.
    """

    valeur: str
    inf: Number = float("-inf")
    sup: Number = float("inf")

    def __call__(self, histoire):
        return (
            self.inf
            <= operator.countOf(histoire.roues.values(), self.valeur)
            <= self.sup
        )

    @property
    def txt(self):
        if self.inf == float("-inf") and self.sup == float("inf"):
            return "Vrai"
        if self.inf == float("-inf"):
            return f"{self.valeur} \u2264 {self.sup}"
        if self.sup == float("inf"):
            return f"{self.inf} \u2264 {self.valeur}"
        return f"{self.inf} \u2264 {self.valeur} \u2264 {self.sup}"


@dataclasses.dataclass(init=False)
class ConditionOu(_Condition):
    """L'une des conditions données en argument est vérifiée."""

    conditions: Collection[_Condition]

    def __init__(self, *args):
        self.conditions = args

    def __call__(self, histoire):
        return any(condition(histoire) for condition in self.conditions)

    @property
    def txt(self):
        return "\nou\n".join(f"({condition.txt})" for condition in self.conditions)


@dataclasses.dataclass(init=False)
class ConditionEt(_Condition):
    """Toutes les conditions données en argument sont vérifiées."""

    conditions: Collection[_Condition]

    def __init__(self, *args):
        self.conditions = args

    def __call__(self, histoire):
        return all(condition(histoire) for condition in self.conditions)

    @property
    def txt(self):
        return "\net\n".join(f"({condition.txt})" for condition in self.conditions)


@dataclasses.dataclass(init=False)
class ConditionRoue(_Condition):
    """Les roues contiennent tous les objets donnés en argument.

    Par exemple, ``_Condition.roue(jaune="chaussons", rouge="Lina")`` vérifie que
    - les chaussons sont sur la roue jaune, et
    - le personnage de la roue rouge est Lina.
    """

    roues: dict

    def __init__(self, **kwargs):
        self.roues = kwargs

    def __call__(self, histoire):
        for key, value in self.roues.items():
            try:
                if histoire.roues[key] != value:
                    return False
            except KeyError:
                return False
        return True

    @property
    def txt(self):
        return " et ".join(
            f"{couleur}={valeur}" for couleur, valeur in self.roues.items()
        )


@dataclasses.dataclass
class ConditionNon(_Condition):
    """Vérifie que la condition n'est pas satisfaite."""

    condition: _Condition

    def __call__(self, histoire):
        return not self.condition(histoire)

    @property
    def txt(self):
        return "NON(\n" + self.condition.txt + "\n)"


@dataclasses.dataclass
class ConditionIntervalle(_Condition):
    """Vérifie que la valeur d'une roue est comprise dans l'intervalle donné"""

    roue: str
    inf: float = -float("inf")
    sup: float = float("inf")

    def __call__(self, histoire):
        return self.inf <= histoire.roues[self.roue] <= self.sup

    @property
    def txt(self):
        if self.inf == float("-inf") and self.sup == float("inf"):
            return "Vrai"
        if self.inf == float("-inf"):
            return f"{self.roue} \u2264 {self.sup}"
        if self.sup == float("inf"):
            return f"{self.inf} \u2264 {self.roue}"
        return f"{self.inf} \u2264 {self.roue} \u2264 {self.sup}"


#: Conditions à vérifier pour être autorisé·e à faire ce choix
#:
#: .. autoclass:: ConditionCompte
#: .. autoclass:: ConditionNon
#: .. autoclass:: ConditionOu
#: .. autoclass:: ConditionEt
#: .. autoclass:: ConditionRoue
#: .. autoclass:: ConditionVrai
#: .. autoclass:: ConditionIntervalle
Condition = types.SimpleNamespace(
    compte=ConditionCompte,
    non=ConditionNon,
    ou=ConditionOu,
    et=ConditionEt,
    roue=ConditionRoue,
    vrai=ConditionVrai,
    intervalle=ConditionIntervalle,
)


################################################################################

ROUES = {
    "rouge": None,
    "vert": None,
    "bleu": None,
    "jaune": None,
}


@dataclasses.dataclass
class Page:
    """Une page, qui contient plusieurs choix."""

    #: Liste des choix possibles
    choix: Collection[Choix] = dataclasses.field(default_factory=list)

    #: Si ``None``, le livre n'est pas terminé.
    #: Sinon, indique la fin (victoire, défaite, ni l'une ni l'autre).
    fin: typing.Optionnal[str] = None

    #: Éventuelles valeurs de départ pour les roues.
    #: Cela n'a de sens que pour le début du livre.
    roues: typing.Optionnal[dict] = dataclasses.field(default_factory=ROUES.copy)

    #: Éventuelles descriptions pour les codes
    descriptions: dict = dataclasses.field(default_factory=dict)

    def iter_pages(self, *, fait: set = None):
        """Itère sur l'ensemble des pages de l'histoire.

        :param set fait: Ensemble des pages déjà renvoyées (qui ne le seront pas à nouveau)
        """
        if fait is None:
            fait = set()
        yield self
        fait.add(id(self))
        for choix in self.choix:
            if choix.cible and id(choix.cible) not in fait:
                yield from choix.cible.iter_pages(fait=fait)


@dataclasses.dataclass
class Choix:
    """Une alternative possible lors d'un choix"""

    #: Code qui sera utilisé pour ce choix lorsque les histoires seront affichées.
    code: str

    #: Page à laquelle on va si on fait ce choix.
    cible: Page

    #: Condition pour pouvoir faire ce choix. Par défaut, aucune condition n'est requise.
    condition: typing.Callable = Condition.vrai()

    #: Effet si ce choix est effectué. C'est un des attributs de :data:`Effet`.
    #: Par exemple, ``effet = Effet.affecte(vert="bouclier")`` signifie :
    #: « Mettre le bouclier sur la roue verte ».
    effet: typing.Callable = Effet.rien()

    def __repr__(self):
        #  pylint: disable=line-too-long
        return f"{ self.__class__.__name__}(code={ self.code }, cible=< {self.cible.__class__.__name__} at { hex(id(self.cible)) }>, condition={ self.condition }, effet={ self.effet })"

    def est_direct(self):
        """Renvoit True si la condition n'a ni condition, ni effet."""
        return isinstance(self.effet, EffetRien) and isinstance(
            self.condition, ConditionVrai
        )


class Histoire:
    """Un récit d'une histoire"""

    def __init__(self, début, *, roues=None, codes=None):
        if isinstance(début, list):
            self.passé = début
        else:
            self.passé = [début]
        if roues is None:
            self.roues = début.roues
        else:
            self.roues = roues
        if codes is None:
            self.codes = []
        else:
            self.codes = codes

    @property
    def page(self):
        """Renvoit la page actuelle, c'est-à-dire la dernière page visitée."""
        return self.passé[-1]

    def applique(self, choix):
        """Applique le choix, et renvoit le nouvel objet :class:`Histoire`."""
        return choix.effet(
            self.__class__(
                self.passé + [choix.cible],
                roues=self.roues.copy(),
                codes=self.codes + [choix.code],
            )
        )

    def suivantes(self, *, préfixe=None, condition=False):
        """Itère l'étape suivantes des histoires

        - N'effectue que les choix possibles
        - Applique les effets
        - Ne fait qu'un seul choix
          (des appels récursifs à cette fonction sont nécessaires pour continuer à avancer).

        :param bool condition: Si vrai, itère des tuples `(Histoire,
            Condition)` où `Histoire` est l'histoire suivante, et `Condition`
            est la condition qui a été vérifiée pour mener à cette histoire.
            Sinon, n'itère que les histoires.
        :param typing.Conditionnal[list[str]] préfixe: Éventuelle liste des
            choix déjà faits (les autres choix sont ignorés).
        """
        if préfixe is None:
            préfixe = []
        for choix in self.page.choix:
            if préfixe and choix.code != préfixe[0]:
                continue
            if choix.cible in self.passé:
                continue
            if choix.condition(self):
                suivant = self.applique(choix)
                if condition:
                    yield (suivant, choix.condition)
                else:
                    yield suivant

    def fins(self):
        """Renvoie sur toutes les fins possibles"""
        if self.page.fin is not None:
            return {self.page.fin}
        # Itère sur les fins des (potentielles) histoires suivantes, en ignorant les conditions
        return set.union(
            *(
                self.applique(choix).fins()
                for choix in self.page.choix
                if choix.cible not in self.passé
            )
        )

    def histoires(self):
        """Itère sur toutes les histoires possibles."""
        if self.page.choix:
            for histoire in self.suivantes():
                yield from histoire.histoires()
        else:
            yield self

    def proba(self, fin: str, préfixe: typing.Optionnal(list[str]) = None):
        """Calcule la probabilité d'obtenir la fin donnée en argument."""
        if préfixe is None:
            préfixe = []
        if self.page.fin is not None:
            # C'est une page finale
            if self.page.fin == fin:
                return 1
            return 0
        # Ce n'est pas une page finale :
        # Calcule la moyenne des probabilités de de victoire pour chacun des choix.
        try:
            return statistics.mean(
                histoire.proba(fin, préfixe=préfixe[1:] if préfixe else None)
                for histoire in self.suivantes(préfixe=préfixe)
            )
        except statistics.StatisticsError:
            # Aucune histoire avec ce préfixe
            return 0
