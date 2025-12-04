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
			f"SELECT idCampaign, Campaign_Name, StartDate, EndDate, idCompany, " \
			f"idCampaign_Category, Budget, Revenue, NetProfit " \
			f"FROM Campaign"
		
		self.SELECT_CHANNELS_FOR_CAMPAIGN_ID = \
			f"SELECT c.idChannel, c.ChannelName, c.idChannel_Category " \
			f"FROM Channel c, Campaign_channel_xref cx " \
			f"WHERE (cx.idCampaign = %s) AND (c.idChannel = cx.idChannel)"
		
		# List all channels SQL
		
		self.SELECT_ALL_CHANNELS = \
			f"SELECT idChannel, ChannelName, idChannel_Category " \
			f"FROM Channel"
		
		self.SELECT_CAMPAIGN_CATEGORY_FOR_CHANNEL_ID = \
			f"SELECT c.idChannel, c.ChannelName, c.idChannel_Category, cc.Channel_CategoryName " \
			f"FROM Channel c  " \
			f"JOIN Channel_Category cc on c.idChannel_Category = cc.idChannel_Category " \
			f"WHERE c.idChannel = %s"
		
		# List all Channel Category SQL
		self.SELECT_ALL_CHANNEL_CATEGORY = \
		f"SELECT idChannel_Category, Channel_CategoryName " \
		f"FROM channel_category " \
		f"ORDER by idChannel_Category" # ID Numbers wouldn't go in order correctly 
									   # and this needed to be fixed and is a pattern

		# List all Campaign Category SQL
		self.SELECT_ALL_CAMPAIGN_CATEGORY = \
		f"SELECT idCampaign_Category, Campaign_CategoryName " \
		f"FROM campaign_category " \
		f"ORDER BY idCampaign_Category" # Pattern from line 90

		# List all Companies
		self.SELECT_ALL_COMPANY = \
		f"SELECT idCompany, CompanyName " \
		f"FROM company " \
		f"ORDER BY idCompany" # Same problem as line 90
		
		# Insert Campaign
		self.INSERT_CAMPAIGN = \
		f"INSERT INTO Campaign " \
		f"(Campaign_Name, StartDate, EndDate, idCompany, idCampaign_Category, Budget, Revenue) " \
		f"VALUES(%s, %s, %s, %s, %s, %s, %s)"

		# Update campaign SQL
		self.UPDATE_CAMPAIGN = \
		f"UPDATE Campaign " \
		f"SET Campaign_Name = %s, StartDate = %s, EndDate = %s, idCompany = %s, " \
		f"idCampaign_Category = %s, Budget = %s, Revenue = %s " \
		f"WHERE idCampaign = %s"

		# Delete campaign SQL
		self.DELETE_CAMPAIGN = \
		f"DELETE FROM Campaign " \
		f"WHERE idCampaign = %s"

		# Insert Channel
		self.INSERT_CHANNEL = \
		f"INSERT INTO Channel (ChannelName, idChannel_Category) " \
		f"VALUES (%s, %s)"
		
		# Insert Campaign Category
		self.INSERT_CAMPAIGN_CATEGORY = \
		f"INSERT INTO Campaign_Category (Campaign_CategoryName) " \
		f"VALUES (%s)"
		
		# Insert Channel Category
		self.INSERT_CHANNEL_CATEGORY = \
		f"INSERT INTO Channel_Category (Channel_CategoryName) " \
		f"VALUES (%s)"

		# Insert Companies
		self.INSERT_COMPANY = \
		f"INSERT INTO Company (CompanyName) " \
		f"VALUES (%s)"


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
					self._logger.log_debug(f"Channel {results}")
					channel_list = self._populate_channel_objects(results)
				for channel in channel_list:
					category_list = \
						self.select_all_categories_for_channel_id(channel.idChannel) # Foreign Key connector
					self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}: \
								{category_list}')
					channel.CategoryName = self._populate_channel_category_objects(category_list)
			
			self._logger.log_debug("Returns channel list")
			return channel_list
		
		except Exception as e:
			self._logger.log_error(f'Problem with select_all_channels(): {e}')
		
	
	def select_all_categories_for_channel_id(self, idChannel_Category:int) \
		->List[Campaign_Category]:
		"""Returns a list of all chanels for campaingn id."""
		cursor = None
		results = None
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor(dictionary = True)
				with cursor:
					cursor.execute(self.SELECT_CAMPAIGN_CATEGORY_FOR_CHANNEL_ID,
					([idChannel_Category]))
					results = cursor.fetchall()
			
			return results
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	# Select all Channel Categories
	def select_all_channel_categories(self)->List[Channel_Category]:
		"Returns a list of all channels"
		cursor = None
		results = None
		channel_category_list = []
		try:
			self._logger.log_debug("Entering channel categories")
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor(dictionary = True)
				with cursor:
					cursor.execute(self.SELECT_ALL_CHANNEL_CATEGORY)
					results = cursor.fetchall()
					self._logger.log_debug(f"Channel {results}")
					channel_category_list = self._populate_channel_category_objects(results)
			return channel_category_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	# Select all Campaign Categories 
	def select_all_campaign_categories(self)->List[Campaign_Category]:
		"Returns a list of all channels"
		cursor = None
		results = None
		campaign_category_list = []
		try:
			self._logger.log_debug("Entering channel categories")
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor(dictionary = True)
				with cursor:
					cursor.execute(self.SELECT_ALL_CAMPAIGN_CATEGORY)
					results = cursor.fetchall()
					self._logger.log_debug(f"Campaign {results}")
					campaign_category_list = self._populate_campaign_category_objects(results)
			return campaign_category_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
		
	# Select all companies
	def select_all_companies(self)->List[Company]:
		"Returns a list of all channels"
		cursor = None
		results = None
		company_list = []
		try:
			self._logger.log_debug("Entering channel categories")
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor(dictionary = True)
				with cursor:
					cursor.execute(self.SELECT_ALL_COMPANY)
					results = cursor.fetchall()
					self._logger.log_debug(f"Company {results}")
					company_list = self._populate_company_objects(results)
			return company_list
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
	
	# Create campaign
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
						campaign.idCompany, campaign.idCampaign_Category, campaign.Budget, 
						campaign.Revenue]))
					connection.commit()
					self._logger.log_debug(f'Updated {cursor.rowcount} row.')
					self._logger.log_debug(f'Last Row ID: {cursor.lastrowid}.')
					campaign.idCampaign = cursor.lastrowid

			return campaign

		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
		
	def update_campaign(self, campaign: Campaign) -> Campaign:
		"""Update an existing campaign in the database."""
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.UPDATE_CAMPAIGN, (
						campaign.Campaign_Name,
						campaign.StartDate,
						campaign.EndDate,
						campaign.idCompany,
						campaign.idCampaign_Category,
						campaign.Budget,
						campaign.Revenue,
						campaign.idCampaign
					))
				connection.commit()
				self._logger.log_debug(f"Updated {cursor.rowcount} campaign(s) with id {campaign.idCampaign}")
			return campaign
		except Exception as e:
			self._logger.log_error(f"{inspect.currentframe().f_code.co_name}: {e}")
	
	

	def delete_campaign(self, idcampaign: int):
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.DELETE_CAMPAIGN, (idcampaign,))
				connection.commit()
			return cursor.rowcount > 0
		except Exception as e:
			self._logger.log_error(f"delete_campaign: {e}")
		
	def create_channel(self, channel: Channel) -> Channel:
		"""Add a new channel if it doesn't already exist"""
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(self.INSERT_CHANNEL, ([channel.ChannelName,channel.idChannel_Category]))
				connection.commit()
				channel.idChannel = cursor.lastrowid
				self._logger.log_debug(f'Updated {cursor.rowcount} row.')
				self._logger.log_debug(f'Last Row ID: {cursor.lastrowid}.')
			return channel
		except Exception as e:
			self._logger.log_error(f"create_channel: {e}")
	
	def create_campaign_category(self, category: Campaign_Category) -> Campaign_Category:
		"""Create a new campaign category record"""
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(
						self.INSERT_CAMPAIGN_CATEGORY, 
						(category.Campaign_CategoryName,)
					)
					connection.commit()
					category.idCampaign_Category = cursor.lastrowid
			return category
		except Exception as e:
			self._logger.log_error(f"create_campaign_category: {e}")

	
	def create_channel_category(self, category: Channel_Category) -> Channel_Category:
		"""Create a new channel category record"""
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(
						self.INSERT_CHANNEL_CATEGORY, 
						(category.Channel_CategoryName,)
					)
					connection.commit()
					category.idChannel_Category = cursor.lastrowid
			return category
		except Exception as e:
			self._logger.log_error(f"create_channel_category: {e}")
		
	def create_company(self, company: Company) -> Company:
		"""Create a new company record"""
		try:
			connection = self._connection_pool.get_connection()
			with connection:
				cursor = connection.cursor()
				with cursor:
					cursor.execute(
						self.INSERT_COMPANY, 
						(company.CompanyName,)
					)
					connection.commit()
					company.idCompany = cursor.lastrowid
			return company
		except Exception as e:
			self._logger.log_error(f"create_company: {e}")
	

			
	

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
				company.idCompany = row['idCompany']
				company.CompanyName = row['CompanyName']
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
				channel.CategoryName = []
				channel_list.append(channel)
			
			return channel_list
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')

	def _populate_channel_category_objects(self, results:List[dict]) ->List[Channel_Category]:
		"""Populate and returns a list of channel objects"""
		channel_category_list = []
		try:
			for row in results:
				channel_category = Channel_Category()
				channel_category.idChannel_Category = row['idChannel_Category']
				channel_category.Channel_CategoryName = row['Channel_CategoryName']
				channel_category_list.append(channel_category)
			
			return channel_category_list
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')
	
	def _populate_campaign_category_objects(self, results:List) ->List[Campaign_Category]:
		"""Populate and returns a list of campaign objects"""
		campaign_category_list = []
		try:
			for row in results:
				campaign_category = Campaign_Category()
				campaign_category.idCampaign_Category = row['idCampaign_Category']
				campaign_category.Campaign_CategoryName = row['Campaign_CategoryName']
				campaign_category_list.append(campaign_category)
			
			return campaign_category_list
		
		except Exception as e:
			self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')