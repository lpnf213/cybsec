import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    def __init__(self, name):
        self.name = name
        self.observer = Observer()
        self.event_handler = self.MyHandler()
        self.observer.schedule(self.event_handler, path='.', recursive=False)
        self.handlers = {}

    def run(self):
        observer_thread = threading.Thread(target=self.observer.start)
        observer_thread.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def add_handler(self, filepath, event_type, handler):
        if filepath not in self.handlers:
            self.handlers[filepath] = {}
        self.handlers[filepath][event_type] = handler

    def get_status(self):
        return self.observer.is_alive()

    def get_monitored_files(self):
        return list(self.handlers.keys())

    def get_name_and_status(self):
        status = "Running" if self.get_status() else "Stopped"
        return f"{self.name}: {status}"

    def __str__(self):
        return self.get_name_and_status()

    class MyHandler(FileSystemEventHandler):
        def __init__(self):
            self.watcher = None

        def set_watcher(self, watcher):
            self.watcher = watcher

        def dispatch(self, event):
            if not event.is_directory:
                filepath = event.src_path
                event_type = event.event_type
                if filepath in self.watcher.handlers and event_type in self.watcher.handlers[filepath]:
                    self.watcher.handlers[filepath][event_type](event)
