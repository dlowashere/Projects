"""
 Copyright (c) 2010 Daniel Lo

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Simple game of life implementation.

Press escape to exit.
Press 'r' to restart with a new random start.

Author: Daniel Lo
"""

import pygame, sys, time, random

"""
Game of life grid
"""
class life_grid:

  def __init__(self, size=10):
    """
    Initialize with a size-by-size grid
    """
    # Create grid array
    self.grid = [0]*size
    for x in range(size):
      self.grid[x] = [0]*size
    self.xlen = size
    self.ylen = size

  def __repr__(self):
    string = ""
    for x in range(self.xlen):
      for y in range(self.ylen):
        string += str(self.grid[x][y]) + " "
      string += "\n"
    return string

  def set_cell(self, x, y, val):
    """
    Set cell[x][y] to val
    """
    if val != 0 and val != 1:
      raise Exception("set_cell val out of bounds")
    self.grid[x][y] = val
    
  def get_cell(self, x, y):
    """
    Return the value of the cell at x,y
    """
    return self.grid[x][y]

  def iterate(self):
    """
    Step through one time step, updating all cells
    """
    # Create a new grid for the next time step
    new_grid = [0]*self.xlen
    for x in range(self.xlen):
      new_grid[x] = [0]*self.ylen
    # For each cell
    for x in range(self.xlen):
      for y in range(self.ylen):
        # Update cell based on number of cells surrounding set
        if self.cell_sum(x,y) in range(3,5):
          new_grid[x][y] = 1
        else:
          new_grid[x][y] = 0
    # Make the newly generated grid the current grid state
    self.grid = new_grid

  def cell_sum(self, x, y):
    """
    Returns number of set cells around x, y, including x,y
    """
    sum = 0
    for i in range(x-1, x+2):
      for j in range(y-1, y+2):
        # Check that i,j are within bounds of array
        if (i >=0 and i < self.xlen) and (j >=0 and j < self.ylen):
          sum += self.grid[i][j]
    return sum
    
  def randomize(self, prob = .05):
    """
    Randomly set cells with probability = prob
    """
    self.clear()
    for x in range(self.xlen):
      for y in range(self.ylen):
        if random.random() < prob:
          self.set_cell(x,y,1)
  
  def clear(self):
    """
    Clears all cells
    """
    for x in range(self.xlen):
      for y in range(self.ylen):
        self.set_cell(x,y,0)
          
# Set up pygame screen
pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)

# define RGB colors
black = 0, 0, 0
white = 255, 255, 255

# Create life grid
LG_SIDE = 50 # Number of cells on each side
# pixels needed to draw each cell
xpixels = width/LG_SIDE
ypixels = height/LG_SIDE
lg = life_grid(LG_SIDE)
# Initialize pattern randomly
lg.randomize()

# Allows logging of cell values to a text file
logging = False
if logging:
  out_file = open("life.log", 'w')
    
while True:
  for event in pygame.event.get():
    # Handle key presses
    if event.type == pygame.KEYDOWN:
      # Reset with random grid when 'r' is pressed
      if event.key == pygame.K_r:
        lg.randomize()
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
      if logging:
        out_file.close()
      sys.exit()
  
  # Fill blank screen black
  screen.fill(black)
  # Draw filled cells in white
  for x in range(LG_SIDE):
    for y in range(LG_SIDE):
      if lg.get_cell(x,y) == 1:
        screen.fill(white, pygame.Rect(x*xpixels, y*ypixels, xpixels, ypixels))
  # Update to new frame
  pygame.display.flip()
  # Write state to log file
  if logging:
    out_file.write(str(lg) + "\n")
  lg.iterate() # Advance time step of life game

if logging:
  out_file.close()
