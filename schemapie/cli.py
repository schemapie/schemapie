from schemapie.utils.api import execute
from importlib.metadata import version
import argparse

def main():
    parser = argparse.ArgumentParser(prog="schemapie")
    parser.add_argument("url", type=str, help="Complete URL of the desired API route.")
    parser.add_argument("--file", type=str, help="File name or path. Use to create reusable schemas, update existing schemas, or just to save a schema.")
    parser.add_argument("--version", action="version", version=f"schemapie {version("schemapie")}", help="Installed version of schemapie.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose Flag. Use to generate multiple examples in the output schema instead of one.")
    args = parser.parse_args()

    execute(url=args.url, file=args.file, verbose=args.verbose)