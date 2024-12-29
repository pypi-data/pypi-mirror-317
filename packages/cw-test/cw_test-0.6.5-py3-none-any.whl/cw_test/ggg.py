from IPython.display import HTML, clear_output, display
import subprocess
import sys

def install_manim():
    lite=True
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
    # output = display(progress(0, n), display_id=True)

    for i, c in enumerate(cmd, 1):
        subprocess.run(c)
        # output.update(progress(i, n))
