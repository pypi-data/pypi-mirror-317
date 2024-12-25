from pure_agent import BaseAgent, RoleCtx, append_msg

class MyAgent(BaseAgent):
    @append_msg()
    def greeting(self, sys_name, prompt):
        with RoleCtx('system'):
            yield f"You are a helpful assistant, your name is {sys_name}."
        with RoleCtx('user'):
            yield prompt

agent = MyAgent(client_config='config.yaml')
response = agent.greeting('agent0', 'who are u?')
print(response)
