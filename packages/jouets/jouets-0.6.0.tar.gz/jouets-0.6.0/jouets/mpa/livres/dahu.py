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

"""Calcul du nombre d'histoires possibles aux jeux *Ma Première Aventure : Sur la piste du dahu*."""

from ..graphe import Choix, Condition, Effet, Page

pageEnAdmirantLePaysage1 = Page()
pageEnAdmirantLePaysage2 = Page()
pageTuAvaisToutPrévu = Page()
pageTuRedescends = Page()

pageVêtuDeTonManteau = Page(fin="victoire")
pageTuArrivesEnHaut = Page(
    fin="bof",
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="WillBarry"), Condition.roue(rouge="AïvyBarry")
            ),
            cible=pageEnAdmirantLePaysage1,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="WillBarry"), Condition.roue(rouge="AïvyBarry")
                )
            ),
            cible=pageEnAdmirantLePaysage2,
        ),
    ),
)

pageTuEsVraimentÉpuisé = Page(
    fin="défaite",
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="AïvyBarry"), Condition.roue(rouge="AïvyPérégrine")
            ),
            cible=pageTuAvaisToutPrévu,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="AïvyBarry"),
                    Condition.roue(rouge="AïvyPérégrine"),
                )
            ),
            cible=pageTuRedescends,
        ),
    ),
)

pageTuArrivesEnfin = Page(
    choix=(
        Choix(
            code="H",
            condition=Condition.et(
                Condition.roue(bleu="manteau", vert="chardon"),
                Condition.intervalle(roue="jaune", inf=4),
            ),
            cible=pageVêtuDeTonManteau,
        ),
        Choix(
            code="M",
            condition=Condition.et(
                Condition.non(Condition.roue(bleu="manteau", vert="chardon")),
                Condition.intervalle(roue="jaune", inf=4),
            ),
            cible=pageTuArrivesEnHaut,
        ),
        Choix(
            code="B",
            condition=Condition.intervalle(roue="jaune", sup=3),
            cible=pageTuEsVraimentÉpuisé,
        ),
    ),
)

pageTuPressesLePas = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="statuette"),
            cible=pageTuArrivesEnfin,
            effet=Effet.affecte(bleu="manteau"),
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="statuette")),
            cible=pageTuArrivesEnfin,
        ),
    ),
)

pageCEstUnVieux = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="fanions"),
            cible=pageTuArrivesEnfin,
            effet=Effet.affecte(bleu="manteau"),
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="fanions")),
            cible=pageTuArrivesEnfin,
        ),
    ),
)

pageLaPisteFaitDes = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(bleu="piolet"),
            cible=pageTuArrivesEnfin,
            effet=Effet.affecte(bleu="manteau"),
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(bleu="piolet")),
            cible=pageTuArrivesEnfin,
        ),
    ),
)

pageUneFoisDehors = Page(
    choix=(
        Choix(code="H", cible=pageTuPressesLePas),
        Choix(code="M", cible=pageCEstUnVieux),
        Choix(code="B", cible=pageLaPisteFaitDes),
    ),
)

pageTuDébouchesSurUne = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="WillBarry"), Condition.roue(rouge="AïvyBarry")
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageUneFoisDehors,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="WillBarry"), Condition.roue(rouge="AïvyBarry")
                )
            ),
            cible=pageUneFoisDehors,
        ),
    ),
)

pageBonSangIlFait = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="AïvyPérégrine"), Condition.roue(rouge="AïvyBarry")
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageUneFoisDehors,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="AïvyPérégrine"),
                    Condition.roue(rouge="AïvyBarry"),
                )
            ),
            cible=pageUneFoisDehors,
        ),
    ),
)

pageEncoreUneSéparation = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.intervalle(roue="jaune", inf=5),
            effet=Effet.affecte(bleu="statuette"),
            cible=pageUneFoisDehors,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.intervalle(roue="jaune", inf=5)),
            effet=Effet.ajoute(jaune=2),
            cible=pageUneFoisDehors,
        ),
    ),
)

pageEnFaisantLeTour = Page(
    choix=(
        Choix(code="H", cible=pageTuDébouchesSurUne),
        Choix(code="M", cible=pageBonSangIlFait),
        Choix(code="B", cible=pageEncoreUneSéparation),
    ),
)

pageCommentÊtreCertain = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="corne"),
            effet=Effet.affecte(vert="chardon"),
            cible=pageEnFaisantLeTour,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="corne")),
            cible=pageEnFaisantLeTour,
        ),
    )
)

pageIciLesBonnesCachettes = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="camouflage"),
            effet=Effet.affecte(vert="chardon"),
            cible=pageEnFaisantLeTour,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="camouflage")),
            cible=pageEnFaisantLeTour,
        ),
    )
)

pageTuDressesUneTable = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.roue(vert="appât"),
            effet=Effet.affecte(vert="chardon"),
            cible=pageEnFaisantLeTour,
        ),
        Choix(
            code="2",
            condition=Condition.non(Condition.roue(vert="appât")),
            cible=pageEnFaisantLeTour,
        ),
    )
)

pageArrivéEnHaut = Page(
    choix=(
        Choix(code="H", cible=pageCommentÊtreCertain),
        Choix(code="M", cible=pageIciLesBonnesCachettes),
        Choix(code="B", cible=pageTuDressesUneTable),
    ),
)

