import random
class WordPair:
    """A pair of words in two languages, with learning statistics."""
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2
        self.stats = Stats()
    
    def record(self, correct):
        self.stats.record(correct)
        
    def __str__(self):
        return f'{self.stats} {self.word1} -> {self.word2}'

class Stats:
    """Learning statistics for a single word pair."""
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
    
    def total(self):
        """The number of attempts."""
        return self.correct + self.incorrect
    
    def success_rate(self):
        """The fraction of successful attempts."""
        return self.correct / self.total()
    
    def record(self, correct):
        """Records a single attempt."""
        if correct:
            self.correct += 1
        else:
            self.incorrect += 1
    
    def __str__(self):
        return f'{self.success_rate():4.0%} ({self.correct}/{self.total()})'
    
class VocabularyUnit:
    """A vocabulary unit to learn, consisting of a set of word pairs."""
    def __init__(self, pairs):
        self.pairs = pairs
    
class ConsoleLearner:
    """A vocabulary prompter for the console (terminal)."""
    def __init__(self, unit, strategy):
        self.unit = unit
        self.strategy = strategy

    def learn(self):
        """Performs a single learning run on the learner's unit using the configured
           learning strategy."""
        print("\033c", end="") # clear console
        for pair in self.strategy.select(self.unit):
            self.test_pair(pair)

    def test_pair(self, pair):
        """Asks for a single word and tests for correctness, recording the outcome."""
        response = input(f'Translate "{pair.word1}": ')
        print("\033[H\033[J", end="")  # erase line
        correct = response == pair.word2
        pair.record(correct)
        if correct:
            print('Correct!')
        else:
            print(f'Incorrect, the translation of "{pair.word1}" is "{pair.word2}"')
        return correct

    def print_stats(self):
        for pair in self.unit.pairs:
            print(f'{pair}')

class SimpleStrategy:
    """A learning strategy that selects all word pairs in a unit, in order.
       Optionally, the number of passes can be set."""
    def __init__(self, passes=1):
        self.passes = passes

    def select(self, unit):
        return unit.pairs * self.passes

class RandomStrategy:
    """A learning strategy that selects a uniform random sample from all word pairs."""
    def __init__(self, passes=1):
        self.passes = passes

    def select(self, unit):
        return random.sample(unit.pairs*self.passes, len(unit.pairs)*self.passes)

