# :space_invader: Projet Jeu de Géographie
Projet pour le cours de Connaissance & Raisonnement à CentraleSupélec


## :page_facing_up: Description
Jeu dans lequel chaque joueur démarre sur un pays du monde et doit parcourir le plus de pays possible. Pour avancer, il doit à la fois donner le nom d'un pays limitrophe de l'endroit dans lequel il est, et répondre à une question (typiquement trouver la capitale, le nombre d'habitants, une question de culture locale, etc). Les données seront récupérées dans [Wikidata](https://www.wikidata.org/wiki/Wikidata:WikiProject_Countries).

## :vertical_traffic_light: Règles du jeu
Le but du jeu est de parcourir le plus de pays possible. Pour avancer, chaque joueur commence son parcours dans un pays.

1. Question 1 : Le joueur doit dans un premier temps donner un pays limitrophe de l'endroit où il se trouve.
2. Question 2 : S'il réussit, il peut alors répondre à une question de culture générale sur le pays limitrophe.

La question 1 vaut un point, tandis que la question 2 vaut deux points. S'il ne réussit pas à répondre à la question 1, il devra attendre la prochaine manche.

Astuce : réfléchissez-bien au pays limitrophe que vous choisissez, certains pays n'ont pas beaucoup de voisins !

## :card_index_dividers: Segmentation
Notre répertoire est segmenté en quatre fichiers python, deux fichiers markdown, un fichier .gitinore et un fichier texte pour les requirements :

```bash 
.
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── requirements.txt 
├── sparQL_query.py
├── Quiz.py
├── script.py 
└── utils.py
```

- ``README.md`` contient l'ensemble des informations sur le projet pour pouvoir l'installer.
- ``CONTRIBUTING.md`` contient l'ensemble des informations sur les normes et les pratiques de collaboration et de gestion du projet.
- ``.gitignore`` contient les fichiers qui doivent être ignorés lors de l'ajout de fichiers au dépôt Git.
- ``requirements.txt`` contient la liste des modules et des bibliothèques Python qui doivent être installés, ainsi que leur version spécifique.
- ``sparQL_query.py`` regroupe les fonctions permettant de réaliser les requêtes sur Wikidata.
- ``Quiz.py`` comprend la classe ``Quiz`` qui permet de générer des questions et traiter les réponses à partir des requêtes effectuées dans le fichier ``sparQL_query.py``
- ``script.py`` englobe l'interface du jeu.
- ``utils.py`` contient l'ensemble des fonctions nécessaires pour l'interface du jeu implémenté sur le fichier ``script.py``.

## :wrench: Installation
Pour jouer au jeu de gégographie :

1. Tout d'abord, assurez-vous que vous avez installé une version `python` supérieure à 3.9. Nous vous conseillons un environnement conda avec la commande suivante : 
```bash
conda create --name jeu_geographie python=3.9`
```
- Pour activer l'environnement :
```bash
conda activate jeu_geographie
```

2. Vous devez ensuite installer tous les `requirements` en utilisant la commande suivante :
```bash
pip install -r requirements.txt
```

3. Exécuter l'interface du jeu en utilisant la commande suivante :
```bash
python script.py
```

## :thinking_face: Choix
Nous avons sélectionné deux cas de pays qui posent problème s'ils sont tirés comme pays initial en début de partie :
1. Les pays ayant aucun pays limitrophe
2. Les îles. Wikidata considèrent sur certaines îles, des pays limitrophes. Néanmoins, nous avons fait le choix de ne pas prendre en compte les îles afin de rester rationnel.

Lorsqu'en début de partie, un joueur tombe sur un pays se situant dans l'un de ces deux cas, le joueur est transféré dans un autre pays pour ne pas être désavantagé.

Lors des manches suivantes, si l'un des joueurs a choisi comme pays limitrophe, un pays qui se trouve dans l'un de ces deux cas, le joueur est transféré dans un autre pays, et devra attendre la manche suivante pour pouvoir jouer. Le joueur doit bien réfléchir aux pays limitrophes qu'il choisit pour ne pas perdre de points. 

## :pencil2: Auteurs
- MICHOT Albane
- NONCLERCQ Rodolphe


