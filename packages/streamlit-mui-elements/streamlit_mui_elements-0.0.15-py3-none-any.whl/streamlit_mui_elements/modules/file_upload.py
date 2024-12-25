import gc
import io
import base64
import pandas as pd
import streamlit as st
from streamlit_mui_elements.modules.mui import mui
from typing import Union, List

def file_upload(extensions: Union[str, List[str]] = ".csv", multiple: bool = False, key: str = "file_upload"):
    """
    Create a MUI file upload button.
    Returns:
        MUI Button element with file input
    """
    if isinstance(extensions, str):
        extensions = [extensions]
    accept = ",".join(extensions)
    
    # Create UI Element with dynamic button text based on extensions
    button_text = f"Upload {extensions[0].replace('.', '').upper()}" if len(extensions) == 1 else "Upload File"
    return mui.Button(
        button_text,
        variant="contained",
        startIcon=mui.icon.Upload(),
        component="label",
        sx={"mt": 1}
    )(
        mui.Input(
            type="file",
            id=key,
            inputProps={
                "accept": accept,
                "multiple": multiple,
            },
            sx={"display": "none"},
            disableUnderline=True,
        )
    )

def handle_upload(extensions: Union[str, List[str]] = ".csv", key: str = "file_upload"):
    """
    Handle the file upload processing.
    Returns:
        tuple of (DataFrame, filename)
    """
    if isinstance(extensions, str):
        extensions = [extensions]
        
    if key not in st.session_state:
        st.session_state[key] = {
            'last_processed_file': None,
            'file_processed': False,
            'cached_df': None
        }

    df, filename = None, None
    events = st.session_state.get("events", {})
    file_event = events.get(key, {})

    if file_event:
        try:
            file_info = file_event.get('value', {})
            if file_info:
                current_filename = file_info.get('name')
                filename = current_filename

                # Validate file extension
                if not any(current_filename.lower().endswith(ext.lower()) for ext in extensions):
                    st.error(f"Invalid file type. Please upload a file with extension: {', '.join(extensions)}")
                    return None, None

                # Check if we already processed this file
                if current_filename == st.session_state[key]['last_processed_file']:
                    df = st.session_state[key]['cached_df']
                else:
                    file_content = file_info.get('result', None)
                    if file_content:
                        content = base64.b64decode(file_content.split(',')[1])
                        # Handle different file types
                        if current_filename.lower().endswith('.csv'):
                            df = pd.read_csv(io.BytesIO(content))
                        elif current_filename.lower().endswith('.xlsx'):
                            df = pd.read_excel(io.BytesIO(content))
                        st.session_state[key]['last_processed_file'] = current_filename
                        st.session_state[key]['cached_df'] = df
                        st.session_state[key]['file_processed'] = True

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.session_state[key]['file_processed'] = False
            st.session_state[key]['cached_df'] = None

    return df, filename
