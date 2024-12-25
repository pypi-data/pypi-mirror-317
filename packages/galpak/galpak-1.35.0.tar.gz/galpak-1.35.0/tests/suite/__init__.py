import sys
from unittest.mock import MagicMock

from galpak.spread_functions import PointSpreadFunction

# Mock the maoppy module
maoppy = MagicMock()
maoppy.__version__ = 'mock_version'
sys.modules['maoppy'] = maoppy
sys.modules['maoppy.utils'] = MagicMock()
sys.modules['maoppy.psfmodel'] = MagicMock()
maoppy.psfmodel.Psfao = MagicMock()
maoppy.psfmodel.Psfao.__class__ = PointSpreadFunction
sys.modules['maoppy.psffit'] = MagicMock()
sys.modules['maoppy.instrument'] = MagicMock()


