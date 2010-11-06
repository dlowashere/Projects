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

import sys, pygame, random, time, math

class Ship:
  """
  Object for spaceship
  """
  
  # Maximum (absolute) velocity
  MAX_VEL = 3
  
  def __init__(self):
    """
    Default constructor. All attributes set to 0.
    """
    self.pos = [0, 0] # Position
    self.vel = [0, 0] # Velocity
    self.acc = [0, 0] # Acceleration
    # Begins facing towards top of screen
    self.heading = math.pi # Heading in radians
    # Default screen size causes no wrapping
    self.screen = [0, 0]
  
  def __init__(self, pos):
    """
    Constructor with position set.
    """
    self.pos = pos
    self.vel = [0, 0]
    self.acc = [0, 0]
    self.heading = math.pi
    self.screen = [0, 0]
    
  def get_position_int(self):
    x = int(self.pos[0])
    y = int(self.pos[1])
    return [x, y]

  def rotate(self, coord):
    """
    Returns [x,y] rotated by the heading
    """
    [x, y] = coord
    xrot = x*math.cos(self.heading) - y*math.sin(self.heading)
    yrot = x*math.sin(self.heading) + y*math.cos(self.heading)
    return [xrot, yrot]
    
  def ship_outline(self):
    # Ship at origin
    vertices = [[0, 10], [-5, -5], [5, -5]]
    [x, y] = self.get_position_int()
    # Rotate at origin
    for i in range(len(vertices)):
      vertices[i] = self.rotate(vertices[i])
    # translate
    for i in range(len(vertices)):
      vertices[i] = [vertices[i][0] + x, vertices[i][1] + y]
    return vertices
    
  def accelerate(self, acc):
    acc_rot = self.rotate([0, acc])
    self.acc[0] += acc_rot[0]
    self.acc[1] += acc_rot[1]
    
  def set_position(self, pos):
    self.pos = pos
    
  def set_velocity(self, vel):
    self.vel = vel
  
  def set_acceleration(self, acc):
    self.acc = acc
    
  def set_screen(self, size):
    """
    Set screen size of game so ship position wraps.
    """
    self.screen = size
    
  def update(self):
    """
    Updates position and velocity.
    """
    t = 1 # time step
    # Calculate new position
    pos_x = self.pos[0] + self.vel[0]*t + self.acc[0]*t*t
    pos_y = self.pos[1] + self.vel[1]*t + self.acc[1]*t*t
    if self.screen[0]:
      pos_x = pos_x % self.screen[0]
    if self.screen[1]:
      pos_y = pos_y % self.screen[1]
    # Bound velocities by -MAX_VEL and MAX_VEL
    vel_x = max(min(self.vel[0] + self.acc[0]*t, self.MAX_VEL), -self.MAX_VEL)
    vel_y = max(min(self.vel[1] + self.acc[1]*t, self.MAX_VEL), -self.MAX_VEL)
    # Don't update position and velocity until end so all values used in
    # calculations are previous values
    self.pos = [pos_x, pos_y]
    self.vel = [vel_x, vel_y]
    
class Bullet:
  """
  Class for bullets that the ship shoots
  """
  
  VELOCITY = 5
  
  def __init__(self):
    # Initial position
    self.pos = [0, 0]
    # Velocity of bullet
    self.velocity = [0, 0]
    # Age of bullet, bullets eventually "die"
    self.age = 0
    # Screen size for wrapping, if 0, 0 then no wrap
    self.screen = [0, 0]
    
  def __init__(self, pos, heading, screen):
    self.pos = pos
    self.heading = heading
    # Calculate velocity from heading
    self.vel = [0, 0]
    self.vel[0] = -self.VELOCITY*math.sin(heading)
    self.vel[1] = self.VELOCITY*math.cos(heading)
    self.age = 0
    self.screen = screen
    
  def get_position_int(self):
    x = int(self.pos[0])
    y = int(self.pos[1])
    return [x, y]
  
  def update(self):
    """
    Update bullet position
    """
    t = 1 # time step
    posx = self.pos[0] + t*self.vel[0]
    posy = self.pos[1] + t*self.vel[1]
    # Wrap around screen
    if self.screen[0]:
      posx %= self.screen[0]
    if self.screen[1]:
      posy %= self.screen[1]
    self.pos = [posx, posy]
    self.age += 1
    
class Asteroid:
  """
  Class for asteroid object
  """
  
  def __init__(self):
    # Position
    self.pos = [0, 0]
   
  def __init__(self, pos):
    self.pos = pos
    
  def get_position_int(self):
    return [int(self.pos[0]), int(self.pos[1])]

# Initialize pygame screen    
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

# colors
black = 0, 0, 0
white = 255,255,255
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
dark_green = 34, 177, 76

# Create a ship
s = Ship([width/2, height/2])
s.set_screen(size)
# Initial empty bullet list
bullets = []
# Asteroids list
asteroids = []
# Create an asteroid
for i in range(10):
  asteroids.append(Asteroid([random.randint(30, 469), random.randint(30, 469)]))

while 1:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      # Shoot bullet
      if event.key == pygame.K_SPACE:
        bullets.append(Bullet(s.pos, s.heading, size))
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
    
  # Get keys pressed down
  keys = pygame.key.get_pressed()
  # Parameters to set rate of acceleration and rotation
  UNIT_ACCEL = .01
  UNIT_ROTATE = 5 # degrees
  # Accelerate forward when UP is pressed
  if keys[pygame.K_UP]:
    s.accelerate(UNIT_ACCEL)
  # Rotate CCW when LEFT is pressed
  if keys[pygame.K_LEFT]:
    s.heading -= (UNIT_ROTATE*math.pi/180)
    s.heading %= 2*math.pi
  # Rotate CW when RIGHT is pressed
  if keys[pygame.K_RIGHT]:
    s.heading += (UNIT_ROTATE*math.pi/180)
    s.heading %= 2*math.pi
    
  # Clear screen
  screen.fill(black)
  # Update and draw ship
  s.update()
  pygame.draw.polygon(screen, white, s.ship_outline())
  MAX_AGE = 50
  # Update and draw bullets
  for b in bullets:
    b.update()
    if b.age > MAX_AGE:
      bullets.remove(b)
    pygame.draw.circle(screen, white, b.get_position_int(), 3)
  # Handle each asteroid
  for a in asteroids:
    # Create rect for asteroid
    a_rect = pygame.Rect(0, 0, 0, 0)
    a_rect.center = a.get_position_int()
    a_rect.width = 30
    a_rect.height = 30
    hit = False
    # Check for collision with bullets
    for b in bullets:
      if a_rect.collidepoint(b.pos):
        hit = True
        asteroids.remove(a)
        bullets.remove(b)
    # Draw asteroids
    if not hit:
      pygame.draw.rect(screen, red, a_rect)
    
  pygame.display.flip() # Update displayed frame
  
  # Control game speed
  time.sleep(.01)
