class Element:
    __slots__ = ("_frame", "_module", "_element", "_props", "_children", 
                 "_is_context_parent", "_registered", "_is_prop", "_parent")

    def __init__(self, frame, module, element):
        self._frame = frame
        self._module = module
        self._element = element
        self._props = {}
        self._children = []
        self._is_context_parent = False
        self._registered = False
        self._is_prop = False
        self._parent = None

    def __enter__(self):
        """Enter a new context for this element."""
        self._is_context_parent = True
        self._frame.capture_children()
        return self

    def __exit__(self, *_):
        """Exit the context and finalize this element."""
        self._frame.save_children(self)

    def __call__(self, *children, **props):
        """Add children and props to this element."""
        self._props.update(props)
        
        # Process nested elements in props first
        for key, value in props.items():
            if isinstance(value, dict):
                self._process_nested_dict(value)
            elif isinstance(value, Element):
                value._is_prop = True
                value._registered = True  # Prevent registration as standalone

        # Process direct children
        for child in children:
            if isinstance(child, Element):
                if not child._is_prop:  # Only add non-prop children
                    child._parent = self
                    self._children.append(child)
            else:
                self._children.append(child)

        # Only register if this is a root element
        if (self._frame.is_capturing_children() and 
            not self._is_context_parent and 
            not self._registered and 
            not self._is_prop and 
            not self._parent):
            self._frame._children.append(self)
            self._registered = True

        return self

    def _process_nested_dict(self, d):
        """Process nested dictionaries to mark Elements as props."""
        for key, value in d.items():
            if isinstance(value, Element):
                value._is_prop = True
                value._registered = True
            elif isinstance(value, dict):
                self._process_nested_dict(value)
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, dict):
                        self._process_nested_dict(item)
                    elif isinstance(item, Element):
                        item._is_prop = True
                        item._registered = True

    def _mark_nested_props(self, prop_dict):
        """Recursively mark nested Elements in props as prop elements"""
        if isinstance(prop_dict.get('children'), Element):
            prop_dict['children']._is_prop = True
        elif isinstance(prop_dict.get('children'), dict):
            self._mark_nested_props(prop_dict['children'])

    def to_dict(self):
        def convert_value(value):
            if isinstance(value, Element):
                return value.to_dict()
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items()}
            elif isinstance(value, (list, tuple)):
                return [convert_value(v) for v in value]
            elif callable(value):  # Handle functions
                return f"function {value.__name__}" if hasattr(value, "__name__") else "function"
            else:
                return value

        result = {
            "type": self._element,
            "module": self._module,
            "props": convert_value(self._props),
            "children": convert_value(self._children),
        }
        # print(f"Element to_dict: {result}")  # Debugging
        return result
