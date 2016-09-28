''' initialize dreamer package '''
import json
from os import path

cwd = path.abspath(path.dirname(__file__))
corpus = json.load(file('%s/corpus/corpus.json' % cwd))

from dreamer import dream
