import csv

tot_black_inmates = 0
tot_white_inmates = 0


with open('9-18.csv', newline='') as censusfile:
    reader = csv.DictReader(censusfile)
    for row in reader:
        if row['Date'] == '2018-09-01':
            if row['Race'] == 'B':
                tot_black_inmates += 1
            if row['Race'] == 'W':
                tot_white_inmates += 1


print(tot_black_inmates,tot_white_inmates)

'''censusfile = open('9-18.csv',newline='')
reader = csv.DictReader(censusfile)

for row in reader:
    if row['Date'] == '2018-09-01':
        if row['Race'] == 'B':
            tot_black_inmates += 1
        if row['Race'] == 'W':
            tot_white_inmates += 1

print(tot_black_inmates,tot_white_inmates)
'''
