from ..components.symbol import Symbol, Part
from ..components.designator import Designator
from ..components.part_number import PartNumber
from ..components.pin import Pin
from ..components.line import Line
from ..components.lines import Lines
from ...styles import default_style


def opamp_generator(component_data, generator_data):
    symbol = Symbol(part_number=component_data['part'],
                    designator=component_data['designator'])

    height = default_style.pin_spacing * 4
    width = default_style.pin_spacing * 5
    #symbol.width = width + 2 * 100 + 40
    #symbol.height = height + 120

    body_x = -width / 2
    body_y = -height / 2
    part = Part(PartNumber(text=component_data['part'], x=-50, y=body_y + height + 40),
                Designator(designator=component_data['designator'], x=-50, y=body_y - 10))
    part.width = width + 2 * 100 + 40
    part.height = height + 120

    # draw triangle body
    triangle = Lines(default_style.pin_spacing * 3, 0)
    triangle.add_point(0, default_style.pin_spacing * 2)
    triangle.add_point(0, default_style.pin_spacing * -2)
    triangle.add_point(default_style.pin_spacing * 3, 0)
    part.add_body(triangle)
    # draw '+' and '-' inside body
    plus1 = Line(x1=10, y1=default_style.pin_spacing, x2=30, y2=default_style.pin_spacing)
    plus2 = Line(x1=10 + 10, y1=default_style.pin_spacing + 10, x2=10 + 10, y2=default_style.pin_spacing - 10)
    minus = Line(x1=10, y1=default_style.pin_spacing * -1, x2=30, y2=default_style.pin_spacing * -1)
    part.add_body(plus1)
    part.add_body(plus2)
    part.add_body(minus)

    pins = find_pins(component_data)
    # add positive pin
    pos_pin_dict = component_data['pins'][pins['pos']]
    pos_pin = Pin(name=pins['pos'],
                  number=pos_pin_dict['no'],
                  function=pos_pin_dict['func'],
                  description=pos_pin_dict['desc'],
                  x=default_style.pin_length * -1,
                  y=default_style.pin_spacing,
                  length=default_style.pin_length,
                  rotation=0,
                  name_visible=False)
    part.add_pin(pos_pin)

    # add negative pin
    neg_pin_dict = component_data['pins'][pins['neg']]
    neg_pin = Pin(name=pins['neg'],
                  number=neg_pin_dict['no'],
                  function=neg_pin_dict['func'],
                  description=neg_pin_dict["desc"],
                  x=default_style.pin_length * -1,
                  y=default_style.pin_spacing * -1,
                  length=default_style.pin_length,
                  rotation=0,
                  name_visible=False)
    part.add_pin(neg_pin)

    # add output pin
    out_pin_dict = component_data['pins'][pins['out']]
    out_pin = Pin(name=pins['out'],
                  number=out_pin_dict['no'],
                  function=out_pin_dict['func'],
                  description=out_pin_dict["desc"],
                  x=default_style.pin_spacing * 3,
                  y=0,
                  length=default_style.pin_length,
                  rotation=0,
                  name_visible=False)
    part.add_pin(out_pin)

    if 'pwr_pos' in pins and 'pwr_neg' in pins:
        # add power pins
        pwr_pos_pin_dict = component_data['pins'][pins['pwr_pos']]
        pwr_pos_pin = Pin(name=pins['pwr_pos'],
                          number=pwr_pos_pin_dict['no'],
                          function=pwr_pos_pin_dict['func'],
                          description=pwr_pos_pin_dict["desc"],
                          x=default_style.pin_spacing,
                          y=default_style.pin_spacing * -3,
                          length=default_style.pin_length - 16,
                          rotation=90,
                          name_visible=False)
        part.add_pin(pwr_pos_pin)

        # add negative power pin
        pwr_neg_pin_dict = component_data['pins'][pins['pwr_neg']]
        pwr_neg_pin = Pin(name=pins['pwr_neg'],
                          number=pwr_neg_pin_dict['no'],
                          function=pwr_neg_pin_dict['func'],
                          description=pwr_neg_pin_dict["desc"],
                          x=default_style.pin_spacing,
                          y=default_style.pin_spacing * 3,
                          length=default_style.pin_length - 16,
                          rotation=270,
                          name_visible=False)
        part.add_pin(pwr_neg_pin)

    symbol.add_part(part)
    return symbol


def find_pins(component_data):
    pins = {'pos': None,
            'neg': None,
            'out': None}
    for pin in component_data['pins']:
        if pin.startswith('IN') and '+' in pin and 'InAnalog' in component_data['pins'][pin]['func']:
            pins['pos'] = pin
        if pin.startswith('IN') and '-' in pin and 'InAnalog' in component_data['pins'][pin]['func']:
            pins['neg'] = pin
        if pin.startswith('OUT') and 'OutAnalog' in component_data['pins'][pin]['func']:
            pins['out'] = pin
        if 'PwrIn' in component_data['pins'][pin]['func']:
            if '+' in pin or pin == 'VCC+':
                pins['pwr_pos'] = pin
            if '-' in pin or pin == 'GND':
                pins['pwr_neg'] = pin
    return pins
