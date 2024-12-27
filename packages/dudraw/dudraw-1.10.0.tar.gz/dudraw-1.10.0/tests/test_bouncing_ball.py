import sys
import os
sys.path.append(os.getcwd())
import src.dudraw as dudraw

RADIUS = .05
DT = 20.0

dudraw.set_x_scale(-1.0, 1.0)
dudraw.set_y_scale(-1.0, 1.0)

rx = .480
ry = .860
vx = .015
vy = .023

while True:
    # Update ball position and draw it there.
    if abs(rx + vx) + RADIUS > 1.0:
        vx = -vx
    if abs(ry + vy) + RADIUS > 1.0:
        vy = -vy
    rx = rx + vx
    ry = ry + vy
    dudraw.clear(dudraw.GRAY)

    dudraw.set_pen_color_rgb( 50, 255, 50, 255 )
    dudraw.filled_square( 0.0, 0.0, 0.5 )

    dudraw.set_pen_color_rgb( 200, 200, 200, 100 )
    dudraw.filled_circle(rx, ry, RADIUS)
    dudraw.show(DT)
