from typing import Optional
from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref

class Switch(ConstrainedControl, AdaptiveControl):
    def __init__(
        self,
        default:str = None,
        controls:Optional[dict] = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.controls_dict = controls

        if self.controls_dict != None:
            if default == None:
                if len(self.controls_dict)> 0:
                    self.active = next(iter(self.controls_dict.keys()))
                    self.__content = self.controls_dict[self.active]
                else:
                    self.__content = None
                    self.active = None
            else:
                self.__content = self.controls_dict[default]
                self.active = default
        else:
            self.__content = None
            self.active = None

    def _get_control_name(self):
        return "container"
    
    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # active
    @property
    def active(self) -> str:
        return self._get_attr("active")

    @active.setter
    def active(self, value: Optional[str]):
        if value in self.controls_dict.keys():
            self._set_attr("active", value)
            self.__content = self.controls_dict[value]
        # raise KeyError(f"Switch: The key '{value}' is not available.")