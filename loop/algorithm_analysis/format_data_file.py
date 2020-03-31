import csv

with open('movie_lens_data/movieLens.data') as input_file:
    lines = input_file.readlines()
    newLines = []
    for line in lines:
        newLine = line.strip().split()
        newLines.append(newLine)

with open('movie_lens_data/movieLens.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(newLines)
