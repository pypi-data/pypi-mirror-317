
import os
import configparser
from .model_sersic3d import ModelSersic
DiskModel = DefaultModel = ModelSersic

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GalPaK: Utils')

#Python3 compatibility
try:
  basestring
except NameError:
  basestring = str

def _save_to_file(filename, contents, clobber):
    if not clobber and os.path.isfile(filename):
        raise IOError("The file {} already exists. Specify overwrite=True to overwrite it.".format(filename))
    with open(filename, 'w') as f:
        f.write(contents)

#def _read_file(filename):
#    with open(filename, 'r') as f:
#        contents = f.read()
#    return contents


def _read_model(file_config):
    """
    sets model from config MODEL
    :return:
    """

    model = None
    if file_config is not None:
        if os.path.isfile(file_config):
            logger.info("Reading model {:s}".format(file_config))
            config = configparser.RawConfigParser()
            config.read(file_config)
        else:
            raise ValueError("Model Config file %s not present" % (file_config))
    else:
        raise ValueError("Model Config file not defined")

    if config.has_section('MODEL'):
        config = config['MODEL']
    else:
        logger.warning("CONFIG file has no MODEL section")

    if 'type' in list(config.keys()):
        model_type = config['type'].lower()
    else:
        logger.error("CONFIG: Model: type not specified")


    args={}
    #try:
    #    redshift = float(config['redshift'])
    #except:
    #    redshift = None

    #args['redshift']=redshift

    if  'default' in model_type:
        model = DefaultModel
    elif 'sersic' in model_type:
        model = ModelSersic
        if 'rotation_curve' in config.keys():
            args['rotation_curve']=config['rotation_curve']
    elif 'disk' in model_type:
        model = DiskModel
    else:
        raise ValueError("Model type invalid. Must be DefaultModel or ModelSersic or DiskModel")

    #args parameters
    import inspect
    var_args = inspect.getfullargspec(model).args
    for k in var_args[1:]:
        if k.lower() in list(config.keys()):
            try:
                args[k]=eval(config[k])
            except:
                args[k]=config[k]


    return model(**args)
