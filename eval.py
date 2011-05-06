# Tocho Tchev's eval script

USAGE="python eval.py gold predictions"

import sys

def main():
    assert len(sys.argv) == 3

    data = [[zip(xrange(1, 1000), map(int, entry.strip().split()))
            for entry in dataset]
            for dataset in zip(*map(open, sys.argv[1:3]))]
    print set(data[0][0])

    directional = [len(set(gold).intersection(prediction)) / float(len(gold))
                   for (gold, prediction) in data]

    def sortit(gold):
        return [tuple(list(sorted(pair))) for pair in gold]
    undirectional = [(len(set(sortit(gold)).intersection(sortit(prediction))) / float(len(gold)))
                    for (gold, prediction) in data]

    print ("Scores(dir;undir): %0.2f%% ; %0.2f%%" % 
            tuple([100*sum(l)/len(l) for l in [directional, undirectional]]))
        

if __name__ == '__main__':
    main()
