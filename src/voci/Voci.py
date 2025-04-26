import random
class WordPair:
    """A pair of words in two languages."""
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2
    
    def __str__(self):
        return f'{self.word1} -> {self.word2}'

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
        return f'{self.successRate():4.0%} ({self.correct}/{self.total()})'
    
class VocabularyUnit:
    """A vocabulary unit to learn, consisting of a set of word pairs."""
    def __init__(self, pairs):
        self.pairs = pairs
        self.stats = {}
    
    def record(self, pair, correct):
        self.stats.setdefault(pair, Stats()).record(correct)
    

class ConsoleLearner:
    def __init__(self, unit, strategy):
        self.unit = unit
        self.strategy = strategy

    def learn(self):
        """Learn words."""
        print("\033c", end="") # clear console
        for pair in self.strategy.select(self.unit):
            self.testPair(pair)

    def testPair(self, pair):
        response = input(f'Translate "{pair.word1}": ')
        print("\033[H\033[J", end="")  # erase line
        correct = response == pair.word2
        self.unit.record(pair, correct)
        if correct:
            print('Correct!')
        else:
            print(f'Incorrect, the translation of "{pair.word1}" is "{pair.word2}"')
        return correct

    def printStats(self):
        for pair, stats in self.unit.stats.items():
            print(f'{stats} {pair}')

class SimpleStrategy:
    def __init__(self, passes=1):
        self.passes = passes

    def select(self, unit):
        """Simply selects all word pairs in the unit."""
        return unit.pairs * self.passes

class RandomStrategy:
    """Learning strategy that uniformly samples from all word pairs"""
    def __init__(self, passes=1):
        self.passes = passes

    def select(self, unit):
        return random.sample(unit.pairs*self.passes, len(unit.pairs)*self.passes)

