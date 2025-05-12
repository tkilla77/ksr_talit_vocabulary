import random, datetime
class WordPair:
    """A pair of words in two languages, with learning statistics."""
    def __init__(self, word1, word2):
        self.word1 = word1
        self.word2 = word2
        self.stats = Stats()
    
    def record(self, correct):
        """Records the result of a single learning attempt."""
        self.stats.record(correct)
    
    def test(self, guess):
        correct = guess == self.word2
        self.record(correct)
        return correct
        
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
    def __init__(self):
        self.index = 0

    def select(self, unit):
        pair = unit.pairs[self.index % len(unit.pairs)]
        self.index += 1
        return pair

class RandomStrategy:
    """A learning strategy that selects a random pair from all word pairs."""
    def select(self, unit):
        return random.choice(unit.pairs)

class ScoreStrategy:
    """A learning strategy that selects a random word pair weighted by inverse score."""
    def select(self, unit):
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

class CountingStopCriterion:
    """A stop criterion that stops after a given number of tries."""
    def __init__(self, n):
        self.count = n
    
    def should_stop(self, unit):
        """Returns False if learning should continue, a string explaining why we're done otherwise."""
        self.count -= 1
        if self.count >= 0:
            return "Enough for now!"
        return False

class TimerCriterion:
    """A stop criterion that stops after a given session duration (a timedelta)."""
    def __init__(self, duration):
        self.end = datetime.datetime.now() + duration

    def should_stop(self, unit):
        if datetime.datetime.now() > self.end:
            return "Time's up!"
        return False

class ScoreCriterion:
    """A stop criterion that stops when the least score in the unit is above the given threshold."""
    def __init__(self, threshold):
        self.threshold = threshold

    def should_stop(self, unit):
        for pair in unit.pairs:
            if pair.stats.score < self.threshold:
                return False
        return f"Good enough - all words above {self.threshold:.0%}!"  # all pairs above

class OrCriterion:
    """A stop criterion that combines multiple criteria and stops if at least one
       criterion is satisfied."""
    def __init__(self, *criteria):
        self.criteria = criteria
    
    def should_stop(self, unit):
        for criterion in self.criteria:
            reason = criterion.should_stop(unit)
            if reason:
                return reason
        return False

class LearningRun:
    """An iterator on top of learning strategy and stop criterion."""
    def __init__(self, unit, strategy, criterion):
        self.unit = unit
        self.strategy = strategy
        self.criterion = criterion
        self.last = None
    
    def __iter__(self):
        return self
    
    def __next__(self):
        reason = self.criterion.should_stop(self.unit)
        if reason:
            print(reason)
            raise StopIteration(reason)
        pair = self.strategy.select(self.unit)
        while pair == self.last and len(self.unit.pairs) > 1:
            pair = self.strategy.select(self.unit)
        self.last = pair
        return pair

class ConsoleLearner:
    """A vocabulary prompter for the console (terminal)."""
    def __init__(self, strategy=ScoreStrategy()):
        self.strategy = strategy

    def clear_console(self):
        """Clears the entire terminal window (console)."""
        # see https://en.wikipedia.org/wiki/ANSI_escape_code
        print("\033c", end="")
    
    def clear_line(self):
        """Clears the current line in the terminal."""
        # see https://en.wikipedia.org/wiki/ANSI_escape_code
        print("\033[H\033[J", end="")

    def learn(self, unit, criterion=None):
        """Performs a single learning run on the learner's unit using the configured
           learning strategy and stopping when the criterion is satisfied.
           
           If no criterion is given, the run stops if either one minute has passed
           or all words have a score >= 90%."""
        if criterion is None:
            # Default criterion: stop after 1m or if all scores above 90%
            criterion = OrCriterion(TimerCriterion(datetime.timedelta(minutes=1)),
                                    ScoreCriterion(0.9))
        learning_run = LearningRun(unit, self.strategy, criterion)
        self.clear_console()
        for pair in learning_run:
            self.test_pair(pair)

    def test_pair(self, pair):
        """Asks for a single word and tests for correctness, recording the outcome."""
        response = input(f'Translate "{pair.word1}": ')
        self.clear_line()
        if pair.test(response):
            print('Correct!')
        else:
            print(f'Incorrect, the translation of "{pair.word1}" is "{pair.word2}"')
