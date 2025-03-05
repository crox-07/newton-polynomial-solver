import numpy as np


def newton_method(f, f_prime, x1, tolerance=1e-10, max_iter=1000):
    """
    Perform the Newton-Raphson method to find a root of the given function within the specified tolerance.
    
    Parameters:
    f (function): The function to find the root of.
    f_prime (function): The derivative of the function.
    x1 (float): The initial guess for the root.
    tolerance (float, optional): The tolerance for convergence. Defaults to 1e-10.
    max_iter (int, optional): The maximum number of iterations. Defaults to 1000.
    
    Returns:
    float or None: The root of the function, or None if no root is found within the specified tolerance.
    """
    
    x = x1
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tolerance:
            return x
        dfx = f_prime(x)
        if abs(dfx) < 1e-10:
            return None
        x = x - fx / dfx
        if abs(fx) < tolerance:
            return x
    return None

def verify_root(f, root, tolerance=1e-8):
    """
    Verify if the given root is correct by checking if the absolute value of the function evaluated at the root is within the specified tolerance.
    
    Parameters:
    f (function): The function to evaluate.
    root (float): The root to verify.
    tolerance (float, optional): The tolerance for verification. Defaults to 1e-8.
    
    Returns:
    bool: True if the root is correct, False otherwise.
    """
    
    return abs(f(root)) < tolerance

def find_roots(coefficients, initial_guesses):
    """
    Find the roots of the given polynomial by calling the Newton-Raphson method and verify the roots using the specified tolerance.
    
    Parameters:
    coefficients (list of float): The coefficients of the polynomial.
    initial_guesses (list of float): The initial guesses for the roots.
    
    Returns:
    list of str: The roots of the polynomial as strings, or an empty list if no roots are found within the specified tolerance.
    """
    
    def f(x):
        """ 
        Find the result of the given polynomial

        Args:
            x (float): input x value

        Returns:
            float: result of f(x)
        """
        return np.polyval(coefficients, x)
    
    def f_prime(x):
        """
        Find the derivative of the given polynomial

        Args:
            x (float): input x value

        Returns:
            float: result of f'(x)
        """
        der_coefficients = np.polyder(coefficients)
        return np.polyval(der_coefficients, x)
    
    roots = []
    
    if len(coefficients) == 3:
        roots = quadratic_formula(coefficients[0], coefficients[1], coefficients[2])
    else:
        for guess in initial_guesses:
            root = newton_method(f, f_prime, guess)
            if root is not None and verify_root(f, root) and not any(np.isclose(root, r) for r in roots):
                roots.append(root)
    
    return [str(x) for x in roots]

def quadratic_formula(a, b, c):
    """
    Calculate the roots of a quadratic equation using the quadratic formula.

    Args:
        a (float): coefficient of x^2
        b (float): coefficient of x
        c (float): constant term

    Returns:
        list of float: roots of the equation
    """
    
    D = b**2 - 4*a*c
    if D < 0:
        return [0]
    elif D == 0:
        return [-b / (2 * a)]
    else:
        return [(-b + np.sqrt(D)) / (2 * a), (-b - np.sqrt(D)) / (2 *a)]

def enter_polynomial():
    """
    Ask the user to enter the coefficients of the polynomial.

    Returns:
        list of float: coefficients of the polynomial
    """
    
    polynomial= []
    stop = False
    counter = 0
    print("Enter polynomial, to enter fractional coefficients type f")
    while not stop:
        res = input(f"Coefficient of x^{counter} term: ")
        if res == '/':
            stop = True
        elif res == 'f':
            try:
                num = float(input('Numerator:'))
                denom = float(input('Denominator:'))
                res = num/denom
                polynomial.append(res)
                counter += 1
            except ValueError:
                print("Invalid input. Please enter a valid fraction.")
        elif res == "":
            print("Invalid input. Please enter a non empty number.")
        else:
            try:
                coefficient = float(res)
                polynomial.append(coefficient)
                counter += 1
            except ValueError:
                print("invalid input. Please enter a valid number.")
    
    return polynomial[::-1]

coefficients = enter_polynomial()
degree = len(coefficients) - 1
print(f"Polynomial: {np.poly1d(coefficients)}")

initial_guesses = np.linspace(-10,10, 10 * degree + 1)

roots = find_roots(coefficients, initial_guesses)
rootstring = ""
if len(roots) == 0:
    rootstring = "No real roots found."
else:
    for i in roots:
        rootstring += i + ", "
        
print("Roots:", rootstring)