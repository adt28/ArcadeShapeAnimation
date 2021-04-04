"""
ArcadeShapeAnimation-Buffered:
By A.D.Tejpal - 04-Apr-2021

Arcade module for arcade.buffered_draw_commands:
https://arcade.academy/_modules/arcade/buffered_draw_commands.html

This sample demonstrates animation of multiple shapes on the
screen, using drawing commands based upon Vertex Buffer
Objects (VBOs). This approach keeps the vertices loaded on the
graphics card for faster rendering.

Buffered drawing commands start with "arcade.create_" as
against conventional "arcade.draw_" . Such functions return a Shape
object that can be drawn with "my_shape.draw()".

Multiple shapes appended to a ShapeElementList facilitate fast
performnce by implementing draw action on that list.

The sample displays a backdrop of falling snow, apart from:
(a) Animated wheels having central disc and radial spokes ending
with outer discs.
(b) Bouncing Balls.
"""

import arcade
import random, math

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 560
SCREEN_TITLE = "Shape Animation - Buffered"
FPS = 30  # Frames per sec

class Shape:
    """
    Generic class - To serve as base shape class
    """
    def __init__(
                self, x=0, y=0, width=20, height=20, 
                angle=0, delta_x=0, delta_y=0, 
                delta_angle=0, color=(255,0,0)):
        self.swd = SCREEN_WIDTH
        self.sht = SCREEN_HEIGHT
        self.cx = self.swd / 2
        self.cy = self.sht / 2
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle        
        self.color = color

        # For oscillation effect in snowfall
        # managed by class SnowDrop
        self.count = 0
        
        self.shape_list = None

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle

        # For bounce action
        if self.x < 0 and self.delta_x < 0:
            self.delta_x *= -1
        if self.y < 0 and self.delta_y < 0:
            self.delta_y *= -1
        if self.x > SCREEN_WIDTH and self.delta_x > 0:
            self.delta_x *= -1
        if self.y > SCREEN_HEIGHT and self.delta_y > 0:
            self.delta_y *= -1

    def draw(self):
        # Positioning & rotation of shape object, as well
        # as its draw action is best handled via
        # ShapeElementList containing the shape object.
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y
        self.shape_list.angle = self.angle
        self.shape_list.draw()

class SnowDrop(Shape):
    """
    This class is used for creating falling snow drops
    """

    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color):

        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                         delta_angle, color)

        shape = arcade.create_ellipse_filled(0, 0,
                                             self.width, self.height,
                                             self.color, self.angle)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)

    def move(self):
        self.x = self.x + self.delta_x
        self.count = self.count + 1

        # For lateral oscillation
        if self.count > 4:
            self.delta_x = -self.delta_x
            self.count = 0
        
        self.y = self.y - self.delta_y        
        if self.y < 0:
            self.y = SCREEN_HEIGHT + 10

class Wheel(Shape):
    """
    This class is used for creating animated wheels having
    central disc and radial spokes ending with outer discs.

    Imp:
        When rotation is involved, best results are obtained by
        creating the shape at 0,0 coordinates and later use the
        following statements for proper positioning:
        self.x = start_x
        self.y = start_y

        In this context, following statements
        do not provide desired results:
        self.shape_list.center_x = start_x
        self.shape_list.center_y = start_y
    """
    def __init__(
                self, start_x=0, start_y=0, 
                radius=50, 
                spokes=3, angle=0,
                dx=0, dy=0, dAngle=0):

        super().__init__(
            delta_x=dx, delta_y=dy, delta_angle=dAngle)

        self.shape_list = arcade.ShapeElementList()

        self.colors = [
            (255,0,0),
            (0,255,0),
            (0,0,255)]
        
        stepAngle = (2 * math.pi) / spokes
        colorCount = len(self.colors)
        for n in range(spokes):
            a = n * stepAngle
            end_x = radius*math.cos(a)
            end_y = radius*math.sin(a)
            
            color = self.colors[n % colorCount]

            sp = arcade.create_line(
                0, 0, end_x, end_y,
                color, line_width=0.1 * radius)

            self.shape_list.append(sp)

            # Outer Discs
            c_x = 1.2 * end_x 
            c_y = 1.2 * end_y

            outerDiscSize = 0.3 * radius
            ep = arcade.create_ellipse(
                c_x, c_y, outerDiscSize, outerDiscSize, color)

            self.shape_list.append(ep)

        # Center Disc
        centerDiscSize = 0.15 * radius
        ep = arcade.create_ellipse(
            0, 0, centerDiscSize, centerDiscSize, (0,0,0))

        self.shape_list.append(ep)

        # Final positioning
        self.x = start_x
        self.y = start_y

class BouncingBall(Shape):
    def __init__(
                self, start_x=0, start_y=0, 
                width=20, height=20, 
                dx=0, dy=0, 
                color=(255,0,0)):

        super().__init__(
            delta_x=dx, delta_y=dy)

        self.shape_list = arcade.ShapeElementList()
       
        ep = arcade.create_ellipse_filled(
            0, 0, width, height, color)

        self.shape_list.append(ep)

        self.x = start_x
        self.y = start_y

class GamePlay(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE, update_rate=1/FPS)

        self.swd = SCREEN_WIDTH
        self.sht = SCREEN_HEIGHT
        self.cx = self.swd/2
        self.cy = self.sht/2

        self.shapeList = None

        self.processing_time = 0
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

        self.numSnowDrops = 250

    def setup(self):
        """ Set up the game"""
        arcade.set_background_color((70, 70, 70))
        
        self.shapeList = []

        # Create shape objects as per class SnowDrop and
        # append the same to shapeList of this class
        for n in range(self.numSnowDrops):
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            width = random.randrange(2, 6)
            height = random.randrange(2, 6)
            angle = 0

            dx = (random.randrange(5, 8))/10
            dy = (random.randrange(5, 8))/10
            dAngle = 0

            if n % 2 > 0:
                dx = -dx

            if n % 10 == 0:
                width = 2 * width
                height = 2 * height

            shape = SnowDrop(x, y, width, height, angle, dx, dy,
                            dAngle, (255, 255, 255, 255))
            self.shapeList.append(shape)

            # Add some animated wheels
            shape = Wheel(
                start_x=0, start_y=self.cy, 
                radius=150, dx=1, 
                dy=0, dAngle=1)
            self.shapeList.append(shape)

            shape = Wheel(
                start_x=self.swd, start_y=self.cy, 
                radius=150, dx=-1, 
                dy=0, dAngle=-1)
            self.shapeList.append(shape)

            shape = Wheel(
                start_x=self.cx, start_y=self.sht, 
                radius=80, dx=0, 
                dy=-2, dAngle=4)
            self.shapeList.append(shape)

            shape = Wheel(
                start_x=self.cx, start_y=0, 
                radius=80, dx=0, 
                dy=2, dAngle=-4)
            self.shapeList.append(shape)

            # Add two bouncing balls
            shape = BouncingBall(
                start_x=0, start_y=0, 
                width=80, height=100, 
                dx=4, dy=4, 
                color=(255,0,0))
            self.shapeList.append(shape)

            shape = BouncingBall(
                start_x=self.swd, start_y=0, 
                width=80, height=100, 
                dx=-4, dy=4, 
                color=(0,255,0))
            self.shapeList.append(shape)
            
    def on_update(self, dt):
        for shape in self.shapeList:
            shape.move()

    def on_draw(self):
        arcade.start_render()

        for shape in self.shapeList:
            shape.draw()

#=====================
def main():
    gp = GamePlay()
    gp.setup()
    arcade.run()

#=====================
if __name__ == "__main__":
    main()
