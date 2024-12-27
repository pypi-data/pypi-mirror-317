================================================================
`mpa` — Calcul du nombre d'histoires dans *Ma Première Aventure*
================================================================

.. currentmodule:: jouets.mpa

La série de livres `Ma Première Aventure <https://ma-premiere-aventure.fr/>`__ raconte des « histoires dont tu es le tout petit héros » : à plusieurs endroits dans le livre, il faut choisir quelle page tourner en fonction de l'histoire. Il est ainsi possible de raconter différentes histoires (et d'obtenir trois fins différentes) en fonction des choix effectués.

Dans cette page, donc calculons combien d'histoires il est possible de raconter avec un seul livre, et quelle est la probabilité de victoire.

J'ai appliqué cette méthode à `Ma Première Aventure <https://ma-premiere-aventure.fr>`__, mais on peut tout aussi bien l'appliquer à n'importe quel jeu à un joueur avec un nombre de cas limités (quelques milliers de cas), comme `Cartaventura <https://blam-edition.com/univers-cartaventura/>`__ [#cartaventura]_.

.. contents::
   :local:

Résultats
=========

Voici, pour les pressé·e·s, les résultats.

Nombres d'histoires et probabilités de victoire
-----------------------------------------------

.. csv-table::
   :header: "N°", "Titre", "Nombre d'histoires", "(dont victoires)", "Probabilité de victoire", "Solutions"

    1, "`En quête du dragon <https://ma-premiere-aventure.fr/livres/en-quete-du-dragon>`__ (seconde édition)", 5184, 60, "1,08 %", ":download:`complet <mpa/mpa-dragon.pdf>` :download:`minimal <mpa/mpa-dragon-minimal.pdf>`"
    2, "`La Découverte de l’Atlantide <https://ma-premiere-aventure.fr/livres/la-decouverte-de-latlantide>`__ (seconde édition)", 5184, 72, "1.39 %", ":download:`complet <mpa/mpa-atlantide.pdf>` :download:`minimal <mpa/mpa-atlantide-minimal.pdf>`"
    8, "`Sur la piste du dahu <https://ma-premiere-aventure.fr/livres/sur-la-piste-du-dahu>`__ (seconde édition)", 5184, 60, "1,47 %", ":download:`complet <mpa/mpa-dahu.pdf>` :download:`minimal <mpa/mpa-dahu-minimal.pdf>`"
    9, "`La Bibliothèque infinie <https://ma-premiere-aventure.fr/livres/la-bibliotheque-infinie>`__", 2484, 64, "2,62 %", ":download:`complet <mpa/mpa-bibliotheque.pdf>` :download:`minimal <mpa/mpa-bibliotheque-minimal.pdf>`"
   10, "`Pattie et l'Épreuve des dieux <https://ma-premiere-aventure.fr/livres/pattie-lepreuve-des-dieux>`__", 2304, 106, "4,22 %", ":download:`complet <mpa/mpa-pattie.pdf>` :download:`minimal <mpa/mpa-pattie-minimal.pdf>`"

Quelques commentaires :

- Nous considérons ici que la même histoire racontée avec deux personnages différents est comptée deux fois.
- La probabilité de victoire est définie comme la probabilité de gagner en faisant chacun des choix au hasard. Elle ne correspond pas toujours à la fréquence des histoires menant à la victoire. C'est normal : toutes les histoires ne sont pas équiprobables.
- Deux graphes des solutions sont proposés pour l'ensemble des chemins menant à la victoire : ``complet`` propose tous les chemins possibles, alors que dans ``minimal``, seuls les choix non contraints sont présentés (par exemple, si sur trois alternatives, seule la seconde est possible car on ne possède pas l'objet nécessaire pour les deux autres, ce choix n'est pas affiché sur ce second graphe).

Probabilité de victoire avec les différents personnages
-------------------------------------------------------

Ces probabilités ont été obtenues avec la commande ``mpa proba LIVRE --préfixe PERSONNAGE``. Par exemple, pour obtenir la probabilité de gagner avec Lina dans *En quête du dragon*, la commande suivante donne la réponse : ``mpa proba dragon --préfixe Pl``.

1. `En quête du dragon <https://ma-premiere-aventure.fr/livres/en-quete-du-dragon>`__ (seconde édition)

   .. csv-table::
      :header: "Lina", "Sachat", "Timon"

      "1,08 %", "1,08 %", "1,08 %"

