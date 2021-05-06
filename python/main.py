import os
import time
import numpy as np

from scipy.io import mmread
from scipy.linalg import norm
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

from sksparse.cholmod import cholesky

for filename in os.listdir('../matrixes/'):
    if filename.endswith(".mtx"):
        print('Analysing ' + filename + ' ...')

        # Read the matrix
        A = mmread('../matrixes/' + filename)
        A = csc_matrix(A)
        
        #create array [1...1]
        size = A.shape[0]        
        xe = np.ones(size)

        #create b
        b = A*xe
        
        start = time.perf_counter()
    
        try:
            # Cholesky
            factor = cholesky(A)
            x = factor(b)

        except Exception as e:
            # Ops. You can't use Cholesky.
            x = spsolve(A, b)
            pass

        stop = time.perf_counter()
        fntime = stop - start
        print(fntime)
        erel = norm(x - xe) / norm(xe)
        print(erel)