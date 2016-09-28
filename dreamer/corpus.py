''' define a starter corpus '''
import json
from os import path

cwd = path.abspath(path.dirname(__file__))
corpus = json.load(file('%s/corpus/corpus.json' % cwd))

nouns = corpus['NN']
proper_nouns = corpus['NNP']
verbs = corpus['VB']
determiners = corpus['DT'] + corpus['WDT']
