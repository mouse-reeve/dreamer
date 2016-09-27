''' define a starter corpus '''
import json
from os import path

cwd = path.abspath(path.dirname(__file__))
def load_file(filename):
    ''' open a corpus file '''
    return json.load(file('%s/corpus/%s' % (cwd, filename)))

nouns = load_file('nouns.json')
proper_nouns = load_file('proper_nouns.json')
transitive_verbs = load_file('transitive_verbs.json')
intransitive_verbs = load_file('intransitive_verbs.json')
determiners = load_file('determiners.json')
