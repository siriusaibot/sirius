cities = {}
i = 0

with open("names.txt") as city_names:
    for line in city_names:
        line = line.split("\n")[0].split("||")
        cities["".join(line[0].split())] = line[1]


def translate(city):
    try:
        return cities["".join(city.split())]
    except:
        pass
