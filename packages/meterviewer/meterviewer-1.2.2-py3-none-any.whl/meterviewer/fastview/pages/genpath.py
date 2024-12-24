# generate dataset path.
import os
import pathlib
from meterviewer.config import get_root_path
import streamlit as st


def main():
  p = get_root_path()
  p = pathlib.Path(st.text_input("root path:", value=p))

  st.text("choose your dataset")
  st.text(os.listdir(p))
  dataset_name = st.text_input("dataset name")
  ds_path = p / dataset_name
  st.button("finish")
  st.text(ds_path)


main()
