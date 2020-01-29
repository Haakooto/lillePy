import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import time
from subprocess import run

def get_tkinter():
    print()
    print("Preparing to install tkinter")
    print("This requires a reconstruction of python")
    print("That will be done using pyenv")
    if not input("Is that okay? [Y/n]") == "Y":
        return 0
    run("sudo apt-get install python-tk python3-tk tk-dev".split())
    run("git clone https://github.com/pyenv/pyenv.git ~/.pyenv".split())
    Vpy = get_py_version()
    run(f"pyenv install {Vpy}".split)

    with open("~/.bashrc", "a") as file:
        file.write('export PATH="$PYENV_ROOT/bin:$PATH"\n')
        file.write('export PYENV_ROOT="$HOME/.pyenv"\n')
        file.write('if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi\n')
    run('exec "$SHELL"'.split())



def main():
    try:
        import _tkinter
        import tkinter
    except ImportError:
        get_tkinter()
    else:
        print(f"tkinter already installed")


if __name__ == "__main__":
    main()


pyenv global system 3.8.1
touch ~/.python-version
echo '3.8.1' >> ~/.python-version
