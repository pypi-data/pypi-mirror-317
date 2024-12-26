# sphinx_feature_flags/__init__.py
from sphinx.application import Sphinx
from .sphinx_feature_flags import (
    SphinxFeatureFlags,
    feature_flag_node,
    visit_feature_flag_node,
    depart_feature_flag_node,
)
import importlib.metadata

# Dynamically fetch the version from pyproject.toml
try:
    __version__ = importlib.metadata.version("sphinx_feature_flags")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

# ENTRY POINT >>
def setup(app: Sphinx):
    print(f"[sphinx_feature_flags::setup] Extension loaded with version: {__version__}")
    
    app.add_config_value("feature_flags", {}, "env", [dict])
    app.add_directive("feature-flag", SphinxFeatureFlags)
    app.add_node(
        feature_flag_node, html=(visit_feature_flag_node, depart_feature_flag_node)
    )

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
