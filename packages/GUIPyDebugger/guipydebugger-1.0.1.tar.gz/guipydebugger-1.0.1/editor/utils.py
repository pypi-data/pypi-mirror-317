import os
import sys
import subprocess
import time

class Debugger():
    def __init__(self, filepath):

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.output_file = open(os.path.join(script_dir, "output.txt"), "r+")

        self.process = subprocess.Popen(
        ["python", "-m", 'pdb', filepath],
        stdin=subprocess.PIPE,
        stdout=self.output_file,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
        bufsize=1
        )
        # this is the actual process with interactions routed to different places

        sys.argv = [filepath]
        sys.path.append(os.path.dirname(filepath))
        # because parent process is not in debug subjects env, artificially create it


    def execute_debug_cmd(self, command):
        self.output_file.truncate(0)
        # Empty the output file, this is really just preference for output
        self.process.stdin.write(command + '\n')
        self.process.stdin.flush()
        # mimic standard pdb shell interaction

        time.sleep(0.2)
        # giving time to ensure response

        self.output_file.flush()

        self.output_file.seek(0)
        # set the cursor back to the first index
        output = self.output_file.readlines()
        # read till EOF

        output = [out.lstrip("\x00") for out in output]
        # get rid of padding for elements (there's quite a bit hopefully it'll avoid issues)

        output = ("".join(output)).replace("(Pdb)", "")
        # convert to string and remove pdb prompt

        return output