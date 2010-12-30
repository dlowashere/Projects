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

"""
Class for snake game board
"""
class snake_game:
  # Board item encodings
  NONE = 0
  FOOD = 1
  SNAKE_BODY = 2
  SNAKE_HEAD = 3
  SNAKE_DEAD = 4
  # Direction encodings
  UP = 0
  RIGHT = 1
  DOWN = 2
  LEFT = 3

  def __init__(self, size = 10):
    self.size = size
    # Reset game
    self.reset()
    
  def new_snake(self):
    """
    Place a new one-pixel snake somewhere on the board
    """
    # Select a random location at least one cell away from the wall
    # This prevents the snake from running right into the wall at the beginning
    x = random.randint(1, self.size-2)
    y = random.randint(1, self.size-2)
    # Snake is represented as a list of points
    self.snake = []
    self.snake.insert(0, [x,y])
    # Select a random direction for it to start going in
    self.dir = random.randint(0,3)
    self.new_dir = self.dir
    
  def new_food(self):
    """
    Place a new pixel of food on the board.
    Checks that it is not on the snake.
    """
    # Randomly generate a location until one is found that is not on the snake
    done = False
    while not done:
      x = random.randint(0, self.size-1)
      y = random.randint(0, self.size-1)
      if [x,y] not in self.snake:
        done = True
    self.food_pos = [x,y]
    
  def reset(self):
    """
    Reset game
    """
    # Create a new snake, new food, and set the snake to alive
    self.new_snake()
    self.new_food()
    self.alive = True
    
  def change_dir(self, new_dir):
    """
    Handle changing the direction the snake is travelling.
    """
    # Can't turn around
    if self.dir != (new_dir+2)%4:
      # The current direction is not changed until the game state is updated
      self.new_dir = new_dir
  
  def update(self):
    """
    Advance game one frame
    """
    # If the snake is dead, then do nothing
    if not self.alive:
      return
      
    # Head
    x, y = self.snake[0]
    # Change direction only on these updates
    self.dir = self.new_dir

    if self.dir == self.UP:
      # If the snake will hit a wall or hit itself
      if y == 0 or ([x,y-1] in self.snake):
        # Then the snake is now dead
        self.alive = False
      else:
        # Add new head position
        self.snake.insert(0, [x, y-1])
        # If food is eaten at this new position
        if [x,y-1] == self.food_pos:
          # Generate a new food and don't remove the tail (growing the snake by 1)
          self.new_food()
        else:
          # Otherwise, snake moves and remove old tail position
          self.snake.pop()        
    elif self.dir == self.DOWN:
      if y == self.size-1 or ([x,y+1] in self.snake):
        self.alive = False
      else:
        self.snake.insert(0, [x, y+1])
        if [x,y+1] == self.food_pos:
          self.new_food()
        else:
          self.snake.pop()
    elif self.dir == self.RIGHT:
      if x == self.size-1 or ([x+1, y] in self.snake):
        self.alive = False
      else:
        self.snake.insert(0, [x+1, y])
        if [x+1,y] == self.food_pos:
          self.new_food()
        else:
          self.snake.pop()
    elif self.dir == self.LEFT:
      if x == 0 or ([x-1, y] in self.snake):
        self.alive = False
      else:
        self.snake.insert(0, [x-1, y])
        if [x-1,y] == self.food_pos:
          self.new_food()
        else:
          self.snake.pop()

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

# Create new snake game
sg_size = 10 # Game is on a 10x10 grid
sgame = snake_game(sg_size)
# How many pixels wide each game board cell is
xpixels = width/sg_size
ypixels = height/sg_size

# Time_cntr is used to determine when to perform game state update
time_cntr = 0
while 1:
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      # Handle arrow key presses to change snake direction
      if event.key == pygame.K_UP:
        sgame.change_dir(sgame.UP)
      elif event.key == pygame.K_DOWN:
        sgame.change_dir(sgame.DOWN)
      elif event.key == pygame.K_LEFT:
        sgame.change_dir(sgame.LEFT)
      elif event.key == pygame.K_RIGHT:
        sgame.change_dir(sgame.RIGHT)
      # Reset game
      elif event.key == pygame.K_r:
        sgame.reset()
      # Quit game
      elif event.key == pygame.K_ESCAPE:
        sys.exit()
    if event.type == pygame.QUIT: sys.exit()

  # Clear screen
  screen.fill(black)
  # Draw snake
  if sgame.alive:
    # Alive snake is in green
    head = True
    snake_body_color = green
  else:
    # Dead snake is red
    snake_body_color = red
  for (x,y) in sgame.snake:
    # Head is a dark green (if alive)
    if head:
      snake_color = dark_green
      head = False
    else:
      snake_color = snake_body_color
    screen.fill(snake_color, pygame.Rect(x*xpixels+1, y*ypixels+1, xpixels-2, ypixels-2))
  # Draw food in white
  (x,y) = sgame.food_pos
  screen.fill(white, pygame.Rect(x*xpixels+1, y*ypixels+1, xpixels-2, ypixels-2))
  pygame.display.flip() # Update displayed frame
  
  # Control game speed
  time.sleep(.01)
  # Update game state every 0.25 seconds
  time_cntr += 1
  time_cntr %= 25
  if time_cntr == 0:
    sgame.update()
