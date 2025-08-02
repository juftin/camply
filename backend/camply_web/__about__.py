"""
camply-web metadata
"""

try:
    from importlib_metadata import version as metadata_version
except ImportError:
    from importlib.metadata import version as metadata_version

__application__ = "camply-web"
__author__ = "justin.flannery@juftin.com"
__version__ = metadata_version(__application__)
