w1 = input("Enter a string:  ")
w2 = input("Enter another string:  ")
w3 = input("Enter a final string:  ")

words = [w1]
if len(w2) <= len(w1):
    words.insert(0, w2)
else:
    words.append(w2)

if len(w3) <= len(w1):
    words.insert(0, w3)
elif len(w3) <= len(w2):
    words.insert(1, w3)
else:
    words.append(w3)

print(words)
