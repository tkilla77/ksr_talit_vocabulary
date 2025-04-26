from Voci import *

unit = VocabularyUnit(
    [
        WordPair('Baum', 'tree'),
        WordPair('Blume', 'flower'),
        WordPair('Fisch', 'fish'),
    ]
)

learner = ConsoleLearner(unit, RandomStrategy())
learner.learn(passes=3)
learner.printStats()