from .rectangular_symbol_generator import rectangular_symbol_generator


def default_generator(data, generator_data):
    half = len(data['pins']) // 2

    left_side = data['pins'].keys()
    generator_data['left_side'] = list(left_side)[:half]
    generator_data['right_side'] = list(left_side)[half:]
    return rectangular_symbol_generator(data, generator_data)
