import numpy as np
import math
import random
import argparse
from queue import Queue
from collections import deque
from obstacle_field import make_obstacle_field
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--grid_size", type=int, help="grid size")
parser.add_argument(
    "--coverage", type=int, help="obstacle coverage percentage"
)
args = parser.parse_args()

#Functions to choose a start and end location for the graph traveral algorithm.
def choose_start(exploring_limit,grid):
    possible_start_locations = []

    for i in range(exploring_limit):
        for j in range(exploring_limit):
            if grid[i][j]!=1:
                possible_start_locations.append([i,j])

    return possible_start_locations

def choose_end(south_west,grid):
    grid_size = grid.shape[0]
    possible_end_locations = []

    for i in range(south_west,grid_size):
        for j in range(south_west,grid_size):
            if grid[i][j]!=1:
                possible_end_locations.append([i,j])

    return possible_end_locations

#Returns 2 lists each of 2 values each for the 2D coordinates corresponding to start and end values
def choose_start_and_goal(grid):
    grid_size = grid.shape[0]
    exploring_limit = int(0.2*grid_size) # Explore 20 percent of the grid from north west and south east corners to find the possible start and end goal locations

    possible_start_locations = choose_start(exploring_limit,grid)

    south_west = grid_size - exploring_limit

    possible_end_locations = choose_end(south_west,grid)
            
    random_start_location = random.choice(possible_start_locations)
    random_end_location = random.choice(possible_end_locations)

    return random_start_location, random_end_location

#Function to check which of the neighbouring vertices are valid and returns a list of those valid neighbour coordinates
def approved_neighbour_nodes(i,j,grid):
    grid_size = grid.shape[0]
    if grid[i][j]==1:
        return []
    neighbours = []
    if i-1>=0 and j>=0 and i-1<=grid_size-1 and j<=grid_size-1:
        if grid[i-1][j]!=1:
            neighbours.append((i-1,j))
    if i+1>=0 and j>=0 and i+1<=grid_size-1 and j<=grid_size-1:
        if grid[i+1][j]!=1:
            neighbours.append((i+1,j))
    if i>=0 and j-1>=0 and i<=grid_size-1 and j-1<=grid_size-1:
        if grid[i][j-1]!=1:
            neighbours.append((i,j-1))
    if i>=0 and j+1>=0 and i<=grid_size-1 and j+1<=grid_size-1:
        if grid[i][j+1]!=1:
            neighbours.append((i,j+1))
    return neighbours

#Function to check which of the neighbouring vertices are valid and returns a dictionary of those valid neighbour coordinates, here all 8 directions are checked.
def approved_weighted_neighbour_nodes(i,j,grid):
    grid_size = grid.shape[0]
    if grid[i][j]==1:
        return {}
    neighbours = {}
    if i-1>=0 and j>=0 and i-1<=grid_size-1 and j<=grid_size-1:
        if grid[i-1][j]!=1:
            neighbours[(i-1,j)]=math.dist((i,j),(i-1,j))
    if i+1>=0 and j>=0 and i+1<=grid_size-1 and j<=grid_size-1:
        if grid[i+1][j]!=1:
            neighbours[(i+1,j)]=math.dist((i,j),(i+1,j))
    if i>=0 and j-1>=0 and i<=grid_size-1 and j-1<=grid_size-1:
        if grid[i][j-1]!=1:
            neighbours[(i,j-1)]=math.dist((i,j),(i,j-1))
    if i>=0 and j+1>=0 and i<=grid_size-1 and j+1<=grid_size-1:
        if grid[i][j+1]!=1:
            neighbours[(i,j+1)]=math.dist((i,j),(i,j+1))
    if i-1>=0 and j-1>=0 and i-1<=grid_size-1 and j-1<=grid_size-1:
        if grid[i-1][j-1]!=1:
            neighbours[(i-1,j-1)]=math.dist((i,j),(i-1,j-1))
    if i-1>=0 and j+1>=0 and i-1<=grid_size-1 and j+1<=grid_size-1:
        if grid[i-1][j+1]!=1:
            neighbours[(i-1,j+1)]=math.dist((i,j),(i-1,j+1))
    if i+1>=0 and j-1>=0 and i+1<=grid_size-1 and j-1<=grid_size-1:
        if grid[i+1][j-1]!=1:
            neighbours[(i+1,j-1)]=math.dist((i,j),(i+1,j-1))
    if i+1>=0 and j+1>=0 and i+1<=grid_size-1 and j+1<=grid_size-1:
        if grid[i+1][j+1]!=1:
            neighbours[(i+1,j+1)]=math.dist((i,j),(i+1,j+1))
    return neighbours

