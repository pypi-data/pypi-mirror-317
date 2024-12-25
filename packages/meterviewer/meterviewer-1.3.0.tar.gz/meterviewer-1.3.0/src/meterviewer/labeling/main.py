import toml
import pathlib
import typing as t
from nicegui import ui
from nicegui.events import ValueChangeEventArguments, KeyEventArguments
from meterviewer.config import get_root_path
from meterviewer.labeling import views


def get_image_path(
  root_path: pathlib.Path, mode: t.Literal["filesys", "db", "quick_view"]
):
  if mode == "filesys":
    return views.filesystem.from_filesystem(root_path=root_path)
  elif mode == "quick_view":
    return views.filesystem.view_dataset(root_path=root_path)
  elif mode == "db":
    return views.db.from_db()
  else:
    raise ValueError("mode not found.")


def show(event: ValueChangeEventArguments):
  name = type(event.sender).__name__
  ui.notify(f"{name}: {event.value}")


def old_layout():
  ui.button("Button", on_click=lambda: ui.notify("Click"))
  with ui.row():
    ui.checkbox("Checkbox", on_change=show)
    ui.switch("Switch", on_change=show)
  ui.radio(["A", "B", "C"], value="A", on_change=show).props("inline")
  with ui.row():
    ui.input("Text input", on_change=show)
    ui.select(["One", "Two"], value="One", on_change=show)


def main():
  ui.markdown("# Labeling tool for meter image.")

  root_path = get_root_path()

  def handle_key(e: KeyEventArguments):
    if e.key == "Enter":
      if e.action.keyup:
        set_img_value()

  _ = ui.keyboard(handle_key)

  dataset_g = get_image_path(root_path=root_path, mode="quick_view")
  img_path, dataset_name, id = next(dataset_g)
  carry_v = None

  def set_img_value():
    nonlocal carry_v, img_path, id, dataset_name
    if carry_v is None:
      return
    print(f"image_name: {img_path}")
    print(f"value_set: {carry_v}")
    img_path, dataset_name, id = next(dataset_g)
    current_img.source = img_path
    mrk.content = f"dataset: {dataset_name}, count: {id}/20222"
    toggle1.set_value(None)

  # make sure which dataset to use.
  collect_set = set()

  def add_data(value):
    if value == "1" or value == 1:
      collect_set.add(dataset_name)

  def write_data():
    with open("temp.toml", "w") as f:
      toml.dump({"dataset": list(collect_set)}, f)

  def set_value(event: ValueChangeEventArguments):
    nonlocal carry_v
    carry_v = event.value
    add_data(carry_v)
    set_img_value()

  mrk = ui.markdown(f"dataset: {dataset_name}, count: 1/20222")
  with ui.row():
    current_img = ui.image(img_path).classes("w-[540px]")

  with ui.row():
    toggle1 = ui.toggle([0, 1, 2, 3, 4, 5, 6], value=carry_v, on_change=set_value)
    ui.input("Carry digit", on_change=set_value)
  with ui.row():
    ui.button("previous")
    ui.button("confirm", on_click=lambda: set_img_value())
    ui.button("write", on_click=write_data)
  # ui.link("And many more...", "/documentation").classes("mt-8")

  ui.run()


if __name__ in {"__main__", "__mp_main__"}:
  main()
