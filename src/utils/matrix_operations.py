from numpy import ones, ndarray, dot
from numpy.linalg import solve

def generate_vandermonde_matrix(x_values, degree):
    """
    Generate a Vandermonde matrix with the given x_values.
    Args:
    x_values (list): A list of x values.
    degree (int): The degree of the polynomial.
    Returns:
    A Vandermonde matrix (ndarray).
    """
    n = len(x_values)
    A = ones((n,degree+1))


    for row in range(0,n):
        x = x_values[row]
        for col in range(1,degree+1):
            A[row][col] = x**col
    return A

def generate_colvector_from_function(f: callable, x_values: list) -> ndarray:
    """
    Generate a column vector from a sympy expression.
    Args:
    f (sympy.Expr): A sympy expression.
    x_values (list): A list of x values.
    Returns:
    A column vector (ndarray).
    """
    result = ndarray((len(x_values),1))
    for i in range(len(x_values)):
        result[i] = f(x_values[i])
    return result

def solve_inconsistent_system(A_matrix, b_vector) -> ndarray:
    """
    Solve an inconsistent system of linear equations.
    Args:
    A_matrix (ndarray): A matrix of coefficients.
    b_vector (ndarray): A column vector of constants.
    Returns:
    A solution vector (ndarray).
    """
    # Create the A matrix and b vector
    A_norm = dot(A_matrix.T, A_matrix) #A^T . A
    b_norm = dot(A_matrix.T, b_vector) #A^T . b
    # Solve the normal equation
    solution = solve(A_norm, b_norm)
    return solution, A_norm, b_norm
    