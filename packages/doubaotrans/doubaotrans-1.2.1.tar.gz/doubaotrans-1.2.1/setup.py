import os
from setuptools import setup

# Let pyproject.toml handle most of the configuration
setup(
    package_dir={"": "src"},
    packages=["doubaotrans"],
    include_package_data=True,
    package_data={
        'doubaotrans': ['py.typed'],
    },
) 