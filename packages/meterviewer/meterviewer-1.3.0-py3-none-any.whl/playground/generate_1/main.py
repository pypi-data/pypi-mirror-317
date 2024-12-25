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

# 设置控制台输出的日志级别为 WARNING
logger.remove()  # 移除默认的控制台输出
logger.add(sys.stdout, level="INFO")


getList = t.Literal["dataset", "path", "length", "total_nums"]


def load_config(config_path: pathlib.Path) -> t.Callable[[getList], t.Any]:
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
    """随机选择一个数据集"""
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


def generate_dataset(config_path: pathlib.Path):
  root_path = get_root_path()
  get_f = load_config(config_path=config_path)

  def read_rand_img(digit: int | str) -> T.NpImage:
    return single.read_rand_img(
      digit=digit,
      root=root_path,
      get_dataset=get_f("dataset"),
      promise=True,
    )

  def gen_block(digit: T.DigitStr) -> T.NpImage:
    return dataset.generate_block_img(digit, dataset.join_with_resize, read_rand_img)

  generated_path = root_path / pathlib.Path(get_f("path")())
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
    length=get_f("length")(),
    nums=get_f("total_nums")(),
    gen_block_img=gen_block,
  )
  filesave(imgs, labels)


def main():
  config_list = [
    "dataset-gen.toml",
    "dataset-gen-2.toml",
    "dataset-gen-3.toml",
    "dataset-gen-4.toml",
    "dataset-gen-5.toml",
  ]
  parent = pathlib.Path(__file__).parent
  for config in config_list:
    logger.info(f"generating dataset with {config}...")
    generate_dataset(parent / config)
