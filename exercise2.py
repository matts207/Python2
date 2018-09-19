file = open('names.txt','r')

names = []
for i in range(4):
    names.append(file.readline().rstrip('\n'))
fixed = []
for i in names:
    fixed.append(i.split())

for i in range(len(names)):
    print("Good evening Dr. %s. Would you mind if I call you %s" % (fixed[i][1],fixed[i][0]))