# filepath: setup.py
from setuptools import setup, find_packages

setup(
    name="gimi9_tree_view",
    version="0.6.0",
    author="gisman",
    author_email="gisman@gmail.com",
    description="Visual treeview utility",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gisman/tree-view",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License-Expression:: CC-BY-NC-SA-4.0",
        "Operating System :: POSIX :: Linux",
    ],
    license="Apache-2.0",
    python_requires=">=3.2",
    # install_requires=open("requirements.txt").read().splitlines(),
    install_requires=["tomli", "wcwidth", "argparse"],
    entry_points={
        "console_scripts": [
            "treeview=gimi9_tree_view.treeview:main",
        ],
    },
)
