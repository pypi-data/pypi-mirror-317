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

"""Calcul du nombre d'histoires possibles au jeu *La Découverte de l'Atlantide*.

https://ma-premiere-aventure.fr/livres/la-decouverte-de-latlantide
"""

from ..graphe import Choix, Condition, Effet, Page

pageDansLeTrésor = Page()
pageFin = Page()
pageDèsQueTuEs = Page()
pageLaBouéeIncorporée = Page()

pageTonSousMarinEstIntact = Page(
    fin="victoire",
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="pinces"),
            cible=pageDansLeTrésor,
        ),
        Choix(
            code="0",
            condition=Condition.non(Condition.roue(vert="pinces")),
            cible=pageFin,
        ),
    ),
)

pageOhNonLeSousMarin = Page(
    fin="défaite",
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Manta"),
            cible=pageDèsQueTuEs,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Manta")),
            cible=pageLaBouéeIncorporée,
        ),
    ),
)
pageTonSousMarinEstEnPiteuxÉtat = Page(fin="bof")

pageTuFranchisEnfin = Page(
    choix=(
        Choix(
            code="H",
            condition=Condition.compte(valeur="fuite", sup=0),
            cible=pageTonSousMarinEstIntact,
        ),
        Choix(
            code="M",
            condition=Condition.compte(valeur="fuite", inf=1, sup=2),
            cible=pageTonSousMarinEstEnPiteuxÉtat,
        ),
        Choix(
            code="B",
            condition=Condition.compte(valeur="fuite", inf=3),
            cible=pageOhNonLeSousMarin,
        ),
    ),
)

pageTuMetsLesGazAlorsQue = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(bleu="queue"), Condition.roue(rouge="Espadon")
            ),
            cible=pageTuFranchisEnfin,
        ),
        Choix(
            code="2",
            cible=pageTuFranchisEnfin,
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(bleu="queue"), Condition.roue(rouge="Espadon")
                )
            ),
            effet=Effet.affecte(bleu="fuite"),
        ),
    ),
)

pageTuAllumesTesLampes = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="lanterne"),
            cible=pageTuFranchisEnfin,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="lanterne")),
            cible=pageTuFranchisEnfin,
            effet=Effet.affecte(bleu="fuite"),
        ),
    ),
)

pageTuFoncesVers = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="encre"),
            cible=pageTuFranchisEnfin,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="encre")),
            cible=pageTuFranchisEnfin,
            effet=Effet.affecte(bleu="fuite"),
        ),
    ),
)

pageLesPremiersBâtiments = Page(
    choix=(
        Choix(
            code="H",
            cible=pageTuMetsLesGazAlorsQue,
        ),
        Choix(
            code="M",
            cible=pageTuAllumesTesLampes,
        ),
        Choix(
            code="B",
            cible=pageTuFoncesVers,
        ),
    )
)

pageLesTentacules = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="répulseur"),
            cible=pageLesPremiersBâtiments,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="répulseur")),
            effet=Effet.affecte(jaune="fuite"),
            cible=pageLesPremiersBâtiments,
        ),
    )
)

pageTuMetsLesGazEtVises = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(jaune="rostre"),
            cible=pageLesPremiersBâtiments,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(jaune="rostre")),
            effet=Effet.affecte(jaune="fuite"),
            cible=pageLesPremiersBâtiments,
        ),
    )
)

pageTuCommencesÀManœuvrer = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(jaune="nageoires"),
                Condition.roue(rouge="Manta"),
            ),
            cible=pageLesPremiersBâtiments,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(jaune="nageoires"),
                    Condition.roue(rouge="Manta"),
                )
            ),
            effet=Effet.affecte(jaune="fuite"),
            cible=pageLesPremiersBâtiments,
        ),
    )
)

pageAaaaahCEstLeKraken = Page(
    choix=(
        Choix(
            code="H",
            cible=pageLesTentacules,
        ),
        Choix(
            code="M",
            cible=pageTuMetsLesGazEtVises,
        ),
        Choix(
            code="B",
            cible=pageTuCommencesÀManœuvrer,
        ),
    )
)

pageTuTeGlisses = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="pinces"),
            cible=pageAaaaahCEstLeKraken,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="pinces")),
            effet=Effet.affecte(vert="fuite"),
            cible=pageAaaaahCEstLeKraken,
        ),
    )
)

pageTuGlissesDeDune = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="camouflage"),
            cible=pageAaaaahCEstLeKraken,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="camouflage")),
            effet=Effet.affecte(vert="fuite"),
            cible=pageAaaaahCEstLeKraken,
        ),
    )
)

