import itertools
import random
import time 
"""Init
"""

fichier = "Instances/100M5_1.txt"

def file_reader(file):
    """Interprétation des fichiers pour les ajouter à notre structure de donnée

    Args:
        file (string): Lien vers le fichier

    Returns:
        final_list:list : _liste finale sous le format d'une liste de liste de tuples(poids,valeur)
        merged_poids:list: _liste des poids de chacun des sacs (contraintes)_
    """
    final_list,final_liste, backpack_poids, value, poids, tmp, weights= list(), list(), list(), list(), list(), list(),list()
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
        l = list()
        for elements in chunks:
            for i in range(len(elements)):
                tmp.append((int(elements[i]), int(merged_value[i]))) #Ajout à la finale liste pour avoir un tuple (int,int)
                l.append(int(elements[i]))
            weights.append(l)
            final_list.append(tmp)
            final_liste.append(tmp)
            tmp = list()
        merged_poids = [int(x) for x in merged_poids] #Cast des valeurs en int
    return final_list,merged_poids,merged_value


def senju_and_toyoda(liste,value,bags):
    temp, fin = list(),list()
    value = [int(x)*len(bags) for x in value]
    for _ in range(len(value)):
        best = max(value)
        best_index = value.index(best)
        for i in range(len(bags)):
            element = liste[i][best_index][0]
            if bags[i] - element > 0:
                temp.append(best_index)
        value.remove(best)
    for e in set(temp):
        if temp.count(e) > len(bags):
            fin.append(e)
    return fin

def get_score(value,indexes):
    return sum([int(value[index]) for index in indexes])

def local_search(indexes,value,bags,liste):
    old_score = get_score(value,indexes)
    while get_score(value,indexes) <= old_score:
        deleted = random.choice(indexes)
        indexes.remove(deleted)
        value.pop(deleted)
        for i in range(len(bags)):
            liste[i].pop(deleted)
        indexes = senju_and_toyoda(liste,value,bags)
    return indexes

def output(liste,length,max_score,file_name):
    """Créer le fichier en 1 ligne de 0 et 1 

    Args:
        liste (list): liste d'index de la meilleur population
        length (int): Nombre de valeur en total
    """
    output = ""
    with open(file_name, 'w') as f:
        for i in range(length):
            if i in liste:
                output+="1"
            else:
                output+="0"
        f.write(str(max_score)+" "+' '.join(output))

def main():
    liste, poids_sac, value = file_reader(fichier)
    index = senju_and_toyoda(liste,value,poids_sac)
    new_index = local_search(index,value,poids_sac,liste)
    output(new_index,len(value),get_score(value,new_index),"simpl_heur_sol_"+fichier.split("/")[1])

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))