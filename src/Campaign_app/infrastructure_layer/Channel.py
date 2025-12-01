import json
from campaign_app.infrastructure_layer.channel_category import Channel_Category

class Channel():

    def __init__(self) ->None:
        self.idChannel:int = 0
        self.ChannelName:str = ""
        self.idChannel_Category:int = 0
    
    def __str__(self) ->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()
    
    def to_json(self)->str:
        channel_dict = {}
        channel_dict['idChannel'] = self.idChannel
        channel_dict['ChannelName'] = self.ChannelName
        channel_dict['idChannel_Category'] = self.idChannel_Category
        return json.dumps(channel_dict)