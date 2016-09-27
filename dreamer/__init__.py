''' words to populate dreams '''
from os import path
import json

cwd = path.abspath(path.dirname(__file__))
def load_file(filename):
    ''' open a corpus file '''
    return json.load(file('%s/corpus/%s' % (cwd, filename)))

class Corpus(object):
    ''' create a starting corpus '''
    nouns = load_file('nouns.json')
    proper_nouns = load_file('proper_nouns.json')
    transitive_verbs = load_file('transitive_verbs.json')
    intransitive_verbs = load_file('intransitive_verbs.json')
    determiners = load_file('determiners.json')

corpus = Corpus()
