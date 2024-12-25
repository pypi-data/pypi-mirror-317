from flet import Page
from typing import Callable

class Xstate:
    def __init__(self,page:Page):
        self.page = page

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
    
    def inject_in_state(self,func:Callable):
            self.__setattr__( func.__name__, func)
