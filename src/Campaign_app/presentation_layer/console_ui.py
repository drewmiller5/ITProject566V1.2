"""Implements the application user interface."""

from campaign_app.application_base import ApplicationBase
from campaign_app.service_layer.app_services import AppServices
from campaign_app.infrastructure_layer.campaign import Campaign
from campaign_app.infrastructure_layer.campaign_category import Campaign_Category
from campaign_app.infrastructure_layer.channel import Channel
from campaign_app.infrastructure_layer.channel_category import Channel_Category
from campaign_app.infrastructure_layer.company import Company
from prettytable import PrettyTable
from prettytable.colortable import ColorTable, Themes
from datetime import datetime
import sys
import inspect


class ConsoleUI(ApplicationBase):
    """ConsoleUI Class Definition."""
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
        print(f"\t2. Add Campaign")
        print(f"\t3. Update Campaign")
        print(f"\t4. Drop Campaign")
        print(f"\t5. List Channel")
        print(f"\t6. Add Channel")
        print(f"\t7. List Campaign Category")
        print(f"\t8. Add Campaign Category")
        print(f"\t9. List Channel Category")
        print(f"\t10. Add Channel Category")
        print(f"\t11. List Company")
        print(f"\t12. List Company")
        print(f"\t13. Exit")
        print()
    

    def process_menu_choice(self)->None:
        """Proccess choices of menu"""
        menu_choice = input("\tMenu Choice: ")

        match menu_choice.strip():
            case '1': self.list_campaigns()
            case '2': self.add_campaign() 
            case '3': self.update_campaign()
            case '4': self.drop_campaign()
            case '5': self.list_channels()
            case '6': self.add_channel()
            case '7': self.list_campaign_category()
            case '8': self.add_campaign_category()
            case '9': self.list_channel_category()
            case '10': self.add_channel_category()
            case '11': self.list_company()
            case '12': self.add_company()
            case '13': sys.exit()
            case _: print(f"Invalid Menu Choice {menu_choice}")
    
    def list_campaigns(self)->None:
        """Lists campaigns"""
        campaigns = self.app_services.get_all_campaigns()
        campaign_table = ColorTable(theme=Themes.EARTH)
        campaign_table.field_names =['id','Campaign Name','Start Date','End Date',
                                     'Company','Campaign Category','Budget','Revenue', 'Net Profit', 'Channels']
        channel_table = ColorTable(theme=Themes.EARTH)
        channel_table.field_names = ['Channel Name']
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

        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: ' \
                                f'{campaigns}')


    def list_channels(self)->None: 
        """Lists channels with their category"""
        
        channels = self.app_services.get_all_channels()
        channel_table = ColorTable(theme=Themes.EARTH)
        channel_table.field_names =['id','Channel Name', 'Category'] 
            # Removed Channel Category Id because wouldn't make sense
        category_table = ColorTable(theme=Themes.EARTH)
        category_table.field_names = ['Category Name']
        category_table.align = 'l'
        for channel in channels:
            for channel_category in channel.CategoryName:
                category_table.add_row([channel_category.Channel_CategoryName])
            
            channel_table.add_row([channel.idChannel, channel.ChannelName, 
                                   category_table.get_string()])
            channel_table.add_divider()
            category_table.clear_rows()
        print(channel_table)

        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: ' \
                                f'{channels}')
    

    def list_channel_category(self)->None:
        """lists all channel categories"""

        categories = self.app_services.get_all_channel_category()
        category_table = ColorTable(theme=Themes.EARTH)
        category_table.field_names = ['idChannel_Category', 'Category Name']
        category_table.align = 'l'
        for category in categories:
            category_table.add_row([category.idChannel_Category, category.Channel_CategoryName])
        print(category_table)
        
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: {categories}')

    def list_campaign_category(self)->None:
        """lists all channel categories"""

        campaign_category = self.app_services.get_all_campaign_category()
        campaign_category_table = ColorTable(theme=Themes.EARTH)
        campaign_category_table.field_names = ['idCampaign_Category', 'Campaign Name']
        campaign_category_table.align = 'l'
        for campaign in campaign_category:
            campaign_category_table.add_row([campaign.idCampaign_Category, campaign.Campaign_CategoryName])
        print(campaign_category_table)
        
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: {campaign_category_table}')

    def list_company(self)->None:
        """list companies"""

        companies = self.app_services.get_all_companies()
        company_table = ColorTable(theme=Themes.EARTH)
        company_table.field_names = ['CompanyId', 'Company Name']
        company_table.align = 'l'
        for company in companies:
            company_table.add_row([company.idCompany,company.CompanyName])
        print(company_table)
        
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: {company_table}')
        

    def add_campaign(self)->None:
        """add campaign"""
        print("add_campaign() method stub called....")
    
    def update_campaign(self)->None:
        """update campaign"""
        print("update_campaign() method stub called....")
    
    def drop_campaign(self)->None:
        """drop campaign"""
        print("drop_campaign() method stub called....")
    
    def add_channel(self)->None:
        """Add channel"""
        print("add_channel() method stub called....")
    
    def add_campaign_category(self)->None:
        """add campaign category"""
        print("add campaign category() method stub called....")
    
    def add_channel_category(self)->None:
        """add channel category"""
        print("add channel category() method stub called....")
    
    def add_company(self)->None:
        """add company"""
        print("add company() method stub called....")



    def start(self) ->None:
        while True:
            self.display_menu()
            self.process_menu_choice()