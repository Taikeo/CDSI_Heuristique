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
    """Création des population

    Args:
        listee (liste des valeurs): _description_
        bags (list): Liste des poids
        population (int): Nb de population

    Returns:
        list: Liste des populations
    """
    pp = list()
    baggy = [x for x in range(len(bags))] #Copie des listes
    solution,solutions,indexes = list(),list(),list()
    for _ in range(population):
        while True:
            if len(pp) == len(listee[0]): #On quitte quand on a atteint le max des valeurs
                break
            rand = random.randint(0,len(listee[0])-1)
            if rand in pp: #Eviter les doublons pour optimiser
                continue
            elements = list(zip(*listee))[rand] #On ajoute les elements par indice avec la fonction zip
            for it in range(len(elements)):
                if baggy[it] <= bags[it]: #On vérifie s'ils sont compliant pour chacun des sacs
                    indexes.append(rand)
                    baggy[it] += elements[it][0] #On retire le poids pour les vérifications
            pp.append(rand)
        pp = list()
        baggy = [0 for x in range(len(bags))] #On recopie les sacs
        for numbers in set(indexes):
            if indexes.count(numbers) == len(bags): #Si l'item apparait le nombre de sac (compliant sur tous les sacs) on l'ajoute
                solution.append(numbers)
        solutions.append(solution)
        solution = list()
        indexes = list()
    return solutions

def get_valuesv2(indexes,value):
    """Récupère les valeurs d'une liste sous format liste de liste

    Args:
        index (list de list): Liste de liste des indexs
        value (list): Liste des valeurs

    Returns:
        list: liste d'index et la somme de chacune des valeurs
    """
    l,liste = list(),list()
    for index in indexes:
        for i in index:
            l.append(int(value[i]))
        liste.append(l)
        l = list()
    return [(indexes[liste.index(x)], sum(x)) for x in liste]


def get_valuesv3(index, value):
    """Récupère les valeurs d'une liste sous format liste de liste

    Args:
        index (list): Liste des indexs
        value (list): Liste des valeurs

    Returns:
        list: liste d'index et la somme de chacune des valeurs
    """
    l, liste = list(), list()
    for i in index:
        l.append(int(value[i]))
    liste.append(l)
    tmp = [(index,sum(x)) for x in liste]
    return list(itertools.chain.from_iterable(tmp))

def get_bests(nb_of_best,values): 
    values.sort(key = lambda x: x[1], reverse = True) #On sort les liste d'indices avec une fonction lambda pour trier en fonction des valeurs et on trie en ascend 
    return values[:nb_of_best] #Return les nb_of_best meilleurs

def get_indexes_from_best(bests_indexes):
    return [x[0] for x in bests_indexes] #On ne récupère que les indices pour chacune des solutions

def weights_evaluation(bests_indexes,bags,liste):
    """Evaluation des poids s'ils sont compliant avec le poids de chaque sacs

    Args:
        bests_indexes (list): Liste de chaque solutions
        bags (list): Liste des poids de sacs
        liste (list): Liste de chacun des tuples (poids,valeurs)

    Returns:
        _type_: _description_
    """
    to_be_evaluated,tmp,sums,boolean = list(),list(),list(),list()
    for j in range(len(bags)):
        for i in range(len(bests_indexes)):
            tmp.append(liste[j][bests_indexes[i]][0])
        to_be_evaluated.append(tmp)
        tmp = list()
    sums = [sum(lists) for lists in to_be_evaluated]
    boolean = [True if sums[i] <= bags[i] else False for i in range(len(sums))]
    return False if False in boolean else True

def get_single_value(indexes,value):
    return sum([int(value[element]) for element in indexes]) #Retourne la somme des valeurs d'une solution
        
def value_evaluation(initial,rival,value):
    value1, value2 = get_single_value(initial, value), get_single_value(rival, value)
    return value1 if value1 >= value2 else value2

