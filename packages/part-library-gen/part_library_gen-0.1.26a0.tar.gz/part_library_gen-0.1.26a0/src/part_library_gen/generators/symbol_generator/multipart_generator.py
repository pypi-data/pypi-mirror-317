from ..components.symbol import Symbol
from .generator_map import generator_map


def multipart_generator(component_data, generator_data):
    symbol = Symbol(component_data['part'], component_data['designator'])
    for part in generator_data:
        part_generator_name = generator_data[part]["generator_name"]
        part_generator_data = generator_data[part]["generator_data"]

        symbol_dict = {
            "designator": component_data['designator'],
            "manufacturer": component_data['manufacturer'],
            "part": component_data['part'],
            "pins": {key: component_data['pins'][key] for key in generator_data[part]['pins']}
        }
        generated_symbol = generator_map[part_generator_name](symbol_dict, part_generator_data)
        symbol.add_part(generated_symbol.parts[0])
    return symbol
