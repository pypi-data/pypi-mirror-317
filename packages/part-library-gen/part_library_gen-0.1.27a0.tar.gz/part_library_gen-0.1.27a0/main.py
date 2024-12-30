import json

from pathlib import Path
from src.part_library_gen.symbol_generator import generate, svg_exporter


def load_files(directory):
    files = Path(directory).rglob('*.json')
    return [x for x in files if not str(x).endswith('_generated.json')]


def generate_schematic_symbols(files):
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            for part in data:
                generated_symbol = generate(part)
                for gs in generated_symbol:
                    symbol, filename = gs
                    svg_exporter(symbol, 'symbols/' + filename)


if __name__ == "__main__":
    generate_schematic_symbols(load_files("tests"))
