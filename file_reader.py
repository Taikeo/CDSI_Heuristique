import itertools


def file_reader(file):
    final_list, backpack_poids, value, poids, tmp = list(), list(), list(), list(), list()
    k = 0
    with open(file, 'r') as f:
        lines = [line for line in f if line.strip()]
        for iteration, line in enumerate(lines):
            if iteration == 0:
                n, m = line.split()
                n = int(n)
                m = int(m)
            if iteration > 0 and iteration <= n/10:
                value.append(line.split())
            if iteration > n/10 and k < m/10:
                poids.append(line.split())
                k = k+1
            if iteration > n/10+1:
                backpack_poids.append(line.split())
        merged_poids = list(itertools.chain.from_iterable(poids))
        merged_value = list(itertools.chain.from_iterable(value))
        flatten_backpack_poids = list(itertools.chain.from_iterable(backpack_poids))
        chunks = [flatten_backpack_poids[x:x+n]
                  for x in range(0, len(flatten_backpack_poids), 100)]
        for elements in chunks:
            for i in range(len(elements)):
                tmp.append((int(elements[i]), int(merged_value[i])))
            final_list.append(tmp)
            tmp = list()
        merged_poids = [int(x) for x in merged_poids]
    print(f'n = {n} | m = {m}')
    print(f'poids = {merged_poids}')
    print(f'value = {merged_value}')
    print(f'final = {final_list}')


file_reader('Instances/100M5_11.txt')
