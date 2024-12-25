import pathlib

from meterviewer.generator.jsondb import gen_db

if __name__ == "__main__":
  for is_test in [True, False]:
    name = "test" if is_test else "train"
    gen_db(
      infile=pathlib.Path(__file__).parent / "config.toml",
      output=pathlib.Path(__file__).parent / f"meterdb_{name}.json",
      is_test=is_test,
    )
