import itertools
from operator import itemgetter


def file_reader(file):
    """Interprétation des fichiers pour les ajouter à notre structure de donnée

    Args:
        file (string): Lien vers le fichier

    Returns:
        final_list:list : _liste finale sous le format d'une liste de liste de tuples(poids,valeur)
        merged_poids:list: _liste des poids de chacun des sacs (contraintes)_
    """
    final_list, backpack_poids, value, poids, tmp = list(), list(), list(), list(), list()
    k = 0
    with open(file, 'r') as f:
        lines = [line for line in f if line.strip()]
        for iteration, line in enumerate(lines):
            if iteration == 0:
                n, m = line.split()
                n, m = int(n),int(m)
            if iteration > 0 and iteration <= n/10: #Récupère les N/10 valeurs
                value.append(line.split())
            if iteration > n/10 and k < m/10: #Récupère les N lignes de poids de sac
                poids.append(line.split())
                k = k+1
            if iteration > n/10+1 and k >= m/10: 
                backpack_poids.append(line.split())
        if m>10: # Pour retirer la ligne de poids en trop qui apparaît pour des raisons inconnues
            backpack_poids.pop(0)
        merged_poids,merged_value,flatten_backpack_poids = list(itertools.chain.from_iterable(poids)),list(itertools.chain.from_iterable(value)),list(itertools.chain.from_iterable(backpack_poids)) #Parsing de chacune des variables pour applatir les listes
        chunks = [flatten_backpack_poids[x:x+n] for x in range(0, len(flatten_backpack_poids), n)] #Découpage en N chunks pour les attribuer aux sacs
        for elements in chunks:
            for i in range(len(elements)):
                tmp.append((int(elements[i]), int(merged_value[i]))) #Ajout à la finale liste pour avoir un tuple (int,int)
            final_list.append(tmp)
            tmp = list()
        merged_poids = [int(x) for x in merged_poids] #Cast des valeurs en int
    #print(f'n = {n} | m = {m}')
    #print(f'poids = {merged_poids}')
    #print(f'value = {merged_value}')
    #print(f'final = {final_list}')
    return final_list,merged_poids

def average(values):
    """Moyenne des poids de chacun des objets dans les sacs --> NON UTILISÉE

    Args:
        values (list:list): Liste de liste de tuple, la liste des valeurs et les poids de chacun des objets

    Returns:
        liste:list : _moyenne de chacun des poids dans chacun des sacs_
    """
    liste = list()
    for element in values:
        liste.append(sum(map(lambda x: x[1], element)) / len(element))
    return liste


def verif_poids(liste):
    """Fonction de test pour vérifier les poids --> NON UTILISÉE

    Args:
        liste (list): Liste de tuples (poids,valeur)

    Returns:
        int: _poids obtenu_
    """
    return sum(map(lambda x: x[0], liste)), sum(map(lambda x: x[1], liste))

