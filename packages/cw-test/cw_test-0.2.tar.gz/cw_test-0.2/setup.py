
from setuptools import setup, find_packages

setup(
    name="cw_test",
    version= "0.2",
    packages= find_packages(),
    entry_points = {
        'console_scripts': [
            "new_test = cw_test:test",
            "new_game = cw_test.call:caller",
        ]
    }
)

