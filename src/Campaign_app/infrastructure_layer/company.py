import json

class Company():
    def __init__(self) ->None:
        self.idCompany:int = 0
        self.CompanyName:str = ""
        
    
    def __str__(self) ->str:
        return self.to_json()

    def __repr__(self)->str:
        return self.to_json()
    
    def to_json(self)->str:
        company_dict = {}
        company_dict['idCompany'] = self.idCompany
        company_dict['CompanyName'] = self.CompanyName
        return json.dumps(company_dict)