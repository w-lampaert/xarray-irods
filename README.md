# Xarray iRODS functions

## About

This repository contains some functions that can allow you to read (netCDF) files directly from iRODS, meaning that you
do not need to download them to cluster first. You should of course expect some sort of slowdown compared to reading the 
files directly from cluster-coupled storage.

## Installation

**NOTE:** **It is recommended to NOT use the package installation method for now!** This repository is a first step in providing VSC users with more practical tools on top of the python iRODS client. As no definite decision has been made as to what extent our teams will maintain such codestacks, this repository might move or become out of date. For this reason it might be better to include the functions in `src/xarray_irods` in your own Python scripts instead of installing this package. Any information on dependencies can be found in the `setup.py` file.

If you would like to install this repository as a package, you can do so by:

```bash
git clone https://github.com/w-lampaert/xarray-irods.git
cd xarray-irods
pip install .
```

## How to use

Currently, there are only two functions in `src/xarray_irods/read_xarray_irods.py`:

- create_irods_session: this sets up an irods session to your zone. You will have to authenticate first however. Follow the instructions on https://mango.vscentrum.be/user/openid/choose_zone, 'How to connect'
- read_xarray: this function allows you to read (netCDF) files directly from iRODS. It requires the following arguments:
    - file_name: path to your file. Can be both a mounted path or a path to your iRODS object
    - session: an iRODS session if you want to read from iRODS. By default it is an empty string (in case you want to read from a mounted storage)
    - read_irods: Boolean. Set to True if you want to read from iRODS. False will require a mounted path.
    - engine: the engine you want to use to read your files with. Currently, tests have only conducted with `scipy` and `h5netcdf` (see the 'Remarks' section below).
    - read_method: the method to read your data. Options are 'load' or 'open'. 'load' will load your full file into memory (using `xr.open_dataset().load()`, while open will try to make use      of the lazy loading methods of xarray, by just using `xr.open_dataset()`.

## Remarks

### Closing xarray dataset

Depending on the engine (mainly `h5netcdf`, see the next paragraph), iRODS can have issues when you do not close your xarray dataset. The `read_xarray` function returns
a xarray dataset object, which requires you to close it explicitly later on (with `ds.close()`).

### h5netcdf engine

When having multiple xarray objects with `h5netcdf` open at the same time, the iRODS rate limiter on our VSC clusters will block any further connections, and your script
will eventually fail. This means that you only should use this engine together with the `open` read method if you have a workflow where you can close the xarray object
before opening the next one.

While this has not been tested in a parallel read setup, it can be expected that this will work the same. Work-arounds might be possible, but currently this
still needs to be investigated. If you need to read multiple files at the same time, it is recommended to use the `load` read method. Due to the lack of the lazy loading
functionalities, this tends to be slower than its `open` alternative.

### Further optimizations

While it has not been tested yet, cache settings in xarray and compression of netCDF files could still improve read speeds. 
 
