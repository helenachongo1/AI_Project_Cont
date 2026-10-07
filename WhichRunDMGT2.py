from pyamaze import maze, agent, COLOR, textLabel

# Dijkstra's Algorithm for shortest path and total cost
def dijstra(m, *h):
    hurdles = [(i.position, i.cost) for i in h]
    
    unvisited = {n: float('inf') for n in m.grid}
    unvisited[(m.rows, m.cols)] = 0
    visited = {}
    revPath = {}
    
    while unvisited:
        currCell = min(unvisited, key=unvisited.get)
        visited[currCell] = unvisited[currCell]
        if currCell == (1, 1):
            break
        for d in 'EWNS':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                
                if childCell in visited:
                    continue
                
                tempDist = unvisited[currCell] + 1
                for hurdle in hurdles:
                    if hurdle[0] == currCell:
                        tempDist += hurdle[1]
                
                if tempDist < unvisited[childCell]:
                    unvisited[childCell] = tempDist
                    revPath[childCell] = currCell
        unvisited.pop(currCell)
        
    fwdPath = {}
    cell = (1, 1)
    while cell != (m.rows, m.cols):
        fwdPath[revPath[cell]] = cell
        cell = revPath[cell]
        
    return fwdPath, visited[(1, 1)]  # Returning the correct path and total cost

# Function to get integer input from the user
def get_user_guess():
    while True:
        user_input = input("Guess the total cost to reach the destination (from bottom-right to top-left):\n")
        try:
            return int(user_input)  # Convert to integer if possible
        except ValueError:
            print("Invalid input. Please enter an integer value.")  # Error message if input is not an integer

# Main function to solve the maze
def solve_maze():
    m_Maze = maze(6, 6)
    m_Maze.CreateMaze(loopPercent=100)
    
    # Hurdles as agents with costs
    h1 = agent(m_Maze, 4, 4, color=COLOR.red)
    h2 = agent(m_Maze, 4, 6, color=COLOR.yellow)
    h3 = agent(m_Maze, 4, 2, color=COLOR.green)
    
    h1.cost = 100
    h2.cost = 100
    h3.cost = 100
    
    # Run Dijkstra's algorithm with hurdles
    correct_path, correct_cost = dijstra(m_Maze, h1, h2, h3)
    #print(f"Correct cost: {correct_cost}")
    
    # Display the maze first
    m_Maze.run()  # Show the maze to the user

    # Get integer input for the total cost
    user_guess = get_user_guess()

    # Compare the user's guess with the actual cost
    if user_guess == correct_cost:
        print("Correct guess! Displaying the path and creating a new maze...")
        a = agent(m_Maze, footprints=True, color=COLOR.blue, filled=True)
        m_Maze.tracePath({a: correct_path}, delay=100)
        m_Maze.run()
        
        # Generate a new maze after the correct guess
        #print("Opening a new maze...")
        #solve_maze()  # Recursively open a new maze
    else:
        print(f"Incorrect guess. The correct cost was {correct_cost}. Try again.")
        solve_maze()  # Restart with the same or new maze after an incorrect guess

# Entry point for the program
if __name__ == '__main__':
    solve_maze()
    