"""Tools module for SMuFLbuilder.

This module provides basic drawing functions tools used by makers to create
specific glyphs and components.

Functions:

draw_rectangle() -- draws a rectangle
draw_circle() -- draws a circle
draw_slash() -- draws slash with vertical ends
draw_rect_frame() -- draws an outlined rectangle
draw_circle_frame() -- draws an outlined circle
"""

# (c) 2021 by Knut Nergaard.

from smuflbuilder import helpers
from FL import *


def draw_rectangle(glyph, p, width, height):
    '''Draws rectangle of assigned width and height.'''
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


def draw_circle(glyph, p, radius):
    '''Draws circle of assigned radius.'''
    degree = 0.5519
    sd = radius * degree  # Sets basier length to 55.19% of radius for circle.
    node = Node(17, Point(p.x - radius, p.y))  # 17 = Move
    node.alignment = 12288  # Fixed
    glyph.Add(node)  # Add starting point

    node.type = 35  # Curve
    node.points = [Point(p.x, p.y - radius), Point(p.x - radius, p.y - sd),
                   Point(p.x - sd, p.y - radius)]
    glyph.Add(node)
    node.points = [Point(p.x + radius, p.y), Point(p.x + sd, p.y - radius),
                   Point(p.x + radius, p.y - sd)]
    glyph.Add(node)
    node.points = [Point(p.x, p.y + radius), Point(p.x + radius, p.y + sd),
                   Point(p.x + sd, p.y + radius)]
    glyph.Add(node)
    node.points = [Point(p.x - radius, p.y), Point(p.x - sd, p.y + radius),
                   Point(p.x - radius, p.y + sd)]
    glyph.Add(node)


def draw_slash(glyph, p, width, left_height, right_height, thickness):
    '''Draws slash with vertical ends.'''
    thickness /= 2
    node = Node(17, Point(p.x, p.y + left_height - thickness))  # 17 = Move
    node.alignment = 0  # 0 = Sharp
    glyph.Add(node)

    node.type = 1  # 1 = Line
    node.points = [Point(p.x + width, p.y + right_height - thickness)]
    glyph.Add(node)

    node.points = [Point(p.x + width, p.y + right_height + thickness)]
    glyph.Add(node)

    node.points = [Point(p.x, p.y + left_height + thickness)]
    glyph.Add(node)


def draw_rect_frame(glyph, p, width, height, thickness):
    '''Draws square frame of assigned width, height and line thickness.'''
    outer_width, outer_height = width + thickness, (height + thickness) / 2
    draw_rectangle(glyph, p, outer_width, outer_height)

    # Draw inner square.
    inner_width, inner_height = width - thickness, (height - thickness) / 2
    p.x += thickness
    draw_rectangle(glyph, p, inner_width, -inner_height)


def draw_circle_frame(glyph, p, radius, thickness):
    '''Draws circular frame of assigned radius and line thickness.'''
    # Draw outer circle.
    outer_radius = radius + thickness / 2
    registration = p
    draw_circle(glyph, registration, outer_radius)

    # Draw inner circle.
    inner_radius = radius - thickness / 2
    draw_circle(glyph, registration, inner_radius)
    glyph.ReverseContour(1)
