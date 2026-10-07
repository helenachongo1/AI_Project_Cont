
from pyamaze import maze,agent,COLOR,textLabel

def dijstra(m,*h):
    
    hurdles=[(i.position,i.cost) for i in h]
    
    unvisited={n:float('inf') for n in m.grid}
    unvisited[(m.rows,m.cols)]=0
    visited={}
    revPath={}
    
    while unvisited:
        currCell=min(unvisited,key=unvisited.get)
        visited[currCell]=unvisited[currCell]
        if currCell==(1,1):
            break
        for d in 'EWNS':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in visited:
                    continue
                tempDist=unvisited[currCell]+1
                for hurdle in hurdles:
                    if hurdle[0]==currCell:
                        tempDist+=hurdle[1]
                
                if tempDist < unvisited[childCell]:
                    unvisited[childCell]=tempDist
                    revPath[childCell]=currCell
        unvisited.pop(currCell)
    fwdPath={}
    cell=(1,1)
    while cell!=(m.rows,m.cols):
        fwdPath[revPath[cell]]=cell
        cell=revPath[cell]
        
        
    return fwdPath,visited[(1,1)]

if __name__=='__main__':
    m_Maze=maze(6,6)
    m_Maze.CreateMaze(loopPercent=100)
    
    h1=agent(m_Maze,4,4,color=COLOR.red)
    h2=agent(m_Maze,4,6,color=COLOR.yellow)
    h3=agent(m_Maze,4,2,color=COLOR.green)
    
    h1.cost=100
    h2.cost=100
    h3.cost=100
    
    c=dijstra(m_Maze, h1,h2)
    path,c=dijstra(m_Maze, h1,h2)
    textLabel(m_Maze, 'Total Cost', c)
    a=agent(m_Maze,color=COLOR.blue,filled=True,footprints=True)
    m_Maze.tracePath({a:path})
    m_Maze.run()
