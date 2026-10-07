
def getNumberOfWays(N, Coins):
    """
    Calculate the number of ways to make amount N using given Coins.
    Order of coins does NOT matter (combinations, not permutations).
    """

    # Create an array 'ways' of size N+1, initialized to 0
    # ways[x] will store the number of ways to make amount x
    ways = [0] * (N + 1)

    # Base case: There is exactly 1 way to make 0 amount (choose no coins)
    ways[0] = 1

    # Loop through each coin
    for coin in Coins:
        # Update ways[] for all amounts from 'coin' up to N
        for amt in range(coin, N + 1):
            # For current amount 'amt', include ways of (amt - coin)
            ways[amt] += ways[amt - coin]

    # Answer is number of ways to make amount N
    return ways[N]


def printArray(coins):
    """Utility function to print coins array."""
    for c in coins:
        print(c, end=" ")
    print()



Coins = [1, 5, 10]
N = 12

print("The Coins Array:")
printArray(Coins)

print("Solution:", getNumberOfWays(N, Coins))

