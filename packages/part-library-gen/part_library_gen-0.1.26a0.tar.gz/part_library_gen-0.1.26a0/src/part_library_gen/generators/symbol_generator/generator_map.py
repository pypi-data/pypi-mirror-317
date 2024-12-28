from .default_generator import default_generator
from .opamp_generator import opamp_generator
from .rectangular_symbol_generator import rectangular_symbol_generator


generator_map = {'default': default_generator,
                 'rectangle': rectangular_symbol_generator,
                 'opamp': opamp_generator
                 }
