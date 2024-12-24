import h5py
import pathlib


def test_h5py():
    path = pathlib.Path("/home/svtter/Work/Dataset/MeterData/generated_merged")
    f = h5py.File(path / "generated.hdf5", "r")
    content = []
    for name, value in f.items():
        content.append(name)
