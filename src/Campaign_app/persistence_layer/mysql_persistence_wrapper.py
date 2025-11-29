"""Defines the MySQLPersistenceWrapper class."""

from campaign_app.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import inspect
import json
from typing import List
from campaign_app.infrastructure_layer.Campaign import Campaign
from campaign_app.infrastructure_layer.Channel import Channel
from enum import Enum

class MySQLPersistenceWrapper(ApplicationBase):
	"""Implements the MySQLPersistenceWrapper class."""

	def __init__(self, config:dict)->None:
		"""Initializes object. """
		self._config_dict = config
		self.META = config["meta"]
		self.DATABASE = config["database"]
		super().__init__(subclass_name=self.__class__.__name__, 
				   logfile_prefix_name=self.META["log_prefix"])
		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = \
			self.DATABASE["connection"]["config"]["database"]
		self.DB_CONFIG['user'] = self.DATABASE["connection"]["config"]["user"]
		self.DB_CONFIG['host'] = self.DATABASE["connection"]["config"]["host"]
		self.DB_CONFIG['port'] = self.DATABASE["connection"]["config"]["port"]

		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}')

		# Database Connection
		self._connection_pool = \
			self._initialize_database_connection_pool(self.DB_CONFIG)
		
		# Campaign Columns ENUMS
		self.CampaignColumns = \
			Enum('CampaignColumns',[('idCampaign',0),('Campaign_name', 1),('StartDate', 2),('EndDate', 3),
						   ('idCompany', 4),('idCampaign_Category', 5),('Budget', 6),('Revenue', 7),('NetProfit', 8)])
		
		# Channel Columns ENUMS
		self.ChannelColumns = \
			Enum('ChannelColumns',[('idChannel', 0),('ChannelName', 1),('idChannel_Category', 2)])

		# SQL Query Constants
		self.SELECT_ALL_CAMPAIGNS = \
			f"SELECT idCampaign, Campaign_Name, StartDate, EndDate, idCompany, idCampaign_Category, Budget, Revenue, NetProfit " \
			f"FROM Campaign"




	# MySQLPersistenceWrapper Methods
	def select_all_campaigns(self)->List[Campaign]:
		"Returns a list of all campaigns"
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_CAMPAIGNS)
					results = cursor.fetchall()
					campaign_list = self._populate_campaign_objects(results)
			for campaign in campaign_list:
				channel_list = \
					self.select_all_channel_for_camapign_id(Campaign.idCampaign)
				self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: \
						   {campaign_list}')
				campaign.training = self._populate_channel_objects(channel_list)
			
			return campaign_list
		
		except Exception as e:
			self._logger.log_error(f'Problem with select_all_campaigns(): {e}')

	def select_all_Channels_for_Campaign_id(self, idCampaign:int) \
		->List[Channel]:
		"""Returns a list of all chanels for campaing id."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_CHANNEL_FOR_CAMPAIGN_ID,
					([idCampaign]))
					results = cursor.fetchall()
				return results
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')




		##### Private Utility Methods #####

	def _initialize_database_connection_pool(self, config:dict)->MySQLConnectionPool:
		"""Initializes database connection pool."""
		try:
			self._logger.log_debug(f'Creating connection pool...')
			cnx_pool = \
				MySQLConnectionPool(pool_name = self.DATABASE["pool"]["name"],
					pool_size=self.DATABASE["pool"]["size"],
					pool_reset_session=self.DATABASE["pool"]["reset_session"],
					**config)
			self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: Connection pool successfully created!')
			return cnx_pool
		except connector.Error as err:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Problem creating connection pool: {err}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: Check DB cnfg:\n{json.dumps(self.DATABASE)}')
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Problem creating connection pool: {e}')
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}:Check DB conf:\n{json.dumps(self.DATABASE)}')

	def _populate_campaign_objects(self, results:List) -> List[Campaign]:
		""" Populates and returns a list of Campaign Objects. """
		campaign_list = []
		try:
			for row in results:
				campaign = Campaign()
				campaign.id = row[self.CampaignColumns['idCampaign'].value]
				campaign.Campaign_Name = row[self.CampaignColumns['Campaign_name'].value]
				campaign.StartDate = row[self.CampaignColumns['StartDate'].value]
				campaign.EndDate = row[self.CampaignColumns['EndDate'].value]
				campaign.idCompany = row[self.CampaignColumns['idCompany'].value]
				campaign.idCampaign_Category = row[self.CampaignColumns['idCampaign_Category'].value]
				campaign.Budget = row[self.CampaignColumns['Budget'].value]
				campaign.Revenue = row[self.CampaignColumns['Revenue'].value]
				campaign.NetProfit = row[self.CampaignColumns['NetProfit'].value]
				campaign_list.append(campaign)
			
			return campaign_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
	
	def _populate_channel_objects(self, results:List) ->List[Channel]:
		"""Populate and returns a list of channel objects"""
		channel_list = []
		try:
			for row in results:
				channel = Channel()
				channel.idChannel = row[self.ChannelColumns['idChannel'].value]
				channel.ChannelName = row[self.ChannelColumns['ChannelName'].value]
				channel.idChannel_Category = row[self.ChannelColumns['idChannel_Category'].value]
				channel_list.append(channel)
			
			return channel_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')