import threading

from pure_agent.client import OpenAIClient

class BaseAgent:
    def __init__(self, client_config):
        self.msgs = []
        self.cur_task = None
        self.client = OpenAIClient(client_config)

    def gen(self):
        return self.client.request(self.msgs)
