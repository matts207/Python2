listoflists = [['mn','pa','ut'],['b','p','c'],['echo','charlie','tango']]
labels = {"state":"US State Abbr: ", "element":"Chemical Element: ", "alpha":"Phonetic Call: "}

for i in listoflists:
    for l in i:
        if len(l) == 1:
            print("%(element)s" % labels, l.upper())
        elif len(l) == 2:
            print("%(state)s" % labels, l.upper())
        else:
            print("%(alpha)s" % labels, l.upper())

