import sys
import platform
import os

class SetupEnvironment:

    def __init__(self, logger) :
        self.logger = logger

    def installAndUnpgradeLibraries(self) :
        try :
            # Upgrading Pip Version
            self.logger.debug("Setup Module : Updating pip version to support the Script functionality")
            pip_install_stream = os.popen('python -m pip install --upgrade pip')
            self.logger.debug(pip_install_stream.read())

            # Selenium Installation
            self.logger.debug("Setup Module : Preparing for Selenium Installation")
            selenium_install_stream = os.popen('pip install selenium')
            self.logger.debug(selenium_install_stream.read())

            # Requests Installation
            self.logger.debug("Setup Module : Preparing for Requests Installation")
            requests_install_stream = os.popen('pip install requests')
            self.logger.debug(requests_install_stream.read())

            #tkinter installation
            self.logger.debug("Setup Module : Preparing for Tkinter Installation")
            tkinter_install_stream = os.popen('pip install tk')
            self.logger.debug(tkinter_install_stream.read())
            

            # JProperties Installation
            self.logger.debug("Setup Module : Preparing for JProperties Installation")
            jproperties_install_stream = os.popen('pip install jproperties')
            self.logger.debug(jproperties_install_stream.read())

            # ConfigObj Installation
            self.logger.debug("Setup Module : Preparing for ConfigObj Installation")
            configobj_install_stream = os.popen('pip install configobj')
            self.logger.debug(configobj_install_stream.read())    

            # Oslo Concurrency Installation
            self.logger.debug("Setup Module : Preparing for Oslo Concurrency Installation")
            oslo_install_stream = os.popen('pip install wheel')
            self.logger.debug(oslo_install_stream.read())
            oslo_install_stream = os.popen('pip install oslo.concurrency')
            self.logger.debug(oslo_install_stream.read())

        except Exception :
            self.logger.error("Setup Module : Environment could not be setup due to System Error")
            self.logger.error("Setup Module : Please provide required privileges to run the Script Or Contact System Administrator")
            sys.exit()
