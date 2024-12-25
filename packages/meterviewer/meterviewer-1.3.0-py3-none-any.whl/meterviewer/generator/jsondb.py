"""create jsondb for meter-viewer"""

import glob
import json
import pathlib
import random
import typing as t

import toml

from meterviewer.datasets.read.detection import read_image_area

from .schema import Item, MeterDB


# cache config function (only read disk once), returns get_random_dataset and load_conf
def load_config(config_path: pathlib.Path) -> t.Callable[[], dict]:
  data: t.Optional[dict] = None

  def load_conf() -> dict:
    nonlocal data
    if data is None:
      with open(config_path, "r") as f:
        data = toml.load(f)
    assert data is not None, (config_path, data)
    return data

  return load_conf


get_local_config = None


# 随机选择一个数据集
def get_random_dataset(is_train: bool = True) -> str:
  dataset_list = get_all_dataset(is_train)
  return random.choice(dataset_list)


# 获取数据集列表
def get_all_dataset(is_train: bool = True) -> list[str]:
  config = get_local_config()
  if is_train:
    key = "train_dataset"
  else:
    key = "test_dataset"
  return config["base"][key]


def get_base_dir() -> str:
  """获取数据集的 base_dir"""
  config = get_local_config()
  return config["base"]["root_path"]


def get_mid_path(is_test: bool = False) -> str:
  """获取数据集的 mid_path"""
  if is_test:
    return "lens_6/CS/all_CS"
  else:
    return "lens_6/XL/XL"


def get_random_data(is_test: bool = False) -> pathlib.Path:
  """随机获取一个数据集下的图片"""
  dataset = get_random_dataset(is_train=not is_test)
  base_dir = get_base_dir()
  mid_path = get_mid_path(is_test=is_test)

  data_path = glob.glob(str(pathlib.Path(base_dir) / mid_path / dataset / "*.jpg"))
  return random.choice(data_path)


def set_local_config(infile: pathlib.Path):
  """设置本地配置"""
  global get_local_config
  get_local_config = load_config(config_path=infile)


def gen_db(infile: pathlib.Path, output: pathlib.Path, is_test: bool = False):
  """读取数据集下所有的图片，以及点的位置，生成一个json文件"""

  # set the get_local_config
  set_local_config(infile)

  data = []
  mid_path = get_mid_path(is_test)

  for dataset in get_all_dataset(is_train=not is_test):
    base_dir = get_base_dir()
    data_path = glob.glob(str(pathlib.Path(base_dir) / mid_path / dataset / "*.jpg"))
    for jpg_data in data_path:
      rect = read_image_area(pathlib.Path(jpg_data))
      item = Item(
        filepath=jpg_data,
        dataset=dataset,
        xmin=rect["xmin"],
        xmax=rect["xmax"],
        ymin=rect["ymin"],
        ymax=rect["ymax"],
      )
      data.append(item)

  meter_db = MeterDB(data=data)

  with open(output, "w") as f:
    json.dump(meter_db.model_dump(), f)

  return output
