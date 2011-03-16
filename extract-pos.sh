# remove phrasal nodes, terminals
cat $1 | sed 's/(/((/g;s/([^()]\+ (//g;s/[^ ()]\+)//g;s/[()]//g;s/ \+/ /g;s/^ \+//' | grep '[A-Za-z]' > training-postags-line.txt

# only with < 10 tags
cat training-postags-line.txt | awk '{if (NF<11) print}' > training-postags-line-10.txt

# generate all dependencies
cat training-postags-line-10.txt |  awk '{for (i=1;i<NF;i++) {print "ROOT",$i; for (j=i+1;j<NF;j++) {print $i,$j; print $j,$i}}}' > pos10alldeps.txt

# sort and count it
less pos10alldeps.txt | sort | uniq -c | sort -g -r -k 1 | head

