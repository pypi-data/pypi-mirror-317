import json
import argparse

from .symbol_generator import generate


def main():
    generate_schematic_symbols()


def generate_schematic_symbols(files):
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            for part in data:
                generate(part)


if __name__ == '__main__':
    main()
