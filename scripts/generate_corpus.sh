#!/bin/bash

source venv/bin/activate
python scripts/trimwordlist.py scripts/ANC-written-lemma.txt | jq . >> dreamer/corpus/corpus.json
deactivate
