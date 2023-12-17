import json
import pathlib
import subprocess
from typing import Optional

EXAMPLE_SCRIPT = pathlib.Path.home() / "/var/task/src/scripts/example.py"


def run_blender_script(
    script_path: pathlib.Path,
    *args,
    blend_file: Optional[pathlib.Path] = None,
    addons: Optional[list] = None,
    timeout: Optional[int] = None
) -> str:
    response_marker = "RESPONSE_MARKER"
    cmd = ["blender"]
    if blend_file is not None:
        cmd.append(blend_file.absolute().as_posix())
    cmd.extend(["-noaudio", "-b"])
    if addons:
        cmd.extend(["--addons", ",".join(addons)])
    cmd.extend(["-P", script_path.absolute().as_posix(), "--", response_marker, *args])

    run = subprocess.run(cmd, timeout=timeout, capture_output=True)
    if run.returncode != 0:
        error_msg = run.stderr.decode()
        raise Exception("Blender script raised error:\n" + error_msg)
    for line in run.stdout.decode().splitlines():
        if line.startswith(response_marker):
            return line[len(response_marker) :]
    raise Exception(
        "Blender script did not return expected response:\n" + run.stderr.decode()
    )


def handler(event, context):
    run_blender_script(EXAMPLE_SCRIPT)

    body = {
        "message": "Blender script executed successfully!",
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
