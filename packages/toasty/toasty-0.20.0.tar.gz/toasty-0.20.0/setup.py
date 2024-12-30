# -*- mode: python; coding: utf-8 -*-
# Copyright 2013-2023 Chris Beaumont and the WorldWide Telescope team
# Licensed under the MIT License

from Cython.Distutils import build_ext  # in pyproject.toml
import numpy as np  # in pyproject.toml
from setuptools import setup, Extension


def get_long_desc():
    in_preamble = True
    lines = []

    with open("README.md", "rt", encoding="utf8") as f:
        for line in f:
            if in_preamble:
                if line.startswith("<!--pypi-begin-->"):
                    in_preamble = False
            else:
                if line.startswith("<!--pypi-end-->"):
                    break
                else:
                    lines.append(line)

    lines.append(
        """

For more information, including installation instructions, please visit [the
project homepage].

[the project homepage]: https://toasty.readthedocs.io/
"""
    )
    return "".join(lines)


setup_args = dict(
    name="toasty",  # cranko project-name
    version="0.20.0",  # cranko project-version
    description="Generate image tile pyramids from existing image data",
    long_description=get_long_desc(),
    long_description_content_type="text/markdown",
    url="https://toasty.readthedocs.io/",
    license="MIT",
    platforms="Linux, Mac OS X",
    author="Chris Beaumont, WorldWide Telescope Team",
    author_email="hello@worldwidetelescope.org",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    packages=[
        "toasty",
        "toasty.pipeline",
        "toasty.tests",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "toasty=toasty.cli:entrypoint",
        ],
    },
    install_requires=[
        "filelock>=3",
        "numpy>=1.7",
        "pillow>=7.0",
        "PyYAML>=5.0",
        "reproject",
        "shapely",
        "tqdm>=4.0",
        "wwt_data_formats>=0.15",
    ],
    extras_require={
        "test": [
            "coveralls",
            "pytest-cov",
        ],
        "docs": [
            "astropy",
            "astropy-sphinx-theme",
            "numpydoc",
            "sphinx",
            "sphinx-automodapi",
        ],
    },
    cmdclass={
        "build_ext": build_ext,
    },
    ext_modules=[
        Extension(
            "toasty._libtoasty",
            ["toasty/_libtoasty.pyx"],
            define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        ),
    ],
    include_dirs=[
        np.get_include(),
    ],
)

for e in setup_args["ext_modules"]:
    e.cython_directives = {"language_level": "3"}

if __name__ == "__main__":
    setup(**setup_args)
