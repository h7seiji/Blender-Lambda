"""Blender script template."""
import argparse
import sys
from typing import List, Tuple

import bpy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("response_marker")

    argv = sys.argv
    argv = argv[argv.index("--") + 1 :]
    args = parser.parse_args(argv)

    scene = bpy.context.scene

    print(f"{args.response_marker}{scene.name}")

    print(f"{args.response_marker}success")

    bpy.ops.wm.quit_blender()


if __name__ == "__main__":
    main()