2. `La Découverte de l’Atlantide <https://ma-premiere-aventure.fr/livres/la-decouverte-de-latlantide>`__ (seconde édition)

   .. csv-table::
      :header: "Béhémoth", "Espadon", "Manta"

      "1,39 %", "1,39 %", "1,39 %"

8. `Sur la piste du dahu <https://ma-premiere-aventure.fr/livres/sur-la-piste-du-dahu>`__ (seconde édition)

   .. csv-table::
      :header: "Aïvy & Barry", "Aïvy & Pérégrine", "Will & Barry", "Will & Pérégrine"

      "1,17 %", "1,68 %", "0,99 %", "1,47 %"

9. `La Bibliothèque infinie <https://ma-premiere-aventure.fr/livres/la-bibliotheque-infinie>`__

   .. csv-table::
      :header: "Camille", "Lilon", "Lucien"

      "2,78 %", "2,78 %", "2,31 %"

10. `Pattie et l'Épreuve des dieux <https://ma-premiere-aventure.fr/livres/pattie-lepreuve-des-dieux>`__

   .. csv-table::
      :header: "Chickos", "Pattie", "Sam"

      "7,92 %", "1,54 %", "3,19 %"



Description des choix
=====================

Cette page sera mieux compréhensible en ayant lu l'histoire (voire en ayant le livre sous les yeux), mais essayons quand-même.

Nous prenons comme exemple ici la seconde édition de `En quête du dragon <https://ma-premiere-aventure.fr/livres/en-quete-du-dragon>`__, mais le principe est le même pour tous les livres de la collection.

