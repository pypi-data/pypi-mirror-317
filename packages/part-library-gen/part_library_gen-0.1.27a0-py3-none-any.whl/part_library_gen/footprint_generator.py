from .generators.footprint_generator.soic import generate as generate_soic
from .generators.footprint_generator.tssop import generate as generate_tssop
from .generators.footprint_generator.vssop import generate as generate_vssop
from .packages.tssop import TSSOP
from .packages.dimension import Dimension


generator_map = {
    "SOIC": (generate_soic, TSSOP),
    "TSSOP": (generate_tssop, TSSOP),
    "VSSOP": (generate_vssop, TSSOP)
}


def generate(data):
    generator_name = data["generator"]
    generator = generator_map[generator_name][0]
    if not isinstance(data["data"], generator_map[generator_name][1]):
        data["data"] = parse_data(data["data"], generator_map[generator_name][1])
    footprint_name = f"{generator_name}-{data['data'].pin_count}"
    return generator(data["data"], footprint_name), footprint_name


def parse_data(data, parameters_class):
    package_data = parameters_class()
    for parameter_name in data:
        if parameter_name == "pin_count":
            package_data.pin_count = data[parameter_name]
        else:
            setattr(package_data, parameter_name, Dimension.from_str(data[parameter_name]))
    return package_data
