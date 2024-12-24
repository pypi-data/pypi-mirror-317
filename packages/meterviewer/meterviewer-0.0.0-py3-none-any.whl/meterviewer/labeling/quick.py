from nicegui import ui
from pathlib import Path


def img_view_app(path: Path):
  ui.markdown("# Quick show of images")
  ui.image(path)
  ui.run()
