from pathlib import Path as P
from meterviewer.generator import db


def main(root_path: P):
    p = P("./alldata.db")
    db.generate_db_for_all(root_path, p)
