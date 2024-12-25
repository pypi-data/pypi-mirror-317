class LiteDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self:
            if isinstance(self[key], dict):
                self[key] = LiteDict(self[key])

    def __getitem__(self, key):
        return self.get(key)

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

class ThreadSafeList:
    def __init__(self):
        self.locals = threading.local()

    def _get_list(self):
        if not hasattr(self.locals, 'data'):
            self.locals.data = []
        return self.locals.data

    def append(self, item):
        lst = self._get_list()
        lst.append(item)

    def get_list(self):
        return self._get_list()

    def clear(self):
        self._get_list().clear()

    def __iter__(self):
        return iter(self._get_list())

    def __str__(self):
        return str(self._get_list())

    def __repr__(self):
        return f"ThreadSafeList({self._get_list()})"

def singleton(cls):
    _instance = {}
    _lock = threading.Lock()
    def wrapper(*args, **kwargs):
        if cls not in _instance:
            with _lock:
                if cls not in _instance:
                    _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]
    return wrapper

class LogLevel:
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __repr__(self):
        return f"LogLevel({self.name})"

    def __lt__(self, other):
        if isinstance(other, LogLevel):
            return self.level < other.level
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, LogLevel):
            return self.level <= other.level
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, LogLevel):
            return self.level == other.level
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, LogLevel):
            return self.level != other.level
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, LogLevel):
            return self.level > other.level
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, LogLevel):
            return self.level >= other.level
        return NotImplemented

DEBUG = LogLevel('DEBUG', 10)
INFO = LogLevel('INFO', 20)
WARNING = LogLevel('WARNING', 30)
ERROR = LogLevel('ERROR', 40)
