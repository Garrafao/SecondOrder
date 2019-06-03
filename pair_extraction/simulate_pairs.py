import sys
sys.path.append('./modules/')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from docopt import docopt
import logging
import time
import codecs
import numpy as np
from scipy.stats import lognorm
from random import shuffle
from collections import defaultdict
from itertools import combinations


def main():
    """
    Simulate artificial pairs with 1st and 2nd order overlap.
    """

    # Get the arguments
    args = docopt("""Simulate artificial pairs with 1st and 2nd order overlap.

    Usage:
        simulate_pairs.py <tsize> <csize> <csamplesize> <outPath>
        
    Arguments:
       
        <tsize> = target set size
        <csize> = context set size
        <csamplesize> = context sample size
        <outPath> = output path

    Note:
        Pairs are not yet shuffled.

    """)
    
    tsize = int(args['<tsize>'])
    csize = int(args['<csize>'])
    csamplesize = int(args['<csamplesize>'])
    outPath = args['<outPath>']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # First order overlap targets
    targets1st = ['(target)' + '1st' + str(i) for i in range(tsize)]
    tcontexts1st = [['(tcontext)' + '1st' + str(i) for i in range(csize)] for target in targets1st]
    tcontexts1st2id = [{tcontext:j for j, tcontext in enumerate(tcontexts1st[i])} for i, target in enumerate(targets1st)]            
    ccontexts1st = [[[tcontext + '(ccontext)' + '1st' + str(i) for i in range(csize)] for tcontext in tcontexts] for tcontexts in tcontexts1st]
    
    # Second order overlap targets
    targets2nd = ['(target)' + '2nd' + str(i) for i in range(tsize)]
    tcontexts2nd = [[target + '(tcontext)' + '2nd' + str(i) for i in range(csize)] for target in targets2nd]
    tcontexts2nd2id = [{tcontext:j for j, tcontext in enumerate(tcontexts2nd[i])} for i, target in enumerate(targets2nd)]            
    ccontexts2nd = [[['(ccontext)' + '2nd' + str(i) for i in range(csize)] for tcontext in tcontexts] for tcontexts in tcontexts2nd]

    # No order overlap targets
    targetsNone = ['(target)' + 'None' + str(i) for i in range(tsize)]
    tcontextsNone = [[target + '(tcontext)' + 'None' + str(i) for i in range(csize)] for target in targetsNone]
    tcontextsNone2id = [{tcontext:j for j, tcontext in enumerate(tcontextsNone[i])} for i, target in enumerate(targetsNone)]            
    ccontextsNone = [[[tcontext + '(ccontext)' + 'None' + str(i) for i in range(csize)] for tcontext in tcontexts] for tcontexts in tcontextsNone]

    ## Generate pairs
    t2c = defaultdict(lambda: [])
    r = lognorm.rvs(1.0, size=csize)
    probs = r/np.sum(r)
    for (targets,tcontextss,tcontexts2id,ccontextss) in ((targets1st,tcontexts1st,tcontexts1st2id,ccontexts1st),(targets2nd,tcontexts2nd,tcontexts2nd2id,ccontexts2nd),(targetsNone,tcontextsNone,tcontextsNone2id,ccontextsNone)):
        shuffle(probs)
        for i in range(tsize):
            target, tcontexts, tcontext2id, ccontexts = targets[i], tcontextss[i], tcontexts2id[i], ccontextss[i]
            tcontextsample = np.random.choice(tcontexts, size=csamplesize, replace=True, p=probs)
            for tcontext in tcontextsample:
                t2c[target].append(tcontext)
                id = tcontext2id[tcontext]                
                ccontextsample = np.random.choice(ccontexts[id], size=csamplesize, replace=True, p=probs)
                for ccontext in ccontextsample:
                    t2c[tcontext].append(ccontext)
                    
    # Export pairs
    logging.info("Exporting pairs")    
    with codecs.open(outPath, 'w') as f_out:
        for t in t2c:
            for c in t2c[t]:
                f_out.write(' '.join((t,c))+'\n')   
                # Add switched pairs
                f_out.write(' '.join((c,t))+'\n')   

    # Export targets
    logging.info("Exporting targets")    
    with codecs.open(outPath+'-targets-1st', 'w') as f_out:
        for (t1,t2) in combinations(targets1st, 2):
                f_out.write('\t'.join((t1,t2))+'\n')   

    with codecs.open(outPath+'-targets-2nd', 'w') as f_out:
        for (t1,t2) in combinations(targets2nd, 2):
                f_out.write('\t'.join((t1,t2))+'\n')   

    with codecs.open(outPath+'-targets-None', 'w') as f_out:
        for (t1,t2) in combinations(targetsNone, 2):
                f_out.write('\t'.join((t1,t2))+'\n')
                
    # Export context samples
    logging.info("Exporting tcontexts")    
    with codecs.open(outPath+'-tcontexts-1st', 'w') as f_out:
        tcontexts = [c for t in tcontexts1st for c in t]        
        idx = list(np.random.choice(len(tcontexts), size=1000, replace=False))
        tcontexts = [tcontexts[i] for i in idx]
        combos = zip(tcontexts[:500],tcontexts[500:])
        for (t1,t2) in combos:
            f_out.write('\t'.join((t1,t2))+'\n')   

    with codecs.open(outPath+'-tcontexts-2nd', 'w') as f_out:
        tcontexts = [c for t in tcontexts2nd for c in t]        
        idx = list(np.random.choice(len(tcontexts), size=1000, replace=False))
        tcontexts = [tcontexts[i] for i in idx]
        combos = zip(tcontexts[:500],tcontexts[500:])
        for (t1,t2) in combos:
            f_out.write('\t'.join((t1,t2))+'\n')   

    with codecs.open(outPath+'-tcontexts-None', 'w') as f_out:
        tcontexts = [c for t in tcontextsNone for c in t]        
        idx = list(np.random.choice(len(tcontexts), size=1000, replace=False))
        tcontexts = [tcontexts[i] for i in idx]
        combos = zip(tcontexts[:500],tcontexts[500:])
        for (t1,t2) in combos:
            f_out.write('\t'.join((t1,t2))+'\n')
                
    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
