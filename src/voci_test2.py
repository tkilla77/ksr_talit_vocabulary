from voci import *

unit = VocabularyUnit.read_from('data/test.voci')

learner = ConsoleLearner()
learner.learn(unit)
unit.print_stats()

unit.save_to('data/test.voci')