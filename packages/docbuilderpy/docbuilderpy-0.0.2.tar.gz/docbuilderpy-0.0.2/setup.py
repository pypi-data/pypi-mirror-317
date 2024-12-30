from setuptools import setup, find_packages

setup(
    name="docbuilderpy",
    version="0.0.2",
    description="Simple creation of documentation for Python projects.",
    author="Jan-Markus Langer",
    packages=find_packages(),
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "docbuilderpy=docbuilderpy.cli:main",
        ],
    },
)
