<div style="text-align: center;">
<img src="docs/assets/fletx.png"/>
</div>

# FletX  

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  
[![Platform](https://img.shields.io/badge/Platform-Flet-blue)](#)  
[![Version](https://img.shields.io/badge/Version-0.1.8-brightgreen)](#)  
[![Downloads](https://static.pepy.tech/badge/fletx)](https://pepy.tech/project/fletx)

FletX is a powerful **routing** and **global state management** library for the Flet framework. It simplifies application development by separating UI and logic while providing intuitive navigation solutions.

---

## ✨ Features  

- **Seamless Routing**: Effortless and dynamic navigation management.  
- **State Management**: Manage complex states with ease.  
- **Logic-UI Separation**: Keep your code clean and maintainable.  
- **Lightweight and Fast**: Designed for performance.  

---

## 📦 Installation  

Add the FletX package to your project:  

```bash
pip install fletx
```

## 🚀 Getting Started
### 🌟 Statefull Counter App Example
**Directory & File Structure**
```bash
📦CounterApp
    ├── main.py
    ├── states
    │   └── main_state.py
    └── views
        ├── counter_view.py
        └── home_view.py
```

**main.py**
````python
import flet as ft
from fletx import Xapp,route
from states.main_state import MainState
from views.home_view import HomeView
from views.counter_view import CounterView

def main(page: ft.Page):
    page.title = "FletX counter example"

    Xapp(
        page=page,
        init_route="/",
        state=MainState,
        routes=[
            route(route="/",view=HomeView),
            route(route="/counter",view=CounterView),
        ]
    )

ft.app(main)
````
**states/main_state.py**
```python
import flet as ft
from fletx import Xstate

class MainState(Xstate):
    def __init__(self, page):
        super().__init__(page)
        
        self.txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(self,e):
        self.txt_number.value = str(int(self.txt_number.value) - 1)
        self.update()

    def plus_click(self,e):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.update()
```
**views/home_view.py**
```python
import flet as ft 
from fletx import Xview

class HomeView(Xview):

    def build(self):
        return ft.View(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("Home View"),
                ft.Text(f"Counts = {self.state.txt_number.value}"),
                ft.ElevatedButton("Go Counter View",on_click=lambda e:self.go("/counter"))
            ]
        )
```
**views/counter_view.py**
```python
import flet as ft 
from fletx import Xview

class CounterView(Xview):

    def build(self):
        return ft.View(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    [
                        ft.IconButton(ft.Icons.REMOVE, on_click=self.state.minus_click),
                        self.state.txt_number,
                        ft.IconButton(ft.Icons.ADD, on_click=self.state.plus_click),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.ElevatedButton("<< Back",on_click=self.back)
            ]
        )
```

<img src="docs/assets/counter.gif"/>

## ❤️ Feedback
Found this repository helpful? Let us know!

- ⭐ Star the [FletX repository](https://github.com/saurabhwadekar/FletX)
- Report issues or suggest improvements in the [Issues section](https://github.com/saurabhwadekar/FletX/issues)
