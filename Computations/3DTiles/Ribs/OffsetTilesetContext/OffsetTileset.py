import os
import sys
import json
import argparse


def define_parser():
    parser = argparse.ArgumentParser(
        description="""
        Generate a triangulation file and the associated point cloud file
        out of the Blender (manually) defined model.
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--offset-x",
        help="Offset to be applied along the X axis (as float number)",
        default=0.0,
        type=float,
    )
    parser.add_argument(
        "--offset-y",
        help="Offset to be applied along the Y axis (as float number)",
        default=0.0,
        type=float,
    )
    parser.add_argument(
        "--offset-z",
        help="Offset to be applied along the Z axis (as float number)",
        default=0.0,
        type=float,
    )
    parser.add_argument(
        "--input-dir",
        help="Directory where the tileset.json is to be found",
        default=".",
        type=str,
    )
    parser.add_argument(
        "--rename-string",
        help="String to be appended to the original filename.",
        default="translated",
        type=str,
    )
    return parser


default_transform = [
    1.0,
    0.0,
    0.0,
    0.0,
    0.0,
    1.0,
    0.0,
    0.0,
    0.0,
    0.0,
    1.0,
    0.0,
    0.0,
    0.0,
    0.0,
    1.0,
]


def main():
    parser = define_parser()
    args = parser.parse_args()

    tileset_filename = os.path.join(args.input_dir, "tileset.json")

    if not os.path.isfile(tileset_filename):
        print("Directory ", args.input_dir, " has not tileset.json file.")
        print("Exiting")
        sys.exit(1)
    with open(tileset_filename, "r") as read_file:
        data = json.load(read_file)

    if "root" not in data:
        print("Tileset entry file ", tileset_filename, " has not root tile!?!?")
        print("Exiting")
        sys.exit(1)
    root_tile = data["root"]
    if "transform" not in root_tile:
        root_tile["transform"] = default_transform
        print("Root tile had no transform matrix. A default one was provided.")
    transform = root_tile["transform"]

    if args.offset_x:
        transform[12] += args.offset_x
    if args.offset_y:
        transform[13] += args.offset_y
    if args.offset_z:
        transform[14] += args.offset_z

    output_filename = os.path.join(
        os.path.dirname(tileset_filename),
        os.path.basename(tileset_filename).split(".", 1)[0]
        + "-"
        + args.rename_string
        + ".json",
    )
    with open(output_filename, "w") as write_file:
        json.dump(data, write_file)


if __name__ == "__main__":
    main()
