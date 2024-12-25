import argparse
from importlib.metadata import entry_points
from pigeon.utils import get_message_hash
import json


def convert(package):
    with open(f"{package}.json", "w") as f:
        json.dump(
            {
                topic: {
                    "schema": model.model_json_schema(),
                    "hash": get_message_hash(model),
                }
                for topic, model in find_package(package).items()
            },
            f,
        )


def find_package(package):
    for entrypoint in entry_points(group="pigeon.msgs"):
        if entrypoint.value.split(":")[0] == package:
            return entrypoint.load()
    raise ImportError(f"Package {package} not found!")


def main():
    parser = argparse.ArgumentParser(
        prog="Convert Messages",
        description="A script to convert message definitions from Python to JavaScript.",
    )
    parser.add_argument("package", type=str, help="The message package to convert.")

    args = parser.parse_args()

    convert(args.package)


if __name__ == "__main__":
    main()
