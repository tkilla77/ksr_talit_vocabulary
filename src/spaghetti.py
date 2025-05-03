v = [
    [["Baum", "tree"], 0, 0],
    [["Blume", "flower"], 0, 0],
    [["Fisch", "fish"], 0, 0],
]
 
for _ in range(3):
    for w in v:
        w1, w2 = w[0]
        if w2 == input(f"Translate {w1}: "):
            w[1]+=1
            print("correct")
        else:
            w[2]+=1
            print("incorrect")
for w in v:
    print(f'{w[1]/(w[1]+w[2]):.0%}: {w[0]}')
