class EventManager:
    def __init__(self):
        self._listeners = {}

    def on_event(self, event_name: str):
        def decorator(func):
            self._listeners.setdefault(event_name, []).append(func)
            return func
        return decorator

    def trigger(self, event_name: str, *args, **kwargs):
        if event_name in self._listeners:
            for func in self._listeners[event_name]:
                func(*args, **kwargs)

event_manager = EventManager()

def on_event(event_name: str):
    return event_manager.on_event(event_name)
