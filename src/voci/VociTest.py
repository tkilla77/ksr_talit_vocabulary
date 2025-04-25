from Voci import *

unit = VocabularyUnit(
    [
        WordPair('Baum', 'tree'),
        WordPair('Blume', 'flower'),
        WordPair('Fisch', 'fish'),
    ]
)

strategy = RandomStrategy(unit)
strategy.learn()