#Function to create an adjacency list representation of the graph for the algorithm to traverse
def create_adjacency_list(grid):
    adjacency_list = {}
    grid_size = grid.shape[0]

    for i in range(grid_size):
        for j in range(grid_size):
            adjacency_list[(i,j)] = approved_neighbour_nodes(i,j,grid)

    return adjacency_list

#Function to create an weghted adjacency list representation of the graph for the algorithm to traverse
def create_weighted_adjacency_list(grid):
    adjacency_list = {}
    grid_size = grid.shape[0]

    for i in range(grid_size):
        for j in range(grid_size):
            adjacency_list[(i,j)] = approved_weighted_neighbour_nodes(i,j,grid)

    return adjacency_list

#Function for Breadth First Search Traversal
def bfs(adjacency_list, start, end):
    nodes_visited = Queue()
    generated_path = []
    visited = dict.fromkeys(adjacency_list, False)
    parent = dict.fromkeys(adjacency_list,False)

    visited[tuple(start)] = True
    nodes_visited.put(tuple(start))

    while not nodes_visited.empty():
        curr = nodes_visited.get()
        generated_path.append(curr)
        for connected_member in adjacency_list[curr]:
            if visited[connected_member]==False:
                if connected_member == tuple(end):
                    visited[connected_member] = True
                    parent[connected_member] = curr
                    with nodes_visited.mutex:
                        nodes_visited.queue.clear()
                    break
                visited[connected_member] = True
                parent[connected_member] = curr
                nodes_visited.put(connected_member)
           
    final_path = []
    current = tuple(end)
    while current!=tuple(start):
        next = parent[current]
        final_path.append(next)
        current = next
            
    return generated_path, final_path    

#Function which returns a list of unvisited neighbours in a graph, called by random traversal function
def get_unvisited_connected_members(vertex,graph,visited):
    unvisited_connected_members = []
    for connected_member in graph.get(vertex, []):
        if not visited[connected_member]:
            unvisited_connected_members.append(connected_member)
    return unvisited_connected_members

#Function for Depth First Search Traversal
def dfs(adjacency_list, start, end):
    stack = deque()
    generated_path = []
    visited = dict.fromkeys(adjacency_list, False)
    parent = dict.fromkeys(adjacency_list,False)

    curr = tuple(start)
    visited[curr] = True
    generated_path.append(curr)
    stack.append(curr)

    while len(stack)!=0:
        connected_members = get_unvisited_connected_members(curr,adjacency_list,visited)
        if len(connected_members)==0:
            curr = stack.pop()

        for connected_member in connected_members:
            if visited[connected_member]==False:
                if connected_member==tuple(end):
                    visited[connected_member]=True
                    parent[connected_member]=curr
                    generated_path.append(connected_member)
                    stack.clear()
                    break
            visited[connected_member]=True
            parent[connected_member]=curr
            generated_path.append(connected_member)
            stack.append(curr)
            curr=connected_member
            break
            
    final_path = []
    current = tuple(end)
    while current!=tuple(start):
        next = parent[current]
        final_path.append(next)
        current = next
            
    return generated_path, final_path 

