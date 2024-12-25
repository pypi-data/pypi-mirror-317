from playground.generate_db import create_all


def test_create(root_path):
    # this script is used for only once.
    if (root_path / "alldata.db").exists():
        return
    create_all.main(root_path)
