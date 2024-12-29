
from .main import test
import subprocess

from IPython.display import HTML, clear_output, display
import subprocess
import sys
ipy = get_ipython()

def progress(value, max, st=None):
    p = int(100 * value / max)
    html = f"<progress value='{value}' max='{max}' style='width: 25%; accent-color: #41FDFE;'></progress> &emsp;[{p}%]"
    return HTML(html)
def magic_func(line):
    # string = "Hello World!"
    alist = line.split()
    # print(type(alist), alist)
    # pck = f"{alist[-1]}.py"
    # ll = f"{alist[-1]}"
    # url = f"https://mscene.curiouswalk.com/src/{pck}"
    cmd = ("pip","install", 'black')
    # print(cmd)
    # from numpy import *
    output = display(progress(2, 2), display_id=True)
    output = subprocess.run(cmd)
    # code = output.returncode
    # if  code == 0:
    #     dwn_cmd = ("wget","-O", pck,  url)
    #     subprocess.run(dwn_cmd)
    #     msg = f"'{pck}' download complete\n 'from {ll} import *"

    # else:
    #     msg = "file not found"
    # print(msg)
ipy.register_magic_function(magic_func, "line", "mscene")
