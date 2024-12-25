from typing import Optional
from flet.core.adaptive_control import AdaptiveControl
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet import ProgressRing

class IsLoading(ConstrainedControl, AdaptiveControl):
    def __init__(
        self,
        is_loading:bool = True,
        loading_control:Optional[Control] = None,
        loaded_control:Optional[Control] = None,
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

        if loading_control == None:
            self.loading_control = ProgressRing(visible=True)
        else:
            self.loading_control = loading_control

        self.loaded_control = loaded_control
        self.is_loading = is_loading

        if self.is_loading:
            self.__content = self.loading_control
        else:
            self.__content = self.loaded_control

    def _get_control_name(self):
        return "container"
    
    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    # is_loading
    @property
    def is_loading(self) -> bool:
        return self._get_attr("is_loading")

    @is_loading.setter
    def is_loading(self, value: Optional[bool]):
        self._set_attr("is_loading", value)
        if self.is_loading:
            self.__content = self.loading_control
        else:
            self.__content = self.loaded_control