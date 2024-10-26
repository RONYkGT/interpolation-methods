import sympy as sp
import numpy as np
from math import cos, sin, pi, log
import utils.plotting as plt
import utils.matrix_operations as mat

class LeastSquares:
    def __init__(self, x_values, y_values):
        """
        Initialize the LeastSquares class. Can not be multiple models at once. Default model is polynomial.
        Args:
        x_values (list): list of x values
        y_values (list): list of y values
        """
        self.x_values = x_values
        self.y_values = y_values

        # Ac = B
        self.A_matrix = None
        self.b_vector = None
        self.A_norm = None # A^TA
        self.b_norm = None # A^TB
        self.c_vector = None

        self.function = None
        self.latex_extra = "" # Output text
        self.latex_C = "" # Initial form of C

    def periodic_interpolation(self):
        """
        Interpolate a periodic function with a set of points.
        """
        A = list()
        for x in self.x_values:
            A.append([1, cos(2*pi*x), sin(2*pi*x)])
        self.A_matrix = np.array(A)
        self.b_vector = np.array(self.y_values).reshape(-1,1) # Convert y values to column vector

        self.c_vector, self.A_norm, self.b_norm = mat.solve_inconsistent_system(self.A_matrix, self.b_vector)
        x = sp.symbols('x')
        self.function = self.c_vector[0][0] + self.c_vector[1][0] * sp.cos(2*sp.pi*x) + self.c_vector[2][0] * sp.sin(2*sp.pi*x)
        self.latex_extra = r"$y = c_0 + c_1\cos(2\pi x)+ c_2\cos(2\pi x)$ and $C = \begin{bmatrix} c_1 \\ c_2  \\ c_3 \end{bmatrix} $"
        self.latex_C = r"\begin{bmatrix} c_1 \\ c_2  \\ c_3 \end{bmatrix}"


    def exponential_interpolation(self):
        """
        Interpolate an exponential function with a set of points.
        """
        self.A_matrix = mat.generate_vandermonde_matrix([log(x) for x in self.x_values], 1)
        y = sp.symbols('y')
        fy = sp.Lambda(y, sp.ln(y))
        self.b_vector = mat.generate_colvector_from_function(fy,self.y_values)
        self.c_vector, self.A_norm, self.b_norm = mat.solve_inconsistent_system(self.A_matrix, self.b_vector)
        self.latex_extra = r"$y = c_1 e^{c_2 t}$" + "\n" + r"$\ln{y} = \ln{c_1}+c_2t$" + "\n" + r"$\ln{y} = k+c_2t $ where $k=\ln{x}$ " + "\n\n" + r"$b = \begin{bmatrix}\ln{y_1} \\ \ln{y_2} \\ \vdots \\ \ln{y_n} \end{bmatrix}$ and $ C = \begin{bmatrix} k \\ c_2 \end{bmatrix} $"
        self.latex_C = r" \begin{bmatrix} k \\ c_2 \end{bmatrix} "
        x = sp.symbols('x')
        c1 = sp.exp(self.c_vector[0][0])
        c2 = self.c_vector[1][0]
        self.function = c1*x**c2

    def polynomial_interpolation(self, degree = 1):
        """
        Calculate the polynomial interpolation of a set of points.
        Args:
        degree (int): Optional, default value 1. The degree of the polynome
        """
        # Generate A matrix
        self.A_matrix = mat.generate_vandermonde_matrix(self.x_values, degree)

        self.b_vector = np.array(self.y_values).reshape(-1,1) # Convert y values to column vector

        self.c_vector, self.A_norm, self.b_norm = mat.solve_inconsistent_system(self.A_matrix, self.b_vector)
        
        self.function = 0
        self.latex_C = r"\begin{bmatrix}"
        self.latex_extra = ""
        x = sp.symbols('x')
        for i in range(degree + 1):
            self.function += self.c_vector[i][0] * x ** i
            if i == 0:
                self.latex_extra += f"$y = c_{i}"
                self.latex_C +=  f"c_{i}"
            else:
                self.latex_extra += f" + c_{i} x^{i}"
                self.latex_C += r"\\" + f"c_{i}"
        self.latex_extra += "$"
        self.latex_C += r"\end{bmatrix}"


    def evaluate_for_x(self, value):
        """
        Evaluate the newton interpolation at a given point x
        """
        x = sp.symbols('x')
        return self.function.subs(x, value)
    
    def plot(self, num_points=100):
        """Plot the interpolation polynomial and data points."""
        # Ensure we have the polynomial
        if self.function is None:
            return

        _, graph = plt.create_fig(1) # First figure window to contain graph 
        _, steps = plt.create_fig(1) # Second figure window to contain the steps

        # Plot a graph on the first subplot of first figure
        plt.plot_graph(graph, self.x_values, self.y_values, self.function, ' Least Squares Interpolation')

        # Write the polynomials on the second subplot of first figure
        sp_A = sp.Matrix(self.A_matrix.tolist())
        sp_A_norm = sp.Matrix(self.A_norm.tolist())
        sp_C = sp.Matrix(self.c_vector.tolist())
        sp_B = sp.Matrix(self.b_vector.tolist())
        sp_B_norm = sp.Matrix(self.b_norm.tolist())

        text = self.latex_extra + "\n\n"
        text += "$A = " + sp.latex(sp_A) + "$, $C="+self.latex_C+"$ and $B="+sp.latex(sp_B)+"$"
        text += "\n\n"+ r"$A^TAC=A^TB$"
        text += "$\\xrightarrow{}"+sp.latex(sp_A_norm) + self.latex_C + r"=" + sp.latex(sp_B_norm) + "$\n\n"
        text += r"$C=" + sp.latex(sp_C) + "$\n\n"
        text += r"$f(x) = " + sp.latex(self.function) + "$"
        plt.write_text(steps, text)

        # Show the entire figures with all subplots
        plt.show()

