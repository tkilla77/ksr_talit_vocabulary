# Define vocabulary unit
voci_unit = [
    {'translation': {'word1':"Baum", 'word2': "tree"}, 'correct': 0, 'incorrect': 0},
    {'translation': {'word1':"Blume", 'word2': "flower"}, 'correct': 0, 'incorrect': 0},
    {'translation': {'word1':"Fisch", 'word2': "fish"}, 'correct': 0, 'incorrect': 0},
]
 
# Make three passes
for _ in range(3):
    for w in voci_unit:
        if w['translation']['word2'] == input(f"Translate {w['translation']['word1']}: "):
            w['correct']+=1
            print("correct")
        else:
            w['incorrect']+=1
            print("incorrect")
 
# Print statistics
for w in voci_unit:
    print(f'{w['correct']/(w['correct']+w['incorrect']):.0%}: {w['translation']}')
