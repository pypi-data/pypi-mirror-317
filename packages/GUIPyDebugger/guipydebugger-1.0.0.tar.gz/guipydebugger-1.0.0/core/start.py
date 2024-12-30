import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# this fixes ModuleNotFoundError's in the installed environment... not elegant but it works

import collector
import manage
import diagrammer

def start():
    code_files = r"static\code_files"

    collector.setup(code_files)

    if len(sys.argv) == 1:
        sys.argv.append(".")
        # script defaults to cwd with no argument

    result = collector.main(sys.argv[1], code_files) # this is src and destination paths

    del sys.argv[1]
    # removing the source path so manage.py can handle all sys.argv elements properly

    sys.argv.append("runserver")
    # this start script will also run the server

    sys.argv.append("0.0.0.0:8000")

    if result != False:
        diagrammer.venv_path = result
        manage.main()

if __name__ == "__main__":
    start()