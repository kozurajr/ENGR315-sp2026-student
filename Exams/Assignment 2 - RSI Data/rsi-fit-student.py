import pandas as pd
import numpy as np
from scipy.stats import norm, chisquare, ttest_ind, ttest_1samp
import matplotlib.pyplot as plt

"""
Preamble: Load data from source CSV file
"""
path_to_datafile = "data/drop-jump/all_participant_data_rsi.csv"

### YOUR CODE HERE

# Load the CSV
df = pd.read_csv(path_to_datafile)

# Pull out the two RSI datasets
force_plate_rsi = df["force_plate_rsi"].dropna()
accelerometer_rsi = df["accelerometer_rsi"].dropna()

"""
Question 1: Load the force plate and acceleration based RSI data for all participants. Map each data set (accel and FP)
to a normal distribution. Clearly report the distribution parameters (mu and std) and generate a graph two each curve's 
probability distribution function. Include appropriate labels, titles, and legends.
"""
print('-----Question 1-----')

### YOUR CODE HERE

# this section of code fits each dataset to a normal distribution and then returns the estimated mean and standard deviation
force_plate_mu, force_plate_std = norm.fit(force_plate_rsi)
accel_mu, accel_std = norm.fit(accelerometer_rsi)

# This part prints the fitted normal distribution parameters for each dataset
print(f"Force Plate Normal Fit: mu = {force_plate_mu:.6f}, std = {force_plate_std:.6f}")
print(f"Accelerometer Normal Fit: mu = {accel_mu:.6f}, std = {accel_std:.6f}")

# This sets up the x values for plotting the fitted normal probability density function curves
x_force_plate = np.linspace(force_plate_rsi.min() - 0.1, force_plate_rsi.max() + 0.1, 500)
x_accel = np.linspace(accelerometer_rsi.min() - 0.1, accelerometer_rsi.max() + 0.1, 500)

# This part plots the fitted normal probability density function for the force plate RSI data
plt.figure()
plt.plot(x_force_plate, norm.pdf(x_force_plate, force_plate_mu, force_plate_std), label=f'Normal PDF (mu={force_plate_mu:.3f}, std={force_plate_std:.3f})')
plt.title("Force Plate RSI Normal Distribution")
plt.xlabel("Force Plate RSI")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(True)
plt.show()

# This part is just like the section above however it is set up to plot the fitted normal probabilty density function
# for the accelerometer RSI data
plt.figure()
plt.plot(x_accel, norm.pdf(x_accel, accel_mu, accel_std), label=f'Normal PDF (mu={accel_mu:.3f}, std={accel_std:.3f})')
plt.title("Accelerometer RSI Normal Distribution")
plt.xlabel("Accelerometer RSI")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(True)
plt.show()


"""
Question 2: Conduct a Chi2 Goodness of Fit Test for each dataset to test whether the data is a good fit
for the derived normal distribution. Clearly print out the p-value, chi2 stat, and an indication of whether it is 
a fit or not. Do this for both acceleration and force plate distributions. It is suggested to generate 9 bins between 
[0,2), add append -inf and +inf to both ends of the bins. An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 2-----')

# This is the significance level for hypothesis testing suggested in the question
alpha = 0.05

# This part of the code creates the bin edges for the chi-square goodness of fit test
# Suggested bin edges:
# 9 bins between [0,2), then 1 bin [2, inf), plus lower tail (-inf, 0)
bins = np.append(np.append([-np.inf], np.linspace(0, 2, 10)), [np.inf])

def chi_square_gof(data, mu, std, label):
    # This part calculates observed frequencies from the actual dataset using the selected bins
    observed, edges = np.histogram(data, bins=bins)

    #This part calculates the expected frequencies from the fitted normal distribution
    # it uses the normal cumulative distribution function at each bin edge, then subtracts the adjacent
    # cumulative distribution function valuues to get the probability of landing in each bin
    cdf_vals = norm.cdf(edges, loc=mu, scale=std)
    expected_probs = np.diff(cdf_vals)
    expected = expected_probs * len(data)

    # This section makes it so that the expected count total matches the observed total
    expected = expected * (observed.sum() / expected.sum())

    # This line performs the chi-square goodness of fit test
    chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)

    # This part prints the test results for the current dataset
    print(f"{label}:")
    print(f"  chi2 stat = {chi2_stat:.6f}")
    print(f"  p-value   = {p_value:.6f}")

    # This part makes a decision based on the p-value and alpha
    if p_value > alpha:
        print("  Result: Good fit to normal distribution")
    else:
        print("  Result: Not a good fit to normal distribution")


"""
Acceleration
"""
### YOUR CODE HERE

# This line runs the chi-square goodness of fit test but for the accelerometer RSI data
chi_square_gof(accelerometer_rsi, accel_mu, accel_std, "Acceleration")

"""
Force Plate
"""
### YOUR CODE HERE

# This line does the same thing as the previous line but for the force plate RSI data
chi_square_gof(force_plate_rsi, force_plate_mu, force_plate_std, "Force Plate")

"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

### YOUR CODE HERE

# This line performs a two sample t-test to compare the RSI means of the two datasets
t_stat, p_value = ttest_ind(accelerometer_rsi, force_plate_rsi)

# This section prints the t-test statistic and p-value
print(f"t-statistic = {t_stat:.6f}")
print(f"p-value     = {p_value:.6f}")

# This part decides whether the two means are statistically different or not
if p_value > alpha:
    print("Result: The means are statistically equal (fail to reject H0).")
else:
    print("Result: The means are statistically different (reject H0).")



"""
Question 4: Calculate the RSI Error for the dataset where error is expressed as the difference between the 
Force Plate RSI measurement and the Accelerometer RSI measurement. Fit this error distribution to a normal curve and 
plot a histogram of the data on the same plot showing the fitted normal curve. Include appropriate labels, titles, and 
legends. The default binning approach from matplot lib with 16 bins is sufficient.
"""

### YOUR CODE HERE

# This part calculates the error as the difference between force plate RSI and accelerometer RSI
# basicaly it is just: Error = Force Plate - Accelerometer
rsi_error = force_plate_rsi - accelerometer_rsi

# This line fits the error data to a normal distribution
err_mu, err_std = norm.fit(rsi_error)

# This section prints the fitted normal distribution parameters for the error data
print('\n\n-----Question 4-----')
print(f"Error Normal Fit: mu = {err_mu:.6f}, std = {err_std:.6f}")

# This creates x values for plotting the fitted normal curve on top of the histogram
x_err = np.linspace(rsi_error.min() - 0.05, rsi_error.max() + 0.05, 500)

# This sets up the plot for the histogram of the RSI error data and overlays the fitted normal PDF
plt.figure()
plt.hist(rsi_error, bins=16, density=True, alpha=0.6, label="RSI Error Histogram")
plt.plot(x_err, norm.pdf(x_err, err_mu, err_std),
         label=f'Fitted Normal Curve (mu={err_mu:.3f}, std={err_std:.3f})')
plt.title("RSI Error Distribution")
plt.xlabel("Force Plate RSI - Accelerometer RSI")
plt.ylabel("Density")
plt.legend()
plt.grid(True)
plt.show()