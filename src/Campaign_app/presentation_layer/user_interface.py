"""Implements the applicatin user interface."""
from campaign_app.application_base import ApplicationBase
from campaign_app.service_layer.app_services import AppServices
import sys

class UserInterface(ApplicationBase):
    """UserInterface Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.app_services = AppServices(config)
    def display_menu(self) ->None:
        """Display the menu"""
        print(f"\t\tCampaign Channel Application Menu")
        print()
        print(f"\t1. List Campaigns")
        print(f"\t2. List Channel")
        print(f"\t3. Add Campaign")
        print(f"\t4 Record Campaign")
        print(f"\t5. Add Channel")
        print(f"t\6. Exit")
        print()




    def start(self) ->None:
        self.display_menu()