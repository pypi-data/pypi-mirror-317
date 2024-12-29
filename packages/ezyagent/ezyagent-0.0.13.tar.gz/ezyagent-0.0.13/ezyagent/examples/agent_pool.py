from ezyagent import AgentPool,AgentTask

pool = AgentPool()
print(pool.run(["what is 2+3"]))
print(pool.run(["what is 2+3","what is 4+5?"]))
print(pool.run([AgentTask(system_prompt="your name is adam",
                          query="what is your name")]))
print(pool.run([AgentTask(system_prompt="your name is bob",
                          query="what is your name",
                          model="huggingface:01-ai/Yi-1.5-34B-Chat")]))