movies = {
    "The Usual Suspects": {
        "Release Date": "Sep 15 1995",
        "Stars (IMDB)": 8.6,
        "Actors": {
            "Stephen Baldwin": {
                "Character": "McManus",
                "Year Born": 1966,
                "Height": "5'10''"},
            "Kevin Spacey (eww)": {
                "Character":  "Kaiser Souzai",
                "Year Born": 1959,
                "Height": "5'10''"}
            }
        },
    "The Shawshank Redemption": {
        "Release Date": "Oct 14 1994",
        "Stars (IMDB)": 9.3,
        "Actors": {
            "Morgan Freeman": {
                "Character": "	Ellis Boyd 'Red' Redding",
                "Year Born": 1937,
                "Height": "6'2''"},
            "Tim Robbins": {
                "Character":  "Andy Dufresne",
                "Year Born": 1958,
                "Height": "6'5''"}

    }
}}


def test(dictionary):
    for key in dictionary:
        print(key)
    keys = dictionary.keys()
    choose(dictionary, keys)


levels = []
keys = []


def choose(dictionary, keys):
    if levels == []:
        key = input("Type the name of the key you'd like to select:  ")
    else:
        key = input("Type the name of the key you'd like to select or type \"B\" to go back:  ")
    while key not in keys:
        key = input("Type the name of the key you'd like to select:  ")
    print("What would you like to do with %s" % key)
    choice = input("Enter O to Open, E to Edit, D to Delete:  ")
    while choice != "O" and choice != "E" and choice != "D" and choice != "B":
        choice = input("""Follow directions. Please select an actual option!
          Enter O to Open, E to Edit, D to Delete""")
    if choice == "O" and levels == []:
        levels.append(key)
        open(dictionary, key)
    elif choice == "O" and len(levels) == 1:
        levels.append(key)
        open1(dictionary, levels[0], key)
    elif choice == "O" and len(levels) == 2:
        levels.append(key)
        open2(dictionary, levels[0], levels[1], key)
    elif choice == "O" and len(levels) == 3:
        levels.append(key)
        open3(dictionary, levels[0], levels[1], levels[2], key)
    elif choice == "E":
        edit(dictionary, key)
    elif choice == "D":
        delete(dictionary, key)
    elif choice == "B":
        pass


def open(dictionary, key):
    keys = list(dictionary[key])
    for k in keys:
        print(k)
    choose(dictionary, keys)


def open1(dictionary, key1, key2):
    if type(dictionary[key1][key2]) is not type(dictionary):
        print(dictionary[key1][key2])
    else:
        keys = list(dictionary[key1][key2])
        for k in keys:
            print(k)
        choose(dictionary, keys)


def open2(dictionary, key1, key2, key3):
    if type(dictionary[key1][key2][key3]) is not type(dictionary):
        print(dictionary[key1][key2][key3])
    else:
        keys = list(dictionary[key1][key2][key3])
        for k in keys:
            print(k)
        choose(dictionary, keys)


def open3(dictionary, key1, key2, key3, key4):
    if type(dictionary[key1][key2][key3][key4]) is not type(dictionary):
        print(dictionary[key1][key2][key3][key4])
    else:
        keys = list(dictionary[key1][key2][key3][key4])
        for k in keys:
            print(k)
        choose(dictionary, keys)


def edit(dictionary, key):
    new = input("Enter the new value:  ")
    dictionary[key] = new
    keys = dictionary.keys()
    for k in keys:
        print(k)
    choose(dictionary, key)


def add(dictionary,key):
    add_key = input("Name your new key:  ")
    new_value = input("Enter the value:  ")
    dictionary.update(add_key=new_value)
    print(movies)

def edit1(dictionary, key1, key2):
    if type(dictionary[key1][key2]) is not type(dictionary):
        print(dictionary[key1][key2])
    else:
        keys = list(dictionary[key1][key2])
        for k in keys:
            print(k)
        choose(dictionary, keys)


def edit2(dictionary, key1, key2, key3):
    if type(dictionary[key1][key2][key3]) is not type(dictionary):
        print(dictionary[key1][key2][key3])
    else:
        keys = list(dictionary[key1][key2][key3])
        for k in keys:
            print(k)
        choose(dictionary, keys)


def edit3(dictionary, key1, key2, key3, key4):
    if type(dictionary[key1][key2][key3][key4]) is not type(dictionary):
        print(dictionary[key1][key2][key3][key4])
    else:
        keys = list(dictionary[key1][key2][key3][key4])
        for k in keys:
            print(k)
        choose(dictionary, keys)

def delete(dictionary,key):
    pass

def retry_open(dictionary, *keys):
    pass


test(movies)