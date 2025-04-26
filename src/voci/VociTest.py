from Voci import *

unit = VocabularyUnit(
    [
        WordPair('Baum', 'tree'),
        WordPair('Blume', 'flower'),
        WordPair('Fisch', 'fish'),
    ]
)

learner = ConsoleLearner(unit, RandomStrategy(passes=3))
learner.learn()
learner.print_stats()