import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from utils.divided_differences import calculate_divided_differences
from utils.plotting import plot_interpolation
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

    
    def evaluate(self, x_value):
        """Evaluate the interpolation polynomial at a given point."""
        if self.coefficients is None:
            self.create_table()
        
        result = self.coefficients[0]
        term = 1
        for i in range(1, len(self.coefficients)):
            term *= (x_value - self.x[i-1])
            result += self.coefficients[i] * term
        return result
    
    def plot(self, num_points=100):
        """Plot the interpolation polynomial and data points."""
        # Ensure we have the polynomial
        if self.polynomial is None:
            self.interpolate()
        
        x_min, x_max = min(self.x), max(self.x)
        x_range = np.linspace(x_min, x_max, num_points)
        y_range = [self.evaluate(x) for x in x_range]
        
        return plot_interpolation(
            self.x, self.y,
            x_range, y_range,
            self.headers, self.table,
            self.polynomial,
            title="Newton Interpolation"
        )