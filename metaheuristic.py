import itertools
import random
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


def randomized(maxi,mini=0):
    return random.randint(mini,maxi)
    
def initialisation(liste,bags,population):
    indexes = list()
    solution = list()
    solutions = list()
    tmp_bags = bags.copy()
    for _ in range(population):
        t1 = randomized(25,10)
        t2 = randomized(25,10)
        for _ in range(min(t1,t2),max(t1,t2)):
            random = randomized(len(liste[0])-1)
            elements = list(zip(*liste))[random]
            for it in range (len(elements)):
                if elements[it][0] <= tmp_bags[it]:
                    indexes.append(random)
                    tmp_bags[it] -= elements[it][0]
        for numbers in set(indexes):
            if indexes.count(numbers) == 5:
                solution.append(numbers)
        solutions.append(solution)
        solution = list()
        indexes = list()
        tmp_bags = bags.copy()
    return solutions
    
def get_elements(indexes_l,liste):
    item = list()
    items = list()
    items_per_bag = list()
    for indexes in indexes_l:
        for index in indexes:
            item.append(list(list(zip(*liste))[index]))
        items.append(item)
        item = list()
    for i in range(len(items)):
        items_per_bag.append([list(x) for x in zip(*items[i])])
    return items_per_bag
            
def get_values(items_per_bag):
    liste, values = list(),list()
    sum_items_bag = 0
    for it,items in enumerate(items_per_bag):
        for item in items:
            for tuples in item:
                sum_items_bag += tuples[1]
        liste.append((items,sum_items_bag))
        values.append((it,sum_items_bag))
        sum_items_bag = 0
    return liste,values

def get_bests(nb_of_best,values):
    values.sort(key = lambda x: x[1], reverse = True)
    return values[:nb_of_best]

def indexes_to_best(best_indexes,liste):
    return 0

def mutation(bests,list_final):
    return 0

def main():
    liste, poids = file_reader('Instances/100M5_1.txt')
    #print(liste, poids)
    indexes_l = initialisation(liste, poids,100)
    items_per_bag = get_elements(indexes_l,liste)
    total_l,values = get_values(items_per_bag)
    best_indexes = get_bests(10,values)
    print(best_indexes)

if __name__ == '__main__':
    main()