#Random planner function
def random_planner(adjacency_list, start, end):
    generated_path = []
    visited = dict.fromkeys(adjacency_list, False)
    parent = dict.fromkeys(adjacency_list,False)

    curr = tuple(start)
    visited[curr] = True
    generated_path.append(curr)

    while curr!=tuple(end) or len(generated_path)<=1000:
        connected_members = get_unvisited_connected_members(curr,adjacency_list,visited)
        
        if not connected_members:
            curr = parent[curr]
            continue

        connected_member = random.choice(adjacency_list[curr])
        if visited[connected_member]==False:
             visited[connected_member]=True
             generated_path.append(connected_member)
             parent[connected_member] = curr
             curr = connected_member

    return generated_path

#Djikstra algorithm function
def dijkstra(weighted_adjacency_list,start,end):
    nodes_visited = Queue()
    generated_path = []
    visited = dict.fromkeys(weighted_adjacency_list, False)
    parent = dict.fromkeys(weighted_adjacency_list,False)

    visited[tuple(start)] = True
    nodes_visited.put(tuple(start))

    while not nodes_visited.empty():
        curr = nodes_visited.get()
        generated_path.append(curr)
        for connected_member in weighted_adjacency_list[curr]:
            if visited[connected_member]==False:
                if connected_member == tuple(end):
                    visited[connected_member] = True
                    parent[connected_member] = curr
                    with nodes_visited.mutex:
                        nodes_visited.queue.clear()
                    break
                visited[connected_member] = True
                parent[connected_member] = curr
                nodes_visited.put(connected_member)
           
    final_path = []
    current = tuple(end)
    while current!=tuple(start):
        next = parent[current]
        final_path.append(next)
        current = next
            
    return generated_path, final_path
   
def main():

    grid_size = args.grid_size
    coverage = args.coverage

    if not grid_size:
        grid_size = 128

    if not coverage:
        coverage = 10

    grid = make_obstacle_field(grid_size,coverage)

    plt.figure()
    plt.imshow(grid,cmap='gray_r')

    start,end = choose_start_and_goal(grid)

    adjacency_list = create_adjacency_list(grid)

    weighted_adjacency_list = create_weighted_adjacency_list(grid)

    bfs_path, final_path_bfs = bfs(adjacency_list,start,end)

    dfs_path, final_path_dfs = dfs(adjacency_list,start,end)

    final_path_random = random_planner(adjacency_list,start,end)
    
    dijkstra_path, final_path_djikstra = dijkstra(weighted_adjacency_list,start,end) 

    no_of_iterations_bfs = len(final_path_bfs)

    no_of_iterations_dfs = len(final_path_dfs)

    no_of_iterations_random = len(final_path_random)

    no_of_iterations_djikstra = len(final_path_djikstra)

    print("No of iterations taken for BFS: ",no_of_iterations_bfs)
    print("No of iterations taken for DFS: ",no_of_iterations_dfs)
    print("No of iterations taken for Random: ",no_of_iterations_random)
    print("No of iterations taken for Djikstra: ",no_of_iterations_djikstra)

    #Below code is purely for plotting purposes
    final_1_bfs = []
    final_2_bfs = []

    final_1_dfs = []
    final_2_dfs = []

    final_1_random = []
    final_2_random = []

    final_1_djikstra = []
    final_2_djikstra = []

    for node in final_path_bfs:
        final_1_bfs.append(node[0])
        final_2_bfs.append(node[1])

    for node in final_path_dfs:
        final_1_dfs.append(node[0])
        final_2_dfs.append(node[1])

    for node in final_path_random:
        final_1_random.append(node[0])
        final_2_random.append(node[1])

    for node in final_path_djikstra:
        final_1_djikstra.append(node[0])
        final_2_djikstra.append(node[1])

    plt.plot(final_2_bfs,final_1_bfs,label="BFS")
    plt.plot(final_2_dfs,final_1_dfs,label="DFS")
    plt.plot(final_2_random,final_1_random,label="Random")
    plt.plot(final_2_djikstra,final_1_djikstra,label="Djikstra")
    plt.title(f"Coverage=%d percent" % coverage)
    plt.legend(loc = "upper right")
    plt.show()


if __name__=="__main__":
    main()














