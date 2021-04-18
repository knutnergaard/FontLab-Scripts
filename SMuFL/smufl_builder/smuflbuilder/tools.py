# (c) 2021 by Knut Nergaard.

from smuflbuilder import helpers
from FL import *


def draw_square(glyph, p, width, height):
    ''' Draws square of assigned width and height. '''
    node = Node(17, Point(p.x, p.y - height))  # 17 = Move
    node.alignment = 0  # 0 = Sharp
    glyph.Add(node)

    node.type = 1  # 1 = Line
    node.points = [Point(p.x + width, p.y - height)]
    glyph.Add(node)

    node.points = [Point(p.x + width, p.y + height)]
    glyph.Add(node)

    node.points = [Point(p.x, p.y + height)]
    glyph.Add(node)


def draw_circle(glyph, p, size):
    ''' Draws circle of assigned radius. '''
    degree = 0.5519
    sd = size * degree  # Sets basier length to 55.19% of radius for circle.
    node = Node(17, Point(p.x - size, p.y))  # 17 = Move
    node.alignment = 12288  # Fixed
    glyph.Add(node)  # Add starting point

    node.type = 35  # Curve

    node.points = [Point(p.x, p.y - size), Point(p.x - size, p.y - sd), Point(p.x - sd, p.y - size)]
    glyph.Add(node)

    node.points = [Point(p.x + size, p.y), Point(p.x + sd, p.y - size), Point(p.x + size, p.y - sd)]
    glyph.Add(node)

    node.points = [Point(p.x, p.y + size), Point(p.x + size, p.y + sd), Point(p.x + sd, p.y + size)]
    glyph.Add(node)

    node.points = [Point(p.x - size, p.y), Point(p.x - sd, p.y + size), Point(p.x - size, p.y + sd)]
    glyph.Add(node)


def draw_circle_frame(glyph, radius, thickness, overshoot):
    ''' Draws circular frame of assigned radiusius and line thickness. '''
    # Draw outer circle.
    outer_radius = radius + thickness / 2
    x, y = outer_radius, outer_radius + overshoot
    width = outer_radius * 2
    registration = Point(x, y)
    draw_circle(glyph, registration, outer_radius)

    # Draw inner circle.
    inner_radius = radius - thickness / 2
    x, y = inner_radius + thickness, inner_radius + thickness + overshoot
    registration = Point(x, y)
    draw_circle(glyph, registration, inner_radius)
    glyph.ReverseContour(1)


def draw_square_frame(glyph, width, height, thickness):
    ''' Draws square frame of assigned width, height and line thickness. '''
    outer_width, outer_height = width + thickness, (height + thickness) / 2
    x, y = 0, outer_height
    registration = Point(x, y)
    draw_square(glyph, registration, outer_width, outer_height)

    # Draw inner square.
    inner_width, inner_height = width - thickness, (height - thickness) / 2
    x, y = thickness, outer_height
    registration = Point(x, y)
    draw_square(glyph, registration, inner_width, -inner_height)
