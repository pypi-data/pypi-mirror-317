import drawsvg as svg
from decimal import Decimal
from .detail import draw_circle
from .detail import draw_lines, draw_rectangle

from ...generators.components.circle import Circle
from ...generators.components.lines import Lines
from ...generators.components.rectangle import Rectangle


def export(footprint, filename=None):
    d = svg.Drawing(footprint.width, footprint.height, origin='center')

    for pad in footprint.pads:
        parts = generate_footprint_pad(pad)
        d.append(parts[0])
        d.append(parts[1])

    for element in footprint.top_overlay:
        if isinstance(element, Lines):
            style = {'stroke_width': 0.15,
                     'fill': 'none',
                     'stroke': 'white'}
            d.append(draw_lines(element,
                                close=True,
                                style=style))
        elif isinstance(element, Circle):
            style = {'stroke_width': 0.15,
                     'fill': 'none',
                     'stroke': 'white'}
            d.append(draw_circle(element, style))

    for element in footprint.assembly_top:
        if isinstance(element, Lines):
            style = {'stroke_width': 0.15,
                     'fill': 'none',
                     'stroke': 'white'}
            d.append(draw_lines(element,
                                close=True,
                                style=style))
        elif isinstance(element, Circle):
            style = {'stroke_width': 0.15,
                     'fill': 'none',
                     'stroke': 'white'}
            d.append(draw_circle(element, style))
        elif isinstance(element, Rectangle):
            style = {'stroke_width': 0.02,
                     'fill': 'none',
                     'stroke': 'blue'}
            d.append(draw_rectangle(element, style))

    if filename:
        d.set_pixel_scale(30)
        d.save_svg(f"{filename}.svg")


def generate_footprint_pad(pad):
    center_x = pad.x
    center_y = pad.y
    rect = svg.Rectangle(center_x - pad.width / 2,
                         (center_y + pad.height / 2) * -1,
                         pad.width,
                         pad.height,
                         stroke_width=0,
                         fill='red',
                         stroke='red')
    text = svg.Text(f"{pad.number}",
                    pad.height,
                    center_x,
                    center_y * -1 + Decimal('0.1'),
                    center=True)
    return [rect, text]
