import unittest
from src.part_library_gen.generators.symbol_generator.rectangular_symbol_generator import rectangular_symbol_generator


class TestRectangularComponentGenerator(unittest.TestCase):
    def test_symbol_generation(self):
        symbol_dict = {
            "designator": "U?",
            "manufacturer": "Test Manufacturer Name",
            "part": "Test Part Name",
            "pins": {
                "I": {"no": 1, "func": "In", "desc": "ddl"},
                "O": {"no": 2, "func": "Out", "desc": "ddl"},
                "IA": {"no": 3, "func": "InAnalog", "desc": "ddl"},
                "OA": {"no": 4, "func": "OutAnalog", "desc": "ddl"},
                "ID": {"no": 5, "func": "InDigital", "desc": "ddl"},
                "OD": {"no": 6, "func": "OutDigital", "desc": "ddl"},
                "PI": {"no": 7, "func": "PwrIn", "desc": "ddl"},
                "PO": {"no": 8, "func": "PwrOut", "desc": "ddl"},
                "PG": {"no": 9, "func": "PwrGND", "desc": "ddl"}
            }
        }
        generator_data = {
            "left_side": ["I", "O", "IA", "OA", "ID"],
            "right_side": ["OD", "PI", "PO", "PG"]
        }
        generated_symbol = rectangular_symbol_generator(symbol_dict, generator_data)
        symbol_dict = generated_symbol.to_dict()
        self.assertEqual(symbol_dict['part_number'], 'Test Part Name')
        self.assertEqual(symbol_dict['designator'], 'U?')
        self.assertEqual(len(symbol_dict['parts']), 1)
