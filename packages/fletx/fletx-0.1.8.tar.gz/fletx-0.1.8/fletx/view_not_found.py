import flet as ft 
from .xview import Xview

class NotFoundView(Xview):
    def build(self):
        return ft.View(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("404 View Not Found",size=30),
                ft.ElevatedButton(text="<< Back",on_click=self.back)
                
            ]
        )