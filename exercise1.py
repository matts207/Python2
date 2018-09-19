num1 = 10
num2 = 10

'''for i in list(range(0,num1)):
    for k in list(range(0,num2)):
        print(k,end='')
    num2-=1
    print('\n')'''


numbers = open('exercise1_answer.txt','w')
for i in list(range(0,num1)):
    for k in list(range(0,num2)):
        numbers.write(str(k))
    num2-=1
    numbers.write('\n')
numbers.close()

