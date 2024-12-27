.. _api-mpa:

`mpa`
=====

.. contents::
   :local:

.. currentmodule:: jouets.mpa.graphe

`Page`
------

Une page est simplement une liste de choix, assortie d'une éventuelle fin (victoire, défaite, ou entre les deux).

.. autoclass:: Page
   :members:

`Choix`
-------

Un choix a davantage d'attributs, dont les effets et les conditions.

.. autoclass:: Choix
   :members: code, cible, condition, effet

`Effets`
--------

Les effets à appliquer en tournant les pages (« Ajoute le marteau sur la roue jaune », « Ajoute une relique sur la roue verte », etc.) :

.. autodata:: Effet

`Conditions`
------------

Des conditions à vérifier (« Il y a un ou deux bobos », « Tu es le personnage Lina », « Tu as les chaussons ou tu es Sachat », etc.) sont construites à partir des fonctions suivantes.

.. autodata:: Condition

`Histoire`
----------

Cet objet représente *une* des histoires possibles (choisir le premier personnage, tourner la page du milieu, tourner deux pages, etc.).

.. autoclass:: Histoire
   :members:
