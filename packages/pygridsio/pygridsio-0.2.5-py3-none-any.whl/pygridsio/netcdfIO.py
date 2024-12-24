import numpy as np
from pygridsio.grid import Grid
from pathlib import Path
from netCDF4 import Dataset
import xarray as xr


def write_grid_to_netcdf_raster(grid: Grid, filename : Path, variable_name : str ="data", RDnew_projection : bool =True):
    # start ncfile setting up the correct dimensions
    ncfile = create_geometry_of_ncfile(grid.gridx, grid.gridy, filename, RDnew_projection)

    # write the data to x, y, data:
    data = ncfile.createVariable(variable_name, float, ('y', 'x'), fill_value=np.nan)
    data[:, :] = grid.z

    ncfile.close()

def write_dataarray_to_netcdf_raster(grids: xr.DataArray, filename: Path, RDnew_projection=True):
    # start ncfile setting up the correct dimensions
    ncfile = create_geometry_of_ncfile(grids.x, grids.y, filename, RDnew_projection)

    # write the data of each grid:
    for grid_name in grids.grid:
        grid_name = str(grid_name.data)
        data = ncfile.createVariable(grid_name, float, ('y', 'x'), fill_value=np.nan)
        data.long_name = grid_name
        if RDnew_projection:
            data.grid_mapping = "oblique_stereographic"
        data[:, :] = grids.sel(grid=grid_name).values

    ncfile.close()

def write_dataset_to_netcdf_raster(grids: xr.Dataset, filename: Path, RDnew_projection=True):
    # start ncfile setting up the correct dimensions
    ncfile = create_geometry_of_ncfile(grids.x, grids.y, filename, RDnew_projection)

    # write the data of each grid:
    for variable in grids:
        data = ncfile.createVariable(variable, float, ('y', 'x'), fill_value=np.nan)
        data.long_name = variable
        if RDnew_projection:
            data.grid_mapping = "oblique_stereographic"
        data[:, :] = grids[variable].values
    ncfile.close()

def read_netcdf_to_custom_grid(filename):
    xr_grid = xr.open_dataset(filename)
    for variable in xr_grid:
        if variable in ["x","y","oblique_stereographic"]: continue
        gridx = xr_grid[variable].x.data
        gridy = xr_grid[variable].y.data
        griddata = xr_grid[variable].data

        grid_temp = Grid(str(variable),"ZMAP",read=False)
        grid_temp.gridx = gridx
        grid_temp.gridy = gridy
        grid_temp.z = griddata
        grid_temp.ory = gridy[0]
        grid_temp.orx = gridx[0]
        grid_temp.dx = gridx[1]-gridx[0]
        grid_temp.dy = gridy[1] - gridy[0]
        return grid_temp

def create_geometry_of_ncfile(x_array : np.array, y_array : np.array, filename: Path, RDnew_projection : bool):
    ncfile = Dataset(filename, mode='w', format='NETCDF4')

    # create dimensions x_dim and y_dim
    ncfile.createDimension('x', len(x_array))  # latitude axis
    ncfile.createDimension('y', len(y_array))  # longitude axis

    # define variables x, y, data and proj_var
    x = ncfile.createVariable('x', float, ('x'))
    x.long_name = "x coordinate of projection"
    x.standard_name = "projection_x_coordinate"
    x.units = "m"

    y = ncfile.createVariable('y', float, ('y'))
    y.long_name = "y coordinate of projection"
    y.standard_name = "projection_y_coordinate"
    y.units = "m"

    if RDnew_projection:
        proj_var = ncfile.createVariable('oblique_stereographic', str, ())
        proj_var.grid_mapping_name = "oblique_stereographic"
        proj_var.longitude_of_central_meridian = 5.38763888888889
        proj_var.false_easting = 155000.0
        proj_var.false_northing = 463000.0
        proj_var.latitude_of_projection_origin = 52.1561605555556
        proj_var.scale_factor_at_central_meridian = 0.9999079
        proj_var.scale_factor_at_projection_origin = 0.9999079
        proj_var.long_name = "CRS definition"
        proj_var.longitude_of_prime_meridian = 0.0
        proj_var.semi_major_axis = 6377397.155
        proj_var.inverse_flattening = 299.1528128
        proj_var.crs_wkt = "PROJCS[\"Amersfoort / RD New\",GEOGCS[\"Amersfoort\",DATUM[\"Amersfoort\",SPHEROID[\"Bessel 1841\",6377397.155,299.1528128]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4289\"]],PROJECTION[\"Oblique_Stereographic\"],PARAMETER[\"latitude_of_origin\",52.1561605555556],PARAMETER[\"central_meridian\",5.38763888888889],PARAMETER[\"scale_factor\",0.9999079],PARAMETER[\"false_easting\",155000],PARAMETER[\"false_northing\",463000],UNIT[\"metre\",1],AXIS[\"Easting\",EAST],AXIS[\"Northing\",NORTH],AUTHORITY[\"EPSG\",\"28992\"]]"
        proj_var.spatial_ref = "PROJCS[\"Amersfoort / RD New\",GEOGCS[\"Amersfoort\",DATUM[\"Amersfoort\",SPHEROID[\"Bessel 1841\",6377397.155,299.1528128]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4289\"]],PROJECTION[\"Oblique_Stereographic\"],PARAMETER[\"latitude_of_origin\",52.1561605555556],PARAMETER[\"central_meridian\",5.38763888888889],PARAMETER[\"scale_factor\",0.9999079],PARAMETER[\"false_easting\",155000],PARAMETER[\"false_northing\",463000],UNIT[\"metre\",1],AXIS[\"Easting\",EAST],AXIS[\"Northing\",NORTH],AUTHORITY[\"EPSG\",\"28992\"]]"
        proj_var.GeoTransform = "2837.0714 1000 0 638593.4412999999 0 -999.9999999999999 "
        proj_var[0] = ""

    # write the data to x, y, data:
    x[:] = x_array
    y[:] = y_array

    return ncfile