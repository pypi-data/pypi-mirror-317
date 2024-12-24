from __future__ import annotations

import functools
import pathlib
import random
import sys
import typing as t

import toml
from loguru import logger

from meterviewer import T, files
from meterviewer.config import get_root_path
from meterviewer.datasets import dataset
from meterviewer.datasets.read import single
from meterviewer.img import process

getList = t.Literal["dataset", "path", "length", "total_nums"]


class DatasetGenerator(object):
  """class format definition of dataset generator"""

  def __init__(self, config_path: pathlib.Path) -> None:
    self.root_path = get_root_path()
    self.config_path = config_path
    self.get_f = self.load_config(config_path=self.config_path)

  def load_config(self, config_path: pathlib.Path) -> t.Callable[[getList], t.Any]:
    data: t.Optional[dict] = None
    dataset_list: t.List[str] = []

    def load_conf() -> dict:
      nonlocal data
      if data is None:
        with open(config_path, "r") as f:
          data = toml.load(f)
      assert data is not None, (config_path, data)
      return data

    def get_dataset() -> str:
      nonlocal dataset_list
      dataset_list = get_config("dataset")
      return random.choice(dataset_list)

    def get_config(name: str):
      c = load_conf().get("generate_config", None)
      if c is None:
        raise Exception('config "generate_config" not found')
      return c.get(name)

    pt = functools.partial
    get_path = pt(get_config, name="path")
    get_length = pt(get_config, name="length")
    get_total_nums = pt(get_config, name="total_nums")

    def get_func(name: getList) -> t.Callable:
      func_map: t.Mapping[str, t.Callable] = {
        "dataset": get_dataset,
        "path": get_path,
        "length": get_length,
        "total_nums": get_total_nums,
      }
      return func_map[name]

    return get_func

  def read_rand_img(self, digit: int | str) -> T.NpImage:
    return single.read_rand_img(
      digit=digit,
      root=self.root_path,
      get_dataset=self.get_f("dataset"),
      promise=True,
    )

  def gen_block(self, digit: T.DigitStr) -> T.NpImage:
    return dataset.generate_block_img(
      digit, dataset.join_with_resize, self.read_rand_img
    )

  def main(self):
    generated_path = self.root_path / pathlib.Path(self.get_f("path")())
    generated_path.mkdir(exist_ok=True)

    filesave = functools.partial(
      files.save_img_labels_with_default,
      prefix_name=generated_path,
      save_to_disk=files.save_to_disk,
    )

    def check_imgs(imglist):
      size = imglist[0].shape
      imgs = process.resize_imglist(imglist)
      for im in imgs:
        assert size == im.shape

    create_dataset = dataset.create_dataset_func(check_imgs=lambda x: None, total=9)
    imgs, labels = create_dataset(
      length=self.get_f("length")(),
      nums=self.get_f("total_nums")(),
      gen_block_img=self.gen_block,
    )
    filesave(imgs, labels)
