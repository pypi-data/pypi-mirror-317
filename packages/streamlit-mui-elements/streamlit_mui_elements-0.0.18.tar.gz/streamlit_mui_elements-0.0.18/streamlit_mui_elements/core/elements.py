import json
import time
from streamlit import session_state, rerun

from streamlit_mui_elements.core.exceptions import ElementsFrameError
from streamlit_mui_elements.core.element import Element
from streamlit_mui_elements.core.render import render_component

ELEMENTS_FRAME_KEY = f"{__name__}.elements_frame"
RERUN_COOLDOWN = 0.1
RERUN_EVENT_TYPES = {'file-change', 'filter-change', 'sort-change', 'pagination-change', 'selection-change'}

class ElementsManager:
    def __init__(self, key):
        self.key = f"{ELEMENTS_FRAME_KEY}.{key}"
        self.frame = None
    
    def __enter__(self):
        self.frame = ElementsFrame(self.key)
        session_state[ELEMENTS_FRAME_KEY] = self.frame
        self.frame.capture_children()
        return self.frame
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.frame:
                ui_tree = self.frame.to_dict()
                if ui_tree:
                    self._handle_component(ui_tree)
        except Exception as e:
            raise e
        finally:
            if ELEMENTS_FRAME_KEY in session_state:
                del session_state[ELEMENTS_FRAME_KEY]
    
    def _handle_component(self, ui_tree):
        ui_description = json.dumps(ui_tree)
        component = render_component(data=ui_description, key=self.key, default=None)
        
        if component is not None and component != 0:
            event_key = component.get('key')
            value = component.get('value')
            timestamp = component.get('timestamp')
            event_type = component.get('type')
            
            if event_key and event_key != 'undefined':
                self._update_event_state(event_key, value, timestamp, event_type)
                if self._should_rerun(event_type, event_key, timestamp):
                    self._trigger_rerun(event_key, timestamp)
    
    def _update_event_state(self, event_key, value, timestamp, event_type):
        try:
            if "events" not in session_state:
                session_state.events = {}
            
            if session_state.events.get(event_key, {}).get('timestamp') == timestamp:
                # Only in case of larage files
                if session_state.events[event_key]["type"] == "file-change": 
                    session_state.events[event_key]["value"]["result"] = None
            else:
                session_state.events[event_key] = {
                    "value": value,
                    "timestamp": timestamp,
                    "type": event_type
                }
        except Exception as e:
            print(f"Error updating event state: {str(e)}")
    
    def _should_rerun(self, event_type, event_key, timestamp):
        if not event_type or event_type not in RERUN_EVENT_TYPES:
            return False
            
        last_event = session_state.get('_last_processed_event', {})
        if (last_event.get('key') == event_key and 
            last_event.get('timestamp') == timestamp):
            return False
            
        last_rerun = session_state.get('_last_rerun_time', 0)
        return time.time() - last_rerun >= RERUN_COOLDOWN
    
    def _trigger_rerun(self, event_key, timestamp):
        session_state._last_processed_event = {
            'key': event_key,
            'timestamp': timestamp
        }
        session_state._last_rerun_time = time.time()
        rerun()

def new_element(module, element):
    if ELEMENTS_FRAME_KEY not in session_state:
        raise ElementsFrameError("Cannot create element outside a frame.")
    return Element(session_state[ELEMENTS_FRAME_KEY], module, element)

def get_elements_frame():
    if ELEMENTS_FRAME_KEY not in session_state:
        raise ElementsFrameError("Frame was not created.")
    return session_state[ELEMENTS_FRAME_KEY]

class ElementsFrame:
    __slots__ = ('_children', '_parents', '_key', '_is_saving')

    def __init__(self, key):
        self._children = []
        self._parents = []
        self._key = key
        self._is_saving = False

    def capture_children(self):
        self._parents.append(self._children)
        self._children = []

    def save_children(self, element):
        if self._is_saving:
            raise RuntimeError("Reentrant save_children call detected.")

        if not self._parents:
            raise RuntimeError("save_children called without active context.")

        self._is_saving = True
        captured_children = self._children
        self._children = self._parents.pop()

        # Only process children that haven't been added to a parent yet
        filtered_children = []
        for child in captured_children:
            if not child._is_prop and not child._parent:
                child._parent = element
                filtered_children.append(child)

        if filtered_children:
            element(*filtered_children)

        # Only add the element if it's not a prop and doesn't have a parent
        if not element._is_prop and not element._parent and element not in self._children:
            self._children.append(element)

        captured_children.clear()
        self._is_saving = False

    def is_capturing_children(self):
        return len(self._parents) > 0

    def to_dict(self):
        result = [child.to_dict() for child in self._children]
        return result
