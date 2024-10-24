import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')

def create_fig(n):
    """
    Create a figure with `n` row subplots (stacked vertically).
    Args:
        n (int): Number of subplots (rows) to create.
    Returns:
        fig, axes: The created figure and list of subplot axes.
    """
    fig, axes = plt.subplots(n, 1, figsize=(6, 2 * n))  # n subplots with height scaled by `n`
    fig.subplots_adjust(hspace=0.5)  # Add some space between the subplots
    return fig, axes

def plot_graph(ax, x_points, y_points, function, title):
    """
    Plot a graph of a function along the input points on a given axis.
    Args:
        ax (matplotlib.axes.Axes): The axis on which to plot.
    """
    if len(x_points) != len(y_points) or function is None:
        return

    ax.scatter(x_points, y_points, color='red', label='Data points')

    x = sp.symbols('x')
    poly_func = sp.lambdify(x, function, 'numpy')
    x_curve = np.linspace(min(x_points), max(x_points), 100)
    y_curve = poly_func(x_curve)

    ax.plot(x_curve, y_curve, label='Polynomial', color='blue')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True)

def latex_table(data):
    """
    Generate a LaTeX formatted table from a 2D array, with each cell wrapped in dollar signs.
    """
    latex_str = "\\begin{tabular}{|" + " | ".join(["c"] * len(data[0])) + "|} \\hline "
    for row in data:
        latex_row = []
        for item in row:
            latex_item = f"${str(item)}$"
            latex_row.append(latex_item)
        latex_str += " & ".join(latex_row) + " \\\\ \\hline "

    latex_str += "\\end{tabular}"
    latex_str = latex_str.replace("\n", " ")
    return latex_str

def draw_table(ax, arr, header=list()):
    """
    Draw a table with the given data in a LaTeX form on a given axis.
    Args:
        ax (matplotlib.axes.Axes): The axis on which to draw the table.
    """
    arr_copy = arr.copy()
    if header:
        if len(header) < len(arr_copy[0]):
            header.extend([''] * (len(arr_copy[0]) - len(header)))
        else:
            print("Header can't be larger than column size of table")
            return
        arr_copy.insert(0, header)
    
    latex_str = latex_table(arr_copy)
    ax.axis('off')  # Turn off the axis for the table
    ax.text(0.5, 0.5, f"${latex_str}$", fontsize=12, ha='center', va='center')

def write_text(ax, text):
    """
    Write text on a given axis.
    Args:
        ax (matplotlib.axes.Axes): The axis on which to write the text.
        text (str): The text to write.
    """
    ax.axis('off')  # Turn off axis lines for text
    ax.text(0.5, 0.5, text, fontsize=12, ha='center', va='center')

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

def show():
    plt.show()