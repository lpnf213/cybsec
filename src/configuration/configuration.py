# Configurations Singleton
class Configuration:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._observers = []
            cls._instance._config_data = {}  # Your configuration data goes here
        return cls._instance

    def set_configuration(self, key, value):
        self._config_data[key] = value
        self.notify_observers()

    def get_configuration(self, key):
        return self._config_data.get(key)

    def subscribe(self, observer):
        self._observers.append(observer)

    def unsubscribe(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()
