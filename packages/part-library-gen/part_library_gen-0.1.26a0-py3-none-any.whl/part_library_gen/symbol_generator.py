import hashlib
from .generators.symbol_generator.default_generator import default_generator
from .generators.symbol_generator.multipart_generator import multipart_generator
from .generators.symbol_generator.generator_map import generator_map
from .exporters.svg.svg_exporter import export as svg_exporter

supported_pin_functions = ['In', 'Out', 'InAnalog', 'InDigital', 'InDigital;ActiveLow', 'InDigital;ActiveHigh',
                           'InDigitalClock',
                           'OutDigital', 'OutDigital;ActiveLow', 'OutDigital;OpenDrain',
                           'OutDigital;OpenDrain;ActiveLow',
                           'OutAnalog', 'OutAnalog;ActiveLow',
                           'InOut',
                           'PwrIn', 'PwrOut', 'PwrGND', 'PwrInOut',
                           'NC', 'NC-GND', 'NC-Float']


def validate(component_data):
    if component_data is not None:
        if 'designator' not in component_data:
            raise ValueError('designator is missing')
        if 'part' not in component_data:
            raise ValueError('part number is missing')
        if 'pins' not in component_data:
            raise ValueError('pins are missing')
        for pin in component_data['pins']:
            pin_data = component_data['pins'][pin]

            if 'func' not in pin_data:
                raise ValueError('pin function is missing')
            if 'no' not in pin_data:
                raise ValueError('pin number is missing')
            if pin_data['func'] not in supported_pin_functions:
                raise ValueError('pin function is not supported: {}'.format(pin_data['func']))


def generate_file_name(component_data, generator_name):
    manufacturer_name = component_data['manufacturer'].replace(' ', '_')
    part = component_data['part'].replace('#', '').replace(' ', '_')
    pins = '_'.join(component_data['pins'].keys())
    hash_hex = hashlib.sha256(pins.encode()).hexdigest()
    return f"{manufacturer_name}_{part}_{generator_name}_{hash_hex}"


def generate(data):
    validate(data)
    if 'symbol_generator' not in data:
        symbol = default_generator(data, {})
        filename = generate_file_name(data, 'generic')
        return [(symbol, filename)]
    else:
        symbols = []
        for generator in data['symbol_generator']:
            generator_data = data['symbol_generator'][generator]
            filename = generate_file_name(data, generator)
            if generator == "multipart":
                symbol = multipart_generator(data, generator_data)
                symbols.append((symbol, filename))
            else:
                symbol = generator_map[generator](data, generator_data)
                symbols.append((symbol, filename))
        return symbols


def export_symbol(symbol, filename):
    exporters = [svg_exporter]
    for exporter in exporters:
        exporter(symbol, filename)
