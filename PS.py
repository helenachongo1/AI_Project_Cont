'''import numpy as np

# To find the correlation
def calculate_correlation(x,y):
    return np.corrcoef(x,y)[0][1]

test_data = [
    ([1.2, 2.5, 3.1], [2.4, 5.1, 6.3]),
    ([10.0, 20.0, 30.0], [15.0, 25.0, 35.0]),
    ([3.3, 5.5, 7.7], [7.7, 5.5, 3.3])]

for i, (x,y) in enumerate(test_data, start=1):
    r = calculate_correlation(x, y)
    print(f"Test {i}: Correlation between {x} and {y} is {r:.4f}")
'''
# To convert variable x to standardized version z
def standardize(data):
    mean = sum(data) / len(data)
    std_dev = (sum((x-mean)**2 for x in data) / len(data))**0.5
    return [(x-mean) / std_dev for x in data]

test_cases = [
    [1.2, 2.5, 3.1],
    [10, 20, 30],
    [5, 5, 5]]

for i, x in enumerate(test_cases, start=1):
    try:
        z_scores = standardize(x)
        print(f"Test {i}: Original: {x} -> Z-scores: {z_scores}")
    except ZeroDivisionError:
        print(f"Test {i}: Standard deviation is zero for {x}, cannot standardize.")