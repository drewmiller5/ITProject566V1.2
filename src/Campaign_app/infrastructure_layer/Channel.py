import json
from campaign_app.infrastructure_layer.channel_category import Channel_Category
from typing import List

class Channel():

    def __init__(self) ->None:
        self.idChannel:int = 0
        self.ChannelName:str = ""
        self.idChannel_Category:int = 0
        self.CategoryName: List[Channel_Category] = []
    
    def __str__(self) ->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()
    
    def to_json(self)->str:
        channel_dict = {}
        channel_dict['idChannel'] = self.idChannel
        channel_dict['ChannelName'] = self.ChannelName
        channel_dict['idChannel_Category'] = self.idChannel_Category
        channel_dict['Category Name'] = []
        

        for item in self.CategoryName:
            channel_dict['Category Name'].append(item.__dict__)

        return json.dumps(channel_dict)
