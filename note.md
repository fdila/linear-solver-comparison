# Note

## Matlab
MATLAB usa una versione di SuiteSparse dell'anteguerra, e usa Fortran BLAS.
Riconosce da solo che tipo di matrice deve risolvere.
Usa le cose di SuiteSparse (visto con spumoni).

algoritmo strano MA57 per ifiss, qualcuno dice che è LDL

## Octave
Come matlab, riconosce tipo di matrici e usa SuiteSparse (visto con spumoni).

## Py
Per le matrici non cholesky chiama spsolve.
Se c'è scikit-umfpack chiama quello (https://people.engr.tamu.edu/davis/suitesparse.html)
Altrimenti chiama SuperLU, metodo gssv (https://github.com/xiaoyeli/superlu_dist_base/blob/master/SRC/bak/xgssv.base.bak)

Per le matrici cholesky usiamo CHOLMOD (sempre da SuiteSparse).

Scikit non funziona su win.

## Altre cose
Sarebbe interessante testare una versione recente con MKL BLAS (come suggerito dell'autore della libreria SuiteSparse).
Provato scikit-intel ma non funziona con le librerie per le matrici sparse.
Octave usa una versione più recente, ma usa sempre Fortran BLAS.
