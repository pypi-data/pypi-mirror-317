from setuptools import setup, find_packages

with open("src/__init__.py") as f:
    exec(f.read())  # This will define __version__

setup(
    name="KEGGaNOG",
    version=__version__,
    description="A tool for generating KEGG heatmaps from eggnog-mapper outputs.",
    long_description=open("README_PyPI.md").read(),
    long_description_content_type="text/markdown",
    author="Ilia Popov",
    author_email="iljapopov17@gmail.com",
    url="https://github.com/iliapopov17/KEGGaNOG",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "KEGGaNOG=src.kegganog:main",  # Maps the command to the main function
        ],
    },
    install_requires=open("requirements.txt").read().splitlines(),
    python_requires=">=3.6",
)
