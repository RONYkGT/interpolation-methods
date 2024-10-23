import numpy as np
import matplotlib.pyplot as plt
from sympy import latex
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')
def create_table_latex(headers, table):
    """Convert the divided differences table to LaTeX format with calculations."""
    latex_table = r"\begin{array}{|" + "c|" * len(headers) + r"}\hline "
    latex_table += " & ".join(headers) + r"\\\hline "
    
    for row in table:
        row_str = []
        for item in row:
            if item == '':
                row_str.append(' ')
            elif '\n' in str(item):  # For calculation rows with fractions
                num, den = item.split('\n')
                row_str.append(f"\\frac{{{num}}}{{{den}}}")
            else:
                row_str.append(str(item))
        latex_table += " & ".join(row_str) + r"\\\hline "
    
    latex_table += r"\end{array}"
    return latex_table

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