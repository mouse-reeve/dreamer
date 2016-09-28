''' generate dreams '''
import tracery
from tracery.modifiers import base_english
from dreamer import corpus

class Dream(object):
    ''' define the components of a dream '''

    types = ['general', 'sex', 'flight', 'nightmare']
    grammars = {
        'general': '#noun.capitalize# #verb#s #noun#',
        'sex': 'You #verb# #noun#',
        'flight': '#noun.capitalize# #verb# #noun#'
    }


    def __init__(self, dream_type='general'):
        self.rules = {
            'noun': ['#determiner# %s' % n for n in corpus.nouns] +
                    corpus.proper_nouns,
            'verb': corpus.verbs,
            'determiner': corpus.determiners
        }
        self.set_type(dream_type)


    def set_type(self, dream_type):
        ''' set the vocabulary and grammar for a given type of dream '''

        # check that the provided type is known
        if not dream_type in self.types:
            raise KeyError('Invalid dream type. Valid types are: %s' %
                           ', '.join(self.grammars.keys()))

        self.dream_type = dream_type
        self.rules['start'] = self.grammars[dream_type] \
                              if dream_type in self.grammars else \
                              self.grammars['general']

        # reset tracery grammar for new patterns and words
        self.grammar = tracery.Grammar(self.rules)
        self.grammar.add_modifiers(base_english)


    def get_type(self):
        ''' check dream type '''
        return self.dream_type


    def dream(self):
        ''' create a dream based on provided words '''
        return self.grammar.flatten('#start#')
