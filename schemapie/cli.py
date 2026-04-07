from schemapie.utils.api import execute
from importlib.metadata import version
import argparse

def main():
    parser = argparse.ArgumentParser(prog="schemapie")
    parser.add_argument("url", type=str, help="Complete URL of the desired API route.")
    parser.add_argument("--file", type=str, help="File name or path. Used to create reusable schemas, update existing schemas, or just to save a schema.")
    parser.add_argument("--version", action="version", version=f"schemapie {version("schemapie")}", help="Installed version of schemapie.")
    args = parser.parse_args()

    execute(url=args.url, file=args.file)