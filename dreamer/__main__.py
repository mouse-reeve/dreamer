''' generate dreams '''
import tracery
from tracery.modifiers import base_english
from dreamer import corpus

class Dream(object):
    ''' define the components of a dream '''

    rules = {
        'start': '#noun.capitalize# #verb#',
        'noun': corpus.nouns,
        'verb': ['coagulates', 'dissapates']
    }

    def __init__(self):
        self.grammar = tracery.Grammar(self.rules)
        self.grammar.add_modifiers(base_english)

    def dream(self):
        ''' create a dream based on provided words '''
        return self.grammar.flatten('#start#')

