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
        * **Pattern**: *Aggregation* (a unit groups many pairs; a pair can exist independent of the unit, or be part of multiple units, however)
        ```mermaid
        classDiagram
          class WordPair {
            word1
            word2
            reversed()
          }
          class VocabularyUnit {
            pairs
            print_stats()
          }
          VocabularyUnit o-- WordPair
        ```
      * Code asking me for words: ConsoleLearner
  * my first class: a word pair for a vocabulary trainer
    * use a list as unit for now
    * write a simple trainer for the console - why not a class `ConsoleTrainer`?

### Lesson 2
  * introducing statistics
    * what do we need? counters for corrects vs. incorrect attempts, per word pair.
    * class modeling: a 'Statistics' class!
    * where do we add it - per word-pair!
      * **Pattern**: *Composition*: a word-pair contains two words and a stats object, none of which exist independently from the pair.
      ```mermaid
        classDiagram
          class WordPair {
            word1
            word2
            reversed()
          }
          class Stats {
            correct
            incorrect
            score
            record(correct)
          }
          WordPair *-- Stats
      ```

    * record the result of a single test
    * print statistics after a learning run

### Lesson 3
  * Learning strategy: outsource two things from the learner:
    1. the order of the learnt pairs
    1. the decision on when to stop
  * Implement a `SimpleStrategy` that iterates through the words for a
    configurable number of passes.
  * Implement a `RandomStrategy` that shuffles the words.
  * **Pattern**: *Strategy*: multiple classes with the same interface, can be used to configure the functionality of our program without blowing up the main structure.
  * **Pattern**: *Inheritance*: a subclass of another class specializes it, but an objects of the subclass still *is a* member of the super class.
  ```mermaid
  classDiagram
    class SelectionStrategy {
      select(unit)
    }
    SelectionStrategy <|-- SimpleStrategy
    SelectionStrategy <|-- RandomStrategy
    SelectionStrategy <|-- ScoreStrategy
    
    ConsoleLearner --> SelectionStrategy
  ```


### Lesson 4
  * Implement a `ScoreStrategy` that serves words randomly but weighted by how bad the statistics are for each word pair.

### Lesson 5
  * Storage: store vocabularies including stats
  * JSON / CSV.
  * **Pattern**: *static methods*: functions that are independent of a class *instance* (object), but still belong to the class.

### Lesson 6
  * Extensions
    * TkLearner showing a gui
    * Decay: older attempts should contribute less weight to the score for each word pair than newer attempts. For example, we could compute the score by taking the average of the previous score and the current attempt (which is either 1 or 0 depending on correctness): $score = \frac{score + correct}{2}$
    * Support multiple translations for a word.
    * Web app for learning
