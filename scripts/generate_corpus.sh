#!/bin/bash

source venv/bin/activate
python scripts/parse_wordlist.py scripts/ANC-written-lemma.txt | jq . > dreamer/corpus/corpus.json
deactivate
