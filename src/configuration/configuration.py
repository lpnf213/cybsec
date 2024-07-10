"""
Singleton Pattern for Configuration: Use the Singleton pattern to manage configuration 
settings for your application. 
This ensures that there's only one instance of the configuration object throughout 
the application's lifecycle, 
making it easy to access and modify settings from different parts of the code.

Observer: This will be your OptionManager.
It will implement an update method that gets called by the 
subject whenever there's a change in configurations.
"""
from typing import List

from option.option import Option
from utils.utils import display_dict_as_table

class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers: List[Option] = [] # type: ignore
            cls._instance._config_data = {}  # Your configuration data goes here
        return cls._instance

    def set_configuration(self, key, value):
        self._config_data[key] = value
        self.notify_observers()

    def get_configuration(self, key):
        return self._config_data.get(key)

    def subscribe(self, observer: Option):
        self._observers.append(observer)

    def unsubscribe(self, observer: Option):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update_by_rules(self)

    def show_configurations(self):
        display_dict_as_table(data = self._config_data,
                              headers = ['Name', 'Value'],
                              title = 'Configurations')
