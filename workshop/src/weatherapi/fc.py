import csv

# favorite_cities = []
with open('resources/fc.txt', 'r') as fc:
    # reader = csv.reader(fc)
    # for row in reader:
    #     favorite_cities.extend(row)
    favorite_cities = fc.read().split(',')

print(favorite_cities)

favorite_cities.append('London')

with open('resources/fc.txt', 'w') as fc:
    for idx, i in enumerate(favorite_cities):
        if idx != len(favorite_cities) - 1:
            fc.write(i + ',')
        else:
            fc.write(i)