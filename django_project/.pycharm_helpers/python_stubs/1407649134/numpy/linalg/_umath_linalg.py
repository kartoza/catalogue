# encoding: utf-8
# module numpy.linalg._umath_linalg
# from /usr/lib/python2.7/dist-packages/numpy/linalg/_umath_linalg.so
# by generator 1.138
# no doc
# no imports

# Variables with simple values

__version__ = '0.1.4'

# functions

def cholesky_lo(x, out=None): # real signature unknown; restored from __doc__
    """
    cholesky_lo(x[, out])
    
    cholesky decomposition of hermitian positive-definite matrices. 
    Broadcast to all outer dimensions. 
        "(m,m)->(m,m)"
    """
    pass

def det(x, out=None): # real signature unknown; restored from __doc__
    """
    det(x[, out])
    
    det of the last two dimensions and broadcast on the rest. 
        "(m,m)->()"
    """
    pass

def eig(x, out1=None, out2=None): # real signature unknown; restored from __doc__
    """
    eig(x[, out1, out2])
    
    eig on the last two dimension and broadcast to the rest. 
    Results in a vector with the  eigenvalues and a matrix with the eigenvectors. 
        "(m,m)->(m),(m,m)"
    """
    pass

def eigh_lo(x, out1=None, out2=None): # real signature unknown; restored from __doc__
    """
    eigh_lo(x[, out1, out2])
    
    eigh on the last two dimension and broadcast to the rest, using lower triangle 
    Results in a vector of eigenvalues and a matrix with theeigenvectors. 
        "(m,m)->(m),(m,m)"
    """
    pass

def eigh_up(x, out1=None, out2=None): # real signature unknown; restored from __doc__
    """
    eigh_up(x[, out1, out2])
    
    eigh on the last two dimension and broadcast to the rest, using upper triangle. 
    Results in a vector of eigenvalues and a matrix with the eigenvectors. 
        "(m,m)->(m),(m,m)"
    """
    pass

def eigvals(x, out=None): # real signature unknown; restored from __doc__
    """
    eigvals(x[, out])
    
    eigvals on the last two dimension and broadcast to the rest. 
    Results in a vector of eigenvalues. 
        "(m,m)->(m),(m,m)"
    """
    pass

def eigvalsh_lo(x, out=None): # real signature unknown; restored from __doc__
    """
    eigvalsh_lo(x[, out])
    
    eigh on the last two dimension and broadcast to the rest, using lower triangle. 
    Results in a vector of eigenvalues and a matrix with theeigenvectors. 
        "(m,m)->(m)"
    """
    pass

def eigvalsh_up(x, out=None): # real signature unknown; restored from __doc__
    """
    eigvalsh_up(x[, out])
    
    eigvalsh on the last two dimension and broadcast to the rest, using upper triangle. 
    Results in a vector of eigenvalues and a matrix with theeigenvectors.
        "(m,m)->(m)"
    """
    pass

def inv(x, out=None): # real signature unknown; restored from __doc__
    """
    inv(x[, out])
    
    compute the inverse of the last two dimensions and broadcast to the rest. 
    Results in the inverse matrices. 
        "(m,m)->(m,m)"
    """
    pass

def slogdet(x, out1=None, out2=None): # real signature unknown; restored from __doc__
    """
    slogdet(x[, out1, out2])
    
    slogdet on the last two dimensions and broadcast on the rest. 
    Results in two arrays, one with sign and the other with log of the determinants. 
        "(m,m)->(),()"
    """
    pass

def solve(x1, x2, out=None): # real signature unknown; restored from __doc__
    """
    solve(x1, x2[, out])
    
    solve the system a x = b, on the last two dimensions, broadcast to the rest. 
    Results in a matrices with the solutions. 
        "(m,m),(m,n)->(m,n)"
    """
    pass

def solve1(x1, x2, out=None): # real signature unknown; restored from __doc__
    """
    solve1(x1, x2[, out])
    
    solve the system a x = b, for b being a vector, broadcast in the outer dimensions. 
    Results in vectors with the solutions. 
        "(m,m),(m)->(m)"
    """
    pass

def svd_m(x, out=None): # real signature unknown; restored from __doc__
    """
    svd_m(x[, out])
    
    svd when n>=m.
    """
    pass

def svd_m_f(x, out1=None, out2=None, out3=None): # real signature unknown; restored from __doc__
    """
    svd_m_f(x[, out1, out2, out3])
    
    svd when m>=n
    """
    pass

def svd_m_s(x, out1=None, out2=None, out3=None): # real signature unknown; restored from __doc__
    """
    svd_m_s(x[, out1, out2, out3])
    
    svd when m>=n
    """
    pass

def svd_n(x, out=None): # real signature unknown; restored from __doc__
    """
    svd_n(x[, out])
    
    svd when n<=m
    """
    pass

def svd_n_f(x, out1=None, out2=None, out3=None): # real signature unknown; restored from __doc__
    """
    svd_n_f(x[, out1, out2, out3])
    
    svd when m>=n
    """
    pass

def svd_n_s(x, out1=None, out2=None, out3=None): # real signature unknown; restored from __doc__
    """
    svd_n_s(x[, out1, out2, out3])
    
    svd when m>=n
    """
    pass

# no classes
