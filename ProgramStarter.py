import psutil
import subprocess
import json
import os.path

json_tasks = json.loads(open("tasks.json", "r").read())

for task in json_tasks["Tasks"]:
    path = task["path"]
    exe = task["exe"]
    args = task["args"]
    name = task["name"]

    # Build system argument list
    cmd = list()
    cmd.append(os.path.join(path, exe))
    cmd.extend(args)

    running_already = False

    # Determine if this program is already running
    for running_process in psutil.process_iter():
        if running_process.name().casefold() == exe.casefold():
            running_already = True
            break

    if not running_already:
        try:
            pid = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE).pid
            print("Started", name, "with pid:", pid)
        except (SystemError, FileNotFoundError):
            print("Had an issue opening", name)
           
    else:
        print(name, "already running.")
