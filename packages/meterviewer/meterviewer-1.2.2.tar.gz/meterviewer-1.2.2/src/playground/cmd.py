import sys
import pathlib
import importlib
import toml

common_config = {
    'loglevel': 'INFO'
}

def load_env():
    parent = pathlib.Path("./playground")
    c = parent / "dataset.toml"
    content = c.read_text()
    data = toml.loads(content)
    base_config = data.get('base', None)
    common_config['loglevel'] = base_config.get('loglevel', 'INFO')


def main():
    load_env()
    mode = sys.argv[1]
    module = importlib.import_module(mode)
    module.main()


if __name__ in ("__main__"):
    main()
