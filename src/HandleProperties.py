from jproperties import Properties
from configobj import ConfigObj

class HandleProperties :

    def read_properties(self, property_file_path) :
        configuration = Properties()
        with open(property_file_path, 'rb') as config_file:
            configuration.load(config_file)
        return configuration

    def write_properties(self, property_file_path, key, value) :
        config = ConfigObj(property_file_path, encoding='utf8')
        config[key] = str(value)
        config.write()