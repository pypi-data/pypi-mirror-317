from meterviewer.generator.jsondb import get_all_dataset


def test_get_all_dataset(set_config):
  assert len(get_all_dataset()) > 0
