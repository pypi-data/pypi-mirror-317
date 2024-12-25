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
from meterviewer.datasets.v2 import dataset

# 设置控制台输出的日志级别为 WARNING
logger.remove()  # 移除默认的控制台输出
logger.add(sys.stdout, level="INFO")


getList = t.Literal["dataset", "path", "length", "total_nums"]


def load_config(config_path: pathlib.Path) -> t.Callable[[getList], t.Any]:
    data: t.Optional[dict] = None

    def load_conf() -> dict:
        nonlocal data
        if data is None:
            with open(config_path, "r") as f:
                data = toml.load(f)
        return data

    def get_config(name: str):
        c = load_conf().get("generate_config", None)
        if c is None:
            raise Exception('Config "generate_config" not found')
        value = c.get(name)
        return value

    def get_dataset_list() -> t.List[str]:
        dataset_list = get_config("dataset")
        if not isinstance(dataset_list, list):
            raise Exception(
                f"'dataset' should be a list, got {type(dataset_list)}: {dataset_list}"
            )
        return dataset_list

    def get_dataset() -> str:
        return random.choice(get_dataset_list())  # 随机选择一个数据集

    func_map = {
        "dataset": get_dataset,  # 随机选择的数据集
        "dataset_list": get_dataset_list,  # 返回完整数据集列表
        "path": functools.partial(get_config, name="path"),
        "length": functools.partial(get_config, name="length"),
        "total_nums": functools.partial(get_config, name="total_nums"),
    }

    def get_func(name: getList) -> t.Callable:
        return func_map[name]

    return get_func


def generate_dataset(config_path: pathlib.Path):
    root_path = get_root_path()
    get_f = load_config(config_path=config_path)
    print(get_f("dataset_list")())

    dataset_list = get_f("dataset_list")()

    # 生成数据集路径
    generated_path = root_path / pathlib.Path(get_f("path")())
    generated_path.mkdir(exist_ok=True)

    available_digits = dataset.scan_available_digits(root_path, dataset_list)

    # 创建生成逻辑
    create_dataset = dataset.create_dataset_func(check_imgs=lambda x: None)

    imgs, labels = create_dataset(
        root=root_path,
        dataset_list=dataset_list,
        available_digits=available_digits,
        nums=get_f("total_nums")(),
        gen_block_img=dataset.generate_block_img,  # 新逻辑
    )

    # 保存图像和标签
    files.save_img_labels_with_default(
        imgs, labels, prefix_name=generated_path, save_to_disk=files.save_to_disk
    )


def main():
    config_list = [
        "dataset-gen copy.toml",
        # "dataset-gen-2.toml",
        # "dataset-gen-3.toml",
        # "dataset-gen-4.toml",
        # "dataset-gen-5.toml",
    ]
    parent = pathlib.Path(__file__).parent
    for config in config_list:
        logger.info(f"generating dataset with {config}...")
        generate_dataset(parent / config)


if __name__ == "__main__":
    main()
