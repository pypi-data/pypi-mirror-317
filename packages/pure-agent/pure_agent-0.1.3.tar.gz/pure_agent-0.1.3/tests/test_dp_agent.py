from pure_agent import *

class MyDPAgent(BaseAgent):
    @append_msg('msgs', return_async_task=True)
    def greeting(self, sys_name, prompt):
        with RoleCtx('system'):
            yield f"You are a helpful assistant, your name is {sys_name}."
        with RoleCtx('user'):
            yield prompt

sys_names = ['pbot0', 'pbot1']
prompts = ['who are u?', 'who are u?']
with MultiThreadExecutor(10, '.cache') as pool:
    for i in range(len(sys_names)):
        agent = MyDPAgent(client_config='config.yaml')
        task = agent.greeting(sys_names[i], prompts[i])
        # print(pretty_print_nested(msgs))
        pool.submit(task)

