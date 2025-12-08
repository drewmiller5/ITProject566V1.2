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
from datetime import date
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
        print(f"\t11. List Companies")
        print(f"\t12. Add Company")
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

            # Adding commas to numbers
            budget_fmt = f"{campaign.Budget:,}" if campaign.Budget is not None else ""
            revenue_fmt = f"{campaign.Revenue:,}" if campaign.Revenue is not None else ""
            netprofit_fmt = f"{campaign.NetProfit:,}" if campaign.NetProfit is not None else ""

            for channel in campaign.channel:
                channel_table.add_row([channel.ChannelName])
            
            campaign_table.add_row([campaign.idCampaign,
                                    campaign.Campaign_Name,
                                    campaign.StartDate,
                                    campaign.EndDate,
                                    campaign.idCompany,
                                    campaign.idCampaign_Category,
                                    budget_fmt,
                                    revenue_fmt,
                                    netprofit_fmt,
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
        

    def add_campaign(self) -> None:
        """Adds a new campaign with input validation"""
        try:
            print("\n--- Add New Campaign ---")

            # 1. Campaign Name Validation
            while True:
                name = input("Campaign Name: ").strip()
                existing_campaigns = [c.Campaign_Name.lower() for c in self.app_services.get_all_campaigns()]
                if name.lower() in existing_campaigns:
                    print("Error: Campaign name already exists. Please enter a unique name.")
                else:
                    break

            # 2. Start and End Date Validation
            while True:
                start_date_str = input("Start Date (YYYY-MM-DD or YYYY/MM//DD): ").strip()
                start_date_str = start_date_str.replace("/","-")

                end_date_str = input("Leave blank if ongoing, format (YYYY-MM-DD or YYYY/MM//DD): ").strip()
                if end_date_str == "":
                    end_date = None
                else:
                    end_date_str = end_date_str.replace("/","-")
                    end_date = date.fromisoformat(end_date_str)
                try:
                    start_date = date.fromisoformat(start_date_str)
                    if end_date is not None and end_date < start_date:
                        print("Error: End Date cannot be before Start Date.")
                    else:
                        break
                except ValueError:
                    print("Error: Invalid date format. Use YYYY-MM-DD.")

            # 3. Company ID Validation
            companies = self.app_services.get_all_companies()
            print("Available Companies:")
            for company in companies:
                print(f"{company.idCompany}: {company.CompanyName}")
            company_ids = [c.idCompany for c in companies]
            while True:
                try:
                    company_id = int(input("Company ID: ").strip())
                    if company_id not in company_ids:
                        print("Error: Invalid Company ID. Please choose from the list.")
                    else:
                        break
                except ValueError:
                    print("Error: Enter a valid integer for Company ID.")

            # 4. Campaign Category ID Validation
            categories = self.app_services.get_all_campaign_category()
            print("Available Campaign Categories:")
            for category in categories:
                print(f"{category.idCampaign_Category}: {category.Campaign_CategoryName}")
            category_ids = [c.idCampaign_Category for c in categories]
            while True:
                try:
                    category_id = int(input("Campaign Category ID: ").strip())
                    if category_id not in category_ids:
                        print("Error: Invalid Campaign Category ID. Please choose from the list.")
                    else:
                        break
                except ValueError:
                    print("Error: Enter a valid integer for Campaign Category ID.")

            # Budget & Revenue
            while True:
                try:
                    budget = float(input("Budget: ").strip())
                    revenue = float(input("Revenue: ").strip())
                    break
                except ValueError:
                    print("Error: Enter valid numbers for Budget and Revenue.")

            # Create Campaign object
            new_campaign = Campaign()
            new_campaign.Campaign_Name = name
            new_campaign.StartDate = start_date
            new_campaign.EndDate = end_date
            new_campaign.idCompany = company_id
            new_campaign.idCampaign_Category = category_id
            new_campaign.Budget = budget
            new_campaign.Revenue = revenue

            # Insert into database
            created_campaign = self.app_services.create_campaign(new_campaign)
            print(f"Campaign '{created_campaign.Campaign_Name}' added with ID {created_campaign.idCampaign}")

        except Exception as e:
            print(f"Error adding campaign: {e}")
            self._logger.log_error(f'{inspect.currentframe().f_code.co_name}: {e}')


    def update_campaign(self) -> None:
        """Update a campaign"""
        campaigns = self.app_services.get_all_campaigns()
        ids = [c.idCampaign for c in campaigns]
        
        try:
            id_to_update = int(input("Enter Campaign ID to update: "))
            if id_to_update not in ids:
                print("Invalid Campaign ID")
                return

            # Find the campaign object
            campaign = next(c for c in campaigns if c.idCampaign == id_to_update)

            # Input new values, fallback to current if empty
            campaign.Campaign_Name = input(f"Campaign Name [{campaign.Campaign_Name}]: ") or campaign.Campaign_Name
            start_date_input = input(f"Start Date (YYYY-MM-DD) [{campaign.StartDate}]: ")
            if start_date_input:
                campaign.StartDate = start_date_input
            end_date_input = input(f"End Date (YYYY-MM-DD) [{campaign.EndDate}]: ")
            if end_date_input:
                campaign.EndDate = end_date_input

            # Company ID
            company_input = input(f"Company ID [{campaign.idCompany}]: ")
            if company_input:
                campaign.idCompany = int(company_input)

            # Campaign Category ID
            category_input = input(f"Campaign Category ID [{campaign.idCampaign_Category}]: ")
            if category_input:
                campaign.idCampaign_Category = int(category_input)

            # Budget and Revenue
            budget_input = input(f"Budget [{campaign.Budget}]: ")
            if budget_input:
                campaign.Budget = float(budget_input)
            revenue_input = input(f"Revenue [{campaign.Revenue}]: ")
            if revenue_input:
                campaign.Revenue = float(revenue_input)

            # Call the service to update
            updated_campaign = self.app_services.update_campaign(campaign)
            if updated_campaign:
                print("Campaign updated successfully.")
            else:
                print("Error updating campaign.")
        except Exception as e:
            print(f"Error: {e}")

    
    def drop_campaign(self) -> None:
        """Delete a campaign"""
        campaigns = self.app_services.get_all_campaigns()

        # Show available IDs for safety
        print("\nAvailable Campaigns:")
        for c in campaigns:
            print(f"ID: {c.idCampaign} | Name: {c.Campaign_Name}")

        try:
            id_to_delete = int(input("\nEnter Campaign ID to delete: "))

            # Validate the ID exists
            if not any(c.idCampaign == id_to_delete for c in campaigns):
                print("Invalid Campaign ID.")
                return

            # Confirm deletion
            confirm = input(f"Are you sure you want to delete Campaign ID {id_to_delete}? (y/n): ").lower()
            if confirm != 'y':
                print("Delete canceled.")
                return

            # Call the service
            deleted = self.app_services.delete_campaign(id_to_delete)

            if deleted:
                print("Campaign deleted successfully.")
            else:
                print("Error deleting campaign.")

        except Exception as e:
            print(f"Error: {e}")

    
    def add_channel(self) -> None:
        """Add a new channel with category validation"""
        # Show existing channels
        existing_channels = self.app_services.get_all_channels()
        print("\nExisting Channels:")
        for ch in existing_channels:
            print(f"- {ch.ChannelName}")

        # Input new channel name
        name = input("\nEnter Channel Name: ").strip()
        if not name:
            print("Channel Name cannot be empty.")
            return
        if any(ch.ChannelName.lower() == name.lower() for ch in existing_channels):
            print("Channel name already exists.")
            return

        # Show available categories
        categories = self.app_services.get_all_channel_category()
        print("\nAvailable Channel Categories:")
        for cat in categories:
            print(f"ID: {cat.idChannel_Category} | Name: {cat.Channel_CategoryName}")

        # Input category ID
        try:
            category_id = int(input("\nEnter Channel Category ID: "))
            if not any(cat.idChannel_Category == category_id for cat in categories):
                print("Invalid category ID.")
                return
        except ValueError:
            print("Invalid input. Must be a number.")
            return

        # Create Channel object
        channel = Channel()
        channel.ChannelName = name
        channel.idChannel_Category = category_id

        # Insert
        new_channel = self.app_services.create_channel(channel)
        if new_channel and new_channel.idChannel:
            print(f"Channel '{new_channel.ChannelName}' added successfully with ID {new_channel.idChannel}.")
        else:
            print("Error adding channel.")
    
    def add_campaign_category(self) -> None:
        """Add a new campaign category"""
        existing_categories = self.app_services.get_all_campaign_category()
        print("\nExisting Campaign Categories:")
        for cat in existing_categories:
            print(f"- {cat.Campaign_CategoryName}")

        name = input("\nEnter Campaign Category Name: ").strip()
        if not name:
            print("Category Name cannot be empty.")
            return
        if any(cat.Campaign_CategoryName.lower() == name.lower() for cat in existing_categories):
            print("Category name already exists.")
            return

        category = Campaign_Category()
        category.Campaign_CategoryName = name

        new_category = self.app_services.create_campaign_category(category)
        if new_category and new_category.idCampaign_Category:
            print(f"Campaign Category '{new_category.Campaign_CategoryName}' added successfully with ID {new_category.idCampaign_Category}.")
        else:
            print("Error adding campaign category.")
    
    
    def add_channel_category(self) -> None:
        """Add a new channel category"""
        existing_categories = self.app_services.get_all_channel_category()
        print("\nExisting Channel Categories:")
        for cat in existing_categories:
            print(f"- {cat.Channel_CategoryName}")

        name = input("\nEnter Channel Category Name: ").strip()
        if not name:
            print("Category Name cannot be empty.")
            return
        if any(cat.Channel_CategoryName.lower() == name.lower() for cat in existing_categories):
            print("Category name already exists.")
            return

        category = Channel_Category()
        category.Channel_CategoryName = name

        new_category = self.app_services.create_channel_category(category)
        if new_category and new_category.idChannel_Category:
            print(f"Channel Category '{new_category.Channel_CategoryName}' added successfully with ID {new_category.idChannel_Category}.")
        else:
            print("Error adding channel category.")

    
    def add_company(self) -> None:
        """Add a new company"""
        existing_companies = self.app_services.get_all_companies()
        print("\nExisting Companies:")
        for comp in existing_companies:
            print(f"- {comp.CompanyName}")

        name = input("\nEnter Company Name: ").strip()
        if not name:
            print("Company Name cannot be empty.")
            return
        if any(comp.CompanyName.lower() == name.lower() for comp in existing_companies):
            print("Company name already exists.")
            return

        company = Company()
        company.CompanyName = name

        new_company = self.app_services.create_company(company)
        if new_company and new_company.idCompany:
            print(f"Company '{new_company.CompanyName}' added successfully with ID {new_company.idCompany}.")
        else:
            print("Error adding company.")


    def start(self) ->None:
        while True:
            self.display_menu()
            self.process_menu_choice()