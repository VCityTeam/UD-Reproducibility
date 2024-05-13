import os
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


def main():
    parser = define_parser()
    args = parser.parse_args()

    tileset_filename = os.path.join(args.input_dir, "tileset.json")

    with open(tileset_filename, "r") as read_file:
        data = json.load(read_file)

    transform = data["root"]["transform"]
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
