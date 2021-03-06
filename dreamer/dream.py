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
            # you're in a car and it kills a deer
            # you try to run but for some reason you sing instead
            # a fish befriends you and you eat it before it can report you
            # you meet a deer but for some reason it is dead
            '#filler# you are in #location# #event# and #S23#',
            '#filler# #S23# and then #event# try to #VB:motion# to #location#' \
                'but it #VBZ# #NP# so you can\'t',
            '#S23# #event#, but then #filler# #S32#',
            '#filler# #S32#, although #RB:hedge# it #VBZ# you #event# as well'
        ],

        'sex': [
            'You #VB:motion# to #location# with #humanoid#. #anysex# and then #p-o# until #reactP#'
        ],
        'flight': '#S23#'
    }


    def __init__(self, dream_type='general'):
        # merge general nouns with specific types for a complete nounlist
        corpus_keys = corpus.keys()
        nounlists = [corpus[n] for n in corpus_keys if n[0:3] == 'NN:']
        nouns = [i for nouns in nounlists for i in nouns]

        # computer 3rd person singular forms of verbs
        verbs_3rd = []
        for original in corpus['VB']:
            original = original.split(' ')
            verb = original[0]
            verb = re.sub(r'([sch])s$', r'\1ses', verb) #         kiss/kisses
            verb = re.sub(r'([aeiou])y$', r'\1ys', verb) #        enjoy/enjoys
            verb = re.sub(r'y$', r'ies', verb) #                  fly/flies
            verb = re.sub(r'o$', 'oes', verb) #                   go/goes
            verb = verb + 's' if verb == original[0] else verb # run/runs

            if len(original) > 1:
                verb = ' '.join([verb] + original[1:])
            original = ' '.join(original)

            verbs_3rd.append(verb)

        # principals of sentence formation
        self.rules = {
            'S23': ['you #VP# #NP#'],# 2nd-person sentence pattern
            'S33': ['#NP# #VPZ# #NP#'],# 3rd-person sentence pattern
            'S32': ['#NP# #VPZ# you'],# 3rd-person to 2nd-person
            'VP': ['#RBP# #VB#'],
            'VPZ': ['#RBP# #VBZ#'],
            'NP': ['#DTP# #JP# %s' % n for n in nouns] +
                  corpus['NNP'] +
                  ['#DTP# person with a #NN:animal# head',
                   '#DTP# #NN:animal# with a #NN:animal# head'],
            # --- 1/3 chance adjective or adverb is used --- #
            'JP': ['', '', '#JJ#'],
            'RBP': ['', '', '#RB#'],
            'flesh': ['', '#JJ:flesh#'],
            # --- prefer a/an articles --- #
            'DTP': ['a', '#DT#'],
            # --- generated verbs --- #
            'VBZ': verbs_3rd,
            # --- special structures --- #
            'location': [
                '#DT# #NN:location#',
                '#DT# #NN:location#',
                '#DT# #NN:location#',
                'your childhood home',
            ],
            'event': [
                '', '', '', '', '', '',
                'during a #NN:event#'
            ],
            # --- weird sex stuff --- #
            'anysex': ['#p-o#', '#o-p#', '#o-o#', '#p-p#'],
            'p-o': [
                'you #VB:insertion# your #flesh# #protrusion# #IN# their' \
                    ' #flesh# #orifice#',
            ],
            'o-p': [
                'they #VB:insertion# their #flesh# #protrusion# #IN# your' \
                    ' #flesh# #orifice#'
            ],
            'o-o': [
                'you #VB:touch# your #flesh# #orifice# #IN# their #flesh# #orifice#',
                'they #VB:touch# their #flesh# #orifice# #IN# your #flesh# #orifice#',
            ],
            'p-p': [
                'you #VB:touch# your #flesh# #protrusion# #IN# their #flesh# #protrusion#',
                'they #VB:touch# their #flesh# #protrusion# #IN# your #flesh# #protrusion#',
            ],
            'reactP': ['they #VB:react#', 'you both #VB:react#', 'you #VB:react# and they #VB:react#']
        }
        # --- simple parts of speech --- #
        for key in corpus_keys:
            self.rules[key] = corpus[key]

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
    # optional parts cause unwanted whitespace
    dream = dream.strip()
    dream = re.sub(r' +', ' ', dream)
    dream = re.sub(r' ,', ',', dream)

    # get the right a/an to match nouns
    dream = re.sub(r'(\b)a ([aeiou])', r'\1an \2', dream)

    return dream
