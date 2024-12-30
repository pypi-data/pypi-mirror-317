
from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="cw_test",
    version= "1.0.4",
    packages= find_packages(),
    readme = "README.md",
    # scripts = ["cw_test/manim_setup.py"],
    long_description=long_description,
    long_description_content_type='text/markdown',

)
