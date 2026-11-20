"""
CULMINATING ASSIGNMENT 2: RSI

Create a program which will provide answers to the tasks posed in the assignment description.

For this assignment, you will start from scratch with this blank template.
It is your reponsibility to include all necessary program components in this file.
Your code needs to be successful as well as sufficiently commented/documented to receive full credit.

The relevant data file is named "all_participant_data_rsi.csv" and is located in data > drop-jump.

All file paths need to be relative and execute from this file's directory;
the Visual Studio Code setting "Python > Terminal: Execute in File Dir" 
must be enabled in File > Preferences > Settings.

See Canvas for additional requirements.
"""
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt

#get data using panda data frame WITH CORRECT RELATIVE PATH!!!
df = pd.read_csv("../../data/drop-jump/all_participant_data_rsi.csv")

#Task 1___________________________________________________________________________________________
#RSI data into force plate and accelerometer data seperately
force_plate = df["force_plate_rsi"]
accelerometer = df["accelerometer_rsi"]

diff_score = force_plate - accelerometer

# find some values used for the paired t-test
n = diff_score.count()
mean_d = diff_score.mean()
sd_d = diff_score.std()
se_d = sd_d / n ** 0.5
alpha = 0.05

#hypotheseis H0 and H1 is checking the mean of the difference between force plate and accelerometer data
#H0: mean of the differences = 0 
#H1: mean of the differences != 0 
expected_mean = 0
(t_value, p_value) = stats.ttest_1samp(diff_score, popmean=expected_mean, alternative='two-sided')

# Clearly report the t-value, p-value, null and alternative hypotheses
print("TASK 1--> Force Plate vs Accelerometer RSI (paired t-test)")
print("Number of pairs:", n)
print("Mean difference:", mean_d)
print("t-value:", t_value)
print("p-value:", p_value)
print("H0: mean difference (force plate - accelerometer) = 0, the methods give the same average RSI")
print("H1: mean difference (force plate - accelerometer) != 0, the methods give different average RSI")

# Test the null hypothesis
if p_value < alpha:
    print("Result: reject H0 (p is less than", alpha, ")")
    print("The two methods give different average RSI values.")
else:
    print("Result: fail to reject H0 (p is not less than", alpha, ")")
    print("Cannot show that the two methods give different average RSI values.")



#Task 2_______________________________________________
#accelerometer data setup
acc_data = df["accelerometer_rsi"].dropna()
n2 = len(acc_data)

# estimate the mean and standard deviation from data
fit_mu, fit_std = stats.norm.fit(acc_data)
print("Fitted mean:", fit_mu)
print("Fitted std:", fit_std)

# interval from -2 to +2 standard deviations around the fitted mean, 0.5 std...
#...wide and choosing bins for the historgram
bins = fit_mu + fit_std * np.linspace(-1.5, 1.5, 7)
bins = np.r_[-np.inf, bins, np.inf]

# probability of each and expected values
expected_prob = np.diff(stats.norm.cdf(bins, loc=fit_mu, scale=fit_std))
expected_counts = expected_prob * n2

# actual values
observed_counts, observed_edges = np.histogram(acc_data, bins=bins, density=False)

# Conduct the chi2 test
alpha = 0.05
(chi_stat, p_value) = stats.chisquare(f_obs=observed_counts, f_exp=expected_counts, ddof=2)

# H0 to find if the accelerometer data follows a normal distribution
# H1 to find if the accelerometer data does not follows a normal distribution
print("Chi2 stat:", chi_stat)
print("p-value:", p_value)
print("Degrees of freedom:", len(observed_counts) - 1 - 2)

if p_value < alpha:
    print("Reject H0--> the normal distribution is NOT a good fit")
else:
    print("Fail to reject H0--> no evidence the normal distribution is a bad fit (good fit)")

# plot histogram of the data with the curve on the top in red
x = np.linspace(acc_data.min(), acc_data.max(), 500)
plt.hist(acc_data, bins=20, density=True, edgecolor="black", label="Accelerometer RSI")
plt.plot(x, stats.norm.pdf(x, loc=fit_mu, scale=fit_std), color="red", linewidth=2, label="Fitted normal")
plt.title("Accelerometer RSI with Fitted Normal Distribution")
plt.xlabel("RSI")
plt.ylabel("Density")
plt.legend()
plt.show()

#Task 3________________________________________________

# only participant F trials
participant_f = df[df["trial"].str.startswith("F_")]

# Print Participant F's data
print("\nTASK 3 --> Participant F RSI Data")
print(participant_f)

# get seperate data types
force_f = participant_f["force_plate_rsi"].dropna()
acc_f = participant_f["accelerometer_rsi"].dropna()

# find the 95% confidence interval for force plate 
n_force = len(force_f)
mean_force = force_f.mean()
se_force = stats.sem(force_f)

ci_force = stats.t.interval(
    confidence=0.95,
    df=n_force - 1,
    loc=mean_force,
    scale=se_force
)

# find the 95% confidence interval for accelerometer data
n_acc = len(acc_f)
mean_acc = acc_f.mean()
se_acc = stats.sem(acc_f)

ci_acc = stats.t.interval(
    confidence=0.95,
    df=n_acc - 1,
    loc=mean_acc,
    scale=se_acc
)

# Print the results
print("\nForce Plate RSI")
print("Mean:", mean_force)
print("95% Confidence Interval:", ci_force)

print("\nAccelerometer RSI")
print("Mean:", mean_acc)
print("95% Confidence Interval:", ci_acc)