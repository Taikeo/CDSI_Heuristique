Dans ce fichier ZIP vous trouverez deux fichiers, un .py et un autre .ex.

Le fichier .py a été développé par Kevin, l'autre par Alexandre.

Le code Python fonctionne sur l'heuristique de Senju et Toyoda, il recherche la meilleur valeur et l'ajoute dans le sac s'il entre.
Le code Elixir fonctionne sur le principe de ratio Poids/Valeur. 

Vous trouverez l'heuristique et la recherche locale pour chacun des codes dans les fichiers "solution1"





Pour les fichiers metaheuristic:

.py = Algorithme génétique, FYI, avec 200k generations sur l'instance "100M5_1.txt" on a 24140 en optimum local.

.ex = Algorithme Tabou



Pour exécuter les fichiers .ex:

1. Télécharger Elixir et Erlang
2. Compiler le fichier à l'aide de la commande "elixirc nom_du_fichier.ex"
3. Lancer un terminal iex à l'aide de la commande "iex"
4. Exécuter le programme à l'aide de la commande :
    - "Heuristique.main" pour le fichier "solution1.ex"
    - "Metaheuristique.main" pour le fichier "metaheuristic.ex"
5. Il est possible de faire varier le nombre d'itération, le nombre d'item bannis 
ainsi que le nombre de ban simultané maximum à l'aide des trois premiers paramètres de la fonction.
Le quatrième paramètre permet de modifier l'instance utilisé.
Par défaut 100, 10, 20 et "100M5_1"

Exemple d'éxécution pour un fichier avec paramètres: "Metaheuristique.main(100, 10, 20, "100M5_1")"