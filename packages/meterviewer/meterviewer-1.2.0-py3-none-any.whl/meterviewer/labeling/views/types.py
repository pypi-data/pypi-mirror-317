import typing as t
import pathlib
from pathlib import Path

viewReturn = t.Generator[t.Tuple[pathlib.Path, pathlib.Path, str], None, None]

FullPath = Path


def isFullPath(p: FullPath):
  return p.is_absolute()
