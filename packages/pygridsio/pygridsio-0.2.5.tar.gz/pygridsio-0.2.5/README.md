# pygridsio



## Introduction

This is a python submodule containing IO functionality for reading and writing .asc and .zmap grids.

## Usage

`from pygridsio.pygridsio import *`

To read a grid file into the custom grid class:

`grid = read_grid(filename)`

To read a grid file into an xarray, with dimensions x, y:

`grid = read_grid_to_xarray(filename)`

Or if you want to read multiple grids into an xarray provide a list of filenames, with dimensions x, y, grids:

`grids = read_grids_to_xarray([file1, file2])`

You can optionally provide labels for each grid:

`grids = read_grids_to_xarray([file1, file2], labels=["grid1","grid2"])`

If you have grids with different dimensions you can provide the filename of a template_grid, which will resample the other grids to have the same geometry as the template_grid.

For example:
`grids = read_grids_to_xarray([file1, file2], labels=["grid1","grid2"],template_grid=file1)`
will resample file2 to have the same geometry as file1.

When writing out grids, you can write out grids to a netcdf raster (which can be read easily by xarray, or QGIS or ArcGIS):

`write_to_netcdf_raster(grid, Filename)`
Where `grid` can be a instance of the custom Grid class, an xr.DataArray or an xr.Dataset.

This will write out a netcdf raster with the projection information set to RD new as default.
If you want to write out the raster without any projection information:
`write_to_netcdf_raster(Grid, Filename,RDnew_projection=False)`



## Installation to Develop the code further

### Anaconda
#### Create/update anaconda environment
The file `environment.yml` can be used to create a working development python environment with the needed packages.
For this open an `Anaconda Prompt` and:

`conda env create -f environment.yml`

Or to update the existing anaconda environment (with an updated version of the`environment.yml`file :

`conda env update -n pygridsio -f environment.yml`

#### Export (updated) anaconda environment
The `environment.yml` file needs to be updated when new packages are added:

`conda env export --from-history -n pygridsio > environment.yml`

#### Use anaconda environment in PyCharm
To connect the anaconda environment to Pycharm you can go to `File` , `Settings`, `Project`, `Python Interpreter`, `add interpreter`, `add local interpreter`, `conda environment` and then select the environment you created using the above steps.

### Poetry
Poetry is becoming the new way to manage your python projects and dependencies. Install poetry here: https://python-poetry.org/docs/ 
(note: if you can't run poetry from your terminal, ensure that the poetry.exe is in your environment variables).

Then after cloning this repo to your local machine, run:
`poetry install`

Which will install a virtual environment in the gitlab repo. This can also be done using the Pycharm Python Interpreter interface.

### Verify Installation
You can verify the installation of the different python packages by running the tests stored in `tests`. 
In pycharm: Right click on the folder marked `tests` and click on `Run python tests in test`

## publishing the project to ci.tno.nl/gitlab
To publish an updated version of the project to the pygridsio package registry I recommend using poetry.

First configure the connection between poetry and the gitlab package registry:
`poetry config repositories.gitlab_pygridsio https://ci.tno.nl/gitlab/api/v4/projects/17422/packages/pypi`

Add your own personal access token details (https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html):
`poetry publish --repository gitlab_pygridsio -u"token name" -p "token value"`

Then you can build and publish the project as a new deployment in the package registry:
`poetry build`
`poetry publish`
(make sure the version number you publish is unique)

## How to import pygridsio into other python projects

### Pip

The basic 0.0.1 version of the code is on the public PyPi repository:
`pip install pygridsio`

### From TNO Gitlab
However, the most up to date versions are found in the TNO gitlab repo (https://ci.tno.nl/gitlab), to add this to your project you need to make a personal access token with API access:
(see: https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

and then to pull the latest verion into your projects you can use:
`pip install pygridsio --index-url https://__token__:<your_personal_token>@ci.tno.nl/gitlab/api/v4/projects/17422/packages/pypi/simple`

Ensuring to replace the <your_personal_token> with the token you created in gitlab.

