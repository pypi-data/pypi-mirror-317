from pathlib import Path

import numpy as np
import xarray as xr

from pygridsio.grid import Grid


def read_grid(filename: str | Path) -> Grid:
    """providing the filename of a grid (in either .asc or .zmap) read in the grid and return a grid object
    Parameters
    ----------
    filename

    Returns
    -------
        A custom Grid object
    """
    return Grid(str(filename))


def grids_to_xarray(grids: list[Grid], labels, grid_template: Grid = None):
    # resample grids if template provided
    if grid_template is not None:
        [grid.gridresample(grid2use=grid_template) for grid in grids]

    # assign values to the data array:
    yarray = grids[0].gridy
    xarray = grids[0].gridx
    data = np.zeros(shape=(len(yarray), len(xarray), len(grids)))
    for i, grid in enumerate(grids):
        if not np.array_equal(grid.gridy, yarray) or not np.array_equal(grid.gridx, xarray):
            raise ValueError(
                f"Grids do not have the same x- and y- coordinates."
                f"You can provide a 'grid_template' as a keyword argument to this function resample all grids to the same shape as the template grid.")
        data[:, :, i] = grid.z

    model = xr.DataArray(data, coords=[("y", yarray), ("x", xarray), ("grid", labels)], dims=["y", "x", "grid"])
    model.attrs["coord system"] = grids[0].coord_sys
    return model


def grid_to_xarray(grid):
    grid_dataarray = xr.DataArray(grid.z, coords=[("y", grid.gridy), ("x", grid.gridx)], dims=["y", "x"])
    grid_dataarray.attrs["coord system"] = grid.coord_sys
    return grid_dataarray


def grids_to_xarray_dataset(grids: list[Grid], labels: list[str] = None, grid_template: Grid = None) -> xr.Dataset:
    """providing a list of filenames of multiple grids (in either .asc or .zmap) read in each grid and return
    a xarray object with dimensions:
    -x, y, grid
    -All grids must have the same dimensions.
    -Optionally: provide a list of labels, to name each grid under the xarray "grid" dimension.

    Parameters
    ----------
    grid_template
    filenames
    labels

    Returns
    -------

    """
    # If grid_template provided, resample grids to have the same geometry as grid_template
    if grid_template is not None:
        [grid.gridresample(grid2use=grid_template) for grid in grids]

    # convert first grid to a dataset
    grid_dataarray = grid_to_xarray(grids[0])
    grid_dataset = grid_dataarray.to_dataset(name=labels[0])

    # add each grid as a datarray to the dataset
    for i in range(1, len(grids)):
        grid_dataarray = grid_to_xarray(grids[i])
        try:
            xr.testing.assert_equal(grid_dataarray.coords, grid_dataset.coords)
        except:
            raise ValueError(
                f"Grids do not have the same x- and y- coordinates."
                f"You can provide a 'grid_template' as a keyword argument to this function resample all grids to the same shape as the template grid.")

        grid_dataset[labels[i]] = grid_dataarray

    grid_dataarray.attrs["coord system"] = grids[0].coord_sys
    return grid_dataset
