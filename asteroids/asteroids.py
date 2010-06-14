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
Snake game

Arrow keys to move.
'r' to reset the game.
Escape to exit.

Author: Daniel Lo
"""

import sys, pygame, random, time

class Ship:
  """
  Object for spaceship
  """
  
  def __init__(self):
    """
    Default constructor. All attributes set to 0.
    """
    self.pos = [0, 0] # Position
    self.vel = [0, 0] # Velocity
    self.acc = [0, 0] # Acceleration
  
  def __init__(self, pos):
    """
    Constructor with position set.
    """
    self.pos = pos
    self.vel = [0, 0]
    self.acc = [0, 0]
    
  def set_position(self, pos):
    self.pos = pos
    
  def set_velocity(self, vel):
    self.vel = vel
  
  def set_acceleration(self, acc):
    self.acc = acc
    
  def update(self):
    """
    Updates position and velocity.
    """
    t = 1 # time step
    pos_x = self.pos[0] + self.vel[0]*t + self.acc[0]*t*t
    pos_y = self.pos[1] + self.vel[1]*t + self.acc[1]*t*t
    vel_x = self.vel[0] + self.acc[0]*t
    vel_y = self.vel[1] + self.acc[1]*t
    self.pos = [pos_x, pos_y]
    self.vel = [vel_x, vel_y]

# Initialize pygame screen    
pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)

# colors
black = 0, 0, 0
white = 255,255,255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
dark_green = 34, 177, 76

# Create a ship
s = Ship([150, 150])

time_cntr = 0
while 1:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      # Handle arrow key presses to change snake direction
      if event.key == pygame.K_UP:
        s.acc[1] -= 1
      elif event.key == pygame.K_DOWN:
        s.acc[1] += 1
      elif event.key == pygame.K_LEFT:
        s.acc[0] -= 1
      elif event.key == pygame.K_RIGHT:
        s.acc[0] += 1
      # Reset game
      elif event.key == pygame.K_r:
        #sgame.reset()
        pass
      # Quit game
      elif event.key == pygame.K_ESCAPE:
        sys.exit()        
    else:
      s.acc = [0, 0]
    if event.type == pygame.QUIT: sys.exit()

  # Clear screen
  screen.fill(black)
  pygame.draw.circle(screen, white, s.pos, 5)
  pygame.display.flip() # Update displayed frame
  
  # Control game speed
  time.sleep(.01)
  time_cntr += 1
  if (time_cntr == 10):
    s.update()
    print s.pos, s.vel, s.acc
    time_cntr = 0
