from newton_interpolation import NewtonInterpolation

def take_n_points(n: int):
    x_vals = list()
    y_vals = list()
    for _ in range(n):
        x = float(input("Enter x value: "))
        y = float(input("Enter y value: "))
        x_vals.append(x)
        y_vals.append(y)
    return x_vals, y_vals



n = int(input("Enter the number of input points(x,y): "))

# Example usage
x_points, y_points = take_n_points(n)

# Create interpolation object
newton = NewtonInterpolation(x_points, y_points)

# Get interpolation polynomial and create plot
newton.interpolate()
newton.plot()