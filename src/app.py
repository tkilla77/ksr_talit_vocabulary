from flask import Flask, jsonify, render_template
from voci import *

app = Flask(__name__)

filename = '../data/test.voci'
the_unit = VocabularyUnit.read_from(filename)
strategy = ScoreStrategy()
criterion = None

def find_unit(unit):
    return the_unit # FIXME

@app.route('/<user>/<unit>/word')
def word(user, unit):
    voci_unit = find_unit(unit)
    if not voci_unit:
        return 404, "No such unit"
    return jsonify(strategy.select(voci_unit).word1)

def find_pair(unit, word1):
    for pair in unit.pairs:
        if pair.word1 == word1:
            return pair
    return None

@app.route('/<user>/<unit>/submit/<word1>/<word2>')
def submit(user, unit, word1, word2):
    voci_unit = find_unit(unit)
    if not voci_unit:
        return 404, f"Unit '{unit}' does not exist"
    pair = find_pair(voci_unit, word1)
    if not pair:
        return 404, f"Word '{word1}' does not exist"
    correct = pair.test(word2)
    return jsonify({'correct': correct, 'answer': word2, 'pair': pair._to_dict()})

@app.route('/<user>/<unit>/')
def learn(user, unit):
    voci_unit = find_unit(unit)
    if not voci_unit:
        return 404, f"Unit '{unit}' does not exist"
    return render_template('learn.html')