def get_indexes(values,list_index,bags):
    """Retourne les éléments en fonction de chacun des indexs récupéré dans la fonction simple_heuristique

    Args:
        values (list:list): Liste de liste de tuple, la liste des valeurs et les poids de chacun des objets
        list_index (list): _Liste d'index des valeurs retenues pour le sac_
        bags (list): _Liste des contraintes de chacun des sacs_

    Returns:
        l:list:list : _Liste imbriquée de tuples avec (poids,valeur) pour chacun_
    """
    l = list()
    for index in list_index:
        for i in range(len(bags)):
            l.append(values[i][index])
    l = [l[i * len(list_index):(i + 1) * len(list_index)] for i in range((len(l) + len(list_index) - 1) // len(list_index))]
    return l

def beautier_print(values,list_index,bags,rest_of_bags):
    """Print viable

    Args:
        values (list:list): Liste de liste de tuple, la liste des valeurs et les poids de chacun des objets
        list_index (list): Liste d'index retenu pour les sacs
        bags (list): liste des poids de chacun des sacs
        rest_of_bags (list): Liste des restes de poids de chaque sacs
    """
    l,summed = list(),list()
    for index in list_index:
        for i in range(len(bags)):
            l.append(values[i][index])
    l = [l[i * len(bags):(i + 1) * len(bags)] for i in range((len(l) + len(bags) - 1) // len(bags))]
    for it,k in enumerate(zip(*l)):
        summed.append((k,(sum(map(lambda x: x[0], k))), (sum(map(lambda x: x[1], k))),bags[it],rest_of_bags[it])) #Ajout des éléments pour l'affichage
    for element in summed:
        print(f'Objets:{element[0]}\t Poids total:{element[1]} Valeur totale:{element[2]} Contrainte:{element[3]} Reste:{element[4]}\n')
  
 # ________________________________________________________________________________________________________________________________________________________________
  
def local_search(values,selected_items,bags,rest_bags):
    """Local search, s'applique à la fin de la première solution heuristique pour avoir une amélioration:
    Recherche du sac le plus rempli --> On retire le plus gros élément et on relance une recherche d'un résultat les plus rentable

    Args:
        values (list:list): Liste de liste de tuple, la liste des valeurs et les poids de chacun des objets
        selected_items (list:list): Liste des valeurs obtenus dans le get_indexes
        bags (list): Liste des poids de chacun des sacs
        rest_bags (list): Liste du reste de poids de chacun des sacs
    """
    for i in range(10):
        most_full = min(rest_bags)
        print(most_full)
        most_full_index = rest_bags.index(most_full)
        copy = bags.copy()
        bigger_object = max(selected_items[most_full_index], key=itemgetter(0))
        print(bigger_object)
        for i in range(len(values)):
            if bigger_object in values[i]:
                values[i].remove(bigger_object) #On supprime l'item le plus gros pour ne plus qu'il soit choisi
        indexes = simple_heuristic(bags, values)
        rest_of_bags = bags
        beautier_print(values, indexes, copy, rest_of_bags)

def simple_heuristic(bags,values):
    """Calcul de l'heuristique:
    Addition de chacun des poids/valeur de tous les items du même indice et on récupère le plus rentable et on vérifie si ses valeurs de bases rentrent
    dans son sac respectif et on répète cela jusqu'à ce qu'on ne puisse plus rien rentrer.

    Args:
        bags (list): Liste des poids des sacs
        values (list:list): Liste de liste de tuple, la liste des valeurs et les poids de chacun des objets

    Returns:
        liste:list: Liste des indices des objets gardés
    """
    t, liste, sum_of_tuples = list(),list(),list()
    s,ss = 0,0
    set_value = True
    for elements in values:
        for i in range(len(elements)):
            s += elements[i][0]
            ss += elements[i][1]
        sum_of_tuples.append((s, ss))
    sum_of_tuples = [tuple(map(sum, zip(*i))) for i in zip(*values)] #Ligne pour additionner chacun des élement du même indice dans la liste de valeurs
    print("\n================================")
    print(sum_of_tuples)
    while 0 not in bags:
        if len(sum_of_tuples) == 0:
            break
        maxi = max(sum_of_tuples, key=itemgetter(1)) #On récupère le max
        index = sum_of_tuples.index(maxi)
        for element in values: #On récupère les valeur à l'indice du max, pour avoir n tuples du même indice dans chaque liste
            t.append(element[index])
        for i in range(len(t)-1): 
            if t[i][0] > bags[i]: #Si c'est au dessus, on le set à false et on ne l'ajoute pas
                set_value = False
        if set_value:
            for i in range(len(t)):
                bags[i] = abs(bags[i] - t[i][0]) #On soustrait dans chacun des sacs le poids de l'objet selectionné
            liste.append(index)
        sum_of_tuples.remove(maxi) #On le supprime de la liste pour ne pas boucler infiniment 
        t = list()
    return liste


def main():
    liste, poids = file_reader('Instances/500M30_21.txt')
    tmp,valeur = poids.copy(),liste.copy()
    indexes = simple_heuristic(poids, liste)
    selected_values = get_indexes(liste, indexes,tmp)
    local_search(valeur,selected_values,tmp,poids)

if __name__ == '__main__':
    main()