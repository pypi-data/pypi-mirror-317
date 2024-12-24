import argparse
from pathlib import Path

from .errors import InvalidNameError, DuplicateNameError
from ._builder import ClassBuilder


def main():
    parser = argparse.ArgumentParser(description="Generate Python class from YAML")
    parser.add_argument(
        "--file",
        dest="yaml_file",
        type=str,
        help="Path to the YAML file",
    )
    parser.add_argument(
        "--from",
        dest="from_dir",
        type=str,
        help="Directory containing multiple YAML files",
    )
    parser.add_argument(
        "--py_result",
        type=str,
        help="Output directory for the generated Python files",
        default="./translation/",
    )

    args = parser.parse_args()

    if not args.yaml_file and not args.from_dir:
        parser.error("You must specify either --yaml_file or --from")

    output_dir = args.py_result
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    if args.from_dir:
        yaml_files = list(Path(args.from_dir).rglob("*.yaml")) + list(
            Path(args.from_dir).rglob("*.yml")
        )

        for yaml_file in yaml_files:
            try:
                generator = ClassBuilder(yaml_file, output_dir)
                generator.generate()
            except (InvalidNameError, DuplicateNameError) as e:
                print(f"Error generating from {yaml_file}: {e}")

        return

    if args.yaml_file:
        try:
            generator = ClassBuilder(args.yaml_file, output_dir)
            generator.generate()
        except (InvalidNameError, DuplicateNameError) as e:
            print(f"Error: {e}")
