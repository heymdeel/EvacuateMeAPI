from flask import Blueprint
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def add_app_url_map_converter(self, func, name=None):
    def register_converter(state):
        state.app.url_map.converters[name or func.__name__] = func
    self.record_once(register_converter)

Blueprint.add_app_url_map_converter = add_app_url_map_converter
