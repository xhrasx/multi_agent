"""
主调度系统（核心入口）
"""
import time
from app.core.controller import AgentController
from app.core.executor import ExecutorAgent
from app.core.reflection import ReflectionAgent
from app.core.memory import Memory
from app.core.llm_reasoner import LLMReasoner


class MultiAgentSystem:

    def __init__(self):
        self.reasoner = LLMReasoner()
        self.executor = ExecutorAgent()
        self.memory = Memory()
        self.controller = AgentController(
            reasoner=self.reasoner,
            executor=self.executor,
            reflector=ReflectionAgent(),
            memory=self.memory
        )

    def run(self, user_input: str):
        start_time = time.time()
        result = self.controller.run(user_input)
        total_elapsed = round(time.time() - start_time, 3)

        if isinstance(result, dict):
            if "metadata" not in result:
                result["metadata"] = {}
            result["metadata"]["total_latency_seconds"] = total_elapsed
            result["metadata"]["model"] = self.reasoner.model
            result["metadata"]["available_tools"] = self.executor.list_tools()

        return result