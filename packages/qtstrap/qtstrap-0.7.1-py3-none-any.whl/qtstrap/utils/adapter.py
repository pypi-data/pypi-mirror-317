from qtstrap import QObject
from qtpy.QtCore import SIGNAL

try:
    from qtstrap import SignalInstance
except:
    from qtstrap import pyqtBoundSignal as SignalInstance


class Adapter(QObject):
    """A signal adapter that helps create disposable connections between objects.

    A signal-based interface can be defined using an Adapter.

    Passing an existing Adapter when creating a new Adapter will automatically link all of
    the existing adapter's signals to the same-named signals on the new Adapter.

    This will allow some other object to connect to these signals for whatever purpose, and
    then simply delete the new Adapter object when it now longer wants to recieve signals.

    Technically, Qt Signals already have a .disconnect() method, but I've never gotten it work
    reliably. Using an Adapter essentially gives you a nuclear .disconnect().
    """

    def __init__(self, other=None):
        super().__init__()
        self._other = other
        if other is None:
            self._original = True
            return
        self._original = False

        for name in self._get_signals(other):
            getattr(other, name).connect(getattr(self, name).emit)

    def _get_signals(self, obj):
        signals = []
        for name in dir(obj):
            if name not in dir(QObject):
                if isinstance(getattr(obj, name), SignalInstance):
                    signals.append(name)
        return signals

    def __str__(self):
        s = ''
        if not self._original:
            s += 'inherited '
        s += f"{self.__class__.__name__}(Adapter): <{', '.join(self._get_signals(self))}>"
        return s

    def __call__(self):
        return self.__class__(self)

    def adapter(self):
        return self.__class__(self)

    def kill(self):
        if self._other:
            for name in self._get_signals(self._other):
                self.disconnect(self._other, SIGNAL(name), getattr(self, name).emit)
            #     # TODO: this might not be safe
            #     getattr(self._other, name).disconnect(getattr(self, name).emit)


if __name__ == '__main__':
    from qtstrap import Signal

    class SignalInterface(Adapter):
        sig = Signal()

    original = SignalInterface()
    original.sig.connect(lambda: print('original'))

    copy = original.adapter()
    copy.sig.connect(lambda: print('copy'))

    original.sig.emit()

    copy.kill()

    original.sig.emit()

    print(original)
    print(copy)
