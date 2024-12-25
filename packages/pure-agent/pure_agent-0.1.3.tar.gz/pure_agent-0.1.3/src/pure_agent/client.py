import os
import pdb
import yaml
import json
import openai
import hashlib

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from pure_agent.utils import pretty_print_nested
from pure_agent.common import LiteDict, DEBUG, INFO, WARNING, ERROR

# TODO support more via liteLLM

class OpenAIClient:
    def __init__(self, config):
        if os.path.isfile(config):
            with open(config, 'r') as f:
                config = yaml.safe_load(f)
        elif not isinstance(config, dict):
            raise ValueError('use yaml or dict to setup config')
        self.config = LiteDict(config)

        assert self.config.env.api_key is not None, 'api_key is required'
        self.client_params = {'api_key': self.config.env.api_key}
        if self.config.env.base_url is not None:
            self.client_params['base_url'] = self.config.env.base_url
        self.client = OpenAI(**self.client_params)

        self.retry = self.config.get('default_retry', 0)
        self.info_level = self.config.get('info_level', INFO)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _request_openai(self, msgs, **kwargs):
        if self.info_level < INFO:
            print(pretty_print_nested(msgs))
        response = self.client.chat.completions.create(messages=msgs, **kwargs)
        if self.info_level < INFO:
            print(response)
        return response

    def request(self, msgs):
        max_attempts = max(self.retry, 1)
        self._request_openai.retry.stop = stop_after_attempt(max_attempts)
        response = self._request_openai(msgs, **self.config.infer_params)

        return response
