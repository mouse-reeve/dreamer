''' generate dreams '''
from dreamer import corpus
import re
import tracery
from tracery.modifiers import base_english

class Dream(object):
    ''' define the components of a dream '''

    types = ['general', 'sex', 'flight', 'nightmare']
    grammars = {
        'general': [
            '#S2#',
            '#S2#, but then #S32#',
            'You #VP# as #S3#',
            '#S2# but then it #VBZ# #NP#',
            'It seems like #S32#, or perhaps it #VBZ# you'],
        'sex': '#S2#',
        'flight': '#S2#'
    }


    def __init__(self, dream_type='general'):
        # merge general nouns with specific types for a complete nounlist
        nounlists = [corpus[n] for n in corpus.keys() if n[0:3] == 'NN:']
        nouns = [i for nouns in nounlists for i in nouns]

        self.rules = {
            'S2': ['You #VP# #NP#'],# 2nd-person sentence pattern
            'S3': ['#NP# #VPZ# #NP#'],# 3rd-person sentence pattern
            'S32': ['#NP# #VPZ# you'],# 3rd-person to 2nd-person
            'VP': ['#RBP# #VB#'],
            'VPZ': ['#RBP# #VBZ#'],
            'NP': ['#DTP# #JP# %s' % n for n in nouns] +
                  corpus['NNP'] + ["person with a #animal# head"],
            # --- 50% chance adjective or adverb is used --- #
            'JP': ['', '#JJ#'],
            'RBP': ['', '#RB#'],
            # --- prefer a/an articles --- #
            'DTP': ['a', '#DT#'],
            # --- straight from the corpus --- #
            'VB': corpus['VB'],
            'VBZ': corpus['VBZ'],
            'DT': corpus['DT'],
            'JJ': corpus['JJ'],
            'RB': corpus['RB'],
            'animal': corpus['NN:animal']
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
        return format_dream(self.grammar.flatten('#start#'))


def format_dream(dream):
    ''' remove formatting quirks '''
    # double spaces are produced by optional adjectives/adverbs
    dream = re.sub('  ', ' ', dream)

    # get the right a/an to match nouns
    return re.sub(r' a ([aeiou])', r' an \1', dream)
