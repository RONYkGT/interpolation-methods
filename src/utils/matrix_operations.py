import numpy as np

def solve_linear_system(A, b):
    """
    Solve linear system Ax = b using numpy.
    
    Args:
        A (array-like): Coefficient matrix
        b (array-like): Right-hand side vector
        
    Returns:
        numpy.ndarray: Solution vector
    """
    return np.linalg.solve(A, b)

def compute_matrix_product(A, B):
    """
    Compute matrix product of A and B.
    
    Args:
        A (array-like): First matrix
        B (array-like): Second matrix
        
    Returns:
        numpy.ndarray: Matrix product
    """
    return np.dot(A, B)

def compute_matrix_transpose(A):
    """
    Compute transpose of matrix A.
    
    Args:
        A (array-like): Input matrix
        
    Returns:
        numpy.ndarray: Transposed matrix
    """
    return np.transpose(A)