'''import numpy as np
from scipy.stats import zscore
import matplotlib.pyplot as plt
import seaborn as sns


def standardize(dt):
    mean = sum(dt) / len(dt)
    std_dev = (sum((x-mean)**2 for x in dt) / len(dt))**0.5
    return [(x-mean) / std_dev for x in dt]

data = [5200, 4800, 5000, 4900, 4600, 5100, 5050, 4950, 11000, 5300,
        5000, 5100, 5150, 4950, 5000, 4950, 4600, 5200, 5050, 10000]

z_scores = standardize(data)

for i, (original, z) in enumerate(zip(data, z_scores), start=1):
    print(f"x {i} = {original}, Z-score = {z:.2f}")

z_rounded = [round(z, 1) for z in z_scores]

from collections import defaultdict

dot_dict = defaultdict(int)

plt.figure(figsize=(10, 4))
for z in z_rounded:
    y = dot_dict[z]
    plt.plot(z, y, 'ko')  
    dot_dict[z] += 1

plt.title("Dot Plot of Z-scores")
plt.xlabel("Z-score")
plt.ylabel("Frequency (stacked dots)")
plt.grid(True, axis='x', linestyle='--', alpha=0.7)
plt.show()'''


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2.5, 4, 5, 6.5, 7.5, 8, 9, 10.5, 11, 12.5])

correlation = np.corrcoef(x, y)[0, 1]
print(f"Correlation Coefficient: {correlation:.4f}")

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
line = slope * x + intercept
print(f"Regression Equation: y = {slope:.2f}x + {intercept:.2f}")

plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='blue', label='Data points')
plt.plot(x, line, color='red', label='Best fit line')
plt.title('Study Hours vs. Test Score')
plt.xlabel('Hours Studied per Week')
plt.ylabel('Test Score out of 15')
plt.legend()
plt.grid(True)
plt.show()

'''
The scatter plot clearly shows a positive linear trend.

The correlation coefficient is high, indicating 
a strong correlation.

The linear regression line fits the data well.

Interpretation:
Yes, increasing study hours is strongly associated with better test performance. 
The university or advisor can confidently 
suggest that more study hours lead to higher standardized test scores.'''

