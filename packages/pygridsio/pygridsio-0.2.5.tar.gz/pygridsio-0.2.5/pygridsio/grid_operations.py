import copy

import numpy as np
import xarray as xr
from pygridsio.grid import Grid


def remove_padding_from_grid(grids : Grid | xr.DataArray | xr.Dataset) -> Grid | xr.DataArray | xr.Dataset:
    if type(grids) == Grid:
        return remove_padding_from_custom_grid(grids)
    elif type(grids) == xr.DataArray:
        return remove_padding_from_xarray(grids)
    elif type(grids) == xr.Dataset:
        print("Not yet implemented for xr.Datasets")

def remove_padding_from_custom_grid(grid: Grid) -> Grid:
    first_col, last_col, first_row, last_row = return_first_and_last_non_nan_rows_and_columns(grid.z)

    newNx = last_col - first_col + 1
    newNy = last_row - first_row + 1
    newGridx = grid.gridx[first_col:last_col+1]
    newGridy = grid.gridy[first_row:last_row+1]
    newValues = grid.z[first_row:last_row+1,first_col:last_col+1]

    # create a new grid object:
    new_grid = copy.deepcopy(grid)
    new_grid.gridx = newGridx
    new_grid.gridy = newGridy
    new_grid.nx = newNx
    new_grid.ny = newNy
    new_grid.z = newValues

    return new_grid

def remove_padding_from_xarray(grid: xr.DataArray) ->  xr.DataArray:
    if "grid" in grid.dims:
        outermost_dimensions=[]
        for i in range(len(grid.grid)):
            first_col, last_col, first_row, last_row = return_first_and_last_non_nan_rows_and_columns(grid.isel(grid=i).data)
            outermost_dimensions.append([first_col, last_col, first_row, last_row])
        outermost_dimensions = np.array(outermost_dimensions)
        first_col = np.min(outermost_dimensions[:,0])
        last_col = np.max(outermost_dimensions[:, 1])
        first_row = np.min(outermost_dimensions[:, 2])
        last_row = np.max(outermost_dimensions[:, 3])
        newGridx = grid.x.data[first_col:last_col + 1]
        newGridy = grid.y.data[first_row:last_row + 1]
        newValues = grid.data[first_row:last_row + 1, first_col:last_col + 1,:]
        return xr.DataArray(newValues, coords=[("y", newGridy), ("x", newGridx), ("grid",grid.grid.data)], dims=["y", "x","grid"])
    else:
        first_col, last_col, first_row, last_row = return_first_and_last_non_nan_rows_and_columns(grid.data)
        newGridx = grid.x.data[first_col:last_col+1]
        newGridy = grid.y.data[first_row:last_row+1]
        newValues = grid.data[first_row:last_row+1,first_col:last_col+1]
        return xr.DataArray(newValues, coords=[("y", newGridy), ("x", newGridx)], dims=["y", "x"])

def return_first_and_last_non_nan_rows_and_columns(grid_values:np.array ):
    nx = grid_values.shape[1]
    ny = grid_values.shape[0]

    first_col=0
    for i in range(nx):
        if np.any(~np.isnan(grid_values[:,i])):
            first_col = i
            break

    last_col=nx-1
    for i in range(nx-1,0,-1):
        if np.any(~np.isnan(grid_values[:,i])):
            last_col = i
            break

    first_row=0
    for j in range(ny):
        if np.any(~np.isnan(grid_values[j,:])):
            first_row = j
            break

    last_row=ny-1
    for j in range(ny-1,0,-1):
        if np.any(~np.isnan(grid_values[j,:])):
            last_row = j
            break

    return first_col,last_col,first_row,last_row
