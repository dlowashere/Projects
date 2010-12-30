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
mandelbrot.py

Generates an image representing the Mandelbrot set.

Author: Daniel Lo
"""

import pygame, sys, math

def mandelbrot(x0, y0):
  """
  Returns a triplet corresponding to a color for the location x, y.
  x0 must be between [-2.5, 1]. y0 must be between [-1, 1].
  """
  # Color for points inside the Mandelbrot set
  in_set = (0, 0, 0) # black
  
  # Check if within cardoid
  p = math.sqrt((x0-0.25)*(x0-0.25) + y0*y0)
  if x0 < p - 2*p*p + 0.25:
    return in_set
  # Check if in period-2 builb
  if (x0+1)*(x0+1) + y0*y0 < 1.0/16:
    return in_set
    
  # Initialize variables
  (x, y) = (0, 0)
  iteration = 0
  # Max iterations before declaring unbounded
  MAX_ITERATION = 1000
  while (x*x + y*y) <= 4 and iteration < MAX_ITERATION:
    # Calculate z = z^2 + z0
    (x, y) = (x*x - y*y + x0, 2*x*y + y0)
    # Increment number of iterations
    iteration += 1
  # Did not finish, assume in set
  if iteration == MAX_ITERATION:
    return in_set # red
  else:
    GRAYSCALE = False
    if GRAYSCALE:
      # Gray scale version
      gray = int(math.log(iteration)*255/math.log(MAX_ITERATION))
      return (gray, gray, gray)
    else:
      # Color version
      iteration = int(math.log(iteration)*360/math.log(MAX_ITERATION))
      c = pygame.Color(1,1,1,1)
      c.hsva = (iteration, 100, 100, 100)
      return c

def display_mandelbrot(viewx, viewy, size, pxarray, display):
  """
  Displays Mandelbrot set to display by writing to the pixel array of the
  screen (pxarray). The set is displayed from x coords of viewx[0] to viewx[1]
  and y coords of viewy[0] to viewy[1]. size is the size of the pygame window.
  """
  print viewx, viewy
  width, height = size
  for x in range(width):
    for y in range(height):
      # Scale x between [-2.5, 1] and y to be between [-1, 1]
      xscaled = (viewx[1]-viewx[0])*x/width + viewx[0]
      yscaled = (viewy[1]-viewy[0])*y/height + viewy[0]
      pxarray[x][y] = mandelbrot(xscaled, yscaled) # Calculate mandelbrot
    if x%10 == 0:
      display.flip() # Update display
  
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
  display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
  
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
          display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_r:
          # Reset view
          viewx = [-2.5, 1.0]
          viewy = [-1.0, 1.0]
          display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_x:
          # Zoom out by 2x
          viewx[0] *= 2
          viewx[1] *= 2
          viewy[0] *= 2
          viewy[1] *= 2
          display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_LEFT:
          # Shift left by half a screen
          width = viewx[1] - viewx[0]
          viewx[0] -= width/2
          viewx[1] -= width/2
          display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_RIGHT:
          # Shift right by half a screen
          width = viewx[1] - viewx[0]
          viewx[0] += width/2
          viewx[1] += width/2
          display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_UP:
          # Shift up by half a screen
          height = viewy[1] - viewy[0]
          viewy[0] -= height/2
          viewy[1] -= height/2
          display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
        elif event.key == pygame.K_DOWN:
          # Shift up by half a screen
          height = viewy[1] - viewy[0]
          viewy[0] += height/2
          viewy[1] += height/2
          display_mandelbrot(viewx, viewy, size, pxarray, pygame.display)
      # Quit
      if event.type == pygame.QUIT:
        sys.exit()
    pygame.display.flip()
    