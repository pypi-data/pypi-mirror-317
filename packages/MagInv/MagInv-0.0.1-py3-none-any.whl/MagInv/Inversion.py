import numpy as np
from scipy.sparse import spdiags

def CalPreM(A, SQS, na):
    """
    Computes the preconditioner matrix M.

    Parameters:
    A : 2D numpy array
        Input matrix (analogous to G).
    SQS : 2D numpy array
        Matrix used in the inversion process.
    na : int
        Number of rows in matrix A (analogous to n in the original problem).

    Returns:
    M : sparse matrix (diagonal)
        Preconditioner matrix.
    """
    m = np.zeros(na)
    
    for i in range(na):
        d = A[i, :]
        m[i] = 1.0 / (d @ SQS @ d.T)  # Compute the inverse for each row
    
    M = spdiags(m, 0, na, na)
    
    return M

def PreCG(A, SQS, D, f, M, igmax, delta):
    """
    Solves the system ASQS'A'x = f using the preconditioned conjugate gradient method.
    
    Parameters:
    A : 2D numpy array
        Matrix A (m x n).
    SQS : 2D numpy array
        Matrix SQS (n x n), which is a product of diagonal matrices S and Q.
    D : 2D numpy array
        Regularization matrix (m x m).
    f : 1D numpy array
        Right-hand side vector (m dimensional).
    M : 2D numpy array (or sparse matrix)
        Preconditioner matrix (m x m).
    igmax : int
        Maximum number of iterations.
    delta : float
        Tolerance for convergence (based on residual).
    
    Returns:
    x0 : 1D numpy array
        Solution vector (m dimensional).
    """
    r0 = -f
    y0 = M @ r0
    p0 = -y0
    k = 0
    x0 = np.zeros_like(r0)
    
    res = (r0.T @ r0) / len(r0)
    
    while k < igmax and res > delta:
        Ap = A @ (SQS @ (A.T @ p0)) + D @ p0
        a0 = (r0.T @ y0) / (p0.T @ Ap)
        x0 = x0 + a0 * p0
        r1 = r0 + a0 * Ap
        y1 = M @ r1
        b0 = (r1.T @ y1) / (r0.T @ y0)
        p0 = -y1 + b0 * p0
        
        k += 1
        res = (r1.T @ r1) / len(r0)
        r0 = r1
        y0 = y1
        
        if k % 10 == 0:
            print(f"Iteration {k} : RMS {res}")
    
    return x0

def Inversion(G, Q, D, obs, delta, itmax, igmax, method=1):
    """
    Solve the inversion problem using an iterative method (conjugate gradient).
    
    Parameters:
    G : 2D numpy array
        The sensitivity matrix (data kernel).
    Q : 2D numpy array
        Covariance matrix.
    D : 1D numpy array
        Unknown vector.
    obs : 1D numpy array
        Observed data.
    delta : float
        Tolerance for the residual.
    itmax : int
        Maximum number of iterations.
    igmax : int
        Maximum number of iterations for the inner CG solver.
    method : int
        Method to use (1 or 2).
    
    Returns:
    model : 1D numpy array
        Inverted model parameters.
    """
    n, m = G.shape
    mk = np.ones(m) * 0.0001  # Initial guess for model parameters
    
    if method == 1:
        dres = obs - G @ mk
    elif method == 2:
        dres = obs - G @ (mk ** 2)
    else:
        raise ValueError("Method must be 1 or 2")
    
    res = (dres.T @ dres) / n
    S = spdiags(np.ones(m), 0, m, m)  # Diagonal matrix
    
    k = 0
    print(res)
    
    while k < itmax and res > delta:
        SQS = S @ Q @ S.T
        if method == 1:
            f = obs - G @ mk
        elif method == 2:
            f = obs - G @ (mk**2)
        
        M = CalPreM(G, SQS, n)
        print(f"CG iteration {k}")
        x0 = PreCG(G, SQS, D, f, M, igmax, delta)
        
        m0 = mk.copy()
        dm = Q @ S.T @ G.T @ x0
        
        mk = m0 + dm
        
        if method == 1:
            dres1 = obs - G @ mk
        elif method == 2:
            dres1 = obs - G @ (mk ** 2)
        
        res1 = (dres1.T @ dres1) / n
        
        while res1 > res:
            dm /= 3.0
            mk = m0 + dm
            if method == 1:
                dres1 = obs - G @ mk
            elif method == 2:
                dres1 = obs - G @ (mk ** 2)
            res1 = (dres1.T @ dres1) / n
        
        S = spdiags(2 * mk, 0, m, m)
        res = res1
        k += 1
    
    model = mk**2
    return model
