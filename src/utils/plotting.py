import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')

def latex_table(data):
    """
    Generate a LaTeX formatted table from a 2D array, with each cell wrapped in dollar signs.

    Args:
        data (list of list): 2D array where each inner list represents a row.

    Returns:
        str: LaTeX formatted table as a single line string.
    """
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a 2D array (list of lists).")

    # Start the LaTeX table
    latex_str = "\\begin{tabular}{|" + " | ".join(["c"] * len(data[0])) + "|} \\hline "

    # Add rows to the table
    for row in data:
        latex_row = []
        for item in row:
            # Wrap each item in dollar signs
            latex_item = f"${str(item)}$"  # Here, we can format each item as a string and add $ around it.
            latex_row.append(latex_item)
        
        latex_str += " & ".join(latex_row) + " \\\\ \\hline "

    # End the LaTeX table
    latex_str += "\\end{tabular}"

    # Replace line breaks with spaces to ensure a single line output
    latex_str = latex_str.replace("\n", " ")

    return latex_str

def draw_table(arr, header = list()):
    arr_copy = arr.copy()
    """
    Draw a table with the given data in a Latex form.
    """
    if header:
        if len(header) < len(arr_copy[0]):
            header.extend([''] * (len(arr_copy[0]) - len(header)))
        else:
            print("header cant be larger than column size of table")
            return
        arr_copy.insert(0,header)
    # Create a LaTeX formatted table
    latex_str = latex_table(arr)

    fig, ax = plt.subplots(figsize=(8, 4))  # Create a figure and axes
    ax.axis('off')  # Hide the axes

    # Display the LaTeX string using text
    ax.text(0.5, 0.5, f"${latex_str}$", fontsize=12, ha='center', va='center')

    plt.title("LaTeX Formatted Table")  # Title for the plot


def plot_graph(x_points, y_points, function, title):
    """
    Plot a graph of a function along the input points
    """
    if len(x_points) != len(y_points):
        return
    if len(x_points) < 2:
        return
    if function == None:
        return

    fig = plt.figure(figsize=(12,10))

    # Make graph space for curve and points
    ax = fig.add_axes([0.1, 0.4, 0.8, 0.5])

    # Plot the input x and y
    ax.scatter(x_points, y_points, color='red', label='Data points')

    x = sp.symbols('x')

    # Convert sympy expression to a lambda function for evaluation
    poly_func = sp.lambdify(x, function, 'numpy')

    x_curve = np.linspace(min(x_points), max(x_points), 100)

    # Store values of y from given polynomial to draw on graph
    y_curve = poly_func(x_curve)

    ax.plot(x_curve, y_curve, label='Polynomial', color='blue')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True)

def plot_interpolation(x_points, y_points, x_curve, y_curve, headers, table, polynomial, title="Newton Interpolation"):
    """Modified plot function to handle the new table format."""
    fig = plt.figure(figsize=(12, 10))
    
    # Create main plot in upper portion
    ax = fig.add_axes([0.1, 0.4, 0.8, 0.5])
    
    # Plot interpolation curve
    ax.plot(x_curve, y_curve, 'b-', label='Interpolation')
    
    # Plot data points
    ax.plot(x_points, y_points, 'ro', label='Data points')
    
    # Customize plot
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)
    ax.legend()
    
    # Add divided differences table
    table_latex = create_table_latex(headers, table)
    plt.text(0.1, 0.25, r"Divided Differences Table:", transform=fig.transFigure, fontsize=10)
    plt.text(0.1, 0.15, f"${table_latex}$", transform=fig.transFigure, fontsize=10)
    
    # Add polynomial
    plt.text(0.1, 0.35, "Interpolation polynomial:", transform=fig.transFigure, fontsize=10)
    plt.text(0.1, 0.3, f"$p(x) = {latex(polynomial)}$", transform=fig.transFigure, fontsize=10)
    
    return fig, ax