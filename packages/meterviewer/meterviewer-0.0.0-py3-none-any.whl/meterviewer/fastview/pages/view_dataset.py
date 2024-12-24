# quick view of a dataset

import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from meterviewer.config import get_root_path
from meterviewer.datasets import imgv
from meterviewer.img import draw, cut
import pathlib


def main():
  st.title("Quick Viewer of Meter dataset")
  data_path = pathlib.Path("/home/xiuhao/work/Dataset/MeterData/lens_5/XL/DATA")

  dataset_len_ = st.number_input("Dataset length", value=6)
  dataset_name = st.text_input("Dataset name", value="M4L1XL")
  filename = st.text_input("Enter the filename", value="2018-11-23-12-16-01.jpg")

  img_path = data_path / dataset_name / filename
  im, v, rect = imgv.view_one_img_v(img_path)

  st.text(f"image shape: {im.shape}")
  st.image(im, caption=f"filename: {filename}")

  st.text("with rect")
  rect_im = draw.draw_rectangle(im, rect)
  st.image(rect_im, caption=f"with rect: {filename}")

  cutted = cut.cut_img(im, rect)
  st.image(cutted, caption=f"cutted: {filename}")


main()
