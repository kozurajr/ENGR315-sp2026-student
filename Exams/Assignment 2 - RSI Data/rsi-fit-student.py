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

# Fit normal distributions
fp_mu, fp_std = norm.fit(force_plate_rsi)
acc_mu, acc_std = norm.fit(accelerometer_rsi)

print(f"Force Plate Normal Fit: mu = {fp_mu:.6f}, std = {fp_std:.6f}")
print(f"Accelerometer Normal Fit: mu = {acc_mu:.6f}, std = {acc_std:.6f}")

# x-values for plotting
x_fp = np.linspace(force_plate_rsi.min() - 0.1, force_plate_rsi.max() + 0.1, 500)
x_acc = np.linspace(accelerometer_rsi.min() - 0.1, accelerometer_rsi.max() + 0.1, 500)

# Force Plate plot
plt.figure()
plt.plot(x_fp, norm.pdf(x_fp, fp_mu, fp_std), label=f'Normal PDF (mu={fp_mu:.3f}, std={fp_std:.3f})')
plt.title("Force Plate RSI Normal Distribution")
plt.xlabel("Force Plate RSI")
plt.ylabel("Probability Density")
plt.legend()
plt.grid(True)
plt.show()

# Accelerometer plot
plt.figure()
plt.plot(x_acc, norm.pdf(x_acc, acc_mu, acc_std), label=f'Normal PDF (mu={acc_mu:.3f}, std={acc_std:.3f})')
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

alpha = 0.05

# Suggested bin edges:
# 9 bins between [0,2), then 1 bin [2, inf), plus lower tail (-inf, 0)
bins = np.append(np.append([-np.inf], np.linspace(0, 2, 10)), [np.inf])

def chi_square_gof(data, mu, std, label):
    # Observed counts
    observed, edges = np.histogram(data, bins=bins)

    # Expected counts from fitted normal distribution
    cdf_vals = norm.cdf(edges, loc=mu, scale=std)
    expected_probs = np.diff(cdf_vals)
    expected = expected_probs * len(data)

    # Small floating-point fix so sums match exactly
    expected = expected * (observed.sum() / expected.sum())

    chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)

    print(f"{label}:")
    print(f"  chi2 stat = {chi2_stat:.6f}")
    print(f"  p-value   = {p_value:.6f}")

    if p_value > alpha:
        print("  Result: Good fit to normal distribution")
    else:
        print("  Result: Not a good fit to normal distribution")


"""
Acceleration
"""
### YOUR CODE HERE

chi_square_gof(accelerometer_rsi, acc_mu, acc_std, "Acceleration")

"""
Force Plate
"""
### YOUR CODE HERE

chi_square_gof(force_plate_rsi, fp_mu, fp_std, "Force Plate")

"""
Question 3: Perform a t-test to determine whether the RSI means for the acceleration and force plate data are equivalent 
or not. Clearly report the p-value for the t-test and make a clear determination as to whether they are equal or not.
An alpha=0.05 is suitable for these tests.
"""
print('\n\n-----Question 3-----')

### YOUR CODE HERE

t_stat, p_value = ttest_ind(accelerometer_rsi, force_plate_rsi)

print(f"t-statistic = {t_stat:.6f}")
print(f"p-value     = {p_value:.6f}")

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

# Error = Force Plate - Accelerometer
rsi_error = force_plate_rsi - accelerometer_rsi

# Fit normal distribution to error
err_mu, err_std = norm.fit(rsi_error)

print('\n\n-----Question 4-----')
print(f"Error Normal Fit: mu = {err_mu:.6f}, std = {err_std:.6f}")

# Plot histogram + fitted normal curve
x_err = np.linspace(rsi_error.min() - 0.05, rsi_error.max() + 0.05, 500)

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