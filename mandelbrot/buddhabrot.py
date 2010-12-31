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
buddhabrot.py

Generates an image of the Buddhabrot (http://en.wikipedia.org/wiki/Buddhabrot).

Author: Daniel Lo
"""

import pygame
import math
import sys
import random
def escape_mandelbrot(x0, y0):
  """
  Returns whether the point escapes (not in Mandelbrot set). If it escapes, returns
  path of escape.
  """  
  # Check if within cardoid
  p = math.sqrt((x0-0.25)*(x0-0.25) + y0*y0)
  if x0 < p - 2*p*p + 0.25:
    return False
  # Check if in period-2 builb
  if (x0+1)*(x0+1) + y0*y0 < 1.0/16:
    return False
    
  # Initialize variables
  (x, y) = (0, 0)
  iteration = 0
  path = [(x,y)] # Save path it takes to escape
  # Max iterations before declaring unbounded
  MAX_ITERATION = 1000
  while (x*x + y*y) <= 4 and iteration < MAX_ITERATION:
    # Calculate z = z^2 + z0
    (x, y) = (x*x - y*y + x0, 2*x*y + y0)
    path.append((x,y))
    # Increment number of iterations
    iteration += 1
  # Did not finish, assume in set
  if iteration == MAX_ITERATION:
    return False
  else:
    return path
      
def display_buddhabrot(viewx, viewy, size, pxarray, display):
  """
  Displays Buddhabrot set to display by writing to the pixel array of the
  screen (pxarray). The set is displayed from x coords of viewx[0] to viewx[1]
  and y coords of viewy[0] to viewy[1]. size is the size of the pygame window.
  """
  print viewx, viewy
  width, height = size
  
  # Initialize empty array of counters[width][height]
  counters = [[0 for i in range(height)] for i in range(width)]
  
  # Pick some random points
  rand_points = []
  NUM_RAND = 1000000
  for i in range(NUM_RAND):
    rand_points.append((random.randint(0, width-1), random.randint(0, height-1)))
  
  point_count = 0
  # For each random point
  for point in rand_points:
    # Scale x between viewx and y to be between viewy
    xscaled = (viewx[1]-viewx[0])*point[0]/width + viewx[0]
    yscaled = (viewy[1]-viewy[0])*point[1]/height + viewy[0]
    # Check if it escapes the Mandelbrot set
    path = escape_mandelbrot(xscaled, yscaled)
    if path != False:
      for path_point in path:
        # Convert to plot coordinates
        xplot = int((path_point[0] - viewx[0])*width/(viewx[1] - viewx[0]))
        yplot = int((path_point[1] - viewy[0])*height/(viewy[1] - viewy[0]))
        # Add to plot counters if in range
        if 0 <= xplot < width and 0 <= yplot < height:
          counters[xplot][yplot] += 1
    
    point_count += 1
    point_count %= (NUM_RAND/10)
    if point_count == 0:
      print "+10%"
      
  max_count = 0
  for i in range(width):
    if max(counters[i]) > max_count:
      max_count = max(counters[i])
  print max_count
  
  # Plot
  for x in range(width):
    for y in range(height):
      # Scale x between [-2.5, 1] and y to be between [-1, 1]
      xscaled = (viewx[1]-viewx[0])*x/width + viewx[0]
      yscaled = (viewy[1]-viewy[0])*y/height + viewy[0]
      g = counters[x][y]*3
      if g < 255:
        pxarray[x][y] = (g,g,g)
      else:
        pxarray[x][y] = (255, 255, 255)
      display.flip() # Update display
  print "Done"

if __name__ == "__main__":
  # Initialize pygame screen    
  pygame.init()
  size = width, height = 700, 400
  # Screen Surface
  screen = pygame.display.set_mode(size)
  
  # Create pixel array to access surface as array
  pxarray = pygame.PixelArray(screen)
  # coords of Mandelbrot to view
  viewx = [-2.5, 1.0]
  viewy = [-1.0, 1.0]
  # Display initial mandelbrot
  display_buddhabrot(viewx, viewy, size, pxarray, pygame.display)
  
  # Main loop
  while(True):
    # Handle pygame events
    for event in pygame.event.get():
      # Key presses
      if event.type == pygame.KEYDOWN:
        # Esc -> exit
        if event.key == pygame.K_ESCAPE:
          sys.exit()
        elif event.key == pygame.K_z:
          # Zoom in by 2x
          viewx[0] /= 2
          viewx[1] /= 2
          viewy[0] /= 2
          viewy[1] /= 2
          display_buddhabrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_r:
          # Reset view
          viewx = [-2.5, 1.0]
          viewy = [-1.0, 1.0]
          display_buddahbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_x:
          # Zoom out by 2x
          viewx[0] *= 2
          viewx[1] *= 2
          viewy[0] *= 2
          viewy[1] *= 2
          display_buddahbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_LEFT:
          # Shift left by half a screen
          width = viewx[1] - viewx[0]
          viewx[0] -= width/2
          viewx[1] -= width/2
          display_buddhabrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_RIGHT:
          # Shift right by half a screen
          width = viewx[1] - viewx[0]
          viewx[0] += width/2
          viewx[1] += width/2
          display_buddhabrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_UP:
          # Shift up by half a screen
          height = viewy[1] - viewy[0]
          viewy[0] -= height/2
          viewy[1] -= height/2
          display_buddhabrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_DOWN:
          # Shift up by half a screen
          height = viewy[1] - viewy[0]
          viewy[0] += height/2
          viewy[1] += height/2
          display_buddhabrot(viewx, viewy, size, pxarray, pygame.display)
      # Quit
      if event.type == pygame.QUIT:
        sys.exit()
