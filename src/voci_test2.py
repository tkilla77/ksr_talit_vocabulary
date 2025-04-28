from voci import *

filename = 'data/test.voci'
unit = VocabularyUnit.read_from(filename)

learner = ConsoleLearner()
learner.learn(unit)
unit.print_stats()

unit.save_to(filename)