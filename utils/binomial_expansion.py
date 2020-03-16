import numpy as np

# Python3 program to print terms of binomial
# series and also calculate sum of series.

# function to calculate factorial
# of a number
def factorial(n):
    f = 1
    for i in range(2, n + 1):
        f *= i

    return f


# Function to print the series
def series(A, X, n):
    factors = list()
    # calculating the value of n!
    nFact = factorial(n)

    # loop to display the series
    for i in range(0, n + 1):
        # For calculating the
        # value of nCr
        niFact = factorial(n - i)
        iFact = factorial(i)

        # calculating the value of
        # A to the power k and X to
        # the power k
        aPow = pow(A, n - i)
        xPow = pow(X, i)

        # display the series
        factor =int((nFact * aPow * xPow) / (niFact * iFact))

        factors.append(factor)

    return factors


def find_incremental_probability(total_probability):
    A = 1
    X = -1
    n = 27

    factors = series(A, X, n)
    factors.reverse()
    factors.append(total_probability)

    roots = np.roots(factors)

    for value in roots:
        if value.imag == 0:
            probability = abs(value.real)
            if 0 < probability < 1:
                incremental_probability = probability
    return_value = min(incremental_probability, total_probability)
    return return_value/10


if __name__ == '__main__':
    find_incremental_probability(total_probability=0.1)
