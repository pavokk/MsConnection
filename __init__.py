from importlib import metadata

ms_connection_metadata = metadata.metadata(__package__)

__author__ = ms_connection_metadata["Author"]
__email__ = ms_connection_metadata["Author-email"]
__version__ = ms_connection_metadata["Version"]

from .MsConnection import MsConnection, Client
