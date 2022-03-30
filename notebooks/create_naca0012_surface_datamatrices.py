"""Create data matrices based on NACA0012 surface pressure coefficients.
"""

from pathlib import Path
import torch as pt
from flowtorch.data import CSVDataloader, mask_box


# create output folder
outpath = "./output/naca0012_data/"
Path(outpath).mkdir(parents=True, exist_ok=True)

# paths to raw data
raw_data = "/media/andre/Elements/naca0012_shock_buffet/run/"
surface_data = "/postProcessing/surface/"
raw_data_z25 = raw_data + "rhoCF_set1_alpha4_saiddes_ref0_z25" + surface_data
raw_data_r1_z25 = raw_data + "rhoCF_set1_alpha4_saiddes_ref1_z25" + surface_data
raw_data_z50 = raw_data + "rhoCF_set1_alpha4_saiddes_ref0_z50" + surface_data

# create data matrices
def convert_and_save_data(loader: CSVDataloader, path: str, extension: str=".pt"):
    times = loader.write_times
    dm = loader.load_snapshot("f", times)
    pt.save(pt.tensor([float(t) for t in times]), path + "times" + extension)
    pt.save(loader.vertices, path + "vertices" + extension)
    pt.save(dm, path + "data_matrix" + extension)

loader = CSVDataloader.from_foam_surface(raw_data_z25, "total(p)_coeff_airfoil.raw")
convert_and_save_data(loader, outpath, "_z25.pt")
loader = CSVDataloader.from_foam_surface(raw_data_r1_z25, "total(p)_coeff_airfoil.raw")
convert_and_save_data(loader, outpath, "_r1_z25.pt")
loader = CSVDataloader.from_foam_surface(raw_data_z50, "total(p)_coeff_airfoil.raw")
convert_and_save_data(loader, outpath, "_z50.pt")
