import sys
# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

__name__="matplotlib.pyplot"

sys.path.append("/usr/share/pyshared/matplotlib")
sys.path.append("/usr/lib/pymodules/python2.7")
sys.path.append("/usr/lib/python2.7/dist-packages")

from pyplot import *

sys.path.remove("/usr/share/pyshared/matplotlib")
sys.path.remove("/usr/lib/pymodules/python2.7")
sys.path.remove("/usr/lib/python2.7/dist-packages")
