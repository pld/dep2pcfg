./BitPar/src/bitpar -v -s S cfg_grammar.$1 wsj10.txt.dup.lex.$1 wsj10.txt.dup.corp wsj10.txt.dup.parse
cat wsj10.txt.dup.parse | sed 's/\((L[^ ]\+\) /\1-H /g' | sed 's/\((R[^ ]\+\) /\1-H /g' | sed 's/^(S (\([^ ]\+\) /(S (\1-H /g' | sed 's/\(_[lr]\) /\1-H /g' > wsj10.txt.parse
python head2pairs.py wsj10.txt.parse > wsj10.txt.parse.pairs
python eval.py wsj10.txt.parse.pairs wsj10.txt.gold