pageTuEntresDansLaZone = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(vert="carapace"), Condition.roue(rouge="Béhémoth")
            ),
            cible=pageAaaaahCEstLeKraken,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(vert="carapace"), Condition.roue(rouge="Béhémoth")
                )
            ),
            effet=Effet.affecte(vert="fuite"),
            cible=pageAaaaahCEstLeKraken,
        ),
    )
)

pageVoilàLesPremièresTraces = Page(
    choix=(
        Choix(
            code="H",
            cible=pageTuTeGlisses,
        ),
        Choix(
            code="M",
            cible=pageTuGlissesDeDune,
        ),
        Choix(
            code="B",
            cible=pageTuEntresDansLaZone,
        ),
    )
)

pageTuVoyagesEnSurface = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Espadon"),
            cible=pageVoilàLesPremièresTraces,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Espadon")),
            effet=Effet.affecte(bleu="queue"),
            cible=pageVoilàLesPremièresTraces,
        ),
    )
)

pageTuAvancesDansLesEaux = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Espadon"),
            effet=Effet.affecte(bleu="encre"),
            cible=pageVoilàLesPremièresTraces,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Espadon")),
            cible=pageVoilàLesPremièresTraces,
        ),
    )
)

pageDansLesProfondeurs = Page(
    choix=(
        Choix(
            code="1",
            effet=Effet.affecte(bleu="lanterne"),
            cible=pageVoilàLesPremièresTraces,
        ),
        Choix(
            code="2",
            cible=pageVoilàLesPremièresTraces,
        ),
    )
)

pageEnfinTeVoilà = Page(
    choix=(
        Choix(code="H", cible=pageTuVoyagesEnSurface),
        Choix(code="M", cible=pageTuAvancesDansLesEaux),
        Choix(code="B", cible=pageDansLesProfondeurs),
    ),
)

pageTuPlongesAuMilieu = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Manta"),
            cible=pageEnfinTeVoilà,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Manta")),
            effet=Effet.affecte(jaune="nageoires"),
            cible=pageEnfinTeVoilà,
        ),
    )
)

pageTuApprochesDoucement = Page(
    choix=(
        Choix(code="1", cible=pageEnfinTeVoilà),
        Choix(
            code="2",
            effet=Effet.affecte(jaune="répulseur"),
            cible=pageEnfinTeVoilà,
        ),
    )
)

pageDansCetteCrique = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Manta"),
            effet=Effet.affecte(jaune="rostre"),
            cible=pageEnfinTeVoilà,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Manta")),
            cible=pageEnfinTeVoilà,
        ),
    )
)

pageAprèsAvoirLongé = Page(
    choix=(
        Choix(code="H", cible=pageTuPlongesAuMilieu),
        Choix(code="M", cible=pageTuApprochesDoucement),
        Choix(code="B", cible=pageDansCetteCrique),
    )
)

pageTuFermesLesÉcoutilles = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Béhémoth"),
            cible=pageAprèsAvoirLongé,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Béhémoth")),
            effet=Effet.affecte(vert="carapace"),
            cible=pageAprèsAvoirLongé,
        ),
    )
)

pageTonSousMarinGlisse = Page(
    choix=(
        Choix(code="1", cible=pageAprèsAvoirLongé),
        Choix(code="2", effet=Effet.affecte(vert="pinces"), cible=pageAprèsAvoirLongé),
    )
)

pageTuLarguesLesAmarres = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(rouge="Béhémoth"),
            effet=Effet.affecte(vert="camouflage"),
            cible=pageAprèsAvoirLongé,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(rouge="Béhémoth")),
            cible=pageAprèsAvoirLongé,
        ),
    )
)


pageÀBordDeTon = Page(
    choix=(
        Choix(code="H", cible=pageTuFermesLesÉcoutilles),
        Choix(code="M", cible=pageTonSousMarinGlisse),
        Choix(code="B", cible=pageTuLarguesLesAmarres),
    )
)

pageChoisisTonPersonnage = Page(
    choix=(
        Choix(code="Pe", effet=Effet.affecte(rouge="Espadon"), cible=pageÀBordDeTon),
        Choix(code="Pm", effet=Effet.affecte(rouge="Manta"), cible=pageÀBordDeTon),
        Choix(code="Pb", effet=Effet.affecte(rouge="Béhémoth"), cible=pageÀBordDeTon),
    ),
    descriptions={
        "": "La Découverte de l'Atlantide",
        "Pe": "Espadon",
        "Pm": "Manta",
        "Pb": "Béhémoth",
    },
)

LIVRES = {
    "atlantide": pageChoisisTonPersonnage,
}
