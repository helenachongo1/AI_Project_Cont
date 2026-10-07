from pyamaze import maze, agent, COLOR, textLabel

# Dijkstra's Algorithm for shortest path
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
        
    return fwdPath, visited[(1, 1)]

# Compare user guessed path with actual path
def compare_paths(user_guess, actual_path):
    return user_guess == actual_path

# Helper function to convert user input string into a list of tuples
def parse_user_input(user_input):
    try:
        # Convert input like "(6, 6), (5, 6), (4, 5)" into a list of tuples
        user_guess = eval(user_input)
        if isinstance(user_guess, list) and all(isinstance(cell, tuple) for cell in user_guess):
            return user_guess
        else:
            print("Invalid format! Please enter the path as a list of tuples.")
            return None
    except:
        print("Invalid input. Please try again.")
        return None

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
    print(f"Correct path: {correct_path}")
    
    # Display the maze first
    m_Maze.run()  # Show the maze to the user

    # Ask the user for input after the maze display
    user_input = input("Enter your guess for the path as a list of tuples (e.g., [(6, 6), (5, 6), (5, 5), (4, 5)]):\n")
    
    # Parse the user input
    user_guess = parse_user_input(user_input)
    
    # Ensure the input is valid before continuing
    if user_guess:
        # Compare user guess with the actual path
        if compare_paths(user_guess, list(correct_path.keys())):
            print("Correct guess! Displaying the path...")
            a = agent(m_Maze, footprints=True, color=COLOR.blue, filled=True)
            m_Maze.tracePath({a: correct_path}, delay=100)
            m_Maze.run()
            
            #print("Another level...")
            #[solve_maze()
        else:
            print("Incorrect guess. Try again.")
    else:
        print("Invalid input format.")

# Entry point for the program
if __name__ == '__main__':
    solve_maze()