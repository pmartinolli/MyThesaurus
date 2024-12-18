# Thésaurus personnel pour gérer sa documentation

*MyThesaurus : Design and manage your own personal thesaurus to index and retrieve information*

## Thesaurus builder CSV->PDF

Exemple de thésaurus à deux niveaux pour le jeu de rôle sur table : [en PDF](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/TTRPG_thesaurus.pdf) ou [en CSV](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/TTRPG_thesaurus.csv) : 
- script Python pour [transformer le CSV en PDF](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/mythesaurus_csv2pdf.py) 
- script Python pour [transformer le CSV en deux colonnes](https://github.com/pmartinolli/MyThesaurus/blob/master/ThesaurusBuilder/thesaurus3to2col.py) (pour les deux programmes ci-dessous par exemple)

## MarkDown Tag Indexer

*Python script to index automatically MarkDown files (an Obsidian.md vault for example) with a CSV of controlled tags :* 
- [MarkdownTagUpdater](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/MarkdownTagUpdater.py) : *searching keywords and adding corresponding #tags in YAML headers.*
- [MarkdownTagHarvester](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/MarkdownTagHarvester.py) : *helping building the tags.csv*
- *Example of [tags.csv](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/tags.csv)*
![How does it works?](https://github.com/pmartinolli/MyThesaurus/blob/master/MarkdownTag/MarkdownTagUpdater_howto.png)

## Zotero Tag Indexer

[ZoteroRDF_retag](https://github.com/pmartinolli/MyThesaurus/blob/master/ZoteroTag): Script Python pour indexer automatiquement des exports de bibliothèques Zotero au format RDF (Bibliontology RDF et Zotero RDF) avec un thésaurus en deux colonnes sous forme de CSV (voir plus haut). 
![How does it works?](https://github.com/pmartinolli/MyThesaurus/blob/master/ZoteroTag/ZoteroTagUpdate_howto.png)


## Outils divers 

- Un [Aide-mémoire (PDF)](https://github.com/pmartinolli/MyThesaurus/blob/master/Affiche/affiche-mythesaurus-v1.1.fr.pdf) à utiliser en formation avec quelques bonnes pratiques de création de mots-clés contrôlés.
- Un chapitre détaillé pour utiliser et se [créer un thésaurus](https://pmartinolli.github.io/QMpRD/chapters/thesaurus.html)
- Un billet de blogue pour utiliser un thésaurus avec les marqueurs de Zotero : [Optimiser l’organisation de sa bibliothèque](https://zotero.hypotheses.org/3298)
- Un modèle de thésaurus simple en tableau [(PDF)](https://github.com/pmartinolli/TM-MyThesaurus/blob/master/files/ModeleSimple/modelethesaurus.pdf) ([ODT](https://github.com/pmartinolli/MyThesaurus/blob/master/Affiche/ModeleSimple/modelethesaurus.odt))

## Besoin d'aide ?

N'hésitez pas à consulter votre bibliothécaire disciplinaire pour la conception ou le maintien de votre thésaurus. C'est notre métier, c'est notre expertise, et c'est aussi notre plaisir de vous aider avec cet outil particulièrement stimulant.


## Bibliographie

Dalbin, Sylvie. 2007. « Thésaurus et informatique documentaires. Partenaires de toujours ? » Documentaliste-Sciences de l’Information 44 (1): 42-55. https://doi.org/10.3917/docsi.441.0042.

Dégez, Danièle. 2009. « Construire un thesaurus ». Archimag, 44-45.

Hudon, Michèle. 2008. Guide pratique pour l’élaboration d’un thésaurus documentaire. Montréal: Éditions ASTED.

Keller, L. (2013). Encadrer la réingénierie d’un thesaurus : méthode, enjeux et impacts pour l’équipe d’un service de veille et documentation en entreprise (Mémoire INTD-CNAM). Institut national des techniques de la documentation du CNAM, Paris. Consulté à l’adresse https://memsic.ccsd.cnrs.fr/mem_00945542/document


## Métadonnées

* Author / Auteur : Pascal Martinolli

* Created / Créé le : 2019-02-24

* License / Licence : CC-BY

* Used by / Utilisé par  : [Séminaire PLU6058 - Rechercher et exploiter la documentation, UdeM](https://bib.umontreal.ca/multidisciplinaire/plu6058) ; [formations libres Zotero et EndNote, UdeM](https://bib.umontreal.ca/formations/).

* Comment le citer / *How to cite it* : Martinolli, Pascal. 2019-2020. *Thésaurus personnel pour collection de références bibliographiques*. Matériel pédagogique. Université de Montréal. https://github.com/pmartinolli/MyThesaurus

* Commments are welcomed at / Commentaires bienvenus : pascal.martinolli [à] umontreal.ca

* Remerciements : Catherine Bernier et Mathieu Thomas pour l'accompagnement des équipes de projet. Danièle Dégez et Sylvie Dalbin, consultantes en thésaurus, dont j’ai eu la chance de suivre les enseignements à l’INTD. 

\
\
https://github.com/pmartinolli/MyThesaurus
