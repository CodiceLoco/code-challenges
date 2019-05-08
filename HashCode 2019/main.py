from sys import argv
from collections import namedtuple


Immagine = namedtuple('Immagine', ['id', 'verticale', 'tags'])
Slide = namedtuple('Slide', ['id_immagini', 'tags'])
Grafo = namedtuple('Grafo', ['slides', 'archi'])



def percorso(u, v, next):
   if next[u][v] == None:
       return []

   path = [u]
   while u != v:
       u = next[u][v]
       path.append(u)

   return path


def floyd_warshall_modddato(slides, archi):
    dist = [[arco if arco is not None else 0 for arco in row] for row in archi]
    next = [[j if i != j else None for j in range(len(slides))] for i in range(len(slides))]

    for k, slide_k in enumerate(slides):
        for i, slide_i in enumerate(slides):
            for j, slides_j in enumerate(slides):
                if i != j and dist[i][j] < dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next[i][j] = next[i][k]

    START, FINISH, max = -1, -1, 0
    for start, _ in enumerate(slides):
        for finish, _ in enumerate(slides):
            if dist[start][finish] > max:
                START, FINISH, max = start, finish, dist[start][finish]

    return percorso(START, FINISH, next)


def dijkstra_modddato(slides, archi):
    for x, row in enumerate(archi):
        for y, arco in enumerate(row):
            if arco == 0:
                archi[x][y] = None

    my_slides = [Slide([], [])] + slides + [Slide([], [])]
    my_archi = [[0 for _ in my_slides]] + [[0] + row + [0] for row in archi]

    dist = [0 for _ in my_slides]
    prev = [None for _ in my_slides]

    Q = {0}
    while len(Q) > 0:
        max, u = -1, -1
        for q in Q:
            if dist[q] > max:
                max = dist[q]
                u = q
        Q.remove(u)

        for v, peso in enumerate(my_archi[u]):
            if peso != None:
                alt = dist[u] + peso
                if alt > dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    Q.add(v)

    return dist, prev




def peso_transizione(slide_i, slide_j):
    peso = len(slide_i.tags & slide_j.tags)
    peso = min(peso, len(slide_i.tags - slide_j.tags))
    return min(peso, len(slide_j.tags - slide_i.tags))


def combina(verticali):
    slides = []
    for i in range(0, len(verticali), 2):
        tags = verticali[i].tags.union(verticali[i + 1].tags)
        ids = [verticali[i].id, verticali[i+1].id]
        slides.append(Slide(ids, tags))
    return slides


def crea_grafo(immagini):
    verticali = list(filter(lambda t: t.verticale, immagini))
    orizzontali = list(filter(lambda t: not t.verticale, immagini))

    slides = combina(verticali)
    slides += [Slide([img.id], img.tags) for img in orizzontali]

    archi = [[None for _ in slides] for _ in slides]

    for i, slide_i in enumerate(slides[:-1]):
        for J, slide_j in enumerate(slides[i+1:]):
            j = i + J + 1  # che belli gli indici
            archi[i][j] = archi[j][i] = peso_transizione(slide_i, slide_j)

    return Grafo(slides, archi)


if __name__ == '__main__':
    file_in_input = argv[1]
    immagini = []

    with open(file_in_input) as input_file:
        number_of_images = int(input_file.readline())

        id = 0
        for line in input_file:
            image = line.split(' ')
            image[-1] = image[-1][:-1]  # toglie il \n
            tags = set(image[2:])
            immagini.append(Immagine(id, image[0] == 'V', tags))
            id += 1

    slides, archi = crea_grafo(immagini)
    percorso = dijkstra_modddato(slides, archi)

    print(len(percorso))
    for slide_id in percorso:
        print(' '.join(str(i) for i in slides[slide_id].id_immagini))