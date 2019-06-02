import sys
sys.path.append('./modules/')

from collections import defaultdict
from docopt import docopt
import logging
import time
import codecs
import numpy as np
from scipy.sparse import dok_matrix, csr_matrix
from composes.semantic_space.space import Space
from composes.matrix.sparse_matrix import SparseMatrix


def main():
    """
    Get second-order pairs from pair file.
    """

    # Get the arguments
    args = docopt("""Get second-order pairs from pair file.

    Usage:
        second_order_pairs.py <pairFile> <samplesize> <freqThr> <outPath>
        
    Arguments:
       
        <pairFile> = path to training pairs with each line in the format 'word1 word2'
        <samplesize> = number new pairs, expressed as percentage of old pairs (1.0 extracts equally many new pairs as old pairs)
        <freqThr> = co-occurrence frequency threshold over which no pairs are extracted
        <outPath> = output path for extracted pairs

    Note:
        Pairs are not yet switched or shuffled.

    """)
    
    pairFile = args['<pairFile>']
    samplesize = float(args['<samplesize>'])
    freqThr = int(args['<freqThr>'])
    outPath = args['<outPath>']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()


    # Build vocabulary
    logging.info("Building vocabulary")
    freqs = defaultdict(int)      
    targets = set()
    contexts = set()
    with codecs.open(pairFile, 'r', 'utf-8') as f_in:
        for line in f_in:
            line = line.strip().split(' ')
            word = line[0]
            freqs[word] += 1
            contextWord = line[1]
            targets.add(word)
            contexts.add(contextWord)
   
    vocabulary = targets.union(contexts)
    w2i = {w: i for i, w in enumerate(vocabulary)}
    
    # Initialize co-occurrence matrix as dictionary
    cooc_mat = defaultdict(lambda: 0)

    # Get counts
    logging.info("Counting context words")
    with codecs.open(pairFile, 'r', 'utf-8') as f_in:
        for line in f_in:
            line = line.strip().split(' ')
            word = line[0]
            windex = w2i[word]
            contextWord = line[1]
            cindex = w2i[contextWord]
            cooc_mat[(windex,cindex)] += 1

    
    # Convert dictionary to sparse matrix
    logging.info("Converting dictionary to matrix")
    cooc_mat_sparse = dok_matrix((len(vocabulary),len(vocabulary)), dtype=float)
    try:
        cooc_mat_sparse.update(cooc_mat)
    except NotImplementedError:
        cooc_mat_sparse._update(cooc_mat)

    # Make space
    vocabulary = [v.encode('utf-8') for v in vocabulary]
    countSpace = Space(SparseMatrix(cooc_mat_sparse), vocabulary, vocabulary)
    id2row = countSpace.get_id2row()
    row2id = countSpace.get_row2id()
    id2column = countSpace.get_id2column()
    column2id = countSpace.get_column2id()
    cid2rid = {cid:row2id[c] for cid, c in enumerate(id2column) if c in row2id}

    space = countSpace
    matrix = space.get_cooccurrence_matrix().get_mat()
    t2c = {}
    # Sample new pairs
    logging.info("Sampling new pairs")
    for i, target in enumerate(id2row):
        freq = freqs[target.decode('utf8')]
        if freq > freqThr:
            continue
        # Get counts as matrix        
        m = space.get_row(target).get_mat()
        # Get nonzero indexes
        nonzeros = list(m.nonzero()[1])
        if nonzeros == []:
            continue
        data = m.data
        # build second-order vector
        contextrowids = [cid2rid[n] for n in nonzeros]
        contextrows = matrix[contextrowids]
        vector2nd = csr_matrix(contextrows.multiply(data.reshape(-1,1)).sum(axis=0))
        # sample from second-order vector
        nonzeros = list(vector2nd.nonzero()[1])        
        if nonzeros == []:
            continue
        data = vector2nd.data
        sampling_probs = data/np.sum(data)
        samplesize_absolute = int(samplesize*freq)
        t_contexts = list(np.random.choice(nonzeros, size=samplesize_absolute, replace=True, p=sampling_probs))
        t2c[target] = [id2column[c] for c in t_contexts if id2column[c]!=target]

    # Export new pairs
    logging.info("Exporting new pairs")    
    with codecs.open(outPath, 'w') as f_out:
        for t in t2c:
            for c in t2c[t]:
                f_out.write(' '.join((t,c))+'\n')
   
     
    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
