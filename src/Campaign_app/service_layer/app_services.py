"""Implements AppServices Class."""

from campaign_app.application_base import ApplicationBase
from campaign_app.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from campaign_app.infrastructure_layer.campaign import Campaign
from campaign_app.infrastructure_layer.channel import Channel
from campaign_app.infrastructure_layer.channel_category import Channel_Category
from campaign_app.infrastructure_layer.company import Company
from campaign_app.infrastructure_layer.campaign_category import Campaign_Category
import inspect
from typing import List, Dict

class AppServices(ApplicationBase):
    """AppServices Class Definition."""
    def __init__(self, config:dict)->None:
        """Initializes object. """
        self._config_dict = config
        self.META = config["meta"]
        super().__init__(subclass_name=self.__class__.__name__,
                         logfile_prefix_name=self.META["log_prefix"])
        self.DB = MySQLPersistenceWrapper(config)
        


    def get_all_campaigns(self) ->List[Campaign]:
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        campaign_dict = {}
        campaign_dict['campaign'] =[]

        try:
            results = self.DB.select_all_campaigns()
            return results
        
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')

    def get_all_channels(self) ->List[Channel]:
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        channel_dict = {}
        channel_dict['channel'] =[]
        try:
            results = self.DB.select_all_channels()
            return results
        
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')
        
    def get_all_channel_category(self) ->List[Channel_Category]:
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        channel_category_dict = {}
        channel_category_dict['channel_cat'] =[]
        try:
            results = self.DB.select_all_channel_categories()
            return results
        
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')
    
    def get_all_campaign_category(self) ->List[Campaign_Category]:
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        campaign_category_dict = {}
        campaign_category_dict['campaign_cat'] =[]
        try:
            results = self.DB.select_all_campaign_categories()
            return results
        
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')
    
    def get_all_companies(self) ->List[Company]:
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        company_dict = {}
        company_dict['company'] =[]
        try:
            results = self.DB.select_all_companies() 
            return results
        
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')

    def create_campaign(self, campaign:Campaign)->Campaign:
        """Creates a  new campaign in the database"""
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        try:
            results = self.DB.create_campaign(campaign)
            return results
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')
    
    def update_campaign(self, campaign:Campaign)->Campaign:
        """Creates a  new campaign in the database"""
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        try:
            results = self.DB.update_campaign(campaign)
            return results
        except Exception as e:
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:{e}')
    
    def delete_campaign(self, idcampaign:int):
        """Delete a campaign"""
        self._logger.log_debug(f'In {inspect.currentframe().f_code.co_name}()...')
        try:
            return self.DB.delete_campaign(idcampaign)
        except Exception as e:
            self._logger.log_error(f"delete_campaign: {e}")
    
    def create_channel(self, channel: Channel) -> Channel:
        """Create Channel"""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            return self.DB.create_channel(channel)
        except Exception as e:
            self._logger.log_error(f"create_channel: {e}")
    
    def create_campaign_category(self, category: Campaign_Category) -> Campaign_Category:
        """Create Campaign Category"""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            return self.DB.create_campaign_category(category)
        except Exception as e:
            self._logger.log_error(f"create_campaign_category: {e}")

    
    def create_channel_category(self, category: Channel_Category) -> Channel_Category:
        """Create Channel Category"""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            return self.DB.create_channel_category(category)
        except Exception as e:
            self._logger.log_error(f"create_channel_category: {e}")
    
    def create_company(self, company: Company) -> Company:
        """Create Company"""
        self._logger.log_debug(f"In {inspect.currentframe().f_code.co_name}()...")
        try:
            return self.DB.create_company(company)
        except Exception as e:
            self._logger.log_error(f"create_company: {e}")



        