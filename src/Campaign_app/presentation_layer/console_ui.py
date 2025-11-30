"""Implements the applicatin user interface."""

from campaign_app.application_base import ApplicationBase
from campaign_app.service_layer.app_services import AppServices
from campaign_app.infrastructure_layer.Campaign import Campaign
from prettytable import PrettyTable
import sys

class ConsoleUI(ApplicationBase):
    """UserInterface Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
        self.app_services = AppServices(config)
    
    
    # Public Methods
    def display_menu(self) ->None:
        """Display the menu"""
        print(f"\n\n\t\tCampaign Channel Application Menu")
        print()
        print(f"\t1. List Campaigns")
        print(f"\t2. List Channel")
        print(f"\t3. Add Campaign")
        print(f"\t4. Record Campaign")
        print(f"\t5. Add Channel")
        print(f"\t6. Exit")
        print()
    

    def process_menu_choice(self)->None:
        """Proccess choices of menu"""
        menu_choice = input("\tMenu Choice: ")

        match menu_choice[0]:
            case '1': self.list_campaigns()
            case '2': self.list_channel()
            case '3': self.add_channel()
            case '4': self.record_campaign()
            case '5': self.add_channel()
            case '6': sys.exit()
            case _: print(f"Invalid Menu Choice {menu_choice[0]}")

    def list_campaigns(self)->None:
        """Lists campaigns"""
        campaigns = self.app_services.get_all_campaigns()
        campaign_table = PrettyTable()
        campaign_table.field_names =['id','Campaign Name','Start Date','End Date',
                                     'Company','Campaign Category','Budget','Revenue',]
        channel_table = PrettyTable()
        channel_table.field_names = ['Channel_Name']
        channel_table.align = 'l'
        for campaign in campaigns:
            for channel in campaign.channel:
                channel_table.add_row([channel.ChannelName])
            campaign_table.add_row([campaign.idCampaign, campaign.Campaign_Name,
                                    campaign.StartDate, campaign.EndDate,
                                    campaign.idCompany, campaign.idCampaign_Category,
                                    campaign.Budget, campaign.Revenue, campaign.NetProfit,
                                    channel_table.get_string()])
            campaign_table.add_divider()
            channel_table.clear_rows()
        print(campaign_table)


    def list_channel(self)->None:
        """Lists channel"""
        print("list_channel() method stub called....")
    

    def add_campaign(self)->None:
        """add campaign"""
        print("add_campaign() method stub called....")
    
    def record_campaign(self)->None:
        """record campaign"""
        print("record_campaign() method stub called....")
    
    def add_channel(self)->None:
        """Add channel"""
        print("add_channel() method stub called....")

    def start(self) ->None:
        while True:
            self.display_menu()
            self.process_menu_choice()