import numpy as np

def calculate_divided_differences(x_points, y_points):
    """
    Calculate divided differences for Newton interpolation.
    
    Args:
        x_points (array-like): x coordinates
        y_points (array-like): y coordinates
        
    Returns:
        list: List of lists containing divided differences
    """
    n = len(x_points)
    # Initialize table with zeros
    table = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # Fill in the first column with f(x) values
    for i in range(n):
        table[i][0] = y_points[i]
    
    # Calculate divided differences
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1]) / (x_points[i + j] - x_points[i])
    
    return table