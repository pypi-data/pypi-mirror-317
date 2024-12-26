# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PdfViewer(Component):
    """A PdfViewer component.
Component description

Keyword arguments:

- id (string; required):
    The ID of the component   Unique ID to identify this component in
    Dash callbacks.

- url (string; required):
    The URL of the PDF file."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_pdf_highlighter'
    _type = 'PdfViewer'
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, url=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'url']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['id', 'url']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(PdfViewer, self).__init__(**args)
