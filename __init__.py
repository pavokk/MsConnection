from importlib import metadata
from .MsConnection import Client
from .session import TokenSession
from .functions import *

ms_connection_metadata = metadata.metadata(__package__)

__author__ = ms_connection_metadata["Paul Volden"]
__email__ = ms_connection_metadata["paul@mystore.no"]
__version__ = ms_connection_metadata["0.1"]