def croisement(best_indexes,bags,liste):
    """Croisement pour création des enfants, Fonctionnement: on slide en deux chacune des listes et on les mets ensemble, 
       on vérifie qu'elles soient compliant en terme de poids

    Args:
        best_indexes (list): Liste des meilleurs solutions
        bags (list): Liste des sacs (leurs poids)
        liste (list): Liste des poids/valeurs

    Returns:
        list: Liste des enfants compliant en poids
    """
    childs,child,accept = list(),list(), list()
    for i in range(len(best_indexes)):
        parent = best_indexes[i]
        for j in range(0,len(best_indexes)):
            child.append(parent[:len(parent)//2] + best_indexes[j][len(best_indexes[j])//2:])
        childs.append(child)
        child = list()
    for elements in childs:
        for element in elements:
            b = weights_evaluation(element, bags, liste)
            if b:
                if element not in accept:
                    accept.append(element)
    return accept

def lists(list1,list2):
    return list1,list2 #retourne deux listes en une

def compare_list_of_list(list1,list2,value,bests=10):
    """Comparaison de la liste parente et enfantes

    Args:
        list1 (list): Liste des parents
        list2 (list): Liste des enfants
        value (list): Liste des valeurs
        bests (int, optional): Nombre de meilleures solutions. Defaults to 10.

    Returns:
        _type_: _description_
    """
    p_list1, p_list2, indexes, p2_p1_list = list(), list(), list(), list()
    for element in list1:
        p_list1.append(get_valuesv3(element,value))
    mins = min(p_list1,key = lambda x: x[1])
    for element in list2:
        element = get_valuesv3(element,value)
        if element[1] >= mins[1]:
            p_list2.append(element)
    p1_p2_list = list(itertools.chain.from_iterable(lists(p_list1,p_list2))) #On crée une liste des parents et des enfants
    for element in p1_p2_list:
        if element not in p2_p1_list:
            p2_p1_list.append(element)
    for x in get_bests(bests, p2_p1_list):
        if x[0] not in indexes:
            indexes.append(x[0]) #On ajoute les X meilleurs dans la liste finale
    return indexes


def mutation(best,list_final,bags,mutation_chance=1,changing_chance=50):
    """Mutation d'un élément au hasard des liste avec une probabilité de mutation et une probabilité de changement

    Args:
        best (liste de liste d'int): Liste des index passable pour chacune solution
        list_final (list de liste de tuples): Liste total de chacun des sacs sous forme de tuples (poids,valeur)
        bags (list): Liste des poids des sacs
        mutation_chance (int, optional): Chance de mutation. Defaults to 1.
        changing_chance (int, optional): Chance de changement. Defaults to 50.

    Returns:
        list: Liste mutée ou non
    """
    l = list()
    for i in range(len(best)):
        element = best[i].copy()
        t1,t2, c1,c2 = random.choice(element), random.choice(list_final[0]), random.randint(1,100), random.randint(1,100)
        element[element.index(t1)] = list_final[0].index(t2)
        if weights_evaluation(element,bags,list_final) == True:
            if c1 <= mutation_chance and c2 <= changing_chance:
                l.append(element)
            else:
                l.append(best[i])
        else:
            l.append(best[i])
    return l

def output(liste,length):
    """Créer le fichier en 1 ligne de 0 et 1 

    Args:
        liste (list): liste d'index de la meilleur population
        length (int): Nombre de valeur en total
    """
    output = ""
    with open('output.txt', 'w') as f:
        for i in range(length):
            if i in liste:
                output+="1"
            else:
                output+="0"
        f.write(' '.join(output))
        
def main():
    
    ####### Définition des variables
    
    
    nombre_population = 100
    nombre_best_population = 10
    nombre_iteration = 1000
    probabilité_mutation = 1
    probabilité_changement = 50
    
    
    #####################
    
    
    ################## Initialisation

    
    liste, copy, poids_sac, value = file_reader('Instances/100M5_1.txt')
    ps = poids_sac.copy()
    indexes_l = initialisation(copy, ps, nombre_population)
    values_indexes = get_valuesv2(indexes_l, value)
    bests_indexes_value = get_bests(nombre_best_population, values_indexes)
    best_indexes = get_indexes_from_best(bests_indexes_value)

    ##################
    
    
    ########### Lancemenet d'un round
    
    
    childs = croisement(best_indexes,poids_sac,liste)
    new_bests = compare_list_of_list(best_indexes, childs, value, nombre_best_population)
    new_pop = mutation(new_bests, liste, poids_sac, probabilité_mutation, probabilité_changement)
    
    
    ############
    
    ######### Lancement des X itérations
    
    for _ in range(nombre_iteration):
        childs = croisement(new_pop,poids_sac,liste)
        new_bests = compare_list_of_list(new_pop, childs, value, nombre_best_population)
        new_pop = mutation(new_bests, liste, poids_sac,probabilité_mutation, probabilité_changement)
    
    ##########
    
    output(new_pop[0],len(value))
    print(new_pop[0],get_single_value(new_pop[0],value))

if __name__ == '__main__':
    main()
