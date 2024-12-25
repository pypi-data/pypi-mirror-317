from streamlit_mui_elements.core.elements import ElementsManager
from streamlit_mui_elements.core.exceptions import *
from streamlit_mui_elements.modules.mui import mui
from streamlit_mui_elements.modules.datagrid import data_grid
from streamlit_mui_elements.modules.file_upload import file_upload
from streamlit_mui_elements.version import __version__

def elements(key: str) -> ElementsManager:
    """Create a Streamlit Elements frame using ElementsManager."""
    return ElementsManager(key)

__all__ = ['elements', 'mui', 'data_grid', 'file_upload', 'handle_csv_upload']

