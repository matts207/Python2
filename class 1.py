python2class = {
    "Name": "Coral",
    "Age": 37,
    "bevsPerWeek": 0,
    "pets": {'cockatiel': "Phoebe",
             'cockatiel': "Pepper",
             'parakeet': 'Francis',
             'chinchilla': 'Princess Eleanor Rubidium Chinchillington III'},
    'typeCar': ('2010 Subaru Forester', '1999 Honda CRV')}


keys = python2class.keys()
print(keys)
key = input("Enter the name of the key you'd like to see.  ")
while key not in keys:
    key = input("Error. Try again.  ")


print(python2class[key])
