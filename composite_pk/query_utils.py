class CompositePrimaryKeyDeferredAttribute(object):
    def __init__(self, *attrs: str):
        self.attrs = attrs

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        return tuple(
            getattr(instance, attr)
            for attr in self.attrs
        )

    def __set__(self, instance, value):
        # ignore
        pass
