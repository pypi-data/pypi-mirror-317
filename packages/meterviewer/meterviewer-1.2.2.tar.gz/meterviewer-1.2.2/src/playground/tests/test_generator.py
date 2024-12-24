from meterviewer.img import process
from PIL import Image


def test_gen_pics():
    im = process.gen_empty_im((30, 120, 3))
    im = Image.fromarray(im)
    filename = "/tmp/test.png"
    im.save(filename)
    process.show_img(im, is_stop=False)
