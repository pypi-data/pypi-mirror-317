import numpy as np

def fsdem(f, start, end, n=1000):
    x_values = np.linspace(start, end, n)
    y_values = f(x_values)
    area = np.trapz(y_values, x_values)
    return area / (end-start)