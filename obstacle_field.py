import numpy as np
import random
import matplotlib.pyplot as plt

np.random.seed(100)

def put_tetromino(grid, random_x_index, random_y_index, random_tetromino_index):
    if(random_tetromino_index==1):
        grid[random_x_index][random_y_index] = 1
        grid[random_x_index][random_y_index+1] = 1
        grid[random_x_index][random_y_index+2] = 1
        grid[random_x_index][random_y_index+3] = 1

    elif(random_tetromino_index==2):
        grid[random_x_index][random_y_index] = 1
        grid[random_x_index][random_y_index+1] = 1
        grid[random_x_index][random_y_index+2] = 1
        grid[random_x_index+1][random_y_index+2] = 1
        
    elif(random_tetromino_index==3):
        grid[random_x_index][random_y_index] = 1
        grid[random_x_index+1][random_y_index] = 1
        grid[random_x_index+1][random_y_index+1] = 1
        grid[random_x_index+2][random_y_index+1] = 1

    else:
        grid[random_x_index][random_y_index] = 1
        grid[random_x_index+1][random_y_index] = 1
        grid[random_x_index+2][random_y_index] = 1
        grid[random_x_index+1][random_y_index+1] = 1

    return grid

def get_curr_coverage(updated_grid,grid_size):
    no_of_black_pixels = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if(updated_grid[i][j]==1):
                no_of_black_pixels+=1
    curr_coverage = no_of_black_pixels/(grid_size*grid_size)

    return curr_coverage

def make_obstacle_field(grid_size,coverage):
    grid = np.zeros((grid_size,grid_size))

    curr_coverage = 0
    des_coverage = coverage/100

    while(curr_coverage<des_coverage):
        random_x_index = random.randint(0, grid_size-4)
        random_y_index = random.randint(0, grid_size-4)

        random_tetromino_index = random.randint(1,4)

        updated_grid = put_tetromino(grid, random_x_index, random_y_index, random_tetromino_index)

        curr_coverage = get_curr_coverage(updated_grid,grid_size)

    return grid

if __name__=='__main__':
    grid_size = 128
    coverage = 10

    grid = make_obstacle_field(grid_size,coverage)

    plt.title("Obstacle field")
    plt.imshow(grid,cmap='gray_r')
    plt.show()








