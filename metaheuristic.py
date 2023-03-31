import itertools
import random

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
    return final_list,final_liste,merged_poids,merged_value

def randomized(maxi,mini=0):
    return random.randint(mini,maxi)

def initialisation(listee,bags,population):
    pp = list()
    baggy = [0 for x in range(len(bags))]
    solution,solutions,indexes = list(),list(),list()
    for _ in range(population):
        while True:
            if len(pp) == len(listee[0]):
                break
            rand = random.randint(0,len(listee[0])-1)
            if rand in pp:
                continue
            elements = list(zip(*listee))[rand]
            for it in range(len(elements)):
                if baggy[it] <= bags[it]:
                    indexes.append(rand)
                    baggy[it] += elements[it][0]
            pp.append(rand)
        pp = list()
        baggy = [0 for x in range(len(bags))]
        for numbers in set(indexes):
            if indexes.count(numbers) == 5:
                solution.append(numbers)
        solutions.append(solution)
        solution = list()
        indexes = list()
    return solutions

def get_valuesv2(indexes,value):
    l,liste = list(),list()
    for index in indexes:
        for i in index:
            l.append(int(value[i]))
        liste.append(l)
        l = list()
    return [(indexes[liste.index(x)], sum(x)) for x in liste]


def get_valuesv3(index, value):
    l, liste = list(), list()
    for i in index:
        l.append(int(value[i]))
    liste.append(l)
    return [ (index,sum(x)) for x in liste]

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

def get_indexes_from_best(bests_indexes):
    return [x[0] for x in bests_indexes]

def weights_evaluation(bests_indexes,bags,liste):
    to_be_evaluated,tmp,sums,boolean = list(),list(),list(),list()
    for j in range(len(bags)):
        for i in range(len(bests_indexes)):
            tmp.append(liste[j][bests_indexes[i]][0])
        to_be_evaluated.append(tmp)
        tmp = list()
    sums = [sum(lists) for lists in to_be_evaluated]
    boolean = [True if sums[i] <= bags[i] else False for i in range(len(sums))]
    #print(boolean,bags)
    b = False if False in boolean else True
    return b

def get_single_value(indexes,value):
    return sum([int(value[element]) for element in indexes])
        
def value_evaluation(initial,rival,value):
    value1, value2 = get_single_value(initial, value), get_single_value(rival, value)
    #print(value1,value2)
    return value1 if value1 >= value2 else value2

def croisement(best_indexes,bags,liste,value):
    childs,child,accept,accepted = list(),list(), list(),list()
    for i in range(len(best_indexes)):
        parent = best_indexes[i]
        for j in range(0,len(best_indexes)):
            child.append(parent[:len(parent)//2] + best_indexes[j][len(best_indexes[j])//2:])
        childs.append(child)
        child = list()
    cpt = 0
    for elements in childs:
        for element in elements:
            b = weights_evaluation(element, bags, liste)
            if b:
                cpt += 1
                accept.append(element)
    for child in accept:
        print(get_valuesv3(child,value))
    return accept
                

def mutation(bests,list_final):
    return 0

def main():
    liste, copy,poids_sac, value = file_reader('Instances/100M5_1.txt')
    ps=poids_sac.copy()
    indexes_l = initialisation(copy,ps,100)
    values_indexes = get_valuesv2(indexes_l, value)
    bests_indexes_value = get_bests(10,values_indexes)
    best_indexes = get_indexes_from_best(bests_indexes_value)
    croisement(best_indexes,poids_sac,liste,value)
    #boolean = weights_evaluation(best_indexes[0], poids_sac, liste)
    #value_evaluation(best_indexes[0], best_indexes[1], value)
    #print(boolean)
    #print(best_indexes)


if __name__ == '__main__':
    main()
