import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  User,
  ChevronDown,
  ChevronRight,
  Cpu,
  Clock,
  Zap,
} from "lucide-react";
import StepCard, { getToolIcon } from "./StepCard";

export default function ChatMessage({ message }) {
  const [showChain, setShowChain] = useState(false);
  const isUser = message.role === "user";
  const data = message.data;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-3 ${isUser ? "flex-row-reverse" : ""}`}
    >
      {/* 头像 */}
      <div
        className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isUser
            ? "bg-blue-600"
            : "bg-gradient-to-br from-purple-600 to-indigo-600"
        }`}
      >
        {isUser ? (
          <User className="w-4 h-4 text-white" />
        ) : (
          <Bot className="w-4 h-4 text-white" />
        )}
      </div>

      {/* 消息体 */}
      <div className={`max-w-2xl flex flex-col ${isUser ? "items-end" : "items-start"}`}>
        {isUser ? (
          <div className="bg-blue-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-md text-sm">
            {message.content}
          </div>
        ) : (
          <div className="space-y-2 w-full">
            {/* 回答文本 */}
            <div className="bg-slate-800 border border-slate-700 text-slate-100 px-4 py-3 rounded-2xl rounded-tl-md text-sm whitespace-pre-wrap">
              {message.content}
            </div>

            {/* 元数据 + 推理链路 */}
            {data && (
              <div className="space-y-2">
                {/* 徽章 */}
                <div className="flex flex-wrap gap-3 px-1">
                  {data.classified_tool && (
                    <Badge
                      icon={getToolIcon(data.classified_tool)}
                      value={data.classified_tool}
                      color="text-emerald-400"
                    />
                  )}
                  <Badge
                    icon={Cpu}
                    label="模型"
                    value={data.metadata?.model || "—"}
                    color="text-purple-400"
                  />
                  <Badge
                    icon={Clock}
                    label="耗时"
                    value={`${data.metadata?.total_latency_seconds || 0}s`}
                    color="text-amber-400"
                  />
                  <Badge
                    icon={Zap}
                    label="Tokens"
                    value={data.metadata?.total_tokens_used || 0}
                    color="text-sky-400"
                  />
                </div>

                {/* 展开推理链路 */}
                <button
                  onClick={() => setShowChain(!showChain)}
                  className="flex items-center gap-1.5 text-xs text-indigo-400 
                             hover:text-indigo-300 transition-colors px-1"
                >
                  {showChain ? (
                    <ChevronDown className="w-3.5 h-3.5" />
                  ) : (
                    <ChevronRight className="w-3.5 h-3.5" />
                  )}
                  查看推理链路（{data.steps?.length || 0} 步）
                </button>

                <AnimatePresence>
                  {showChain && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="space-y-2 overflow-hidden"
                    >
                      {data.steps?.map((step, i) => (
                        <StepCard key={i} step={step} index={i} />
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}

function Badge({ icon: Icon, label, value, color }) {
  return (
    <div className={`flex items-center gap-1.5 text-xs ${color || "text-slate-400"}`}>
      <Icon className="w-3.5 h-3.5" />
      {label && <span className="text-slate-500">{label}</span>}
      <span className="font-mono">{value}</span>
    </div>
  );
}