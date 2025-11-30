import json

class Channel_Category():
    def __init__(self) ->None:
        self.idChannel_Category:str = ""
        self.Channel_CategoryName:str = ""
        
    
    def __str__(self) ->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()
    
    def to_json(self)->str:
        channel_dict = {}
        channel_dict['idChannel_Category'] = self.idChannel_Category
        channel_dict['Channel_CategoryName'] = self.Channel_CategoryName
        return json.dumps(channel_dict)