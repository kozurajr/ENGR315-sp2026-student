"""
Given two lists, use the standard deviation function from numpy to determine
which language has the largest standard deviation. Usage will be np.std()
https://numpy.org/doc/stable/reference/generated/numpy.std.html
"""

"""
Dr. Forsyth's Code. Do Not Modify.
"""
# bring in randomness because we need it in our lives
import random
import numpy as np

# randomly sample a distribution between 20 and 100
random_length = int(random.uniform(20, 100))

# generate a random list of random length containing values up to 100
random_list_A = random.sample(range(100), random_length)

# generate a random list of random length containing values up to 100
random_list_B = random.sample(range(100), random_length)

# use the std() method from numpy to determine which list has the largest standard deviation

### YOUR CODE HERE

# set this variable equal to the list with the largest standard deviation
# do not modify this variable's name, you can/should adjust the contents ;)
# e.g. longest_list_is = myList
longest_list_is = None

### YOUR CODE HERE

sample_A = np.std(random_list_A)
sample_B = np.std(random_list_B)
<<<<<<< HEAD
largest_sample = "none"

if sample_A > sample_B:
    longest_list_is = sample_A
    largest_sample = "List A"
else:
    longest_list_is = sample_B
    largest_sample = "List B"

print("The largest standard deviation is", largest_sample, longest_list_is)
=======

if sample_A > sample_B:
    longest_list_is = sample_A
else:
    longest_list_is = sample_B

print("The longest list is: longest_list_is")
>>>>>>> 3e89f2f5c218250e2f546ca1c5ca7abdc9ca001c
