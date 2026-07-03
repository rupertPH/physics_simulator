import configparser
import os

def read_config(path_to_config):

    if not os.path.exists(path_to_config):
        raise FileExistsError(f"Config file not found!")
    
    config = configparser.ConfigParser()
    config.read(path_to_config)

    sections = ['VARIABLES', 'PARAMETERS', 'INITIAL STATE', 'LAGRANGIAN', '2D VISUALIZATION', 'RENDER']
    for section in sections:
        if section not in config:
            raise KeyError(f"No {section} section found in the config file {path_to_config}!")
        
    return config