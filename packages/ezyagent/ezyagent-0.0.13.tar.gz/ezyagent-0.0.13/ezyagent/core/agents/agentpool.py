from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Union

from .._types._huggingface import HFModelType
from ...customs.main import HFAgent


@dataclass
class AgentTask:
    query: str
    system_prompt: str = field(default="")
    model: HFModelType = field(default="huggingface:Qwen/Qwen2.5-72B-Instruct")
    model_args: dict = field(default_factory=lambda: {"temperature": 0})


class AgentPool:
    def __init__(self,
                 model: Optional[HFModelType] = None,
                 system_prompt: Optional[str] = None,
                 max_concurrent: int = 10,
                 agent_model=None):
        self._agents = {}
        self._executor = ThreadPoolExecutor(max_workers=max_concurrent)
        self.agent_pool_model = model
        self.agent_pool_system_prompt = system_prompt
        self.agent_model = agent_model

    def _controlled_query(self, task: AgentTask):
        agent_key = f"{task.model}_{task.system_prompt}"
        if agent_key not in self._agents:
            # Create new agent instance
            agent = self.agent_model or HFAgent(self.agent_pool_model or task.model, **task.model_args)
            self._agents[agent_key] = agent(self.agent_pool_system_prompt or task.system_prompt)

        return self._agents[agent_key](task.query)

    def _process_batch(self, tasks: List[Union[AgentTask, str]]) -> list:
        # Convert string tasks to AgentTask objects
        tasks = [AgentTask(query=t) if isinstance(t, str) else t for t in tasks]

        # Use ThreadPoolExecutor to run queries concurrently
        results = list(self._executor.map(self._controlled_query, tasks))
        return results

    def run(self, tasks: Union[List[AgentTask], List[str]]) -> list:
        """
        Process a batch of tasks and return results.
        This method runs queries concurrently using threads.
        """
        try:
            return self._process_batch(tasks)
        except Exception as e:
            return [f"Error: {str(e)}"] * len(tasks)

    def __del__(self):
        """Cleanup the ThreadPoolExecutor on deletion"""
        self._executor.shutdown(wait=False)


# Usage example:
if __name__ == "__main__":
    agents = AgentPool()
    results = agents.run(["2+4?", "what is 4-2?"])
    print(results)