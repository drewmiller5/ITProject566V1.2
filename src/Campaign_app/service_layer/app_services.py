"""Implements AppServices Class."""

from campaign_app.application_base import ApplicationBase
from campaign_app.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect

class AppServices(ApplicationBase):
    """AppServices Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')


    def get_all_campaigns(self):
        try:
            return self.DB.select_all_campaigns()
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')
