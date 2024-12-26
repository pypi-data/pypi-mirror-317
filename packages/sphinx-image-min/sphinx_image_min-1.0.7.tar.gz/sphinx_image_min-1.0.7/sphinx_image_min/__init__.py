# sphinx_image_min/__init__.py
from sphinx.application import Sphinx
from .sphinx_image_min import SphinxImageMin, optimize_images
import importlib.metadata

# Dynamically fetch the version from pyproject.toml
try:
    __version__ = importlib.metadata.version("sphinx_image_min")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"


# ENTRY POINT >>
def setup(app: Sphinx):
    # Configuration values for the extension from that project's conf.py
    print(f"[sphinx_image_min::setup] Extension loaded with version: {__version__}")
    app.add_config_value("img_optimization_enabled", True, "env", [bool])
    app.add_config_value("img_optimization_max_width", 1920, "env", [int])

    # Register the directive, even if it doesn't do anything specific right now
    app.add_directive("optimize-images", SphinxImageMin)

    # Connect the optimization function to the build-finished event
    app.connect("build-finished", optimize_images)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
