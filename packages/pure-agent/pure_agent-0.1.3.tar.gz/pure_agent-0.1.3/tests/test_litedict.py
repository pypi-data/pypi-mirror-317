from pure_agent import LiteDict

config={'env': {'api_key': 123}, 'infer_params': {'tempurature': 0.8}, 'tags': ['yaml', 'example', 'configuration']}

dct = LiteDict(config)
print(dct)
print(dct.env)
print(dct.env.api_key)
print(dct.infer_params.get('tags', []))
# print(dct.infer_params.tags)
# print(dct.non_existent.key)
