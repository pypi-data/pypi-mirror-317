import pandas as pd
import streamlit as st
from streamlit_mui_elements.modules.mui import mui  # Changed import statement

def data_grid(df: pd.DataFrame):
    """Create a MUI DataGrid with server-side pagination, sorting, and filtering."""
    
    # Add event tracking state
    if '__last_grid_event' not in st.session_state:
        st.session_state.__last_grid_event = None

    # Add filter state
    if '__grid_filter' not in st.session_state:
        st.session_state.__grid_filter = None
    if '__grid_page' not in st.session_state:
        st.session_state.__grid_page = 0
    if '__grid_page_size' not in st.session_state:
        st.session_state.__grid_page_size = 25
    if '__grid_sort_field' not in st.session_state:
        st.session_state.__grid_sort_field = None
    if '__grid_sort_dir' not in st.session_state:
        st.session_state.__grid_sort_dir = None

    # Create a copy of the dataframe to avoid modifying the original
    processed_df = df.copy()

    # Handle grid events with deduplication
    grid_event = st.session_state.get("events", {}).get("data-grid", {})
    if grid_event:
        current_event = (grid_event.get('type'), str(grid_event.get('value')))
        
        # Only process if event is different from last one
        if current_event != st.session_state.__last_grid_event:
            st.session_state.__last_grid_event = current_event
            
            if grid_event.get('type') == 'filter-change':
                filter_model = grid_event['value']
                st.session_state.__grid_filter = filter_model
                
                # Apply filtering
                if filter_model and filter_model.get('items'):
                    filtered_df = df.copy()
                    for filter_item in filter_model['items']:
                        field = filter_item.get('field')
                        operator = filter_item.get('operator')
                        value = filter_item.get('value')
                        
                        if field and operator == '=':
                            filtered_df = filtered_df[filtered_df[field] == value]
                    
                    st.session_state.__df = filtered_df
                    st.session_state.__grid_page = 0
                else:
                    st.session_state.__df = df.copy()
                    st.session_state.__grid_page = 0

            elif grid_event.get('type') == 'sort-change':
                sort_model = grid_event['value']
                if sort_model and len(sort_model) > 0:
                    st.session_state.__grid_sort_field = sort_model[0].get('field')
                    st.session_state.__grid_sort_dir = sort_model[0].get('sort')
                    # Apply sorting
                    if st.session_state.__grid_sort_field and st.session_state.__grid_sort_dir:
                        sorted_df = df.copy()
                        st.session_state.__df = sorted_df.sort_values(
                            by=st.session_state.__grid_sort_field,
                            ascending=(st.session_state.__grid_sort_dir == 'asc')
                        )
                        st.session_state.__grid_page = 0

            elif grid_event.get('type') == 'pagination-change':
                st.session_state.__grid_page = grid_event['value'].get('page', 0)
                st.session_state.__grid_page_size = grid_event['value'].get('pageSize', 25)

    # Apply pagination inside the pagination event
    row_count = 0
    start_idx = st.session_state.__grid_page * st.session_state.__grid_page_size
    end_idx = start_idx + st.session_state.__grid_page_size
    if '__df' in st.session_state:
        processed_df = st.session_state.__df.iloc[start_idx:end_idx]
        row_count = len(st.session_state.__df)
    else:
        processed_df = df.iloc[start_idx:end_idx]
        row_count = len(df)

    # Convert processed DataFrame to rows format
    rows = processed_df.to_dict('records')
    for i, row in enumerate(rows):
        row['id'] = i + start_idx

    # Create columns configuration with types
    columns = []
    for col in df.columns:
        column_def = {
            'field': col, 
            'headerName': col.title(), 
            'width': 100
        }
        
        # Set column type based on dtype
        if pd.api.types.is_numeric_dtype(df[col].dtype):
            column_def['type'] = 'number'
        elif pd.api.types.is_datetime64_any_dtype(df[col].dtype):
            column_def['type'] = 'dateTime'
        elif pd.api.types.is_bool_dtype(df[col].dtype):
            column_def['type'] = 'boolean'
            
        columns.append(column_def)

    if len(columns) > 2000:
        return mui.Typography(
            "Too many columns ",
            sx={"textAlign": "center"}
        )
    else:
        return mui.DataGrid(
            id="data-grid",
            rows=rows,
            columns=columns,
            checkboxSelection=True,
            paginationMode="server",
            sortingMode="server",
            filterMode="server",
            rowCount=row_count,
            pageSizeOptions=[5, 10, 25, 50],
            page=st.session_state.__grid_page,
            pageSize=st.session_state.__grid_page_size,
            initialState={
                "pagination": {
                    "paginationModel": {
                        "pageSize": st.session_state.__grid_page_size,
                        "page": st.session_state.__grid_page
                    }
                }
            }
        )
