import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """

    ### YOUR CODE HERE ###
    a = 1
    b=1 / math.sqrt(2)
    t= 1/4
    p = 1
    # change this so an actual value is returned
    while True:
        a_new = (a+b) / 2
        b_new = math.sqrt(a*b)
        t_new = t - p*(a - a_new)**2
        p_new = 2 * p

        pi_estimation = (a_new + b_new)**2 / (4 * t_new)
        if abs(pi_estimation - math.pi) < target_error:
            return pi_estimation

        a, b, t, p =a_new, b_new, t_new, p_new

desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
