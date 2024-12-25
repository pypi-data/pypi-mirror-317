import numpy as np

def approx_func(x, y):
    def f(x_val):
        if np.max(x_val) >= max(x) + 1:
            raise ValueError("x is larger than max observed value.")
        return np.interp(x_val, x, y)
    def df(x_val):
        if np.max(x_val) > max(x):
            raise ValueError("x is larger than max observed value.")
        h = 1e-7  
        return (f(x_val + h) - f(x_val - h)) / (2 * h)
    return f, df