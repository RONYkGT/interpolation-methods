import numpy as np
import sympy as sp
from utils.divided_differences import calculate_divided_differences, beautify_difftable
import utils.plotting as plt
class NewtonInterpolation:
    def __init__(self, x_points, y_points):
        """
        Initialize Newton Interpolation with data points, and automatically stores the result of
        the divided differences calculation of x and y
        
        Args:
            x_points (list/array): x coordinates
            y_points (list/array): y coordinates
        """
        self.difftable = calculate_divided_differences(x_points,y_points)
        self.polynomial = None
        self.latex_polynomial = None
    
    def interpolate(self):
        """Calculate Newton interpolation polynomial."""
        
        # Create symbolic polynomial
        x = sp.symbols('x')
        poly = 0
        latex_poly = ""
        xProduct = 1
        latex_xProduct = ""
        for col in range(1,len(self.difftable)):
            coefficient = self.difftable[col][0]
            if col != 1:
                xProduct *= (x - self.difftable[0][col-2])
                latex_xProduct += f"(x - {self.difftable[0][col-2]})"
            poly += coefficient * xProduct
            if col != 1: 
                latex_poly += f"+ {coefficient} * " + latex_xProduct
            else:
                latex_poly += f"{coefficient}"
        self.polynomial = sp.expand(poly)
        self.latex_polynomial = latex_poly


    def plot(self, num_points=100):
        """Plot the interpolation polynomial and data points."""
        # Ensure we have the polynomial
        if self.polynomial is None:
            self.interpolate()
        fig, axes = plt.create_fig(2)
        tablefig, tableax = plt.create_fig(1)
        # Plot a graph on the first subplot
        plt.plot_graph(axes[0], self.difftable[0], self.difftable[1], self.polynomial, ' Newton Interpolation')

        # Create a table and draw it on the second subplot
        arr = beautify_difftable(self.difftable)
        plt.draw_table(tableax, arr, ['x', 'y'])

        # Write some text on the third subplot
        plt.write_text(axes[1], "Deduced Polynomial from table:\n $P(x)=" + self.latex_polynomial +"$\n\nExpanded Form:\n$P(x)=" + sp.latex(sp.expand(self.polynomial)) + "$")

        # Show the entire figure with all subplots
        plt.show()
