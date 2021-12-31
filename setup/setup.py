""" This is the Starting Point of Kijiji Web Scraping Script Environment Setup """

import sys, os
from datetime import datetime
from Logging import Logging
from SetupEnvironment import SetupEnvironment

""" Getting Basic Logging Options """

logger = Logging().get_logger("setup")
if logger != None :

    # Checking Python Version
    python_major_version = sys.version_info.major

    if python_major_version <3:
        logger.critical("Setup Module : Version Issue : Please install Python Version 3 or greater to execute this script")
    else:
        logger.debug("Setup Module : Correct Python Version Found")
        logger.debug("Setup Module : Preparing Script Environment")
        logger.debug("Setup Module : installing virtualenv first")
        # virtualenv_install_stream = os.popen('pip install virtualenv')
        # logger.debug(virtualemv_install_stream.read())

        # virtualenv_run_stream = os.popen('virtualenv venv')
        # logger.debug(virtualenv_run_stream.read())

        #Staring Environment Setup
        setupEnvironment = SetupEnvironment(logger)
        setupEnvironment.installAndUnpgradeLibraries()

        logger.debug("Setup Module : Environment Setup Completed")
else :
    print("Setup Module : Critical : Logging Setup Could Not Be Completed")
    print("Setup Module : Critical : Process will Exit")
    print("Setup Module : Critical : Contact Administrator For Resolution")
    sys.exit()