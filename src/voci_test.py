from voci import *

unit = VocabularyUnit([
    WordPair('Baum', 'tree'),
    WordPair('Blume', 'flower'),
    WordPair('Fisch', 'fish')
])

learner = ConsoleLearner()
learner.learn(unit)
unit.print_stats()
