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
    tmp = liste[0].copy()
    for _ in range(population):
        while 0 not in bags or len(liste[0])==0:
            if len(liste[0]) > 1:
                random = randomized(len(liste[0])-1)
            else:
                random = randomized(0)
            
            if len(liste[0]) == 0:
                break
            elements = list(zip(*liste))[random]
            for it,element in enumerate(elements):
                if element[0] <= bags[it]:
                    indexes.append(random)
                    bags[it] -= element[0]
                if element in liste[0]:
                    list[0].pop(random)
        for numbers in set(indexes):
            if indexes.count(numbers) == 5:
                solution.append(numbers)
        indexes = list()
        solutions.append(solution)
        solution = list()
    for element in solutions:
        print(element)
    return solutions
    

def main():
    liste, poids = file_reader('Instances/100M5_1.txt')
    #print(liste, poids)
    print(initialisation(liste, poids,10))


if __name__ == '__main__':
    main()
