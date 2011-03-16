#!/usr/bin/python

from collections import defaultdict

import argparse

if __name__ == '__main__':
    help = {
        'b':    'build grammar in bitpar format',
        'd':    'convert dependency grammar to CFG',
        'g':    'gold file',
        'l':    'build a lexicon',
        'o':    'file to output a CFG to',
        's':    'score',
        'v':    'verbose output',
        'w':    'add weights and pseudo-counts',
        'y':    'yield file to manipulate'
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bitpar', action='store_const', default=False, const=True, help=help['b'])
    parser.add_argument('-d', '--dependency-grammar', type=str, help=help['d'])
    parser.add_argument('-l', '--build-lexicon', type=str, help=help['l'])
    parser.add_argument('-o', '--output-cfg', nargs='?', default='cfg_grammar',
        help=help['g'])
    parser.add_argument('-g', '--gold', type=str, help=help['g'])
    parser.add_argument('-s', '--score', type=str, help=help['s'])
    parser.add_argument('-v', '--verbose', action='store_const', default=False, 
        const=True, help=help['v'])
    parser.add_argument('-w', '--weights', action='store_const', default=False, 
        const=True, help=help['w'])
    parser.add_argument('-y', '--yield-file', type=str, help=help['y'])

    args = parser.parse_args()

cfg_min = False 
with_counts = True
uniform_counts = True
root = 'ROOT'

def log(str):
    print('[INFO] %s' % str)

def main():
    bitpar = args.bitpar
    dep = args.dependency_grammar
    gold = args.gold
    gram = args.output_cfg
    lex = args.build_lexicon
    verbose = args.verbose
    weights = args.weights
    _yield = args.yield_file
    score = args.score

    if dep:
        # we're converting
        dep_file = open(dep, 'r')

        rules = defaultdict(int)
        lhs_count = defaultdict(float)
        if verbose:
            log('split-head encoding grammar')
        for i, line in enumerate(dep_file):
            if with_counts:
                c, l, r = line.split()
            else:
                l, r = line.split()
            new_rules = []
            if l == root:
                # root is argument as l, head as r
                if cfg_min:
                    new_rules = [
                        tuple(['S', 'X_' + r]),
                        tuple(['X_' + r, 'L_' + r, r + '_R']),
                        tuple(['L_' + r, r + '_l']),
                        tuple([r + '_R', r + '_r'])
                    ]
                else:
                    new_rules = [
                        tuple(['S', 'X_' + r]),                 # S -> X_H
                        tuple(['X_' + r, 'L_' + r, 'R_' + r]),  # X_H -> L_H R_H
                        tuple(['L_' + r, r + '_l']),            # L_H -> H_L
                        tuple(['L_' + r, 'L1_' + r]),           # L_H -> L^1_H
                        tuple(['Lp_' + r, r + '_l']),           # L'_H -> H_L
                        tuple(['Lp_' + r, 'L1_' + r]),          # L'_H -> L^1_H
                        tuple(['R_' + r, r + '_r']),            # R_H -> H_R
                        tuple(['R_' + r, 'R1_' + r]),           # ...
                        tuple(['Rp_' + r, r + '_r']),           # 
                        tuple(['Rp_' + r, 'R1_' + r]),          # 
                    ]
            else:
                if cfg_min:
                  new_rules = [
                      tuple(['L_' + r, 'X_' + l, 'L_' + r]),
                      tuple(['R_' + r, 'R_' + r, 'X_' + l])
                  ]
                else:
                    new_rules = [
                        # argument as l, head as r, L^1_H -> X_A L'_H
                        tuple(['L1_' + r, 'X_' + l, 'Lp_' + r]), 
                        # argument as r, head as l, R^1_H -> R'_H X+A
                        tuple(['R1_' + r, 'Rp_' + r, 'X_' + l])
                    ]
            for new_rule in new_rules:
                if with_counts:
                    rules[new_rule] = int(c)
                else:
                    rules[new_rule] += 1
                lhs_count[new_rule[0]] += 1
            if verbose and i % 100 == 0:
                log('line: %d, last added rule: %s, with count: %d' % (i, 
                    new_rules[-1], rules[new_rules[-1]]))
        dep_file.close()

        if verbose:
            log('writing %d unique rules to %s' % (len(rules), gram))

        out_file = open(gram, 'w')
        total_count = float(sum(rules.values()))
        total_weight = 0
        for rule in sorted(rules.iterkeys()):
            count = 1 if uniform_counts else rules[rule]
            weight = count/lhs_count[rule[0]]
            total_weight += weight
            if bitpar:
                line = '%d %s %s\n' % (count, rule[0], ' '.join(rule[1:]))
            else:
                # format for Johnson io
                # '[Weight [Pseudocount]] Parent --> Child1 ... Childn'
                line = '%s --> %s\n' % (rule[0], ' '.join(rule[1:]))
                if weights:
                   line = '%.3f 0 %s' % (weight, line)
            out_file.write(line)
        out_file.close()
        if verbose:
            log('total weight: %f >> 1' % (total_weight))
    if _yield and not add:
        # we're dupping
        if verbose:
            log('duplicating output for yield file %s' % y)
            log('output format "w1 w2" => "w1_l w1_r w2_l w2_r"')
        yield_file = open(_yield, 'r')
        out_file = open(_yield + '.dup', 'w')

        for line in yield_file:
            words = line.split()
            line = ''
            for word in words:
                if len(line):
                    line += ' '
                line += '%s_l %s_r' % (word, word)
            out_file.write(line+'\n')
        yield_file.close()
        out_file.close()
    if lex:
        # we're creating a lexicon and corpus
        if verbose:
            log('creating lexicon from %s' % lex)
        lex_file = open(lex, 'r')

        lexicon = defaultdict(int)
        out_file = open(lex + '.corp', 'w')
        for line in lex_file:
            for word in line.split():
                lexicon[word] += 1
                out_file.write('"%s"\n' % word)
            out_file.write('\n')
        lex_file.close()
        out_file.close()

        out_file = open(lex + '.lex', 'w')
        for word in sorted(lexicon.iterkeys()):
            out_file.write('"%s"\t%s %d\n' % (word, word, lexicon[word]))
        out_file.close()
    if score and gold:
        gold_file = open(gold, 'r')
        our_file = open(score, 'r')
        score = 0
        size = 0
        for line in our_file:
            size += 1
            line = line.split()
            gold = gold_file.readline().split()
            num = 0.0
            for i, pos in enumerate(line):
                if pos == gold[i]:
                    num += 1
            score += num/len(line)
        score /= size
        print "score %0.5f" % score
        gold_file.close()
        our_file.close()
main()
