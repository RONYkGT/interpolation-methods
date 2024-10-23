from newton_interpolation import NewtonInterpolation
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{amsmath}')
# Example usage
x_points = [0, 1, 2, 4]
y_points = [1, 2, 4, 8]

# Create interpolation object
newton = NewtonInterpolation(x_points, y_points)

# Get interpolation polynomial and create plot
newton.interpolate()
newton.plot()
plt.show()