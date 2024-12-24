import typing as t
from meterviewer import files
from meterviewer.datasets import dataset
import pathlib
from .types import viewReturn


def from_filesystem(root_path: pathlib.Path) -> viewReturn:
  for dataset_name in dataset.get_dataset_list(root_path):
    img_p = files.scan_pics(dataset.get_dataset_path(root_path, str(dataset_name)))
    img_p = list(img_p)
    for p in img_p:
      yield p, dataset_name, "invalid"


def view_dataset(root_path: pathlib.Path) -> viewReturn:
  def get_images(dataset_path: pathlib.Path):
    # lookup 3 images.
    pics = list(files.scan_pics(dataset_path))[:1]
    return pics

  datasets = dataset.get_dataset_list(root_path)
  for dataset_name in datasets:
    res = dataset.get_dataset_path(root_path, str(dataset_name))
    pics = get_images(res)
    for pic in pics:
      yield pic, dataset_name, "_"
