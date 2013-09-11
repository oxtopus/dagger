""" Dagger package.  Attributes imported or defined here are available
when dagger package is imported, establishing the "Dagger API"
"""

from .core import (
  getcwdbranch,
  getrevisions,
  workingdir
)
from .config import (
  Config
)

__all__ = ['']