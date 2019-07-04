__version__ = '0.1dev0'

try:
    from .fields import CompositePrimaryKey  # noqa: F401
except ImportError:
    pass
