"""Defines the MySQLPersistenceWrapper class."""

from campaign_app.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import (MySQLConnectionPool)
import json
import inspect
from typing import List
from campaign_app.infrastructure_layer.campaign_category import Campaign_Category
from campaign_app.infrastructure_layer.campaign import Campaign
from campaign_app.infrastructure_layer.channel_category import Channel_Category
from campaign_app.infrastructure_layer.channel import Channel
from campaign_app.infrastructure_layer.company import Company
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
		

		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = self.DATABASE["connection"]["config"]["database"]
		self.DB_CONFIG['user'] = self.DATABASE["connection"]["config"]["user"]
		self.DB_CONFIG['host'] = self.DATABASE["connection"]["config"]["host"]
		self.DB_CONFIG['port'] = self.DATABASE["connection"]["config"]["port"]

		self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}')

		# Database Connection
		self._connection_pool = self._initialize_database_connection_pool(self.DB_CONFIG)
		
		# Campaign Columns ENUMS
		self.CampaignColumns = Enum('CampaignColumns', [('idCampaign',0),('Campaign_Name', 1),
												  ('StartDate', 2),('EndDate', 3),('idCompany', 4),
												  ('idCampaign_Category', 5),('Budget', 6),('Revenue', 7),
												  ('NetProfit', 8)])
		
		# Channel Columns ENUMS
		self.ChannelColumns = Enum('ChannelColumns',
							 [('idChannel', 0),('ChannelName', 1),('idChannel_Category', 2)])
		
		# Company Columns ENUMS
		self.CompanyColumns = Enum('CompanyColumns',
							 [('idCompany', 0),('CompanyName', 1)])
		
		# Campaign Category ENUMS
		self.CampaignCategoryColumns = Enum('CampaignCategoryColumns',
							 [('idCampaign_Category', 0),('Campaign_CategoryName', 1)])

		# Channel Category ENUMS
		self.ChannelCategoryColumns = Enum('ChannelCategoryColumns',
							 [('idChannel_Category', 0),('Channel_CategoryName', 1)])

		# SQL Query Constants Lists Campaigns
		self.SELECT_ALL_CAMPAIGNS = \
			f"SELECT idCampaign, Campaign_Name, StartDate, EndDate, idCompany, idCampaign_Category, Budget, Revenue, NetProfit " \
			f"FROM Campaign"
		
		self.SELECT_CHANNELS_FOR_CAMPAIGN_ID = \
			f"SELECT c.idChannel, c.ChannelName, c.idChannel_Category " \
			f"FROM Channel c, Campaign_channel_xref cx " \
			f"WHERE (cx.idCampaign = %s) AND (c.idChannel = cx.idChannel)"
		
		# SQL Query Constants Lists Channels
		self.SELECT_ALL_CHANNELS = \
			f"SELECT idChannel, ChannelName " \
			f"FROM Channel"
		
		self.SELECT_CAMPAIGN_CATEGORY_FOR_CHANNEL_ID = \
			f"SELECT c.idChannel, c.ChannelName, cc.Channel_CategoryName " \
			f"FROM Channel c  " \
			f"JOIN Channel_Category cc on c.idChannel_Category = cc.idChannel_Category"
		
		self.INSERT_CAMPAIGN = \
		f"INSERT INTO Campaign " \
		f"(idCampaign, Campaign_Name, StartDate, EndDate, idCompany, idCampaign_Category, Budget, Revenue) " \
		f"VALUES(%s, %s, %s, %s, %s, %s, %s)"

	# Lists all campaigns 
	def select_all_campaigns(self)->List[Campaign]:
		"Returns a list of all campaigns"
		cursor = None
		results = None
		campaign_list = []
		try:
			self._logger.log_debug("Entering campaigns")
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_CAMPAIGNS)
					results = cursor.fetchall()
					campaign_list = self._populate_campaign_objects(results)

			for campaign in campaign_list:
				channel_list = \
					self.select_all_channels_for_campaign_id(campaign.idCampaign)
				self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: \
						   {campaign_list}')
				campaign.channel = self._populate_channel_objects(channel_list)
			
			self._logger.log_debug("Returns campaign list")
			return campaign_list
		
		except Exception as e:
			self._logger.log_error(f'Problem with select_all_campaigns(): {e}')

	def select_all_channels_for_campaign_id(self, idCampaign:int) \
		->List[Channel]:
		"""Returns a list of all chanels for campaingn id."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_CHANNELS_FOR_CAMPAIGN_ID,
					([idCampaign]))
					results = cursor.fetchall()
			
			return results
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
	
	# Lists all Channels 
	def select_all_channels(self)->List[Channel]:
		"Returns a list of all channels"
		cursor = None
		results = None
		channel_list = []
		try:
			self._logger.log_debug("Entering channels")
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_ALL_CHANNELS)
					results = cursor.fetchall()
					channel_list = self._populate_campaign_objects(results)
			for channel in channel_list:
				category_list = \
				self.select_all_channe()
				self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: \
						   {campaign_list}')
				campaign.channel = self._populate_channel_objects(channel_list)
			
			self._logger.log_debug("Returns campaign list")
			return campaign_list
		
		except Exception as e:
			self._logger.log_error(f'Problem with select_all_campaigns(): {e}')
		
	
	def select_all_categories_for_channel_id(self, idChannel_Category:int) \
		->List[Campaign_Category]:
		"""Returns a list of all chanels for campaingn id."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.SELECT_CAMPAIGN_CATEGORY_FOR_CHANNEL_ID,
					([idChannel_Category]))
					results = cursor.fetchall()
			
			return results
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
	
	def create_campaign(self, campaign:Campaign)->Campaign:
		"""Create a new record in the campaign table"""
		cursor = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.INSERT_CAMPAIGN, 
						([campaign.Campaign_Name, campaign.StartDate, campaign.EndDate, 
		campaign.idCompany, campaign.idCampaign_Category, campaign.Budget, campaign.Revenue]))
					connection.commit()
					self._logger.log_debug(f'Updated {cursor.rowcount} row.')
					self._logger.log_debug(f'Last Row ID: {cursor.lastrowid}.')
					campaign.idCampaign, = cursor.lastrowid

			return campaign

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
						use_pure=self.DATABASE["pool"]["use_pure"],
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
				campaign.idCampaign = row[self.CampaignColumns['idCampaign'].value]
				campaign.Campaign_Name = row[self.CampaignColumns['Campaign_Name'].value]
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
	
	def _populate_company_objects(self, results:List) ->List[Company]:
		"""Populate and returns a list of channel objects"""
		company_list = []
		try:
			for row in results:
				company = Company()
				company.idCompany = row[self.CompanyColumns['idCompany'].value]
				company.CompanyName = row[self.CompanyColumns['CompanyName'].value]
				company_list.append(company)
			
			return company_list
		
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

	def _populate_channel_category_objects(self, results:List) ->List[Channel_Category]:
		"""Populate and returns a list of channel objects"""
		channel_category_list = []
		try:
			for row in results:
				channel_category = Channel_Category()
				channel_category.idChannel_Category = row[self.ChannelCategoryColumns['idChannel_Category'].value]
				channel_category.Channel_CategoryName = row[self.ChannelCategoryColumns['Channel_CategoryName'].value]
				channel_category_list.append(channel_category)
			
			return channel_category_list
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
	
	def _populate_campaign_category_objects(self, results:List) ->List[Campaign_Category]:
		"""Populate and returns a list of channel objects"""
		campaign_category_list = []
		try:
			for row in results:
				campaign_category = Campaign_Category()
				campaign_category.idCampaign_Category = row[self.CampaignCategoryColumns['idCampaign_Category'].value]
				campaign_category.Campaign_CategoryName = row[self.CampaignCategoryColumns['Campaign_CategoryName'].value]
				campaign_category_list.append(campaign_category)
			
			return campaign_category_list
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')