import json
from campaign_app.infrastructure_layer.channel import Channel
from campaign_app.infrastructure_layer.campaign_category import Campaign_Category
from campaign_app.infrastructure_layer.company import Company
from campaign_app.infrastructure_layer.channel_category import Channel_Category
from typing import List

class Campaign():
    
    def __init__(self)->None:
        self.idCampaign:int = 0
        self.Campaign_Name:str = ""
        self.StartDate:str = ""
        self.EndDate:str = ""
        self.idCompany:int = 0
        self.idCampaign_Category:int = 0
        self.Budget:str = ""
        self.Revenue:str = ""
        self.NetProfit:str = ""
        self.channel:List[Channel] = []


    def __str__(self)->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()
    

    def to_json(self)->str:
        campaign_dict = {}
        campaign_dict['idCampaign'] = self.idCampaign
        campaign_dict['Campaign_Name'] = self.Campaign_Name
        campaign_dict['StartDate'] = self.StartDate
        campaign_dict['EndDate'] = self.EndDate
        campaign_dict['idCompany'] = self.idCompany
        campaign_dict['idCampaign_Category'] = self.idCampaign_Category
        campaign_dict['Budget'] = self.Budget
        campaign_dict['Revenue'] = self.Revenue
        campaign_dict['NetProfit'] = self.NetProfit
        campaign_dict['channel'] = []

        for item in self.channel:
            campaign_dict['channel'].append(item.__dict__)

            return json.dumps(campaign_dict)

        