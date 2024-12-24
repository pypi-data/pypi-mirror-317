# import cv2
from meterviewer import types as T


def cut_img(img: T.NpImage, rect: T.Rect) -> T.NpImage:
  def to_int(rect: T.Rect):
    return (
      int(rect["xmin"]),
      int(rect["ymin"]),
      int(rect["xmax"]),
      int(rect["ymax"]),
    )

  def get_cut_region(rect: T.Rect):
    x_min, y_min, x_max, y_max = to_int(rect)
    x, y, w, h = x_min, y_min, x_max - x_min, y_max - y_min
    return x, y, w, h

  x_min, y_min, x_max, y_max = to_int(rect)
  cropped_image = img[y_min:y_max, x_min:x_max]
  return cropped_image
