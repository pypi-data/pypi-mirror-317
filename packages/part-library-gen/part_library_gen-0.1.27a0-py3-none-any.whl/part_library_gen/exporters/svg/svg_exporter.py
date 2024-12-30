import drawsvg as svg
from drawsvg import Circle

from .pin import generate_symbol_pin
from ...generators.components.rectangle import Rectangle
from ...generators.components.line import Line
from ...generators.components.lines import Lines


def export(symbol, filename=None):
    parts_svg = []
    for i, part in enumerate(symbol.parts):
        d = svg.Drawing(part.width, part.height, origin='center')

        for element in part.body:
            if isinstance(element, Rectangle):
                d.append(svg.Rectangle(element.x,
                                       element.y,
                                       element.width,
                                       element.height,
                                       stroke_width=3,
                                       fill='yellow',
                                       stroke='black'))
            if isinstance(element, Lines):
                points = [element.x, element.y]
                for point in element.points:
                    points += list(point)
                d.append(svg.Lines(*points,
                                   stroke_width=4,
                                   fill='yellow',
                                   stroke='black'))
            if isinstance(element, Line):
                d.append(svg.Line(element.x1, element.y1, element.x2, element.y2, stroke_width=4, stroke='black'))

        for pin in part.pins:
            d.append(generate_symbol_pin(pin))

        d.append(svg.Text(part.designator.designator,
                          40,
                          part.designator.x,
                          part.designator.y))

        d.append(svg.Text(part.part_number.text,
                          40,
                          part.part_number.x,
                          part.part_number.y))

        if filename:
            if len(symbol.parts) > 1:
                d.save_svg(f"{filename}_{i}.svg")
            else:
                d.save_svg(f"{filename}.svg")
        parts_svg.append(d.as_svg())
    return parts_svg
