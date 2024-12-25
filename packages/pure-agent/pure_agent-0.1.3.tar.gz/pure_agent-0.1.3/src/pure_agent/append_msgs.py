import threading

from pure_agent.tasks import Task
from pure_agent.utils import compute_unique_hash

_local = threading.local()

class RoleCtx:
    def __init__(self, role):
        assert role in ['system', 'user', 'assistant'], 'only supports system/user/assistant'
        self.role = role

    def __enter__(self):
        _local.role = self.role

    def __exit__(self, exc_type, exc_value, traceback):
        del _local.role

def append_msg(attribute_name='msgs', return_async_task=False):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            messages = getattr(self, attribute_name, None)
            gen = func(self, *args, **kwargs)
            for content in gen:
                role = getattr(_local, 'role', 'unknown')
                messages.append({'role': role, 'content': content})

            client = getattr(self, 'client', None)
            if client is None:
                raise ValueError('client is None')
            if return_async_task:
                # FIXME msg + req_params
                task = Task(client.request, {'msgs': messages}, compute_unique_hash(messages))
                setattr(self, 'cur_task', task)
                return task
            else:
                return self.gen()
        return wrapper
    return decorator
