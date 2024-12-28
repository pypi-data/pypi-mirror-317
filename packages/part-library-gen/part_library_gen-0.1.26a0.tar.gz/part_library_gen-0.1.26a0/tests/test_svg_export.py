import unittest
from src.part_library_gen.symbol_generator import svg_exporter
from src.part_library_gen.generators.components.symbol import Symbol
from src.part_library_gen.generators.components.part_number import PartNumber
from src.part_library_gen.generators.components.designator import Designator


class TestSVGExport(unittest.TestCase):
    def test_svg_export(self):

        symbol = Symbol(PartNumber("*", 10, 10),
                        Designator("*", 0, 0))

        svg = svg_exporter(symbol)
        self.assertIsNotNone(svg)
