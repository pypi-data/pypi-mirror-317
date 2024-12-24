"""SILK2 usage python module
"""
__all__ = []

try:
    import pyecharts
except ImportError:
    print('SILK2.Tools.usage requires "pyecharts" package.')
    print('Install it via command:')
    print('    pip3 install pyecharts')
    raise

try:
    import bs4
except ImportError:
    print('SILK2.Tools.usage requires "bs4" package.')
    print('Install it via command:')
    print('    pip3 install bs4')
    raise