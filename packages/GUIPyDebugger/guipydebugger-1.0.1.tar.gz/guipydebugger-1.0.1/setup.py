from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="GUIPyDebugger",
    version="1.0.1",
    url="https://github.com/33QWERTY33/GUI-python-debugger",
    author="Curtis Jones",
    author_email="curlejo.4career@gmail.com",
    description="GUI debugging server accessible on LAN connected devices through a browser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["django"],
    entry_points={
        "console_scripts": [
            'gui_pdb=core.start:start'
        ]
    },
    package_data={
        "editor": ["output.txt"],
        "templates": ["base/*", "about/*", "diagrammer/*", "editor/*"],
        "static": ["code_files/*", "images/*"]
    }
)