pageTuObservesLaRoche = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="AïvyPérégrine"), Condition.roue(rouge="AïvyBarry")
            ),
            effet=Effet.affecte(bleu="piolet"),
            cible=pageArrivéEnHaut,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="AïvyPérégrine"),
                    Condition.roue(rouge="AïvyBarry"),
                )
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageArrivéEnHaut,
        ),
    )
)

pageTuTAides = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="AïvyPérégrine"),
                Condition.roue(rouge="WillPérégrine"),
            ),
            effet=Effet.affecte(bleu="fanions"),
            cible=pageArrivéEnHaut,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="AïvyPérégrine"),
                    Condition.roue(rouge="WillPérégrine"),
                )
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageArrivéEnHaut,
        ),
    )
)

pageTuCheminesTranquillement = Page(
    choix=(
        Choix(
            code="1",
            effet=Effet.et(Effet.affecte(bleu="statuette"), Effet.ajoute(jaune=-1)),
            cible=pageArrivéEnHaut,
        ),
        Choix(code="2", cible=pageArrivéEnHaut),
    )
)

pageLeLendemainMatin = Page(
    choix=(
        Choix(code="H", cible=pageTuObservesLaRoche),
        Choix(code="M", cible=pageTuTAides),
        Choix(code="B", cible=pageTuCheminesTranquillement),
    ),
)

pageTuAperçoisAuLoin = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.intervalle(roue="jaune", inf=3),
            effet=Effet.affecte(vert="appât"),
            cible=pageLeLendemainMatin,
        ),
        Choix(
            code="2",
            condition=Condition.intervalle(roue="jaune", sup=2),
            effet=Effet.ajoute(jaune=2),
            cible=pageLeLendemainMatin,
        ),
    ),
)

pageQuelquesSentiersCourent = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="AïvyPérégrine"),
                Condition.roue(rouge="WillPérégrine"),
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageLeLendemainMatin,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="AïvyPérégrine"),
                    Condition.roue(rouge="WillPérégrine"),
                )
            ),
            cible=pageLeLendemainMatin,
        ),
    )
)

pageOuhLàLà = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="WillBarry"), Condition.roue(rouge="WillPérégrine")
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageLeLendemainMatin,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="WillBarry"),
                    Condition.roue(rouge="WillPérégrine"),
                )
            ),
            cible=pageLeLendemainMatin,
        ),
    ),
)

pageAuDessusDeLaForêt = Page(
    choix=(
        Choix(code="H", cible=pageTuAperçoisAuLoin),
        Choix(code="M", cible=pageQuelquesSentiersCourent),
        Choix(code="B", cible=pageOuhLàLà),
    ),
)

pageBoisFeuillesMousses = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="WillBarry"), Condition.roue(rouge="WillPérégrine")
            ),
            effet=Effet.affecte(vert="camouflage"),
            cible=pageAuDessusDeLaForêt,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="WillBarry"),
                    Condition.roue(rouge="WillPérégrine"),
                )
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageAuDessusDeLaForêt,
        ),
    ),
)

pageEnTÉcartant = Page(
    choix=(
        Choix(
            code="1",
            effet=Effet.et(Effet.affecte(vert="appât"), Effet.ajoute(jaune=-1)),
            cible=pageAuDessusDeLaForêt,
        ),
        Choix(code="2", cible=pageAuDessusDeLaForêt),
    ),
)

pageIlYABeaucoup = Page(
    choix=(
        Choix(
            code="1",
            condition=Condition.ou(
                Condition.roue(rouge="WillBarry"), Condition.roue(rouge="AïvyBarry")
            ),
            effet=Effet.affecte(vert="corne"),
            cible=pageAuDessusDeLaForêt,
        ),
        Choix(
            code="2",
            condition=Condition.non(
                Condition.ou(
                    Condition.roue(rouge="WillBarry"), Condition.roue(rouge="AïvyBarry")
                )
            ),
            effet=Effet.ajoute(jaune=1),
            cible=pageAuDessusDeLaForêt,
        ),
    ),
)

pageVoiciLeDahu = Page(
    choix=(
        Choix(code="H", cible=pageBoisFeuillesMousses),
        Choix(code="M", cible=pageEnTÉcartant),
        Choix(code="B", cible=pageIlYABeaucoup),
    )
)

pageChoisisTonDuo = Page(
    roues={"jaune": 2},
    choix=(
        Choix(
            code="Pab",
            effet=Effet.affecte(rouge="AïvyBarry"),
            cible=pageVoiciLeDahu,
        ),
        Choix(
            code="Pap",
            effet=Effet.affecte(rouge="AïvyPérégrine"),
            cible=pageVoiciLeDahu,
        ),
        Choix(
            code="Pwb",
            effet=Effet.affecte(rouge="WillBarry"),
            cible=pageVoiciLeDahu,
        ),
        Choix(
            code="Pwp",
            effet=Effet.affecte(rouge="WillPérégrine"),
            cible=pageVoiciLeDahu,
        ),
    ),
    descriptions={
        "": "Sur la piste du dahu",
        "Pab": "Aïvy et Barry",
        "Pap": "Aïvy et Pérégrine",
        "Pwb": "Will et Barry",
        "Pwp": "Will et Pérégrine",
    },
)

LIVRES = {
    "dahu": pageChoisisTonDuo,
}
