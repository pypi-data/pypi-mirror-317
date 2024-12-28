import drawsvg as svg


def draw_circle(circle, style):
    return svg.Circle(circle.center_x, circle.center_y * -1, circle.radius, **style)


def draw_lines(lines, close, style):
    points = [lines.x, lines.y]
    for point in lines.points:
        points += list(point)
    return svg.Lines(*points,
                     close=close,
                     **style)


def draw_rectangle(rectangle, style):
    return svg.Rectangle(rectangle.x,
                         rectangle.y * -1,
                         rectangle.width,
                         rectangle.height,
                         **style)
