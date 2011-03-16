: ${1?"Usage: $0 grammar lexicon corpus"}

run=99
#cp $1 $1.$run
#cp $2 $2.$run

while [ "$run" -lt 200 ]
do
  echo "start run $run"
  ./BitPar/src/bitpar -s S $1.$run $2.$run $3 -em em
  run=$((run + 1))
  less em.gram | grep -v '\<0.00\>' > $1.$run
  less em.lex | grep -v '\<0.00\>' > $2.$run
  diff $1.$run em.gram | head -20
done

