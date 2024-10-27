import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
plt.rc('text', usetex=True) # Use latex to render text in matplotlib
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
        x_points (list): List of x values to plot.
        y_points (list): List of y values to plot.
        function (sp.polynomial): Polynomial to draw.
        title (str): Graph title.
    """
    if len(x_points) != len(y_points) or function is None:
        return

    ax.scatter(x_points, y_points, color='red', label='Data points')

    x = sp.symbols('x')
    poly_func = sp.lambdify(x, function, 'numpy') # Turn sympy polynomial into a lambda function that takes x and returns f(x)
    x_curve = np.linspace(min(x_points), max(x_points), 100) # Create evenly spaced x values to put in f(x)
    y_curve = poly_func(x_curve) # Create an array out of f(x_curve)

    ax.plot(x_curve, y_curve, label='Polynomial', color='blue')
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()
    ax.grid(True)

def latex_table(data):
    """
    Generate a LaTeX formatted table from a 2D array, with each cell wrapped in dollar signs for latex format.
    Args:
        data (list of list): table array
    Returns:
        str: LaTeX formatted table
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
        arr (list of list): table array
        header (list): table header
    """
    arr_copy = arr.copy()
    if header:
        if len(header) <= len(arr_copy):
            header.extend([''] * (len(arr_copy[0]) - len(header))) # Extend the remaining header columns to match size
        else:
            print("Header can't be larger than column size of table")
            return
        
        # Add header argument to the array first row
        arr_copy.insert(0, header)
    
    # Get table latex format of the array
    latex_str = latex_table(arr_copy)

    ax.axis('off')  # Turn off the axis for the table
    print(latex_str)
    # Write the latex table on the axis
    ax.text(0.5, 0.5, f"${latex_str}$", fontsize=12, ha='center', va='center')

def write_text(ax, text):
    """
    Write text on a given axis.
    Args:
        ax (matplotlib.axes.Axes): The axis on which to write the text.
        text (str): The text to write.
    """
    print(text)
    ax.axis('off')  # Turn off axis lines for text
    ax.text(0.5, 0.5, text, fontsize=12, ha='center', va='center')

def show():
    plt.show()