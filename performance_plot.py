# 5 10 15 20 25 30 35 40
import matplotlib.pyplot as plt

bfs_iterations = [192,213,217,222,189,214,211,261]
dfs_iterations = [8318,7289,5029,5278,4463,1972,1999,1909]
random_iterations = [11175,4731,9198,6983,4508,7012,5268,2547]
djikstra_iterations = [103,111,118,126,109,125,132,139]

coverage = [5,10,15,20,25,30,35,40]

plt.plot(coverage,bfs_iterations,label="BFS")
plt.plot(coverage,dfs_iterations,label="DFS")
plt.plot(coverage,random_iterations,label="Random")
plt.plot(coverage,djikstra_iterations,label="Djikstra")
plt.title("No of iterations v/s obstacle density")
plt.xlabel("Obsacle Density")
plt.ylabel("No of Iterations")
plt.legend(loc = "upper right")

plt.show()

