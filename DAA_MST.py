#Define the graph

a,b,c,d,e,f = 0,1,2,3,4,5
graph = [[a,b,2],[a,c,3],[a,d,4],
         [b,d,1],[b,e,5],[c,d,3],
         [d,e,2],[e,f,4]]

#Define the adjacency matrix
def adjMatrix (V,G):
    adj = [[0 for i in range (V)] for j in range(V)]
    for i in range(len(G)):
        adj[G[i][0]][G[i][1]]=G[i][2]
        adj[G[i][1]][G[i][0]]=G[i][2]
    return adj

def Prims(V,G):
    adj = adjMatrix(V, G)
    vertex = 0 #Source vertex
    edges = []
    visited = []
    minedge = [None, None, float('inf')]
    
    MST = []
    while(len(MST)!=V-1):
        visited.append(vertex)
        for ed in range(0,V):
            if(adj[vertex][ed]!=0):
                edges.append([vertex,ed,adj[vertex][ed]])
        
        for ed in range(len(edges)):
            if(edges[ed][2] < minedge[2] and edges[ed][1] not in visited):
                minedge = edges[ed]
        
        MST.append(minedge)
        vertex = minedge[1]
        minedge = [None, None, float('inf')]
        
    return MST

print(Prims(6,graph))

# What if the graaph is disconnected? Apply Kruskal aproach into this approach
# You need to find the minimum edge

