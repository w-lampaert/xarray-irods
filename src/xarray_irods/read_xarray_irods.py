import os
import xarray as xr
from irods.session import iRODSSession

def create_irods_session():
    '''
    Create an irods session. You will have to set up
    authentication first though (check out the mango 
    'How to connect' info)

    Returns
    -------
    session:
        an irods session

    '''
    try:

        env_file = os.environ['IRODS_ENVIRONMENT_FILE']

    except KeyError:

        env_file = os.path.expanduser('~/.irods/irods_environment.json')

    session = iRODSSession(irods_env_file=env_file)
    return session


def read_xarray(file_name, session='', read_irods=False,
                engine='scipy', read_method='load'):

    '''
    Read xarray files with xr.open_dataset. Will first create an iRODS
    object of the file if you are trying to read directly from iRODS

    Parameters
    ----------

    file_name: str
        full path to your file. Be sure to provide a '/vsc-climate'
        path if you want to use iRODS
    session: 
        an existing iRODS session. Use the create_irods_session
        function. Empty string by default.
    read_irods: bool
        declare if you want to read from iRODS or from a path on the
        cluster.
    engine: str
        One of the allowed engine types for xr.open_dataset. Currently
        only h5netcdf and scipy have been tested
    read_method: str
        'load' or 'open'. With 'open' you use the xr.open_dataset() function
        while 'load' will also explitly load the dataset (with
        xr.open_dataset().load())

    Returns
    -------

    xarray dataset object
    '''

    if read_irods:
        with session:
            irods_obj = session.data_objects.get(file_name)
            irods_file = irods_obj.open('r')

            if read_method == 'open':
                ds = xr.open_dataset(irods_file, engine=engine)
            else:
                ds = xr.open_dataset(irods_file, engine=engine).load()
            
            irods_file.close()
            return ds
    else:
         return xr.open_dataset(file_name, engine=engine)

