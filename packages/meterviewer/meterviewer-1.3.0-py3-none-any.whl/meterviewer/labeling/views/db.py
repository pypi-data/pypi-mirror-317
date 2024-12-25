import pathlib
from meterviewer.models import func
import typing as t


def from_db() -> t.Generator[t.Tuple[pathlib.Path, pathlib.Path, str], None, None]:
  dbpath = "alldata.db"
  items = func.get_carry_items(dbpath)
  items = list(items)
  for item in items:
    yield (
      pathlib.Path(item.filename),
      pathlib.Path(item.filename).parent,
      str(id),
    )
