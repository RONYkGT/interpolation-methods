import numpy as np
import sympy as sp
from utils.divided_differences import calculate_divided_differences, beautify_difftable
import utils.plotting as plt

class CubicSplineInterpolation:

    def __init__(self, x_points, y_points,w0 = 0,wn = 0):
        """
        Initialize Cubic Spline Interpolation with data points
        and calculate divided differences with 3 iterations
        and store it in self.difftable 2d array with the first row as x values and second as y values.
        
        Args:
            x_points (list/array): x coordinates
            y_points (list/array): y coordinates
            w0 (float, optional): weight at the start. Defaults to 0.
            wn (float, optional): weight at the end. Defaults to 0.
        """

        # Store the divded differences with row0 and row1 as x and y values
        self.difftable = calculate_divided_differences(x_points,y_points,3) 

        # Calculate hi values where hi = x_i+1 - xi
        self.h_values = [x2 - x1 for x1, x2 in zip(x_points[:-1], x_points[1:])]

        self.A_matrix = None
        self.b_vector = None
        self.w_values = None
        self.piecewise = None

        self.create_A_matrix()
        self.create_b_vector()

        self.solve_for_omega()
        self.w_values.insert(0,w0)
        self.w_values.append(wn)
    
    def create_A_matrix(self):
        """
        Create the matrix A for the system of linear equations which has a diagonal form
        """
        n = len(self.h_values) - 1 # Length of matrix diagonal
        matrix = sp.zeros(n) # Fill matrix with 0's initially

        # Fill the diagonal with hi+hi1/3
        for i in range(n):
            matrix[i, i] = (self.h_values[i] + self.h_values[i+1])/3

        # Fill the upper and lower diagonal with hi+1/6
        for i in range(n - 1):
            matrix[i, i+1] = self.h_values[i+1]/6
            matrix[i+1, i] = self.h_values[i+1]/6

        self.A_matrix = matrix

    def create_b_vector(self):
        """
        Create the vector b for the system of linear equations
        """
        n = len(self.h_values) - 1
        vector = sp.zeros(n,1)
        for i in range(n):
            vector[i] = (self.h_values[i] + self.h_values[i+1])*self.difftable[3][i]
        self.b_vector = vector
    
    def solve_for_omega(self):
        """
        Solve the system of linear equations to find omega values
        """
        np_A_matrix = np.array(self.A_matrix)
        np_b_vector = np.array(self.b_vector)

        # Solve for omega, where it will be saved as a 1d array instead of a vertical numpy vector
        self.w_values = np.linalg.solve(np_A_matrix.astype(np.float64), np_b_vector.astype(np.float64)).flatten().tolist()


    def generate_splines(self):
        """
        Generate the cubic splines
        """
        splines = []
        n = len(self.h_values)
        x = sp.symbols('x')
        
        for i in range(n):
            # Format: 
            # self.difftable[0][i] = xi
            # self.difftable[1][i] = yi
            # self.h_values[i] = hi+1

            h_iplus1 = self.h_values[i]
            w_i = self.w_values[i]
            w_iplus1 = self.w_values[i+1]
            x_i = self.difftable[0][i]
            x_iplus1 = self.difftable[0][i + 1]
            y_i = self.difftable[1][i]
            y_iplus1 = self.difftable[1][i+1]

            print(f"i = {i}")
            print(f"h_iplus1 = {h_iplus1}")
            print(f"wi = {w_i}")
            print(f"wi+1 = {w_iplus1}")
            func = ((w_i / (6 * h_iplus1)) * ((x_iplus1 - x)**3)) + \
           ((w_iplus1 / (6 * h_iplus1)) * ((x - x_i)**3)) + \
           (((y_i / h_iplus1) - (h_iplus1 * (w_i / 6))) * (x_iplus1 - x)) + \
           (((y_iplus1 / h_iplus1) + (h_iplus1 * (w_iplus1 / 6))) * (x - x_i))
            
            condition = (x >= x_i) & (x < x_iplus1)

            splines.append((func.expand(),condition))

        # Convert saved (Polynomial, condition) pairs in splines array as a Piecewise object
        self.piecewise = sp.Piecewise(*splines)

    def evaluate_for_x(self, value):
        """
        Evaluate the cubic spline at a given point x
        """
        x = sp.symbols('x')
        return self.piecewise.subs(x, value)

    def plot(self, num_points=100):
        """Plot the interpolation polynomial and data points."""
        # Ensure we have the polynomial
        if self.piecewise is None:
            return
        
        _, ax1 = plt.create_fig(1)
        _, tableax = plt.create_fig(1)
        _, textax = plt.create_fig(1)
        # Plot a graph on the first subplot
        plt.plot_graph(ax1, self.difftable[0], self.difftable[1], self.piecewise, ' Cubic Splines Interpolation')

        # Create a table and draw it on the second subplot
        arr = beautify_difftable(self.difftable)

        spaced_h_values = list()
        for i in range(len(self.h_values)):
            spaced_h_values.append('')
            spaced_h_values.append(self.h_values[i])
        spaced_h_values.append('')
        arr = np.insert(arr, 2, spaced_h_values, axis=1).tolist()
        
        plt.draw_table(tableax, arr, ['x', 'y', 'h_{i+1}','[x_i,x_{i+1}]','[x_{i-1},x_i,x_{i+1}]'])

        # Write some text on the third subplot
        plt.write_text(
            textax, 
            "Deduced Piecewise from table:\n" +
            "$P(x) = " + sp.latex(self.piecewise) + "$\n\n" +
            "Matrix:\n" +
            "$A = " + sp.latex(self.A_matrix.applyfunc(lambda x: round(x, 4))) + "$\n" +
            "Vectors b and w: $b = " + sp.latex(self.b_vector.applyfunc(lambda x: round(x, 4))) + 
            ", \omega = " + sp.latex(sp.Matrix(self.w_values).applyfunc(lambda x: round(x, 4))) + "$"
        )

        # Show the entire figure with all subplots
        plt.show()
