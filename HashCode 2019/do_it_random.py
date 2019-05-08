from sys import argv
from collections import namedtuple
from random import shuffle


Immagine = namedtuple('Immagine', ['id', 'verticale', 'tags'])
Slide = namedtuple('Slide', ['id_immagini', 'tags'])
Grafo = namedtuple('Grafo', ['slides', 'archi'])


def peso_transizione(slide_i, slide_j):
    peso = len(slide_i.tags & slide_j.tags)
    peso = min(peso, len(slide_i.tags - slide_j.tags))
    return min(peso, len(slide_j.tags - slide_i.tags))


def combina(verticali):
    slides = []
    shuffle(verticali)
    for i in range(0, len(verticali), 2):
        tags = verticali[i].tags.union(verticali[i + 1].tags)
        ids = [verticali[i].id, verticali[i+1].id]
        slides.append(Slide(ids, tags))
    return slides


def do_it_random(immagini):
    max_points, max = 0, []
    for _ in range(500):
        verticali = list(filter(lambda t: t.verticale, immagini))
        orizzontali = list(filter(lambda t: not t.verticale, immagini))

        slides = combina(verticali)
        slides += [Slide([img.id], img.tags) for img in orizzontali]

        shuffle(slides)

        points = 0
        for i, slide_i in enumerate(slides[:-1]):
            points += peso_transizione(slide_i, slides[i + 1])
        if points > max_points:
            max_points = points
            max = slides.copy()

    return max, points


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

    slides, points = do_it_random(immagini)

    print('points', points)
    print(len(slides))
    for slide in slides:
        print(' '.join(str(i) for i in slide.id_immagini))