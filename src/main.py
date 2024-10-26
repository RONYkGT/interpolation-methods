from newton_interpolation import NewtonInterpolation
from cubic_splines import CubicSplineInterpolation
#import sympy as sp

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
x_points, y_points = take_n_points(n)

print("""
Select the interpolation method:
    1. Newton Interpolation
    2. Cubic Spline Interpolation
    3. Exit
    """)

choice = int(input("Enter your choice: "))
while choice != 3:

    if choice == 1:
        newton = NewtonInterpolation(x_points,y_points)
        newton.interpolate()
        newton.plot()

    elif choice == 2:
        w0 = input("Enter weight w_0 (leave empty for default value 0): ")
        w0 = int(w0) if w0.isdigit() else 0
        wn = input("Enter weight w_n (leave empty for default value 0): ")
        wn = int(wn) if wn .isdigit() else 0

        spline = CubicSplineInterpolation(x_points,y_points, w0, wn)
        spline.generate_splines()
        print("for x = 3: ")
        print(spline.evaluate_for_x(-3))
        spline.plot()

    else:
        print("Invalid choice")  # This will be executed if the choice is neither 1 nor
    choice = int(input("Enter your choice again to choose another method: "))

