import json

class Campaign_Category():
    def __init__(self) ->None:
        self.idCampaign_Category:int = 0
        self.Campaign_CategoryName:str = ""
        
    
    def __str__(self) ->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()
    
    def to_json(self)->str:
        campaign_category_dict = {}
        campaign_category_dict['idCampaign_Category'] = self.idCampaign_Category
        campaign_category_dict['Campaign_CategoryName'] = self.Campaign_CategoryName
        return json.dumps(campaign_category_dict)