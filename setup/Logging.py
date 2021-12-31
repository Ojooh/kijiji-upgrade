import pathlib
import logging
import os
from datetime import datetime

class Logging :

    def get_logger(self, log_file_name) :
        return self.create_Logging_Environment(log_file_name)
        

    def basic_logging_configuration (self) :
        logging.basicConfig(filename=self.log_file_name, filemode='a', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logger = logging.getLogger('dev')
        logger.setLevel(logging.DEBUG)
        return logger

    def create_Logging_Environment(self, log_file_name) :
        logging_script_path = pathlib.Path(__file__).parent.absolute()

        """ Changing Directory To Create Logs Folder If It Does Not Exist """

        # Changing Directory To Main Project Directory
        
        try :
            os.chdir(logging_script_path)
            os.chdir("../")

            # Fetching Project Directory Path and Appending Logs to that Path
            project_directory_path = pathlib.Path().absolute()
            logs_directory_path = str(project_directory_path) + "/Logs/"

            # Creating Logs Folder If it does not exists
            if not os.path.exists(logs_directory_path) :
                os.makedirs(logs_directory_path)
                
            self.log_file_name = datetime.now().strftime(str(logs_directory_path) + str(log_file_name) + '_%d_%m_%Y_%H_%M_%S' + '.log')
            return self.basic_logging_configuration()

        except OSError :
            print("Logging Module : Unable to create Logs Directory : Process Exiting")
            return None
        