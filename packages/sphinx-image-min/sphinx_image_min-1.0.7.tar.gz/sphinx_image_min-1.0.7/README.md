# Sphinx Extension: Image Minimizer

<!-- Badges go here on the same line; PyPi doesn't support `\` or single-multi-line (it'll stack vertically) -->
[![PyPI](https://img.shields.io/pypi/v/sphinx-image-min)](https://pypi.org/project/sphinx-image-min/) [![PyPI - License](https://img.shields.io/pypi/l/sphinx-image-min)](https://opensource.org/licenses/MIT)

## Description

This Sphinx extension allows for automatically minimizing build dir images, most useful when only used for CI.

## Setup

1. Add the following to your `conf.py`:

    ```python
    import sys, os
    
    # Sphinx Minimizer [Optional] Options
    image_min_max_width = 1080  # Default
    ```

## Usage

After a build is complete, images in `build/_images/` will be compressed (lossless, if png). 

## Requirements

- Python>=3.6
- Sphinx>=1.8
- pillow>=10.4.0

This may work with older versions, but has not been tested.

## Entry Point

See `setup(app)` definition at `sphinx_image_min.py`.

## Tested in

- Windows 11 via PowerShell 7
- Ubuntu 22.04 via ReadTheDocs (RTD) CI

## Notes

- `__init__.py` is required for both external pathing and to treat the directory as a pkg
