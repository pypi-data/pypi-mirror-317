from streamlit_mui_elements.core.elements import new_element


class MUIIcons:
    """MUI Icons (https://mui.com/components/material-icons)"""

    def __getattr__(self, element):
        return new_element("muiIcons", element)

    def __getitem__(self, element):
        return new_element("muiIcons", element)


class MUILab:
    """MUI Lab (https://mui.com)"""

    def __getattr__(self, element):
        return new_element("muiLab", element)

    def __getitem__(self, element):
        return new_element("muiLab", element)
    

class MUI:
    """MUI Elements (https://mui.com)"""

    __slots__ = ("_icon", "_lab")  # Remove _plot from slots since we're not using it

    def __init__(self):
        self._icon = MUIIcons()
        self._lab = MUILab()

    @property
    def icon(self):
        return self._icon

    @property
    def lab(self):
        return self._lab

    def DataGrid(self, **kwargs):
        """Convenience method for creating DataGrid component"""
        return new_element("muiElements", "DataGrid")(**kwargs)

    def __getattr__(self, element):
        return new_element("muiElements", element)

    def __getitem__(self, element):
        return new_element("muiElements", element)

# Create a single instance to be imported by other modules
mui = MUI()

# Export the mui instance
__all__ = ['mui']
