import pathlib

from meterviewer.generator.jsondb import get_random_data


def test_get_random_data(set_config):
  data = get_random_data()
  assert pathlib.Path(data).exists()
