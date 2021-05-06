import os
import time
from scipy.io import mmread
from scipy.sparse.linalg import spsolve
from numpy import ones
from scipy.sparse import csc_matrix
from sksparse.cholmod import cholesky
from scipy.linalg import norm
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigs

""" def check_symmetric(a, rtol=1e-05, atol=1e-08):
    return np.allclose(a, a.T, rtol=rtol, atol=atol)
def isPSD(A, tol=1e-8):
    E = np.linalg.eigvalsh(A)
    return np.all(E > -tol)
def check_PSD(L):
    origin_L = L.todense() + L.T.todense() - np.diag(L.diagonal())
    E, V = linalg.eigh(origin_L)
    return np.all(E > -1e-10)


def is_pos_def(x):
    return check_PSD(x)
    #return isPSD(x)
    #return np.all(eigs(x) > 0)

def is_sym(x):
    return check_symmetric(x)
    #return x.traspose() == x """

for filename in os.listdir('../matrixes/'):
    if filename.endswith(".mtx"):
        print('Analysing ' + filename + ' ...')

        # Read the matrix
        A = mmread('../matrixes/' + filename)
        A = csc_matrix(A)
        
        #create array [1...1]
        size = A.shape[0]        
        xe = ones(size)

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