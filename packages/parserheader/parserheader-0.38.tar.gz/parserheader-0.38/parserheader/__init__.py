from .parserheader import *

from . import __version__ as version
if isinstance(version, float):
    __version__ 	= version
else:
    try:
        __version__ 	= version.version
    except:
        __version__		= version

__email__		= "licface@yahoo.com"
__author__		= "licface@yahoo.com"
