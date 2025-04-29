import random
class WordPair:
    """A pair of words in two languages, with learning statistics."""
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2
        self.stats = Stats()
    
    def record(self, correct):
        """Records the result of a single learning attempt."""
        self.stats.record(correct)
        
    def __str__(self):
        return f'{self.stats} {self.word1} -> {self.word2}'
    
    def _to_dict(self):
        return {'word1': self.word1, 'word2': self.word2, 'correct': self.stats.correct, 'incorrect': self.stats.incorrect, 'score': self.stats.score}
    
    @staticmethod
    def _from_dict(data):
        import math
        pair = WordPair(data['word1'], data['word2'])
        if 'correct' in data:
            pair.stats.correct = data['correct']
        if 'incorrect' in data:
            pair.stats.incorrect = data['incorrect']
        if 'score' in data:
            pair.stats.score = data['score']
        elif not math.isnan(pair.stats.success_rate()):
            pair.stats.score = pair.stats.success_rate()
        return pair

class Stats:
    """Learning statistics for a single word pair."""
    def __init__(self):
        self.correct = 0
        self.incorrect = 0
        self.score = 0.0
    
    def total(self):
        """The number of attempts."""
        return self.correct + self.incorrect
    
    def success_rate(self):
        """The fraction of successful attempts."""
        import math
        return self.correct / self.total() if self.total() > 0 else math.nan
    
    def record(self, correct):
        """Records a single attempt."""
        if correct:
            self.correct += 1
        else:
            self.incorrect += 1
        self.score = 0.5 * (self.score + correct)
    
    def __str__(self):
        return f'{self.score:4.0%} ({self.correct}/{self.total()})'
    
class VocabularyUnit:
    """A vocabulary unit to learn, consisting of a set of word pairs."""
    def __init__(self, pairs):
        self.pairs = pairs

    def print_stats(self):
        for pair in sorted(self.pairs, key=lambda p:p.stats.score):
            print(f'{pair}')
    
    @staticmethod
    def read_from(filename):
        import json
        pairs = []
        with open(filename, 'r') as infile:
            for line in infile:
                data = json.loads(line)
                pairs.append(WordPair._from_dict(data))
        return VocabularyUnit(pairs)

    def save_to(self, filename):
        import json
        with open(filename, 'w') as out:
            for pair in self.pairs:
                json.dump(pair._to_dict(), out)
                out.write('\n')

class SimpleStrategy:
    """A learning strategy that selects all word pairs in a unit, in order."""
    def select(self, unit, i):
        return unit.pairs[i%len(unit.pairs)]

class RandomStrategy:
    """A learning strategy that selects a random pair from all word pairs."""
    def select(self, unit, i):
        return random.choice(unit.pairs)

class ScoreStrategy:
    """A learning strategy that selects a random word pair weighted by inverse score."""
    def select(self, unit, i):
        # WordPair scores are in the interval [0, 1), with exponential decay:
        # After a single correct answer, the score is at 0.5, after two correct at 0.75
        # after 7 attempts at 0.99. We choose weights such that a perfect pair still has a
        # non-zero chance of being chosen. Let's define 'non-zero' such that a perfect pair
        # (score 1) has 10% the chance of a pristine (score 0) pair:
        # weight(1.0) = 0.1 * weight(0.0) # perfect pairs have 10% the weight of zero pairs
        # weight(score) = b - score       # we want a linear function
        # b-1 = 0.1*(b-0)
        # 0.9b = 1
        # b = 1/0.9 = 1.11
        perfect_weight = 0.1  # 10%
        b = 1/(1-perfect_weight)
        return random.choices(unit.pairs, weights=[b-p.stats.score for p in unit.pairs])[0]

class ConsoleLearner:
    """A vocabulary prompter for the console (terminal)."""
    def __init__(self, strategy=ScoreStrategy()):
        self.strategy = strategy

    def learn(self, unit, count=None):
        """Performs a single learning run on the learner's unit using the configured
           learning strategy."""
        print("\033c", end="") # clear console
        if count is None:
            count = len(unit.pairs)
        last = None
        for i in range(count):
            pair = self.strategy.select(unit, i)
            # Avoid asking the same pair twice in a row.
            while pair == last and len(unit.pairs) > 1:
                pair = self.strategy.select(unit, i)
            last = pair
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

