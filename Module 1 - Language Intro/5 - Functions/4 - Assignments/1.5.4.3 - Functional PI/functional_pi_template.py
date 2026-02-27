import math


def my_pi(target_error):
    """
    Implementation of Gauss–Legendre algorithm to approximate PI from https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm

    :param target_error: Desired error for PI estimation
    :return: Approximation of PI to specified error bound
    """
    a = 1
    b = 1/math.sqrt(2)
    t = .25
    p = 1
    pi_estimate = 0

    while True:
        a_next = (a + b) / 2.0
        b_next = math.sqrt(a * b)
        t_next = t - p * (a - a_next) ** 2
        p_next = 2.0 * p

        a = a_next
        b = b_next
        t = t_next
        p = p_next

        pi_estimate = ((a + b) ** 2) / (4.0 * t)
        if abs(pi_estimate - math.pi) < abs(target_error):
            return pi_estimate


desired_error = 1E-10

approximation = my_pi(desired_error)

print("Solution returned PI=", approximation)

error = abs(math.pi - approximation)

if error < abs(desired_error):
    print("Solution is acceptable")
else:
    print("Solution is not acceptable")
