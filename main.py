from solution import try_to_solve, read_file
from scoring import JudgeSystem
from os import listdir

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

FILES = sorted(map(lambda f: f.split('.')[0], listdir(INPUT_FOLDER)))
INPUT_FILES = list(map(lambda f: f'{INPUT_FOLDER}/{f}.in', FILES))
OUTPUT_FILES = list(map(lambda f: f'{OUTPUT_FOLDER}/{f}.out', FILES))

total = 0
for input_file, output_file in zip(INPUT_FILES, OUTPUT_FILES):
    params, ride = read_file(input_file)
    try_to_solve(params, ride, output_file)
    j = JudgeSystem(input_file, output_file)
    score = int(j.score)
    total += score
    print(f'Scored {score} points with {input_file}')

print(f'Total: {total} points')
