import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronDown,
  ChevronRight,
  Wrench,
  Brain,
  Zap,
  Calculator,
  Globe,
  Cloud,
  CalendarDays,
  Search,
  Sparkles,
  Clock,
} from "lucide-react";

const TOOL_ICONS = {
  calculator: Calculator,
  translator: Globe,
  weather: Cloud,
  datetime: CalendarDays,
  search: Search,
  direct_answer: Sparkles,
  timeout: Clock,
};

export function getToolIcon(toolName) {
  return TOOL_ICONS[toolName] || Wrench;
}

export default function StepCard({ step, index }) {
  const [expanded, setExpanded] = useState(true);
  const ToolIcon = TOOL_ICONS[step.tool] || Wrench;
  const isToolCall = step.reasoning?.type === "tool";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.12 }}
      className="border border-slate-700 rounded-lg overflow-hidden bg-slate-800/60"
    >
      {/* 折叠标题 */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-2 px-3 py-2 text-left 
                   hover:bg-slate-700/40 transition-colors"
      >
        {expanded ? (
          <ChevronDown className="w-4 h-4 text-slate-400 shrink-0" />
        ) : (
          <ChevronRight className="w-4 h-4 text-slate-400 shrink-0" />
        )}

        <span className="bg-indigo-500/20 text-indigo-300 text-xs font-mono px-2 py-0.5 rounded">
          Step {step.step}
        </span>
        <Brain className="w-3.5 h-3.5 text-purple-400 shrink-0" />
        <span className="text-xs text-slate-300">{step.agent}</span>

        {isToolCall && (
          <>
            <span className="text-slate-600">→</span>
            <ToolIcon className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
            <span className="text-xs text-emerald-300 font-mono">{step.tool}</span>
          </>
        )}

        {step.latency && (
          <span className="text-xs text-slate-500 ml-auto shrink-0">{step.latency}s</span>
        )}
      </button>

      {/* 展开内容 */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-3 pb-3 space-y-2 border-t border-slate-700">
              {/* LLM 推理 */}
              <div className="mt-2">
                <p className="text-xs text-slate-500 mb-1 flex items-center gap-1">
                  <Brain className="w-3 h-3" /> LLM 推理
                </p>
                <pre className="text-xs bg-slate-900 rounded p-2 text-slate-300 overflow-x-auto whitespace-pre-wrap break-all">
                  {JSON.stringify(step.reasoning, null, 2)}
                </pre>
              </div>

              {/* 工具调用 */}
              {isToolCall && (
                <div>
                  <p className="text-xs text-slate-500 mb-1 flex items-center gap-1">
                    <Wrench className="w-3 h-3" /> 工具调用
                  </p>
                  <div className="flex items-center gap-2 bg-slate-900 rounded p-2">
                    <ToolIcon className="w-4 h-4 text-emerald-400" />
                    <code className="text-xs text-emerald-300">
                      {step.tool}(<span className="text-amber-300">{step.tool_input}</span>)
                    </code>
                    {step.tool_latency !== undefined && (
                      <span className="text-xs text-slate-500 ml-auto">{step.tool_latency}s</span>
                    )}
                  </div>
                </div>
              )}

              {/* 结果 */}
              <div>
                <p className="text-xs text-slate-500 mb-1 flex items-center gap-1">
                  <Zap className="w-3 h-3" /> 结果
                </p>
                <div className="bg-slate-900 rounded p-2 text-sm text-slate-200 whitespace-pre-wrap break-words">
                  {step.observation}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}