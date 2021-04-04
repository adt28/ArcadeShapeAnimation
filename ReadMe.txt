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