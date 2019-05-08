from collections import namedtuple


Image = namedtuple('Image', ['id', 'type', 'tags'])


def read_file(filename):
    images = []

    with open(filename) as dataset:
        N = int(dataset.readline())

        for i, line in enumerate(dataset):
            data = line.split()
            type = data[0]
            tags = data[2:]

            images.append(Image(i, type, tags))
    
    return images