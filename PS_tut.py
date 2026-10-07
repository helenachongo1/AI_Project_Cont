import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Data
travel_times = np.array([26, 33, 65, 28, 34, 55, 25, 44, 50, 36, 
                         26, 37, 43, 62, 35, 38, 45, 32, 28, 34])

mean = 38.8
std_dev = 11.4


z_scores = (travel_times - mean) / std_dev # Convert to z-scores

fig, axes = plt.subplots(1, 2, figsize=(14, 5)) # Create histograms and overlay normal curves for both distributions

# Normal distribution
x1 = np.linspace(min(travel_times), max(travel_times), 100)
pdf1 = norm.pdf(x1, mean, std_dev)
axes[0].hist(travel_times, bins=8, density=True, alpha=0.6, color='skyblue', edgecolor='black')
axes[0].plot(x1, pdf1, 'r-', label='Normal Curve')
axes[0].set_title('Normal Distribution Graph')
axes[0].set_xlabel('Travel Time (minutes)')
axes[0].set_ylabel('Density')
axes[0].legend()

# Plot normalized (z-score) distribution
x2 = np.linspace(min(z_scores), max(z_scores), 100)
pdf2 = norm.pdf(x2, 0, 1)
axes[1].hist(z_scores, bins=8, density=True, alpha=0.6, color='lightgreen', edgecolor='black')
axes[1].plot(x2, pdf2, 'r-', label='Standard Normal Curve')
axes[1].set_title('Normalized Z-Score Distribution')
axes[1].set_xlabel('Z-Score')
axes[1].set_ylabel('Density')
axes[1].legend()

plt.tight_layout()
plt.show()

