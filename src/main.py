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
        spline = CubicSplineInterpolation(x_points,y_points)
        spline.generate_splines()
        print("for x = 3: ")
        print(spline.evaluate_for_x(-3))
        spline.plot()

    else:
        print("Invalid choice")  # This will be executed if the choice is neither 1 nor
    choice = int(input("Enter your choice again to choose another method: "))

"""# Create interpolation object
newton = NewtonInterpolation(x_points, y_points)

# Get interpolation polynomial and create plot
newton.interpolate()
newton.plot()


x_vals = [-6,-4,-2,-1,0,6,7]
y_vals = [-121,-25,-1,-1,-1,335,503]
cubic = CubicSplineInterpolation(x_vals,y_vals,0,0)
print("\ndifftable: ")
sp.pprint(cubic.difftable)
print("\nh_i+1 values: \n")
sp.pprint(cubic.h_values)
print("\nA matrix: \n")
sp.pprint(cubic.A_matrix)
print("\nb vector: \n")
sp.pprint(cubic.b_vector)
print("\nw values: ")
sp.pprint(cubic.w_values)
cubic.generate_splines()
print("for x = 3: ")
print(cubic.evaluate_for_x(-3))
cubic.plot()


"""