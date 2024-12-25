import queue
import traceback
import threading

from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor

from pure_agent.cache import LocalCache

@dataclass
class Task:
    func: object
    params: dict
    cache_key: str
    expire: int = None

# FIXME only suit for io-intensive tasks. xpu-intensive tasks need MultiProcessExecutor.
class MultiThreadExecutor:
    def __init__(self, num_workers, cache_dir='.cache'):
        self.num_workers = num_workers
        self.q = queue.Queue()
        self.cache = LocalCache(cache_dir)
        self.write_thread = threading.Thread(target=self.write_thread, args=())
        self.write_thread.start()

        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.is_shutdown = False

    def task_wrapper(self, task):
        def func_wrapper():
            try:
                ret = task.func(**task.params)
                self.q.put((task, ret))
            except Exception as e:
                print(f"Exception in task {task.cache_key}:")
                print(traceback.format_exc())

        return func_wrapper

    def write_thread(self):
        while True:
            ele = self.q.get()
            if ele is None:
                break
            task, ret = ele
            self.cache.set(task.cache_key, ret, task.expire)

    def submit(self, task):
        wrap = self.task_wrapper(task)
        if self.is_shutdown:
            raise RuntimeError("ThreadPool is shutdown, cannot accept new tasks.")
        self.executor.submit(wrap)

    def shutdown(self):
        if not self.is_shutdown:
            self.executor.shutdown(wait=True)
            self.is_shutdown = True
        self.q.put(None)
        self.write_thread.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
