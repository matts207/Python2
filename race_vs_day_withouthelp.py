tot_black_inmates = 0
tot_white_inmates = 0

total_inmates = 0

days = []
dictionary = []

with open('9-18.csv','r') as jail_file:
    key = jail_file.readline().split(',')
    lines = jail_file.readlines()
    [days.append(row.rstrip('\n').split(',')) for row in lines if row.split(',')[1] == '2018-09-01']
    #in-line if statement splitting up the data in the row if the date is correct
    #in-line for loop adding those dates to the list 'd'
    [dictionary.append(dict(zip(key, k))) for k in days]
    #in-line for loop adding the dicts


for d in dictionary:
    total_inmates += 1

for row in dictionary:
    if row['Date'] == '2018-09-01':
        if row['Race'] == 'B':
            tot_black_inmates += 1
        if row['Race'] == 'W':
            tot_white_inmates += 1



w_percentage = tot_white_inmates/total_inmates * 100
b_percentage = tot_black_inmates/total_inmates * 100


print("There are %s black inmates." % tot_black_inmates)
print("There are %s white inmates." % tot_white_inmates)
print("%.2f percent of inmates are black and only %.2f percent of inmates are white." % (b_percentage,w_percentage))
print("Allegheny County's population is 84.33 percent white and only 12.41 percent black.")
