# Tocho Tchev's eval script

import sys

import pprint

from pyparsing import nestedExpr

pp = pprint.PrettyPrinter(indent=4)

def depgen(parse, parent, memory):
    if not isinstance(parse[1], list):
        return [(parse[0], memory, parent)]
    else:
        def determine_parent_memory(x):
            if '-H' in x[0]:
                return [parent, memory]
            else:
                return [memory, object()] 
        return sum([depgen(x,*determine_parent_memory(x)) 
                    for x in parse[1:]],[])
    return []


def output(line):
    txt = line.strip()

    parse = nestedExpr('(',')').parseString(txt).asList()[0]
    
    #print "\n\n"; pprint.pprint(parse)

    depstruct = depgen(parse, None, object())

    #pprint.pprint(depstruct)

    parents = [x[2] for x in depstruct]
    ids = [None] + [x[1] for x in depstruct]

    try:
        deps = [ids.index(p) for p in parents]
    except:
        pp.pprint(p)
        pp.pprint(ids)
        raise


    #assert deps[1::2]==deps[::2], deps
    #deps = [(d+1)/2 for d in deps[::2]]

    for i in range(0, len(deps)):
        if deps[i] > 0:        
            deps[i] = (deps[i]+1)/2
    print ' '.join(map(str, deps[::2]))
    """
    sentence = ([x[0] for x in depstruct])
    print ' '.join(sentence)
    for i,x in enumerate(sentence):
        print '%s(%s)' % (x, (["ROOT"] + sentence)[deps[i]]) ,
    else:
        print
    print
    """

def main():
# command line
    if len(sys.argv) == 2:
        in_path = sys.argv[1]
    else:
        in_path = '../parses'
    
    fin = open(in_path, 'r')
    
    while True:
        s = fin.readline()
        if len(s) == 0:
            break
        if s[0] != '(':
            t = ''
            s = s.split()
            for i in range(0, len(s)-3):
                t += '0 '
            print t[::4]
        else:
            output(s)


if __name__ == '__main__':
    main()
