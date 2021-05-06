import os
import csv
import time
import numpy as np

from scipy.io import mmread
from scipy.linalg import norm
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

from sksparse.cholmod import cholesky

from memory_profiler import memory_usage

def sparse_solve(A,b):

    chol = True
    start = time.perf_counter()
    try:
        # Cholesky
        factor = cholesky(A)
        x = factor(b)
        
    except Exception as e:
        # Ops. You can't use Cholesky.
        chol = False
        # Use spsolve
        x = spsolve(A, b)   

    finally:
        stop = time.perf_counter()
        fntime = stop - start
        erel = norm(x - xe) / norm(xe)

    return [chol, fntime, erel]
    
with open('../reports/python.csv', 'w+', newline='') as file:
    writer = csv.writer(file)
    # Set csv header 
    writer.writerow(["Matrix", "Cholesky", "Time", "Memory", "RelError"])
    
    for filename in os.listdir('../matrixes/'):
        
        if filename.endswith(".mtx"):
            print('Analysing ' + filename + ' ...')

            # Read the matrix
            A = mmread('../matrixes/' + filename)
            A = csc_matrix(A)
            
            # Create array [1...1]
            size = A.shape[0]        
            xe = np.ones(size)

            # Create b
            b = A*xe
            
            # Solve
            (mem_usage, [chol, tot_time, erel]) = memory_usage((sparse_solve, (A, b)), retval=True)
                
            mem_usage = max(mem_usage)
            writer.writerow([filename, chol, tot_time, mem_usage, erel])
            #print(time)     
            #print(erel)
            #print(chol)
            #print(mem_usage)
            