"""'%run mscene -h' — view commands"""

from IPython.display import HTML, clear_output
import subprocess
import sys


def progress(value, max, st=None):
    p = int(100 * value / max)
    html = f"<progress value='{value}' max='{max}' style='width: 25%; accent-color: #41FDFE;'></progress> &emsp;[{p}%]"
    return HTML(html)

base_pkg = ("libcairo2-dev", "libpango1.0-dev")
latex_pkg = ("texlive",
            "texlive-latex-extra",
            "texlive-science",
            "texlive-fonts-extra",
            )

def install_manim(lite=False):

    cmd = [("apt-get", "install", "-y", pkg) for pkg in base_pkg]

    if lite:
        # [optional font] STIX Two Text (stixfonts.org)
        font_url = "https://raw.githubusercontent.com/stipub/stixfonts/master/fonts/static_ttf/STIXTwoText-Regular.ttf"
        font_path = "/usr/share/fonts/truetype/stixfonts"
        font_cmd = ("wget", "-P", font_path, font_url)
        cmd.append(font_cmd)
    else:
        for pkg in latex_pkg:
            cmd.append(("apt-get", "install", "-y", pkg))

    cmd.append(("uv", "pip", "install", "--system", "manim"))

    # cmd.append(("uv", "pip", "install", "--system", "IPython==8.21.0"))

    n = len(cmd)
    print("Installation")
    output = display(progress(0, n), display_id=True)

    for i, c in enumerate(cmd, 1):
        subprocess.run(c)
        output.update(progress(i, n))

def setup_manim():
    
    config.disable_caching = True
    config.verbosity = "WARNING"
    config.media_width = "50%"
    config.media_embed = True

    Text.set_default(font="STIX Two Text")

    info = f"Manim – Mathematical Animation Framework (Version {version('manim')})"
    
    clear_output()
    print(info)


def install_latex():
    
    cmd = [("apt-get", "install", "-y", pkg) for pkg in latex_pkg]

    n = len(cmd)
    print("Installation")
    output = display(progress(0, n), display_id=True)

    for i, c in enumerate(cmd, 1):
        subprocess.run(c)
        output.update(progress(i, n))

# if __name__ == "__main__":
def main(args = sys.argv[1:])

    # args = sys.argv[1:]

    if "manim" in args and len(args) == 1:

        if "manim" not in sys.modules:
            install_manim()

        from manim import *

        setup_manim()

    elif all(i in args for i in ("-l", "manim")) and len(args) == 2:

        if "manim" not in sys.modules:
            install_manim(lite=True)

        from manim import *

        setup_manim()

    elif "latex" in args and len(args) == 1:

        install_latex()

        from manim import *

        setup_manim()

    elif "-h" in args and len(args) == 1:

        cmd_info = "Commands\n--------\n'%run mscene manim' — install Manim\n'%run mscene -l manim' — install Manim without LaTeX\n'%run mscene latex' — install LaTeX\n'%run mscene -h' — view commands"
        print(cmd_info)

    else:

        err_msg = "Invalid Command\n'%run mscene -h' — view commands"
        print(err_msg)
    
