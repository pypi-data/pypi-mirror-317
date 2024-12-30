from ..components.designator import Designator
from ..components.part_number import PartNumber
from ..components.pin import Pin
from ..components.rectangle import Rectangle
from ..components.symbol import Symbol, Part


pin_spacing = 50
pin_font_size = 40
pin_desc_spacing = 15


def calculate_height(symbol_data):
    left_height = len(symbol_data['left_side'])
    right_height = len(symbol_data['right_side'])
    return max(left_height, right_height) * pin_spacing + pin_spacing


def calculate_width(symbol_data):
    longest_text_left = 0
    for text in symbol_data['left_side']:
        if text != "!@#SEPARATOR#@!":
            longest_text_left = max(longest_text_left, len(text))

    longest_text_right = 0
    for text in symbol_data['right_side']:
        if text != "!@#SEPARATOR#@!":
            longest_text_right = max(longest_text_right, len(text))
    width = (longest_text_left + longest_text_right) * pin_font_size * 0.6 + 100
    return 50 * round(width / 50)


def rectangular_symbol_generator(component_data, generator_data):
    symbol = Symbol(part_number=component_data['part'],
                    designator=component_data['designator'])

    height = calculate_height(generator_data)
    width = calculate_width(generator_data)

    # symbol.width = width + 2 * 100 + 40
    # symbol.height = height + + 120

    body_x = -width/2
    body_y = -height/2

    part = Part(PartNumber(text=component_data['part'], x=body_x, y=body_y + height + 40),
                Designator(designator=component_data['designator'], x=body_x, y=body_y - 10))
    part.width = width + 2 * 100 + 40
    part.height = height + + 120
    part.add_body(Rectangle(width=width, height=height, x=body_x, y=body_y))
    add_pins(part, component_data, generator_data, width, body_y)

    symbol.add_part(part)

    return symbol


def add_pins(symbol, component_data, generator_data, width, body_y):
    left_pin_begin = -width / 2 - 100
    for i, left_pin in enumerate(generator_data['left_side']):
        if left_pin != "!@#SEPARATOR#@!":
            pin_data = component_data['pins'][left_pin]
            symbol.add_pin(Pin(name=left_pin,
                               number=pin_data['no'],
                               function=pin_data['func'],
                               description=pin_data['desc'] if 'desc' in pin_data else None,
                               x=int(left_pin_begin),
                               y=int(body_y + pin_spacing + i * pin_spacing),
                               length=100,
                               rotation=0))

    right_pin_begin = width / 2 + 100
    for i, right_pin in enumerate(generator_data['right_side']):
        if right_pin != "!@#SEPARATOR#@!":
            pin_data = component_data['pins'][right_pin]
            symbol.add_pin(Pin(name=right_pin,
                               number=pin_data['no'],
                               function=pin_data['func'],
                               description=pin_data['desc'] if 'desc' in pin_data else None,
                               x=int(right_pin_begin),
                               y=int(body_y + pin_spacing + i * pin_spacing),
                               length=100,
                               rotation=180))