- Le premier choix à faire est celui du personnage : trois sont disponibles.
- Le deuxième choix s'effectue dans le village : allons-nous visiter le moulin, la grange, ou la maison du cartographe ? Il y a derrière chacun de ces choix un nouveau choix entre deux alternatives, soit libres, soit déterminées par le personnage choisi.
- Le choix précédent (trois possibilités, puis deux pour chacune des trois) est répété cinq nouvelles fois, avec parfois des contraintes (fonction du personnage, ou des objets récoltés plus tôt dans l'histoire).
- À la fin, en fonction du nombre de « bobos » subis, il y a trois fins : victoire, défaite, ou entre les deux.

Nombre d'histoires : Calcul mathématique
========================================

Un premier calcul naïf donne donc comme nombre d'histoires : :math:`3\times (3\times2)^6\times3` :

- trois personnages ;
- trois alternatives, puis deux alternatives selon le choix précédent (:math:`3\times2`), le tout répété six fois (puissance 6) ;
- trois fins possibles.

Mais ce calcul est faux, car tous les choix ne sont pas libres :

- certains chemins sont contraints par le personnage ou l'objet ;
- les fins sont contraintes par le nombre de « bobos ».

En ne regardant que les choix libres, le nombre de chemins possibles est donc :

- trois personnages ;
- trois alternatives, suivi de (globalement) quatre alternatives possibles (puisque certains choix sont contraints), le tout répété trois fois (:math:`4^3`) ;
- trois alternatives, suivi d'un choix contraint, le tout répété trois fois (:math:`3^3`) ;
- la fin est contrainte en fonction du nombre de bobos, donc aucun choix ici.

Cela donne donc :math:`3\times4^3\times3^3=5184` histoires possibles.

Mais en faisant cela, nous avons fait une interprétation particulière du problème. En effet, si un même chemin peut être emprunté par deux personnages différents, devons nous compter cela comme un seul chemin, ou deux ? Le résultat précédent (5184 histoires possibles) compte comme deux chemins le même chemin emprunté par deux personnages différents.

Combien d'histoires sont possibles en comptant une seule fois plusieurs chemins empruntés par des personnages différents ? Je ne sais pas comment le faire par le calcul. Faisons le de manière informatique.

Un peu d'informatique
=====================

.. currentmodule:: jouets.mpa.graphe

Description des livres
----------------------

Un livre est une liste de :class:`pages <Page>` interconnectées.  Voici par exemple la première page du livre. Elle contient simplement que trois choix sont possibles, sans conditions, sans effets.

.. code-block:: python

   pageTuVisDansUn = Page(
       choix=(
           Choix(code="H", cible=pageDemanderDeLAide),
           Choix(code="M", cible=pageFouillerLaGrangeAbandonnée),
           Choix(code="B", cible=pageVolerUneCarteChez),
       )
   )

Le premier choix avec conditions est celui-ci :

.. code-block:: python

   pageDemanderDeLAide = Page(
       choix=(
           Choix(
               # Si la roue rouge est Sachat,
               # alors tourner une page vers la page « Alors que tu quittes… »
               code="1",
               condition=Condition.roue(rouge="Sachat"),
               cible=pageAlorsQueTuQuittes,
           ),
           Choix(
               # Si la rouge rouge n'est pas Sachat,
               # alors ajoute la pierre sur la roue verte,
               # et tourne deux pages vers la page « Alors que tu quittes… »
               code="2",
               condition=condition_non(Condition.roue(rouge="Sachat")),
               effet=Effet.affecte(vert="pierre"),
               cible=pageAlorsQueTuQuittes,
           ),
       )
   )

De plus, une :class:`histoire <Histoire>` est *une* seule des histoires possibles.

Commande : ``graphe``
---------------------

Cette commande permet de tracer le graphe représentant les choix possibles dans l'histoire. Elle me sert à vérifier que ma représentation de l'histoire est correcte. Elle génère le graphe au format `graphviz <https://graphviz.org/>`__.

.. code-block:: shell

   $ mpa graphe dragon | dot -Tpdf -o graphe-dragon.pdf

Le résultat est :download:`ce graphique <mpa/mpa-dragon-graphe.pdf>`.

Commande : ``histoires``
------------------------

La commande ``histoires`` permet de compter le nombre de chemins (avec la méthode :meth:`Histoire.histoires`). Pour cela, nous itérons sur les choix, si la condition est remplie.

.. literalinclude:: ../jouets/mpa/graphe.py
 :linenos:
 :pyobject: Histoire.histoires

C'est la méthode :meth:`Histoire.suivantes` qui permet de ne sélectionner que les choix remplissant les conditions.

.. literalinclude:: ../jouets/mpa/graphe.py
   :linenos:
   :pyobject: Histoire.suivantes

À l'aide de ce programme, nous obtenons une liste de codes, correspondant chacun à une histoire.


.. code-block:: shell

   $ mpa histoires dragon

   PlB2B1B2B2B2B2B2
   PlB2B1B2B2B2H1M
   …
   PtM2M2M2M2M2H2B1
   PtM2M2M2M2M2M2B1

Par exemple ``PlH2B1H2B2H2B2B2`` signifie :

- ``Pl`` : choisir le personnage Lina ;
- ``H2`` : au premier choix, tourner la page du haut, puis faire le choix qui fait tourner deux pages ;
- ``B1`` : au second choix, tourner la page du bas, puis faire le choix qui fait tourner une seule page ;
- ``H2``, ``B2``, ``H2``, ``B2`` : etc.
- ``B2`` : à la fin, tourner la page du bas (défaite) puis faire le choix qui fait tourner deux pages.

Notre programme affiche la liste brute de tous les chemins possibles, mais avec quelques commandes shell, nous pouvons répondre à quelques questions :

- Combien d'histoires sont possibles (sachant que le même chemin suivi par deux personnages compte comme deux histoires) ?

  .. code-block:: shell

     $ mpa histoires dragon | wc -l
     5184

  Nous retrouvons le nombre calculé plus haut.

- Combien d'histoires sont possibles (sachant que le même chemin suivi par deux personnages compte comme une seule histoire) ?

  .. code-block:: shell

     $ mpa histoires dragon | # Génère toutes les histoires \
     > cut -c3- | # Supprime la première lettre (choix du personnage) \
     > sort -u | # Trie les histoires, et ne conserve qu'un exemplaire des histoires identiques \
     > wc -l # Compte le nombre d'histoires
     4783

- En considérant le même chemin suivi par deux personnages différent comme deux histoires :

  - Combien d'histoires mènent à la victoire ?

    .. code-block:: shell

       $ mpa histoires dragon | # Génère toutes les histoires \
       grep H$ | # Ne conserve que celles qui se terminent par "H" (ce qui correspond à une victoire) \
       wc -l # Compte le nombre d'histoires
       60

  - Combien d'histoires mènent à une semi-victoire semi-défaite ?

    .. code-block:: shell

       $ mpa histoires dragon | # Génère toutes les histoires \
       grep M$ | # Ne conserve que celles qui se terminent par "M" (ce qui correspond à une semi-victoire semi-défaite) \
       wc -l # Compte le nombre d'histoires
       3024

  - Combien d'histoires mènent à une défaite ?

    .. code-block:: shell

       $ mpa histoires dragon | # Génère toutes les histoires \
       grep B[12]$ | # Ne conserve que celles qui se terminent par "B" suivi de 1 ou 2 (ce qui correspond à une défaite) \
       wc -l # Compte le nombre d'histoires
       2100

  - Bilan : Sur 5184 histoires, il y en a donc seulement 60 qui mènent à la victoire, soit à peine 1,2 % environ.


Commande : ``proba``
--------------------

Puisque 1,2 % des histoires mènent à la victoire, nous pourrions être tenté d'affirmer que la probabilité de victoire en tournant les pages au hasard est de 1,2 %. Mais nous faisons ici l'erreur de croire que toutes les histoires sont équiprobables, ce qui n'est pas le cas (certaines histoires ont plus de chance d'être racontées au hasard que d'autres).

La commande ``proba`` permet de calculer cela, à l'aide de la méthode :meth:`Histoire.proba` de la classe :class:`Page` qui calcule la probabilité d'une fin donnée. C'est une fonction récursive :

- Si la fin de la page est connue (c'est la page qui annonce la victoire, ou la défaite, ce qui est déterminé en regardant l'attribut :attr:`Page.fin`), la probabilité est 0 ou 1, suivant que c'est la fin recherchée.
- Si la fin n'est pas connue (l'attribut :attr:`Page.fin` est ``None``), la probabilité d'obtenir la fin cherchée est la moyenne des probabilités d'obtenir cette fin pour chacun des choix possibles de cette page.

