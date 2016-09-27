''' generate dreams '''
import tracery
from tracery.modifiers import base_english
from dreamer import corpus

class Dream(object):
    ''' define the components of a dream '''

    rules = {
        'start': '#nounpart.capitalize# #transitive_verb# #nounpart#',
        'nounpart': '#determiner# #noun#',
        'noun': corpus.nouns,
        'transitive_verb': corpus.transitive_verbs,
        'determiner': corpus.determiners
    }

    def __init__(self):
        self.grammar = tracery.Grammar(self.rules)
        self.grammar.add_modifiers(base_english)

    def dream(self):
        ''' create a dream based on provided words '''
        return self.grammar.flatten('#start#')

