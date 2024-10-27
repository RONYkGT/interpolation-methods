from newton_interpolation import NewtonInterpolation
from cubic_splines import CubicSplineInterpolation
from least_squares import LeastSquares
from fractions import Fraction

def take_n_points(n: int):
    x_vals = list()
    y_vals = list()
    for _ in range(n):
        x = float(Fraction(input("Enter x value: ")))
        y = float(Fraction(input("Enter y value: ")))
        x_vals.append(x)
        y_vals.append(y)
    return x_vals, y_vals

print("Notice: If you can't run latex in matplotlib, you can still see the latex text as output in console.")
n = int(input("Enter the number of input points(x,y): "))
x_points, y_points = take_n_points(n)

print("""
Select the interpolation method:
    1. Newton Interpolation
    2. Cubic Spline Interpolation
    3. Least Squares Model Interpolation
    0. Exit
    """)

choice = int(input("Enter your choice: "))
while choice != 0:

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
    
    elif choice == 3:
        print("""
Select the model:
    1. Polynomial Degree n Model
    2. Powerlaw Model
    3. Periodic Model
    4. Drug Concentration Model
    5. Exponential Interpolation
    0. Back""")
        model = LeastSquares(x_points, y_points)
        model_choice = -1
        while model_choice != 0:
            model_choice = int(input("Enter your model choice: "))
            if model_choice == 1:
                degree = int(input("Enter the degree of the polynomial model: "))
                model.polynomial_interpolation(degree)
                model.plot()
            elif model_choice == 2:
                model.powerlaw_interpolation()
                model.plot()
            elif model_choice == 3:
                model.periodic_interpolation()
                model.plot()
            elif model_choice == 4:
                model.drug_concentration_interpolation()
                model.plot()
            elif model_choice == 5:
                model.exponential_interpolation()
                model.plot()
            elif model_choice != 0:
                print("Enter a valid choice")
                model_choice = int(input("Enter your model choice: "))
                
    else:
        print("Invalid choice")  # This will be executed if the choice is neither 1 nor
    choice = int(input("Enter your choice again to choose another method: "))