Cela utilise la formule des probabilités totales, que j'enseigne à mes élèves de première.

.. proof:property:: Formule des probabilités totales

   Soient :math:`A_1`, :math:`A_2`, …, :math:`A_n` des évènements non vides formant une partition d'un univers :math:`\Omega`, et :math:`B` un évènement. Alors :

   .. math::

      P(B)=P(A_1)\times P_{A_1}(B)+P(A_2)\times P_{A_2}(B)+\cdots+P(A_n)\times P_{A_n}(B)

Ici, la partition est l'ensemble des choix, qui sont équiprobables (par exemple une chance sur trois d'aller en haut :math:`H`, au milieu :math:`M`, ou en bas :math:`B`), et on considère l'évènement :math:`V=\text{« Obtenir la victoire}`. La formule devient donc :

.. math::

   P(V)=P(B)\times P_B(V)+P(M)\times P_M(V)+P(H)\times P_H(V)

.. literalinclude:: ../jouets/mpa/graphe.py
   :linenos:
   :pyobject: Histoire.proba

Nous obtenons alors les probabilités suivantes.

.. code-block:: shell

   $ mpa proba dragon
   Probabilité de bof : 0.5648148148148149
   Probabilité de défaite : 0.4243827160493827
   Probabilité de victoire : 0.010802469135802469

Et comme on pouvait s'en douter, la probabilité de victoire (1,08 %) n'est pas égale à la proportions d'histoires victorieuses (1,16 %).


Commande : ``victoires``
------------------------

Une fois le livre représenté comme un graphe (dans les parties précédentes), il devient relativement aisé de représenter toutes les histoires victorieuses possibles. Le résultat est du code :math:`\LaTeX` qui, une fois compilé, donne le dessin suivant (:download:`en PDF <mpa/mpa-dragon.pdf>`).

Légende :

- **L**, **S**, **T** : Choix des personnages (Lina, Sachat, Timon).
- **H**, **M**, **B** : Morceau de page à tourner (Haut, Milieu, Bas).
- **1**, **2** : Tourner une ou deux pages.

:download:`Ce graphique <mpa/mpa-dragon.pdf>` a été obtenu avec :

.. code-block:: shell

   $ mpa victoires dragon | pdflatex

Remarquons que ce code :math:`\LaTeX` est ensuite modifié à la main pour obtenir la version `publié par l'éditeur sur les réseaux sociaux <https://www.facebook.com/photo/?fbid=950322350430137&set=pcb.950322413763464>`__.

Commande : ``fins``
-------------------

Cette commande liste simplement toutes les fins possibles. Ce n'est pas la commande la plus utile, mais j'en ai eu besoin.

.. literalinclude:: ../jouets/mpa/graphe.py
 :linenos:
 :pyobject: Histoire.fins


.. code-block:: shell

 $ mpa fins dragon
 bof
 défaite
 victoire

.. rubric:: Notes de bas de page

.. [#cartaventura] D'ailleurs, `éditions Blam! <https://blam-edition.com>`__, vous pouvez m'embaucher pour faire :download:`les mêmes infographies <mpa/mpa-dragon.pdf>`, mais il faut `me payer en droits d'auteurs <https://www.education.gouv.fr/vie-professionnelle-et-situation-personnelle-cumul-d-activites-3977>`__.
