from typing import List, Optional, Any, Dict, Union, Iterable

from litellm import api_key
from llama_index.core.agent import ReActAgent as LlamaIndexReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.llms.ollama import Ollama
from llama_index.core.tools import BaseTool, FunctionTool
from ..base import BaseAgent,Tool,AgentResult
from openai.types.chat import ChatCompletionMessageParam
from openai import NotGiven, NOT_GIVEN


class ReactAgent(BaseAgent):
    """ReactAgent that combines BaseAgent with LlamaIndex's ReActAgent functionality."""

    def __init__(
        self,
        model: str = "openai:gpt-4-turbo-preview",
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        log_level: str | None = None,
        verbose: bool = False,
        **kwargs: Any
    ):
        """Initialize the ReactAgent."""
        self.provider = self._get_llama_index_llm_provider(model,api_key,
                                                           base_url)
        super().__init__(
            model_name=model,
            provider=self.provider,
            api_key=api_key,
            base_url=base_url,
            log_level=log_level,
            **kwargs
        )
        self.model= self._get_model(model)
        self.verbose = verbose
        self._llama_agent = None
        self._llama_tools = []
        self._setup_llama_agent()


    def _setup_llama_agent(self) -> None:
        """Setup LlamaIndex ReactAgent with current tools."""
        if not self._llama_agent:
            # Convert our tools to LlamaIndex tools
            self._llama_tools = []
            for tool_name, tool in self.tools.items():
                llama_tool = FunctionTool.from_defaults(
                    fn=tool.function,
                    name=tool_name,
                    description=tool.description
                )
                self._llama_tools.append(llama_tool)


            # Create LlamaIndex ReactAgent
            self._llama_agent = LlamaIndexReActAgent.from_tools(
                tools=self._llama_tools,
                llm=self.provider,
                verbose=self.verbose
            )

    def _get_llama_index_llm_provider(self,model:str,
                                      api_key: Optional[str] = None,
                                      base_url: Optional[str] = None):
        _provider = OpenAI if 'openapi' in model else Ollama
        model = self._get_model(model)
        return _provider(
            model=model,
            api_key=api_key,
            api_base=base_url
        )

    def chat(
        self,
        messages: Union[Iterable[ChatCompletionMessageParam], str],
        model: Optional[str] = None,
        temperature: Optional[float] | NotGiven = 0,
        **kwargs: Any
    ) -> AgentResult:
        """
        Chat with the ReactAgent using LlamaIndex's reasoning capabilities.

        Args:
            messages: Either a string message or list of chat messages
            model: Optional model override
            temperature: Temperature for response generation
            **kwargs: Additional arguments passed to the underlying API

        Returns:
            AgentResult: The agent's response
        """

        # Convert messages to string if needed
        if isinstance(messages, str):
            query = messages
        else:
            # Take the last user message if multiple messages provided
            for msg in reversed(messages):
                if msg["role"] == "user":
                    query = msg["content"]
                    break
            else:
                raise ValueError("No user message found in the provided messages")

        # Get response from LlamaIndex agent
        response = self._llama_agent.chat(query)

        return AgentResult(
            type='text',
            content=str(response)
        )

    @property
    def available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tools.keys())

    def add_tool(self, tool: Tool) -> None:
        """
        Add a new tool to the agent.

        Args:
            tool: Tool instance to add
        """
        self.tools[tool.name] = tool
        # Reset LlamaIndex agent to rebuild with new tools
        self._llama_agent = None
        self._llama_tools = []

    def remove_tool(self, tool_name: str) -> None:
        """
        Remove a tool from the agent.

        Args:
            tool_name: Name of the tool to remove
        """
        if tool_name in self.tools:
            del self.tools[tool_name]
            # Reset LlamaIndex agent to rebuild without removed tool
            self._llama_agent = None
            self._llama_tools = []

