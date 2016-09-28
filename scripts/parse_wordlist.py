''' prune the wordlist to something useful '''
import json
import re
import sys

raw = open(sys.argv[1])

wordset = {}
while True:
    line = raw.readline()
    if not line:
        break

    # [word, lemma, PoS, freq]
    line = line.split('\t')
    try:
        lemma = line[1]
        freq = int(line[3].strip())
    except IndexError:
        pass

    # I dunno what the ? words are about
    if freq > 100 and not '?' in lemma:
        pos = line[2]
        try:
            json.dumps([lemma])
        except UnicodeDecodeError:
            continue

        # words are already lemmatized, verb tense markers don't matter
        if re.match('^VB', pos):
            pos = 'VB'

        wordset[pos] = [lemma] if not pos in wordset else wordset[pos] + [lemma]
        wordset[pos] = list(set(wordset[pos]))

print json.dumps(wordset)
