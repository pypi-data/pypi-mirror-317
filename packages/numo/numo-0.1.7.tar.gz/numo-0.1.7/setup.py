import os
import re
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_version():
    init_path = os.path.join("src", "numo", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Version string not found")


setup(
    name="numo",
    version=get_version(),
    author="Furkan Coşgun",
    author_email="furkan51cosgun@gmail.com",
    description="A Python library for mathematical operations, unit conversions, currency conversions, and translations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/furkancosgun/numo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "aiohttp>=3.8.0",
    ],
    include_package_data=True,
    package_data={
        "numo": ["infrastructure/runners/units/data/*.json"],
    },
)
