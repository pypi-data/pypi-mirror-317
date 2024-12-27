from setuptools import setup, find_packages
import os
import re


def get_version():
    init_path = os.path.join("src", "numo_cli", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Version string not found")


setup(
    name="numo-cli",
    version=get_version(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numo>=0.2.2",
    ],
    entry_points={
        "console_scripts": [
            "numo-cli=numo_cli.main:main",
        ],
    },
    author="Furkan Cosgun",
    author_email="furkan51cosgun@gmail.com",
    description="A powerful CLI tool for calculations, unit conversions, and translations using Numo",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/furkancosgun/numo-cli",
    project_urls={
        "Bug Tracker": "https://github.com/furkancosgun/numo-cli/issues",
        "Documentation": "https://github.com/furkancosgun/numo-cli#readme",
        "Source Code": "https://github.com/furkancosgun/numo-cli",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    keywords="cli, calculator, converter, translator, utility, numo",
)
