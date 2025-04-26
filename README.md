# Object-Oriented Programming

## TODO
  * Missing:
    * testing
    * packages
    * visibility
    * iterators: use `__next__` in the strategy
    * inheritance

## TOC
What is the problem? 
  * show code using list<list<string>> to model a vocabulary
  * need to group data and behavior
  * internal vs. external
  * skip for now: inheritance

Refer to objects already known:
  * strings
  * lists
  * dicts

We want to create our own classes!
  * basic class syntax & naming conventions
  * `__init__` and `self`
  * instance methods

Special methods:
  * `__str__`
  * if time allows: [container types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types)

## Syllabus
### Lesson 1
  * problem statement (see above)
    * first class modeling: identify "natural" classes
      * Translation: WordPair
      * List of translations: VocabularyUnit
      * Code asking me for words: ConsoleLearner
  * my first class: a word pair for a vocabulary trainer
    * use a list as unit for now
    * write a simple trainer for the console - why not a class `ConsoleTrainer`?

### Lesson 2
  * introducing statistics
    * what do we need? counters for corrects vs. incorrect attempts, per word pair.
    * class modeling: a 'Statistics' class!
    * where do we add it - per word-pair!
    * record the result of a single test
    * print statistics after a learning run

### Lesson 3
  * Learning strategy: outsource two things from the learner:
    1. the order of the learnt pairs
    1. the decision on when to stop
  * Implement a `SimpleStrategy` that iterates through the words for a
    configurable number of passes.
  * Implement a `RandomStrategy` that shuffles the words.

### Lesson 4
  * Implement a `EfficientStrategy` that serves words randomly but weighted by how bad the statistics are for each word pair.

### Lesson 5
  * Storage: store vocabularies including stats
  * JSON / CSV.

### Lesson 6
  * Extensions
    * TkLearner showing a gui
    * 
