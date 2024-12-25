from flet import Page,View,Text
from .xstate import Xstate
from .xparams import Xparams

class Xview:
    def __init__(self,page:Page,state:Xstate,params:Xparams):
        self.page = page
        self.state = state
        self.__params = params
        self.init()

    def init(self):
        ...

    def get_param(self,var:str):
        return self.__params.get(var)
    
    def get_all_param(self):
        return self.__params.get_all()

    def update(self):
        self.page.update()

    async def update_async(self):
        self.page.update_async()

    def go(self,route):
        self.page.go(route=route)
    
    def pop_go(self,route):
        if self.page.views.__len__()>=1:
            self.page.views.pop()
            self.page.go(route=route)
    
    def pop_all_go(self,route):
            self.page.views.clear()
            self.page.go(route=route)

    def back(self,*args, **kwargs):
        if self.page.views.__len__()>1:
            pre_r = self.page.views[-2].route
            self.page.views.pop()
            self.page.views.pop()
            self.page.go(pre_r)
            
    def onBuildComplete(self):
        ...
            
    def build(self):
        return View(
            controls=[
                Text("Xview")
            ]
        )

    