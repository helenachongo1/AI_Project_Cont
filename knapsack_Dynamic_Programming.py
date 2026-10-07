# 0/1 Knapsack using Dynamic Programming
def Knapsack(wt, profit, capacity):
    n = len(wt)
    # Create DP table (n+1) x (capacity+1)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Build the table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if wt[i - 1] <= w:  # item can fit
                dp[i][w] = max(profit[i - 1] + dp[i - 1][w - wt[i - 1]],
                               dp[i - 1][w])  # take it or leave it
            else:
                dp[i][w] = dp[i - 1][w]  # can't take it

    return dp[n][capacity]

wt = [2, 3, 1, 4, 3, 2, 7]
profit = [10, 5, 3, 2, 8, 7, 11]
capacity = 10

gain = Knapsack(wt, profit, capacity)
print("Maximum Profit:", gain)

