import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, simplify, Rational
from utils.divided_differences import calculate_divided_differences
from utils.plotting import plot_interpolation
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')
class NewtonInterpolation:
    def __init__(self, x_points, y_points):
        """
        Initialize Newton Interpolation with data points.
        
        Args:
            x_points (list/array): x coordinates
            y_points (list/array): y coordinates
        """
        self.x = np.array(x_points)
        self.y = np.array(y_points)
        self.coefficients = None
        self.polynomial = None
        self.headers = None
        self.table = None
    
    def create_table(self):
        """Create and return a table of points and divided differences."""
        n = len(self.x)
        
        # Calculate basic divided differences first to store coefficients
        diff_table = [[0.0 for _ in range(n)] for _ in range(n)]
        
        # Fill in the first column with f(x) values
        for i in range(n):
            diff_table[i][0] = self.y[i]
        
        # Calculate divided differences
        for j in range(1, n):
            for i in range(n - j):
                diff_table[i][j] = (diff_table[i + 1][j - 1] - diff_table[i][j - 1]) / (self.x[i + j] - self.x[i])
        
        # Store coefficients for polynomial creation (first row of differences)
        self.coefficients = [diff_table[0][j] for j in range(n)]
        
        # Create headers for the simplified format
        headers = ['x_i', 'f_i', 'F[x_i,x_j]', 'F[x_i,x_j,x_k]']
        
        # Create formatted table with calculation rows
        formatted_table = []
        
        # First row
        formatted_table.append([f'x1', f'{self.y[0]}', '', ''])
        
        # Calculate and add divided differences with calculation rows
        for i in range(1, n):
            # Add calculation row for first-order difference
            if i == 1:
                first_diff = (self.y[1] - self.y[0]) / (self.x[1] - self.x[0])
                calc_row = ['', '', f'f[x1,x2]={self.y[1]}-{self.y[0]}\n{self.x[1]}-{self.x[0]}', '']
                formatted_table.append(calc_row)
            
            # Add point value row
            row = [f'x{i+1}', f'{self.y[i]}']
            
            # Add first-order difference result if applicable
            if i == 1:
                row.append(f'{first_diff:.3f}')
            else:
                row.append('')
                
            # Add second-order difference for third row
            if i == 2:
                second_diff = ((self.y[2] - self.y[1])/(self.x[2] - self.x[1]) - (self.y[1] - self.y[0])/(self.x[1] - self.x[0]))/(self.x[2] - self.x[0])
                row.append(f'{second_diff:.3f}')
            else:
                row.append('')
                
            formatted_table.append(row)
            
            # Add calculation row for next first-order difference
            if i < n-1:
                calc_row = ['', '', f'f[x{i+1},x{i+2}]={self.y[i+1]}-{self.y[i]}\n{self.x[i+1]}-{self.x[i]}', '']
                formatted_table.append(calc_row)
        
        self.headers = headers
        self.table = formatted_table
        return headers, formatted_table
    
    def interpolate(self):
        """Calculate Newton interpolation polynomial."""
        # Ensure we have coefficients
        if self.coefficients is None:
            self.create_table()
        
        # Create symbolic polynomial
        x = symbols('x')
        
        try:
            # Convert first coefficient to Rational
            polynomial = Rational(str(self.coefficients[0]))
            
            # Build the polynomial term by term
            term = 1
            for i in range(1, len(self.coefficients)):
                term *= (x - Rational(str(self.x[i-1])))
                coeff = Rational(str(self.coefficients[i]))
                polynomial += coeff * term
            
            self.polynomial = simplify(polynomial)
            return self.polynomial
            
        except Exception as e:
            print(f"Error creating polynomial: {e}")
            print(f"Coefficients: {self.coefficients}")
            print(f"x points: {self.x}")
            return None
    
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