from flet import Page
from .xstate import Xstate
from .xparams import Xparams
from repath import match

class Xmiddleware:
    def __init__(self,page:Page,state:Xstate,params:Xparams):
        self.page = page
        self.state = state
        self.__params = params
        self.init()

    def init(self)->None:
        ...

    def middleware(self)->None:
        ...

    def get_param(self,var:str):
        return self.__params.get(var)
    
    def get_all_param(self)->dict:
        return self.__params.get_all()
    
    def get_curunt_route(self)->str:
        return self.page.route 
    
    def redirect_route(self,route)->None:
        self.page.route = route

    def is_route_match(self,route)->bool:
        if match(route, self.page.route):
            return True
        else:False
    
    def is_route_not_matched(self,route)->bool:
        if match(route, self.page.route):
            return False
        else:True

