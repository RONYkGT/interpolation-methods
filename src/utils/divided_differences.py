def calculate_divided_differences(x_points, y_points, n=0):
    """
    Calculate divided differences for x and y given.
    if n is left default, function will fully calculate the divided differences (len(x_points)-1 times).
    if n is specified, function will calculate divided divided differences up to n times.
    Args:
        x_points (array-like): x coordinates
        y_points (array-like): y coordinates
        n (int, optional): number of times to calculate divided differences. Defaults to 0.
        
    Returns:
        list: List of lists containing divided differences in the form of [[xpoints...],[ypoints...],[f[xi,xi+1]...], ...]
    """
    if len(x_points) != len(y_points):
        return None
    if n < 0:
        return None
    it = len(x_points) if n==0 else n #number of iterations
    table = list()
    table.append(x_points)
    table.append(y_points)
    
    # Calculate divided differences
    for row in range(2,it+1):
        arr = list()
        for col in range(len(x_points)-row+1):
            arr.append(round((table[row-1][col+1]-table[row-1][col])/(table[0][col+row-1]-table[0][col]),4))
        table.append(arr)
    
    return table
def beautify_difftable(data):
    """
    Beautify divided differences table by transposing rows and giving it a horizontal triangular shape
    Args:
    data (list): List of lists containing divided differences
    Returns:
    list(list()): Beautified divided differences table
    """

    #Initialize empty 2D array with columns equal to number of data rows, and rows equal to number of data columns
    result = [['' for _ in range(len(data))] for _ in range(len(data[0])*2 - 1)] 
    next = 0
    # Fill the first two columns of the result with spaced x and y values
    for i in range(len(data[0])):
        result[next][0] = data[0][i]
        result[next][1] = data[1][i]
        next += 2
        
    # Fill each remaining row as spaced and offset to give it a horizontal centered triangular shape
    for i in range(2, len(data)):
        next = i - 1
        for j in range(len(data[i])):
            result[next][i] = data[i][j]
            next += 2

    return result
