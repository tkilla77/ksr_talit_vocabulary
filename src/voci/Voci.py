import random
class WordPair:
    """A pair of words in two languages."""
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2
    
    def __str__(self):
        return f'{self.word1}'

class Stats:
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
    
    def total(self):
        return self.correct + self.incorrect
    
    def successRate(self):
        return self.correct / self.total()
    
    def record(self, correct):
        if correct:
            self.correct += 1
        else:
            self.incorrect += 1
    
    def __str__(self):
        return f'{self.successRate()} ({self.correct}/{self.total()})'
    
class VocabularyUnit:
    """A vocabulary unit to learn, consisting of a set of word pairs."""
    def __init__(self, pairs):
        self.pairs = pairs
        self.stats = {}
    
    def record(self, pair, correct):
        self.stats.setdefault(pair, Stats()).record(correct)
    
    def printStats(self):
        for pair, stats in self.stats.items():
            print(f'{pair}: {stats}')

class LearningStrategy:
    def __init__(self, unit):
        self.unit = unit

    def testPair(self, pair):
        response = input(f'Translate "{pair.word1}": ')
        correct = response == pair.word2
        self.unit.record(pair, correct)
        if correct:
            print('Correct!')
        else:
            print(f'Incorrect, the translation is "{pair.word2}"')
        return correct
    
    def learn(self):
        """Performs a single learning run."""
        for pair in self.unit.pairs:
            self.testPair(pair)
        self.unit.printStats()

class RandomStrategy(LearningStrategy):
    def __init__(self, unit):
        super().__init__(unit)
    
    def learn(self):
        for pair in random.sample(self.unit.pairs, len(self.unit.pairs)):
            self.testPair(pair)
        self.unit.printStats()

