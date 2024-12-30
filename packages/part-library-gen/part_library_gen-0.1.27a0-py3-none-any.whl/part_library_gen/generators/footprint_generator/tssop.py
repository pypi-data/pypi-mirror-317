from decimal import Decimal
from .footprint import Footprint
from ..components.pad import Pad
from ..components.lines import Lines
from ..components.circle import Circle
from ..components.rectangle import Rectangle


class Parameters:
    def __init__(self, pin_count: int, pin_pitch, pad_width, pad_height, pad_row_spacing):
        self.pin_count = pin_count
        self.pin_pitch = pin_pitch
        self.pad_width = pad_width
        self.pad_height = pad_height
        self.pad_row_spacing = pad_row_spacing


def generate(package_parameters, name):
    row_spacing = package_parameters.E.get_available_max() + 2 * package_parameters.b.get_available_max() - package_parameters.L.get_available_max()
    overlay_d = package_parameters.D.get_available_max()
    overlay_e = package_parameters.E.get_available_max() - package_parameters.L.get_available_max() - Decimal('0.5')
    parameters = Parameters(pin_count=package_parameters.pin_count,
                            pin_pitch=package_parameters.e.get_available_max(),
                            pad_width=package_parameters.L.get_available_max(),
                            pad_height=package_parameters.b.get_available_max() + Decimal('0.06'),
                            pad_row_spacing=package_parameters.L.get_available_max() + 2*package_parameters.b.get_available_max()-package_parameters.L.get_available_max())

    pin_count_per_side = int(parameters.pin_count / 2)
    first_pad_y = (pin_count_per_side - 1) * parameters.pin_pitch / 2
    left_pads = add_vertical_pads(first=1,
                                  last=pin_count_per_side,
                                  pitch=parameters.pin_pitch,
                                  width=parameters.pad_width,
                                  height=parameters.pad_height,
                                  x=row_spacing / -2,
                                  y_offset=first_pad_y)
    right_pads = add_vertical_pads(first=parameters.pin_count,
                                   last=pin_count_per_side + 1,
                                   pitch=parameters.pin_pitch,
                                   width=parameters.pad_width,
                                   height=parameters.pad_height,
                                   x=row_spacing / 2,
                                   y_offset=first_pad_y)

    footprint = Footprint(name)
    footprint.add_pad(left_pads)
    footprint.add_pad(right_pads)

    # add overlay layer
    overlay_rectangle = Lines(overlay_e / -2, overlay_d / 2)
    overlay_rectangle.add_point(overlay_e / -2, overlay_d / -2)
    overlay_rectangle.add_point(overlay_e / 2, overlay_d / -2)
    overlay_rectangle.add_point(overlay_e / 2, overlay_d / 2)
    footprint.add_overlay(overlay_rectangle)
    radius = Decimal('0.5')
    spacing = Decimal('0.5')
    overlay_one_position_mark = Circle(overlay_e / -2 + radius + spacing, overlay_d / 2 - radius - spacing, radius)
    footprint.add_overlay(overlay_one_position_mark)

    # add assembly layer
    width = package_parameters.E1.get_available_max()
    height = package_parameters.D.get_available_max()
    pad_max_x = package_parameters.E.get_available_max()/2
    footprint.assembly_top.append(Rectangle(width=width, height=height, x=-width/2, y=height/2))
    for i in range(pin_count_per_side):
        pad_height = package_parameters.b.get_available_max()
        footprint.assembly_top.append(Rectangle(width=pad_max_x - width/2,
                                                height=pad_height,
                                                x=-pad_max_x,
                                                y=first_pad_y + pad_height/2 - i*parameters.pin_pitch))
        footprint.assembly_top.append(Rectangle(width=pad_max_x - width / 2,
                                                height=pad_height,
                                                x=width / 2,
                                                y=first_pad_y + pad_height/2 - i * parameters.pin_pitch))

    footprint.width = row_spacing + 3
    footprint.height = overlay_d + 2
    return footprint


def add_vertical_pads(first, last, pitch: Decimal, width: Decimal, height: Decimal, x, y_offset: Decimal):
    pads = []
    count = abs(last - first)
    for i in range(count + 1):
        pads.append(Pad(number=first + i if first < last else first - i,
                        x=x,
                        y=y_offset - Decimal(i) * pitch,
                        width=width,
                        height=height
                        ))
    return pads
