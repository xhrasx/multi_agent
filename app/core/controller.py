"""
主调度控制器
"""
import app.tools
import time


class AgentController:

    def __init__(self, reasoner, executor, reflector, memory):
        self.reasoner = reasoner
        self.executor = executor
        self.reflector = reflector
        self.memory = memory

    def run(self, goal: str, max_steps: int = 5):
        steps_log = []
        llm_calls = []
        total_tokens = 0

        print("=== Agent Start ===")
        print(f"Goal: {goal}")
        self.memory.add("goal", goal)

        for step in range(max_steps):
            print(f"\n--- Step {step + 1} ---")

            # 1️⃣ LLM 推理
            result = self.reasoner.reason(goal, self.memory)
            if isinstance(result, tuple):
                action, meta = result
            else:
                action = result
                meta = {}

            llm_calls.append({
                "call": step + 1,
                "model": meta.get("model"),
                "latency": meta.get("latency_seconds"),
                "tokens": meta.get("total_tokens"),
                "finish_reason": meta.get("finish_reason"),
            })
            total_tokens += (meta.get("total_tokens") or 0)

            step_record = {
                "step": step + 1,
                "agent": "Reasoner",
                "reasoning": action,
                "model": meta.get("model"),
                "latency": meta.get("latency_seconds"),
            }

            classified_tool = action.get("tool", "")
            print(f"  📋 分类: type={action['type']}, tool={classified_tool}")

            # ====== finish ======
            if action["type"] == "finish":
                final_answer = action.get("output", action.get("input", ""))
                print(f"  ✅ 直接回答: {final_answer}")
                step_record["observation"] = final_answer
                steps_log.append(step_record)

                return {
                    "query": goal,
                    "classified_tool": "direct_answer",
                    "steps": steps_log,
                    "final": final_answer,
                    "metadata": {
                        "total_steps": len(steps_log),
                        "total_tokens_used": total_tokens,
                        "llm_calls": llm_calls,
                    }
                }

            # 2️⃣ 执行工具
            tool_start = time.time()
            observation = self.executor.execute(action)
            tool_elapsed = round(time.time() - tool_start, 3)

            step_record["tool"] = classified_tool
            step_record["tool_input"] = action.get("input", "")
            step_record["observation"] = observation
            step_record["tool_latency"] = tool_elapsed
            steps_log.append(step_record)

            print(f"  📦 结果: {observation[:200]}")

            # 3️⃣ 存储
            self.memory.add("observation", observation)

            # 4️⃣ 反思
            self.reflector.reflect(self.memory)

            return {
                "query": goal,
                "classified_tool": classified_tool,
                "steps": steps_log,
                "final": observation,
                "metadata": {
                    "total_steps": len(steps_log),
                    "total_tokens_used": total_tokens,
                    "llm_calls": llm_calls,
                }
            }

        return {
            "query": goal,
            "classified_tool": "timeout",
            "steps": steps_log,
            "final": "未完成目标",
            "metadata": {
                "total_steps": len(steps_log),
                "total_tokens_used": total_tokens,
                "llm_calls": llm_calls,
            }
        }