class QueueEventRegistrar(object):
    """Simple class for handling the registration of event handlers and
    propagation of events to those handlers."""

    def __init__(self, queue):
        self._queue = queue
        self._handlers = []

    def register(self, handler):
        """Registers a handler to receive events."""
        if handler not in self._handlers:
            self._handlers.append(handler)
            handler.on_register(self._queue)

        self.create_proxy_method('on_pop')
        self.create_proxy_method('on_reclaim')
        self.create_proxy_method('on_push')
        self.create_proxy_method('on_complete')
        self.create_proxy_method('on_success')
        self.create_proxy_method('on_error')
        self.create_proxy_method('on_retry')
        self.create_proxy_method('on_expire')
        self.create_proxy_method('on_operation_error')

    def create_proxy_method(self, name):
        def proxy_method(*args, **kwargs):
            for handler in self._handlers:
                if hasattr(handler, name):
                    getattr(handler, name)(*args, **kwargs)
        setattr(self, name, proxy_method)
